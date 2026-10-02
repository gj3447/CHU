#!/usr/bin/env python3
"""Reproducible, offline-guest CHU VM substrate experiment; JSON on stdout."""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import tarfile
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import RDF, XSD, Graph, Literal, URIRef
from rdflib.namespace import PROV

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.chu/os'
HOST = WORK / 'hosts' / hashlib.sha256(json.dumps(json.loads(
    (ROOT / 'os/inputs.lock.json').read_text())['packages'], sort_keys=True).encode()).hexdigest()[:16]
SHA256 = re.compile(r'[a-f0-9]{64}')
REQUIRED_HOST_PACKAGES = frozenset({'genisoimage', 'qemu-system-x86', 'qemu-utils', 'seabios'})


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def lock():
    manifest = json.loads((ROOT / 'os/inputs.lock.json').read_text())
    validate_lock(manifest)
    return manifest


def validate_lock(manifest):
    """Reject malformed VM inputs before any download, extraction, or boot."""
    if not isinstance(manifest, dict) or manifest.get('schema') != 'chu-vm-inputs/v1':
        raise ValueError('Invalid VM input lock schema')

    def require_spec(spec, fields, label):
        if not isinstance(spec, dict):
            raise ValueError(f'Invalid {label} input')
        for field in fields:
            if not isinstance(spec.get(field), str) or not spec[field]:
                raise ValueError(f'Invalid {label}.{field}')
        if not spec['url'].startswith('https://'):
            raise ValueError(f'Invalid {label}.url')
        if not SHA256.fullmatch(spec['sha256']):
            raise ValueError(f'Invalid {label}.sha256')
        if Path(spec['file']).name != spec['file'] or spec['file'] in {'.', '..'}:
            raise ValueError(f'Invalid {label}.file')

    packages = manifest.get('packages')
    if not isinstance(packages, list) or not packages:
        raise ValueError('Invalid host package inputs')
    names = set()
    for package in packages:
        require_spec(package, ('name', 'version', 'url', 'sha256', 'file'), 'package')
        if package['name'] in names:
            raise ValueError(f"Duplicate host package: {package['name']}")
        names.add(package['name'])
    if not REQUIRED_HOST_PACKAGES <= names:
        raise ValueError('Missing required host package input')

    require_spec(manifest.get('image'), ('url', 'sha256', 'file'), 'image')
    require_spec(manifest.get('node'), ('version', 'url', 'sha256', 'file'), 'node')
    sources = manifest.get('source_artifacts')
    if not isinstance(sources, list) or not sources:
        raise ValueError('Invalid source artifact inputs')
    for source in sources:
        require_spec(source, ('name', 'version', 'url', 'sha256', 'file'), 'source artifact')
    return manifest


def fetch(spec, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if digest(destination) != spec['sha256']:
            raise ValueError(f'Cached checksum mismatch: {destination.name}')
        return destination
    temporary = destination.with_suffix(destination.suffix + '.part')
    try:
        with urllib.request.urlopen(spec['url'], timeout=60) as response:
            with temporary.open('wb') as stream:
                shutil.copyfileobj(response, stream)
        if digest(temporary) != spec['sha256']:
            raise ValueError(f'Download checksum mismatch: {destination.name}')
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def host_env():
    return {**os.environ, 'LD_LIBRARY_PATH': str(HOST / 'usr/lib/x86_64-linux-gnu')}


def command(name, *args):
    return [str(HOST / 'usr/bin' / name), *map(str, args)]


def run(argv):
    return subprocess.run(argv, check=True, capture_output=True, text=True,
                          env=host_env(), timeout=60)


def host_files(directory):
    return {str(p.relative_to(directory)): 'link:' + os.readlink(p) if p.is_symlink() else digest(p)
            for p in sorted(directory.rglob('*'))
            if (p.is_file() or p.is_symlink()) and p.name != 'receipt.json'}


def host_valid():
    receipt = HOST / 'receipt.json'
    return receipt.is_file() and json.loads(receipt.read_text()) == host_files(HOST)


def bootstrap():
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise ValueError('This host tool profile requires Debian 13 Linux x86_64')
    release = Path('/etc/os-release').read_text()
    if not re.search(r'^ID=debian$', release, re.M) or 'VERSION_ID="13"' not in release:
        raise ValueError('Pinned Debian host libraries require Debian 13; port explicitly')
    WORK.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(WORK).free < 1024 ** 3:
        raise ValueError('At least 1 GiB free space is required for bootstrap')
    manifest = lock()
    packages = [fetch(spec, WORK / 'debs' / spec['file']) for spec in manifest['packages']]
    HOST.parent.mkdir(parents=True, exist_ok=True)
    # Each package-set gets a clean extraction, never an overlay over old packages.
    if HOST.exists():
        if not host_valid():
            raise ValueError('Host extraction changed; remove that generated host directory and bootstrap')
    else:
        with TemporaryDirectory(prefix='staging-', dir=HOST.parent) as temporary:
            staging = Path(temporary) / 'host'
            staging.mkdir()
            for package in packages:
                run(['dpkg-deb', '-x', str(package), str(staging)])
            (staging / 'receipt.json').write_text(json.dumps(host_files(staging), sort_keys=True))
            staging.rename(HOST)
    for key in ('image', 'node'):
        fetch(manifest[key], WORK / manifest[key]['file'])
    node = WORK / 'node'
    with tarfile.open(WORK / manifest['node']['file']) as archive:
        prefix = 'node-v' + manifest['node']['version'] + '-linux-x64/'
        for member, output in [('bin/node', node), ('LICENSE', WORK / 'node-LICENSE')]:
            entry = archive.getmember(prefix + member)
            if not entry.isfile():
                raise ValueError('Expected regular Node archive member')
            with archive.extractfile(entry) as stream, output.open('wb') as target:
                shutil.copyfileobj(stream, target)
    node.chmod(0o755)
    return doctor()


def doctor():
    checks = {}
    expected = {'qemu-system-x86_64': 'QEMU emulator version 10.0.13 ',
                'qemu-img': 'qemu-img version 10.0.13 ',
                'genisoimage': 'genisoimage 1.1.11 '}
    for name in expected:
        try:
            flag = '-version' if name == 'genisoimage' else '--version'
            result = run(command(name, flag))
            checks[name] = (result.stdout + result.stderr).splitlines()[0]
        except (OSError, subprocess.SubprocessError, IndexError) as exc:
            checks[name] = str(exc)
    valid = all(checks[name].startswith(prefix) for name, prefix in expected.items())
    valid &= (WORK / 'node').is_file() and (WORK / 'ubuntu.img').is_file()
    extracted = host_valid()
    valid &= extracted
    return {'schema': 'chu-vm-doctor/v1', 'ok': bool(valid), 'host_tools': checks,
            'host_receipt_matches': extracted,
            'kvm_available': os.access('/dev/kvm', os.R_OK | os.W_OK),
            'selected_accelerator': 'tcg', 'guest_network': 'none',
            'hswm': 'NOT_READY', 'scope': 'VM substrate only'}


def sources():
    directory = WORK / 'sources'
    manifest = lock()
    for spec in manifest['source_artifacts']:
        fetch(spec, directory / spec['file'])
    run(['dpkg-deb', '-x', str(directory / 'linux-source.deb'), str(directory / 'ubuntu')])
    archive = directory / 'ubuntu/usr/src/linux-source-6.8.0/linux-source-6.8.0.tar.bz2'
    selected = {}
    with tarfile.open(archive) as source:
        for name in ('init/main.c', 'init/do_mounts.c', 'init/initramfs.c', 'COPYING'):
            member = source.getmember('linux-source-6.8.0/' + name)
            if not member.isfile():
                raise ValueError('Expected regular kernel source member')
            output = directory / ('ubuntu-' + name.replace('/', '-'))
            output.write_bytes(source.extractfile(member).read())
            selected[name] = digest(output)
    return {'ok': True, 'schema': 'chu-source-review/v1', 'selected_sha256': selected,
            'scope': 'Selected Ubuntu GA boot sources, not a full kernel audit or rebuild',
            'versions': manifest['source_artifacts']}


def seed(directory, nonce):
    directory.mkdir()
    for filename in ('guest-probe.mjs', 'chu-probe.service'):
        shutil.copyfile(ROOT / 'os' / filename, directory / filename)
    shutil.copyfile(WORK / 'node', directory / 'node')
    (directory / 'nonce').write_text(nonce + '\n')
    config = {
        'users': [], 'ssh_pwauth': False, 'disable_root': True,
        'ssh_deletekeys': False,
        'runcmd': [
            ['mkdir', '-p', '/mnt/chu-seed', '/opt/chu'],
            ['mount', '-o', 'ro', '/dev/sr0', '/mnt/chu-seed'],
            ['cp', '/mnt/chu-seed/node', '/mnt/chu-seed/guest-probe.mjs',
             '/mnt/chu-seed/nonce', '/opt/chu/'],
            ['chmod', '0755', '/opt/chu/node'],
            ['cp', '/mnt/chu-seed/chu-probe.service', '/etc/systemd/system/'],
            ['systemctl', 'daemon-reload'],
            ['systemctl', 'mask', 'systemd-networkd-wait-online.service'],
            ['systemctl', 'enable', 'chu-probe.service'],
            ['systemctl', '--no-block', 'start', 'chu-probe.service'],
        ],
    }
    (directory / 'user-data').write_text('#cloud-config\n' + json.dumps(config) + '\n')
    (directory / 'meta-data').write_text(json.dumps({'instance-id': nonce,
                                                   'local-hostname': 'chu-vm-probe'}))
    (directory / 'network-config').write_text('version: 2\nethernets: {}\n')


def guest_report(log, nonce, expected_boot):
    matches = re.findall(r'CHU_GUEST_REPORT=(\{[^\r\n]*\})', log)
    if len(matches) != 1:
        raise ValueError('Expected exactly one guest report in this boot')
    report = json.loads(matches[0])
    expected = {'schema': 'chu-guest-probe/v1', 'nonce': nonce, 'ok': True,
                'boots': expected_boot, 'pid1': 'systemd', 'node': 'v24.13.0',
                'arch': 'x64', 'cgroup_v2': True, 'hswm': 'NOT_READY',
                'kernel': '6.8.0-139-generic'}
    if any(report.get(k) != v for k, v in expected.items()):
        raise ValueError('Guest report violates the pinned substrate contract')
    uuid.UUID(report['boot_id'])
    if not re.fullmatch('[a-f0-9]{64}', report['state_sha256']):
        raise ValueError('Invalid durable state digest')
    state = {'nonce': nonce, 'boots': expected_boot, 'boot_id': report['boot_id']}
    encoded = json.dumps(state, separators=(',', ':')).encode()
    if hashlib.sha256(encoded).hexdigest() != report['state_sha256']:
        raise ValueError('Durable state digest does not match guest state')
    previous = report.get('previous_state_sha256')
    if expected_boot == 1:
        if 'previous_state_sha256' not in report or previous is not None:
            raise ValueError('First boot must start with no previous state')
    elif not isinstance(previous, str) or not re.fullmatch('[a-f0-9]{64}', previous):
        raise ValueError('Second boot must report the previous state digest')
    return report


def validate_boots(boots):
    if len(boots) != 2:
        raise ValueError('Exactly two complete boots are required')
    for number, report in enumerate(boots, 1):
        guest_report('CHU_GUEST_REPORT=' + json.dumps(report), boots[0]['nonce'], number)
    if boots[0]['boot_id'] == boots[1]['boot_id']:
        raise ValueError('Reboot did not produce a new kernel boot ID')
    if boots[1]['previous_state_sha256'] != boots[0]['state_sha256']:
        raise ValueError('Second boot did not read the first boot state')


def write_evidence(report, out, inputs):
    graph = Graph()
    activity = URIRef('urn:uuid:' + report['nonce'])
    graph.add((activity, RDF.type, PROV.Activity))
    for field, predicate in [('started_at', PROV.startedAtTime), ('ended_at', PROV.endedAtTime)]:
        graph.add((activity, predicate, Literal(report[field], datatype=XSD.dateTime)))
    for value in inputs.values():
        entity = URIRef('urn:sha256:' + value)
        graph.add((entity, RDF.type, PROV.Entity))
        graph.add((activity, PROV.used, entity))
    for path in [out / 'report.json', *sorted(out.glob('boot-*.log'))]:
        entity = URIRef('urn:sha256:' + digest(path))
        graph.add((entity, RDF.type, PROV.Entity))
        graph.add((entity, PROV.wasGeneratedBy, activity))
        if path.name == 'report.json':
            graph.add((entity, PROV.value, Literal(json.dumps(report, sort_keys=True))))
    graph.serialize(out / 'evidence.ttl', format='turtle')


def source_inputs(out, manifest):
    """Digest the exact local bytes used to form a new VM-run observation."""
    paths = [
        ROOT / 'scripts/chu_vm.py', ROOT / 'os/inputs.lock.json',
        ROOT / 'os/guest-probe.mjs', ROOT / 'os/chu-probe.service',
        WORK / manifest['image']['file'], WORK / 'node', HOST / 'receipt.json',
        out / 'seed.iso',
    ]
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def boot(timeout):
    manifest = lock()
    if not doctor()['ok']:
        raise ValueError('Run ./chu vm bootstrap first')
    if shutil.disk_usage(WORK).free < 768 * 1024 ** 2:
        raise ValueError('At least 768 MiB free space required for the VM experiment')
    for key in ('image', 'node'):
        if digest(WORK / manifest[key]['file']) != manifest[key]['sha256']:
            raise ValueError('VM input checksum mismatch')
    # Verify the executable actually copied into the guest, not just its archive.
    with tarfile.open(WORK / manifest['node']['file']) as archive:
        member = 'node-v' + manifest['node']['version'] + '-linux-x64/bin/node'
        expected_node = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
    if digest(WORK / 'node') != expected_node:
        raise ValueError('Extracted Node executable checksum mismatch; rerun bootstrap')
    nonce = str(uuid.uuid4())
    out = WORK / 'runs' / nonce
    out.mkdir(parents=True)
    seed(out / 'seed', nonce)
    run(command('genisoimage', '-quiet', '-output', out / 'seed.iso',
                '-volid', 'cidata', '-joliet', '-rock', out / 'seed'))
    overlay = out / 'root.qcow2'
    run(command('qemu-img', 'create', '-f', 'qcow2', '-F', 'qcow2',
                '-b', WORK / 'ubuntu.img', overlay))
    run(command('qemu-img', 'resize', overlay, '4G'))
    argv = command('qemu-system-x86_64', '-machine', 'pc', '-accel', 'tcg',
                   '-cpu', 'max', '-smp', '2', '-m', '1536', '-display', 'none',
                   '-vga', 'none', '-monitor', 'none', '-serial', 'stdio',
                   '-nic', 'none', '-no-reboot', '-L', HOST / 'usr/share/qemu',
                   '-bios', HOST / 'usr/share/seabios/bios-256k.bin',
                   '-drive', f'file={overlay},format=qcow2,if=virtio',
                   '-drive', f'file={out}/seed.iso,format=raw,media=cdrom,readonly=on')
    started = time.monotonic()
    inputs = source_inputs(out, manifest)
    report = {'schema': 'chu-vm-run/v1', 'nonce': nonce, 'ok': False,
              'started_at': datetime.now(timezone.utc).isoformat(),
              'source_sha256': inputs,
              'accelerator': 'tcg', 'network': 'none', 'boots': [], 'hswm': 'NOT_READY',
              'inputs_sha256': digest(ROOT / 'os/inputs.lock.json'),
              'guest_probe_sha256': digest(ROOT / 'os/guest-probe.mjs'),
              'unit_sha256': digest(ROOT / 'os/chu-probe.service')}
    try:
        for number in (1, 2):
            log = out / f'boot-{number}.log'
            with log.open('w') as stream:
                result = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT,
                                        env=host_env(), timeout=timeout)
            if result.returncode:
                raise ValueError(f'QEMU boot {number} exit {result.returncode}')
            report['boots'].append(guest_report(log.read_text(errors='replace'), nonce, number))
        validate_boots(report['boots'])
        report['ok'] = True
    except subprocess.TimeoutExpired:
        report['error'] = f'QEMU boot {number} exceeded {timeout} seconds'
    except (ValueError, KeyError, OSError) as exc:
        report['error'] = str(exc)
    report['ended_at'] = datetime.now(timezone.utc).isoformat()
    report['duration_s'] = round(time.monotonic() - started, 3)
    report['evidence'] = str(out.relative_to(ROOT))
    report['log_sha256'] = {p.name: digest(p) for p in sorted(out.glob('boot-*.log'))}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    write_evidence(report, out, inputs)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['bootstrap', 'doctor', 'boot', 'sources'])
    parser.add_argument('--timeout', type=int, default=300, help='Seconds per boot (1..900)')
    parser.add_argument('--json', action='store_true', help='JSON is the default output')
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 900:
        parser.error('--timeout must be between 1 and 900 seconds')
    result = {'bootstrap': bootstrap, 'doctor': doctor, 'sources': sources,
              'boot': lambda: boot(args.timeout)}[args.command]()
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

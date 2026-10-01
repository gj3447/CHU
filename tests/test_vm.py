import hashlib
import json
import subprocess
import uuid

import pytest
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import PROV

import chu_vm
from chu_vm import fetch, guest_report, validate_boots, write_evidence


def valid_report(*, nonce=None, boots=1, boot_id=None, previous_state_sha256=None):
    report = {'schema': 'chu-guest-probe/v1', 'nonce': nonce or str(uuid.uuid4()),
            'ok': True, 'boots': boots, 'pid1': 'systemd', 'node': 'v24.13.0',
            'arch': 'x64', 'cgroup_v2': True, 'hswm': 'NOT_READY',
            'kernel': '6.8.0-139-generic', 'boot_id': boot_id or str(uuid.uuid4()),
            'previous_state_sha256': previous_state_sha256, 'state_sha256': 'a' * 64}
    state = {key: report[key] for key in ('nonce', 'boots', 'boot_id')}
    report['state_sha256'] = hashlib.sha256(
        json.dumps(state, separators=(',', ':')).encode()).hexdigest()
    return report


def test_guest_evidence_is_bound_to_run_and_boot():
    report = valid_report()
    log = 'unrelated boot output\nCHU_GUEST_REPORT=' + json.dumps(report) + '\n'
    assert guest_report(log, report['nonce'], 1) == report
    with pytest.raises(ValueError):
        guest_report(log, str(uuid.uuid4()), 1)
    with pytest.raises(ValueError):
        guest_report(log, report['nonce'], 2)
    with pytest.raises(ValueError):
        guest_report(log + log, report['nonce'], 1)


def test_two_boot_evidence_binds_the_persisted_state_chain():
    nonce = str(uuid.uuid4())
    first = valid_report(nonce=nonce, boots=1)
    second = valid_report(nonce=nonce, boots=2,
                          previous_state_sha256=first['state_sha256'])
    validate_boots([first, second])


@pytest.mark.parametrize('change', ['previous_state_sha256', 'boot_id'])
def test_two_boot_evidence_rejects_broken_state_or_boot_chain(change):
    nonce = str(uuid.uuid4())
    first = valid_report(nonce=nonce, boots=1)
    second = valid_report(nonce=nonce, boots=2,
                          previous_state_sha256=first['state_sha256'])
    if change == 'previous_state_sha256':
        second[change] = '0' * 64
    else:
        second[change] = first[change]
    with pytest.raises(ValueError):
        validate_boots([first, second])


def test_two_boot_evidence_requires_null_previous_state_on_first_boot():
    nonce = str(uuid.uuid4())
    first = valid_report(nonce=nonce, boots=1, previous_state_sha256='a' * 64)
    with pytest.raises(ValueError):
        guest_report('CHU_GUEST_REPORT=' + json.dumps(first), nonce, 1)


def test_two_boot_evidence_rejects_nonce_mismatch():
    first = valid_report(boots=1)
    second = valid_report(boots=2, previous_state_sha256=first['state_sha256'])
    with pytest.raises(ValueError):
        validate_boots([first, second])


@pytest.mark.parametrize('field,value', [
    ('ok', False), ('node', 'v22.0.0'), ('pid1', 'bash'),
    ('cgroup_v2', False), ('kernel', 'host-kernel'), ('boot_id', 'invalid'),
    ('state_sha256', 'missing'), ('state_sha256', 'b' * 64), ('hswm', 'READY'),
])
def test_boot_marker_alone_does_not_establish_vm_substrate_evidence(field, value):
    report = valid_report()
    report[field] = value
    with pytest.raises(ValueError):
        guest_report('CHU_GUEST_REPORT=' + json.dumps(report), report['nonce'], 1)


def test_missing_guest_evidence_fails():
    with pytest.raises(ValueError):
        guest_report('Ubuntu login: ', 'run', 1)


def test_corrupt_cached_input_is_not_used_or_silently_replaced(tmp_path):
    path = tmp_path / 'image'
    path.write_bytes(b'corrupt')
    with pytest.raises(ValueError, match='Cached checksum mismatch'):
        fetch({'sha256': '0' * 64, 'url': 'https://invalid.example'}, path)
    assert path.read_bytes() == b'corrupt'


def test_evidence_binds_report_inputs_and_each_boot_log(tmp_path):
    report = {
        'nonce': str(uuid.uuid4()), 'started_at': '2026-10-01T00:00:00+00:00',
        'ended_at': '2026-10-01T00:00:01+00:00', 'ok': True,
    }
    inputs = {'os/inputs.lock.json': 'a' * 64, 'os/guest-probe.mjs': 'b' * 64}
    report_path = tmp_path / 'report.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    for number in (1, 2):
        (tmp_path / f'boot-{number}.log').write_text(f'boot {number}\n')

    write_evidence(report, tmp_path, inputs)

    graph = Graph().parse(tmp_path / 'evidence.ttl')
    activity = URIRef('urn:uuid:' + report['nonce'])
    report_entity = URIRef('urn:sha256:' + hashlib.sha256(report_path.read_bytes()).hexdigest())
    assert (report_entity, PROV.wasGeneratedBy, activity) in graph
    assert (report_entity, PROV.value, Literal(json.dumps(report, sort_keys=True))) in graph
    for value in inputs.values():
        assert (activity, PROV.used, URIRef('urn:sha256:' + value)) in graph
    for number in (1, 2):
        log = tmp_path / f'boot-{number}.log'
        entity = URIRef('urn:sha256:' + hashlib.sha256(log.read_bytes()).hexdigest())
        assert (entity, PROV.wasGeneratedBy, activity) in graph


def test_doctor_rejects_a_single_wrong_host_tool_version(monkeypatch, tmp_path):
    host = tmp_path / 'host'
    work = tmp_path / 'work'
    (host / 'usr/bin').mkdir(parents=True)
    work.mkdir()
    (work / 'node').write_bytes(b'node')
    (work / 'ubuntu.img').write_bytes(b'image')
    monkeypatch.setattr(chu_vm, 'HOST', host)
    monkeypatch.setattr(chu_vm, 'WORK', work)
    monkeypatch.setattr(chu_vm, 'host_valid', lambda: True)

    versions = {
        'qemu-system-x86_64': 'QEMU emulator version 10.0.13 ',
        'qemu-img': 'qemu-img version 10.0.13 ',
        'genisoimage': 'wrong version',
    }

    def fake_run(argv):
        return subprocess.CompletedProcess(argv, 0, stdout=versions[argv[0].split('/')[-1]], stderr='')

    monkeypatch.setattr(chu_vm, 'run', fake_run)
    assert chu_vm.doctor()['ok'] is False
    versions['genisoimage'] = 'genisoimage 1.1.11 '
    assert chu_vm.doctor()['ok'] is True

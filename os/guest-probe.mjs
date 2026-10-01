// CHU OS substrate probe. This does not import or execute HSWM.
import fs from 'node:fs';
import os from 'node:os';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const root = '/var/lib/chu';
const read = (path) => fs.readFileSync(path, 'utf8').trim();
const nonce = read('/opt/chu/nonce');
fs.mkdirSync(root, { recursive: true });
const previous = fs.existsSync(`${root}/state.json`) ? read(`${root}/state.json`) : null;
const old = previous === null ? { boots: 0, nonce } : JSON.parse(previous);
assert.equal(old.nonce, nonce);
const bootId = read('/proc/sys/kernel/random/boot_id');
assert.notEqual(bootId, old.boot_id);
assert.equal(process.version, 'v24.13.0');
assert.equal(read('/proc/1/comm'), 'systemd');
assert.equal(os.platform(), 'linux');
assert.match(read('/etc/os-release'), /^ID=ubuntu$/m);
assert.ok(fs.existsSync('/sys/fs/cgroup/cgroup.controllers'));
const state = { nonce, boots: old.boots + 1, boot_id: bootId };
const bytes = JSON.stringify(state);
const fd = fs.openSync(`${root}/state.tmp`, 'w', 0o600);
fs.writeFileSync(fd, bytes);
fs.fsyncSync(fd);
fs.closeSync(fd);
fs.renameSync(`${root}/state.tmp`, `${root}/state.json`);
const dir = fs.openSync(root, 'r');
fs.fsyncSync(dir);
fs.closeSync(dir);
assert.equal(read(`${root}/state.json`), bytes);
const report = {
  schema: 'chu-guest-probe/v1', nonce, ok: true, boots: state.boots,
  boot_id: bootId, kernel: os.release(), pid1: read('/proc/1/comm'),
  node: process.version, arch: os.arch(), cgroup_v2: true,
  previous_state_sha256: previous === null ? null
    : crypto.createHash('sha256').update(previous).digest('hex'),
  state_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  hswm: 'NOT_READY',
  hswm_reason: 'HSWM package, model provider and authorized resource transport not provisioned',
};
fs.writeFileSync(`${root}/probe.json`, JSON.stringify(report) + '\n');
console.log('CHU_GUEST_REPORT=' + JSON.stringify(report));

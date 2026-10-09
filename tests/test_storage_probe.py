"""Storage-specific counterexamples; the registered probe exercises SIGKILL/races."""
import sqlite3

import pytest

from chu_model import Change, Edge, Incidence, State, cid
from chu_storage_probe import ProbeStore, RequestConflict


@pytest.fixture
def store(tmp_path):
    value = ProbeStore(tmp_path / "probe.db", initialize=True)
    yield value
    value.close()


def test_binary_bytes_and_ordered_nary_roles_survive_reopen(store):
    raw = (b"\x00\xff\x80", "é".encode(), "e\u0301".encode())
    created = store.commit(State().cid, 0, Change("create", add_nodes=raw), "create")
    parts = tuple(Incidence("subject" if i == 0 else "candidate", cid(b))
                  for i, b in enumerate(raw))
    first = Edge("requires-any", parts)
    reverse = Edge("requires-any", (parts[0], parts[2], parts[1]))
    event = store.commit(created["result"], 1, Change("link", add_edges=(first, reverse)), "link")
    loaded = store.load(event["result"])
    assert dict(loaded.nodes) == {cid(b): b for b in raw}
    assert len({first.cid, reverse.cid}) == 2
    assert {e.cid: e.participants for e in loaded.edges} == {
        first.cid: parts, reverse.cid: reverse.participants}


@pytest.mark.parametrize("difference", ["actor", "branch", "revision", "base"])
def test_idempotency_key_cannot_cross_a_different_request_scope(store, difference):
    change = Change("create", add_nodes=(b"one",))
    event = store.commit(State().cid, 0, change, "same-id")
    inputs = dict(base=State().cid, revision=0, change=change, request="same-id")
    inputs.update({difference: {"actor": "urn:chu:agent:other", "branch": "other",
                               "revision": 1, "base": event["result"]}[difference]})
    before = store.audit()
    with pytest.raises(RequestConflict):
        store.commit(**inputs)
    assert store.audit() == before


def test_failed_validation_rolls_back_without_adding_objects(store):
    before = store.audit()
    with pytest.raises(ValueError):
        store.commit(State().cid, 0, Change("create", add_nodes=(b"new",),
                                           remove_nodes=(cid(b"old"),)), "invalid")
    assert store.audit() == before
    assert not store.db.in_transaction


def test_python_exception_between_event_and_head_rolls_back(store):
    def fail(stage):
        if stage == "after_event":
            raise RuntimeError("injected exception")
    before = store.audit()
    with pytest.raises(RuntimeError, match="injected"):
        store.commit(State().cid, 0, Change("create", add_nodes=(b"new",)), "fail", hook=fail)
    assert store.audit() == before


def test_history_survives_current_state_delete_and_duplicate_branch_fails(store):
    created = store.commit(State().cid, 0, Change("create", add_nodes=(b"old",)), "create")
    store.fork("archive")
    store.commit(created["result"], 1, Change("delete", remove_nodes=(cid(b"old"),)), "delete")
    assert store.head()["state"] == State().cid
    assert store.head("archive")["state"] == created["result"]
    assert store.load(created["result"]).nodes == ((cid(b"old"), b"old"),)
    before = store.audit()
    with pytest.raises(sqlite3.IntegrityError):
        store.fork("archive")
    assert store.audit() == before


def test_network_filesystem_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr("chu_storage_probe.subprocess.check_output", lambda *a, **k: "nfs4\n")
    with pytest.raises(ValueError, match="known local filesystem"):
        ProbeStore(tmp_path / "network.db", initialize=True)
    assert not (tmp_path / "network.db").exists()

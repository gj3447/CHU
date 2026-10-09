#!/usr/bin/env python3
"""Bounded process-crash/CAS research on disposable local SQLite databases."""
import argparse
import hashlib
import json
import multiprocessing
import os
import platform
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from chu_model import Change, Edge, Incidence, Model, State, cid, group, members
from chu_storage_probe import Conflict, ProbeStore, RequestConflict, local_filesystem

ROOT = Path(__file__).resolve().parents[1]
CUTS = ("after_objects", "after_state", "after_event", "after_head", "before_commit",
        "after_commit_before_reply")
CTX = multiprocessing.get_context("spawn")


def _crash_writer(path, cut, pipe):
    store = ProbeStore(path)

    def pause(stage):
        if stage == cut:
            pipe.send({"stage": stage, "head": store.head(), "counts": store.counts()})
            pipe.recv()  # Parent kills exactly this child while it is at the cut point.

    store.commit(State().cid, 0, Change("create", add_nodes=(b"crash-data",)), "crash", hook=pause)
    raise RuntimeError("Fault cut was not reached")


def _racing_writer(path, request, body, pipe):
    try:
        store = ProbeStore(path)
        pipe.send("ready")
        pipe.recv()
        try:
            event = store.commit(State().cid, 0, Change("create", add_nodes=(body,)), request)
            pipe.send({"status": "COMMITTED", "result": event["result"]})
        except Conflict:
            pipe.send({"status": "STALE"})
        finally:
            store.close()
    except BaseException as exc:
        pipe.send({"status": "ERROR", "error": repr(exc)})
        raise


def receive(pipe):
    if not pipe.poll(15):
        raise TimeoutError("Research child did not reach its handshake")
    return pipe.recv()


def stop(process):
    if process.is_alive():
        process.kill()
    process.join(5)
    if process.is_alive():
        raise RuntimeError("Research child failed to exit")


def crash_case(path, cut):
    observer = ProbeStore(path, initialize=True)
    baseline = observer.audit()
    parent, child = CTX.Pipe()
    process = CTX.Process(target=_crash_writer, args=(str(path), cut, child))
    process.start()
    child.close()
    try:
        reached = receive(parent)
        assert reached["stage"] == cut
        # Independent reader must see a whole committed state, never the writer's prefix.
        visible = observer.audit()
        committed = cut == "after_commit_before_reply"
        assert visible["events"] == int(committed)
        if not committed:
            assert visible == baseline
            assert observer.head() == {"state": State().cid, "revision": 0, "tip": None}
        process.kill()
        process.join(5)
        assert process.exitcode == -signal.SIGKILL
    finally:
        stop(process)
        parent.close()
        observer.close()
    recovered = ProbeStore(path)
    try:
        recovered_counts = recovered.audit()
        assert recovered_counts == visible
        head_before_retry = recovered.head()
        response = recovered.commit(State().cid, 0, Change("create", add_nodes=(b"crash-data",)), "crash")
        expected = Model().apply(State().cid, Change("create", add_nodes=(b"crash-data",)), "oracle")
        assert response["result"] == expected
        assert recovered.load(expected).nodes == ((cid(b"crash-data"), b"crash-data"),)
        assert recovered.audit()["events"] == 1
        assert recovered.head()["revision"] == 1
        return {"case": "sigkill-" + cut, "status": "PASS", "child_exit": process.exitcode,
                "cut_reached": reached, "visible_before_kill": visible,
                "recovered_before_retry": recovered_counts, "head_before_retry": head_before_retry,
                "after_retry": recovered.audit(), "result": response["result"]}
    finally:
        recovered.close()


def race_case(path, same_request):
    seed = ProbeStore(path, initialize=True)
    workers = []
    try:
        for i in range(2):
            parent, child = CTX.Pipe()
            process = CTX.Process(target=_racing_writer, args=(
                str(path), "same" if same_request else f"writer-{i}",
                b"same" if same_request else f"writer-{i}".encode(), child))
            process.start()
            child.close()
            workers.append((process, parent))
        for _, pipe in workers:
            assert receive(pipe) == "ready"
        for _, pipe in workers:
            pipe.send("go")
        outcomes = [receive(pipe) for _, pipe in workers]
        for process, _ in workers:
            process.join(5)
            assert process.exitcode == 0
        expected = ["COMMITTED", "COMMITTED"] if same_request else ["COMMITTED", "STALE"]
        assert sorted(o["status"] for o in outcomes) == expected, outcomes
        if same_request:
            assert outcomes[0] == outcomes[1]
        assert seed.audit()["events"] == 1
        assert seed.head()["revision"] == 1
        return {"case": "concurrent-same-request" if same_request else "concurrent-different-requests",
                "status": "PASS", "outcomes": outcomes, "head": seed.head(), "counts": seed.audit()}
    finally:
        for process, pipe in workers:
            stop(process)
            pipe.close()
        seed.close()


def semantic_cases(path):
    store = ProbeStore(path, initialize=True)
    observations = []
    try:
        model = Model()
        def apply(change, request, branch="main"):
            head = store.head(branch)
            expected = model.apply(head["state"], change, request)
            event = store.commit(head["state"], head["revision"], change, request, branch=branch)
            assert expected == event["result"]
            assert store.load(expected) == model.states[expected]
            return event

        a, b, payload = b"group:a", b"group:b", b"document:immutable"
        created = apply(Change("create", add_nodes=(a, b, payload)), "create")
        edges = (group(cid(a), cid(payload)), group(cid(b), cid(payload)))
        linked = apply(Change("link", add_edges=edges), "link")
        store.fork("alternative")
        left = apply(Change("unlink", remove_edges=(edges[0].cid,)), "unlink-a")
        right = apply(Change("unlink", remove_edges=(edges[1].cid,)), "unlink-b", "alternative")
        assert members(store.load(linked["result"]), cid(a)) == [cid(payload)]
        assert members(store.load(linked["result"]), cid(b)) == [cid(payload)]
        assert members(store.load(left["result"]), cid(a)) == []
        assert members(store.load(left["result"]), cid(b)) == [cid(payload)]
        assert members(store.load(right["result"]), cid(a)) == [cid(payload)]
        assert members(store.load(right["result"]), cid(b)) == []
        # Retry with old base/revision is a lookup, not a second write or stale error.
        replay = store.commit(State().cid, 0, Change("create", add_nodes=(payload, b, a, a)), "create")
        assert replay == created
        before = store.audit()
        try:
            store.commit(State().cid, 0, Change("create", add_nodes=(b"changed",)), "create")
        except RequestConflict:
            pass
        else:
            raise AssertionError("Request ID collision was accepted")
        head = store.head()
        invalid = Edge("group", (Incidence("group", cid(a)), Incidence("member", cid(b"absent"))))
        try:
            store.commit(head["state"], head["revision"], Change("link", add_edges=(invalid,)), "invalid")
        except ValueError:
            pass
        else:
            raise AssertionError("Dangling endpoint accepted")
        assert before == store.audit()
        observations.append({"case": "model-parity-branching-retry-validation", "status": "PASS",
                             "states": {"linked": linked["result"], "left": left["result"], "right": right["result"]},
                             "counts": before})
        previous = store.head()
        duplicate = apply(Change("create", add_nodes=(payload,)), "dedup-new-event")
        assert duplicate["result"] == previous["state"]
        assert store.counts()["states"] == before["states"]
        assert store.counts()["events"] == before["events"] + 1
        observations.append({"case": "same-state-distinct-event", "status": "PASS", "counts": store.audit()})
    finally:
        store.close()
    reopened = ProbeStore(path)
    try:
        assert reopened.load(linked["result"]) == model.states[linked["result"]]
        assert reopened.audit()["events"] == before["events"] + 1
        observations.append({"case": "reopen-historical-snapshot", "status": "PASS"})
    finally:
        reopened.close()
    return observations


def aba_case(path):
    store = ProbeStore(path, initialize=True)
    try:
        initial = store.head()
        added = store.commit(initial["state"], 0, Change("create", add_nodes=(b"temporary",)), "add")
        store.commit(added["result"], 1, Change("delete", remove_nodes=(cid(b"temporary"),)), "remove")
        current = store.head()
        assert current["state"] == initial["state"] and current["revision"] == 2
        # Negative control: the CID-only UPDATE really matches after A -> B -> A.
        store.db.execute("BEGIN IMMEDIATE")
        matched = store.db.execute("UPDATE branches SET state=? WHERE name='main' AND state=?",
                                   (added["result"], initial["state"])).rowcount
        store.db.execute("ROLLBACK")
        assert matched == 1
        before = store.audit()
        try:
            store.commit(initial["state"], 0, Change("create", add_nodes=(b"stale",)), "stale")
        except Conflict:
            pass
        else:
            raise AssertionError("ABA stale writer was accepted")
        assert before == store.audit()
        return {"case": "aba-cid-only-negative-control", "status": "PASS",
                "old": initial, "current": current, "unsafe_cid_only_rows_matched": matched,
                "state_and_revision_rejected": True}
    finally:
        store.close()


def isolation_case(path):
    writer = ProbeStore(path, initialize=True)
    reader = ProbeStore(path)
    contender = ProbeStore(path, timeout=0.05)
    try:
        reader.db.execute("BEGIN")
        old = reader.head()
        event = writer.commit(old["state"], 0, Change("create", add_nodes=(b"new",)), "new")
        assert reader.head() == old
        reader.db.execute("COMMIT")
        assert reader.head()["state"] == event["result"]
        writer.db.execute("BEGIN IMMEDIATE")
        try:
            contender.commit(event["result"], 1, Change("create", add_nodes=(b"blocked",)), "busy")
        except sqlite3.OperationalError as exc:
            assert exc.sqlite_errorcode == sqlite3.SQLITE_BUSY
            busy = exc.sqlite_errorname
        else:
            raise AssertionError("Competing writer did not report BUSY")
        finally:
            writer.db.execute("ROLLBACK")
        assert writer.audit()["events"] == 1
        return {"case": "reader-snapshot-and-busy", "status": "PASS", "busy_error": busy}
    finally:
        writer.close()
        reader.close()
        contender.close()


def corruption_case(path):
    store = ProbeStore(path, initialize=True)
    try:
        event = store.commit(State().cid, 0, Change("create", add_nodes=(b"known",)), "known")
        store.db.execute("UPDATE objects SET body=? WHERE cid=?", (b"damaged", cid(b"known")))
        try:
            store.load(event["result"])
        except ValueError:
            return {"case": "content-corruption-detection", "status": "PASS"}
        raise AssertionError("Damaged content returned as valid")
    finally:
        store.close()


def run(out, repeats=3):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    filesystem = local_filesystem(out)
    started = time.monotonic()
    cases = []
    with tempfile.TemporaryDirectory(prefix="chu-storage-probe-", dir=out) as tmp:
        root = Path(tmp)
        cases.extend(semantic_cases(root / "semantics.db"))
        cases.append(aba_case(root / "aba.db"))
        cases.append(isolation_case(root / "isolation.db"))
        cases.append(corruption_case(root / "corruption.db"))
        for repeat in range(repeats):
            for cut in CUTS:
                cases.append({**crash_case(root / f"crash-{repeat}-{cut}.db", cut), "repeat": repeat})
            for same in (False, True):
                cases.append({**race_case(root / f"race-{repeat}-{same}.db", same), "repeat": repeat})
        configured = ProbeStore(root / "semantics.db")
        try:
            pragmas = {key: configured.db.execute("PRAGMA " + key).fetchone()[0] for key in (
                "journal_mode", "synchronous", "foreign_keys", "page_size", "max_page_count",
                "wal_autocheckpoint", "read_uncommitted")}
            assert pragmas["journal_mode"] == "wal" and pragmas["synchronous"] == 2
            assert pragmas["foreign_keys"] == 1 and pragmas["read_uncommitted"] == 0
        finally:
            configured.close()
        artifact_bytes = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
        assert artifact_bytes < 32 * 1024 * 1024
    inputs = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in (
        "scripts/chu_model.py", "scripts/chu_storage_probe.py", "scripts/check_storage_probe.py",
        "spec/IDENTITY.md", "spec/DATA_MODEL.md", "spec/OPERATIONS.md")}
    db = sqlite3.connect(":memory:")
    source_id = db.execute("SELECT sqlite_source_id()").fetchone()[0]
    db.close()
    report = {"schema": "chu-storage-research/v1", "authority": "SECONDARY_AI",
              "observed_at": datetime.now(timezone.utc).isoformat(),
              "git_base": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "input_sha256": inputs, "argv": sys.argv, "python": sys.version,
              "platform": platform.platform(), "filesystem": filesystem,
              "sqlite_version": sqlite3.sqlite_version, "sqlite_source_id": source_id,
              "configuration": {"journal_mode": "wal", "synchronous": "FULL", "timeout_s": 2,
                                "max_page_count": 1024, "concurrent_workers": 2},
              "observed_pragmas": pragmas,
              "wal_reset_fix_status": "NOT_VERIFIED_FOR_THIS_VENDOR_BUILD",
              "duration_s": round(time.monotonic() - started, 3), "temporary_db_bytes": artifact_bytes,
              "repeats": repeats, "status": "PASS", "cases": cases,
              "scope": "Synthetic research adapter; process kill, not power-loss/VFS fault testing",
              "not_tested": ["power loss", "torn writes", "disk full", "SQLite WAL-reset race",
                             "malicious database tampering", "authentication/capabilities", "external effects",
                             "VM boot", "HSWM", "Rust kernel", "backup/restore", "migrations", "GC"]}
    (out / "storage-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3, choices=range(1, 11))
    args = parser.parse_args()
    if os.name != "posix":
        parser.error("SIGKILL experiment requires a POSIX host")
    report = run(args.out, args.repeats)
    print(json.dumps({"status": report["status"], "cases": len(report["cases"]),
                      "duration_s": report["duration_s"], "report": str(args.out / "storage-report.json")}))


if __name__ == "__main__":
    main()

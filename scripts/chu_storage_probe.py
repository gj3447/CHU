"""SQLite research adapter for chu_model. Not an OS service or production backend.

All content uses the existing model encoding. Branch revisions are concurrency
tokens, outside content identity. Callers are trusted; actor URNs are not auth.
"""
import json
import sqlite3
import subprocess
from pathlib import Path

from chu_model import Edge, Incidence, Model, State, cid, encoded


class Conflict(ValueError):
    """The named branch has advanced since the caller's observed revision."""


class RequestConflict(ValueError):
    """A request ID was reused with a different normalized request."""


def local_filesystem(path):
    """Research admission: WAL must not silently run on the shared NFS volume."""
    kind = subprocess.check_output(
        ["findmnt", "-T", str(Path(path).resolve()), "-n", "-o", "FSTYPE"],
        text=True, timeout=5,
    ).strip()
    if kind not in {"ext4", "xfs", "btrfs", "tmpfs", "overlay"}:
        raise ValueError(f"Research WAL requires a known local filesystem, found {kind!r}")
    return kind


class ProbeStore:
    def __init__(self, path, *, initialize=False, timeout=2.0):
        path = Path(path)
        local_filesystem(path.parent)
        if not initialize and not path.is_file():
            raise ValueError("Initialize the research database explicitly")
        self.db = sqlite3.connect(path, timeout=timeout, isolation_level=None)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA max_page_count=1024")  # <=4 MiB main DB at default page size
        if initialize:
            if self.db.execute("PRAGMA journal_mode=WAL").fetchone()[0] != "wal":
                self.close()
                raise ValueError("WAL mode was not enabled")
            self.db.executescript("""
                CREATE TABLE IF NOT EXISTS objects(cid TEXT PRIMARY KEY, body BLOB NOT NULL);
                CREATE TABLE IF NOT EXISTS states(cid TEXT PRIMARY KEY REFERENCES objects(cid));
                CREATE TABLE IF NOT EXISTS events(
                    request TEXT PRIMARY KEY, fingerprint TEXT NOT NULL,
                    body BLOB NOT NULL, base TEXT NOT NULL REFERENCES states(cid),
                    result TEXT NOT NULL REFERENCES states(cid));
                CREATE TABLE IF NOT EXISTS branches(
                    name TEXT PRIMARY KEY, state TEXT NOT NULL REFERENCES states(cid),
                    revision INTEGER NOT NULL CHECK(revision>=0),
                    tip TEXT REFERENCES events(request));
            """)
            self.db.execute("BEGIN IMMEDIATE")
            try:
                self._save_state(State())
                self.db.execute("INSERT OR IGNORE INTO branches VALUES(?, ?, 0, NULL)",
                                ("main", State().cid))
                self.db.execute("COMMIT")
            except BaseException:
                self._rollback()
                self.close()
                raise
        elif self.db.execute("PRAGMA journal_mode").fetchone()[0] != "wal":
            self.close()
            raise ValueError("Research database is not in WAL mode")

    def close(self):
        self.db.close()

    def _rollback(self):
        if self.db.in_transaction:
            self.db.execute("ROLLBACK")

    def _put(self, body):
        key = cid(body)
        self.db.execute("INSERT OR IGNORE INTO objects VALUES(?, ?)", (key, body))
        if self._get(key) != body:
            raise ValueError("Content-address collision or damaged object")
        return key

    def _get(self, key):
        row = self.db.execute("SELECT body FROM objects WHERE cid=?", (key,)).fetchone()
        if row is None or cid(row[0]) != key:
            raise ValueError("Missing or damaged content object")
        return row[0]

    def _save_state(self, state, hook=lambda stage: None):
        state.validate()
        for _, body in state.nodes:
            self._put(body)
        for edge in state.edges:
            self._put(encoded(edge.record()))
        hook("after_objects")
        body = encoded({"schema": "chu-state/v1", "nodes": sorted(k for k, _ in state.nodes),
                        "edges": sorted(e.cid for e in state.edges)})
        if self._put(body) != state.cid:
            raise ValueError("State encoding differs from the reference model")
        self.db.execute("INSERT OR IGNORE INTO states VALUES(?)", (state.cid,))
        hook("after_state")

    def load(self, key):
        if self.db.execute("SELECT 1 FROM states WHERE cid=?", (key,)).fetchone() is None:
            raise ValueError("Unknown state")
        record = json.loads(self._get(key))
        if set(record) != {"schema", "nodes", "edges"} or record["schema"] != "chu-state/v1":
            raise ValueError("Invalid state encoding")
        edges = []
        for edge_key in record["edges"]:
            item = json.loads(self._get(edge_key))
            if set(item) != {"schema", "type", "participants"} or item["schema"] != "chu-edge/v1":
                raise ValueError("Invalid edge encoding")
            edge = Edge(item["type"], tuple(Incidence(**p) for p in item["participants"]))
            if edge.cid != edge_key:
                raise ValueError("Noncanonical edge")
            edges.append(edge)
        state = State(tuple((k, self._get(k)) for k in record["nodes"]), tuple(edges))
        state.validate()
        if state.cid != key:
            raise ValueError("Noncanonical state")
        return state

    def head(self, branch="main"):
        row = self.db.execute("SELECT state, revision, tip FROM branches WHERE name=?",
                              (branch,)).fetchone()
        if row is None:
            raise ValueError("Unknown branch")
        return {"state": row[0], "revision": row[1], "tip": row[2]}

    def fork(self, name, source="main"):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.head(source)
            self.db.execute("INSERT INTO branches VALUES(?, ?, 0, ?)",
                            (name, old["state"], old["tip"]))
            self.db.execute("COMMIT")
        except BaseException:
            self._rollback()
            raise

    def commit(self, base, revision, change, request, actor="urn:chu:agent:research",
               branch="main", hook=lambda stage: None):
        if type(revision) is not int or revision < 0:
            raise ValueError("A nonnegative branch revision is required")
        fingerprint = cid(encoded({"schema": "chu-store-request/v1", "base": base,
                                   "revision": str(revision), "branch": branch,
                                   "actor": actor, "change": change.record()}))
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute("SELECT fingerprint, body FROM events WHERE request=?",
                                    (request,)).fetchone()
            if prior:
                if prior[0] != fingerprint:
                    raise RequestConflict("Request ID reused with different input")
                response = json.loads(prior[1])
                self.db.execute("COMMIT")
                return response  # Retry returns original result even after the head advances.
            old = self.head(branch)
            if (old["state"], old["revision"]) != (base, revision):
                raise Conflict("Stale branch state/revision")
            model = Model()
            model.states = {base: self.load(base)}
            result = model.apply(base, change, request, actor)
            self._save_state(model.states[result], hook)
            event = {**model.events[request], "model_fingerprint": model.events[request]["fingerprint"],
                     "fingerprint": fingerprint, "branch": branch, "revision": revision + 1,
                     "parent_request": old["tip"]}
            self.db.execute("INSERT INTO events VALUES(?, ?, ?, ?, ?)",
                            (request, fingerprint, encoded(event), base, result))
            hook("after_event")
            changed = self.db.execute(
                "UPDATE branches SET state=?, revision=revision+1, tip=? "
                "WHERE name=? AND state=? AND revision=?",
                (result, request, branch, base, revision),
            ).rowcount
            if changed != 1:
                raise Conflict("Branch compare-and-swap failed")
            hook("after_head")
            hook("before_commit")
            self.db.execute("COMMIT")
            hook("after_commit_before_reply")
            return event
        except BaseException:
            self._rollback()
            raise

    def counts(self):
        return {table: self.db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                for table in ("objects", "states", "events", "branches")}

    def audit(self):
        """Check stored hashes, endpoints, event/head consistency and SQLite structure."""
        if self.db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise ValueError("SQLite integrity check failed")
        if self.db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("SQLite foreign key check failed")
        for (key,) in self.db.execute("SELECT cid FROM objects"):
            self._get(key)
        for (key,) in self.db.execute("SELECT cid FROM states"):
            self.load(key)
        for request, fingerprint, body, base, result in self.db.execute("SELECT * FROM events"):
            event = json.loads(body)
            if (event["request"], event["fingerprint"], event["base"], event["result"]) != (
                    request, fingerprint, base, result):
                raise ValueError("Event envelope differs from indexed values")
            parent = event["parent_request"]
            if parent:
                row = self.db.execute("SELECT result FROM events WHERE request=?", (parent,)).fetchone()
                if row != (base,):
                    raise ValueError("Event parent does not produce its base state")
        for name, state, revision, tip in self.db.execute("SELECT * FROM branches"):
            if tip:
                event = json.loads(self.db.execute("SELECT body FROM events WHERE request=?", (tip,)).fetchone()[0])
                if event["result"] != state or (revision and (event["branch"], event["revision"]) != (name, revision)):
                    raise ValueError("Branch head differs from its event")
        return self.counts()

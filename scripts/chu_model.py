#!/usr/bin/env python3
"""Executable CHU v0.1 contract, in memory; not the persistent Rust kernel."""
import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV

ROOT = Path(__file__).resolve().parents[1]
CHU = Namespace("https://github.com/gj3447/CHU/vocab#")
ROLES = {"group": ("group", "member"), "requires-any": ("subject", "candidate")}
OPERATIONS = {"create", "link", "unlink", "retag", "delete"}
EXAMPLES = ("README.md", "plan/chu_os_plan.graph.json", "chu_core_prototype/chu_core.rs",
            "plan/check_plan.py", "lean/CHU_WolframRewrite.lean")


def encoded(value):
    """CHU v0.1 object encoding: restricted JSON, UTF-8, sorted keys, no whitespace."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def cid(data):
    return "urn:sha256:" + hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Incidence:
    role: str
    node: str


@dataclass(frozen=True)
class Edge:
    relation: str
    participants: tuple[Incidence, ...]

    def record(self):
        return {"schema": "chu-edge/v1", "type": self.relation,
                "participants": [{"role": p.role, "node": p.node} for p in self.participants]}

    @property
    def cid(self):
        return cid(encoded(self.record()))


@dataclass(frozen=True)
class State:
    # Immutable values; physical storage layout is not this model's node identity.
    nodes: tuple[tuple[str, bytes], ...] = ()
    edges: tuple[Edge, ...] = ()

    @property
    def cid(self):
        return cid(encoded({"schema": "chu-state/v1", "nodes": sorted(n for n, _ in self.nodes),
                            "edges": sorted(e.cid for e in self.edges)}))

    def validate(self):
        nodes = dict(self.nodes)
        if len(nodes) != len(self.nodes) or len({e.cid for e in self.edges}) != len(self.edges):
            raise ValueError("Duplicate object identity in snapshot")
        if any(cid(data) != name for name, data in self.nodes):
            raise ValueError("Content digest does not match bytes")
        for edge in self.edges:
            if edge.relation not in ROLES or len(edge.participants) < 2:
                raise ValueError("Unregistered relation or missing participants")
            first, rest = ROLES[edge.relation]
            for i, part in enumerate(edge.participants):
                if part.node not in nodes:
                    raise ValueError("Dangling incidence endpoint")
                if part.role != (first if i == 0 else rest):
                    raise ValueError("Role does not match relation/ordinal contract")


@dataclass(frozen=True)
class Change:
    operation: str
    add_nodes: tuple[bytes, ...] = ()
    remove_nodes: tuple[str, ...] = ()
    add_edges: tuple[Edge, ...] = ()
    remove_edges: tuple[str, ...] = ()

    def record(self):
        return {"schema": "chu-change/v1", "operation": self.operation,
                "add_nodes": sorted({cid(b) for b in self.add_nodes}),
                "remove_nodes": sorted(set(self.remove_nodes)),
                "add_edges": sorted({e.cid for e in self.add_edges}),
                "remove_edges": sorted(set(self.remove_edges))}


class Model:
    def __init__(self):
        initial = State()
        self.states = {initial.cid: initial}
        self.initial = initial.cid
        self.events = {}

    def apply(self, base, change, request, actor="urn:chu:agent:reference"):
        if not request or not actor.startswith("urn:"):
            raise ValueError("A request ID and explicit actor URN are required")
        fingerprint = cid(encoded({"base": base, "change": change.record(), "actor": actor}))
        if request in self.events:
            event = self.events[request]
            if event["fingerprint"] != fingerprint:
                raise ValueError("Request ID reused with different input")
            return event["result"]
        if base not in self.states or change.operation not in OPERATIONS:
            raise ValueError("Unknown base state or operation")
        allowed = {
            "create": bool(change.add_nodes) and not (change.remove_nodes or change.add_edges or change.remove_edges),
            "link": bool(change.add_edges) and not (change.add_nodes or change.remove_nodes or change.remove_edges),
            "unlink": bool(change.remove_edges) and not (change.add_nodes or change.remove_nodes or change.add_edges),
            "retag": bool(change.remove_edges and change.add_edges) and not (change.add_nodes or change.remove_nodes),
            "delete": bool(change.remove_nodes) and not (change.add_nodes or change.add_edges),
        }
        if not allowed[change.operation]:
            raise ValueError("Delta does not match the declared operation")
        nodes, edges = dict(self.states[base].nodes), {e.cid: e for e in self.states[base].edges}
        if set(change.remove_nodes) - nodes.keys() or set(change.remove_edges) - edges.keys():
            raise ValueError("Remove precondition failed")
        for key in change.remove_nodes:
            nodes.pop(key, None)
        for key in change.remove_edges:
            edges.pop(key, None)
        nodes.update((cid(data), data) for data in change.add_nodes)
        edges.update((edge.cid, edge) for edge in change.add_edges)
        candidate = State(tuple(sorted(nodes.items())), tuple(edges[k] for k in sorted(edges)))
        candidate.validate()  # All validation occurs before either history collection changes.
        result = candidate.cid
        event = {"request": request, "fingerprint": fingerprint, "base": base, "result": result,
                 "operation": change.operation, "actor": actor, "change": change.record(),
                 "observed_at": datetime.now(timezone.utc).isoformat()}
        self.states[result] = candidate
        self.events[request] = event
        return result


def group(*nodes):
    return Edge("group", tuple(Incidence("group" if i == 0 else "member", node)
                               for i, node in enumerate(nodes)))


def members(state, group_node):
    return sorted({p.node for e in state.edges if e.relation == "group"
                   and e.participants[0].node == group_node for p in e.participants[1:]})


def demo():
    model = Model()
    sources = {path: cid((ROOT / path).read_bytes()) for path in EXAMPLES}
    data = tuple((ROOT / path).read_bytes() for path in EXAMPLES)
    labels = (b"CHU group: implementation", b"CHU group: theory")
    base = model.apply(model.initial, Change("create", add_nodes=data + labels), "import-examples")
    groups = tuple(cid(label) for label in labels)
    common = sources["README.md"]
    edges = (group(groups[0], common, sources["chu_core_prototype/chu_core.rs"]),
             group(groups[1], common, sources["lean/CHU_WolframRewrite.lean"]),
             Edge("requires-any", (Incidence("subject", sources["plan/chu_os_plan.graph.json"]),
                                   Incidence("candidate", groups[0]), Incidence("candidate", groups[1]))))
    linked = model.apply(base, Change("link", add_edges=edges), "link-two-views")
    left = model.apply(linked, Change("unlink", remove_edges=(edges[0].cid,)), "branch-left")
    right = model.apply(linked, Change("unlink", remove_edges=(edges[1].cid,)), "branch-right")
    views = {label: [f"{label}/{node.removeprefix('urn:sha256:')}" for node in members(model.states[linked], gid)]
             for label, gid in zip(("implementation", "theory"), groups)}
    return model, {"schema": "chu-model-demo/v1", "scope": "in-memory executable specification",
                   "sources": sources, "base": base, "linked": linked,
                   "branches": [left, right], "shared_content": common, "groups": list(groups),
                   "views": views, "events": list(model.events.values())}


def to_rdf(model, info):
    g = Graph()
    g.bind("chu", CHU)
    g.bind("prov", PROV)
    g.add((CHU.referenceProfile, RDF.type, PROV.Entity))
    g.add((CHU.referenceProfile, CHU.authority, Literal("SECONDARY_AI")))
    g.add((CHU.referenceProfile, PROV.wasAttributedTo, URIRef("urn:chu:agent:reference")))
    g.add((CHU.referenceProfile, PROV.wasDerivedFrom, URIRef("https://www.w3.org/TR/swbp-n-aryRelations/")))
    for state in model.states.values():
        subject = URIRef(state.cid)
        g.add((subject, RDF.type, CHU.Snapshot))
        g.add((subject, RDF.type, PROV.Entity))
        for name, data in state.nodes:
            node = URIRef(name)
            g.add((subject, CHU.containsNode, node))
            g.add((node, RDF.type, CHU.Node))
            g.add((node, CHU.byteLength, Literal(len(data), datatype=XSD.integer)))
        for edge in state.edges:
            eid = URIRef(edge.cid)
            g.add((subject, CHU.containsEdge, eid))
            g.add((eid, RDF.type, CHU.Hyperedge))
            g.add((eid, CHU.relationType, Literal(edge.relation)))
            g.add((eid, CHU.arity, Literal(len(edge.participants))))
            for ordinal, part in enumerate(edge.participants):
                incidence = URIRef(f"{edge.cid}:incidence:{ordinal}")
                g.add((eid, CHU.hasIncidence, incidence))
                g.add((incidence, RDF.type, CHU.Incidence))
                g.add((incidence, CHU.ordinal, Literal(ordinal)))
                g.add((incidence, CHU.role, Literal(part.role)))
                g.add((incidence, CHU.node, URIRef(part.node)))
    for path, name in info["sources"].items():
        g.add((URIRef(name), CHU.pathView, Literal(path)))
    for event in model.events.values():
        subject = URIRef("urn:chu:event:" + cid(encoded([event["fingerprint"], event["request"]])).split(":")[-1])
        g.add((subject, RDF.type, PROV.Activity))
        g.add((subject, CHU.base, URIRef(event["base"])))
        g.add((subject, CHU.result, URIRef(event["result"])))
        g.add((subject, CHU.operation, Literal(event["operation"])))
        g.add((subject, CHU.requestId, Literal(event["request"])))
        g.add((subject, PROV.used, URIRef(event["base"])))
        g.add((subject, PROV.generated, URIRef(event["result"])))
        g.add((subject, PROV.wasAssociatedWith, URIRef(event["actor"])))
        g.add((subject, PROV.endedAtTime, Literal(event["observed_at"], datatype=XSD.dateTime)))
        g.add((URIRef(event["actor"]), RDF.type, PROV.SoftwareAgent))
    return g


def validate_rdf(g):
    ontology = Graph().parse(ROOT / "spec/ontology.ttl")
    ok, _, report = validate(g, shacl_graph=str(ROOT / "spec/shapes.ttl"),
                             ont_graph=ontology, inference="none", meta_shacl=True)
    errors = [] if ok else [str(report)]
    for predicate in set(g.predicates()):
        if str(predicate).startswith(str(CHU)) and (predicate, RDF.type, None) not in ontology:
            errors.append("Unregistered predicate: " + str(predicate))
    for predicate, domain in ontology.subject_objects(RDFS.domain):
        for subject in g.subjects(predicate, None):
            if (subject, RDF.type, domain) not in g:
                errors.append(f"Wrong asserted domain: {subject} {predicate}")
    return {"ok": not errors, "triples": len(g), "errors": errors}


def roadmap():
    checked = subprocess.run([sys.executable, str(ROOT / "plan/check_plan.py")], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
    if checked.returncode:
        raise ValueError("Invalid plan: " + checked.stdout.strip())
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    nodes = {node["id"]: node for node in plan["nodes"]}
    done = {name for name, node in nodes.items() if node.get("status") == "done"}
    rows = []
    for name, node in nodes.items():
        prerequisites = {p for e in plan["hyperedges"] if name in e["head"] for p in e["tail"]}
        rows.append({**node, "status": "done" if name in done else "blocked" if prerequisites - done else "ready",
                     "requires": sorted(prerequisites), "blocked_by": sorted(prerequisites - done)})
    return {"schema": "chu-roadmap/v1", "source": "plan/chu_os_plan.graph.json", "tasks": rows,
            "ready": [row["id"] for row in rows if row["status"] == "ready"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["demo", "export", "check", "roadmap"])
    parser.add_argument("--json", action="store_true", help="JSON is the default except RDF export")
    parser.add_argument("--format", choices=["turtle", "json-ld", "nt"], default="turtle")
    args = parser.parse_args(argv)
    if args.action == "roadmap":
        result = roadmap()
    else:
        model, info = demo()
        g = to_rdf(model, info)
        if args.action == "export":
            print(g.serialize(format=args.format))
            return 0
        result = info if args.action == "demo" else validate_rdf(g)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())

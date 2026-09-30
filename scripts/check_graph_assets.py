#!/usr/bin/env python3
"""Verify archived RDF and portable Linux graph fixtures without rewriting history."""
import importlib.util
import json
from pathlib import Path

from pyshacl import validate
from rdflib import Graph
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    host = load("research/linux_os/to_rdf.py")
    fixture = {"nodes": [{"id": "file:one", "type": "File"},
                         {"id": "group:two", "type": "Group"},
                         {"id": "group:three", "type": "Group"}],
               "hyperedges": [{"id": "fixture", "type": "membership", "participants": [
                   {"role": "member", "node": "file:one"},
                   {"role": "group", "node": "group:two"},
                   {"role": "group", "node": "group:three"}]}]}
    graph = host.build(fixture)
    shapes = Graph().parse(ROOT / "research/linux_os/shapes.ttl")
    assert host.shacl(graph, shapes)[0], "valid n-ary fixture rejected"
    assert host.negative_control(shapes), "invalid role/arity fixtures accepted"
    roundtrip = Graph().parse(data=graph.serialize(format="json-ld"), format="json-ld")
    assert isomorphic(graph, roundtrip), "JSON-LD roundtrip changed graph semantics"
    for q in sorted((ROOT / "research/linux_os/queries").glob("*.rq")):
        list(graph.query(q.read_text()))
    findings = load("research/linux_os/findings_graph.py")
    stored = Graph().parse(ROOT / "research/linux_os/findings.ttl")
    assert isomorphic(stored, findings.build()), "findings source and archived RDF differ"
    assert validate(stored, shacl_graph=Graph().parse(data=findings.SHAPES, format="turtle"))[0]
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    assert {t for _, ts in findings.DECISIONS.values() for t in ts} <= {n["id"] for n in plan["nodes"]}
    session = load("journal/2026-09-29/session_graph.py")
    archived = Graph().parse(ROOT / "journal/2026-09-29/session.ttl")
    assert validate(archived, shacl_graph=Graph().parse(data=session.SHAPES, format="turtle"))[0]
    answers = {}
    for q in sorted((ROOT / "journal/2026-09-29/queries").glob("*.rq")):
        answers[q.stem] = [{str(k): str(v) for k, v in row.asdict().items()}
                          for row in archived.query(q.read_text())]
    assert not session.check_answers(answers), "archived competency answers changed"
    print(json.dumps({"ok": True, "host_fixture": "PASS", "negative_controls": "PASS",
                      "jsonld_roundtrip": "PASS", "findings": "PASS", "session_archive": "PASS",
                      "scope": "portable fixtures and stored evidence; not live sibling repositories or full host inventory"}))


if __name__ == "__main__":
    main()

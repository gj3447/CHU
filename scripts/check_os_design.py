#!/usr/bin/env python3
"""Validate the local OS research graph; never boot a VM or execute HSWM."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

from pyshacl import validate
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace
from rdflib.namespace import DCTERMS, PROV

from check_cli_tools import bindings, run
from chu_vm import validate_boots

ROOT = Path(__file__).resolve().parents[1]
OS = Namespace("https://github.com/gj3447/CHU/os#")
PLAN = Namespace("https://github.com/gj3447/CHU/plan#")


def design_graph():
    graph = Graph().parse(ROOT / "os/design.ttl")
    if list(graph.triples((None, OS.taskStatus, None))):
        raise ValueError("Task status must be projected from the canonical plan")
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    for node in plan["nodes"]:
        graph.add((PLAN[node["id"]], RDF.type, OS.PlanTask))
        graph.add((PLAN[node["id"]], OS.taskStatus, Literal(node.get("status", "pending"))))
    return graph


def validate_design(graph):
    ontology = Graph().parse(ROOT / "os/ontology.ttl")
    shapes = Graph().parse(ROOT / "os/design-shapes.ttl")
    valid, _, report = validate(graph, shacl_graph=shapes,
                                ont_graph=ontology, inference="none", meta_shacl=True)
    errors = [] if valid else [str(report)]

    def has_class(node, expected):
        return any(expected in ontology.transitive_objects(kind, RDFS.subClassOf)
                   for kind in graph.objects(node, RDF.type))

    for subject, predicate, obj in graph:
        if not str(predicate).startswith(str(OS)):
            continue
        if (predicate, RDF.type, RDF.Property) not in ontology:
            errors.append(f"Unregistered predicate: {predicate}")
            continue
        domain, range_ = ontology.value(predicate, RDFS.domain), ontology.value(predicate, RDFS.range)
        if not has_class(subject, domain):
            errors.append(f"Wrong predicate domain: {predicate}")
        if str(range_).startswith(str(XSD)):
            if not isinstance(obj, Literal) or (obj.datatype or XSD.string) != range_:
                errors.append(f"Wrong datatype: {predicate}")
        elif not has_class(obj, range_):
            errors.append(f"Wrong predicate range: {predicate}")
    known_tasks = {PLAN[n["id"]]: n.get("status", "pending") for n in
                   json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())["nodes"]}
    actual_tasks = {task: str(graph.value(task, OS.taskStatus))
                    for task in graph.subjects(RDF.type, OS.PlanTask)}
    if actual_tasks != known_tasks:
        errors.append("Plan projection differs from canonical task IDs/statuses")
    for artifact in graph.subjects(RDF.type, OS.Artifact):
        view = str(graph.value(artifact, OS.pathView))
        expected_authority = ("USER_PRIMARY" if view.startswith("canon/sources/USER_PRIMARY_")
                              else "SECONDARY_AI")
        if str(graph.value(artifact, OS.authority)) != expected_authority:
            errors.append(f"Artifact source authority mismatch: {artifact}")
        path = (ROOT / view).resolve()
        if (PurePosixPath(view).is_absolute() or ".." in PurePosixPath(view).parts
                or not path.is_relative_to(ROOT) or not path.is_file()):
            errors.append(f"Invalid artifact path view: {artifact}")
        elif str(artifact) != "urn:sha256:" + hashlib.sha256(path.read_bytes()).hexdigest():
            errors.append(f"Artifact byte CID mismatch: {artifact}")
    archive = Graph().parse(ROOT / "research/linux_os/findings.ttl")
    for previous in graph.objects(None, DCTERMS.replaces):
        if not list(archive.triples((previous, RDF.type, None))):
            errors.append(f"Superseded decision absent from preserved archive: {previous}")
    # Inspect the committed report only: no access to ignored serial logs or stale live runs.
    archived = json.loads((ROOT / "os/boot-verification.json").read_text())
    validate_boots(archived["boots"])
    if not archived["ok"] or archived["hswm"] != "NOT_READY":
        errors.append("Archived report exceeds the substrate evidence contract")
    for observation in graph.subjects(RDF.type, OS.Observation):
        artifact = graph.value(observation, PROV.wasDerivedFrom)
        if str(graph.value(artifact, OS.pathView)) != "os/boot-verification.json":
            errors.append("Substrate observation must cite the archived boot report")
        when = Literal(archived["ended_at"], datatype=XSD.dateTime)
        if graph.value(observation, OS.observedAt) != when:
            errors.append("Observation time differs from archived experiment end")
    return errors


def check_answers(answers):
    expected = {"R-VM-OS": {"T69"}, "R-HSWM": {"T64", "T65"}, "R-GRAPH": {"T63"},
                "R-IMAGE": {"T66"}, "R-UPDATE": {"T67"}, "R-RECOVERY": {"T68"},
                "R-SUBSTRATE": {"T62"}}
    coverage = {(row["requirement"], row["task"]) for row in answers["coverage"]}
    assert coverage == {(str(OS[req]), str(PLAN[task])) for req, tasks in expected.items()
                        for task in tasks}, "Requirement/task coverage changed"
    for req, filename in [("R-VM-OS", "USER_PRIMARY_VM_OS_HSWM_2026-09-30.txt"),
                          ("R-HSWM", "USER_PRIMARY_VM_OS_HSWM_2026-09-30.txt"),
                          ("R-GRAPH", "USER_PRIMARY_CHU_HYPERGRAPH_OS_2026-09-29.txt")]:
        cid = "urn:sha256:" + hashlib.sha256((ROOT / "canon/sources" / filename).read_bytes()).hexdigest()
        assert {r["source"] for r in answers["coverage"] if r["requirement"] == str(OS[req])} == {cid}
    decisions = answers["decisions"]
    assert {(r["decision"], r["authority"], r["status"], r["proposal"], r["replaces"])
            for r in decisions} == {(str(OS["D-linux-image"]), "SECONDARY_AI", "PROPOSED",
                                     str(OS["S-mkosi"]), "https://github.com/gj3447/CHU/research/linux_os#D04")}
    assert {r["alternative"] for r in decisions} == {str(OS[name]) for name in
                                                     ("S-buildroot", "S-yocto", "S-new-kernel")}
    assert {r["source"] for r in decisions} == {str(OS["R-VM-OS"]), "https://mkosi.systemd.io/",
                                                "https://github.com/nodejs/node/blob/v24.13.0/BUILDING.md"}
    evidence = answers["evidence"]
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == str(OS["R-SUBSTRATE"])
    assert evidence[0]["scope"] == "CLEAN_BOOT_SUBSTRATE"
    assert evidence[0]["path"] == "os/boot-verification.json"


def check(out):
    subprocess.run([sys.executable, str(ROOT / "plan/check_plan.py")], cwd=ROOT,
                   check=True, capture_output=True, timeout=30)
    graph = design_graph()
    errors = validate_design(graph)
    if errors:
        raise ValueError("\n".join(errors))
    out.mkdir(parents=True, exist_ok=True)
    graph.serialize(out / "os-design.ttl", format="turtle")
    answers = {}
    with TemporaryDirectory(prefix="chu-os-design-") as directory:
        store = Path(directory) / "store"
        run("oxigraph", "load", "--location", store, "--file", out / "os-design.ttl")
        for query in sorted((ROOT / "os/queries").glob("*.rq")):
            expected = json.loads(graph.query(query.read_text()).serialize(format="json"))
            actual = json.loads(run("oxigraph", "query", "--location", store,
                                   "--query-file", query, "--results-format", "json").stdout)
            assert bindings(expected) == bindings(actual), query.name
            answers[query.stem] = [{key: term["value"] for key, term in row.items()}
                                   for row in actual["results"]["bindings"]]
    check_answers(answers)
    (out / "os-design-answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=2) + "\n")
    return {"ok": True, "scope": "research trace and archived report consistency; not a new boot or OS acceptance",
            "triples": len(graph), "answers": answers, "engines": ["RDFLib", "Oxigraph"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.out.resolve()), ensure_ascii=False, indent=2))

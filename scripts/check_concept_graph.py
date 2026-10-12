"""Query/verify CHU concept claims locally; no shared KG writes or OS execution."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS, PROV, SKOS

from check_cli_tools import bindings, run

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "philosophy/graph"
PC = Namespace("https://github.com/gj3447/CHU/philosophy#")
REVISION = "806258fe9a7974cf9bb237d6578d2c61094eabe0"
QUERIES = {"distinction", "viewpoint", "separation", "sources"}
SOURCES = {
    "naming": ("canon/sources/USER_PRIMARY_CHU_CHU_OS_2026-10-12.txt", "USER_PRIMARY"),
    "direction": ("canon/sources/USER_PRIMARY_CHU_PHILOSOPHY_FIRST_2026-10-12.txt", "USER_PRIMARY"),
    "handoff": ("docs/CHU_CHU_OS_REPOSITORY_SPLIT.md", "SECONDARY_AI"),
}
REPO = URIRef("https://github.com/gj3447/CHU")
OS_REPO = URIRef("https://github.com/gj3447/CHU_OS")
# Acceptance expectations use existing C01/C02/C03 claim IDs and owner-reported handoff scope.
EXPECTED = {
    "C01": (PC.CHU_OS, PC.computerImplementationOf, PC.CHU, "naming", "USER_NAMING", "SOURCE_SUPPORTED"),
    "C02": (OS_REPO, PC.separateRepositoryFrom, REPO, "direction", "USER_DIRECTION", "SOURCE_SUPPORTED"),
    "C03": (PC.Universe, PC.viewedAs, PC.CHU, "naming", "USER_VIEWPOINT", "NOT_EMPIRICALLY_VALIDATED"),
    "owner-chu-20261012": (REPO, PC.ownsScope, PC.ConceptTheoryCanon, "handoff", "OWNER_REPORTED_OBSERVATION", "SOURCE_REPORTED"),
    "owner-os-20261012": (OS_REPO, PC.ownsScope, PC.OSImplementation, "handoff", "OWNER_REPORTED_OBSERVATION", "SOURCE_REPORTED"),
    "handoff-20261012": (OS_REPO, PC.handoffStatus, PC.InitialHandoffRecorded, "handoff", "OWNER_REPORTED_OBSERVATION", "SOURCE_REPORTED"),
    "consumer-switch-20261012": (PC.ConsumerMigration, PC.workStatus, PC.PendingConsumerSwitch, "handoff", "OWNER_REPORTED_OBSERVATION", "SOURCE_REPORTED"),
}


def source_id(name):
    return PC[f"source-{name}-20261012"]


def claim_graph():
    return Graph().parse(BASE / "claims.ttl")


def source_bytes(path, revision):
    view = PurePosixPath(path)
    if view.is_absolute() or ".." in view.parts or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Invalid source path/revision")
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT,
                                   stderr=subprocess.PIPE, timeout=10)


def validate_graph(graph):
    ontology = Graph().parse(BASE / "ontology.ttl")
    ok, _, report = validate(graph, shacl_graph=Graph().parse(BASE / "shapes.ttl"),
                             ont_graph=ontology, inference="none", meta_shacl=True)
    if not ok:
        return [str(report)]
    errors = []

    def has_class(node, expected):
        return any(expected in ontology.transitive_objects(kind, RDFS.subClassOf)
                   for kind in graph.objects(node, RDF.type))

    claim_predicates = set(ontology.subjects(RDF.type, PC.ClaimPredicate))
    standard = {RDF.type, RDF.subject, RDF.predicate, RDF.object, SKOS.prefLabel,
                RDFS.seeAlso, PROV.wasDerivedFrom, PROV.wasAttributedTo,
                PROV.atLocation, DCTERMS.date}
    known_types = set(ontology.subjects(RDF.type, RDFS.Class)) | {
        RDF.Statement, PROV.Entity, PROV.Agent, PROV.SoftwareAgent, PROV.Person, SKOS.Concept}
    for subject, predicate, obj in graph:
        if predicate in claim_predicates:
            errors.append("Unqualified claim assertion is forbidden; retain the claim record")
        elif predicate not in standard:
            if (predicate, RDF.type, RDF.Property) not in ontology:
                errors.append(f"Unregistered predicate: {predicate}")
                continue
            domain = ontology.value(predicate, RDFS.domain)
            range_ = ontology.value(predicate, RDFS.range)
            if not has_class(subject, domain):
                errors.append(f"Wrong metadata domain: {predicate}")
            if str(range_).startswith(str(XSD)):
                if not isinstance(obj, Literal) or (obj.datatype or XSD.string) != range_:
                    errors.append(f"Wrong metadata datatype: {predicate}")
            elif not has_class(obj, range_):
                errors.append(f"Wrong metadata range: {predicate}")
        if predicate == RDF.type and obj not in known_types:
            errors.append(f"Undeclared type or unqualified membership: {obj}")
    if set(graph.subjects(RDF.type, PC.Claim)) != {PC[k] for k in EXPECTED}:
        errors.append("Claim IDs differ from the scoped C01–C03 and handoff contract")
    if set(graph.subjects(RDF.type, PC.Source)) != {source_id(k) for k in SOURCES}:
        errors.append("Missing or extra source records")
    for key, (subject, relation, obj, source, kind, status) in EXPECTED.items():
        node = PC[key]
        fields = (RDF.subject, RDF.predicate, RDF.object, PROV.wasDerivedFrom,
                  PC.kind, PC.epistemicStatus)
        expected = (subject, relation, obj, source_id(source), Literal(kind), Literal(status))
        if tuple(graph.value(node, p) for p in fields) != expected:
            errors.append(f"Claim direction, scope, source or status differs: {key}")
        for endpoint, boundary in [(subject, RDFS.domain), (obj, RDFS.range)]:
            if not has_class(endpoint, ontology.value(relation, boundary)):
                errors.append(f"Wrong claim endpoint type: {key}")
        contexts = set(graph.objects(node, PC.context))
        if contexts != ({PC.WorldModel} if key == "C03" else set()):
            errors.append(f"Lost or unsupported qualification: {key}")
    for key, (path, authority) in SOURCES.items():
        node = source_id(key)
        expected = (Literal(path), Literal(REVISION), Literal(authority),
                    PC.User if authority == "USER_PRIMARY" else PC.Codex,
                    URIRef(f"{REPO}/blob/{REVISION}/{path}"))
        fields = (PC.pathView, PC.revision, PC.authority, PROV.wasAttributedTo, PROV.atLocation)
        if tuple(graph.value(node, p) for p in fields) != expected:
            errors.append(f"Source provenance differs: {key}")
            continue
        raw = source_bytes(path, REVISION)
        if graph.value(node, PC.content) != URIRef("urn:sha256:" + hashlib.sha256(raw).hexdigest()):
            errors.append(f"Source byte CID differs: {key}")
        for claim in graph.subjects(PROV.wasDerivedFrom, node):
            if str(graph.value(claim, PC.sourceExcerpt)) not in raw.decode():
                errors.append(f"Quote is absent from original source: {claim}")
    return errors


def query(graph, name):
    if name not in QUERIES:
        raise ValueError(f"Unknown concept query: {name}")
    return json.loads(graph.query((BASE / "queries" / (name + ".rq")).read_text())
                      .serialize(format="json"))


def values(answer):
    return [{k: v["value"] for k, v in row.items()} for row in answer["results"]["bindings"]]


def check_answers(answers):
    naming = values(answers["distinction"])
    assert len(naming) == 1 and (naming[0]["claim"], naming[0]["implementation"],
                               naming[0]["concept"], naming[0]["authority"]) == (
        str(PC.C01), str(PC.CHU_OS), str(PC.CHU), "SECONDARY_AI")
    view = values(answers["viewpoint"])
    assert len(view) == 1 and tuple(view[0][k] for k in (
        "claim", "subject", "object", "context", "kind", "epistemicStatus", "speaker")) == (
        str(PC.C03), str(PC.Universe), str(PC.CHU), str(PC.WorldModel),
        "USER_VIEWPOINT", "NOT_EMPIRICALLY_VALIDATED", str(PC.User))
    expected = {(str(PC[k]), str(s), str(p), str(o), kind, state, str(source_id(src)), REVISION)
                for k, (s, p, o, src, kind, state) in EXPECTED.items() if k not in {"C01", "C03"}}
    assert {tuple(row[k] for k in ("claim", "subject", "relation", "object", "kind",
                                   "epistemicStatus", "source", "revision"))
            for row in values(answers["separation"])} == expected
    source_rows = values(answers["sources"])
    assert len(source_rows) == len(EXPECTED)
    assert {r["claim"] for r in source_rows} == {str(PC[k]) for k in EXPECTED}
    for row in source_rows:
        key = row["claim"].removeprefix(str(PC))
        source = EXPECTED[key][3]
        path, authority = SOURCES[source]
        expected_cid = "urn:sha256:" + hashlib.sha256(source_bytes(path, REVISION)).hexdigest()
        assert (row["source"], row["path"], row["revision"], row["content"], row["sourceAuthority"]) == (
            str(source_id(source)), path, REVISION, expected_cid, authority)


def check(out):
    graph = claim_graph()
    errors = validate_graph(graph)
    if errors:
        raise ValueError("\n".join(errors))
    out.mkdir(parents=True, exist_ok=True)
    graph.serialize(out / "concept-claims.ttl", format="turtle")
    graph.serialize(out / "concept-claims.jsonld", format="json-ld")
    assert isomorphic(graph, Graph().parse(out / "concept-claims.jsonld", format="json-ld"))
    answers = {}
    with TemporaryDirectory(prefix="chu-concept-") as directory:
        store = Path(directory) / "store"
        run("oxigraph", "load", "--location", store, "--file", out / "concept-claims.ttl")
        for name in sorted(QUERIES):
            actual = json.loads(run("oxigraph", "query", "--location", store,
                                    "--query-file", BASE / "queries" / (name + ".rq"),
                                    "--results-format", "json").stdout)
            expected = query(graph, name)
            assert set(expected["head"]["vars"]) == set(actual["head"]["vars"]), name
            assert bindings(expected) == bindings(actual), name
            answers[name] = actual
    check_answers(answers)
    (out / "concept-answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=2) + "\n")
    return {"ok": True, "claims": len(EXPECTED), "pinned_sources": len(SOURCES),
            "queries": sorted(answers), "engines": ["RDFLib", "Oxigraph"],
            "jsonld_roundtrip": True, "scope": "Attributed concept graph and pinned handoff report; "
            "not HSWM runtime state, shared KG publication, new OS execution or empirical cognition proof"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("query", help="Read a named SPARQL answer with source attribution")
    p.add_argument("name", choices=sorted(QUERIES))
    p = sub.add_parser("export", help="Export attributed data; never assert claim triples")
    p.add_argument("--format", choices=["turtle", "json-ld"], default="turtle")
    p = sub.add_parser("check", help="SHACL, source pins, two SPARQL engines, JSON-LD roundtrip")
    p.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "check":
        result = check(args.out.resolve())
    else:
        graph = claim_graph()
        errors = validate_graph(graph)
        if errors:
            raise ValueError("\n".join(errors))
        if args.command == "export":
            print(graph.serialize(format=args.format))
            return 0
        result = query(graph, args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

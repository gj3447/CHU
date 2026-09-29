#!/usr/bin/env python3
"""CHU 하이퍼엣지 JSON -> RDF(Turtle/JSON-LD) + SHACL 검증 + SPARQL 질의.

표준: RDF 1.1, W3C "Defining N-ary Relations on the Semantic Web" (relation node + incidence),
SHACL 1.0 (SHACL-SPARQL 포함), SPARQL 1.1, PROV-O.
실행: uv run --with rdflib --with pyshacl python research/linux_os/to_rdf.py
출력: out/host_graph.ttl, out/query_results.json, public_summary.json (공개 커밋용 집계)
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, XSD, BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV

HERE = Path(__file__).parent
OUT = HERE / "out"
CHU = Namespace("https://github.com/gj3447/CHU/vocab#")
HOST = Namespace("urn:chu:host-snapshot:")


def iri(nid):
    return HOST[hashlib.sha256(nid.encode()).hexdigest()[:24]]


def build(data):
    g = Graph()
    g.bind("chu", CHU)
    g.bind("prov", PROV)
    for n in data["nodes"]:
        s = iri(n["id"])
        g.add((s, RDF.type, CHU.Node))
        g.add((s, CHU.kind, Literal(n["type"])))
        g.add((s, CHU.label, Literal(n["id"].split(":", 1)[1])))
        if "bytes" in n:
            g.add((s, CHU.bytes, Literal(n["bytes"], datatype=XSD.integer)))
    for e in data["hyperedges"]:
        s = HOST[e["id"]]
        g.add((s, RDF.type, CHU.Hyperedge))
        g.add((s, CHU.relationType, Literal(e["type"])))
        g.add((s, CHU.arity, Literal(len(e["participants"]), datatype=XSD.integer)))
        for k, p in enumerate(e["participants"]):
            i = BNode()
            g.add((s, CHU.hasIncidence, i))
            g.add((i, RDF.type, CHU.Incidence))
            g.add((i, CHU.role, Literal(p["role"])))
            g.add((i, CHU.node, iri(p["node"])))
            g.add((i, CHU.ordinal, Literal(k, datatype=XSD.integer)))
    act = HOST["extraction"]
    g.add((act, RDF.type, PROV.Activity))
    g.add((act, PROV.used, URIRef("file:///var/lib/dpkg/status")))
    g.add((act, PROV.endedAtTime, Literal(datetime.now(timezone.utc).isoformat(), datatype=XSD.dateTime)))
    return g


def shacl(g, shapes):
    ok, _, text = validate(g, shacl_graph=shapes, advanced=True, inference="none")
    return ok, text


def negative_control(shapes):
    """검증이 공허하지 않음을 보인다: 잘못된 하이퍼엣지 2개를 반드시 거부해야 한다."""
    bad = Graph()
    n = HOST["neg-node"]
    bad.add((n, RDF.type, CHU.Node))
    e = HOST["neg-edge-arity"]  # arity 3 이라고 주장하지만 incidence 2개
    bad.add((e, RDF.type, CHU.Hyperedge))
    bad.add((e, CHU.relationType, Literal("neg:arity")))
    bad.add((e, CHU.arity, Literal(3, datatype=XSD.integer)))
    for k in range(2):
        i = BNode()
        bad += [(e, CHU.hasIncidence, i), (i, RDF.type, CHU.Incidence), (i, CHU.role, Literal("x")),
                (i, CHU.node, n), (i, CHU.ordinal, Literal(k, datatype=XSD.integer))]
    e2 = HOST["neg-edge-norole"]  # role 없는 incidence
    bad.add((e2, RDF.type, CHU.Hyperedge))
    bad.add((e2, CHU.relationType, Literal("neg:norole")))
    bad.add((e2, CHU.arity, Literal(2, datatype=XSD.integer)))
    for k in range(2):
        i = BNode()
        bad += [(e2, CHU.hasIncidence, i), (i, RDF.type, CHU.Incidence), (i, CHU.node, n),
                (i, CHU.ordinal, Literal(k, datatype=XSD.integer))]
    ok, text = shacl(bad, shapes)
    role_path_reported = "chu:role" in text or str(CHU.role) in text
    return (not ok) and "arity differs" in text and role_path_reported


def main():
    data = json.loads((OUT / "host_graph.json").read_text())
    g = build(data)
    shapes = Graph().parse(HERE / "shapes.ttl")
    ok, text = shacl(g, shapes)
    neg = negative_control(shapes)
    g.serialize(OUT / "host_graph.ttl", format="turtle")

    results = {}
    for q in sorted((HERE / "queries").glob("*.rq")):
        rows = [{str(k): (v.toPython() if hasattr(v, "toPython") else str(v)) for k, v in r.asdict().items()}
                for r in g.query(q.read_text())]
        results[q.stem] = rows
    (OUT / "query_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str))

    # 공개 요약: 패키지·유닛·호스트 경로 이름 없이 구조만. content 결과는 공개 저장소 경로이므로 포함.
    public = {
        "schema": "chu-linux-host-graph-rdf-summary/v1",
        "triples": len(g),
        "shacl_conforms": ok,
        "shacl_negative_control_rejected": neg,
        "arity_profile": results["arity_profile"],
        "multi_membership": results["multi_membership"],
        "nary_alternatives_count_arity_ge_4": len(results["nary_alternatives"]),
        "content_identity_top": results["content_identity"][:8],
    }
    (HERE / "public_summary.json").write_text(json.dumps(public, ensure_ascii=False, indent=2, default=str) + "\n")
    print(json.dumps({k: public[k] for k in ("triples", "shacl_conforms", "shacl_negative_control_rejected")}))
    if not ok:
        print(text[:3000])
    sys.exit(0 if ok and neg else 1)


if __name__ == "__main__":
    main()

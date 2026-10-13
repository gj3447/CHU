import json
import subprocess
import sys

import pytest
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import OWL, PROV, SKOS

from check_concept_graph import (PC, ROOT, QUERIES, claim_graph, check_answers,
                                 query, source_id, validate_graph)


def test_scoped_claims_answer_questions_with_original_sources():
    graph = claim_graph()
    assert validate_graph(graph) == []
    check_answers({name: query(graph, name) for name in QUERIES})
    # Reification describes the attributed statement, without asserting it as fact.
    assert (PC.Universe, PC.viewedAs, PC.CHU) not in graph
    assert (PC.CHU_OS, OWL.sameAs, PC.CHU) not in graph
    restored = Graph().parse(data=graph.serialize(format="json-ld"), format="json-ld")
    assert isomorphic(graph, restored)
    assert validate_graph(restored) == []


@pytest.mark.parametrize("mutation", [
    "claim-authority", "proven-universe", "lost-world-model", "same-entity", "reverse-implementation",
    "bare-viewpoint", "cosmic-type", "repository-as-concept", "untyped-endpoint", "unknown-predicate",
    "forged-quote", "wrong-source", "source-authority", "source-cid", "source-revision", "outside-path",
    "extra-object", "missing-claim", "false-consumer-completion", "observation-as-user-direction",
    "cognition-only-label", "lost-brain", "brain-as-os", "scope-as-world-model", "scope-old-source",
    "cognition-required", "reversed-computable-scope", "computability-old-source",
    "hypergraph-view-as-fact", "bare-computable-scope",
])
def test_rejects_identity_evidence_and_handoff_conflation(mutation):
    graph = claim_graph()
    if mutation == "claim-authority":
        graph.set((PC.C01, PC.authority, Literal("USER_PRIMARY")))
    elif mutation == "proven-universe":
        graph.set((PC.C03, PC.epistemicStatus, Literal("SOURCE_SUPPORTED")))
    elif mutation == "lost-world-model":
        graph.remove((PC.C03, PC.context, None))
    elif mutation == "same-entity":
        graph.add((PC.CHU_OS, OWL.sameAs, PC.CHU))
    elif mutation == "reverse-implementation":
        graph.set((PC.C01, RDF.subject, PC.CHU))
        graph.set((PC.C01, RDF.object, PC.CHU_OS))
    elif mutation == "bare-viewpoint":
        graph.add((PC.Universe, PC.viewedAs, PC.CHU))
    elif mutation == "cosmic-type":
        graph.add((PC.Universe, RDF.type, PC.CHU))
    elif mutation == "repository-as-concept":
        graph.add((PC.CHU, RDF.type, PC.Repository))
    elif mutation == "untyped-endpoint":
        graph.remove((PC.CHU_OS, RDF.type, None))
    elif mutation == "unknown-predicate":
        graph.add((PC.C01, URIRef("urn:unknown:relation"), PC.CHU))
    elif mutation == "forged-quote":
        graph.set((PC.C03, PC.sourceExcerpt, Literal("우주 인지능력이 실험으로 입증됨")))
    elif mutation == "wrong-source":
        graph.set((PC.C03, PROV.wasDerivedFrom, source_id("direction")))
    elif mutation == "source-authority":
        graph.set((source_id("handoff"), PC.authority, Literal("USER_PRIMARY")))
    elif mutation == "source-cid":
        fake = URIRef("urn:sha256:" + "0" * 64)
        graph.add((fake, RDF.type, PROV.Entity))
        graph.set((source_id("naming"), PC.content, fake))
    elif mutation == "source-revision":
        graph.set((source_id("naming"), PC.revision, Literal("0" * 40)))
    elif mutation == "outside-path":
        graph.set((source_id("naming"), PC.pathView, Literal("../private.txt")))
    elif mutation == "extra-object":
        graph.add((PC.C01, RDF.object, PC.WorldModel))
    elif mutation == "missing-claim":
        graph.remove((PC["consumer-switch-20261012"], None, None))
    elif mutation == "false-consumer-completion":
        graph.set((PC["consumer-switch-20261012"], RDF.object, PC.InitialHandoffRecorded))
    elif mutation == "observation-as-user-direction":
        graph.set((PC["handoff-20261012"], PC.kind, Literal("USER_DIRECTION")))
    elif mutation == "cognition-only-label":
        graph.set((PC.CHU, SKOS.prefLabel, Literal("CHU — 인지능력체 개념")))
    elif mutation == "lost-brain":
        graph.remove((PC.C13, None, None))
    elif mutation == "brain-as-os":
        graph.set((PC.C13, RDF.object, PC.CHU_OS))
    elif mutation == "scope-as-world-model":
        graph.set((PC.C13, PC.context, PC.WorldModel))
    elif mutation == "scope-old-source":
        graph.set((source_id("scope"), PC.revision, graph.value(source_id("naming"), PC.revision)))
    elif mutation == "cognition-required":
        graph.set((PC.C16, RDF.predicate, PC.includesAllOf))
    elif mutation == "reversed-computable-scope":
        graph.set((PC.C15, RDF.subject, PC.ComputableThings))
        graph.set((PC.C15, RDF.object, PC.CHU))
    elif mutation == "computability-old-source":
        graph.set((PC.C15, PROV.wasDerivedFrom, source_id("scope")))
    elif mutation == "hypergraph-view-as-fact":
        graph.set((PC.C17, PC.epistemicStatus, Literal("SOURCE_SUPPORTED")))
    elif mutation == "bare-computable-scope":
        graph.add((PC.CHU, PC.includesAllOf, PC.ComputableThings))
    assert validate_graph(graph), mutation


def test_cli_returns_sources_from_outside_checkout_and_rejects_unknown_query(tmp_path):
    argv = [sys.executable, str(ROOT / "scripts/chu_dev.py"), "concept", "query"]
    result = subprocess.run([*argv, "viewpoint"], cwd=tmp_path, capture_output=True, text=True,
                            check=True, timeout=15)
    rows = json.loads(result.stdout)["results"]["bindings"]
    row = next(r for r in rows if r["claim"]["value"] == str(PC.C03))
    assert row["epistemicStatus"]["value"] == "NOT_EMPIRICALLY_VALIDATED"
    assert row["source"]["value"] == str(source_id("naming"))
    scope = {r["subject"]["value"]: r for r in rows
             if r["context"]["value"] == str(PC.PhilosophicalScope)
             and r["object"]["value"] == str(PC.CHU)}
    assert set(scope) == {str(PC.Computer), str(PC.HumanBrain), str(PC.Universe)}
    assert all(r["source"]["value"] == str(source_id("scope")) for r in scope.values())
    worldview = next(r for r in rows if r["claim"]["value"] == str(PC.C17))
    assert worldview["subject"]["value"] == str(PC.Everything)
    assert worldview["object"]["value"] == str(PC.HypergraphStructure)
    assert worldview["source"]["value"] == str(source_id("computability"))
    invalid = subprocess.run([*argv, "missing"], cwd=tmp_path, capture_output=True, text=True,
                             timeout=15)
    assert invalid.returncode != 0


def test_cli_answers_computable_scope_without_cognitive_membership_or_truth_promotion(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "scripts/chu_dev.py"),
                             "concept", "query", "scope"], cwd=tmp_path,
                            capture_output=True, text=True, check=True, timeout=15)
    rows = {row["claim"]["value"]: row for row in json.loads(result.stdout)["results"]["bindings"]}
    included, optional, worldview = (rows[str(PC[key])] for key in ["C15", "C16", "C17"])
    assert (included["relation"]["value"], included["object"]["value"]) == (
        str(PC.includesAllOf), str(PC.ComputableThings))
    assert (optional["relation"]["value"], optional["object"]["value"]) == (
        str(PC.doesNotRequire), str(PC.Cognition))
    assert worldview["epistemicStatus"]["value"] == "NOT_EMPIRICALLY_VALIDATED"
    assert all(row["authority"]["value"] == "SECONDARY_AI" for row in rows.values())
    assert all(row["speaker"]["value"] == str(PC.User) for row in rows.values())
    assert all(row["source"]["value"] == str(source_id("computability")) for row in rows.values())


def test_cli_exports_qualified_graph_only(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "scripts/chu_dev.py"),
                             "concept", "export", "--format", "json-ld"], cwd=tmp_path,
                            capture_output=True, text=True, check=True, timeout=15)
    restored = Graph().parse(data=result.stdout, format="json-ld")
    assert isomorphic(claim_graph(), restored)

import json
import subprocess
from copy import deepcopy

import pytest
from rdflib import RDF, Literal, URIRef
from rdflib.namespace import PROV

from chu_model import (CHU, ROOT, Change, Edge, Incidence, Model, State, cid, demo,
                       group, members, roadmap, to_rdf, validate_rdf)

# pySHACL's SPARQL implementation currently triggers these RDFLib deprecations
# once per graph access. Retain the notices without tens of thousands of copies.
pytestmark = [pytest.mark.filterwarnings("once:Dataset.default_context is deprecated.*:DeprecationWarning:rdflib.graph"),
              pytest.mark.filterwarnings("once:Dataset.identifier is deprecated.*:DeprecationWarning:rdflib.graph")]


def test_content_identity_order_and_independent_event_identity():
    assert cid(b"abc") == "urn:sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    model = Model()
    change = Change("create", add_nodes=(b"abc", b"abc", b"group"))
    base = model.apply(model.initial, change, "one")
    assert len(model.states[base].nodes) == 2
    assert model.apply(model.initial, change, "one") == base and len(model.events) == 1
    assert model.apply(model.initial, change, "two") == base and len(model.events) == 2
    assert State(tuple(reversed(model.states[base].nodes))).cid == base
    assert group(cid(b"group"), cid(b"abc")).cid != group(cid(b"abc"), cid(b"group")).cid
    before = deepcopy(model.events)
    with pytest.raises(ValueError, match="reused"):
        model.apply(model.initial, Change("create", add_nodes=(b"changed",)), "one")
    assert model.events == before


@pytest.mark.parametrize("case", ["dangling", "unknown-type", "wrong-role", "missing-remove", "delete-referenced", "wrong-operation"])
def test_rewrite_rejection_is_atomic(case):
    model, info = demo()
    base = info["linked"]
    node = info["shared_content"]
    changes = {
        "dangling": Change("link", add_edges=(group(node, cid(b"absent")),)),
        "unknown-type": Change("link", add_edges=(Edge("anything", (Incidence("x", node),)),)),
        "wrong-role": Change("link", add_edges=(Edge("group", (Incidence("member", node), Incidence("member", node))),)),
        "missing-remove": Change("unlink", remove_edges=(cid(b"absent"),)),
        "delete-referenced": Change("delete", remove_nodes=(node,)),
        "wrong-operation": Change("create", remove_nodes=(node,)),
    }
    before = deepcopy((model.states, model.events))
    with pytest.raises(ValueError):
        model.apply(base, changes[case], "bad-request")
    assert (model.states, model.events) == before


def test_two_views_branch_isolation_retag_and_explicit_delete():
    model, info = demo()
    left_group, right_group = info["groups"]
    common = info["shared_content"]
    linked = model.states[info["linked"]]
    assert common in members(linked, left_group) and common in members(linked, right_group)
    assert members(model.states[info["branches"][0]], left_group) == []
    assert common in members(model.states[info["branches"][0]], right_group)
    assert members(model.states[info["branches"][1]], right_group) == []
    edge = next(e for e in linked.edges if e.relation == "group" and e.participants[0].node == left_group)
    updated = model.apply(info["linked"], Change("retag", add_edges=(group(left_group, common),),
                                              remove_edges=(edge.cid,)), "retag")
    assert members(model.states[updated], left_group) == [common]
    incident = tuple(e.cid for e in model.states[updated].edges if any(p.node == common for p in e.participants))
    deleted = model.apply(updated, Change("delete", remove_nodes=(common,), remove_edges=incident), "delete")
    assert common not in dict(model.states[deleted].nodes)
    assert common in dict(linked.nodes)  # old content and branch remain available


def test_registered_hypergraph_cycles_are_allowed():
    model = Model()
    a, b = cid(b"a"), cid(b"b")
    base = model.apply(model.initial, Change("create", add_nodes=(b"a", b"b")), "create")
    result = model.apply(base, Change("link", add_edges=(group(a, b), group(b, a))), "cycle")
    model.states[result].validate()
    assert members(model.states[result], a) == [b] and members(model.states[result], b) == [a]


def test_competency_answers_are_subjects_and_grouped_alternatives():
    model, info = demo()
    g = to_rdf(model, info)
    assert validate_rdf(g)["ok"]
    assert {p.rsplit(".", 1)[-1] for p in info["sources"]} == {"md", "json", "rs", "py", "lean"}
    rows = list(g.query((ROOT / "spec/queries/membership.rq").read_text()))
    pairs = {(str(row.group), str(row.member)) for row in rows if str(row.state) == info["linked"]}
    assert {(gid, info["shared_content"]) for gid in info["groups"]} <= pairs
    rows = list(g.query((ROOT / "spec/queries/alternatives.rq").read_text()))
    rows = [row for row in rows if str(row.state) == info["linked"]]
    assert len({row.clause for row in rows}) == 1
    assert {str(row.candidate) for row in rows} == set(info["groups"])
    assert {str(row.subject) for row in rows} == {info["sources"]["plan/chu_os_plan.graph.json"]}
    branches = list(g.query((ROOT / "spec/queries/branches.rq").read_text()))
    assert {str(row.result) for row in branches if str(row.base) == info["linked"]} == set(info["branches"])


@pytest.mark.parametrize("mutation", ["unknown-predicate", "wrong-domain", "bad-cid", "dangling", "duplicate-position",
                                     "position-gap", "arity", "role", "unknown-relation", "cross-state", "no-actor", "authority"])
def test_shacl_and_schema_reject_malformed_exports(mutation):
    model, info = demo()
    g = to_rdf(model, info)
    state = URIRef(info["linked"])
    edge = next(g.subjects(CHU.relationType, Literal("group")))
    incidences = list(g.objects(edge, CHU.hasIncidence))
    node = URIRef(info["shared_content"])
    if mutation == "unknown-predicate":
        g.add((node, CHU.unknown, Literal(1)))
    elif mutation == "wrong-domain":
        g.add((state, CHU.byteLength, Literal(1)))
    elif mutation == "bad-cid":
        g.add((URIRef("urn:not-a-cid"), RDF.type, CHU.Node))
        g.add((URIRef("urn:not-a-cid"), CHU.byteLength, Literal(0)))
    elif mutation == "dangling":
        g.set((incidences[0], CHU.node, URIRef("urn:missing")))
    elif mutation == "duplicate-position":
        g.set((incidences[0], CHU.ordinal, g.value(incidences[1], CHU.ordinal)))
    elif mutation == "position-gap":
        g.set((incidences[0], CHU.ordinal, Literal(9)))
    elif mutation == "arity":
        g.set((edge, CHU.arity, Literal(99)))
    elif mutation == "role":
        g.set((incidences[0], CHU.role, Literal("not-a-role")))
    elif mutation == "unknown-relation":
        g.set((edge, CHU.relationType, Literal("not-registered")))
    elif mutation == "cross-state":
        g.remove((state, CHU.containsNode, node))
    elif mutation == "no-actor":
        g.remove((None, PROV.wasAssociatedWith, None))
    elif mutation == "authority":
        g.set((CHU.referenceProfile, CHU.authority, Literal("USER_PRIMARY")))
    assert not validate_rdf(g)["ok"]


def test_agent_model_interface_and_ready_tasks(tmp_path):
    result = subprocess.run([str(ROOT / "chu"), "model", "demo", "--json"], cwd=tmp_path,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    info = json.loads(result.stdout)
    assert len(info["branches"]) == 2 and len(info["events"]) == 4
    rows = roadmap()["tasks"]
    assert all(row["status"] != "ready" or not row["blocked_by"] for row in rows)
    assert next(row for row in rows if row["id"] == "T12")["blocked_by"] == ["T11"]

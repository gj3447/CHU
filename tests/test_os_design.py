import pytest
from rdflib import Literal, URIRef
from rdflib.namespace import PROV

from check_os_design import OS, PLAN, design_graph, validate_design


def test_os_design_cites_real_bytes_and_keeps_proposal_separate_from_user_source():
    assert validate_design(design_graph()) == []


@pytest.mark.parametrize("mutation", ["authority", "adoption", "fake-task", "fake-cid",
                                     "complete-os", "hswm-evidence", "unknown-predicate",
                                     "wrong-domain", "wrong-time", "outside-path",
                                     "source-authority", "report-authority", "byte-cid"])
def test_os_design_rejects_unsupported_claims(mutation):
    graph = design_graph()
    decision, observation = OS["D-linux-image"], OS["O-clean-boots-20261001"]
    if mutation == "authority":
        graph.set((decision, OS.authority, Literal("USER_PRIMARY")))
    elif mutation == "adoption":
        graph.set((decision, OS.status, Literal("ADOPTED")))
    elif mutation == "fake-task":
        graph.set((OS["R-VM-OS"], OS.plannedBy, PLAN.T999))
    elif mutation == "fake-cid":
        graph.set((observation, PROV.wasDerivedFrom, URIRef("urn:sha256:" + "0" * 64)))
    elif mutation == "complete-os":
        graph.set((observation, OS.claimScope, Literal("COMPLETE_OS")))
    elif mutation == "hswm-evidence":
        graph.set((observation, OS.reportsOn, OS["R-HSWM"]))
    elif mutation == "unknown-predicate":
        graph.add((decision, OS.installed, Literal(True)))
    elif mutation == "wrong-domain":
        graph.add((decision, OS.plannedBy, PLAN.T66))
    elif mutation == "wrong-time":
        graph.set((observation, OS.observedAt, Literal("2026-10-02")))
    elif mutation == "outside-path":
        artifact = graph.value(observation, PROV.wasDerivedFrom)
        graph.set((artifact, OS.pathView, Literal("../outside.json")))
    elif mutation == "source-authority":
        artifact = graph.value(OS["R-VM-OS"], PROV.wasDerivedFrom)
        graph.set((artifact, OS.authority, Literal("SECONDARY_AI")))
    elif mutation == "report-authority":
        artifact = graph.value(observation, PROV.wasDerivedFrom)
        graph.set((artifact, OS.authority, Literal("USER_PRIMARY")))
    elif mutation == "byte-cid":
        artifact = graph.value(observation, PROV.wasDerivedFrom)
        graph.set((artifact, OS.pathView, Literal("os/inputs.lock.json")))
    assert validate_design(graph), mutation

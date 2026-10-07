import copy
import json
import subprocess

import pytest
from rdflib import Literal, RDF, URIRef

from chu_dev import DEV, ROOT
from chu_repo import ENG, PLAN, build, local_jsonld_contexts, query, scan_syntax_and_links, source_files, validate_graph


@pytest.fixture(scope="module")
def sources():
    return source_files()


def test_inventory_answers_cover_sources_and_preserve_profile_boundaries(sources):
    dataset, summary = build(sources)
    assert validate_graph(dataset, sources) == []
    rows = {r["path"]: r for r in query(dataset, "files")}
    assert set(rows) == set(sources)
    assert rows["AGENTS.md"]["content"] == rows["CLAUDE.md"]["content"]
    assert rows["AGENTS.md"]["representation"] != rows["CLAUDE.md"]["representation"]
    primary = {p for p, row in rows.items() if row["authority"] == "USER_PRIMARY"}
    assert primary == {p for p in sources if p.startswith("canon/sources/USER_PRIMARY_")}
    assert len(primary) == 8
    assert rows["canon/VM_OS_TARGET.md"]["authority"] == "SECONDARY_AI"
    assert rows["journal/2026-09-29/session.ttl"]["lifecycle"] == "HISTORICAL"
    assert summary["profiles"] == 12
    assets = query(dataset, "assets")
    assert any(r["profile"] == str(ENG["profile-model"]) and r["path"] == "spec/shapes.ttl"
               and r["role"] == "shapes" for r in assets)
    assert len(dataset.default_graph) == 0
    for path in ("spec/ontology.ttl", "research/linux_os/shapes.ttl", "journal/2026-09-29/session.ttl"):
        assert len(dataset.graph(URIRef(rows[path]["representation"]))) > 0
    # Reused namespace symbols in an archive cannot change current inventory authority.
    dataset.graph(URIRef(rows["journal/2026-09-29/session.ttl"]["representation"])).add(
        (URIRef(rows["README.md"]["representation"]), ENG.authority, Literal("USER_PRIMARY")))
    assert {r["path"] for r in query(dataset, "files") if r["authority"] == "USER_PRIMARY"} == primary
    assert {r["path"] for r in query(dataset, "source-graphs")} == {
        "dev/catalog.ttl", "os/design.ttl", "research/linux_os/findings.ttl"}


def test_alias_paths_share_content_but_keep_source_authority_context(sources):
    files = dict(sources)
    primary = "canon/sources/USER_PRIMARY_VM_OS_HSWM_2026-09-30.txt"
    files["docs/source-copy.md"] = files[primary]
    dataset, _ = build(files)
    rows = {r["path"]: r for r in query(dataset, "files")}
    assert rows[primary]["content"] == rows["docs/source-copy.md"]["content"]
    assert rows[primary]["authority"] == "USER_PRIMARY"
    assert rows["docs/source-copy.md"]["authority"] == "SECONDARY_AI"
    assert validate_graph(dataset, files) == []


def test_identical_rdf_bytes_keep_separate_source_contexts_without_blank_node_duplication(sources):
    files = dict(sources)
    files["dev/copy.ttl"] = files["dev/catalog.ttl"]
    config = json.loads(files["engineering/catalog.json"])
    config["profiles"][0]["assets"]["data"].append("dev/copy.ttl")
    files["engineering/catalog.json"] = json.dumps(config).encode()
    dataset, _ = build(files)
    rows = {r["path"]: r for r in query(dataset, "files")}
    original, copied = rows["dev/catalog.ttl"], rows["dev/copy.ttl"]
    assert original["content"] == copied["content"]
    assert original["representation"] != copied["representation"]
    first = dataset.graph(URIRef(original["representation"]))
    second = dataset.graph(URIRef(copied["representation"]))
    assert len(first) == len(second) > 0
    first.add((DEV.catalog, ENG.testMarker, Literal("only first")))
    assert not list(second.triples((None, ENG.testMarker, None)))


def test_final_and_gate_and_historical_freshness_are_queryable(sources):
    dataset, _ = build(sources)
    rows = [r for r in query(dataset, "plan") if r["gate"] == str(PLAN.E37)]
    assert {r["tail"] for r in rows} == {str(PLAN[f"T{x}"]) for x in range(63, 69)}
    assert {r["head"] for r in rows} == {str(PLAN.T69)}
    evidence = {r["path"]: r for r in query(dataset, "evidence")}
    assert evidence["scripts/chu_vm.py"]["freshness"] == "CHANGED"
    assert evidence["os/guest-probe.mjs"]["freshness"] == "MATCH"
    assert all(row["freshness"] == "UNAVAILABLE" for p, row in evidence.items() if p.startswith(".chu/"))
    assert {r["gap"] for r in query(dataset, "gaps")} >= {
        str(ENG["gap-hswm"]), str(ENG["gap-legacy-vocabulary"])}


@pytest.mark.parametrize("mutation", ["authority", "missing-file", "fake-cid", "gate", "freshness", "predicate", "check",
                                     "recorded-evidence", "missing-evidence", "missing-asset", "false-done"])
def test_inventory_rejects_false_metadata(sources, mutation):
    dataset, _ = build(sources)
    graph = dataset.graph(ENG.inventory)
    representation = graph.value(None, DEV.pathView, Literal("README.md"))
    if mutation == "authority":
        graph.set((representation, ENG.authority, Literal("USER_PRIMARY")))
    elif mutation == "missing-file":
        graph.remove((representation, ENG.content, None))
    elif mutation == "fake-cid":
        graph.set((representation, ENG.content, URIRef("urn:sha256:" + "0" * 64)))
    elif mutation == "gate":
        graph.remove((PLAN.E37, ENG.tailTask, PLAN.T68))
    elif mutation == "freshness":
        binding = next(graph.subjects(RDF.type, ENG.EvidenceBinding))
        graph.set((binding, ENG.freshness, Literal("MATCH")))
        graph.remove((binding, ENG.currentContent, None))
    elif mutation == "predicate":
        graph.add((representation, ENG.pretend, Literal(True)))
    elif mutation == "check":
        graph.set((ENG["profile-model"], ENG.validatedBy, DEV.unknown))
    elif mutation == "recorded-evidence":
        # There is both a representation and an evidence binding for a current source path.
        binding = next(n for n in graph.subjects(RDF.type, ENG.EvidenceBinding)
                       if graph.value(n, DEV.pathView) == Literal("scripts/chu_vm.py"))
        graph.set((binding, ENG.recordedContent, graph.value(binding, ENG.currentContent)))
        graph.set((binding, ENG.freshness, Literal("MATCH")))
    elif mutation == "missing-evidence":
        binding = next(graph.subjects(RDF.type, ENG.EvidenceBinding))
        graph.remove((binding, None, None))
    elif mutation == "missing-asset":
        binding = next(graph.subjects(RDF.type, ENG.AssetBinding))
        graph.remove((binding, None, None))
    elif mutation == "false-done":
        graph.set((PLAN.T69, ENG.taskStatus, Literal("done")))
    assert validate_graph(dataset, sources), mutation


@pytest.mark.parametrize("mutation", ["unclassified", "unprofiled-rdf", "missing-asset", "unknown-check", "duplicate-id"])
def test_catalog_rejects_silent_omissions(sources, mutation):
    files = dict(sources)
    config = copy.deepcopy(json.loads(files["engineering/catalog.json"]))
    if mutation == "unclassified":
        files["unclassified.txt"] = b"new"
    elif mutation == "unprofiled-rdf":
        files["os/unprofiled.ttl"] = b"<urn:a> <urn:b> <urn:c> ."
    elif mutation == "missing-asset":
        config["profiles"][0]["assets"]["data"].append("dev/missing.ttl")
    elif mutation == "unknown-check":
        config["profiles"][0]["checks"] = ["missing"]
    elif mutation == "duplicate-id":
        config["collections"].append(config["collections"][0])
    files["engineering/catalog.json"] = json.dumps(config).encode()
    with pytest.raises(ValueError):
        build(files)


def test_syntax_and_owned_link_check_does_not_follow_workspace_or_web():
    files = {"README.md": b"[yes](docs/ok.md) [no](docs/missing.md) [sibling](../other/x.md) [web](https://example.com/x)",
             "docs/ok.md": b"# okay"}
    scan = scan_syntax_and_links(files)
    assert scan["broken_local_links"] == [{"source": "README.md", "target": "docs/missing.md"}]
    assert scan["workspace_links_not_checked"] == 1


@pytest.mark.parametrize("document", [
    {"@context": "https://example.invalid/context"},
    {"@graph": [{"@context": [None, "https://example.invalid/nested"]}]},
    {"@context": {"@import": "https://example.invalid/imported"}},
])
def test_inventory_jsonld_never_dereferences_remote_contexts(document):
    with pytest.raises(ValueError, match="contexts"):
        local_jsonld_contexts(document)


def test_repo_cli_works_outside_checkout_and_has_bounded_queries(tmp_path):
    result = subprocess.run([str(ROOT / "chu"), "repo", "query", "files", "--path", "spec/IDENTITY.md", "--json"],
                            cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    rows = json.loads(result.stdout)
    assert len(rows) == 1 and rows[0]["path"] == "spec/IDENTITY.md"

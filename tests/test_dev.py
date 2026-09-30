import json
import subprocess
import sys

import pytest
from rdflib import RDF, Graph, Literal
from rdflib.compare import isomorphic
from rdflib.namespace import PROV

import chu_dev as dev


def test_catalog_and_competency_answers():
    assert dev.graph_validate()["ok"]
    tools = {r["tool"].split("#")[-1]: r for r in dev.query("tools")}
    assert set(tools) == {"python", "uv", "rust", "lean", "rdflib", "pyshacl", "ruff", "pytest", "actionlint"}
    assert tools["pyshacl"]["source"] == "https://github.com/RDFLib/pySHACL"
    checks = dev.query("checks")
    assert {r["tool"] for r in checks if r["check"] == str(dev.DEV.truncation)} == {
        str(dev.DEV.python), str(dev.DEV.lean)}
    assert {r["source"] for r in dev.query("sources") if r["subject"] == str(dev.DEV.catalog)} >= {
        "https://www.w3.org/TR/shacl/", "https://www.w3.org/TR/prov-o/"}


@pytest.mark.parametrize("mutation", ["dangling-tool", "no-source", "two-versions", "authority", "predicate", "domain", "cycle", "pin-drift"])
def test_graph_rejects_invalid_controls(mutation):
    g = dev.catalog()
    if mutation == "dangling-tool":
        g.add((dev.DEV.plan, dev.DEV.requires, dev.DEV.missing))
    elif mutation == "no-source":
        g.remove((dev.DEV.pyshacl, PROV.wasDerivedFrom, None))
    elif mutation == "two-versions":
        g.add((dev.DEV.python, dev.DEV.version, Literal("0.0")))
    elif mutation == "authority":
        g.set((dev.DEV.catalog, dev.DEV.authority, Literal("USER_PRIMARY")))
    elif mutation == "predicate":
        g.add((dev.DEV.python, dev.DEV.unknownPredicate, Literal("x")))
    elif mutation == "domain":
        g.add((dev.DEV.plan, dev.DEV.version, Literal("1")))
    elif mutation == "cycle":
        head = g.value(dev.DEV.plan, dev.DEV.argv)
        g.set((head, RDF.rest, head))
    elif mutation == "pin-drift":
        g.set((dev.DEV.lean, dev.DEV.version, Literal("0.0")))
    assert not dev.graph_validate(g)["ok"]


def test_catalog_roundtrip_preserves_identity_and_order():
    original = dev.catalog()
    restored = Graph().parse(data=original.serialize(format="json-ld"), format="json-ld")
    assert isomorphic(original, restored)
    assert dev.commands(original) == dev.commands(restored)


@pytest.mark.parametrize("argv,timeout,status", [
    ([sys.executable, "-c", "raise SystemExit(7)"], 10, "FAIL"),
    (["/not-a-real-chu-executable"], 10, "ERROR"),
    ([sys.executable, "-c", "import time; time.sleep(10)"], 0.1, "TIMEOUT"),
])
def test_runner_does_not_report_execution_failures_as_pass(argv, timeout, status):
    assert dev.execute(argv, timeout)["status"] == status


def test_cli_from_another_directory_and_unknown_check(tmp_path):
    cli = dev.ROOT / "chu"
    result = subprocess.run([str(cli), "tools", "--json"], cwd=tmp_path,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert any(row["tool"] == str(dev.DEV.pyshacl) for row in json.loads(result.stdout))
    bad = subprocess.run([str(cli), "check", "--only", "not-registered", "--json"],
                         cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert bad.returncode == 2
    assert not json.loads(bad.stdout)["ok"]


def test_evidence_roundtrip_and_failed_observation_query(tmp_path):
    report = {"run_id": "00000000-0000-4000-8000-000000000001",
              "started_at": "2026-09-30T00:00:00+00:00", "ended_at": "2026-09-30T00:00:01+00:00",
              "source_sha256": {"one.txt": "a" * 64, "alias.txt": "a" * 64},
              "checks": [{"id": "plan", "uri": str(dev.DEV.plan), "status": "FAIL"}]}
    dev.write_evidence(report, tmp_path)
    g = dev.catalog() + Graph().parse(tmp_path / "evidence.ttl")
    assert dev.graph_validate(g)["ok"]
    result = list(g.query((dev.ROOT / "dev/queries/failures.rq").read_text()))
    assert len(result) == 1 and str(result[0].check) == str(dev.DEV.plan)
    assert str(result[0].status) == "FAIL"
    entities = set(g.subjects(dev.DEV.pathView, None))
    assert len(entities) == 1  # two path projections, one content identity


def test_portable_truncation_path():
    from check_graph_assets import load
    checker = load("chu_core_prototype/trunc_collapse_realized_check.py")
    assert checker.LEAN == dev.ROOT / "lean/CHU_WolframRewrite.lean"
    assert checker.LEAN.is_file()


def test_download_rejects_checksum_mismatch():
    from download_tool import extract_verified
    with pytest.raises(ValueError, match="checksum"):
        extract_verified(b"wrong release bytes", {"sha256": "0" * 64, "member": "tool"})


def test_bootstrap_recognizes_existing_exact_lean_toolchain(monkeypatch):
    import bootstrap
    monkeypatch.setattr(bootstrap.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(
        a, 0, "leanprover/lean4:v4.34.1 (default)\nleanprover/lean4:v4.33.0\n", ""))
    assert bootstrap.lean_is_installed("leanprover/lean4:v4.34.1")
    assert not bootstrap.lean_is_installed("leanprover/lean4:v4.34")

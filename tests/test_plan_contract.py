import copy
import json
import subprocess
import sys

import pytest

import chu_model
from chu_model import ROOT, roadmap


@pytest.mark.parametrize("mutation", ["duplicate-node", "duplicate-edge", "missing-gate", "dangling", "empty-tail", "done-too-early"])
def test_plan_rejects_invalid_engineering_contract(tmp_path, mutation):
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    if mutation == "duplicate-node":
        plan["nodes"].append(plan["nodes"][0])
    elif mutation == "duplicate-edge":
        plan["hyperedges"].append(plan["hyperedges"][0])
    elif mutation == "missing-gate":
        plan["nodes"][0]["verify"] = ""
    elif mutation == "dangling":
        plan["hyperedges"][0]["tail"].append("T_NOT_PRESENT")
    elif mutation == "empty-tail":
        plan["hyperedges"][0]["tail"] = []
    elif mutation == "done-too-early":
        next(n for n in plan["nodes"] if n["id"] == "T12")["status"] = "done"
    (tmp_path / "chu_os_plan.graph.json").write_text(json.dumps(plan))
    script = tmp_path / "check_plan.py"
    script.write_bytes((ROOT / "plan/check_plan.py").read_bytes())
    result = subprocess.run([sys.executable, str(script)], cwd=tmp_path,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 1 and "FAIL" in result.stdout
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("mutation", [
    "root-list", "schema", "nodes-container", "node-object", "node-id", "status", "status-unhashable",
    "effort-bool", "effort-infinite", "effort-huge", "edge-endpoint-duplicates", "evidence-not-object",
    "evidence-missing-checks", "evidence-invalid-date", "evidence-unsafe-source", "evidence-empty-check",
])
def test_plan_rejects_malformed_v1_structure_without_reading_evidence_files(tmp_path, mutation):
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    if mutation == "root-list":
        plan = []
    elif mutation == "schema":
        plan["schema"] = "other-plan/v1"
    elif mutation == "nodes-container":
        plan["nodes"] = {}
    elif mutation == "node-object":
        plan["nodes"][0] = "not-an-object"
    elif mutation == "node-id":
        plan["nodes"][0]["id"] = 1
    elif mutation == "status":
        plan["nodes"][0]["status"] = "running"
    elif mutation == "status-unhashable":
        plan["nodes"][0]["status"] = []
    elif mutation == "effort-bool":
        plan["nodes"][0]["effort"] = True
    elif mutation == "effort-infinite":
        plan["nodes"][0]["effort"] = float("inf")
    elif mutation == "effort-huge":
        plan["nodes"][0]["effort"] = 10 ** 400
    elif mutation == "edge-endpoint-duplicates":
        plan["hyperedges"][0]["tail"] *= 2
    elif mutation == "evidence-not-object":
        plan["nodes"][0]["completion_evidence"] = "PASS"
    elif mutation == "evidence-missing-checks":
        plan["nodes"][0]["completion_evidence"] = {
            "date": "2026-10-02", "scope": "declared only", "source": "spec/DATA_MODEL.md"
        }
    elif mutation == "evidence-invalid-date":
        plan["nodes"][0]["completion_evidence"] = {
            "date": "not-a-date", "scope": "declared only", "source": "spec/DATA_MODEL.md", "checks": ["old free-text label"]
        }
    elif mutation == "evidence-unsafe-source":
        plan["nodes"][0]["completion_evidence"] = {
            "date": "2026-10-02", "scope": "declared only", "source": "../outside.md", "checks": ["old free-text label"]
        }
    elif mutation == "evidence-empty-check":
        plan["nodes"][0]["completion_evidence"] = {
            "date": "2026-10-02", "scope": "declared only", "source": "does-not-need-to-exist.md", "checks": [""]
        }
    (tmp_path / "chu_os_plan.graph.json").write_text(json.dumps(plan))
    script = tmp_path / "check_plan.py"
    script.write_bytes((ROOT / "plan/check_plan.py").read_bytes())
    result = subprocess.run([sys.executable, str(script)], cwd=tmp_path,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 1 and "FAIL" in result.stdout
    assert "Traceback" not in result.stderr


def test_completion_evidence_and_next_frontier():
    rows = {row["id"]: row for row in roadmap()["tasks"]}
    assert set(roadmap()["ready"]) == {"T07", "T10", "T66"}
    for key in ("T01", "T02", "T03", "T04", "T05"):
        assert rows[key]["status"] == "done"
        evidence = rows[key]["completion_evidence"]
        assert (ROOT / evidence["source"]).is_file()
        assert "kernel-contract" in evidence["checks"]
    assert rows["T22"]["status"] != "done"  # projection demo is not a kernel import/export implementation


def test_final_vm_os_gate_requires_the_entire_lifecycle_conjunction(monkeypatch, tmp_path):
    plan_dir = tmp_path / "plan"
    plan_dir.mkdir()
    plan = json.loads((ROOT / "plan/chu_os_plan.graph.json").read_text())
    for node in plan["nodes"]:
        if node["id"] != "T69":
            node["status"] = "done"
    (plan_dir / "chu_os_plan.graph.json").write_text(json.dumps(plan))
    (plan_dir / "check_plan.py").write_bytes((ROOT / "plan/check_plan.py").read_bytes())
    monkeypatch.setattr(chu_model, "ROOT", tmp_path)

    rows = {row["id"]: row for row in chu_model.roadmap()["tasks"]}
    assert rows["T69"]["status"] == "ready"
    required = ["T63", "T64", "T65", "T66", "T67", "T68"]
    assert rows["T69"]["requires"] == required
    for missing in required:
        candidate = copy.deepcopy(plan)
        unfinished = {missing}
        changed = True
        while changed:
            changed = False
            for edge in candidate["hyperedges"]:
                if unfinished.intersection(edge["tail"]):
                    for head in edge["head"]:
                        if head != "T69" and head not in unfinished:
                            unfinished.add(head)
                            changed = True
        for node in candidate["nodes"]:
            if node["id"] in unfinished:
                node.pop("status")
        (plan_dir / "chu_os_plan.graph.json").write_text(json.dumps(candidate))
        rows = {row["id"]: row for row in chu_model.roadmap()["tasks"]}
        assert rows["T69"]["status"] == "blocked"
        assert missing in rows["T69"]["blocked_by"]

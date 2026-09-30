import json
import subprocess
import sys

import pytest

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


def test_completion_evidence_and_next_frontier():
    rows = {row["id"]: row for row in roadmap()["tasks"]}
    assert set(roadmap()["ready"]) == {"T07", "T10"}
    for key in ("T01", "T02", "T03", "T04", "T05"):
        assert rows[key]["status"] == "done"
        evidence = rows[key]["completion_evidence"]
        assert (ROOT / evidence["source"]).is_file()
        assert "kernel-contract" in evidence["checks"]
    assert rows["T22"]["status"] != "done"  # projection demo is not a kernel import/export implementation

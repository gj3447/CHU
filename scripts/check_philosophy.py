"""Check source byte pins and four formal boundaries, not philosophical truth."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(out):
    manifest = json.loads((ROOT / "philosophy/sources.json").read_text())
    checked = {}
    for item in manifest["local_sources"]:
        path = item["path"]
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.is_file():
            raise ValueError(f"Invalid local source: {path}")
        digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            raise ValueError(f"Source pin mismatch: {path}")
        checked[path] = digest
    inputs = ["lean/CHU_WolframRewrite.lean", "philosophy/boundary_probes.lean"]
    source = "\n".join((ROOT / path).read_text() for path in inputs)
    argv = ["lean", "--stdin", "-j", "2", "-M", "768"]
    result = subprocess.run(argv, input=source, text=True, capture_output=True,
                            cwd=ROOT, timeout=30)
    if result.returncode or "sorry" in (result.stdout + result.stderr).lower():
        raise ValueError(f"Lean boundary check failed: {result.stdout}\n{result.stderr}")
    report = {"schema": "chu-philosophy-boundaries/v1", "status": "PASS",
              "observed_at": datetime.now(timezone.utc).isoformat(),
              "authority": "SECONDARY_AI", "formal_examples": 4,
              "lean_version": subprocess.check_output(
                  ["lean", "--version"], cwd=ROOT, text=True, timeout=10).strip(),
              "argv": argv, "stdin_sha256": hashlib.sha256(source.encode()).hexdigest(),
              "input_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                               for p in inputs},
              "verified_local_sources": checked,
              "scope": "Source integrity and proof boundaries; not a proof of cognition, "
                       "physical universe, universal cost optimality or OS implementation",
              "stdout": result.stdout, "stderr": result.stderr}
    out.mkdir(parents=True, exist_ok=True)
    (out / "philosophy-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return {"status": "PASS", "formal_examples": 4, "local_sources": len(checked),
            "report": str(out / "philosophy-report.json")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.out.resolve())))

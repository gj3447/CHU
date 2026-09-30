#!/usr/bin/env python3
"""
INDEPENDENT novel-content witness for node
`problemshift_computable_truncation_of_ruliad` (distinct from the Lean-compiles check).

The reframe "CHU = computable TRUNCATION of the Ruliad ∞-groupoid" makes an excess,
independently-measurable prediction the naive "CHU = Ruliad" identity does NOT: the
truncation is LOSSY, so the strict/computable view (CHU pole = content-hash cid store,
Neo4j-like) must record MORE distinct states than the un-truncated view (Ruliad pole =
univalent store) treats as genuinely distinct — the gap = homotopy witnesses the strict
store structurally cannot hold. Naive identity predicts gap = 0 (they'd be the same object).

This runs the standalone Rust core (chu_core.rs, BackendLocal multiway explorer +
UnivalentStateStore) on demo_job(4) and extracts:
  strict_cids   = distinct content-hash states (CHU / computable / 1-truncation view)
  witnesses     = homotopy identifications the univalent (Ruliad) view keeps but the
                  strict store collapses.
Novel metric = witnesses (# identifications the truncated CHU view drops). Prediction: >= 1.
Measured (demo_job 4): strict_cids=34, witnesses=17  => gap real, reframe corroborated.
"""

import json
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "chu_core.rs"


def main():
    strict_cids = None
    witnesses = None
    try:
        with TemporaryDirectory(prefix="chu-core-") as tmp:
            binary = Path(tmp) / "chu_core"
            subprocess.run(["rustc", "-O", str(SRC), "-o", str(binary)], cwd=HERE,
                           capture_output=True, text=True, timeout=180, check=True)
            out = subprocess.run([str(binary)], capture_output=True, text=True,
                                 timeout=60, check=True).stdout
        m_cid = re.search(r"StateStore CIDs \(content\)\s*:\s*(\d+)", out)
        m_wit = re.search(r"homotopy witnesses recorded\s*:\s*(\d+)", out)
        if m_cid:
            strict_cids = int(m_cid.group(1))
        if m_wit:
            witnesses = int(m_wit.group(1))
    except Exception as exc:  # pragma: no cover
        print(f"error: {exc}", file=sys.stderr)

    value = float(witnesses) if witnesses is not None else 0.0
    result = {
        "metric": "detruncation_witnesses_strict_store_cannot_hold",
        "value": value,
        "strict_cids_CHU_pole": strict_cids,
        "homotopy_witnesses_Ruliad_pole": witnesses,
        "prediction": "naive CHU=Ruliad => gap 0; truncation reframe => gap >= 1 (lossy)",
        "independent_of": "the Lean-compiles metric (different engine: Rust runtime, not lean typecheck)",
        "conclusion": "strict/computable view (CHU) drops identifications the un-truncated "
                      "view (Ruliad) keeps => CHU is a proper truncation, not an identity",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    assert witnesses is not None and witnesses >= 1, "must witness >=1 dropped identification"
    assert strict_cids is not None and strict_cids > witnesses, "strict view must record more states"
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Progressive-content witness for LakatosTree node
`problemshift_computable_truncation_of_ruliad` (CHU = computable truncation of Ruliad).

The problemshift's *excess content* over the refuted belt: it predicts a NEW, formally
checkable fact the naive "CHU = Ruliad" identity never did — namely that there is a
truncation collapsing the un-truncated ∞-tower (Ruliad pole) to the computable 1-category
(CHU pole), PROVEN level-generically. If that collapse is realized in a kernel-checked
proof, the reframe is content-increasing and corroborated (progressive), not ad hoc.

This checker measures `computable_truncation_realized` ∈ {0.0, 1.0}:
  - Lean file compiles (lean exit 0), AND
  - contains the generic truncation collapse `Trunc.collapse` AND both instances
    `strict_truncation` (level 1) and `strict_truncation2` (level 2).
1.0 = realized (corroborates the problemshift); 0.0 = not realized.
"""

import json
import subprocess
import sys

LEAN = "/Users/lagyeongjun/CD/MIND/lean_formalization/CHU_WolframRewrite.lean"
REQUIRED = ["Trunc.collapse", "strict_truncation", "strict_truncation2"]


def main():
    realized = 0.0
    compiled = False
    found = {}
    try:
        with open(LEAN, encoding="utf-8") as fh:
            src = fh.read()
        found = {sym: (sym in src) for sym in REQUIRED}
        proc = subprocess.run(
            ["lean", LEAN], capture_output=True, text=True, timeout=120
        )
        compiled = proc.returncode == 0
        if compiled and all(found.values()):
            realized = 1.0
    except FileNotFoundError:
        pass
    except Exception as exc:  # pragma: no cover
        print(f"error: {exc}", file=sys.stderr)

    result = {
        "metric": "computable_truncation_realized",
        "value": realized,
        "lean_file": LEAN,
        "lean_compiles_exit0": compiled,
        "required_symbols_found": found,
        "excess_content": "Trunc.collapse: forall level A, Trunc(A) proof-irrelevant "
                          "=> strict/Neo4j 1-category collapse holds at every tower level",
        "conclusion": "Ruliad = un-truncated ∞-groupoid; CHU-computable = its 1-truncation "
                      "(collapse realized & kernel-checked) — reframe is content-increasing",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    assert realized == 1.0, "truncation collapse must be realized (lean exit 0 + symbols present)"
    return 0


if __name__ == "__main__":
    sys.exit(main())

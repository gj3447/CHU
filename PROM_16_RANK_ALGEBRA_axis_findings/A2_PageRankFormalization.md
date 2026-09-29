# A2 — PageRank Formalization Prior Art

> **Cycle:** `prom16-chu-rank-algebra-2026-04-29` | **Axis:** A2 | **Sub-axes:** S1-S4

---

## A2::S1 OfficialCanon (D05) — HIGH

**oneLineSummary**: Isabelle/HOL Markov_Models (Hölzl) + Coq Dvoretzky stochastic approximation provide formal foundations (transition matrices, stationary distributions, convergence), but **no published monolithic PageRank formalization exists**; power iteration eigenvalue proofs remain open in ITP domain.

**rootCause**: PageRank decomposes into 3 layers — (1) Markov chain transition matrix (Isabelle Markov_Models complete), (2) Stochastic matrix + convergence (Isabelle PF, Coq Dvoretzky), (3) Power iteration eigenvalue (unverified). Gap: no integrated end-to-end certified PageRank.

**Recommendation**:
1. Use Isabelle/HOL Markov_Models as semantic base (transition matrix normalization)
2. Adapt Coq Dvoretzky theorem (ITP 2022, Vajjha) for power iteration convergence — Coquelicot real analysis + martingale-difference
3. Reference AFP Stochastic_Matrices PF for eigenvalue dominance
4. Lean 4 thin wrapper around Isabelle Markov chains + Mathlib probability
5. Damping factor d=0.85 reduce to: `(1-d)*M + d*teleport_uniform` stochastic ~50 lines Isabelle

**References**:
- [AFP Markov_Models](https://www.isa-afp.org/entries/Markov_Models.html)
- [AFP Stochastic_Matrices PDF](https://www.isa-afp.org/browser_info/current/AFP/Stochastic_Matrices/document.pdf)
- [Dvoretzky Coq ITP 2022](https://drops.dagstuhl.de/storage/00lipics/lipics-vol237-itp2022/LIPIcs.ITP.2022.31/LIPIcs.ITP.2022.31.pdf)
- [Markov Processes Isabelle CPP 2017](https://popl17.sigplan.org/details/CPP-2017/19/Markov-Processes-in-Isabelle-HOL)

---

## A2::S2 Implementation (D06) — HIGH

**oneLineSummary**: Isabelle AFP (Stochastic_Matrices + Markov_Models) provides canonical formalization of transition matrices and Markov chains; Lean 4 mathlib has PMF/probability infrastructure but **no dedicated stochastic matrix module**; Coq-community offers graph algorithms (Tarjan) but PageRank remains unformalised across all major systems.

**rootCause**: No major theorem prover has unified PageRank formalization despite strong foundations. Isabelle excels at stochastic matrix theory, Lean 4 has measure-theoretic probability, Coq has graph algorithms — but separately. No integrated executable PageRank with convergence proofs.

**Recommendation**:
- **Lean 4**: (1) Mathlib Probability.PMF + Data.Matrix.Kronecker → right-stochastic matrices. (2) Port Isabelle Stochastic_Matrices irreducibility/aperiodicity. (3) Power iteration spectral norm bounds.
- **Isabelle**: bridge Markov_Models.DTMC + Stochastic_Matrices.PF
- **Coq**: extend Tarjan + custom Markov kernel

**Alternatives**:
- Probly (Lean 4 prob programming) substrate
- Random walk on graph directly (custom Markov kernel)
- Port PyTorch PageRank to Lean Mathlib.Computation

**References**:
- [AFP Stochastic_Matrices](https://www.isa-afp.org/entries/Stochastic_Matrices.html)
- [Mathlib4 GitHub](https://github.com/leanprover-community/mathlib4)
- [Probly](https://github.com/lecopivo/Probly)
- [Coq graph-theory](https://github.com/rocq-community/graph-theory)

---

## A2::S3 TheoryBridge (D07) — HIGH

**oneLineSummary**: Bridge PageRank to SimpleGraph via CHU-indexed Kernel. Mathlib4 separates SimpleGraph.Adj from Kernel — no canonical bridge. CHU type unifies via:

```lean
def PageRankKernel (G : SimpleGraph V) [MeasurableSpace V] [Countable V] : Kernel V V :=
  fun v => Measure.sum (fun u : V =>
    (if G.Adj u v then (1 : ℝ) / G.degree v else 0) • Measure.dirac u)
```

**rootCause**: Mathlib4 SimpleGraph + Kernel separated. CHU type (categorical closure) could unify both layers, requires manual enrichment of SimpleGraph with measurable space + Markov kernel semantics.

**Recommendation**:
- Define CHU-indexed random walk kernel pattern
- `PageRankWalk : CHUPiece V → CHUPiece V → Type*` where CHUPiece maps SimpleGraph.adj to measurable subsets
- Use `Kernel.deterministic + ENNReal.ofReal` for stateless normalization
- Wrap in enriched-category functor `SimpleGraph ⇝ ProbabilityKernels`

**Alternatives**:
- Reflexive quivers (Mathlib.Combinatorics.Quiver.ReflQuiver) — explicit edge weights
- Matrix-free Markov: typeclass `IsMarkovWalk` directly on SimpleGraph (less modular but faster prototyping)
- Functor `(Graph V) (Prob.Kernels V)` via enriched-category (full Mathlib.CategoryTheory.Enriched)

**Caveats**: SimpleGraph vertices typeless (no MeasurableSpace by default). Kernel needs measurable structure. Dangling node degree-0 custom handling. PF gap: convergence requires Mathlib.LinearAlgebra.Eigenspace (incomplete).

**References**:
- [Mathlib4 Probability.Kernel.Defs](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Kernel/Defs.html)
- [Markov kernels Mathlib arXiv 2510.04070](https://arxiv.org/html/2510.04070v1)
- [Mathlib4 SimpleGraph.Basic](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Basic.html)
- [LeanCat Benchmark 2512.24796](https://arxiv.org/pdf/2512.24796)

---

## A2::S4 Critique (D08) — HIGH

**oneLineSummary**: PageRank formalizes poorly because (1) **proof burden** (measure theory + Markov convergence) >> **algorithmic risk** (이미 PF guaranteed), (2) ML/formal methods communities don't communicate, (3) industry empirical validation. CHU rank discrete foundation enables better formal coverage via APT + symbolic evaluation. Lean Mathlib analysis library mature.

**rootCause**: 3 reinforcing barriers:
- **Cultural**: formal methods ≠ ML community 단절. Recent neural network verification boom 있지만 graph algorithms 우선순위 낮음.
- **Technical**: measure theory + real analysis + non-discrete fixed-points + floating-point semantics. Mathlib mature (1M+ LOC) but expensive.
- **Incentive**: PF 이미 mathematically proven, formal proof ROI low vs effort.

**Recommendation** for CHU:
1. **Decouple discrete topology** (formalize) from **continuous ranking score** (defer to oracle)
2. Lean Mathlib measure foundation (teorth/analysis + Mathlib.MeasureTheory.Function.ConvergenceInMeasure)
3. **Contract pair**: symbolic spec (stochastic matrix + irreducibility + aperiodicity) + numerical witness (convergence error bounds, damping factor)
4. Borrow from "Formalization of Convergence Rates of First-order Algorithms" for proof infrastructure

**Alternatives**:
- Sidestep real numbers: discrete algebraic framework over rationals
- Pragmatic hybrid: graph invariants formal, numerical empirical
- Abstract interpretation: intervals/polyhedra bound convergence behavior

**References**:
- [Convergence Rates First-order arXiv 2104.02466](https://arxiv.org/abs/2104.02466)
- [teorth/analysis](https://github.com/teorth/analysis)
- [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/mathematics_in_lean.pdf)

---

## 합의 (A2 axis)

- **D05+D06+D08**: PageRank monolithic formalization 부재, cross-system 분산 (Isabelle Markov_Models / Coq Dvoretzky / Lean PMF) → **C3 consensus**
- **D08**: ROI critique — but CHU discrete substrate 가 barriers 우회 가능
- **D07**: 구체 Lean Kernel signature 제공 → C2 consensus 강화

## 분기

- **D08 ROI critique** vs **D03/D07 signature 제안**: D08 회의적, D03/D07 가능성 제시. → 양립 (D08은 cost 인정, D03/D07은 cost 감수 시 가능)

## CHU 시사점

- **PageRank 가 어느 proof assistant 에서도 monolithic formalization 부재** = CHU rank 가 첫 통합 시도의 큰 기회
- D03 signature + D07 kernel 결합 가능 — Mathlib4 IsEigenvector + Kernel.Defs 인프라 충분
- Cipollina 2025 (A1::S1) PR merge 시 PageRank-as-CHU-rank-instance 형식화 직접 가능

# A1 — Mathlib4 Perron-Frobenius / Stochastic Matrix / Markov Chain 형식화 status

> **Cycle:** `prom16-chu-rank-algebra-2026-04-29` | **Axis:** A1 | **Sub-axes:** S1-S4

---

## A1::S1 OfficialCanon (D01) — HIGH

**oneLineSummary**: Lean 4 Perron-Frobenius NOT in Mathlib4 main yet. Cipollina et al. (arxiv:2512.07766, Dec 2025) delivered first formalization for Boltzmann machine ergodicity; PR to mathlib under review. Eigenspace + Irreducibility modules exist; stochastic matrix + dominant eigenvalue chain pending.

**rootCause**: PF for nonneg matrices NOT yet merged into Mathlib4 mainline. Cipollina et al. (Dec 2025) FIRST Lean 4 formalization, under review. Eigenspace/Spectrum/LinearAlgebra modules exist, but stochastic matrix + irreducibility + dominant eigenvalue chain incomplete in main library.

**Recommendation**: (1) Await Mathlib PR merge (H1 2026); (2) Integrate Cipollina PF into CHU_RankAlgebra locally; (3) Leverage Mathlib4.LinearAlgebra.Eigenspace.Basic + Mathlib4.LinearAlgebra.Matrix.Irreducible.Defs as scaffolding.

**Caveats**: Cipollina formalization 15,342 LOC, integration HIGH complexity. Irreducibility now in Mathlib4 (graph-quiver), PF eigenvalue dominance still external. AFP entry not directly portable.

**References**:
- [Cipollina et al. arXiv 2512.07766](https://arxiv.org/html/2512.07766v1)
- [Mathlib4 Eigenspace.Basic](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Eigenspace/Basic.html)
- [AFP Stochastic_Matrices](https://www.isa-afp.org/entries/Stochastic_Matrices.html)

---

## A1::S2 Implementation (D02) — HIGH

**oneLineSummary**: Mathlib4 implements PF infrastructure via Matrix.IsIrreducible/Matrix.IsPrimitive (graph-quiver characterization, strongly connected ↔ ∃k:(A^k)_{ij}>0) BUT does NOT formalize full PF theorem (leading eigenvalue positivity, eigenvector nonnegativity, simplicity). Spectral radius/perronRoot not located in stable Mathlib4.

**rootCause**: Mathlib4 IsIrreducible defined over LinearOrderedRing requires PosMulStrictMono. Full PF listed as open in mathlib4#6091 ("100 theorems"). Spectral radius + leading eigenvalue chain pending.

**Recommendation**: CHU rank algebra formalization: (1) Import Mathlib.LinearAlgebra.Matrix.Irreducible.Defs zero-cost. (2) CHU type (X→Prop) natively encodes graph; irreducibility = CHU predicate. (3) Extend perronRoot via Mathlib.LinearAlgebra.Matrix.Spectrum or sketch within CHU semantics. Markov chain via Mathlib.Analysis.Convex.DoublyStochasticMatrix.

**Caveats**: GitHub code search blocked. Module structure inferred from doc site. PF listed as open in mathlib4#6091.

**References**:
- [Mathlib4 Matrix.Irreducible.Defs](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Irreducible/Defs.html)
- [Mathlib4 DoublyStochasticMatrix](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Convex/DoublyStochasticMatrix.html)

---

## A1::S3 TheoryBridge (D03) — HIGH

**oneLineSummary**: Mathlib4 spectral infrastructure (IsEigenvector + InnerProductSpace.Spectrum self-adjoint + Adjoint Hilbert) all mature SOTA 2026. PageRank vector = stationary eigenvector of row-stochastic Google matrix (eigenvalue 1). PF unique largest eigenvalue.

**Proposed Lean 4 type signature**:
```lean
def CHURankInstance (G : CHU → CHU → ℝ) : Prop :=
  ∃ (n : ℕ) (φ : Fin n → CHU),
  let M : Matrix (Fin n) (Fin n) ℝ := fun i j => G (φ i) (φ j)
  (∀ i, ∑ j : Fin n, M i j = 1) ∧                  -- row-stochastic
  (∃ (v : Fin n → ℝ),
    (∀ i, v i ≥ 0) ∧
    (∑ i : Fin n, v i = 1) ∧
    IsEigenvector M 1 v)                           -- Perron vector
```

**Why this works**:
- Direct Mathlib4 usage — `IsEigenvector M 1 v` uses existing SOTA linear algebra
- Finite projection — `Fin n` embedding manages infinite CHU universe (computability)
- PageRank instance — Google matrix M, PageRank vector v = φ⁻¹(rank)
- CHU abstraction — generalizes beyond internet to any rankable hypergraph

**Caveats**: Infinite CHU requires finite projection (unavoidable for computability). Matrix.IsStochasticMatrix not yet canonical (RFC). Power iteration convergence needs aperiodicity + irreducibility preconditions.

**References**:
- [Mathlib4 Eigenspace.Basic](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Eigenspace/Basic.html)
- [Mathlib4 InnerProductSpace.Spectrum](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/InnerProductSpace/Spectrum.html)

---

## A1::S4 Critique (D04) — HIGH

**oneLineSummary**: Lean 4 classical.choice 가 Markov chain convergence 형식화의 computational semantics 깨뜨림. Classical proofs of ergodic convergence require existence claims (stationary distribution, eigenvector) that cannot be extracted as constructive algorithms. CHU 'hyperuniverse' boundary mirrors ZFC+choice limit.

**rootCause**: Lean 4 Prop (classical meta-truth) vs Type (computable data) split. classical.choice → noncomputable mark. CHU computability 의미 = ZFC+inaccessible ↔ Lean CIC equiconsistent, 같은 epistemic limit.

**Recommendation** — Bifurcation strategy:
1. **Proof layer**: Classical.choice 자유 사용, noncomputable mark
2. **Computation layer**: 사전 decidable fragment 추출 — fix matrix rank/dimension/precision as ℕ; convergence rate as computable bound
3. **Boundary annotation**: `::|ComputableBoundary` metadata
4. CHU contexts 시 bounded ZFC vs full ZFC+choice 사전 선언

**Caveats**: Classical.choice 'pure' (soundness 유지, computability만 손실). Type class heartbeat limits 별도 issue. CHU analogy 구조적: 자기참조 + closure → 결정불가 boundary.

**References**:
- [Lean 4 Axioms and Computation](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/)
- [Markov kernels in Mathlib (arXiv 2510.04070)](https://arxiv.org/html/2510.04070v1)
- [Brownian motion in Lean (arXiv 2511.20118)](https://arxiv.org/html/2511.20118v1)

---

## 합의 (A1 axis)

- **D01+D02+D03**: Mathlib4 인프라 mature, full PF 미완 (Cipollina 2025 첫 시도) → **C1 consensus**
- **D03**: 구체 Lean type signature 제안 → **C2 consensus 핵심**
- **D04 + D01-03 양립**: classical.choice boundary 인정하면서 signature 가능 (proof/computation layer bifurcation)

## 분기

- 없음 (D04 가 D01-03 의 가능성을 부정하지 않음, 대신 boundary 명시)

## CHU 시사점

- **CHU rank algebra Lean 4 형식화는 가능**: Mathlib4 인프라 충분 + Cipollina 2025 통합 + signature 정착
- 단, classical.choice boundary 인정 필수 (proof layer noncomputable, computation layer decidable substrate)
- **mathlib4#6091 OPEN 상태 확인** — full PF 형식화는 mathlib 최우선 미완 100 theorem 중 하나

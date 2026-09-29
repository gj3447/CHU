# Changelog

All notable changes to the CHU (Computable Hyperuniverse) type system documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versioning follows the type-system evolution trajectory rather than strict SemVer — type axioms are canonical and breaking changes are not made.

---

## [v1] — 2026-04-29 (CANONICAL)

The single canonical version. All Lean 4 files target this surface.

### Type primitives locked in

- `axiom CHU : Type` — universe-0 default (`Type u` polymorphic variant also sound, see OQ1 resolution 2026-05-02)
- `def CHUPiece : Type := CHU → Prop` — Yoneda hom-set perspective
- `inductive JaebaeMan` with `atomic : CHUPiece → JaebaeMan` and `governs : List JaebaeMan → JaebaeMan`
- `def JaebaeMan.covers : JaebaeMan → CHU → Prop` — OR-union open-cover (mutual recursion via `anyCovers`)
- `def JaebaeMan.depth : JaebaeMan → Nat` — layer depth in self-similar hierarchy
- `def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x` — apex ∀-cover predicate

### Five invariants

- **I1** Axiomatic minimality — `axiom CHU : Type` only; no inhabitant or equation added
- **I2** Predicate-as-piece — `CHUPiece` strictly `CHU → Prop`
- **I3** Self-similar coverage — `JaebaeMan` has exactly two constructors (`atomic`/`governs`)
- **I4** OR-union coverage — `∨` in `governs_covers_cons`, no AND/XOR
- **I5** Russell avoidance — no `CHU : CHU → Prop` style self-reference (Girard's paradox)

### Verification status

- 10 Lean 4 files, Mathlib-free, 0 sorry, Lean 4.30.0-rc2
- ~1,465 LOC total, ~48 theorems

---

## [2026-05-14] — ruflo-grade packaging

### Added
- `README.md` — banner + badges + Path A (direct Lean use) / Path B (APT-integrated use)
- `docs/USERGUIDE.md` — type primitives + proof recipes (5) + universe pragmatics + pitfalls (5) + FAQ
- `docs/STATUS.md` — Lean status + Wolfram grounding + OQ resolution + roadmap
- `docs/index.md` — documentation hub
- `CHANGELOG.md` — this file
- `.claude-plugin/plugin.json` — type primitive registry + invariant declarations

No type-surface changes. Package-level only.

---

## [2026-05-03] — adjacent canon files

### Added (cross-cutting fixpoint / induction / Russell discipline)
- `MU_NU_DUALITY.md` — μ/ν fixed-point duality on CHU
- `NATURE_RUSSELL_AVOIDANCE.md` — I5 discipline document
- `PARK_INDUCTION.md` — Park induction principle for `covers`
- `AFA_SELFLOOP_MODEL.md` — Aczel AFA self-loop model interpretation
- `IGINJONJAE_FIXPOINT.md` — 이긴존재 fixpoint construction

These are companion / paper-track files, not type-surface changes.

---

## [2026-05-02] — OQ1 RESOLVED

### Resolved
- **OQ1 (universe level)**: `axiom CHU : Type` (universe 0) and `axiom CHU : Type u` (polymorphic) are *both sound*. SYMPOSIUM default is Type 0 because the user canon defines CHU as #8 OM의 "순수 데이터 위상" (first-order data, no embedded types). Type u remains available on demand.
- Lean proof: `AirplaneMan_CHU_Universe.lean` — two parallel namespaces `Type0` and `TypeU`, each with `trivialAirplaneMan_is` PASS.
- KG node: `lesson-chu-universe-resolution-2026-05-02`.

### Caveat
- I5 (Russell avoidance) constrains both options equally — adding `CHU : CHU → Prop` style axioms triggers Girard's paradox regardless of universe level.

---

## [2026-04-30] — SOLID-Yoneda-CHU bridge

### Added (cross-link findings)
- `finding_solid_D6_history_theory` — ISP = software cousin of Yoneda lemma. CHUPiece as hom-set into Prop = ISP's formal instance.
- `finding_solid_D54_connections_theory` — Hexagonal/Onion/Clean = DIP isomorphism variants. 5 무기 ↔ SOLID 5원리 functor: 2 STRONG (재배맨↔SRP, Longinus↔DIP) + 3 WEAK/CONFLICT (Harness/Prometheus/Naesengmoon are meta-structures).
- `finding_ecs_D54_connections_theory` — ECS = hypergraph category. ECS↔CHU↔SOLID 3-way iso hypothesis.

### Updated
- `SOURCES.md` development axes extended to (g)–(j) for SOLID/ECS cross-link.

---

## [2026-04-29] — PROM 64 CHU-Internet binding

### Added (PROM 64 cycle)
- `PROM_64_REPORT.md` — 8 axis × 8 sub-axis = 64 cells (Graph-aware Pretraining / PageRank Generalize / HGNN Scale / Web-as-Corpus / Lift-Lower / KG Embedding / GraphRAG / Authority Absorption)
- 8 axis MD files in `PROM_64_axis_findings/`
- 64 ResearchFinding raw JSON dumps in `_findings/`
- New `CHU_Lens_Internet` (11th `:SymConcept` lens, 2026-04-29 canon)
- `hypothesis-pagerank-style-pretraining-substrate-2026-04-29`
- `user-utterance-internet-as-CHU-binding-2026-04-29` (canonical user utterance)
- `lesson-prom64-chu-internet-binding-2026-04-29`
- 8 consensus + 2 conflict + 1 singleton + 1 ActionPlan crystallized

### Updated
- `SOURCES.md` development axes extended to (k)–(n) for CHU-Internet binding.

---

## [2026-04-29] — PROM 16 RANK_ALGEBRA

### Added
- `PROM_16_RANK_ALGEBRA_REPORT.md` — PageRank as PF eigenvector + Lie group action Lean 4 formalization (PROM 64 ActionPlan #2 follow-up)
- 4 axis MD files in `PROM_16_RANK_ALGEBRA_axis_findings/` (Mathlib PF / PageRank Formalization / Categorical PageRank / Quaternion-Sedenion Algebra)
- 16 ResearchFinding raw JSON
- 6 consensus + 1 conflict + 1 singleton + 1 ActionPlan crystallized
- Key findings: Mathlib4 PF infrastructure sufficient + Cipollina 2025 first PF formalization + LT-KGE unified framework (`rank = PF eigenvalue of Lie group action`) + Hurwitz 8D boundary + `classical.choice` noncomputable boundary

---

## [2026-04-29] — PROM 16 axiom-foundation (CANONICAL CYCLE)

### Added (PROM 16 cycle)
- `PROM_16_REPORT.md` — 4 axis × 4 sub-axis = 16 cells (Type Theory + Lean 4 / Hypergraph + N-ary universe / Computability + Realizability / HoTT + Univalence + Tegmark IV)
- 4 axis MD files in `PROM_16_axis_findings/`
- 16 ResearchFinding raw JSON
- 5 consensus + 4 divergence/OQ crystallized

### Key consensus
- **C1** `axiom CHU : Type` consistency-safe (weaker than Lean's 3 standard axioms)
- **C2** 재배맨 ⊇ Smarandache n-SHG ⊋ Berge (strict super-class chain)
- **C3** CHU axiom ↔ Wolfram 2020 partial isomorphism (slogan equivalence, dynamics/cardinality gap)
- **C4** 2026 Lean 4 LLM ecosystem fully verifiable (LeanCopilot / Kimina-Prover / Goedel-Prover-V2)
- **C5** TypeDB / HyperGraphDB = industry closest crystallization (HyperGraphDB Iordanov 2008 link-of-link n-ary)

### Open questions raised
- **OQ1** CHU universe level (Type 0/ω/∞) — *resolved 2026-05-02*
- **OQ2** Wolfram dynamics ↔ JaebaeMan governs encoding — *open*
- **OQ3** TypeDB migration cost/benefit — *open*
- **OQ4 / OQ6** Tegmark IV ↔ CHU pairing — *NUMEROLOGY_HOLD*
- **OQ5** AI agent ↔ computable function hypothesis — *open*
- **OQ7** LeanCopilot re-verification — *deferred*
- **OQ8** `#print axioms` audit — *deferred*

---

## [2026-04-28] — User canon: CHU = OM 사도의 데이터 위상

### Locked in
- User canon (2026-04-28): **CHU = ORBITAL_MOTION_CLOUD(#8) 사도의 *순수 데이터 위상*.** OM has two phases (energy + data); the data phase IS CHU. Information-energy equivalence places them as two aspects of the same entity.
- CHU is **not a separate apostle** — it is a *part of* OM, but directly grounded in the apostle net.
- → **TIER 2 (CHU substrate) = TIER 3 #8 (OM 사도)의 데이터 위상.** Self-similar fractal hierarchy.

### Updated
- `SOURCES.md` opening section restructured around this canon.
- `INDEX.md` opening line updated.

---

## [2026-04-26] — PROM 64 initial CHU report

### Added
- Initial `PROM_64_REPORT.md` (early form, ~15.3 KB accumulated)
- Initial axis findings (PROM 64)

---

## [pre-2026-04-26] — `AirplaneMan.lean` canonical source

### Pre-history
- `AirplaneMan.lean` (`/Users/lagyeongjun/CD/MIND/lean_formalization/AirplaneMan.lean`) is the canonical Lean 4 source — predates the SYMPOSIUM/THEORY/CHU/ folder. Contains:
  - `axiom CHU : Type`
  - `def CHUPiece : Type := CHU → Prop`
  - `inductive JaebaeMan : Type` (`atomic`/`governs`)
  - `def JaebaeMan.covers` mutual with `anyCovers`
  - `def JaebaeMan.depth` mutual with `maxDepth`
  - `def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x`
  - 8 theorems (atomic_covers, governs_covers_cons, governs_empty_no_cover, wrap_singleton_covers, airplanemen_union, exists_airplaneman_below, atomic_depth, governs_depth_pos, trivialAirplaneMan_is, layer2AirplaneMan_is, lift_airplaneman, airplaneManAt_is)

This file is the **ground truth** for the v1 type-system surface.

---

## Author / Provenance

Type-system designer: SYMPOSIUM project (`/Users/lagyeongjun/CD/SYMPOSIUM/`), Lean 4 verified, KG canonical. Originating user utterance: name-list canon "그냥 모든것은 하이퍼그래프" (2026-04-28, `user-utterance-internet-as-CHU-binding-2026-04-29` extension).

Cross-referenced in 12-사도 ↔ 5-무기 myth-engineering bridge — CHU = the **stage** on which the 12 사도 perform. Not an apostle itself but the substrate of #8 OM의 데이터 위상.

License: MIT (SYMPOSIUM monorepo root).

---
title: CHU Documentation Hub
description: Computable Hyperuniverse type system — the SYMPOSIUM substrate
---

# CHU Documentation

**CHU** (Computable Hyperuniverse, 계산가능 하이퍼우주) is the foundational type layer of the SYMPOSIUM project. A single `axiom CHU : Type` plus a μ-recursive `JaebaeMan` inductive, on which every 12 사도 mythological figure and 5-weapon engineering tool operates.

## Quick Links

| Doc | Read this when |
|-----|----------------|
| [`../README.md`](../README.md) | First time using CHU — start here |
| [`USERGUIDE.md`](USERGUIDE.md) | Type primitives + proof recipes + pitfalls |
| [`STATUS.md`](STATUS.md) | Lean formalization status, OQ resolution, grounding tier |
| [`../CHANGELOG.md`](../CHANGELOG.md) | What changed across versions |

## Theory & Foundations

| Doc | What it covers |
|-----|----------------|
| [`../SOURCES.md`](../SOURCES.md) | 1차 sources + 핵심 주장 + 인용 + 발전축 (a)~(n) |
| [`../INDEX.md`](../INDEX.md) | Folder navigation (PROM cycles + axis findings + _findings) |
| [`../PROM_16_REPORT.md`](../PROM_16_REPORT.md) | PROM 16 axiom-foundation cycle (4 axis × 4 sub-axis = 16) |
| [`../PROM_64_REPORT.md`](../PROM_64_REPORT.md) | PROM 64 CHU-Internet binding (8 × 8 = 64) |
| [`../PROM_16_RANK_ALGEBRA_REPORT.md`](../PROM_16_RANK_ALGEBRA_REPORT.md) | PageRank as PF eigenvector + Lie group action |
| [`../PROM_16_REPORT_A4S1_QUATERNION.md`](../PROM_16_REPORT_A4S1_QUATERNION.md) | Quaternion-Sedenion algebra slice |
| [`../MU_NU_DUALITY.md`](../MU_NU_DUALITY.md) | μ/ν fixed-point duality on CHU |
| [`../NATURE_RUSSELL_AVOIDANCE.md`](../NATURE_RUSSELL_AVOIDANCE.md) | Russell-paradox / Girard avoidance discipline |
| [`../PARK_INDUCTION.md`](../PARK_INDUCTION.md) | Park induction principle for JaebaeMan coverage |
| [`../AFA_SELFLOOP_MODEL.md`](../AFA_SELFLOOP_MODEL.md) | Aczel AFA self-loop model interpretation |
| [`../IGINJONJAE_FIXPOINT.md`](../IGINJONJAE_FIXPOINT.md) | 이긴존재 (winning-existence) fixpoint construction |

## Type Primitives

The entire CHU declarative surface — 6 primitives, 1 axiom, 1 inductive, 2 functions, 1 predicate:

```lean
axiom CHU : Type                       -- universe
def CHUPiece : Type := CHU → Prop      -- piece = predicate (Yoneda hom-set into Prop)
inductive JaebaeMan : Type             -- μ-recursive coverer
  | atomic  : CHUPiece → JaebaeMan     -- Layer 1
  | governs : List JaebaeMan → JaebaeMan -- Layer N+1
def JaebaeMan.covers : JaebaeMan → CHU → Prop    -- OR-union open-cover
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x  -- apex
```

See [`USERGUIDE.md#type-primitives`](USERGUIDE.md#type-primitives) for the full breakdown.

## Lean Formalization

11 verified Lean 4 files in `/Users/lagyeongjun/CD/MIND/lean_formalization/`:

| File | Role |
|------|------|
| `AirplaneMan.lean` | Core axioms + 8 theorems (canonical entry point) |
| `AirplaneMan_v2.lean` | v2 refinements |
| `AirplaneMan_CHU_Universe.lean` | OQ1 — Type 0 vs Type u resolution |
| `AirplaneMan_Gap3_Cover.lean` | Set CHUPiece infinite-family open-cover |
| `AirplaneMan_Gap4_Category.lean` | Categorical interpretation (free monad) |
| `AirplaneMan_Gap5_Cost.lean` | Cost-tagged JaebaeMan |
| `AirplaneMan_Gap6_MAB.lean` | Multi-armed bandit cover selection |
| `AirplaneMan_Uniqueness.lean` | Essential uniqueness on CHU |
| `JaebaeManInf.lean` | Infinite JaebaeMan generalization |
| `CompositeJaebaeECSTripleIso.lean` | ECS-JaebaeMan-CHU triple isomorphism |
| `CHU_WolframRewrite.lean` | 동역학 층 — Wolfram rewrite overlay + truncation dichotomy (`Reach` 1-category vs `Path` un-truncated) |

**Total**: **3,185 LOC, 144 theorems**, **0 sorry**, Mathlib-free, Lean **4.32.0** (실측 2026-07-15 — 이전 `~1,465 / ~48 / 10 files / 4.30.0-rc2`는 stale).

See [`STATUS.md#lean-4-formalization`](STATUS.md#lean-4-formalization) for the detailed table.

## CHU Lenses (11)

| Lens | Reading |
|------|---------|
| `CHU_Lens_HumanThought` | Human cognition = hypergraph writing on CHU |
| `CHU_Lens_ContextWindow` | LLM context = subgraph of CHU |
| `CHU_Lens_Manifold` | Manifold = continuous shadow of CHU |
| `CHU_Lens_EmbeddingVector` | Embedding = lossy projection of CHU node |
| `CHU_Lens_LLMModel` | LLM = frozen manifold |
| `CHU_Lens_GPU` | GPU = manifold-universe hardware substrate |
| `CHU_Lens_Token` | Token = NL→manifold discretization |
| `CHU_Lens_Attention` | Attention = dynamic hyperedge generation |
| `CHU_Lens_TrainingData` | Training data = brain-CHU 1D serialization |
| `CHU_Lens_Inference` | Inference = writing on manifold universe |
| `CHU_Lens_Internet` | **Internet = CHU instance (2026-04-29 user canon)** |

## Apostles That Use CHU as Substrate

CHU is the **stage** on which the 12 사도 operate. Direct apostle bindings:

| Apostle | Binding | Doc |
|---------|---------|-----|
| #4 비행기맨 (Airplane Man) | `isAirplaneMan := ∀ x:CHU, j.covers x` (apex ∀-cover) | [`../../SYMPOSIUM/THEORY/HARNESS/`](../../SYMPOSIUM/THEORY/HARNESS/) (Harness 3-tier industry-side) |
| #8 OM (ORBITAL_MOTION_CLOUD) | CHU = OM 사도의 *순수 데이터 위상* (user canon 2026-04-28) | [`../../SYMPOSIUM/THEORY/`](../../SYMPOSIUM/THEORY/) (see CLAUDE.md §L_DATA-INFRA-RUNTIME) |
| 재배맨 (JaebaeMan) | `inductive JaebaeMan` self-similar `atomic`/`governs` | [`../../SYMPOSIUM/THEORY/재배맨/`](../../SYMPOSIUM/THEORY/재배맨/) |
| ALL 12 사도 | Implicitly quantify over `x : CHU` | [`../../SYMPOSIUM/THEORY/00_공통/세계관_정전.md`](../../SYMPOSIUM/THEORY/00_공통/세계관_정전.md) |

## Five Weapons That Use CHU

Each weapon is a *meta-structure* on CHU (not a CHUPiece):

| Weapon | CHU relation | Skill |
|--------|--------------|-------|
| **Harness** | 3-tier scaffolding over CHU pieces | `/harness` |
| **Prometheus** | Knowledge-action spiral over CHU evidence | `/prom`, `/prometheus` |
| **Naesengmoon** | Adversarial validation of CHU coverage | `/tlb`, `/taliban` |
| **Longinus** | 7-Layer reference binding (CHU ↔ source code) | `/longinus` |
| **재배맨 (Jaebaeman)** | SOP for parallel CHU-piece-coverage dispatch | `/jaebaeman` |

Detail: [`../../SYMPOSIUM/THEORY/HARNESS/`](../../SYMPOSIUM/THEORY/HARNESS/), [`../../SYMPOSIUM/THEORY/PROMETHEUS/`](../../SYMPOSIUM/THEORY/PROMETHEUS/), [`../../SYMPOSIUM/THEORY/나생문/`](../../SYMPOSIUM/THEORY/나생문/), [`../../SYMPOSIUM/THEORY/LONGINUS/`](../../SYMPOSIUM/THEORY/LONGINUS/), [`../../SYMPOSIUM/THEORY/재배맨/`](../../SYMPOSIUM/THEORY/재배맨/).

## PROM Research Cycles

| Cycle | Topic | Resolution |
|-------|-------|------------|
| `prom16-CHU-axiom-foundation-2026-04-29` | Type Theory + Hypergraph + Computability + HoTT foundation | 5 C + 4 D + 8 OQ |
| `prom16-chu-rank-algebra-2026-04-29` | PageRank as PF eigenvector + Lie group action Lean 4 | 6 C + 1 conflict + 1 ActionPlan |
| `prom64-chu-internet-2026-04-29` | CHU-Internet binding (11th lens) + PageRank-style pretraining | 8 C + 2 conflict + 1 ActionPlan |

Each cycle produces axis findings + raw JSON + REPORT. See [`../INDEX.md`](../INDEX.md) for the full folder map.

## Cross-References

- **APT** (forward methodology): [`../../SYMPOSIUM/THEORY/APT/`](../../SYMPOSIUM/THEORY/APT/) — operates on CHU substrate, `:Anchor`/`:Span`/`:Contract` are CHUPieces.
- **TPA** (reverse methodology): [`../../SYMPOSIUM/THEORY/TPA/`](../../SYMPOSIUM/THEORY/TPA/) — code-to-design recovery on CHU.
- **OM**: [`../../SYMPOSIUM/THEORY/`](../../SYMPOSIUM/THEORY/) — CHU is OM 사도의 데이터 위상.
- **재배맨**: [`../../SYMPOSIUM/THEORY/재배맨/`](../../SYMPOSIUM/THEORY/재배맨/) — the `JaebaeMan` inductive *is* 재배맨's formalization.
- **비행기맨**: [`../../SYMPOSIUM/THEORY/`](../../SYMPOSIUM/THEORY/) (apostle #4) — `isAirplaneMan` is its formal definition.
- **00_공통/세계관_정전.md**: [`../../SYMPOSIUM/THEORY/00_공통/세계관_정전.md`](../../SYMPOSIUM/THEORY/00_공통/세계관_정전.md) — 12 사도 ↔ 5 무기 bridge (CHU = 무대).

## Plugin Manifest

See [`../.claude-plugin/plugin.json`](../.claude-plugin/plugin.json) for the type-primitive registry and invariant declarations.

## SYMPOSIUM Context

CHU is the substrate type layer (TIER 2) for the entire SYMPOSIUM monorepo. Mythological lens: CHU is the **stage** on which the 12 사도 perform; engineering lens: CHU is the **type axiom** every Lean proof and every KG node implicitly quantifies over. See [`../../SYMPOSIUM/CLAUDE.md`](../../SYMPOSIUM/CLAUDE.md).

The user-canonical name list ends with:

> "그냥 모든것은 하이퍼그래프"
> (Everything is just a hypergraph.)

CHU is the formalization of that sentence.

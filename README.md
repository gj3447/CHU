<div align="center">

# CHU — Computable Hyperuniverse · Hypergraph OS

**VM OS under development · Agent-native graph workspace · Formal foundations**

[![Type System](https://img.shields.io/badge/Type_System-CHU_v1-D97757?style=for-the-badge&logoColor=white)](docs/STATUS.md)
[![Lean 4 Verified](https://img.shields.io/badge/Lean_4-11_files_/_dated_observation-10b981?style=for-the-badge&logoColor=white)](#lean-formalization)
[![KG Lenses](https://img.shields.io/badge/CHU_Lenses-11_SymConcept-6366f1?style=for-the-badge&logoColor=white)](INDEX.md)
[![Sources](https://img.shields.io/badge/External_Canon-Friedman_/_Wolfram_/_Voevodsky-8b5cf6?style=for-the-badge&logoColor=white)](SOURCES.md)
[![License](https://img.shields.io/badge/License-AGPL--3.0--or--later_%2B_Commercial-blue?style=for-the-badge)](LICENSING.md)

</div>

> **현재 사용자 목표 (2026-09-29/30 USER_PRIMARY)**: CHU = **하이퍼그래프 기반 OS**. 파일·문서·코드·모델은 노드와 역할 있는 n항 하이퍼엣지로 다루며, VM에서 부팅해 HSWM을 실행할 수 있어야 한다. 현재 목표·근거·작업 상태는 [engineering README](engineering/README.md), [OS 설계](os/README.md), [계획](plan/CHU_OS_PLAN.md), [사용자 원문](canon/sources/USER_PRIMARY_VM_OS_HSWM_2026-09-30.txt)에서 확인한다.

> **Lean/type-theory 층 (역사적·현재의 보조 자산)**: `axiom CHU : Type`, `CHUPiece := CHU → Prop`, `JaebaeMan`은 CHU의 형식적 이론·프로토타입 층이다. 이는 완성된 OS 커널이나 HSWM 실행 증거가 아니다. 2026-04-28의 SYMPOSIUM TIER 2 해석은 [역사적 이론 맥락](docs/index.md#historical-theory-context)으로 보존한다.
> 생태계: [CHU · HSWM · USL](ECOSYSTEM.md) — CHU ⊇ HSWM(LLM AI), USL = n항 의미 연결 문법.
> 작업환경 참여(“우리는 하나의 존재다”)는 저장소 사용과 분리된 opt-in 약정으로 제안 중:
> [MetaHumotonic Covenant — MHP-0001 (DRAFT)](https://github.com/gj3447/metahumotonic-foundation/pull/1). 이 저장소를 쓰는 것만으로는 작업환경 권한이 넘어가지 않는다.

---

## What the Formal Layer Models

CHU formalizes the user's name-list axiom **"그냥 모든것은 하이퍼그래프"** ("everything is a hypergraph") as a *minimal*, *model-independent*, *consistency-safe* Lean 4 axiom layer:

```lean
axiom CHU : Type                       -- the universe of all "things"
def CHUPiece : Type := CHU → Prop      -- a piece = a set-defining predicate (hom-set into Prop)
inductive JaebaeMan : Type             -- recursive coverer
  | atomic  : CHUPiece → JaebaeMan     -- Layer 1: covers one piece directly
  | governs : List JaebaeMan → JaebaeMan -- Layer N+1: governs lower JaebaeMen
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x
```

That is the small type-theory core. The VM OS, persistent graph service and agent execution contracts are separate implementation layers described in [the architecture](spec/ARCHITECTURE.md).

## Why This Formal Layer

Most type universes are either too specific (a particular set theory model, e.g. ZFC) or too abstract for engineering use (univalent Type Theory with Mathlib transit). CHU is deliberately **the minimum sufficient stage**:

1. **Axiomatic minimality** — `axiom CHU : Type` adds *no* inhabitant, *no* equation. It is strictly weaker than Lean's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`). Consistency-safe.
2. **Predicate-as-piece** — Pieces of CHU are *not* subsets in some ambient set theory; they are functions `CHU → Prop`. This is the Yoneda perspective: an object is determined by its hom-set, applied to software design. ISP (Interface Segregation Principle) becomes the *software cousin* of the Yoneda lemma.
3. **Self-similar coverage** — `JaebaeMan` is a μ-recursive `μX. (CHUPiece + List X)` initial algebra. It strictly subsumes Berge (1-level finite hyperedges) and Smarandache n-SHG (𝒫ⁿ(V), finite n) — the entire SYMPOSIUM ontology is one inductive type.
4. **AirplaneMan = ∀-cover** — A single Lean line — `∀ x : CHU, j.covers x` — formalizes the apex of the SYMPOSIUM mythology: there exists exactly one role whose coverage is total. Existence proven by `airplaneManAt n` for every depth n (`AirplaneMan.lean`).

Grounded in 4 external canons: **Sy Friedman Hyperuniverse Programme** (V-logic, set-generic absoluteness), **Wolfram 2020 Physics Project** (everything-is-hypergraph slogan, partial isomorphism), **Voevodsky Univalent Foundations** (HoTT, ⚠ Lean 4 UIP-incompatible — open question), **Hyland Effective Topos** (`Eff(N)` realizability, computability boundary). See [`SOURCES.md`](SOURCES.md) for the full grounding table.

---

## Quick Start

Start with [engineering README](engineering/README.md) for the current graph-engineering map and [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for reproducible development. Inspect the current repository projection instead of relying on prose counts:

```bash
./chu repo status --json
./chu repo query profiles --json
./chu repo query evidence --json
```

`./chu doctor --json`, `./chu tools --json`, and `./chu check --json` provide environment and verification views. The RDF development registry is [dev/catalog.ttl](dev/catalog.ttl).

CHU's current OS target is a VM-booting environment capable of running HSWM.
The present Ubuntu/QEMU substrate and its strict boundary are documented in
[os/README.md](os/README.md): it verifies a guest boot contract but does **not**
yet run HSWM or constitute a complete CHU OS.

There are **two paths** to use CHU. Pick based on whether you want the raw type system or APT-integrated workflow.

| | **Path A — Direct CHU type system use** | **Path B — APT-integrated use** |
|---|---|---|
| What you get | Lean 4 files imported / consulted as type axioms in your own proofs | Use CHU implicitly as the substrate of APT's `:Anchor` / `:Span` / `:Contract` |
| Surface | `axiom CHU : Type` + `CHUPiece` + `JaebaeMan` inductive | Full `/apt` orchestrator with CHU as silent substrate |
| Skills needed | None (pure Lean / KG reference) | `/apt`, `/apt-sa`, …, `/apt-meta-review` (see [`../SYMPOSIUM/THEORY/APT/`](../SYMPOSIUM/THEORY/APT/)) |
| Best for | Formal proof, paper writing, KG cross-reference design | Building applications on the SYMPOSIUM substrate |
| Token cost | Zero (offline) | Standard APT cycle cost |

### Path A — Direct CHU type system

Use the Lean 4 sources directly:

```bash
cd lean/
lean AirplaneMan.lean                  # core axioms + JaebaeMan + isAirplaneMan + 8 theorems
lean AirplaneMan_CHU_Universe.lean     # universe-level resolution (Type 0 + Type u)
lean AirplaneMan_Gap3_Cover.lean       # Set CHUPiece (infinite family) cover semantics
lean AirplaneMan_Gap4_Category.lean    # categorical interpretation
lean AirplaneMan_Uniqueness.lean       # essential uniqueness on CHU
lean JaebaeManInf.lean                 # infinite JaebaeMan generalization
```

**2026-09-29 observation:** all 11 files verified with pinned Lean 4.34.1, **Mathlib-free**, **0 sorry**. Run `./chu check --json` for fresh verification; `./chu repo status --json` is inventory discovery only.

For paper / KG use, cite the axioms by their canonical file path. The README of any SYMPOSIUM-derivative project can pull CHU as a one-line `axiom CHU : Type` postulate.

### Path B — APT-integrated use

CHU is the *silent substrate* of APT. When you run:

```
/apt "Add OAuth2 login with PKCE flow"
```

`/apt-sa` creates a `:Anchor`, `/apt-sp` decomposes into `:Span`s — all of these are CHU pieces (`CHUPiece := CHU → Prop`) under the hood. You don't *call* CHU; CHU *holds up* APT. See [`../SYMPOSIUM/THEORY/APT/README.md`](../SYMPOSIUM/THEORY/APT/README.md).

### Hello-World: prove "there exists a JaebaeMan covering all of CHU"

```lean
-- in AirplaneMan.lean
def wholeCHU : CHUPiece := fun _ => True
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU
theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by
  intro _; trivial
```

That's the simplest 비행기맨 witness. `airplaneManAt n` extends it to any depth n.

---

## Architecture

### Type Primitives (formal-layer surface)

| Primitive | Lean signature | Role |
|-----------|----------------|------|
| `CHU` | `axiom CHU : Type` | The universe. Everything else quantifies over `x : CHU`. |
| `CHUPiece` | `def CHUPiece : Type := CHU → Prop` | A predicate (= a "piece" / hyperedge characteristic function). |
| `JaebaeMan` | `inductive JaebaeMan` with `atomic`/`governs` | μ-recursive coverer. Strictly subsumes Berge/Smarandache. |
| `JaebaeMan.covers` | `JaebaeMan → CHU → Prop` | Coverage as OR-union of atomic predicates. |
| `JaebaeMan.depth` | `JaebaeMan → Nat` | Layer depth in the self-similar hierarchy. |
| `isAirplaneMan` | `JaebaeMan → Prop` | `∀ x : CHU, j.covers x` — the apex predicate. |

That's the **entire** declarative surface. 6 primitives, 1 axiom, 1 inductive, 2 functions, 1 predicate. Everything in SYMPOSIUM is composition over this.

### Invariants

5 invariants hold across every CHU-using construction:

| # | Invariant | What it forbids |
|---|-----------|-----------------|
| **I1** | **Axiomatic minimality** | Adding any inhabitant or equation to `CHU` (`axiom CHU : Type` only) |
| **I2** | **Predicate-as-piece** | Treating `CHUPiece` as anything other than a function `CHU → Prop` |
| **I3** | **Self-similar coverage** | Defining a coverer outside the `atomic`/`governs` inductive (no second JaebaeMan variant) |
| **I4** | **OR-union coverage** | Replacing the `∨` in `governs_covers_cons` with AND/XOR (changes semantics from open-cover to partition; see `AirplaneMan_Gap3_Cover.lean` for the rationale) |
| **I5** | **Russell avoidance** | Asserting `CHU : CHU → Prop` or similar self-reference (`Girard paradox`; see [`NATURE_RUSSELL_AVOIDANCE.md`](NATURE_RUSSELL_AVOIDANCE.md)) |

Violate any → the inductive becomes unsound or the cover semantics drift. See [`AirplaneMan_CHU_Universe.lean`](lean/AirplaneMan_CHU_Universe.lean) for the universe-level proof that both `Type 0` and `Type u` satisfy I1–I5.

### CHU Lenses (11 :SymConcept)

CHU is observed through 11 lenses (each one a `:SymConcept` KG node) — these are *not* extensions of CHU, but viewpoints onto it:

| Lens | Reading of CHU |
|------|----------------|
| `CHU_Lens_HumanThought` | Human cognition = hypergraph writing on CHU |
| `CHU_Lens_ContextWindow` | LLM context = subgraph of CHU |
| `CHU_Lens_Manifold` | Manifold = continuous shadow of CHU |
| `CHU_Lens_EmbeddingVector` | Embedding = lossy projection of a CHU node |
| `CHU_Lens_LLMModel` | LLM = frozen manifold, replaceable engine |
| `CHU_Lens_GPU` | GPU = manifold-universe substrate hardware |
| `CHU_Lens_Token` | Token = NL→manifold discretization compiler |
| `CHU_Lens_Attention` | Attention = dynamic hyperedge generation |
| `CHU_Lens_TrainingData` | Training data = brain-CHU 1D serialization |
| `CHU_Lens_Inference` | Inference = writing onto the manifold universe |
| `CHU_Lens_Internet` | **Internet = CHU instance, 11th lens** (2026-04-29 user canon) |

See [`SOURCES.md`](SOURCES.md) §"CHU-Internet binding" for the 11th lens grounding (Common Crawl + WDC + PageRank-as-PF eigenvector).

### Lean Formalization

**2026-09-29 observation:** 11 verified Lean 4 files (Mathlib-free standalone, Lean 4.34.1, **0 sorry**):

- [`AirplaneMan.lean`](lean/AirplaneMan.lean) — core axioms + 8 theorems (canonical entry point)
- [`AirplaneMan_v2.lean`](lean/AirplaneMan_v2.lean) — v2 refinements
- [`AirplaneMan_CHU_Universe.lean`](lean/AirplaneMan_CHU_Universe.lean) — Type 0 vs Type u resolution
- [`AirplaneMan_Gap3_Cover.lean`](lean/AirplaneMan_Gap3_Cover.lean) — `Set CHUPiece` infinite family open-cover semantics
- [`AirplaneMan_Gap4_Category.lean`](lean/AirplaneMan_Gap4_Category.lean) — categorical interpretation
- [`AirplaneMan_Gap5_Cost.lean`](lean/AirplaneMan_Gap5_Cost.lean) — cost-tagged JaebaeMan
- [`AirplaneMan_Gap6_MAB.lean`](lean/AirplaneMan_Gap6_MAB.lean) — multi-armed bandit cover selection
- [`AirplaneMan_Uniqueness.lean`](lean/AirplaneMan_Uniqueness.lean) — essential uniqueness on CHU
- [`JaebaeManInf.lean`](lean/JaebaeManInf.lean) — infinite JaebaeMan generalization
- [`CompositeJaebaeECSTripleIso.lean`](lean/CompositeJaebaeECSTripleIso.lean) — ECS-JaebaeMan triple isomorphism
- [`CHU_WolframRewrite.lean`](lean/CHU_WolframRewrite.lean) — rewrite dynamics and truncation overlay

Current CHU copy: [`lean/`](lean/). Historical origin: `MIND/lean_formalization/AirplaneMan*.lean` + `JaebaeMan*.lean` (provenance only, not the current navigation path).

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [`docs/USERGUIDE.md`](docs/USERGUIDE.md) | CHU type definition + usage patterns + ∀-cover proof recipes + pitfalls |
| [`docs/STATUS.md`](docs/STATUS.md) | Lean formalization status, OQ resolution, external grounding tier |
| [`docs/index.md`](docs/index.md) | Documentation hub: current OS route and historical theory route |
| [`engineering/README.md`](engineering/README.md) | Current graph-engineering profiles, evidence and query entry |
| [`CHANGELOG.md`](CHANGELOG.md) | Type-system evolution history |
| [`SOURCES.md`](SOURCES.md) | 1차 sources + 핵심 주장 + 인용 + 발전축 (a)~(n) |
| [`INDEX.md`](INDEX.md) | Folder navigation (PROM cycles + axis findings + raw _findings) |
| [`PROM_16_REPORT.md`](PROM_16_REPORT.md) | PROM 16 axiom-foundation cycle (4 axis × 4 sub-axis = 16 cells) |
| [`PROM_64_REPORT.md`](PROM_64_REPORT.md) | PROM 64 CHU-Internet binding cycle (8 × 8 = 64 cells) |
| [`PROM_16_RANK_ALGEBRA_REPORT.md`](PROM_16_RANK_ALGEBRA_REPORT.md) | PageRank as PF eigenvector + Lie group action formalization |
| [`MU_NU_DUALITY.md`](MU_NU_DUALITY.md) | μ/ν fixed-point duality on CHU |
| [`NATURE_RUSSELL_AVOIDANCE.md`](NATURE_RUSSELL_AVOIDANCE.md) | Russell-paradox / Girard avoidance discipline |
| [`PARK_INDUCTION.md`](PARK_INDUCTION.md) | Park induction principle for JaebaeMan coverage |
| [`AFA_SELFLOOP_MODEL.md`](AFA_SELFLOOP_MODEL.md) | Aczel AFA self-loop model interpretation |
| [`IGINJONJAE_FIXPOINT.md`](IGINJONJAE_FIXPOINT.md) | 이긴존재 (winning-existence) fixpoint construction |

For the SYMPOSIUM context (12 사도 ↔ 5 무기 myth-engineering bridge): [`../SYMPOSIUM/CLAUDE.md`](../SYMPOSIUM/CLAUDE.md).

---

## Comparison

| | CHU | ZFC | HoTT (Voevodsky) | Tegmark IV MUH | Wolfram Hypergraph |
|---|---|---|---|---|---|
| Foundational layer | `axiom CHU : Type` | Sets + axioms | Univalent types | All consistent math structures | Hypergraph + rewrite rules |
| Inhabitants asserted | None (axiom only) | ∅ + pairing + … | Identity types as paths | All structures exist | Vertices + hyperedges |
| Self-reference safety | Disciplined (I5 avoidance) | Foundation axiom | UIP-compatible | Undefined ("structure" undefined) | Term-rewrite confluence |
| Computability tier | Hyland Eff(N) realizability layer overlay | Set-theoretic, generally non-constructive | Constructive (cubical) | Beyond computability | Computable rewrite |
| Engineering use | SYMPOSIUM substrate (12 apostles, 5 weapons) | Mathematics foundations | Proof assistants (Coq-HoTT, Cubical Agda) | Speculative cosmology | Physics project |
| Lean 4 native | **Yes** (Mathlib-free) | Implicit in classical logic | ⚠ UIP-incompatible (Carneiro 2025) | N/A | Indirectly via rewrite tactics |

Detail: [`PROM_16_REPORT.md`](PROM_16_REPORT.md) and [`SOURCES.md`](SOURCES.md).

---

## Status

The following describes the Lean/type-theory layer. Current repository, OS, and evidence status must be queried through the commands above.

- **Type system version**: v1 (canonical, no breaking change since 2026-04-29 PROM 16 axiom-foundation lock-in)
- **Lean layer evidence**: 2026-09-29 observation: 11 files, 0 sorry; run `./chu check --json` for fresh verification.
- **External canon grounding tier**: A (4 canons cross-referenced: Friedman / Wolfram / Voevodsky / Hyland)
- **OQ1 (universe level)**: RESOLVED (`lesson-chu-universe-resolution-2026-05-02`, both Type 0 and Type u sound)
- **OQ4 (Tegmark IV pairing)**: NUMEROLOGY_HOLD (form-iso unprovable; held as poetic pair)
- **Detailed status**: [`docs/STATUS.md`](docs/STATUS.md)

---

## License

Copyright © 2026 Ra Gyeongjun (라경준). Dual-licensed: **GNU AGPL-3.0-or-later** ([LICENSE](LICENSE)) or a separate commercial license ([LICENSING.md](LICENSING.md)). Until 2026-09-29 this material was MIT-declared inside SYMPOSIUM; see [LICENSING.md § License history](LICENSING.md#license-history).

---

<div align="center">

**Everything is a hypergraph. CHU is the stage. JaebaeMan is the cover. 비행기맨 is the apex.**

[Documentation](docs/index.md) · [Lean Sources](#lean-formalization) · [Changelog](CHANGELOG.md) · [SYMPOSIUM](../SYMPOSIUM/CLAUDE.md)

</div>

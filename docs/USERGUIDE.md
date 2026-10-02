# CHU User Guide

> How to read, use, and extend the Computable Hyperuniverse type system.
> Current OS/evidence navigation: [`../engineering/README.md`](../engineering/README.md) and `./chu repo status --json`. This guide covers only the Lean/type-theory layer; it is not a CHU OS or HSWM runtime guide.
>
> Quick overview: [`../README.md`](../README.md). Status: [`STATUS.md`](STATUS.md).

---

## Table of Contents

- [When to use CHU](#when-to-use-chu)
- [Type primitives](#type-primitives)
  - [`axiom CHU : Type`](#axiom-chu--type)
  - [`CHUPiece := CHU → Prop`](#chupiece--chu--prop)
  - [`JaebaeMan` inductive](#jaebaeman-inductive)
  - [`covers` / `anyCovers`](#covers--anycovers)
  - [`isAirplaneMan` (∀-cover predicate)](#isairplaneman--cover-predicate)
- [The hypergraph axiom](#the-hypergraph-axiom)
- [Five invariants (essence)](#five-invariants-essence)
- [Proof recipes](#proof-recipes)
- [Universe-level pragmatics (Type 0 vs Type u)](#universe-level-pragmatics-type-0-vs-type-u)
- [Common pitfalls](#common-pitfalls)
- [FAQ](#faq)

---

## When to use CHU

**Use CHU when:**

- Writing a Lean 4 proof that needs to quantify over "all things" without committing to set theory.
- Designing a KG node typology that needs μ-recursive nested coverage (Berge / Smarandache-style hyperedges are insufficient).
- Reasoning about a SYMPOSIUM construct (12 사도, 5 무기, APT phases, CHU lenses) — *every* such construct quantifies over `x : CHU` implicitly.
- Formalizing the "everything is a hypergraph" intuition without picking a particular graph database.
- Establishing the substrate over which `:Anchor` / `:Span` / `:Contract` (APT) and `:ReferenceSite` (Longinus) sit.

**Skip CHU when:**

- You need a concrete set theory model (use ZFC + Mathlib `Set` types).
- You need univalence / identity-as-path (use Cubical Agda or Coq-HoTT — Lean 4 mainline is UIP-friendly and HoTT-incompatible; see `PROM_16_REPORT.md` D3).
- You only need a simple `Finset` of hyperedges (Berge is sufficient; CHU is overkill).
- You're working purely in code without any formal-verification / KG-typology component.

A useful heuristic: if you ever say "this applies to *everything* in the system," you are reaching for CHU. Make it explicit.

---

## Type primitives

The CHU type system has exactly **6 primitives**. They are the entire declarative surface.

### `axiom CHU : Type`

```lean
axiom CHU : Type
```

This is the universe. It asserts that some type called `CHU` exists. **It does not assert any inhabitant.** It does not specify any equation, structure, or topology.

- It is *strictly weaker* than Lean's three standard axioms (`propext` / `Classical.choice` / `Quot.sound`) — it is a *type-level postulate*, not a propositional or quotient axiom.
- It is consistency-safe: assuming `CHU : Type` introduces no contradiction (PROM 16 C1).
- The choice of `Type` (universe 0) is the **default** for SYMPOSIUM data-phase semantics. The polymorphic alternative `axiom CHU : Type u` is also sound (see [`AirplaneMan_CHU_Universe.lean`](../lean/AirplaneMan_CHU_Universe.lean)).

### `CHUPiece := CHU → Prop`

```lean
def CHUPiece : Type := CHU → Prop
```

A *piece* of CHU is a **predicate** — a function that asks of any `x : CHU` whether `x` belongs to the piece.

This is the **Yoneda perspective**: an object is fully determined by its hom-set into another fixed object (here, `Prop`). ISP (Interface Segregation Principle) is the software cousin — "split an interface into pieces of its hom-set."

`CHUPiece` is **not** a subset of CHU in any set-theoretic sense. It is a function. This avoids commitment to a particular set theory model.

### `JaebaeMan` inductive

```lean
inductive JaebaeMan : Type where
  | atomic  : CHUPiece → JaebaeMan
  | governs : List JaebaeMan → JaebaeMan
  deriving Inhabited
```

`JaebaeMan` is a μ-recursive coverer:

- `atomic p` — Layer 1. Covers exactly the piece `p`.
- `governs js` — Layer N+1. Covers the **union** of what the `js : List JaebaeMan` cover.

This single inductive **strictly subsumes**:

- **Berge hypergraphs** (1-level finite hyperedges) — special case `atomic`.
- **Smarandache n-SHG** (𝒫ⁿ(V), finite n) — special case `governs` of finite depth n.
- And generalizes to **infinite depth** (because `JaebaeMan` is well-founded as Lean inductive, but the depth is *unbounded*).

The `deriving Inhabited` is intentional — there is always at least one JaebaeMan (e.g. `.atomic (fun _ => True)`), so the type is non-empty and proofs about it can use `Inhabited` machinery.

### `covers` / `anyCovers`

```lean
mutual
  def JaebaeMan.covers : JaebaeMan → CHU → Prop
    | .atomic p,  x => p x
    | .governs js, x => JaebaeMan.anyCovers js x

  def JaebaeMan.anyCovers : List JaebaeMan → CHU → Prop
    | [],        _ => False
    | j :: rest, x => j.covers x ∨ JaebaeMan.anyCovers rest x
end
```

`covers` defines coverage as **OR-union**: a `governs` JaebaeMan covers `x` iff *any* of its children covers `x`.

This is the **open-cover** semantics (not partition, not sheaf) — see [`AirplaneMan_Gap3_Cover.lean`](../lean/AirplaneMan_Gap3_Cover.lean) for why this is the canonical choice on a structureless CHU.

The mutual recursion via `anyCovers` is the standard Lean 4 idiom for definitions that recurse through `List X` where `X` is the inductive being defined.

### `isAirplaneMan` (∀-cover predicate)

```lean
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x
```

**The apex predicate.** A JaebaeMan `j` is a 비행기맨 (Airplane Man) iff `j` covers *every* element of CHU.

This single line formalizes the user's deepest intuition: **there exists one role whose coverage is total**. Apostles (12 사도) are *not* 비행기맨 in general — only the apex (#4) is. The other apostles cover proper sub-regions.

Witness: `trivialAirplaneMan := .atomic (fun _ => True)`. Proof: `intro _; trivial`.

---

## The hypergraph axiom

The user's name-list canon (2026-04-28) ends with:

> "그냥 모든것은 하이퍼그래프"
> (Everything is just a hypergraph.)

**Formal reading**:

> The set of *pieces* of CHU is isomorphic to the set of *hyperedges* of some hypergraph **H** whose vertices are CHU elements. Each `p : CHUPiece` is the characteristic function of one hyperedge `e ⊆ vertices(H)`.

So:

- CHU element = hypergraph vertex
- CHUPiece = hypergraph hyperedge (characteristic predicate)
- JaebaeMan = recursive nested hyperedge family (closed under OR-union)
- 비행기맨 = hyperedge family covering all vertices

This is *partially isomorphic* to **Wolfram 2020 Physics Project** (everything-is-hypergraph slogan):

- ✅ **Slogan equivalence**: Both axiomatize the universe as a hypergraph.
- ✅ **Dynamics layer** (2026-07-15 정정 — 이전엔 ⚠ gap "CHU has none"): Wolfram이 rewrite rule을 더하듯, CHU도 이제 갖고 있다. [`lean/CHU_WolframRewrite.lean`](../lean/CHU_WolframRewrite.lean)이 `Rewrite := CHU → CHU`(Def 2.2), `Step`(Def 2.4 multiway one-step), `Type`-valued `Path`를 정의하고 `lean` exit 0으로 검증됨 (신규 axiom 0 = I1 보존). 남은 것은 `governs` 인코딩 대응.
- ⚠ **Cardinality gap**: Wolfram is at the computability level (Wolfram Physics Model). CHU is at the type level (`axiom CHU : Type`).

See [`PROM_16_REPORT.md`](../PROM_16_REPORT.md) C3 for the open-question status.

---

## Five invariants (essence)

CHU enforces five invariants across every construction (see [`README.md`](../README.md#invariants)):

| # | Invariant | What it forbids |
|---|-----------|-----------------|
| **I1** | Axiomatic minimality | Adding inhabitant or equation to `CHU` (only `axiom CHU : Type`). |
| **I2** | Predicate-as-piece | Defining `CHUPiece` as anything other than `CHU → Prop`. |
| **I3** | Self-similar coverage | Adding a third constructor to `JaebaeMan` (`atomic` and `governs` only). |
| **I4** | OR-union coverage | Replacing `∨` with `∧` or XOR in `covers` (changes from open-cover to partition or otherwise). |
| **I5** | Russell avoidance | Asserting `CHU : CHU → Prop` or similar self-reference (`Girard's paradox`). |

Violate any → the inductive becomes unsound or the cover semantics drift. See [`../NATURE_RUSSELL_AVOIDANCE.md`](../NATURE_RUSSELL_AVOIDANCE.md) for I5 discipline.

---

## Proof recipes

### Recipe 1 — Construct a trivial 비행기맨

```lean
def wholeCHU : CHUPiece := fun _ => True
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU

theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by
  intro _; trivial
```

The simplest possible 비행기맨: a single atomic piece whose predicate is `True`.

### Recipe 2 — Lift any 비행기맨 by one layer

```lean
theorem lift_airplaneman (j : JaebaeMan) :
    isAirplaneMan j → isAirplaneMan (JaebaeMan.governs [j]) := by
  intro hj x
  exact Or.inl (hj x)
```

Wrapping a 비행기맨 in `governs [_]` keeps it a 비행기맨. This is the **self-similar lift**.

### Recipe 3 — Construct a 비행기맨 at any depth n

```lean
def airplaneManAt : Nat → JaebaeMan
  | 0     => trivialAirplaneMan
  | n + 1 => .governs [airplaneManAt n]

theorem airplaneManAt_is (n : Nat) : isAirplaneMan (airplaneManAt n) := by
  induction n with
  | zero => exact trivialAirplaneMan_is
  | succ k ih => intro x; exact Or.inl (ih x)
```

**For every depth n, a 비행기맨 exists**. The self-similar fractal hierarchy is non-vacuous at every level.

### Recipe 4 — Union of 비행기맨s

```lean
theorem airplanemen_union (j₁ j₂ : JaebaeMan) :
    isAirplaneMan j₁ → isAirplaneMan (JaebaeMan.governs [j₁, j₂]) := by
  intro h₁ x
  exact Or.inl (h₁ x)
```

If `j₁` covers everything, then `governs [j₁, j₂]` also covers everything regardless of `j₂`.

### Recipe 5 — Existential lift

```lean
theorem exists_airplaneman_below (js : List JaebaeMan) :
    (∃ j ∈ js, isAirplaneMan j) → isAirplaneMan (JaebaeMan.governs js) := by
  intro ⟨j, hmem, hj⟩ x
  induction js with
  | nil => exact absurd hmem (by intro h; cases h)
  | cons head tail ih =>
    rw [List.mem_cons] at hmem
    cases hmem with
    | inl heq => subst heq; exact Or.inl (hj x)
    | inr hrest => exact Or.inr (ih hrest)
```

If *any* child is a 비행기맨, the parent is too.

All 5 recipes are in [`AirplaneMan.lean`](../lean/AirplaneMan.lean); the Mathlib-free verification statement is a dated Lean-layer observation, not current OS evidence.

---

## Universe-level pragmatics (Type 0 vs Type u)

`axiom CHU : Type` puts CHU at **universe 0** (set-level).

`axiom CHU : Type u` would make it **universe-polymorphic** (can hold types as elements).

PROM 16 OQ1 resolution (`lesson-chu-universe-resolution-2026-05-02`):

- **Both are sound.** Neither introduces inconsistency.
- **SYMPOSIUM default is `Type` (universe 0)** because the user spec defines CHU as "pure data phase of #8 OM" — first-order data, no embedded types.
- **`Type u` is available on demand** for future embeddings of type-theoretic apparatus on top of CHU (e.g. embedding categories of types as CHU pieces).

The full proof that both options compile to genuine `Inhabited` JaebaeMan inductives is in [`AirplaneMan_CHU_Universe.lean`](../lean/AirplaneMan_CHU_Universe.lean) — two namespaces `Type0` and `TypeU`, each with a working `trivialAirplaneMan_is`.

⚠ **Caveat (I5)**: if a future axiom asserts `CHU : CHU → Prop` style self-reference (Russell-style universe-of-universes), **Girard's paradox** strikes both options. The fix is to *not add that axiom*, not to change CHU's universe level.

---

## Common pitfalls

### Pitfall 1 — Treating `CHUPiece` as a `Set`

❌ Wrong:

```lean
def MyPiece : Set CHU := { x | x.someProperty }   -- requires Mathlib + commits to set theory
```

✅ Right:

```lean
def MyPiece : CHUPiece := fun x => x.someProperty   -- pure predicate
```

`CHUPiece` is a predicate, not a `Set`. Using `Set` pulls in Mathlib and commits to a set-theory model.

### Pitfall 2 — Forgetting `governs []` covers nothing

```lean
theorem governs_empty_no_cover (x : CHU) :
    ¬ (JaebaeMan.governs []).covers x := by
  intro h; exact h
```

`(.governs [])` is a valid JaebaeMan (the empty governor) but it covers **nothing**. It is never a 비행기맨. If you accidentally construct `(.governs [])` you have an empty coverer.

### Pitfall 3 — Trying to define cover as AND/partition

```lean
-- ❌ Wrong: makes JaebaeMan unsound for the SYMPOSIUM "everything overlaps" semantics
def covers' : JaebaeMan → CHU → Prop
  | .governs js, x => js.all (fun j => j.covers x)   -- AND, not OR
```

CHU coverage is **OR-union (open cover)**. Layer 1 pieces *can* and often *do* overlap. The user's intuition is "resonance" (공명), not "partition" (분할). See [`AirplaneMan_Gap3_Cover.lean`](../lean/AirplaneMan_Gap3_Cover.lean) for the formal argument.

### Pitfall 4 — `∀ x : CHU` without any inhabitant axiom

```lean
-- ❌ Vacuous: there's no axiom that CHU is non-empty
theorem foo : ∀ x : CHU, ... := ...
```

`axiom CHU : Type` does not assert `Inhabited CHU`. `∀ x : CHU` may be vacuous (Lean accepts it, but you can't construct an `x : CHU` directly). If you need a witness, add `axiom chu_nonempty : Inhabited CHU` or work with `isAirplaneMan` which is universally quantified anyway.

### Pitfall 5 — Mutating I5 (Russell)

❌ Never:

```lean
axiom CHU_is_piece : CHU = (CHU → Prop)   -- Girard's paradox
```

If you ever feel you "need" to assert CHU equals its own piece-space, **rethink your design**. See [`../NATURE_RUSSELL_AVOIDANCE.md`](../NATURE_RUSSELL_AVOIDANCE.md).

---

## FAQ

**Q: Why `axiom` and not `def CHU := ...`?**
A: Because we don't want to commit to any concrete model. `axiom CHU : Type` makes CHU model-independent. Any proof that uses only the axiom transfers to any concrete CHU model later.

**Q: Is CHU the same as a Tegmark IV mathematical universe?**
A: No — Tegmark IV has no formal definition of "structure." CHU is concretely a Lean 4 type. The pairing is held as a poetic resemblance only (NUMEROLOGY_HOLD, see PROM 16 D4).

**Q: Can I have an infinite list of children in `governs`?**
A: `List JaebaeMan` is always finite. For **infinite families** of Layer 1 pieces, see [`AirplaneMan_Gap3_Cover.lean`](../lean/AirplaneMan_Gap3_Cover.lean) which uses `Set CHUPiece` to express open covers of infinite cardinality.

**Q: Is CHU a category?**
A: It is a `Type`, which is an object of the category of types. The inductive `JaebaeMan` over CHUPiece can be viewed as a free monad on the `(- + List -)` functor (μ-recursive initial algebra). See [`AirplaneMan_Gap4_Category.lean`](../lean/AirplaneMan_Gap4_Category.lean) for the categorical interpretation.

**Q: How does CHU relate to APT?**
A: APT's `:Anchor`, `:Span`, `:Contract` are all CHU pieces under the hood. CHU is the substrate; APT is one methodology that operates on CHU substrate. See [`../APT/README.md`](../../SYMPOSIUM/THEORY/APT/README.md).

**Q: How does CHU relate to Longinus?**
A: Longinus 7-Layer Reference Model is one *lens* onto CHU (each layer is a CHUPiece). The reverse-orphan scan in Longinus v3 is implemented by scanning CHU pieces that are referenced but not covered.

**Q: Why is `CHU` capitalized in the user's prose but `chu` lowercase in some user utterances?**
A: User-stylistic. We canonize **CHU** uppercase in formal contexts. Lowercase `chu` in user utterances is the same entity.

**Q: Where is the "computable" of "Computable Hyperuniverse"?**
A: At the **realizability layer overlay**, not in `axiom CHU : Type` itself. Hyland Effective Topos `Eff(N)` (PROM 16 A3) provides the realizability model — predicates that are decidable / partial-recursive / BHK-realizable form a sub-topos. `axiom CHU : Type` is hyperuniverse-level; "computable" is the *modular restriction* we work in.

---

For more depth see [`../PROM_16_REPORT.md`](../PROM_16_REPORT.md), [`../SOURCES.md`](../SOURCES.md), and the current local Lean files in [`../lean/`](../lean/). Historical origin: `MIND/lean_formalization/AirplaneMan*.lean` (provenance only).

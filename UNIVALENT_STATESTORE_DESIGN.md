# Univalent StateStore — design (the un-truncated identity regime)

> **Status: IMPLEMENTED (level-2, strictly additive) 2026-07-13.** `chu_core_prototype/chu_core.rs`
> — `UnivalentStateStore` trait + `BackendLocal` impl + `evolve_univalent`; native asserts + wasm32 green
> (see §5). Extends `333_ADAPTER_CONTRACT.md` §1.2 `StateStore`.
> Answers the OPEN fork from `finding-prom16-wolfram-chu-A4-S2` (FORK_GROUNDED): the current
> store is the *strict-eq* pole; this is the *univalent* pole. Both are realisable; the choice
> is a truncation level, not a correctness question.
> KG: `lesson-neo4j-is-strict-eq-1category-truncation-of-chu-infgroupoid-2026-07-13`,
> `prom16-wolfram-chu-ruliad-hott-2026-07-13`. Lean: `CHU_WolframRewrite.lean` (`Cell`, `strict_truncation2`).

---

## 0. The problem

`BackendLocal::StateStore` keys states by `cid = hash(sorted edges)`. Two states are identified
**iff their edge sets are literally equal** — strict propositional equality. Per Lean
`strict_truncation` / `strict_truncation2`, that collapses the whole homotopy tower to a
**1-category**: every parallel derivation and every equivalence-between-derivations is discarded.
That is exactly a property-graph DB (Neo4j). It is correct, cheap, and lossy.

The Ruliad (arXiv:2111.03460 Prop 4.3/4.4) is the **un-truncated** object: states are identified
by *homotopy* (a witnessed path-between-paths), not by literal equality, and the identifications
*carry data*. A univalent StateStore stores those witnesses instead of collapsing.

---

## 1. The extension

```rust
/// A homotopy witness between two states/derivations = a level-2 `Cell` (Lean), i.e. a
/// sequence of higher rewrite moves turning one derivation into a parallel one.
pub struct HomotopyWitness { pub moves: Vec<HigherMove>, pub provenance: Cid }
type HCid = u64;

pub trait UnivalentStateStore: StateStore {
    /// Record (do NOT collapse) that a and b are the same up to `w`. Returns a 2-cell id.
    fn put_homotopy(&mut self, a: Cid, b: Cid, w: HomotopyWitness) -> HCid;
    /// Univalent identity: a ≡ b iff a homotopy witness connects them (reflexive-transitive).
    fn identified(&self, a: Cid, b: Cid) -> bool;
    /// Univalence transport: a fact/metric proven of `a` moves to `b` along the witness.
    fn transport<T: Clone>(&self, a: Cid, b: Cid, datum: &T) -> Option<T>;
}
```

- `HomotopyWitness.moves` is precisely the `Cell` inductive from the Lean level-2 layer — the
  store persists what `Cell` denotes.
- Strict and univalent regimes **coexist**: `cid` still gives the 1-truncation view (fast DB
  queries, Neo4j-compatible); `identified`/`transport` give the ∞-groupoid view on demand. A
  consumer picks the truncation level per query — this *is* "CHU viewable at any homotopy level."

---

## 2. Three design forks (all OPEN)

### F1 — witness representation & storage cost
A witness is a 2-path in a 2-graph; naively O(derivation length). Options: (a) store full move
sequences (faithful, heavy); (b) store only witness *existence* + a seed to re-derive (cheap,
recomputable); (c) normal-form witnesses (canonical 2-cell per pair). **Recommend (b)** for the
first pass — matches ooptdd "earn, don't cache" discipline (re-derive the witness on demand).

### F2 — isomorphism-up-to-relabeling (the expensive one)
Wolfram states are *labeled*; `{ {1,2} }` and `{ {7,9} }` are the same hypergraph under node
renaming but have different `cid`. True univalent identity must quotient by graph isomorphism —
which is **GI-complete** (no known poly algorithm). Honest cost. Options: (a) canonical labeling
(nauty/bliss-style) as the `cid` — moves the cost into `put`; (b) keep raw `cid` + record isos
lazily as homotopy witnesses only where two branches actually meet (pay only on observed merges).
**Recommend (b)**: the Ruliad's mergers are exactly "different computations, equivalent outcome",
so canonicalise *at merge points*, not eagerly. Never silently claim full GI closure.

### F3 — transport semantics
Univalence gives `transport` for free *in type theory*; here it must be implemented per datum
kind. Safe subset first: transport metrics that are **isomorphism-invariant** (state count,
degree sequence, causal-graph shape). Non-invariant data (raw node ids) must NOT transport —
guard it. `transport` returns `Option` so a non-invariant datum yields `None`, not a lie.

---

## 3. Why this matters (ties the whole arc)

- The opening question ("why beyond Neo4j to CHU?") gets its *operational* answer here: Neo4j =
  the `cid`-only strict store; CHU's value = the `HomotopyWitness` layer Neo4j structurally cannot
  hold (Cypher has no notion of a proof-of-equivalence-between-derivations).
- It is strictly additive: the univalent store *contains* the strict store (`cid` untouched) and
  adds the 2-cell layer. So adopting it never breaks the 1-truncation / DB path — it de-truncates.

---

## 4. Honest status & recommendation

- **IMPLEMENTED (2026-07-13), level-2, strictly additive.** `chu_core.rs` now carries the
  `UnivalentStateStore` trait + `BackendLocal` impl: `put_homotopy` (union-find over relabel
  witnesses), `identified` (reflexive–transitive closure), `transport` (F3 guard), and
  `evolve_univalent` (records witnesses at observed merges). `HigherMove` = the Lean `Cell.move`
  generator, split into `Merge` (path-2-cell at literal co-termination — recorded WITHOUT
  identifying the distinct parents) and `Relabel` (F2-b iso-2-cell). The strict
  `StateStore`/`evolve`/`cid` path is byte-for-byte untouched — both `main` assert-blocks pass.
- **GI-hardness (F2) is real** — honored: `canonical_cid` canonicalises exactly only for
  ≤ `CANON_MAX_NODES` (7) nodes and returns `None` above it (state stays strict), with
  `canon_hits`/`canon_skips` logged. Never presents partial iso-closure as full.
- **Recommended path — taken.** Strict `cid` stays default/primary; the univalent layer pays
  homotopy/canonicalisation cost only at observed merges (F1-b existence+seed, F2-b at-merge,
  F3 invariant-only). Full ∞-groupoid closure stays OPEN — bare Lean/Rust lack native HITs,
  consistent with the level-2-only Lean formalisation.

## 5. Implementation receipt (2026-07-13)

`chu_core_prototype/chu_core.rs` (rustc 1.97, std-only, no external crates):
- **native** — `rustc chu_core.rs -o chu_core && ./chu_core` ⇒ `ALL ASSERTS PASS` + `ALL UNIVALENT ASSERTS PASS`.
- **wasm32** — `rustc --target wasm32-unknown-unknown --crate-type=cdylib -C panic=abort chu_core.rs` ⇒ OK; exports `chu_explore_count`, `chu_witness_count`.
- **Concrete de-truncation**: `demo_job(4)` = **34 strict `cid`s → 17 homotopy witnesses** recorded
  (iso identifications the `cid`-only / Neo4j store structurally drops); all 34 states canonicalised
  exactly (0 skips). This *is* "CHU viewable at any homotopy level" — the same run yields a 34-object
  1-truncation and a coarser ∞-groupoid view on demand.
- **Soundness asserted**: a non-isomorphic pair is never `identified`; a `RawNodeId` datum never
  `transport`s (`None`, not a relabeled lie).
- **Design refinement**: the sketch's `transport<T: Clone>` was tightened to `transport<T: Transportable>`
  so the F3 "None, not a lie" guard is actually enforceable (a bare generic cannot decide invariance).
- **Still OPEN (by design)**: the genuine `n→∞` colimit / native HITs (tower levels ≥ 3) — unchanged.

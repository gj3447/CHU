# CHU-Wolfram ↔ 333 Adapter Contract (decouple sketch)

> **Status: PRELIMINARY DESIGN (no code).** The decoupling *interface*, not an implementation.
> Verdict (2026-07-13): develop the CHU-Wolfram core **standalone against this Contract**;
> 333 is *one* backend behind it, ORRR another. Full 333/ORRR wiring = 엄청 나중.
> Grounds: Contract = 재배맨's dual (APT root axiom); 333 modules already app-agnostic; ORRR unbuilt.
> KG: `prom16-wolfram-chu-ruliad-hott-2026-07-13`, `orrr-orbital-rain-ruin-rein-2026-05-15`,
> `apt-contract-root-axiom-2026-05-27`.

---

## 0. Why a Contract (not deep melding)

The CHU core = a **multiway rewrite explorer**: given a rule set and an initial hyperstate,
it walks Wolfram update rules `H₁→H₂` to build a multiway subgraph (§CHU_WolframRewrite.lean:
`Rewrite / Step / Path / Cell`). Exploring the Ruliad is **compute- and state-heavy** but the
core logic is substrate-agnostic. So the core depends only on 4 abstract *ports*; each has a
local in-process default and a 333/ORRR implementation. Per the contract-dual-coupling canon:
at **coupling = 0** every port degenerates to its identity element (local, no network) — the
core runs fully standalone. 333 becomes non-trivial only when you actually distribute.

```
   CHU-Wolfram core  ──depends-on──▶  4 Ports (Contract)
                                        ├─ ComputeSink   ← local | dgx | ORRR(paid)
                                        ├─ StateStore    ← memory | 333 DHT+IndexedDB
                                        ├─ BranchBus     ← in-proc | 333 PubSub/CRDT
                                        └─ Identity      ← anon | 333 Ed25519
```

---

## 1. The four ports (language-neutral; Rust/WASM-flavored since 333 = WASM)

### 1.1 `ComputeSink` — where rewriting actually runs
```rust
trait ComputeSink {
    /// Submit one rewrite job; returns the produced multiway subgraph (states + causal edges).
    fn evolve(&self, job: RewriteJob) -> MultiwayFragment;
}
struct RewriteJob { rules: RuleSet, init: HyperState, max_steps: u32, branch_policy: BranchPolicy }
```
- **local**: run in the same process (dev / small ruliad slice).
- **dgx**: submit to the dgx GB10 (existing vLLM/compute box) — batch exploration.
- **ORRR** (paid marketplace, on top of 333): rent compute; Rain = compute 비처럼 내림.
  `orrr-orbital-rain-ruin-rein-2026-05-15`. **This is the natural home for large ruliad sweeps.**

### 1.2 `StateStore` — content-addressed hyperstate persistence
```rust
trait StateStore {
    fn put(&self, s: &HyperState) -> Cid;         // content hash = node identity
    fn get(&self, cid: &Cid) -> Option<HyperState>;
}
```
- Hyperstates are **content-addressed** — the CID *is* the CHU-node identity. This is exactly
  the strict-eq / distinct-node identity regime (= 1-category truncation; see
  `lesson-neo4j-is-strict-eq-1category-truncation-of-chu-infgroupoid-2026-07-13`). A univalent
  store additionally records *homotopies* between CIDs (level-2 `Cell`) — **IMPLEMENTED 2026-07-13**
  in `chu_core.rs` (`UnivalentStateStore`); see `UNIVALENT_STATESTORE_DESIGN.md` §5.
- **333 backend**: `333_MOD_Storage` (DHT/Kademlia k=3 + IndexedDB local cache, Merkle integrity).

### 1.3 `BranchBus` — distribute multiway branches across peers
```rust
trait BranchBus {
    fn publish(&self, frag: &MultiwayFragment);
    fn subscribe(&self, on_fragment: impl Fn(MultiwayFragment));
}
```
- Multiway exploration is embarrassingly parallel *and* mergeable (paths merge on state
  equivalence — Ruliad property). Peers each explore a region, gossip fragments, and merge.
- **333 backend**: `333_MOD_PubSub` (typed topics) + `333_MOD_CRDT` (OR_Set of states,
  LWW_Map of edges) for conflict-free merge = the causal-invariance "different orders,
  same graph" property implemented as CRDT convergence.

### 1.4 `Identity` — who contributed which branch
```rust
trait Identity { fn sign(&self, frag: &MultiwayFragment) -> Sig; fn peer(&self) -> PeerId; }
```
- **333 backend**: `333_MOD_Identity` (Ed25519, PeerId = pubkey hash). Enables ORRR
  attribution/payment (who earned compute credit) + anti-Sybil (`333_SybilResistance`).

---

## 2. Backend mapping (each port × substrate)

| Port | local (coupling=0) | 333 module | ORRR |
|---|---|---|---|
| ComputeSink | in-proc loop | (via 333 Runtime WASM) | **paid marketplace** ← primary value |
| StateStore | HashMap | `333_MOD_Storage` DHT+IDB | (uses 333) |
| BranchBus | direct call | `333_MOD_PubSub` + `333_MOD_CRDT` | (uses 333) |
| Identity | anon | `333_MOD_Identity` Ed25519 | attribution/payment |

**Stack**: `333 (P2P 무료 base) → ORRR (paid compute) → CHU-Wolfram core`. The core imports the
4 traits; a `Backend333` bundle implements all four; `BackendLocal` is the degenerate identity.

---

## 3. Honest status & OPEN

- **PRELIMINARY interface; core now runnable.** `chu_core_prototype/chu_core.rs` implements the 4
  ports against this Contract — `BackendLocal` (coupling=0) as a real multiway rewrite explorer,
  strict `StateStore` + the additive `UnivalentStateStore` (level-2). native asserts + wasm32 green.
- The CHU dynamics layer is also formalised in Lean
  (`MIND/lean_formalization/CHU_WolframRewrite.lean`, exit 0; level 1 + level 2), which the Rust
  `HigherMove` ↔ `Cell.move` correspondence mirrors.
- **OPEN**: (1) univalent `StateStore` — **RESOLVED 2026-07-13** (`UnivalentStateStore` in
  `chu_core.rs`; `UNIVALENT_STATESTORE_DESIGN.md` §5). (2) ORRR itself is unbuilt (canonical name
  only). (3) `BranchPolicy` (how to bound ruliad exploration) undefined.
- Path forward is **B (decouple)**: `BackendLocal` first → prove the core explores a small
  ruliad slice → only then `Backend333` as a swap. A→풀스택 stays a *risk-free* later.

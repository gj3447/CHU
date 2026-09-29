//! CHU-Wolfram core — BackendLocal first implementation (the decouple-B substrate-agnostic core).
//!
//! Concretises `333_ADAPTER_CONTRACT.md`: the 4 ports (ComputeSink / StateStore / BranchBus /
//! Identity) as traits, with an in-process `BackendLocal` degenerate implementation (coupling=0,
//! no network). The core is a REAL multiway hypergraph-rewrite explorer:
//!   - HyperState = a Wolfram spatial hypergraph = finite collection of ordered relations
//!     (arXiv:2111.03460 Def 2.1: E ⊂ P(V)\{∅}, ordered).
//!   - Rule = an update rule H1->H2 over node VARIABLES (Def 2.2 = set-substitution system).
//!   - evolve() = the multiway system (Def 2.4): apply every rule at every match, dedup states
//!     by content hash. Content-hash identity = STRICT equality = the 1-category truncation the
//!     Lean side proves (lesson-neo4j-is-strict-eq-1category-truncation-of-chu-infgroupoid).
//!
//! No external crates (std only) so it builds with a bare `rustc` — no cargo `target/` dir.
//!   Native (verify): rustc chu_core.rs -o chu_core && ./chu_core
//!   WASM  (333 fit): rustc --target wasm32-unknown-unknown --crate-type=cdylib -C panic=abort chu_core.rs
//!
//! KG: prom16-wolfram-chu-ruliad-hott-2026-07-13, orrr-orbital-rain-ruin-rein-2026-05-15

use std::collections::hash_map::DefaultHasher;
use std::collections::{HashMap, HashSet};
use std::hash::{Hash, Hasher};

// ---------- CHU data (Wolfram hypergraph) ----------

/// A hyperedge = an ordered relation between node ids (n-ary, not just binary).
type Edge = Vec<u32>;

/// A HyperState = a finite collection of ordered relations = one point of CHU.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HyperState {
    edges: Vec<Edge>,
}

impl HyperState {
    fn new(mut edges: Vec<Edge>) -> Self {
        edges.sort();
        edges.dedup();
        HyperState { edges }
    }
    /// Content id (Cid): hash of the canonical (sorted) edge set. Two states are identified
    /// iff they have the same edge multiset — STRICT equality (the 1-category truncation).
    fn cid(&self) -> u64 {
        let mut h = DefaultHasher::new();
        self.edges.hash(&mut h);
        h.finish()
    }
    fn max_node(&self) -> u32 {
        self.edges.iter().flatten().copied().max().unwrap_or(0)
    }
}

type Cid = u64;

/// An update rule H1->H2 over node VARIABLES (negative ints = variables, matched to real nodes;
/// RHS variables absent from LHS become FRESH nodes on application).
#[derive(Clone)]
pub struct Rule {
    lhs: Vec<Vec<i32>>,
    rhs: Vec<Vec<i32>>,
}

/// The produced multiway subgraph: states (by cid) + causal/update edges between them.
#[derive(Default)]
pub struct MultiwayFragment {
    pub states: HashMap<Cid, HyperState>,
    pub updates: Vec<(Cid, Cid)>, // (from, to) per rule application
}

pub struct RewriteJob {
    pub rules: Vec<Rule>,
    pub init: HyperState,
    pub max_steps: u32,
}

// ---------- the 4 ports (the Contract) ----------

pub trait ComputeSink {
    fn evolve(&mut self, job: &RewriteJob) -> MultiwayFragment;
}
pub trait StateStore {
    fn put(&mut self, s: &HyperState) -> Cid;
    fn get(&self, cid: &Cid) -> Option<&HyperState>;
}
pub trait BranchBus {
    fn publish(&mut self, frag: &MultiwayFragment);
}
pub trait Identity {
    fn peer(&self) -> String;
    fn sign(&self, data: u64) -> u64;
}

// ---------- univalent (level-2) extension: the un-truncated identity regime ----------
// Design: UNIVALENT_STATESTORE_DESIGN.md §1/§4 — strictly ADDITIVE over the strict `cid` store.
// F1-b (earn-don't-cache witnesses) · F2-b (canonicalise only at observed merges, never claim
// full GI) · F3 (transport iso-invariant metrics only, else None — an honest refusal).
// Lean: CHU_WolframRewrite.lean (`Cell`, `strict_truncation2`). KG: prom16-wolfram-chu-ruliad-hott-2026-07-13.

pub type HCid = u64;

/// One `Cell.move` generator (Lean `CHU_WolframRewrite.lean:120`,
/// `move : hr p q → Cell q r → Cell p r`): a single higher-rewrite step relating two *parallel*
/// level-1 derivations. F1-b keeps only the move's IDENTITY, not the full re-derivable 2-path.
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub enum HigherMove {
    /// Two distinct derivations co-terminate at one state (literal multiway merge): a path-level
    /// 2-cell that paths reaching `meet` via `a_path` / `b_path` are parallel. NOT a claim that
    /// the parents are the same state — literal co-termination is not state-identity.
    Merge { a_path: Cid, b_path: Cid, meet: Cid },
    /// Two states are equal up to node relabeling (F2-b graph isomorphism): the higher rule is
    /// the relabeling, certified by a shared canonical form `canon`.
    Relabel { canon: Cid },
}

/// A 2-cell (homotopy) as a move-sequence — the Lean `Cell` as `vtrans` of `move` generators.
#[derive(Clone, Debug)]
pub struct HomotopyWitness {
    pub moves: Vec<HigherMove>,
    /// F1-b re-derivation seed: the state the witness is recomputable from (not cached in full).
    pub provenance: Cid,
}

/// A datum `transport` MAY carry across a univalence identification. F3: only
/// isomorphism-invariant data returns `Some`; non-invariant data (raw node ids) returns `None`
/// (never a relabeled lie). Refines the design's bare `<T: Clone>` so the guard is enforceable.
pub trait Transportable: Clone {
    fn iso_invariant(&self) -> bool;
}

/// The un-truncated store: the strict `StateStore` (`cid`, 1-truncation, Neo4j-shaped) PLUS the
/// level-2 witness layer that Cypher structurally cannot hold (a proof-of-equivalence-between-
/// derivations). Adopting it never breaks the strict/DB path — it *de-truncates* it.
pub trait UnivalentStateStore: StateStore {
    /// Record (do NOT collapse) that `a` and `b` are the same up to `w`. Returns the 2-cell id.
    fn put_homotopy(&mut self, a: Cid, b: Cid, w: HomotopyWitness) -> HCid;
    /// Univalent identity: reflexive–transitive closure over recorded relabel witnesses.
    fn identified(&self, a: Cid, b: Cid) -> bool;
    /// Univalence transport along the identification; `None` for non-invariant data (F3).
    fn transport<T: Transportable>(&self, a: Cid, b: Cid, datum: &T) -> Option<T>;
}

/// Demo transportable metrics: the invariant ones cross an identification; a raw node id does not.
#[derive(Clone, Debug, PartialEq)]
pub enum Datum {
    StateCount(usize),        // iso-invariant
    EdgeCount(usize),         // iso-invariant
    DegreeSequence(Vec<u32>), // iso-invariant
    RawNodeId(u32),           // NOT invariant — must not transport
}
impl Transportable for Datum {
    fn iso_invariant(&self) -> bool {
        !matches!(self, Datum::RawNodeId(_))
    }
}

// ---------- rewrite engine (the real multiway logic) ----------

/// Try to match all LHS edges against `state`, extending `bind` (variable->node). Returns every
/// complete binding (each = one distinct rule application site => one multiway branch).
fn matches(lhs: &[Vec<i32>], state: &HyperState) -> Vec<HashMap<i32, u32>> {
    fn go(
        lhs: &[Vec<i32>],
        i: usize,
        state: &HyperState,
        bind: HashMap<i32, u32>,
        out: &mut Vec<HashMap<i32, u32>>,
    ) {
        if i == lhs.len() {
            out.push(bind);
            return;
        }
        let pat = &lhs[i];
        for edge in &state.edges {
            if edge.len() != pat.len() {
                continue;
            }
            let mut b = bind.clone();
            let mut ok = true;
            for (v, &node) in pat.iter().zip(edge.iter()) {
                match b.get(v) {
                    Some(&existing) if existing != node => {
                        ok = false;
                        break;
                    }
                    _ => {
                        b.insert(*v, node);
                    }
                }
            }
            if ok {
                go(lhs, i + 1, state, b, out);
            }
        }
    }
    let mut out = Vec::new();
    go(lhs, 0, state, HashMap::new(), &mut out);
    out
}

/// Apply one rule at one binding: remove matched LHS edges, add RHS edges (fresh nodes for
/// RHS-only variables). Returns the successor state.
fn apply(rule: &Rule, bind: &HashMap<i32, u32>, state: &HyperState, fresh_base: u32) -> HyperState {
    // Concrete matched LHS edges to remove.
    let mut removed: HashSet<Edge> = HashSet::new();
    for pat in &rule.lhs {
        let e: Edge = pat.iter().map(|v| bind[v]).collect();
        removed.insert(e);
    }
    let mut edges: Vec<Edge> = state
        .edges
        .iter()
        .filter(|e| !removed.contains(*e))
        .cloned()
        .collect();
    // Resolve RHS, minting fresh nodes for variables not bound by the LHS.
    let mut b = bind.clone();
    let mut next_fresh = fresh_base + 1;
    for pat in &rule.rhs {
        let mut e: Edge = Vec::with_capacity(pat.len());
        for v in pat {
            let node = match b.get(v) {
                Some(&n) => n,
                None => {
                    let n = next_fresh;
                    next_fresh += 1;
                    b.insert(*v, n);
                    n
                }
            };
            e.push(node);
        }
        edges.push(e);
    }
    HyperState::new(edges)
}

// ---------- BackendLocal: coupling=0 degenerate implementation of all 4 ports ----------

#[derive(Default)]
pub struct BackendLocal {
    store: HashMap<Cid, HyperState>,
    published: usize,
    // --- univalent (level-2) layer; the strict `store`/`cid` path above is left untouched ---
    witnesses: HashMap<HCid, HomotopyWitness>,
    uf_parent: HashMap<Cid, Cid>, // union-find over cids for identified()'s refl-trans closure
    canon_hits: usize,            // F2-b: states we canonicalised exactly
    canon_skips: usize,           // states too big to certify => kept strict (never falsely iso'd)
}

impl StateStore for BackendLocal {
    fn put(&mut self, s: &HyperState) -> Cid {
        let c = s.cid();
        self.store.entry(c).or_insert_with(|| s.clone());
        c
    }
    fn get(&self, cid: &Cid) -> Option<&HyperState> {
        self.store.get(cid)
    }
}
impl BranchBus for BackendLocal {
    fn publish(&mut self, frag: &MultiwayFragment) {
        // Degenerate: no network, just count (a 333 BranchBus would gossip via PubSub/CRDT).
        self.published += frag.states.len();
    }
}
impl Identity for BackendLocal {
    fn peer(&self) -> String {
        "local:anon".to_string()
    }
    fn sign(&self, data: u64) -> u64 {
        data // degenerate identity element (no crypto; 333 => Ed25519)
    }
}
impl ComputeSink for BackendLocal {
    fn evolve(&mut self, job: &RewriteJob) -> MultiwayFragment {
        let mut frag = MultiwayFragment::default();
        let init_cid = self.put(&job.init);
        frag.states.insert(init_cid, job.init.clone());
        let mut frontier = vec![job.init.clone()];
        for _step in 0..job.max_steps {
            let mut next = Vec::new();
            for state in &frontier {
                let from = state.cid();
                let base = state.max_node();
                for rule in &job.rules {
                    for bind in matches(&rule.lhs, state) {
                        let succ = apply(rule, &bind, state, base);
                        let to = self.put(&succ);
                        frag.updates.push((from, to));
                        if !frag.states.contains_key(&to) {
                            frag.states.insert(to, succ.clone());
                            next.push(succ); // new state => keep exploring (mergers dedup here)
                        }
                    }
                }
            }
            if next.is_empty() {
                break;
            }
            frontier = next;
        }
        frag
    }
}

// ---------- BackendLocal: univalent (level-2) impl — strictly additive to the strict impls ----------

// F2-b: EXACT canonical form, sound only up to CANON_MAX_NODES nodes. Above it we canonicalise
// NOTHING and keep the strict `cid` (GI is GI-complete; we never present partial closure as full).
const CANON_MAX_NODES: usize = 7;

/// Distinct nodes of a state, sorted.
fn nodes_of(s: &HyperState) -> Vec<u32> {
    let mut v: Vec<u32> = s.edges.iter().flatten().copied().collect();
    v.sort();
    v.dedup();
    v
}

/// All permutations of `0..n` (Heap's algorithm); n ≤ CANON_MAX_NODES so ≤ 5040, run only at merges.
fn perms(n: usize) -> Vec<Vec<usize>> {
    let mut a: Vec<usize> = (0..n).collect();
    let mut out = vec![a.clone()];
    let mut c = vec![0usize; n];
    let mut i = 0;
    while i < n {
        if c[i] < i {
            if i % 2 == 0 {
                a.swap(0, i);
            } else {
                a.swap(c[i], i);
            }
            out.push(a.clone());
            c[i] += 1;
            i = 0;
        } else {
            c[i] = 0;
            i += 1;
        }
    }
    out
}

/// EXACT canonical form via lexicographically-minimal relabeling. `Some(c)` ⇒ any state sharing
/// `c` is PROVABLY isomorphic (equal canon ⟺ iso). `None` ⇒ too big to certify — the caller must
/// fall back to strict `cid` and NOT assume iso. Design F2-b (canonicalise at merge points only).
fn canonical_cid(s: &HyperState) -> Option<Cid> {
    let nodes = nodes_of(s);
    let n = nodes.len();
    if n > CANON_MAX_NODES {
        return None;
    }
    let index: HashMap<u32, usize> = nodes.iter().enumerate().map(|(i, &x)| (x, i)).collect();
    let mut best: Option<Vec<Edge>> = None;
    for p in perms(n) {
        let mut relabeled: Vec<Edge> = s
            .edges
            .iter()
            .map(|e| e.iter().map(|x| p[index[x]] as u32).collect())
            .collect();
        relabeled.sort();
        if best.as_ref().map_or(true, |b| relabeled < *b) {
            best = Some(relabeled);
        }
    }
    let mut h = DefaultHasher::new();
    best.hash(&mut h);
    Some(h.finish())
}

impl BackendLocal {
    /// Read-only union-find root (a missing key is its own root — untouched cids stay strict).
    fn uf_root(&self, mut c: Cid) -> Cid {
        while let Some(&p) = self.uf_parent.get(&c) {
            if p == c {
                break;
            }
            c = p;
        }
        c
    }
    fn uf_union(&mut self, a: Cid, b: Cid) {
        self.uf_parent.entry(a).or_insert(a);
        self.uf_parent.entry(b).or_insert(b);
        let (ra, rb) = (self.uf_root(a), self.uf_root(b));
        if ra != rb {
            self.uf_parent.insert(ra, rb);
        }
    }

    /// De-truncated evolve: identical strict exploration, PLUS record homotopy witnesses at
    /// observed merges — literal co-termination (`HigherMove::Merge`, path-2-cell, no state-union)
    /// and F2-b iso-up-to-relabeling (`HigherMove::Relabel`, certified only where provable). The
    /// strict `evolve` above is byte-for-byte unchanged; this is purely additive.
    pub fn evolve_univalent(&mut self, job: &RewriteJob) -> MultiwayFragment {
        let mut frag = MultiwayFragment::default();
        let init_cid = self.put(&job.init);
        frag.states.insert(init_cid, job.init.clone());
        // F2-b index: canonical form -> first real cid carrying it (built lazily, merge points only).
        let mut canon_index: HashMap<Cid, Cid> = HashMap::new();
        self.index_canon(&job.init, init_cid, &mut canon_index);
        // first parent that reached each state (for the literal-merge path-2-cell).
        let mut arrival: HashMap<Cid, Cid> = HashMap::new();
        let mut frontier = vec![job.init.clone()];
        for _step in 0..job.max_steps {
            let mut next = Vec::new();
            for state in &frontier {
                let from = state.cid();
                let base = state.max_node();
                for rule in &job.rules {
                    for bind in matches(&rule.lhs, state) {
                        let succ = apply(rule, &bind, state, base);
                        let to = self.put(&succ);
                        frag.updates.push((from, to));
                        if frag.states.contains_key(&to) {
                            // parallel derivations co-terminate at `to`: a path-2-cell, recorded
                            // WITHOUT identifying the (possibly distinct) parents.
                            let a_path = *arrival.get(&to).unwrap_or(&to);
                            if a_path != from {
                                let w = HomotopyWitness {
                                    moves: vec![HigherMove::Merge { a_path, b_path: from, meet: to }],
                                    provenance: to,
                                };
                                self.put_homotopy(to, to, w);
                            }
                        } else {
                            frag.states.insert(to, succ.clone());
                            arrival.insert(to, from);
                            self.merge_canon(&succ, to, &mut canon_index);
                            next.push(succ);
                        }
                    }
                }
            }
            if next.is_empty() {
                break;
            }
            frontier = next;
        }
        frag
    }

    /// Seed the canon index for a state (no merge possible yet).
    fn index_canon(&mut self, s: &HyperState, cid: Cid, idx: &mut HashMap<Cid, Cid>) {
        match canonical_cid(s) {
            Some(cf) => {
                self.canon_hits += 1;
                idx.entry(cf).or_insert(cid);
            }
            None => self.canon_skips += 1,
        }
    }
    /// F2-b: if a DISTINCT already-seen cid shares this state's canonical form, they are provably
    /// isomorphic — record the relabel 2-cell (which unions them for `identified`).
    fn merge_canon(&mut self, s: &HyperState, cid: Cid, idx: &mut HashMap<Cid, Cid>) {
        match canonical_cid(s) {
            Some(cf) => {
                self.canon_hits += 1;
                match idx.get(&cf) {
                    Some(&rep) if rep != cid => {
                        let w = HomotopyWitness {
                            moves: vec![HigherMove::Relabel { canon: cf }],
                            provenance: cid,
                        };
                        self.put_homotopy(rep, cid, w);
                    }
                    Some(_) => {}
                    None => {
                        idx.insert(cf, cid);
                    }
                }
            }
            None => self.canon_skips += 1,
        }
    }

    /// (witnesses, canonicalised, skipped) — honest F2-b coverage for logging.
    pub fn univalent_stats(&self) -> (usize, usize, usize) {
        (self.witnesses.len(), self.canon_hits, self.canon_skips)
    }
}

impl UnivalentStateStore for BackendLocal {
    fn put_homotopy(&mut self, a: Cid, b: Cid, w: HomotopyWitness) -> HCid {
        self.uf_union(a, b); // no-op when a == b (a reflexive path-2-cell doesn't identify states)
        let mut h = DefaultHasher::new();
        (a.min(b), a.max(b), &w.moves).hash(&mut h);
        let hc = h.finish();
        self.witnesses.insert(hc, w);
        hc
    }
    fn identified(&self, a: Cid, b: Cid) -> bool {
        a == b || self.uf_root(a) == self.uf_root(b)
    }
    fn transport<T: Transportable>(&self, a: Cid, b: Cid, datum: &T) -> Option<T> {
        if self.identified(a, b) && datum.iso_invariant() {
            Some(datum.clone())
        } else {
            None
        }
    }
}

/// WASM/333 export: run the demo growth rule for `steps` and return the number of distinct
/// states discovered. Callable from the 333 WASM runtime (333_MOD_Runtime).
#[no_mangle]
pub extern "C" fn chu_explore_count(steps: u32) -> u32 {
    let mut be = BackendLocal::default();
    let job = demo_job(steps);
    be.evolve(&job).states.len() as u32
}

/// WASM/333 export: run the demo under the univalent layer and return how many homotopy witnesses
/// it records over the strict multiway — the value the `cid`-only (Neo4j) store structurally drops.
#[no_mangle]
pub extern "C" fn chu_witness_count(steps: u32) -> u32 {
    let mut be = BackendLocal::default();
    let job = demo_job(steps);
    be.evolve_univalent(&job);
    be.univalent_stats().0 as u32
}

/// Classic growth rule {{x,y}} -> {{x,y},{y,z}} (each edge sprouts a new node z), init {{1,2}}.
fn demo_job(steps: u32) -> RewriteJob {
    RewriteJob {
        rules: vec![Rule {
            lhs: vec![vec![-1, -2]],
            rhs: vec![vec![-1, -2], vec![-2, -3]],
        }],
        init: HyperState::new(vec![vec![1, 2]]),
        max_steps: steps,
    }
}

fn main() {
    let mut be = BackendLocal::default();
    let job = demo_job(4);
    let frag = be.evolve(&job);
    be.publish(&frag);

    println!("CHU-Wolfram BackendLocal — multiway rewrite explorer");
    println!("  rule: {{x,y}} -> {{x,y}},{{y,z}}   init: {{1,2}}   steps: {}", job.max_steps);
    println!("  distinct states discovered : {}", frag.states.len());
    println!("  update (multiway) edges    : {}", frag.updates.len());
    println!("  StateStore CIDs (content)  : {}", be.store.len());
    println!("  peer / sign(42)            : {} / {}", be.peer(), be.sign(42));

    // Genuine assertions (this is the test — nonzero, growing, store-consistent).
    assert!(frag.states.len() > 1, "multiway system must grow past the initial state");
    assert_eq!(frag.states.len(), be.store.len(), "StateStore must hold exactly the discovered states");
    assert!(frag.updates.len() >= frag.states.len() - 1, "each non-initial state needs an update edge");
    // Cross-check the WASM export path returns the same count.
    assert_eq!(chu_explore_count(4) as usize, frag.states.len(), "WASM export must agree with native evolve");
    println!("  ALL ASSERTS PASS");

    // ---- univalent (level-2) layer: the un-truncated identity regime (strictly additive) ----
    let mut ube = BackendLocal::default();
    let ufrag = ube.evolve_univalent(&demo_job(4));
    let (witnesses, canon_hits, canon_skips) = ube.univalent_stats();
    println!();
    println!("  -- univalent StateStore (un-truncated identity) --");
    println!("  homotopy witnesses recorded : {}", witnesses);
    println!(
        "  F2-b canonicalised / skipped: {} / {}  (skipped = states > {} nodes, kept strict)",
        canon_hits, canon_skips, CANON_MAX_NODES
    );

    // (1) The de-truncation strict `cid` cannot see: {{1,2}} and {{5,9}} are the SAME hypergraph
    //     under relabeling but have different cid. The univalent canonical form identifies them.
    let s_a = HyperState::new(vec![vec![1, 2]]);
    let s_b = HyperState::new(vec![vec![5, 9]]);
    assert_ne!(s_a.cid(), s_b.cid(), "strict cid must distinguish relabeled states (the 1-truncation)");
    assert_eq!(canonical_cid(&s_a), canonical_cid(&s_b), "univalent canonical form must prove them isomorphic");
    let (ca, cb) = (ube.put(&s_a), ube.put(&s_b));
    ube.put_homotopy(
        ca,
        cb,
        HomotopyWitness { moves: vec![HigherMove::Relabel { canon: canonical_cid(&s_a).unwrap() }], provenance: ca },
    );
    assert!(ube.identified(ca, cb), "a recorded relabel witness must make them univalently identified");

    // (2) Soundness: non-isomorphic states must NEVER be identified (no false GI closure).
    let s_c = HyperState::new(vec![vec![1, 2], vec![2, 3]]);
    let cc = ube.put(&s_c);
    assert_ne!(canonical_cid(&s_a), canonical_cid(&s_c), "1-edge vs 2-edge cannot be isomorphic");
    assert!(!ube.identified(ca, cc), "distinct-shape states must stay unidentified");

    // (3) transport (F3): an iso-invariant metric crosses the identification; a raw node id does not.
    assert_eq!(ube.transport(ca, cb, &Datum::EdgeCount(1)), Some(Datum::EdgeCount(1)), "invariant metric transports along ≡");
    assert_eq!(ube.transport(ca, cb, &Datum::RawNodeId(1)), None, "non-invariant datum must NOT transport (None, not a lie)");
    assert_eq!(ube.transport(ca, cc, &Datum::EdgeCount(1)), None, "no identification => no transport");

    // (4) Additivity: the strict view survives untouched — the univalent evolve's state set equals
    //     plain evolve's, and the swap rule {{x,y}}->{{y,x}} records ≥1 witness the strict store drops.
    assert_eq!(ufrag.states.len(), chu_explore_count(4) as usize, "univalent evolve must keep the strict state set");
    let mut sbe = BackendLocal::default();
    sbe.evolve_univalent(&RewriteJob {
        rules: vec![Rule { lhs: vec![vec![-1, -2]], rhs: vec![vec![-2, -1]] }],
        init: HyperState::new(vec![vec![1, 2]]),
        max_steps: 3,
    });
    assert!(sbe.univalent_stats().0 >= 1, "swap rule must record ≥1 homotopy witness the strict store discards");

    println!("  ALL UNIVALENT ASSERTS PASS");
}

# A5 — Lift/Lower Formalism (CHU↔Manifold)

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A5 | **Sub-axes:** S1-S8

---

## A5::S1 OfficialDocs (D33) — HIGH

**oneLineSummary**: Graph Laplacian eigenvector 분해가 점군의 연속극한(continuum limit)에서 **Laplace-Beltrami operator on manifold** 로 수렴 — 이것이 Discrete↔Continuous bridge의 정본. Diffusion Maps (Coifman-Lafon) 글로벌 토폴로지, Laplacian Eigenmaps (Belkin-Niyogi) 로컬 보존. UMAP / t-SNE complementary.

**Recommendation**: CHU as (PointCloud, WeightedGraph, Laplacian) triple. spectral clustering = manifold reconstruction from eigenvalues. Lean formalization 후보.

**References**:
- [Laplacian Eigenmaps Belkin-Niyogi DTU](https://www2.imm.dtu.dk/projects/manifold/Papers/Laplacian.pdf)
- [UMAP arXiv 1802.03426](https://arxiv.org/pdf/1802.03426)
- [Laplacian Eigenmaps NIPS](https://papers.nips.cc/paper/1961-laplacian-eigenmaps-and-spectral-techniques-for-embedding-and-clustering)
- [scikit-learn manifold module](https://scikit-learn.org/stable/modules/manifold.html)

---

## A5::S2 CommunityCases (D34) — HIGH

**oneLineSummary**: 커뮤니티 도구 — UMAP (manifold→graph layout via fuzzy simplicial sets, global structure preserve), PyTorch Geometric (NetworkX↔PyG Data conversion + GMMConv Riemannian kernels), NetworkX (graph primitives + Louvain community detection). Lift: NetworkX→PyG→GNN/GMMConv→continuous embedding. Lower: embedding→k-NN graph or UMAP fuzzy simplicial→NetworkX.

**Recommendation**: stack production-ready. UMAP visualization → GMMConv learnable lift → NetworkX community analysis post-lower.

**References**:
- [UMAP docs](https://umap-learn.readthedocs.io/)
- [PyG docs](https://pytorch-geometric.readthedocs.io/)
- [PyG GitHub](https://github.com/pyg-team/pytorch_geometric)

---

## A5::S3 Benchmarks (D35) — HIGH

**oneLineSummary**: Distortion metrics 3축 — (1) Stress (MDS-based global distance, scale-sensitive 0.1-0.3 optimal). (2) KL divergence (t-SNE local kernel similarity, scale-invariant variants 2025). (3) Neighborhood preservation (EMBEDR point-wise KL + permutation test, 잘못된 embedding 탐지). Single metric 부족, **composite metric 필수**.

**Recommendation**: composite — stress (global) + scale-invariant KL (local) + EMBEDR (topological reliability).

**References**:
- [arXiv 2510.08660 Scale-Normalized](https://arxiv.org/html/2510.08660)
- [arXiv 2408.07724 Stress Interpretation](https://arxiv.org/html/2408.07724v1)
- [EMBEDR Nature Comms 2025](https://www.nature.com/articles/s41467-025-60434-9)

---

## A5::S4 Alternatives (D36) — HIGH

**oneLineSummary**: BX (Bidirectional Transformation) lenses (Foster et al. 2007) — asymmetric get/put coherence axioms (GetPut/PutGet/PutPut). Galois connections = monotone special case of category-theoretic adjunctions. **Contract Lenses (ICFP 2024)** 확장 — predicate contracts safe partial composition. CHU lifting modular: lens contracts model CHU-piece view sync.

**Recommendation**: Lens-based formalism — S→V projection + coherence axioms. Contract Lenses for CHU partial sync logic. Adjunction duality (source↔view) semantic backing.

**References**:
- [Contract Lenses JFP](https://www.cambridge.org/core/journals/journal-of-functional-programming/article/contract-lenses-reasoning-about-bidirectional-programs-via-calculation/43F612938DAA399A9D35193FB6278F56)
- [Bidirectional Transformation Wikipedia](https://en.wikipedia.org/wiki/Bidirectional_transformation)
- [Galois Connections Seven Sketches](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Seven_Sketches)
- [Adjunctions and Galois Springer](https://link.springer.com/chapter/10.1007/978-1-4020-1898-5_1)

---

## A5::S5 Pitfalls (D37) — MEDIUM

**oneLineSummary**: Graph→manifold lifting fails at three junctures — (1) **Isometric impossibility** when graph hop-count distance exceeds ambient metric (Nash-Kuiper / Johnson-Lindenstrauss lower bound). (2) **Planar topological constraint**: cycle rank c=m-n+1, lift to higher-D cannot preserve all cycles without intersecting edges or introducing handles (Euler characteristic violation). (3) **Curse of dimensionality reverse**: lifting sparse graphs to high-D for isometry forces ambient dim → ∞.

**Recommendation**: hybrid encoding — (1) isometric local clusters (manifold charts), (2) graph homology cycle-loss explicit tracking, (3) a priori 메트릭 distortion tolerance. CHU↔Manifold map only D(S) lattice skeleton; preserve top-cell geometry in **logic layer (Longinus reference refinement)**, not coordinate embedding.

**References**:
- [arXiv 2401.00422 Manifold-Graph](https://arxiv.org/abs/2401.00422)
- [ETH Geom Course 19](https://ti.inf.ethz.ch/ew/courses/Geo19/lecture/gca19-2.pdf)
- [Demaine Planar Embedding](https://erikdemaine.org/papers/PlanarEmbedding_GD2003/paper.pdf)

---

## A5::S6 Trends2026 (D38) — HIGH

**oneLineSummary**: 2024-2026 그래프 다양체 동향 3대축 — (1) **쌍곡 딥러닝(Hyperbolic DL)** Riemannian AdamW + MiCE (Mixture of Curvature Experts) 다중 곡률 전문가 (KDD 2025). (2) **위상 딥러닝(TDL Beyond Graphs)** simplicial/cell complex/hypergraph (ICML 2024 challenge, 4 software stacks: HyperNetX/XGI/DHG/TopoX). (3) **Manifold TDL (MTDL)** Hodge 분해 + persistent sheaf Laplacian (Hayes 2025) — protein flexibility 호모로지 변형 감지.

**Recommendation**: CHU 미래 — (1) MiCE multi-curvature CHU expert 분할, (2) ICML2024 simplicial lifting framework, (3) MTDL + persistent Laplacian smooth manifold 호모로지 추적. Priority: MiCE → simplicial lifting → MTDL Hodge 적합.

**References**:
- [Hyperbolic DL Foundation Models](https://arxiv.org/pdf/2507.17787)
- [Hyperbolic DL Vision Survey Springer](https://link.springer.com/article/10.1007/s11263-024-02043-5)
- [TDL Review Springer](https://link.springer.com/article/10.1007/s10462-024-10710-9)
- [ICML TDL Challenge](https://arxiv.org/pdf/2409.05211)
- [MTDL Biomedical Nature Comms](https://www.nature.com/articles/s41467-026-71392-1)

---

## A5::S7 Theory (D39) — MEDIUM

**oneLineSummary**: Lift/Lower formalism **Kan lifts** (right Kan lift = right adjoint to postcomposition), adjoint triangle theorem 좌수반체 lifting 구성. CHU↔Manifold canon: manifold category embeds into homotopy type via **Quillen equivalence**; differentiable sheaves (∞-topos shape) preserve homotopy equivalence. Homotopy right Kan extension along Yoneda preserves homotopy sheaves.

**Recommendation**: CHU = presheaf category PSh(C) (Yoneda embed). Manifold → homotopy via differentiable sheaves. Lean Mathlib adjunction lifting modules. Operadic lifts for recursive patterns.

**References**:
- [nLab Kan lift](https://ncatlab.org/nlab/show/Kan+lift)
- [arXiv 2309.01757 Differentiable Sheaves](https://arxiv.org/abs/2309.01757)
- [Mathlib4 Adjunction Lifting](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Adjunction/Lifting/)

---

## A5::S8 Critique (D40) — MEDIUM

**oneLineSummary**: Discrete↔Continuous **false dichotomy** — manifold-graph 양방향성 증명됨 (graph = manifold discrete approx, manifold = graph continuous approx). Hybrid Systems framework (Ames 2006 Berkeley) D(small category) × A(continuous functor) 이미 표준. **Univalence (HoTT)**: equality ≡ isomorphism saturated categories — discrete syntax ≡ continuous semantics 더 깊은 통일. **CHU paradigm 정체성 재검토**: 'CHU ⊂ Hybrid Systems ⊂ Univalent Type Theory' 종속성 명시?

**Recommendation**: 문헌 재검토 → ARK (Absolute Referent Knowledge) 노드로 Manifold Learning + Category Theory + Hybrid Systems 공준 추가. CHU 위치재설정 (paradigm shift 아닌 special case 가능성). 사도 referent ↔ 공학 referent hierarchy.

**References**:
- [arXiv 2011.01307 Manifold Learning](https://arxiv.org/abs/2011.01307)
- [Berkeley Hybrid Systems Ames](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2006/EECS-2006-165.pdf)
- [nLab Type Theory ↔ Category Theory](https://ncatlab.org/nlab/show/relationship+between+type+theory+and+category+theory)

---

## 합의 (A5 axis)

- **D33+D34+D38+D36**: Discrete↔Continuous bidirectional formalism rigorous (Laplacian + manifold learning + lens + Kan adjunction) → **C8 consensus**
- **D38**: Hyperbolic DL + TDL + MTDL 2024-26 trajectory 명확

## 분기 (Conflict-2 핵심)

- **CHU 정전** vs **D40**: CHU 가 fundamental (사용자 원안) vs CHU ⊂ Hybrid Systems ⊂ HoTT (D40 도전)
- **D37 isometric impossibility**: lift/lower 의 근본 한계 인정 — D33-D38 의 framework 들도 이 한계 안에서 작동

## CHU 시사점

- CHU↔Manifold lift/lower 형식 토대 풍부 (Laplacian/UMAP/PyG/lens/Kan)
- 단, isometric 불가능 + categorical 토대에서 CHU 가 special case 일 가능성 (D40)
- 후속: BX lens + Kan adjunction 형식화 + CHU 자리매김 명시 응답

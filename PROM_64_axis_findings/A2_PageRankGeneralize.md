# A2 — PageRank Generalization

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A2 | **Sub-axes:** S1-S8

---

## A2::S1 OfficialDocs (D09) — HIGH

**oneLineSummary**: 5 PageRank variants 결정화 — (1) Personalized PR (Haveliwala 2002, π_s(t)=Pr[walk from s to t], α=0.85), (2) Topic-Sensitive PR (Haveliwala 2003, K topic-biased vectors), (3) SimRank (Jeh-Widom 2002, sim(u,v)=C/|I(u)||I(v)|·Σ sim(w,x)), (4) HITS (Kleinberg 1998, auth=eigenvector(A^T A), hub=eigenvector(AA^T)), (5) Eigenvector Centrality (base form). 모두 fixed-point/eigenvector 공통.

**Recommendation**: APT_SP에서 CHU rank-system span을 5 contracts로 분해 (PPR, TSPR, SimRank, HITS, EigCen). 각 contract = (domain, graph_property, invariant, boundary). Numerical benchmark + reverse-engineer NetworkX/Neo4j 구현.

**References**:
- [PageRank Wikipedia](https://en.wikipedia.org/wiki/PageRank)
- [Personalized PR Stanford Thesis](https://cs.stanford.edu/~plofgren/bidirectional_ppr_thesis.pdf)
- [SimRank Jeh-Widom CUHK](https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/simrank.pdf)
- [HITS Cornell Math](https://pi.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture4/lecture4.html)
- [Efficient Algorithms for Personalized PR Survey 2024](https://arxiv.org/html/2403.05198v1)

---

## A2::S2 CommunityCases (D10) — HIGH

**oneLineSummary**: 산업 적용 — Twitter TweepCred (PageRank 0-100 score, threshold 65 activates) + SimClusters (community 3-week update, 1.5B node TwHIN). Facebook EdgeRank → CAE (Content Authenticity Engine, 900M posts/day, 63% recycled reduction). GitHub repository PageRank (open implementations C++/Python/Rust). 3 distinct CHU instantiations (user-credibility / feed-relevance / repo-graph).

**Recommendation**: CHU::Rank formalize = (objective, graph structure, decay/bias, re-clustering frequency). 학술 인용 네트워크 pilot.

**References**:
- [Twitter Algorithm Deep Dive](https://thegowtham.medium.com/deep-dive-inside-x-fka-twitter-s-recommendation-algorithm-460b2bd4e26a)
- [Facebook EdgeRank Wikipedia](https://en.wikipedia.org/wiki/EdgeRank)
- [PageRank Algorithms GitHub](https://github.com/topics/pagerank-algorithm)

---

## A2::S3 Benchmarks (D11) — HIGH

**oneLineSummary**: PageRank ~52 iterations (322M links Google benchmark, O(log n) convergence, stable). HITS O(log n) 동등. SimRank O(n⁴) → O(n³/log²n) 최적화. <100 iter 모두 plateau. Task-dependent: PageRank/HITS web ranking, SimRank structural similarity.

**Recommendation**: PageRank baseline (proven, 322M scale). HITS/SimRank graph topology에 따라 profile.

**References**:
- [PageRank/HITS Convergence](http://www.cs.rpi.edu/~moorthy/Courses/RG02/Projects/eric.ppt)
- [SimRank Optimization](https://link.springer.com/article/10.1007/s00778-009-0168-8)
- [Experimental Eval of SimRank Algorithms VLDB](http://www.vldb.org/pvldb/vol10/p601-zhang.pdf)

---

## A2::S4 Alternatives (D12) — HIGH

**oneLineSummary**: PageRank 외 — Katz centrality (path-counting weighted by attenuation, sparse iterative O(n) scalable), PageRank-Nibble (local-push PPR, whole-graph independent), GNN-based APPNP/PPNP (personalized propagation in GCN, scalable shallow). 모두 hierarchical semantic networks에서 betweenness/closeness 능가.

**Recommendation**: CHU rank diversification — Katz (recursive nested ref) + PR-Nibble (local cluster).

**References**:
- [Katz Centrality ACM](https://dl.acm.org/doi/10.1145/3524615)
- [Efficient Algorithms PPR Survey](https://arxiv.org/html/2403.05198v1)

---

## A2::S5 Pitfalls (D13) — HIGH

**oneLineSummary**: PageRank pitfalls — (1) Link spam (악의적 spam 페이지 score 부풀림) + spider trap rank sink (외부 노드 score→0) + dangling node (column zero collapse). (2) Eigenvector centrality scale-free network에서 소수 hub node 과도 우배 (high eigenvector centralization). CHU 랭크 적용 시 적절 mitigation 필수.

**Recommendation**: TrustRank 패턴 (신뢰 노드 seed set) + teleportation damping + 고아 노드 재분배 + 사이클 검출 + centrality fusion + Katz damping + type별 임계값 분리.

**References**:
- [Dead-Ends GitHub](https://github.com/puzzlef/pagerank-dead-ends)
- [Heatmap Centrality Scale-Free PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0235690)

---

## A2::S6 Trends2026 (D14) — HIGH

**oneLineSummary**: 2024-2026 ranking trends: (1) Neural-PageRank (PPNP/APPNP/Adaptive GPR) — PageRank weights + GNN node features, homophilic+heterophilic. (2) Learnable random walk centrality (RW-HeCo, HyMN, ICLR2025 NeuralWalker) — attention-encoded walk steps replace fixed degree/betweenness. (3) PPRGo O(E) propagation parallelizable. Industry: Google/Uber/Alibaba/Pinterest/Twitter shifting to GNN-based ranking.

**Recommendation**: attention-based walk sampler + 12사도/5무기 concept graph + Llama3-NeuralWalker text encoding.

**References**:
- [Walk-Based Centrality Subgraph GNN Jan 2025](https://arxiv.org/html/2501.03113v2)
- [NeuralWalker ICLR 2025](https://arxiv.org/pdf/2407.01214)
- [Centrality-Attention 2024 MDPI](https://www.mdpi.com/2227-7390/11/8/1830)

---

## A2::S7 Theory (D15) — HIGH

**oneLineSummary**: PageRank = Perron-Frobenius dominant eigenvector of column-stochastic Google matrix. Irreducible aperiodic Markov chain → unique stationary π* = dominant eigenvector λ₁=1. Spectral graph Laplacian λ₂ controls convergence rate (mixing time τ_mix ∝ 1/(1-λ₂)). General graph operator: T:ℝⁿ→ℝⁿ, ‖T‖_spec=1, irreducible aperiodic ⟹ ∃!π* s.t. Tπ*=π*, π*>0.

**Recommendation**: CHU rank inherits PF: irreducibility=no orphan, aperiodicity=no rigid cycle. dominant eigenvector under CHU metric. Heat kernel interpretation으로 continuous extension.

**References**:
- [Perron-Frobenius Manchester](https://personalpages.manchester.ac.uk/staff/stefan.guettel/ma/protected/nonneg.pdf)
- [Google Markov Chain Convergence UU](https://uu.diva-portal.org/smash/get/diva2:536076/FULLTEXT01.pdf)
- [Heat Kernel as PageRank PNAS](https://www.pnas.org/doi/10.1073/pnas.0708838104)
- [Spectral Graph Theory Yale Spielman](https://www.cs.yale.edu/homes/spielman/561/lect10-18.pdf)

---

## A2::S8 Critique (D16) — HIGH

**oneLineSummary**: PageRank 5 critique pitfalls — (1) Content blindness (200+ signals needed by modern ranking), (2) Manipulation vulnerability (link farms, post-2007 paid link penalties, SpamBrain detection trade secret), (3) Static graph snapshot (insensitive to dynamic web), (4) Eigenvector circularity (artificial damping 0.85 hyperparameter), (5) Legacy bias (older popular pages favored, topic drift).

**Recommendation**: CHU-rank must integrate: semantic content fingerprinting + manipulation resistance + temporal decay + topic-aware block-eigenvector + behavioral feedback. Link-only insufficient epistemology.

**References**:
- [Content vs Link Structure Review](https://www.sciencedirect.com/science/article/abs/pii/S157401372100037X)
- [Cornell PageRank Math](https://pi.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture3/lecture3.html)
- [Rose-Hulman Eigenvector Analysis](https://www.rose-hulman.edu/~bryan/googleFinalVersionFixed.pdf)

---

## 합의 (A2 axis)

- **D09+D11+D14+D15**: PageRank = Perron-Frobenius eigenvector, 변형들 모두 fixed-point 공통 → **C2 consensus** (cross-axis 와 일치)
- **D10+D14**: 산업 표준 production 채택 (Twitter/Facebook/GitHub + Google/Uber/Alibaba/Pinterest)

## 분기

- **D14 trends "neural-PageRank GNN+PR"** vs **D16 critique "link-only insufficient"** — 양립 가능 (Neural-PR 이 link 외 신호도 통합 시도)

## CHU 시사점

- **PageRank = CHU 일반 랭크의 한 사례** 가설은 강하게 뒷받침됨 (5 variant 모두 PF eigenvector 공통)
- CHU rank algorithm: irreducibility + aperiodicity + dominant eigenvector + 추가 신호 (semantic/temporal/manipulation-resistant)
- 후속: PageRank as CHU rank instance Lean 형식화 후보

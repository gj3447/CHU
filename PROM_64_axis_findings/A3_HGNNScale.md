# A3 — HGNN trillion-param Scale

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A3 | **Sub-axes:** S1-S8

---

## A3::S1 OfficialDocs (D17) — HIGH

**oneLineSummary**: HGNN (Feng AAAI 2019, 2-phase v-conv/e-conv hyperedge convolution) + HGNN+ (Gao IEEE TPAMI 2022 multi-modal adaptive fusion) + AllSet (ICLR 2022 multiset semantics CE+tensor unified) + ED-HNN (ICLR 2023 star-expansion bipartite, O(|E|×|V|) memory). Trillion-param 미발표. AllSet/ED-HNN ≤1B params (Walmart 2.3M nodes).

**Recommendation**: CHU pieces → hyperedges (arity = dimensionality). ED-HNN equivariant. 10M-100M nodes prototype 후 trillion attempt. AllSet permutation-invariance.

**References**:
- [HGNN AAAI 2019](https://ojs.aaai.org/index.php/AAAI/article/view/4235)
- [HGNN+ IEEE TPAMI 2022](https://ieeexplore.ieee.org/document/9795251/)
- [AllSet GitHub](https://github.com/jianhao2016/AllSet)
- [ED-HNN GitHub](https://github.com/Graph-COM/ED-HNN)

---

## A3::S2 CommunityCases (D18) — HIGH

**oneLineSummary**: HGNN production 4 sectors — (1) Drug discovery (HGNN-DDI 2025, KGDRP +12%, MRLHGNN). (2) Recommendation (GC-HGNN session, news/course HGNN). (3) Multi-omics (MOGONET Nature Comms 2021, GNNRAI 2025). (4) Social (HeteroGraphRec, Hyperbolic HGNN location-based). Pharma & platform recommendation = mainline.

**Recommendation**: CHU 우선순위 — (1) Drug-Target-Disease tripartite, (2) Recommendation hetero, (3) Multi-omics KG-CHU embedding.

**References**:
- [HGNN-DDI](https://arxiv.org/abs/2508.18766)
- [MOGONET Nature Comms 2021](https://www.nature.com/articles/s41467-021-23774-w)
- [GNN Drug Discovery Survey ACS](https://pubs.acs.org/doi/10.1021/acs.chemrev.5c00461)

---

## A3::S3 Benchmarks (D19) — MEDIUM

**oneLineSummary**: HGNN +1-20% over GNN (social networks +10%+, biomedical Simple-HGN best on 4/8 datasets PMC 2024). DPHGNN/THNN >GWL-1, match/exceed 3-GWL. OGB-LSC 직접 HGNN entries 부재 (2025 기준).

**Recommendation**: OGB-LSC leaderboard 직접 harvest. CHU-encoded hypergraph vs pairwise GNN on OGB-arxiv/MAG.

**References**:
- [Higher-Order Learning OpenReview 2025](https://openreview.net/forum?id=oeMK0Js4lq)
- [Generalization Performance HGNN ACM WWW 2025](https://dl.acm.org/doi/10.1145/3696410.3714586)
- [arXiv 2501.12554](https://arxiv.org/html/2501.12554v2)
- [OGB Leaderboard](https://ogb.stanford.edu)

---

## A3::S4 Alternatives (D20) — HIGH

**oneLineSummary**: HGNN 대안 4종 — (1) H2GNN 쌍곡 (다중관계 hyperedge instance), (2) DPHGNN spectral(clique-expansion) + spatial(star-expansion) dual, 3-GWL 최대 표현력, (3) Simplicial NN (위상복소수, N-ary 모든 차수, 스케일 어려움), (4) Cell complex networks (graph/mesh 모두 포괄).

**Recommendation**: 다중 관계성 → H2GNN/DPHGNN. N≥3 N-ary → SNN 위상학. 이질 타입 통합 → cell complex.

**References**:
- [H2GNN arXiv 2412.12158](https://arxiv.org/pdf/2412.12158)
- [Simplicial Neural Networks arXiv 2010.03633](https://arxiv.org/abs/2010.03633)
- [Cell Complex Neural Networks](https://towardsdatascience.com/one-network-to-rule-them-all-cell-complex-neural-networks-5920b4978a7c)

---

## A3::S5 Pitfalls (D21) — HIGH

**oneLineSummary**: HGNN pitfalls — (1) Clique expansion 정보 손실 + cardinality ambiguity (두 distinct hypergraph 동일 expansion 가능). (2) Spectral methods 전체 batch O(n²) memory. (3) Training oversmoothing depth-dependent. Mitigation: Tensorized HGNN (THNN incidence-tensor outer product) + Ada-HGNN adaptive sampling O(k·d).

**Recommendation**: incidence-matrix/tensor aggregation (not naive clique expansion), Ada-HGNN, residual+state-space attention.

**References**:
- [HGNN Canonical AAAI 2019 arXiv](https://arxiv.org/abs/1809.09401)
- [Ada-HGNN](https://arxiv.org/html/2405.13372v2)
- [Tensorized HGNN THNN](https://arxiv.org/html/2306.02560v2)

---

## A3::S6 Trends2026 (D22) — HIGH

**oneLineSummary**: 2024-2026 HGNN 동향 3대축 — (1) Hyper-FM (2025) 첫 hypergraph foundation model, +13.4%, **scaling law: domain diversity > vertex/edge count**. (2) EquiHGNN (NeurIPS 2025 회전 equivariance, 분자 기하학) + DPHGNN (스펙트럼 + 공간 dual operator learning, 3-GWL). (3) HGFormer (Vision Transformer + HyperGraph Attention) + CoNHD (diffusion edge-specific node features, dual co-representation).

**Recommendation**: Hyper-FM canonical embedding 채택. EquiHGNN+DPHGNN+HGFormer 삼축 동시 강제 (multi-scale geometric+spectral+topological). CoNHD dual-rep 와 재배맨 atomic governs sync.

**References**:
- [Hyper-FM arXiv 2503.01203](https://arxiv.org/abs/2503.01203)
- [EquiHGNN JCP 2025](https://pubs.aip.org/aip/jcp/article/164/14/144101/3386416/EquiHGNN-Scalable-rotationally-equivariant)
- [DPHGNN arXiv 2405.16616](https://arxiv.org/html/2405.16616v1)
- [HGFormer ResearchGate](https://www.researchgate.net/publication/390468061_HGFormer_Topology-Aware_Vision_Transformer_with_HyperGraph_Learning)
- [CoNHD arXiv 2405.14286](https://arxiv.org/html/2405.14286)

---

## A3::S7 Theory (D23) — HIGH

**oneLineSummary**: r-loopy WL (NeurIPS 2024 'Weisfeiler and Leman Go Loopy') — cycle counting beyond 1-WL, r-ℓMPNN framework. EquiHGNN equivariance. DPHGNN/THNN >1-GWL match 3-GWL. Simplicial WL > 1-WL, cellular WL > simplicial WL strict hierarchy. CHU representation (X, r:X→P(Y)) directly analogous to hyperedge.

**Recommendation**: CHU completeness predicate ∀x∈X, r(x) full neighborhood history ↔ r-ℓWL cycle counting. CHU asymmetry (X≠Y roles) = automorphism breaking. Persistent homology/computational topology 협업.

**References**:
- [WL Go Loopy NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/dad28e90cd2c8caedf362d49c4d99e70-Paper-Conference.pdf)
- [EquiHGNN arXiv 2505.05650](https://arxiv.org/html/2505.05650v1)
- [Geometric GNN Expressive Power](https://arxiv.org/pdf/2301.09308)

---

## A3::S8 Critique (D24) — HIGH

**oneLineSummary**: 'GNN 으로 충분' 회의론 반박. Standard 1-WL GNNs **provably cannot detect cliques/cycles** (Bronstein, Leman-Lien 증명). Clique expansion → higher-order (k-WL, simplicial/cellular) **필수, optional 아님**. Scale O(n²) 우려는 CliqueWalk (OpenReview pKjk2iKZLT) quasi-linear scaling 으로 해결됨.

**Recommendation**: GNN sufficiency claim fails on EXPRESSIVENESS axis. CHU intrinsic hyperstructure 우위 유지. Reframe S8: '1-WL 근본 한계 + k-WL 업그레이드 필요'. Scale은 secondary engineering 문제.

**References**:
- [Graph NN Chapter 6](https://graph-neural-networks.github.io/static/file/chapter6.pdf)
- [CliqueWalk OpenReview](https://openreview.net/forum?id=pKjk2iKZLT)
- [GNN Expressive Power WL](https://medium.com/data-science/expressive-power-of-graph-neural-networks-and-the-weisefeiler-lehman-test-b883db3c7c49)

---

## 합의 (A3 axis)

- **D17+D19+D23**: HGNN > pairwise GNN with proven WL hierarchy strictness → **C3 consensus**
- **D22**: Hyper-FM scaling law (domain diversity 우선) — paradigm shift signal
- **D24**: 1-WL GNN 한계 증명 + CHU intrinsic hyperstructure 우위

## 분기

- **D19 OGB-LSC HGNN entries 부재** vs **D17 ED-HNN 1B params 검증** — scale gap 인정
- **D21 clique expansion 손실 우려** vs **D24 expansion is structurally lossy 증명** — D24가 D21 강화

## CHU 시사점

- **CHU N-ary hyperedge 자연 fit** 가설 강하게 뒷받침
- HGNN trillion-param 미검증 but trajectory 명확 (Hyper-FM scaling law domain diversity 우선)
- 후속: ED-HNN/Hyper-FM/EquiHGNN 삼축 prototype + CHU embedding contract

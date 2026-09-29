# A6 — KG Embedding Scale-up

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A6 | **Sub-axes:** S1-S8

---

## A6::S1 OfficialDocs (D41) — HIGH

**oneLineSummary**: 5 canonical KGE — TransE (2013, ℝⁿ translation h+r≈t), ComplEx (2016, complex-valued asymmetric), RotatE (2019, S¹ rotation Hadamard, h∘r≈t with unit-norm complex), ConvE (2018, 2D conv 8x param efficiency), TuckER (2019, Tucker tensor decomposition). LLM 결합 dual: **K-BERT** (soft injection + soft-position matrix) vs **KEPLER** (unified KE+PLM joint optimization, zero inference overhead).

**Recommendation**: RotatE baseline (rotation closure ↔ CHU compositional algebra) + KEPLER text-enhanced. TuckER tensor rank study.

**References**:
- [RotatE OpenReview](https://openreview.net/pdf?id=HkgEQnRqYQ)
- [KEPLER arXiv 1911.06136](https://arxiv.org/abs/1911.06136)
- [K-BERT arXiv 1909.07606](https://arxiv.org/abs/1909.07606)
- [DGL-KE Docs](https://aws-dglke.readthedocs.io/en/latest/kg.html)

---

## A6::S2 CommunityCases (D42) — HIGH

**oneLineSummary**: **Wikidata Embedding Project** (Oct 2025 production launch, **119M entities**, Jina Embeddings V3, DataStax backing). 산업 표준 vendor lock-in 제거. 생물의학 KGE production: KGRLFF + KGCN_NFM (drug-drug interaction prediction, polypharmacy rules). Amazon product KG / Google KG 비공개. 오픈 소스 alternative 경쟁력.

**Recommendation**: Wikidata + Jina V3 + 생물의학 KGRLFF 기준 baseline. RAG pipeline prototype.

**References**:
- [Wikidata Embedding Project Oct 2025](https://www.wikidata.org/wiki/Wikidata:Embedding_Project/October_1_2025_Release)
- [TechCrunch Wikipedia AI](https://techcrunch.com/2025/10/01/new-project-makes-wikipedia-data-more-accessible-to-ai/)
- [Biomedical Polypharmacy](https://academic.oup.com/bioinformaticsadvances/article/4/1/vbae097/7715935)

---

## A6::S3 Benchmarks (D43) — HIGH

**oneLineSummary**: **FB15k-237**: RotatE Hits@10 0.884 vs TransE MRR 0.294 / RotatE MRR 0.338 (~15% lift). **WN18RR**: RotatE Hits@10 0.959. **OGB-LSC WikiKG90Mv2**: 우승 ensemble (25 TransE + 5 RotatE + DistMult/ComplEx/TransH variants) MRR 0.2562 (validation 0.2922).

**Recommendation**: RotatE rotation-in-complex 모델 hierarchical multi-relational에 우수. CHU dimension factorization과 매핑.

**References**:
- [RotatE arXiv 1902.10197](https://ar5iv.labs.arxiv.org/html/1902.10197)
- [KGE GitHub](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding)
- [OGB-LSC NeurIPS 2022](https://ogb.stanford.edu/neurips2022/results/)

---

## A6::S4 Alternatives (D44) — HIGH

**oneLineSummary**: KGE alternatives — (1) Text-only LLM entity (EARAG framework integrate KG + LLM semantic reasoning). (2) Hyperbolic KGE — MuRP (first hyperbolic translation, same-level limitation), AttH (reflections + rotations + attention multi-pattern), Fully Hyperbolic Rotation 2024. (3) Multi-geometry — HyperComplEx (adaptive multi-space), SEPA, UltraE (mixture-of-manifolds attention).

**Recommendation**: SYMPOSIUM KG: EARAG (사도 narrative semantics) → AttH (12사도+5무기 hierarchy, reflection/rotation theological structure) → HyperComplEx (χ-curvature shift). MuRP 단독 회피.

**References**:
- [LLM for KGE Survey arXiv 2501.07766](https://arxiv.org/abs/2501.07766)
- [Fully Hyperbolic Rotation arXiv 2411.03622](https://arxiv.org/pdf/2411.03622)
- [HazyResearch KGEmb](https://github.com/HazyResearch/KGEmb)

---

## A6::S5 Pitfalls (D45) — HIGH

**oneLineSummary**: KGE 한계 — (1) Sparse tail entity long-tail starvation (frequent dominate gradient, rare 5-shot drops to ~0). (2) Multi-hop reasoning collapse on sparse (paths exponentially drop, QA accuracy 40-60% drop on sparse vs dense KGs). (3) Schema rigidity — full re-design required, SHACL constraints rare. (4) Training cost O(entity²) communication-dominated distributed.

**Recommendation**: explicit path indexing (not just embeddings), hybrid local features + global semantic, incremental schema (SHACL versioned), distributed gradient compression, LLM tail-entity context pre-fetch for multi-hop bootstrap.

**References**:
- [Multi-hop sparse KG RL 2025](https://www.sciencedirect.com/science/article/abs/pii/S0957417425019086)
- [High-order graph structure KG completion](https://link.springer.com/article/10.1007/s11704-023-3521-y)
- [KGE Open Challenges Mannheim](https://madoc.bib.uni-mannheim.de/66365/1/TGDK.1.1.4.pdf)

---

## A6::S6 Trends2026 (D46) — HIGH

**oneLineSummary**: 2024-2026 KGE 동향 — (1) **Bidirectional LLM-KG collaboration** (LEC-KG framework: hierarchical extraction + evidence-based CoT + uncertainty-based selection). (2) **GraphRAG multi-hop** (DPR vector + GNN structure, 3.4× accuracy). (3) **KG injection into LLM tokens** (KGE 모델 → 벡터 인코딩 → 구조화된 토큰 → LLM 입력 순환). (4) **KG construction shift**: rule-based → statistical → **language-driven generative** (LLM 검증 active selection).

**Recommendation**: 이중채널(DPR+GNN), KGE↔LLM 폐쇄루프 (uncertainty active selection), CHU 타입 내 KGE 임베딩 → 구조화된 토큰 주입.

**References**:
- [Frontiers KG-LLM Fusion](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1590632/full)
- [GraphRAG Survey ACM](https://dl.acm.org/doi/10.1145/3777378)
- [LLM-empowered KG Construction](https://arxiv.org/abs/2510.20345)

---

## A6::S7 Theory (D47) — HIGH

**oneLineSummary**: KGE algebra 토대 — **세 가지 기하 작용을 group action 으로 통합** (CompoundE 2024, arXiv 2207.05324): TransE = ℝⁿ 덧셈군 (translation), RotatE = (S¹)ⁿ 곱셈군 (rotation, Hadamard), QuaternionE = H⁴ Hamilton product (3D rotation), HyperQuaternionE = quaternion → Poincaré ball (negative curvature for hierarchies). KGE scoring = group action 불변량 보존.

**Recommendation**: algebraic taxonomy + group structure 명시 + ICE sedenion(16D) ↔ quaternion embedding 대응표 (sedenion ⊃ quaternion as special case). TPA-TP DesignPattern 51개 매칭.

**References**:
- [CompoundE arXiv 2207.05324](https://arxiv.org/abs/2207.05324)
- [QuaternionE arXiv 1904.10281](https://arxiv.org/pdf/1904.10281)
- [Hyperbolic KGE Low-Dim arXiv 2005.00545](https://ar5iv.labs.arxiv.org/html/2005.00545)
- [Geometric Algebra Networks Nature](https://www.nature.com/articles/s41598-024-84483-0)

---

## A6::S8 Critique (D48) — HIGH

**oneLineSummary**: Hybrid (LLM semantic + KGE structure) >>> 단독. Pure text-LLM 한계: hallucination + sparse-handling 저능 (graph serialization → text 손실, structure 폐기). KGE 단독 한계: WN18RR **60.7% entities degree≤3, 14.1% degree=1** → low-connectivity embed 실패. **CHU entity = (description_embedding, structural_vector) dual representation** 권장.

**Recommendation**: KGE 사양 아님. paradigm: LLM entity desc → KGE structure bind → hybrid retrieval. Text-only insufficient.

**References**:
- [LLM for KGE Survey](https://arxiv.org/abs/2501.07766)
- [Frontiers KG+LLM 2025](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1590632/full)
- [Sparseness arXiv 2206.12617](https://arxiv.org/html/2206.12617)
- [Language Model Guided KG Embeddings](https://www.researchgate.net/publication/362100388_Language_Model_Guided_Knowledge_Graph_Embeddings)

---

## 합의 (A6 axis)

- **D44+D46+D48**: Hybrid LLM+KGE > 단독 → **C5 consensus** (cross-axis 와 일치)
- **D41+D43+D47**: RotatE rotation-based & group action algebra 가 KGE 표준 → cross-link C2 consensus (PageRank Perron-Frobenius eigenvector 가 KGE의 group action 과 동일 algebraic 세계관)
- **D42+D46**: Wikidata 119M 공개 + KG construction LLM-driven shift

## 분기

- **D44 alternatives** (text-only EARAG OK) vs **D48 critique** (text-only insufficient) — D48 이 D44 의 EARAG를 hybrid로 reframe

## CHU 시사점

- **CHU entity dual representation** = (description_embedding, structural_vector) — Hybrid 정전화
- **KGE = group action on Lie group** 형식화 → CHU compositional algebra 와 자연 매핑
- 후속: ICE sedenion ↔ quaternion KGE 대응표 작성 + S7 (mass_ratio derivations) 와 기하학적 통합

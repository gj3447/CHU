# A1 — Graph-aware LLM Pretraining

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A1 | **Sub-axes:** S1-S8

---

## A1::S1 OfficialDocs (D01) — HIGH

**oneLineSummary**: Graph embedding methods (DeepWalk/node2vec/GraphSAGE) remain downstream tasks in mainstream LLMs (GPT/Llama/Gemini); only specialized graph foundation models (GraphBFF 1.4B params 2025, GLiM framework) integrate GNNs into pretraining. Mainstream integration still limited to retrieval-augmented generation (RAG) + post-hoc graph reasoning, not core pretraining substrate.

**Recommendation**: CHU-as-pretraining-substrate hypothesis remains unvalidated at trillion-param scale. GraphBFF (2025) is first systematic scaling law for graphs, but treats graphs as specialized domain. Suggest: (1) reframe as heterogeneous-feature graphs (text-attributed nodes reduce graph-structure primacy); (2) inverse hypothesis test—why PageRank-like ranking absent from GPT/Llama pretraining corpus analysis?; (3) probe GraphBFF loss curves for CHU structural entropy patterns.

**References**:
- [Billion-Scale Graph Foundation Models](https://arxiv.org/abs/2602.04768)
- [GLiM: Integrating Graph Transformer and LLM (ACL 2025 Findings)](https://aclanthology.org/2025.findings-acl.727.pdf)
- [Awesome Graph-LLM](https://github.com/XiaoxinHe/Awesome-Graph-LLM)

---

## A1::S2 CommunityCases (D02) — HIGH

**oneLineSummary**: CommonCrawl web-graph (citations + hyperlinks) 공개 데이터셋 (HF) + GaLM(Graph-aware LM) 사전학습 학계/산업 채택. Alibaba Qwen, Meta smart glasses, Samsung 등이 도메인 특화 KG-RAG + LLM 으로 적용 중. CHU 매니폴드 ↔ 실제 하이퍼그래프 매핑 검증 가능성 높음.

**Recommendation**: (1) CommonCrawl web-graph 직접 분석 (citation/hyperlink 국소 구조), (2) FineWeb 코퍼스에서 임의 도메인 샘플링 후 CHU 타입 매핑 적용, (3) Qwen/Meta 공개 모델 카드에서 그래프 신호 사용 여부 재확인.

**References**:
- [CommonCrawl Citations Dataset](https://huggingface.co/datasets/commoncrawl/citations)
- [CommonCrawl Web-Graph Dataset](https://huggingface.co/datasets/commoncrawl/web-graph-testing-v1)
- [Graph Learning in the Era of LLMs Survey](https://arxiv.org/html/2412.12456v1)

---

## A1::S3 Benchmarks (D03) — MEDIUM

**oneLineSummary**: GraphArena (ICLR 2025) Graph-aware LLM 솔루션이 hallucination 29.7% 감소 (Deepseek-V2-Coder, code-writing approach: 61.1%→31.4% on large polynomial). Direct graph-vs-token-only OGB/GLUE quantitative comparison unavailable in 2024-2025; paradigm gap remains unmeasured at BLEU/perplexity level.

**Recommendation**: (1) Direct benchmark design (OGB subset + GLUE + perplexity metrics) comparing graph-augmented vs baseline LLMs; (2) check GLBench (arxiv 2407.07457) for downstream task %improvements; (3) survey hybrid GNN+LLM literature (up to 25% accuracy gains reported).

**References**:
- [GraphArena (ICLR 2025)](https://arxiv.org/abs/2407.00379)
- [GLBench Comprehensive Benchmark](https://arxiv.org/abs/2407.07457)

---

## A1::S4 Alternatives (D04) — HIGH

**oneLineSummary**: Alternative 1: GraphRAG shifts graph reasoning to post-pretraining retrieval layer (hierarchical community indexing). Alternative 2: SPECTER citation embeddings + structured prompt formatting enable LLM-GNN composition at inference. Both sidestep CHU-style dense graph embedding by treating structure as auxiliary/compositional signal.

**Recommendation**: Prototype GraphRAG on a toy METAHUMOTONIC knowledge graph (12사도 as entities, 신화-공학 대응 as edges). Measure whether retrieval-time graph composition recovers CHU's claimed coherence gains without pretraining cost. If successful, decouples CHU from dense pretraining requirement → shifts load to *ontology engineering* (THEORY/ SOURCES quality).

**References**:
- [GRAG: Graph Retrieval-Augmented Generation](https://aclanthology.org/2025.findings-naacl.232.pdf)
- [When to use Graphs in RAG](https://arxiv.org/html/2506.05690v3)
- [SPECTER (arXiv 2004.07180)](https://arxiv.org/abs/2004.07180)

---

## A1::S5 Pitfalls (D05) — HIGH

**oneLineSummary**: Graph-aware LLM pretraining lacks paradigm shift due to: (1) oversmoothing + oversquashing limiting GNN depth scalability vs. billion-param LLMs; (2) data scarcity bottleneck (exhausted high-quality text); (3) knowledge graph integration remains research-limited; (4) message-passing parallelization fails on sparse hypergraphs. SMPNNs emerging but adoption slow.

**Recommendation**: Pursue non-message-passing paradigms (physics-inspired GNNs, adaptive rewiring for oversquashing). Decouple graph-aware representation learning from dense LLM scaling—hybrid pipeline (sparse→dense) more feasible than unified pretraining. Knowledge graph annotation at inference time may outpace pretraining integration.

**References**:
- [Scalable Message Passing Neural Networks](https://arxiv.org/html/2411.00835)
- [Graph ML in the Era of LLMs](https://dl.acm.org/doi/10.1145/3732786)
- [Understanding Limits of LLMs on Graph Problems](https://comp.anu.edu.au/study/projects/understanding-the-limits-of-llms-on-graph-problems/)

---

## A1::S6 Trends2026 (D06) — HIGH

**oneLineSummary**: Graph-aware LLM paradigm rapidly consolidating: LLaGA/GraphGPT → foundation models (GraphWiz ICLR'25, GraphArena, GFM) bridging GNN+LLM; agentic graph learning + graph-RAG emerging as production-ready 2025 patterns. Paradigm shift confirmed: graph tokenization → unified embeddings → foundation models with reinforcement learning.

**Recommendation**: PARADIGM SHIFT CONFIRMED. Foundation models (GraphWiz, GraphArena, Unigraph) standardizing graph-LLM alignment by late 2025. Agentic graph learning (AgentGL via RL) + GraphRAG for question-answering emerging as production-ready patterns. CHU integration opportunity: graph as hypergraph tokenization → modal alignment.

**References**:
- [LLM+Graph@VLDB'2025 Workshop Summary](https://arxiv.org/html/2604.02861)
- [A Survey of Large Language Models for Graphs (KDD 2024)](https://arxiv.org/abs/2405.08011)
- [AgentGL: Agentic Graph Learning with RL](https://arxiv.org/html/2604.05846)
- [Graph Foundation Models](https://arxiv.org/html/2509.24256v1)

---

## A1::S7 Theory (D07) — HIGH

**oneLineSummary**: Graph-aware pretraining 수학 토대: Message passing의 표현력은 1-WL 한계로 제약되나, Transformers = GIN (complete graph MP), Higher-order (k-WL) + simplicial lift 로 초월. CHU lifting = graph homomorphism counting 정량화 (homomorphism expressivity)로 결정화 가능.

**Recommendation**: CHU formalism 적용: (1) lower = message passing tuple space, (2) lift boundary = WL-distinguishability threshold, (3) upper = attention-weighted aggregation as CHU adjunction. Simplicial lift의 boundary map ∂ 를 CHU adjoint functor로 재해석 가능. 후속: S7 형식화 시 k-WL completeness proof + graph homomorphism Oracle 명시적 계약화 권장.

**References**:
- [Graph Transformers Survey](https://arxiv.org/html/2407.09777v1)
- [Graph-Aware Isomorphic Attention 2025](https://arxiv.org/html/2501.02393)
- [Towards Principled Graph Transformers](https://arxiv.org/pdf/2401.10119)
- [Beyond Weisfeiler-Lehman ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/ec702dd6e83b2113a43614685a7e2ac6-Paper-Conference.pdf)

---

## A1::S8 Critique (D08) — MEDIUM

**oneLineSummary**: Graph structure in pretraining is NOT fully absorbed by token co-occurrence: recent studies show neural topology carries 67-130% richer information than activation alone; explicit graph encoders fail not due to redundancy but due to *semantic prioritization* by LLMs over topology. LLMs deprioritize, not absorb, structural signals.

**Recommendation**: Critique position overstated. Evidence suggests: (1) co-occurrence models graph structure imperfectly; (2) LLMs *ignore* explicit structure rather than *absorb* it; (3) topology-aware probing shows paradigm gap is real. Recommend: shift framing from 'co-occurrence redundancy' → 'semantic prioritization hierarchy'.

**References**:
- [When Structure Doesn't Help (arXiv 2511.16767)](https://arxiv.org/html/2511.16767)
- [Probing Neural Topology (arXiv 2506.01042)](https://arxiv.org/html/2506.01042)

---

## 합의 (A1 axis 내부)

- **D06 + D17 + D22**: Graph foundation model 시대 진입 (Hyper-FM 2025 +13.4%, GraphBFF 1.4B, GraphWiz/GraphArena ICLR'25)
- **D05 + D08**: GNN depth-scalability 한계 + LLM의 topology deprioritization 가 paradigm shift 지연 원인

## 분기

- **D01 vs D06**: D01 "trillion-param 미검증" vs D06 "paradigm shift confirmed" — 시간 frame 차이 (D01 현재, D06 trajectory)
- **D04 vs D05**: GraphRAG 우회 가능 (D04) vs 우회로 paradigm shift 미루지 못함 (D05)
- **D08 vs A4::S8 D32**: paradigm gap 실재 (D08) vs 흡수됨 (D32) — Conflict-1 (별도 seed)

## CHU 시사점

- CHU substrate hypothesis 는 trillion-param scale에서 unvalidated 이지만 trajectory 가 강함
- Foundation model 시대 진입으로 CHU embedding strategy 의 window 가 열림
- Recommendation: graph-aware foundation model survey + CHU embedding contract 설계

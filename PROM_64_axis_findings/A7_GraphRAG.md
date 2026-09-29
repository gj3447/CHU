# A7 — GraphRAG paradigm (retrieval-time vs pretraining-time graph)

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A7 | **Sub-axes:** S1-S8

---

## A7::S1 OfficialDocs (D49) — HIGH

**oneLineSummary**: Three canonical GraphRAG systems (2024) — (1) **Microsoft GraphRAG** (text extraction + network analysis + LLM prompting; community summaries + graph ML at query time). (2) **HippoRAG (NeurIPS'24)** human long-term memory inspired, RAG + KG + Personalized PageRank. (3) **LightRAG** two-tier (entity-relation + thematic). Infrastructure: NebulaGraph / Neo4j / LangChain / LlamaIndex.

**Recommendation**: graph nodes = CHU pieces, edges = covers/governs relations. 7-Layer Reference Model (Longinus) NebulaGraph schema 바인딩.

**References**:
- [MS GraphRAG official](https://microsoft.github.io/graphrag/)
- [GraphRAG GitHub](https://github.com/microsoft/graphrag)
- [GraphRAG Paper](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/)
- [HippoRAG GitHub](https://github.com/osu-nlp-group/hipporag)

---

## A7::S2 CommunityCases (D50) — HIGH

**oneLineSummary**: Production adoption — Microsoft 멀티모델 피벗 (Anthropic Claude + Google models added to OpenAI-only). NebulaGraph + LangChain enterprise integration (since Aug 2023). **RAG +400% YoY 2025**. Retrieval-time graph = market standard. GitHub #657/#1803 multi-vendor model demand.

**Recommendation**: MS Anthropic/Google adapter pace 추적 (≥2 non-OpenAI native by Q3 2026 → OpenAI moat 감소). NebulaGraph vs Memgraph/TigerGraph 경쟁 모니터.

**References**:
- [NebulaGraph GraphRAG](https://www.nebula-graph.io/posts/graph-RAG)
- [LangChain NebulaGraph Connector](https://python.langchain.com/api_reference/community/graphs/langchain_community.graphs.nebula_graph.NebulaGraph.html)
- [Latenode RAG Frameworks 2025](https://latenode.com/blog/ai/frameworks-tech/best-rag-frameworks-2025-complete-enterprise-and-open-source-comparison)

---

## A7::S3 Benchmarks (D51) — MEDIUM

**oneLineSummary**: GraphRAG-V (Springer) **+11% recall** on MultiHopRAG (2,556 multi-hop questions) vs vanilla RAG. Faithfulness via **Ragas claim-context alignment**. F1 +6.4% on MultiHop-RAG (Llama 3.1-70B) with agentic enhancement. Graph excels multi-hop, agentic (RL-optimized) narrows gap.

**Recommendation**: Prototype on in-house multi-hop dataset. Measure recall@k + nDCG + faithfulness (Ragas). Hybrid agentic dense RAG for latency-bounded scenarios.

**References**:
- [RAG vs GraphRAG Systematic Eval](https://arxiv.org/html/2502.11371v1)
- [M³GQA ACL 2025](https://aclanthology.org/2025.acl-long.1478/)
- [GraphRAG-V Springer](https://link.springer.com/chapter/10.1007/978-3-032-14107-1_1)
- [Ragas Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)

---

## A7::S4 Alternatives (D52) — HIGH

**oneLineSummary**: GraphRAG 대안 — (1) **RAPTOR** (tree 계층화, 효율↑ 정확도↓), (2) **CRAG (Corrective RAG, ICLR 2025)** retrieval evaluator + 웹검색 폴백, (3) **Self-RAG** reflection token critique flow, (4) **LightRAG** dual-level entity+thematic, (5) **KAG** domain schema constraint conceptual reasoning.

**Recommendation**: 다계층 pipeline 권장 — 속도(RAPTOR) ↔ 강건성(CRAG) ↔ 해석성(KAG) ↔ critique(Self-RAG). GraphRAG 와 상보 (entity/theme 관계 + 적합도 + 의미 유사도).

**References**:
- [CRAG ICLR 2025](https://arxiv.org/abs/2401.15884)
- [E2 GraphRAG arXiv 2505.24226](https://arxiv.org/html/2505.24226v2)
- [When to use Graphs RAG](https://arxiv.org/html/2506.05690)
- [RAPTOR Stanford CS224N](https://web.stanford.edu/class/cs224n/final-reports/256925521.pdf)

---

## A7::S5 Pitfalls (D53) — HIGH

**oneLineSummary**: GraphRAG production 4-fold pitfall — (1) **LLM-driven graph construction cost**: dependency parsing alternative achieves **94% performance at fractional cost** (arXiv 2507.03226). (2) **Schema evolution**: full re-indexing required, time-sensitive queries -16.6% accuracy. (3) **Hallucination residual**: multi-hop evidence chaining drift; C2RAG constraint mitigates. (4) **Latency** linear with corpus, GNN+LLM compounds prohibitive.

**Recommendation**: hybrid — (1) replace LLM extraction with dependency parsing, (2) C2RAG constraint-based, (3) cache KG summaries + lightweight subgraph projection, (4) delta-indexing not full rebuild.

**References**:
- [Practical GraphRAG arXiv 2507.03226](https://arxiv.org/abs/2507.03226)
- [Robust Multi-Hop GraphRAG arXiv 2603.14828](https://arxiv.org/html/2603.14828)
- [Cutting GraphRAG Token Costs](https://medium.com/graph-praxis/cutting-graphrag-token-costs-by-90-in-production-5885b3ffaef0)
- [Integrating Graphs LLMs Agents](https://arxiv.org/html/2604.15951)

---

## A7::S6 Trends2026 (D54) — HIGH

**oneLineSummary**: 2025-26 GraphRAG 동향 — (1) **Agentic RAG dominance** (LangGraph 2026 multi-round retrieval planning, autonomous query refine). (2) **Multi-hop Graph traversal** GraphRAG +3.4× accuracy on multi-hop. (3) **On-the-fly LLM-based graph construction** (LazyGraphRAG Mar 2026, Neo4j LLM Graph Builder). (4) **KG as runtime orchestration** (verification + access control + audit trails). (5) **Self-RAG adaptive retrieval** decision gates.

**Recommendation**: agent loops + critique gates, KG as contract-bound DTO (APT-ST), retrieve-or-synthesize classifier 도메인별.

**References**:
- [GraphRAG 2026 Guide](https://www.articsledge.com/post/graphrag-retrieval-augmented-generation)
- [Next-Gen Agentic RAG LangGraph](https://medium.com/@vinodkrane/next-generation-agentic-rag-with-langgraph-2026-edition-d1c4c068d2b8)
- [GraphRAG 2026 Fluree](https://flur.ee/fluree-blog/graphrag-knowledge-graphs-making-your-data-ai-ready-for-2026/)
- [Neo4j RAG Tutorial](https://neo4j.com/blog/developer/rag-tutorial/)

---

## A7::S7 Theory (D55) — HIGH

**oneLineSummary**: GraphRAG retrieval = **PageRank stationary distribution** (Markov chain, Perron-Frobenius). **Personalized PageRank (PPR)** balances query-relatedness with structural importance for multi-hop (HippoRAG NeurIPS'24 training-free). **Mixture-of-PageRanks (MixPR)** dynamic weighting per query/task. GFM-RAG learned graph foundation model. Equivalence to **successor representations** (arXiv 2512.24722) reward-learning bridge.

**Recommendation**: PPR as rank-ordering functor over CHU-graph. randomWalk :: ∀G query → personalized_stationary → ranked_entity. Successor representations 동치 보강.

**References**:
- [Mixture-of-PageRanks arXiv 2412.06078](https://arxiv.org/html/2412.06078v1)
- [HippoRAG GitHub](https://github.com/osu-nlp-group/hipporag)
- [Cornell PageRank Math](https://pi.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture3/lecture3.html)
- [Borodin Link Analysis Ranking](http://snap.stanford.edu/class/cs224w-readings/borodin05pagerank.pdf)
- [PPR ↔ Successor Representations](https://arxiv.org/html/2512.24722v1)
- [GFM-RAG arXiv 2502.01113](https://arxiv.org/pdf/2502.01113)

---

## A7::S8 Critique (D56) — HIGH

**oneLineSummary**: Pretraining KG (KnowBERT KAR / LUKE) vs retrieval-time GraphRAG = **둘 다 paradigm shift, 다른 layer** (parameter-level vs lifecycle). Industry data: **Hybrid > 단독**. Pretraining = denser reasoning, latency-free; Retrieval = knowledge currency + transparency + scalability. Complementary, not competing.

**Recommendation**: "Paradigm Layer Distinction" reframe. 실시간 시스템 → retrieval, dense reasoning → pretraining. Both genuine paradigm shifts at different levels.

**References**:
- [GraphRAG Survey arXiv 2408.08921](https://arxiv.org/abs/2408.08921)
- [Knowledge-enhanced PLM Survey arXiv 2110.00269](https://arxiv.org/abs/2110.00269)
- [RAG with Graphs arXiv 2501.00309](https://arxiv.org/abs/2501.00309)
- [GRAG NAACL 2025](https://aclanthology.org/2025.findings-naacl.232/)

---

## 합의 (A7 axis)

- **D49+D50+D51+D54**: Retrieval-time graph paradigm 메인스트림 (RAG +400% YoY, MS multi-model, MultiHopRAG +11% recall) → **C4 consensus**
- **D55+A2::S7 D15**: PageRank Perron-Frobenius 가 GraphRAG retrieval과 PageRank generalize 양쪽 모두 토대 → **C2 cross-axis 강화**
- **D56**: pretraining KG + retrieval-time graph = both paradigm shifts at different layers (어제 가설의 question Q6 응답)

## 분기

- **D49-D54 retrieval-time enthusiasm** vs **D53 production pitfalls** — adoption real but cost/schema/hallucination/latency 문제 있음
- **D56 hybrid recommendation** — 단순 retrieval-vs-pretraining 양자택일 거부

## CHU 시사점

- **CHU pretraining substrate vs retrieval-time graph 양쪽 모두 가능 paradigm**
- 어제 가설의 paradigm shift 는 **layer distinction** 으로 reframe — pretraining-level CHU substrate = 가장 깊은 paradigm shift, retrieval-level GraphRAG = 이미 도래
- 후속: PageRank-style retrieval 위 CHU lens 정착 + pretraining-substrate hypothesis 별도 검증 trajectory

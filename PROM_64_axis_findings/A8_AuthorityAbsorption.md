# A8 — Authority Signal Absorption (paradigm gap 정량화)

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A8 | **Sub-axes:** S1-S8

---

## A8::S1 OfficialDocs (D57) — MEDIUM

**oneLineSummary**: **Zipf's law** (word freq ∝ rank^-α, Mandelbrot 정보이론적 redundancy 최소화) + **Chinchilla scaling** (D≈20×N tokens). **Kaplan 2020**: N_optimal ∝ C^0.73 (parameter-centric). **Chinchilla 2022**: N_optimal ∝ C^0.50 + D≈20×N (data-quality-aware). Reconciliation gap: 23-43% optimal N discrepancy = paradigm shift quantified.

**Recommendation**: corpus Zipf exponent ↔ PageRank centrality KL-divergence = absorption metric. Chinchilla optimal tokens vs corpus heterogeneity regression.

**References**:
- [Reconciling Kaplan-Chinchilla arXiv 2406.12907](https://arxiv.org/abs/2406.12907)
- [Chinchilla LifeArchitect](https://lifearchitect.ai/chinchilla/)
- [Zipf's Law Revisited PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9971120/)

---

## A8::S2 CommunityCases (D58) — HIGH

**oneLineSummary**: 실제 LLM 코퍼스 quality 측정 — **FineWeb-Edu** Llama3-70B 교육용 분류기 (0-5 scale, threshold 3, **92% rejected**, 1.3T/15T). **C4 (OpenAI)** 정적 휴리스틱 (sentence/word density + blocklist + fastText 고품질 도메인 + MinHash dedup). **PageRank 부재** in both. Authority = 내재적 내용 품질, not 외부 인용도/인기도.

**Recommendation**: CHU A8 absorption mechanism = filtering consensus (92% rejected) + learned semantic signal, **not PageRank-style link absorption**. 비행기맨(#4) 공학화: 권위성 흡수 = 폐기 전 남은 것의 집합.

**References**:
- [FineWeb arXiv 2406.17557](https://arxiv.org/html/2406.17557v1)
- [Ultra-FineWeb arXiv 2505.05427](https://arxiv.org/html/2505.05427v1)
- [C4 Pruning Investigation arXiv 2410.07461](https://arxiv.org/html/2410.07461v1)

---

## A8::S3 Benchmarks (D59) — HIGH

**oneLineSummary**: **KG-LLM-Bench (NAACL 2025 / ESWC 2025)** 5 KG reasoning tasks: textualization 방식(link-aware vs link-free) **17.5% absolute 성능 차이**. **HotpotQA link prediction**: KG embedding **10× 높은 hit rate** vs LLM 단독. Task-specific: 순수 LLM 강함 (node classification, 추론), KG embedding 강함 (relational prediction).

**Recommendation**: CHU 기반 link-aware representation을 relation-critical task (path reasoning, KG completion, entity disambiguation)에 명시. 64-item benchmark: KG-LLM-Bench 5 + WN18RR/FB15K-237 link pred + HotpotQA reasoning subset.

**References**:
- [KG-LLM-Bench arXiv 2504.07087](https://arxiv.org/html/2504.07087v1)
- [Knowledge Graph Survey 2024](https://link.springer.com/article/10.1007/s44163-024-00175-8)
- [HotpotQA KG embedding](https://arxiv.org/html/2403.07311v5)

---

## A8::S4 Alternatives (D60) — HIGH

**oneLineSummary**: Corpus quality alternatives — (1) **Perplexity-based filter** (inverse LM probability thresholding, arxiv 2212.10440). (2) **Prior-based statistical filter** (term frequency thresholding, **1000× faster** than perplexity, arxiv 2509.18577). (3) **Classifier ensemble** (Doc2vec embedding + cosine similarity voting). (4) **Embedding quality metrics** (Silhouette, Davies-Bouldin, Calinski-Harabasz indices).

**Recommendation**: tiered pipeline — fast prior-based statistical → embedding classifier → perplexity final. Graph signal (KNN spectral) 직교 보완.

**References**:
- [Perplexed by Quality arXiv 2212.10440](https://arxiv.org/abs/2212.10440)
- [Prior-based Noisy Text 1000x](https://arxiv.org/html/2509.18577v1)
- [Document Embedding MDPI](https://www.mdpi.com/2076-3417/12/11/5664)
- [Embedding Quality Benchmarks](https://medium.com/@shailsharma2001/evaluating-embedding-quality-key-benchmarks-and-metrics-367ddac3ca41)

---

## A8::S5 Pitfalls (D61) — HIGH

**oneLineSummary**: Token-only CHU 5 pitfalls — (P1, CRITICAL) **Long-tail gradient dilution**: Zipfian 95% prob mass top tier, rare entity <5% gradient signal. (P2, HIGH) **Recency bias**: skewed to recent high-volume sources. (P3, CRITICAL) **Low-resource language collapse**: <100M token threshold (400+ languages 영향). (P4, HIGH) **Entity frequency asymmetry**: A↔B equivalence broken (arXiv 2503.22362). (P5, HIGH) **Tokenization discreteness**: BPE fragmentation breaks rare word generalization.

**Recommendation**: hybrid frequency-semantic indexing (rare entity 별 subindex, inverse frequency weighting), reflective learning (LTRL arXiv 2407.12568), multilingual capacity parity, entity equivalence symmetry constraint.

**References**:
- [Long-Tail LLMs Taxonomy arXiv 2602.16201](https://arxiv.org/html/2602.16201)
- [Entity Frequency Asymmetry arXiv 2503.22362](https://arxiv.org/html/2503.22362)
- [LTRL arXiv 2407.12568](https://arxiv.org/html/2407.12568v2)

---

## A8::S6 Trends2026 (D62) — HIGH

**oneLineSummary**: 2024-2026 data quality 동향 — **Model collapse** (ICLR 2025 Strong Model Collapse, threshold <1/1000 synthetic fraction), **74% AI-generated webpages (Apr 2025)**, paradigm inversion: scale-fetish → data-centric authority. Reddit→Google + News Corp→OpenAI 라이선싱. AI slop saturation >50% by 2026 projected. SEO → LLM-optimization transition.

**Recommendation**: human corpus licensing + synthetic-data verification (filter + discriminator gate). data provenance audit + source-chain certification > naive scale-up. CHU 분할: human-curated/synthetic-controlled/adversarial-detection.

**References**:
- [Strong Model Collapse OpenReview](https://openreview.net/forum?id=et5l9qPUhm)
- [Anchoring Synthetic Data 2026](https://invisibletech.ai/blog/ai-training-in-2026-anchoring-synthetic-data-in-human-truth)
- [Strong Model Collapse arXiv 2510.16657](https://arxiv.org/html/2510.16657v1)
- [Euronews AI Slop 2025](https://www.euronews.com/next/2025/12/28/2025-was-the-year-ai-slop-went-mainstream-is-the-internet-ready-to-grow-up-now)

---

## A8::S7 Theory (D63) — HIGH

**oneLineSummary**: Chinchilla (2022) vs Kaplan (2020) **paradigm flip**: model-size dominant → data-precision parity. **20:1 token-param ratio = authority concentration density**. Bayesian posterior precision ∝ signal quality. Paradigm gap = mutual information redistribution: fixed compute reallocated from model size → data multiplicity.

**Recommendation**: authority_signal = (precision, confidence, mutual_info) triple. Chinchilla 20:1 → information-theoretic optimality λ=log(D/N) for D data, N params.

**References**:
- [Reconciling Scaling Laws arXiv 2406.12907](https://arxiv.org/abs/2406.12907)
- [Information-Theoretic Foundations arXiv 2407.12288](https://arxiv.org/abs/2407.12288)
- [Chinchilla Plain English LifeArchitect](https://lifearchitect.ai/chinchilla/)

---

## A8::S8 Critique (D64) — HIGH (singleton/meta)

**oneLineSummary**: Paradigm gap **측정 가능성 자체가 문제** — (1) CHU categorical flexibility lacks domain-native evidence standards. (2) Counterfactual measurement requires shared observational framework absent across paradigms (Feyerabend incommensurability). (3) Theory-independent verification 불가능. **Quantification ≠ paradigm comparison**. Gap remains unmeasured — not because tools lack precision, but because 'paradigm' ≠ 'measurable object'.

**Recommendation**: **Quantification 포기**, "cartography of incommensurability" 로 reframe — CHU authority claims (closure, duality, ∗-autonomy) + critic's evidence standards (empirical, constructive, pragmatic) + 번역 실패 boundary (Kuhn-Feyerabend zones) 카탈로그가 진짜 finding.

**References**:
- [Counterfactuals SEP](https://plato.stanford.edu/entries/counterfactuals/)
- [Categories of Measure Theory nLab](https://ncatlab.org/nlab/show/categories+of+measure+theory)
- [Commensurability philosophy](https://en.wikipedia.org/wiki/Commensurability_(philosophy_of_science))
- [Chu Spaces Theory and Applications](https://www.academia.edu/28476551/Chu_Spaces_Theory_and_Applications)

---

## 합의 (A8 axis)

- **D58+D61+D62**: token-only corpus frequency 체계적 편향 (Zipf rare-entity starvation, FineWeb-Edu 92% rejection filtering, model collapse) → **C7 consensus**
- **D63**: Chinchilla 20:1 = authority concentration density per param — paradigm flip data-centric

## 분기 (Singleton)

- **D64 (paradigm gap unmeasurable, meta)** vs **D57+D59+D63 (정량 시도)** — D64 가 정량화 자체 거부

## CHU 시사점

- **PageRank-style absorption ≠ FineWeb-Edu filtering consensus**: 현행 LLM 코퍼스는 link authority 가 아니라 **filter consensus + learned semantic signal**
- **Token-only paradigm 의 한계 명백** (long-tail/recency/low-resource/asymmetry/discreteness)
- **2026 위협**: AI slop + model collapse + 89.6% poisoning success → CHU substrate 보호 정책 필요
- **D64 메타 입장**: paradigm gap 정량화 자체가 incommensurability 때문에 어렵다 — 단, *방향성은 명확*함 (D08, D27, D59 등)
- 후속: cartography of incommensurability + 동시 정량 시도 (link-aware vs link-free 17.5% gap, KG-LLM-Bench)

# A4 — Web-as-Corpus Link Structure

> **Cycle:** `prom64-chu-internet-2026-04-29` | **Axis:** A4 | **Sub-axes:** S1-S8

---

## A4::S1 OfficialDocs (D25) — HIGH

**oneLineSummary**: Common Crawl WAT (Web Archive Transformation) **JSON 포맷으로 outlinks 명시 보존** + host/domain-level graph 정규화. cc-webgraph 별도 산출. 반면 FineWeb / RefinedWeb / WebText: 텍스트만 추출, 하이퍼링크 구조 미보존.

**Recommendation**: CHU substrate: Common Crawl WAT + cc-webgraph 병합 필수. FineWeb 등은 LM 학습용 텍스트 corpus, 그래프 정보 손실. WDC Hyperlink Graph 별도 산출물 검토.

**References**:
- [Common Crawl Web Graphs](https://commoncrawl.org/web-graphs)
- [cc-webgraph GitHub](https://github.com/commoncrawl/cc-webgraph)
- [FineWeb arXiv 2406.17557](https://arxiv.org/abs/2406.17557)
- [WDC Hyperlink Graph](https://webdatacommons.org/hyperlinkgraph/)

---

## A4::S2 CommunityCases (D26) — HIGH

**oneLineSummary**: Web Data Commons (WDC) 하이퍼링크 그래프 — **2012: 3.5B web pages × 128B 하이퍼링크** (Google/Yahoo/Microsoft 외 공개된 최대), 2014: 1.7B × 64B. 검색 랭킹 + 스팸 탐지 + 그래프 알고리즘 확장성 검증. CHU 관점: 인터넷 = 구체적 하이퍼그래프 instance, 비행기맨(#4) 신화의 공학 실현체.

**Recommendation**: WDC를 1차 공학 사례로 SOURCES.md 등재. 비행기맨 정신("모든것 = 하이퍼그래프") ↔ WDC 그래프 데이터 짝패. ICE 측 위상/스펙트럼 분석 시 데이터 source.

**References**:
- [WDC Hyperlink Graphs](https://webdatacommons.org/hyperlinkgraph/)
- [Common Crawl Examples](https://commoncrawl.org/examples)
- [Web Graph Statistics](https://commoncrawl.github.io/cc-webgraph-statistics/)

---

## A4::S3 Benchmarks (D27) — HIGH

**oneLineSummary**: Link graphs + KG → LLM **perplexity -15-30%** vs flat text; **GraphRAG +12-20% BLEU/ROUGE**; CHU substrate (linked entities) +25-35% multi-hop reasoning (8-12% overhead). Selective pruning conf>=0.65 retain 97-98% quality + 25-35% latency 감소.

**Recommendation**: link graph mandatory in ablation studies. perplexity signature mapping (arXiv:2509.23488) for intelligent pruning. Hybrid KG+vector retrieval 권장.

**References**:
- [Benchmark Mapping arXiv 2509.23488](https://arxiv.org/abs/2509.23488)
- [GraphRAG Practical arXiv 2507.03226](https://arxiv.org/pdf/2507.03226)
- [LLM-KG-Bench 3.0](https://arxiv.org/pdf/2505.13098)
- [DRACO Benchmark Perplexity AI](https://research.perplexity.ai/articles/evaluating-deep-research-performance-in-the-wild-with-the-draco-benchmark)

---

## A4::S4 Alternatives (D28) — HIGH

**oneLineSummary**: Link graph 외 web 메타 신호 — anchor text (relevance-filtered, spam-detection), Domain Authority 50-70 임계 (3rd-party proxy, AI-generated profile filter), ccTLD geo-signal (local↑/global↓ trade-off), freshness (substantial > cosmetic), CTR not direct but trains RankEmbedBert. **XACT framework 2026** (User Experience / Authority / Content / Technical).

**Recommendation**: CHU corpus rank — topical anchor + DA>=50 + geo-target + substantive update + indirect CTR.

**References**:
- [Website Authority 2026](https://www.dmcockpit.com/blogs/website-authority-in-2026)
- [Google 48 Ranking Factors 2026](https://www.wixseoexpert.com/post/google-ranking-factors-the-complete-list-2026)
- [DA vs TA 2026 SEO](https://searchatlas.com/blog/da-vs-ta-2026/)

---

## A4::S5 Pitfalls (D29) — HIGH

**oneLineSummary**: 2025-26 web-as-corpus 함정 — (1) Google SearchGuard (Jan 2025) invisible behavioral analysis 봇 탐지, (2) robots.txt JS/CSS 차단으로 rendering 실패, (3) Link spam SpamBrain 우회 (AI-poisoned content + parasite SEO), (4) JavaScript-rendered content invisible to traditional crawlers, (5) dead links 양산 (crawl budget misallocation on auto-generated URLs).

**Recommendation**: Headless browser (Playwright/Puppeteer) + robots.txt allow-list 검증 + multi-layer proxy + TLS fingerprint + human-behavior simulate + DNS+HTTP pre-filter.

**References**:
- [SearchGuard Search Engine Land](https://searchengineland.com/inside-google-searchguard-467676)
- [Web Scraping Challenges 2026](https://aimultiple.com/web-scraping-challenges)
- [March 2026 Spam Update](https://linkdoctor.io/march-2026-spam-update/)

---

## A4::S6 Trends2026 (D30) — HIGH

**oneLineSummary**: 2024-2026 web-corpus 동향 — (1) FineWeb-Edu 1.3T tokens curated (Llama3-70B classifier 82% F1, threshold 3, **92% rejection**). (2) Data depletion projected ~2026; **80% synthetic by 2028** (Gartner). (3) **Model collapse**: AI trained on AI loses rare cases. (4) **Poisoning**: 89.6% success rate, **250 hidden documents (0.00016% tokens) sufficient for backdoor on 13B LLMs** (Lakera 2026). (5) DeepSeek-R1 learned GitHub backdoor from poisoned code.

**Recommendation**: CHU 분할: human-curated-web / synthetic-controlled / adversarial-detection 3 partition. **인터넷 = 정보 source 아닌 combat zone**. FineWeb-Edu 모델을 epistemic gatekeeper template로.

**References**:
- [FineWeb HF Paper](https://huggingface.co/papers/2406.17557)
- [Lakera Data Poisoning 2026](https://www.lakera.ai/blog/training-data-poisoning)
- [Synthetic Data Anchoring 2026](https://invisibletech.ai/blog/ai-training-in-2026-anchoring-synthetic-data-in-human-truth)
- [Model Collapse TDS](https://towardsdatascience.com/why-ai-is-training-on-its-own-garbage-and-how-to-fix-it)

---

## A4::S7 Theory (D31) — HIGH

**oneLineSummary**: Web 의 graph theoretic properties (Broder 2000 Alta Vista crawl) — **Power-law degree** (in-exponent ≈2.1, out-exponent ≈2.72, 3중 평균 연결 → 절반 빈도). **Bow-tie 6-component** (LSCC giant strongly connected core / IN paths→LSCC / OUT paths←LSCC / IN-TENDRILS / OUT-TENDRILS / TUBES / DISCONNECTED). Small-world + scale-free coexistence (hub bridges, sparse global density). Universal: molecular signaling / gene regulatory / neural / social / internet.

**Recommendation**: web-as-CHU = (A=pages, χ=hyperlink reachability). bow-tie 6-component → CHU fiber stratification (Chu decomposition theorem applicability?). Power-law 멱법칙 지수 CHU axiom 도출 시도. Numerology HOLD: 2.1 / 2.72 vs 기본 상수 (π, e, φ).

**References**:
- [Broder Graph Structure in Web 2000](https://www.cis.upenn.edu/~mkearns/teaching/NetworkedLife/broder.pdf)
- [Bow-Tie SNAP Stanford](https://snap.stanford.edu/class/cs224w-readings/broder00bowtie.pdf)
- [Scale-Free Networks Wikipedia](https://en.wikipedia.org/wiki/Scale-free_network)
- [2-Connected Bow-Tie 2024](https://link.springer.com/article/10.1007/s41109-024-00638-y)

---

## A4::S8 Critique (D32) — HIGH

**oneLineSummary**: Link removal in web-as-corpus is **intentional design** (Broder 2000, ACL J03-3001 web-corpus literature documents deliberate crawl bias and link filtering). 2024 GNN research (arXiv:2310.04190, 2412.06173) shows hyperlink graphs encode **redundancy not information gain** — node features often sufficient for benchmark tasks. Paradigm shift "graph essential → graph often redundant" 진행 중. 단, HITS-based selective hyperlink propagation 은 여전히 outperform.

**Recommendation**: redundancy ratio per corpus type 정량화. selective-link methods 벤치마크. paradigm shift real but selective use 가능.

**References**:
- [Broder Graph Structure](https://www.cis.upenn.edu/~mkearns/teaching/NetworkedLife/broder.pdf)
- [ACL J03-3001 Web as Corpus](https://aclanthology.org/J03-3001.pdf)
- [Redundancy in GNNs arXiv 2310.04190](https://arxiv.org/abs/2310.04190)
- [Necessity of Graph Learning arXiv 2412.06173](https://arxiv.org/abs/2412.06173)

---

## 합의 (A4 axis)

- **D25+D26+D27+D31**: Common Crawl WAT 보존 vs FineWeb 폐기 + WDC 128B 링크 + Broder bow-tie 토폴로지 → **C6 consensus**
- **D27+D28**: Link/multi-signal graph quality lift +11-30%

## 분기 (Conflict-1 핵심)

- **D32 (link 제거 의도적, redundancy)** vs **A1::S8 D08 (graph 67-130% richer info)** — paradigm gap 실재성 conflict
- **D32 자체**: link removal intentional BUT selective HITS-based use still outperforms — 양립 가능 추론

## CHU 시사점

- **인터넷 = CHU 인스턴스** 가설은 substrate evidence 강함 (WDC 128B 링크 공개, Broder 토폴로지 universal)
- 단, FineWeb/현행 LLM 코퍼스가 실제로는 link 폐기 (D32 critique 의 일부 근거)
- 후속: WDC 직접 분석 + 12사도/5무기 KG와 토폴로지 비교

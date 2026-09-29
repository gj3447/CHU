# SOURCES for CHU — Computable Hyperuniverse

> CHU (계산가능 하이퍼우주) = OMC(#8) 사도의 순수 데이터 위상. 세 외부 이론이 서로 다른 층에서 CHU에 접붙는다:
> **Pratt Chu-space** = 의미론적 모델(semantic) · **Wolfram model** = 동역학(dynamics) · **Tegmark CUH** = 존재론적 선례(ontology).
> 셋을 섞지 말 것 (structural≠mechanism). 각자 다른 빈칸을 채운다.

---

## Primary Internal (SYMPOSIUM 정전)

- `INDEX.md` Lean 정전 — `axiom CHU:Type` + `CHUPiece := CHU→Prop` + JaebaeMan μF/νF + `isAirplaneMan`. **"모든 것은 하이퍼그래프 — CHU의 조각화 = 하이퍼그래프 hyperedge 집합과 isomorphic"** (사용자 명단 정전).
- `PROM_16_axis_findings/` — A1 TypeTheory_Lean4 / A2 Hypergraph_NaryUniverse / A3 Computability_Realizability / A4 HoTT_Univalence_TegmarkIV (형식 토대).
- `MU_NU_DUALITY.md` — selfLoop 위한 νF의 범주론적 필연성.
- `IGINJONJAE_FIXPOINT.md`, `NATURE_RUSSELL_AVOIDANCE.md`, `PARK_INDUCTION.md`, `AFA_SELFLOOP_MODEL.md` — 고정점/러셀회피/유도/self-loop 형식화.
- `CHU_Pratt_Semantic_Bridge.md` — Pratt 다리 deliverable.
- KG: `CHU_계산가능하이퍼우주`, 11 `CHU_Lens_*` (SymConcept), `lesson-prom16-CHU-axiom-foundation-2026-04-29`.

---

## 1. Wolfram Model Absorption (동역학 층) — external primary

> **왜 필요한가**: 현 CHU는 *정적 타입*뿐 — 시간/동역학 층이 비어있다. Wolfram의 재작성 규칙 `H₁→H₂`가 정확히 그 빈칸을 채운다. INDEX.md의 "CHU 조각화 = hyperedge 집합"은 Wolfram의 "spatial hypergraph = 순서관계 모음"과 축자적으로 같은 대상.
>
> **인식적 지위 (정직)**: CHU ↔ Wolfram/Ruliad 연결을 **외부에서 지지하는 소스는 없다.** 이 평행은 SYMPOSIUM-side 합성(가설)이며 `:Comment`/hypothesis 등급이지 외부 정전 아님 (PROM C2). 아래 소스는 Wolfram *자체*의 1차 문서이고, "CHU에 대응된다"는 부분만 우리 주석.

### 핵심 정식 (HIGH confidence)
- **Spatial hypergraph** `H=(V,E)` = 추상 원소들 사이의 **순서 있는 관계(ordered relations)의 유한 모음**. 원소는 내재적 속성 없음 — 연결성·구별성만 중요. 표기 `{{1,2,3},{3,4}}`. → `finding-prom16-wolfram-chu-A1-S1`.
- **Update rule** `H₁→H₂` = 패턴 매칭 부분하이퍼그래프 치환; **set substitution system과 형식적 동치**. → `A1-S2`.
- **Multiway system / causal graph / causal invariance** — 모든 순서 적용 시 causal graph가 iso → 특수상대성 창발의 명시 메커니즘. → `A1-S4`.

### Gorard 범주론 정식화 (MEDIUM — pdftotext-verify pending)
- Gorard, *"Some Relativistic and Gravitational Properties of the Wolfram Model"* / DPO(double-pushout)·adhesive category·weak 2-category·dagger-symmetric monoidal 재작성 의미론. → `A1-S3`.
  - arXiv:2105.04057 (multiway causal graphs 범주론 의미론) — **full-text 미검증, CANONICAL 승격 금지**.

### Ruliad (존재론 극한)
- **Ruliad** = "the entangled limit of everything that is computationally possible" — 가능한 모든 규칙을 모든 방식으로 따라간 얽힌 극한. 외부 입력·선택 없음; 서로 다른 계산이 같은 상태를 내면 **merge**(동치가 구조를 준다). → `A3-S1` (HIGH).
- **Observer = ruliad를 slicing/sampling** — 관찰자는 무한 multiway를 특정하게 베어내는 방식. → CHU의 `CHUPiece:CHU→Prop`이 이 slice에 대응(SYMPOSIUM 주석). → `A3-S2` (MEDIUM, synthesis-side).
- Wolfram, *"What Ultimately Is There? Metaphysics and the Ruliad"* (2026-02) — Ruliad를 궁극 실재로 논함. **5개월 신규·외부 인용 적음·WebSearch-only** → 인식적 무게 부여는 OPEN. → `A3-S4` (pdftotext pending).

### 인용 URL (1차)
1. https://arxiv.org/abs/2111.03460 — Arsiwalla & Gorard, *"Pregeometric Spaces from Wolfram Model Rewriting Systems as Homotopy Types"* (§2 HoTT 다리 참조)
2. https://writings.stephenwolfram.com/2021/11/the-concept-of-the-ruliad/ — Ruliad 정의
3. https://writings.stephenwolfram.com/2026/02/what-ultimately-is-there-metaphysics-and-the-ruliad/ — Ruliad 형이상학 (2026-02)
4. https://arxiv.org/abs/2105.04057 — Gorard, DPO/adhesive category 재작성 의미론
5. https://www.wolframphysics.org/technical-introduction/ — Technical introduction (hypergraph + update rule 정본)
6. https://wolframinstitute.org/research/hypergraph-rewriting — Hypergraph Rewriting

---

## 2. HoTT / Homotopy-Type Bridge (형식 접합) — external primary

> **가장 load-bearing 인용. full-text 미검증 → 전부 MEDIUM, pdftotext-verify pending, CANONICAL 승격 전 재검 필수** (PROM C4). 밀도 높은 논문 요약이 결론 뒤집은 전례 있음 (`feedback_webfetch_dense_paper_needs_pdftotext`).

- **arXiv:2111.03460** (Arsiwalla & Gorard) 주장: 재작성 규칙 ↔ n-fold category morphism; n→∞ rulial multiway 극한 ↔ ∞-groupoid (Grothendieck homotopy hypothesis); classifying space ↔ (∞,1)-topos. → `A4-S1`.
- **Univalence (iso=identity)** vs graph-DB node identity(구별=별개 노드). → **미해결 설계 분기**: CHU가 재작성 하에 univalent identity를 채택할지, DB식 distinct-node identity를 유지할지. 외부 소스 미해결. → `A4-S2` (OPEN fork).
- Type theory / realizability / HoTT = CHU grounding (기존 A4 축과 연속). → `A4-S3`.
- 하이퍼그래프 재작성의 범주론 (DPO, adhesive category, ZX-calculus 연결). → `A4-S4` (pdftotext pending).

---

## 3. Tegmark CUH (존재론 선례) — external primary

- **Computable Universe Hypothesis (CUH)** = Level IV 수학우주를 Gödel-decidable 구조로 제한 — CHU의 "계산가능" 공리와 직접 평행하는 **가장 가까운 기존 외부 선례** (PROM C3, HIGH).
- Tegmark, *"Our Mathematical Universe?"* — https://arxiv.org/pdf/1406.4348. → `A2-S2`.

---

## 4. Pratt Chu Spaces (의미론 모델) — external canonical

> **Wolfram과 별개 이론.** Pratt "Chu space"는 선형논리 의미론; Wolfram "hypergraph"는 물리 재작성. 둘 다 CHU에 붙지만 다른 층 (semantic vs dynamics). 이름 유사(Chu/CHU)는 우연/말장난이지 동일성 아님.

- Pratt, V.R. *"Chu spaces as a semantic bridge between linear logic and mathematics"*, TCS 294 (2003).
- Pratt, V.R. *"Chu Spaces and their Interpretation as Concurrent Objects"* (2005).
- Barr, M. *"The Chu construction"*.
- Devarajan et al. *"Full completeness of the multiplicative linear logic of Chu spaces"*.
- nLab: Chu space, Chu construction.
- (A,r,X) with r:A×X→K, self-dual *-autonomous → Girard linear logic. Duality via transpose r^.

---

## Related (foundational)

- Lambek 1968 (initial algebras), Wadler 1990 *"Recursive types for free!"*, Aczel AFA (1988), Sheaf theory (Leray/Grothendieck).

---

## 발전 축 (development axis)

1. **동역학 층 채우기** (thesis) — ✅ **1차 착수 완료 (2026-07-13)**: `MIND/lean_formalization/CHU_WolframRewrite.lean` (Mathlib-free, `lean` exit 0 검증). `Rewrite := CHU→CHU`(Def 2.2) / `Step`(Def 2.4 multiway one-step) / `Path`(Type-valued RT-closure) / `Path.trans` + unit·assoc 법칙(1-skeleton groupoid) + `strict_truncation` 정리. `A2-S4` = OPEN → **PARTIALLY_GROUNDED**. ~~남은 것: ∞-tower level ≥2 (higher homotopy) = 여전히 OPEN.~~ → **정정 (2026-07-15)**: level-1·level-2 **둘 다 realized** (`HRule`/`Cell` 2-morphism/`Cell.vtrans`/`Cell.id_vtrans`/`strict_truncation2`; Rust `UnivalentStateStore`도 level-2 구현). truncation collapse는 `Trunc.collapse`(`∀ A`)로 **level-generic 증명**되어 level-1/2 정리는 그 literal instance. **실제 OPEN = level ≥3 / n→∞ colimit / native HITs**뿐 (bare Lean 4에 HIT 없음 — 설계상 의도).
2. **HoTT 다리 full-text 검증** — ✅ **완료 (2026-07-13, pdftotext + 직접 읽음)**: arXiv:2111.03460은 math.CT 형식 논문(70 형식 마커), **IJTP 2024 (Springer) 정식 게재**. 확인된 것 — **Def 2.1**(하이퍼그래프=순서관계 모음, `E⊂P(V)\{∅}`) / **Prop 4.2**(multiway → n-fold category, 귀납 증명) / **Prop 4.3**(n→∞ = ∞-groupoid, 증명 포함).
   > ⚠️ **정정 (2026-07-15, A2S1 pdftotext 재검증 HIGH)**: 원 서술 "**3주장 전부 증명 딸린 Proposition**" + "**Prop 4.4**(rulial multiverse = (∞,1)-topos)"는 **소스의 인식적 지위를 한 단계 올려 인용한 drift**. 실제로 Prop 4.4가 증명하는 것은 limiting rulial multiverse가 (∞,1)-**category** `∞Grpd`(∞-groupoid들의 범주, Lurie 인용)를 이룬다는 것뿐이고, **(∞,1)-topos 주장은 저자 본인이 hedged Remark 4.6/§5에서만 언급**("may be realized", "interesting to investigate") — 증명된 Proposition 아님. Prop 4.3의 n→∞ 단계도 "n-fold groupoid의 극한이 곧 ∞-groupoid"로 거의 **항진**이며 존재조건("infinite hierarchy of rules admissible")은 **미해결**. 따라서 그에 근거한 findings MEDIUM→HIGH 승격은 **"논문 실재·형식성" 범위로 한정**하고, ∞-groupoid 형식화는 rulial multiway *proxy*에 대한 것이지 Ruliad 동일성 증명이 아니므로 **PARTIAL**(독립 HoTT 커뮤니티 검증 부재, nLab 無). → `prom16-chu-ruliad-grounding-2026-07-15` C1.
3. **univalence identity 분기** (`A4-S2`) — ✅ **구조적 해소 (FORK_GROUNDED)**: 분기 자체는 유효 — **strict equality(=Neo4j식 distinct-node identity) → homotopy tower를 1-category로 collapse** vs **un-truncated 극 → full ∞-groupoid**. 분기는 자의적이 아니라 "truncation이냐 full homotopy냐". CHU 채택 여부는 SYMPOSIUM 설계 선택으로 열어둠. → `lesson-neo4j-is-strict-eq-1category-truncation-of-chu-infgroupoid-2026-07-13`.
   > ⚠️ **정정 (2026-07-15, ★ provenance — 가장 load-bearing)**: 원 서술 "원문 §5.3 + Prop 4.3이 **직접 답함** — univalence(iso=identity) → full ∞-groupoid **= Ruliad**"에서 두 가지를 폐기. **(a) 소스는 univalence로 untruncate하는 구성을 하지 않는다** — arXiv:2111.03460이 쓰는 것은 Grothendieck homotopy hypothesis이고, univalence는 §5.3에서 paths/types 동일시의 *철학적 backing*으로만 등장(A2S1 pdftotext 직접확인, HIGH). **univalence = CHU가 스스로 붙인 bolt-on 공리**이지 소스 상속 아님 (`PROM_16_axis_findings/A4_HoTT_Univalence_TegmarkIV.md` L238 "CHU의 identity = hypergraph isomorphism을 univalence로 공리화"). **(b) "= Ruliad" 등호는 REFUTED** (아래 2026-07-15 갱신 §). 분기 구조(truncated↔un-truncated)는 유효하므로 FORK_GROUNDED 판정 자체는 유지. → `lesson-chu-ruliad-identity-refuted-truncation-reframe-2026-07-15`.
4. **스택 위치 + 어댑터 계약** — CHU 프로그램은 아키텍처상 `333(P2P 무료 base) → ORRR(유료 compute marketplace) → CHU`. Ruliad 탐색 = 대량 병렬 compute이므로 ORRR(Rain=compute 내림)이 연료층. 통합 경로 = **디커플(B): 코어 standalone 개발 → 얇은 333 어댑터를 backend 하나로** (Contract dual; 333 모듈 이미 app-agnostic; ORRR 미구현). 인터페이스 계약 스케치(4-port: ComputeSink/StateStore/BranchBus/Identity) = **`333_ADAPTER_CONTRACT.md`** (PRELIMINARY design). `orrr-orbital-rain-ruin-rein-2026-05-15`.
5. **ooptdd 검증 (2026-07-13)** — 동역학 층 Lean을 SUT로 하는 trace-gate 테스트: level-1 gate 2/2 GREEN(진짜 `lean` 컴파일로 earn + RED-proof로 non-tautological 확인), 실이벤트가 live dgx Oo(LAN 192.168.0.23:5080)로 ingest→query 왕복 성사(production LTDD). adapter=`bhgman_tool/ooptdd/chu_wolfram_adapter.py` (commit 7220da6). Lean은 level-2(`Cell` 2-morphism + `strict_truncation2`)까지 확장·exit 0.

---

## 인식적 지위 요약 (2026-07-13 PROM 16)

| 층 | 외부 소스 | confidence | 상태 |
|---|---|---|---|
| Wolfram 정식 (H₁→H₂, causal invariance) | 있음, 1차 | HIGH | 확립 |
| Gorard 범주론 정식화 | arXiv:2105.04057 | MEDIUM | pdftotext pending (2105 미검증) |
| ★ CHU↔Ruliad/observer 평행 | **없음** | MEDIUM | ~~SYMPOSIUM-side 합성(가설) — 불변~~ → **2026-07-15 정정: 문자 그대로의 동일시 REFUTED** (3축 독립 DIVERGES). 재정의 = "Ruliad ∞-groupoid의 computable truncation/thread" = PLAUSIBLE |
| CHU 동역학 층 | Lean 형식화 | MEDIUM | **PARTIALLY_GROUNDED** (CHU_WolframRewrite.lean exit 0). **2026-07-15: level-1·2 모두 realized** (`Cell`/`vtrans`/`strict_truncation2` + Rust `UnivalentStateStore`), `Trunc.collapse`(`∀ A`)로 collapse는 level-generic 증명 → 실제 OPEN = **level≥3 / n→∞ colimit / native HITs** |
| ★ HoTT 다리 (2111.03460) | 있음, **검증됨** | **HIGH** (범위 한정) | ✅ full-text 확인 (Def 2.1 / Prop 4.2·4.3 / §5.3). **2026-07-15 정정: Prop 4.4는 (∞,1)-category `∞Grpd`까지만 증명 — (∞,1)-topos는 저자 hedge(Remark 4.6), 증명 아님.** HIGH는 "논문 실재·형식성"에 한정, ∞-groupoid↔Ruliad 동일성은 PARTIAL |
| ★ univalence 분기 (A4-S2) | Prop 4.3 (분기 구조) / **소스 아님** (univalence 채택) | HIGH | **FORK_GROUNDED** (strict-eq=1-cat truncation ↔ un-truncated ∞-groupoid). **단 univalence는 CHU bolt-on 공리 — 소스 미상속** |
| Tegmark CUH 선례 | arXiv:1406.4348 | HIGH | 확립 |
| Pratt Chu-space (의미론) | 있음, 1차 | HIGH | 확립 (별개 이론) |

**KG**: cycle `prom16-wolfram-chu-ruliad-hott-2026-07-13` · `lesson-prom16-wolfram-chu-ruliad-hott-2026-07-13` (lakatos: concept-stretching + proof-analysis) · `finding-prom16-wolfram-chu-{A1..A4}-S{1..4}-2026-07-13` (16) · `hyperedge-prom16-wolfram-chu-ruliad-hott-2026-07-13` (cardinality=16).

**Note (2026-07-13 시점 기록 — 역사 보존)**: Wolfram 흡수는 기존 정전("모든 것은 하이퍼그래프", INDEX.md)의 *완성*이지 신규 이탈 아님. 단 CHU↔Ruliad 동일시는 아직 가설 — 외부 grounding 확보 전까지 `:Comment` 등급 유지. 열린 질문(동역학 층·univalence 분기)은 열린 채로.

> **⚠️ SUPERSEDED (2026-07-15)**: 위 Note의 "동일시는 아직 가설, grounding 확보 전까지 `:Comment` 유지"는 **그 grounding 조사가 실제로 수행되어 종결됨**. `prom16-chu-ruliad-grounding-2026-07-15`(16셀) 결과 — **문자 그대로의 동일시는 grounding 실패가 아니라 REFUTED**(3축 독립 DIVERGES). 따라서 `:Comment` 대기 상태가 아니라 반증된 명제이며, 생존하는 것은 재정의("Ruliad ∞-groupoid의 computable truncation/thread")뿐. 첫 문장(Wolfram 흡수=정전의 완성)은 유효. 상세 = 아래 §"인식적 지위 갱신 (2026-07-15)" + `PROM_16_RULIAD_GROUNDING_REPORT_2026-07-15.md`.

---

## 인식적 지위 갱신 (2026-07-15 PROM 16 — Ruliad grounding 전용 사이클)

> 전용 사이클 `prom16-chu-ruliad-grounding-2026-07-15` (16셀, 리포트 `PROM_16_RULIAD_GROUNDING_REPORT_2026-07-15.md`). 위 2026-07-13 표의 CHU↔Ruliad 행을 아래로 **정밀화**.

- **문자 그대로 "CHU = Ruliad" 동일시 = REFUTED** (3축 독립 DIVERGES: A1S4 category-error / A3S4 limit-computable 비폐쇄 / A4S4 plenitude↔unique-totality 존재양화 충돌).
- **재정의 = CHU는 Ruliad ∞-groupoid의 computable 1-truncation(또는 computable thread)** → PLAUSIBLE, grounded. Lean `Trunc.collapse`(2026-07-15)의 truncation dichotomy가 형식 뒷받침. "Ruliad=un-truncated ∞-groupoid" vs "CHU-computable=그 truncation"이라 동일시는 두 극을 conflate.
- **★ univalence provenance 정정**: arXiv:2111.03460은 univalence-untruncation 구성을 *하지 않음*(§5.3 철학적 backing만). univalence는 **CHU bolt-on 공리**이지 소스 상속 아님 (A2S1 pdftotext + A2S4 + A4S3/S4). 기존 106행 "FORK_GROUNDED"는 유효하나 "소스가 univalence로 Ruliad를 만든다"는 함의는 제거해야 함.
- **CHU computable 제약 = GROUNDED** (Tegmark CUH §VII / Schmidhuber ATOE / Zuse) — CHU 최강 외부앵커. 단 CUH 비판(unfalsifiability/measure/Gödel) 상속.
- **∞-groupoid 형식화 = PARTIAL** — IJTP 2024 peer-reviewed 실재하나 rulial multiway *proxy*이지 Ruliad 동일성 증명 아님, 독립 HoTT 검증 부재(nLab 無).

| CHU↔Ruliad 관계 | 이전(07-13) | 갱신(07-15) |
|---|---|---|
| 문자 그대로 동일 | 가설 `:Comment` | **REFUTED** |
| computable truncation/thread 관계 | — | **PLAUSIBLE (재정의)** |
| univalence 상속처 | 소스 §5.3 함의 | **CHU bolt-on (정정)** |

**KG (결정화 완료 2026-07-15)**: cycle `prom16-chu-ruliad-grounding-2026-07-15` + 16 `:ResearchFinding`(citation_url 전수) + `lesson-chu-ruliad-identity-refuted-truncation-reframe-2026-07-15`(resolved, lakatos=concept-stretching) + 5 seed(2 DONE) + `impl-chu-trunc-collapse-level-generic-2026-07-15`(sha256 바인딩). 실측 tally `{PARTIAL:8, DIVERGES:3, GROUNDED:3, UNGROUNDED:2}`. ⚠️ 초판의 "KG unreachable"은 **오진** — 포트는 OPEN, MCP 세션만 stale이었음(python 드라이버 직결로 해소). 열린 채: (a) truncation 재정의의 완전 정합성 (Ruliad 측 형식화 미완이라 한쪽 흐림) (b) n→∞ colimit 존재조건 (c) univalence 물리 정당화. [[feedback_webfetch_dense_paper_needs_pdftotext]] — PARTIAL 다수 신뢰 MEDIUM, 1차 정독으로 격상 필요.

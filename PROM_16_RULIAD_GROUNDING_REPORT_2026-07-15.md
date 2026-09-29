# PROM 16 — CHU↔Ruliad 동일시 External Grounding 검증 (2026-07-15)

> **Cycle**: `prom16-chu-ruliad-grounding-2026-07-15` (KG 결정화 **완료·검증** — lesson resolved + 16 RF + 5 seed + impl 링크, §KG 참조. 초판의 "KG unreachable"은 오진이었음)
> **질문**: SYMPOSIUM CHU(Computable Hyperuniverse)를 Wolfram Ruliad와 동일시하는 내부 합성 가설(`:Comment`)이 외부 문헌으로 접지되는가, 아니면 어디서 반증/분기되는가.
> **매트릭스**: 4 axis × 4 lens = 16 셀, sonnet 리서치 에이전트 병렬 출격 (haiku는 이 주제 깊이에 부족).
> **선행**: `project_chu_wolfram_absorption_2026_07_13`, memory OPEN #2 (CHU↔Ruliad `:Comment` 가설, grounding 미확보).

---

## 0. 한 줄 결론

**문자 그대로의 "CHU = Ruliad" 동일시는 REFUTED. 구조적 관계로 재정의하면 PARTIALLY GROUNDED.**
정확히는 — CHU는 Ruliad와 *동일한 것*이 아니라, **Ruliad ∞-groupoid의 computable 1-truncation(또는 computable thread)** 이다. 이 재정의는 2026-07-15 Lean 작업(`Trunc.collapse`)의 truncation dichotomy와 정확히 맞물린다.

---

## 1. 판정 매트릭스 (16셀)

| | S1 primary | S2 critique | S3 formal-bridge | S4 falsification |
|---|---|---|---|---|
| **A1 Ruliad 형식지위** | UNGROUNDED | UNGROUNDED* | PARTIAL | **DIVERGES** |
| **A2 homotopy 동일시** | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| **A3 계산가능성 경계** | GROUNDED | PARTIAL | PARTIAL | **DIVERGES** |
| **A4 존재론 선례** | GROUNDED | GROUNDED | PARTIAL | **DIVERGES** |

집계: **GROUNDED 3 · DIVERGES 3 · PARTIAL 8 · UNGROUNDED 2** (합 16).
*A1S2는 서브에이전트가 grounding_verdict 필드를 누락 → finding 내용상 UNGROUNDED로 코딩(KG도 동일). 초판이 이를 합계에서 빼 "UNGROUNDED 1"로 적었던 것은 매트릭스와 불일치한 오기 → 2026-07-15 KG 실측(`{PARTIAL:8, DIVERGES:3, GROUNDED:3, UNGROUNDED:2}`)과 일치하도록 정정.

---

## 2. Consensus (C1~C4)

### C1 — ∞-groupoid 형식화는 실재하고 peer-reviewed지만 *proxy*이지 Ruliad와의 *증명된 동일성*이 아니다
근거 셀: A1S3, A2S1, A2S2, A2S3, A2S4 (5셀 수렴, 최고신뢰 consensus)

- arXiv:2111.03460 (Arsiwalla & Gorard, "Pregeometric Spaces from Wolfram Model Rewriting Systems as Homotopy Types")는 **IJTP 2024 (Springer) 정식 게재** — preprint 이상의 지위. Prop 4.2(multiway → n-fold category, 귀납 증명) + Prop 4.3(n→∞ = ∞-groupoid) 실재.
- **그러나**: (a) Prop 4.3의 n→∞ 단계는 "n-fold groupoid의 n→∞ 극한 = ∞-groupoid"로 거의 **항진(near-tautological)**, 존재조건("infinite hierarchy of rules admissible")은 미검증. (b) (∞,1)-topos 주장은 **저자 본인이 Remark 4.6/§5에서 hedge**("may be realized", "interesting to investigate") — 증명된 Proposition 아님. (c) "colimit / terminal object" 어휘는 어느 Gorard 논문에서도 확인 안 됨 (SYMPOSIUM-side 용어일 가능성). (d) **독립 HoTT 커뮤니티 검증 부재** — nLab에 Wolfram/ruliad 항목 없음, 인용은 저자 자기순환 + Wolfram 생태계에 국한.
- 즉 ∞-groupoid는 *rulial multiway system*(형식적 proxy)에 대한 것이지, Wolfram이 비형식적으로 서술한 *Ruliad 자체*와의 증명된 동일성이 아니다.

### C2 — "univalence로 untruncate"는 CHU 자체의 bolt-on 공리이지 소스에서 상속한 게 아니다 ★ 가장 load-bearing
근거 셀: A2S1, A2S4, A4S3, A4S4 (4셀 수렴)

- arXiv:2111.03460은 **univalence를 §5.3에서 철학적 backing으로만 언급**(paths/types 동일시의 정당화), "untruncation via univalence" 구성은 **논문에 아예 없음**. 논문은 Grothendieck homotopy hypothesis(∞-groupoid ≃ homotopy type)만 사용 — 더 약한 주장.
- CHU의 로컬 문서(`A4_HoTT_Univalence_TegmarkIV.md` L238)가 "CHU의 identity = hypergraph isomorphism을 univalence로 **공리화**"라 명시 — 즉 univalence는 **CHU가 스스로 추가한 공리**.
- ⚠️ 정정 포인트: "CHU = Ruliad untruncated via univalence"라는 서술은 소스가 하지 않은 것을 소스에 귀속시킨다. 이건 [[feedback_external_canonical_referent]]가 아니라 그 반대 — AI-made 확장을 외부 정전인 양 취급한 drift.

### C3 — Ruliad 자체의 형식적 지위가 (Wolfram 본인 인정) 미완성이고 peer 물리학계는 엄밀 수학으로 인정 안 함
근거 셀: A1S1, A1S2, A1S4

- Wolfram 원문("The Concept of the Ruliad", 2021): "entangled limit of everything that is computationally possible" — 서술적/철학적 정의. Wolfram 스스로 "we're still only at the very beginning of nailing down those technical details ... difficult mathematics and formalism" 인정. 무한극한 조립에 "particular choices" 개입 + hyperruliad 무한회귀.
- 학계 비판: Aaronson("infinitely flexible", post-hoc grafting, 반증불가), Harlow("at best qualitative", QM/GR 정량예측 미재현). 단 이 비판들은 Wolfram Physics Project 일반 겨냥이지 Ruliad의 순수 계산이론적 형식화를 직접 다루지 않음(caveat).

### C4 — CHU의 *computable 제약*은 독립적 lineage에 잘 접지된다 (CHU의 최강 외부 앵커)
근거 셀: A3S1, A3S3, A4S1, A4S2

- **Tegmark CUH** (arXiv:0704.0646 §VII): "The mathematical structure that is our external physical reality is defined by computable functions." 제약 이유 = Gödel 불완전성 + Church-Turing 비계산성 회피. CHU의 computable 제약과 동기·구조 일치.
- **Schmidhuber** (Algorithmic Theories of Everything) + **Zuse** (Rechnender Raum) + **Zenil** (A Computable Universe) = "우주 = 계산가능 구조" 전통. CHU가 이 계보에 위치.
- Wolfram 본인도 Ruliad에서 **hypercomputation을 명시적으로 배제**("우리 우주에선 computation만, hypercomputation은 없다") → Ruliad = Turing-bounded rule의 얽힘.
- 비용: CHU가 CUH를 계승하면 CUH의 비판(unfalsifiability + measure problem + Gödel)도 상속.

---

## 3. Conflict — 핵심 발견: CHU의 두 앵커가 서로를 당긴다

3개 축의 falsification 셀(A1S4, A3S4, A4S4)이 **서로 다른 축에서 독립적으로** DIVERGES에 도달했고, 그 이유가 *일관*된다:

| 셀 | 축 | 분기 이유 |
|---|---|---|
| **A3S4** | 계산가능성 | limit-computable 함수 클래스는 inverse limit 하에서 **닫히지 않음**(Limit lemma). CHU=computable-closed vs Ruliad=limit-completion → 서로 다른 cardinality/위상. |
| **A4S4** | 존재론 | CUH = plenitude(∃-many 별개 실재 구조) vs Ruliad = ONE unique totality(관찰자가 slice) → **상호배타적 존재양화 구조**. 둘을 동시에 빌릴 수 없음. |
| **A1S4** | 형식지위 | 명확한 opaque axiom(CHU, Lean kernel-safe) vs 조립절차 미정의 극한(Ruliad) → category error. |

**합성**: CHU는 두 가지를 동시에 원한다 — (a) computable/CUH grounding(단일 decidable 구조) **그리고** (b) Ruliad 동일성(∀-포괄 uncomputable totality). 이 둘은 정반대로 당긴다.

이것은 **CHU 이름 자체의 내부 긴장**이다: "**Computable** Hyperuniverse"를 "untruncated Ruliad"와 동일시하면, untruncated Ruliad는 정의상 **computable이 아니므로**(A3S4) 모순이다. A3S3의 표현이 정확하다 — "CHU is coherent as *a computable thread within the Ruliad*, but not as *a computable characterization of the Ruliad itself*."

**이 긴장은 2026-07-15 Lean 작업과 정확히 맞물린다**: `strict_truncation`/`Trunc.collapse`가 ∞-tower를 computable/Neo4j 1-category로 붕괴시킨다. 즉:
- **Ruliad = un-truncated ∞-groupoid** (Type-값, witness 보존)
- **CHU-computable = 그 truncation** (Prop-값, 1-category)
"CHU = Ruliad"는 truncated 극과 un-truncated 극을 conflate한다.

---

## 4. Singleton

- **A4S3**: univalence → ontic structural realism 선례가 실재 (Ladyman & Presnell 2024, "Univalence and Ontic Structuralism", Found. Phys.; + "Hole Argument in HoTT" 2019). "동형 = 동일" 존재론에 형식 근거 있음 — CHU의 univalence *선택*에 대한 긍정적 grounding. 단 문헌 자체가 "univalence는 type에만, 물리 model은 type 아님"이라 **자기제한적** — 임의 물리/존재 대상으로 자동 이전 불가. (1셀 단독 → VERIFY 태그)

---

## 5. 원 가설에 대한 최종 verdict

| 주장 | verdict | 근거 |
|---|---|---|
| CHU = Ruliad (문자 그대로 동일) | **REFUTED** | C1-C3 + Conflict(A1S4/A3S4/A4S4) |
| CHU = Ruliad ∞-groupoid의 computable truncation/thread | **PLAUSIBLE, 재정의로 grounded** | C4 + A3S3 + Lean truncation dichotomy |
| ∞-groupoid 형식화가 CHU를 뒷받침 | **PARTIAL** | C1 — proxy(rulial multiway) O, Ruliad 동일성 X |
| univalence 상속이 소스에서 옴 | **FALSE** | C2 — CHU bolt-on 공리 |
| computable 제약의 존재론 선례 | **GROUNDED** | C4 — Tegmark CUH / Schmidhuber / Zuse |

---

## 6. 권장 후속 작업 (씨앗)

1. **[HIGH] 정전 재정의**: CHU를 "Ruliad와 동일"이 아니라 **"Ruliad ∞-groupoid의 computable 1-truncation"** 으로 canon 재배치. `:Comment` 가설 → 재정의된 명제로 승격 후보. Lean `Trunc.collapse`가 형식 뒷받침. (열린 사고 원칙: "동일" 주장은 닫지 말고 "truncation 관계"로 열어둠.)
2. **[HIGH] univalence provenance 정정**: CHU 문서 전반에서 "소스(2111.03460)가 univalence untruncation을 한다"는 함의를 제거, "CHU 자체 공리"로 명시. [[feedback_ai_made_content_self_correct_on_measurement]] 적용.
3. **[EXPLORATION] computable-thread vs untruncated-totality 분기 형식화**: A3S4의 "limit-computable은 inverse limit 하 비폐쇄" 정리를 Lean/문서로 접지 — CHU(computable)와 Ruliad(completion)의 위상 차이를 정리로.
4. **[VERIFY] A4S3 univalence-구조실재론 선례**: Ladyman & Presnell 2024를 1차 정독(pdftotext), CHU states/paths가 실제 HoTT type으로 형식화됐는지 확인.
5. **[MEDIUM] Wolfram 2026 "What Ultimately Is There? Metaphysics and the Ruliad"** (A4S4가 인용) — Ruliad 존재론 최신 원문, Ruliad=unique-totality 주장 재확인용.

---

## 7. 인식적 지위 요약

- **가장 확실**: CHU의 computable 제약 grounding (C4, GROUNDED ×3), univalence가 CHU bolt-on이라는 사실 (C2).
- **확정적 반증**: 문자 그대로의 CHU=Ruliad 동일성 (3축 독립 DIVERGES).
- **열린 채 유지**: (a) CHU = Ruliad의 computable truncation이라는 재정의가 완전히 정합적인지 (Lean 뒷받침은 있으나 Ruliad 측 형식화가 미완이라 양변 중 한쪽이 흐림). (b) n→∞ colimit 존재조건 (2026-07-15 Lean OPEN과 동일). (c) univalence의 물리/존재론적 정당화.
- **방법론 caveat**: 리서치 에이전트 대부분이 논문 full-text 아닌 abstract/search-snippet 기반 (A2S1만 pdftotext 직접) → PARTIAL 다수의 신뢰는 MEDIUM. [[feedback_webfetch_dense_paper_needs_pdftotext]]. 후속 1차 정독으로 격상 필요.

---

## KG — 결정화 완료 (2026-07-15)

KG write **완료·검증됨**: `lesson-chu-ruliad-identity-refuted-truncation-reframe-2026-07-15`(resolved=true, lakatos_mechanism=concept-stretching) + 16 `:ResearchFinding`(citation_url 전수) + cycle `prom16-chu-ruliad-grounding-2026-07-15` + 5 seed(2건 DONE) + `impl-chu-trunc-collapse-level-generic-2026-07-15`(sha256 바인딩, lean_verified). 실측 검증: RF=16 / seeds=5 / verdict tally = `{PARTIAL:8, DIVERGES:3, GROUNDED:3, UNGROUNDED:2}`.

> **⚠️ 진단 정정 (2026-07-15)**: 본 리포트 초판은 "정본 KG unreachable(No route to host, CP migration)"이라 기록하고 KG write를 defer했으나 **오진**이었다. 포트는 계속 OPEN이었고 **MCP 세션만 stale**했던 것 — `reference_neo4j_mcp_stale_direct_driver_fallback`이 정확히 이 경우를 경고했는데 적용하지 않았다. python 드라이버 직결(`bolt://127.0.0.1:7687`)로 즉시 write 성공(97,818 노드 라이브 확인). 부수 피해: defer용 pending cypher를 `/tmp` 스크래치패드에 뒀다가 세션 전환과 함께 소실 (`feedback_agent_work_must_be_pushed_not_left_dirty` 재발) — 다만 KG가 살아있어 내용 손실은 없음.

KG write는 Constrain Layer 트리거 `t_researchfinding_citation_required`(Longinus L4 covenant)에 1차 차단됨 → 16셀 전부에 1차 인용 URL 부착 후 통과. 스키마가 의도대로 동작.

axis 상세 findings: `PROM_16_RULIAD_GROUNDING_axis_findings/A{1,2,3,4}_*.md`.

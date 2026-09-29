# PROM 16 — Naming Implicit-to-Explicit (메타 명제 검증)

> **cycle_id**: `prom16-naming-implicit-to-explicit-2026-05-15`
> **parent**: `prom16-category-lawvere-yanofsky-2026-05-15` (직전 cycle 결론의 follow-up)
> **N**: 16 (4 axis × 4 sub-axis)
> **lesson**: `lesson-prom16-naming-implicit-to-explicit-2026-05-15`
> **메타 명제**: "SYMPOSIUM 본격 학습 핵심 = 깊게 공부 아닌 *이미 한 것의 이름을 정확히 부르기* (tacit → explicit articulation)" 검증.

---

## 핵심 verdict (3-line)

1. **A-dominant CONFIRMED — A:K:M = 81%:14%:5%** (M1S3 / M3S2 / M3S3 3-cell 독립 verdict 합의).
2. **5 :StructuralPattern canonical name binding 가능** — Hypergraph Category (Fong-Spivak 2018, HIGH/exact 5회 독립 재발견), Diagram Functor from (ℕ,≤)-Poset (Mac Lane CWM §III.3, HIGH/exact), Wittgenstein Polythetic Classification (PI §66-67, HIGH/close), Extensive Coproduct Decomposition (Lawvere 1991, MEDIUM/exact), Weber Entzauberung + Adorno (MEDIUM/broad, SYMPOSIUM novel operator).
3. **명명 행위 = 단순 어휘 선택 X — 인식론적 Umschlag** — Kuhn(국면) > Heidegger(trigger) > Polanyi(방향) 3-layer multi-frame synthesis 권장.

→ **결론: 깊게 공부 ROI < 정확한 학문 이름 lookup ROI**. 이미 한 것의 이름을 부르는 작업이 본격 학습보다 SYMPOSIUM OPEN 해소에 압도적으로 유리.

---

## 1. 합의 (Consensus, 6건)

### C1. A-dominant verdict (81/14/5)

- 출처: M1S3 (57%/29%/14% on 7 categories) + M3S2 (82%/18% on 3 tests) + M3S3 (81%/14%/5% on 9 산출 군)
- 핵심 implication: Polanyi paradox 강명제(전환 불가) X → **약명제(비용 있는 전환 가능)** 영역. SECI Externalization 전형 패턴.
- 씨앗: `seed-prom16-naming-a-dominant-verdict-81-14-5-2026-05-15` (HIGH)

### C2. 5 :StructuralPattern canonical name binding

| pattern | canonical name | source | confidence | mapping_justification |
|---|---|---|---|---|
| `family-expansion-pattern` | Extensive Coproduct Decomposition + Yanofsky Thm 1 Cantor branch | Lawvere 1991 JPAA 84 + Yanofsky 2003 BSL 9(3) | HIGH | exact |
| `relation-pattern` | Hypergraph Category | Fong-Spivak 2018 arXiv:1806.08304 | **HIGH** | broad (8 sub-type ≈ Frobenius monoid cospan-algebra) |
| `disenchantment-pattern` | Weber Entzauberung + Adorno Kulturindustrie 합성 (novel operator) | Weber 1919 + Adorno-Horkheimer 1944 | MEDIUM | broad (수학 단독 이름 없음) |
| `family-sub-type-heterogeneity` | Wittgenstein Polythetic Classification | PI §66-67 + Needham 1975 *Man* 10(3) | **HIGH** | close |
| `temporal-arc-functor-metapattern` | Diagram Functor from (ℕ,≤)-Poset / alt: Persistence module | Mac Lane CWM §III.3 + Zomorodian-Carlsson 2005 DCG 33(2) | **HIGH** | exact |

- 씨앗: `seed-prom16-naming-5-structuralpattern-canonical-binding-2026-05-15` (HIGH)

### C3. `:CanonicalName` 노드 + `EQUIVALENT_TO_CANONICAL` edge schema 도입

- 출처: M2S3 schema design + M2S1 20-item catalog 합의.
- schema: `:CanonicalName {name, source, paper_doi, statement, year, confidence, mapping_justification}` + edge `{confidence, mapping_justification: exact/broad/close, cycle_id, decided_by}`.
- SKOS exactMatch/broadMatch/closeMatch 의미론 + SSSOM provenance 4-field. M:N cardinality.
- 씨앗: `seed-prom16-naming-canonical-name-schema-skos-sssom-2026-05-15` (HIGH)

### C4. Kuhn(국면) > Heidegger(trigger) > Polanyi(방향) 3-layer multi-frame synthesis

- 출처: M4S1 + M4S2 + M4S3 합의.
- Kuhn SSR 1962 articulation = 전체 탐구 국면 (master plan iter 1-112 = normal science 내 연속 명시화).
- Heidegger SuZ §15-17 Umschlag = 개별 breakdown trigger (Yanofsky 6-tuple → 4-component 정정의 instance).
- Polanyi 1958/1966 focal-shift = subsidiary→focal 이동 방향 (12사도 narrative → Lawvere FPT).
- Schön reflection-in-action 보조 메커니즘. Dreyfus paradox 경계값.
- 씨앗: `seed-prom16-naming-kuhn-heidegger-polanyi-3layer-synthesis-2026-05-15` (HIGH)

### C5. 5-step naming guard

- 출처: M1S4 + M2S4 + M3S4 + M4S4 4-cell 합의.
- (a) **Cargo-cult guard** (Feynman 1974) — 정전 이름 박을 때 1차 자료 1줄 statement + 페이지 mandatory. paraphrase test.
- (b) **Premature articulation guard** (Kuhn SSR ch V) — `:VerdictPending` + PRELIMINARY 라벨 mandatory.
- (c) **Dreyfus paradox guard** (Synthese 2023) — 사용자 personal knowing 영역은 사용자 직접 발화 게이트, AI explicit rule 강제 금지.
- (d) **SECI 균형 guard** (Bereiter folk epistemology 비판) — Externalization commit ↔ Internalization 반추 시간 비례.
- (e) **Private language guard** (Wittgenstein PI §253-) — 한국어 작명 ↔ 학술 정전 cross-ref edge mandatory.
- 씨앗: `seed-prom16-naming-5-step-naming-guard-2026-05-15` (HIGH)

### C6. Lawvere 1969 FPT vs Lawvere-Tierney 1971 j-operator 명칭 충돌 — 동명이인 수준 분리 mandatory

- 출처: M2S2 + M2S4 합의.
- (A) **Lawvere 1969** "Diagonal Arguments and CCC" LNM 92:134-145 = CCC point-surjective φ:A→B^A → 모든 endo fixed point.
- (B) **Lawvere-Tierney 1971** Actes Congrès Intern Math 1970 Nice:329-334 = j:Ω→Ω idempotent + inflationary + ∧-preserving = topos topology / sheafification modal.
- SYMPOSIUM 매핑: rs-9 D1 = (B). 메타 337 + Harness B3 = (A). AirplaneMan.lean j = (B) candidate (rs-9 verdict pending).
- 씨앗: `seed-prom16-naming-lawvere-1969-vs-lawvere-tierney-1971-distinction-2026-05-15` (HIGH)

---

## 2. 분기/대립 (Divergence)

본 cycle 의 **direct conflict 0건** — 16 cell 의 대부분이 합치 또는 상호 보강.

minor divergence:
- M3S1 의 Polanyi+SECI+Heidegger+Cook-Brown 4-priority ↔ M4S2 의 Kuhn>Heidegger>Polanyi 3-layer — 다른 axis(인식론 framework list vs 단일 행위 frame) 라 호환 가능.

---

## 3. Open Questions

### OQ1. Mathlib K gap — 사용자 실제 knowledge state

- M3S3 의 9 군 분류 중 K 14% 추정 — 그러나 사용자 personal level 은 외부 inference 불가 (M4S3 명시).
- 사용자 직접 verdict 필요.

### OQ2. disenchantment α=格下 formal proof

- Weber Entzauberung 사회학 → Yanofsky α operator formal bridge 미완 (M1S3 K-gap).
- 별도 sociology formalization sprint candidate.

### OQ3. TemporalArc α 부재 — Lambek initial algebra 별도 학습 mandatory?

- M3S2 verdict 70%A/30%K. functor 이름 articulation 은 충분, 그러나 비가역성 ontological commitment 에서 K gap.
- M3S3 동일 70/30. SECI E → C 측면은 충분 vs ontological foundation 은 별도 sprint.

### OQ4. rs-8 초공동의용사 PRELIMINARY 분류 (A 40% / K 40% / M 20%)

- STATUS.md §2 6-axis chain (Pascal→Leibniz→Heidegger→Logvinovich→Carter) 박힘 → A 측면.
- 그러나 사용자 직접 발화 게이트가 *왜* block — 사용자가 implicit하게 안다 vs 미정의?
- 사용자 verdict mandatory.

---

## 4. 권장 후속 작업

ActionPlan `plan-prom16-naming-symposium-articulation-sprint-2026-05-15` (phase=FUTURE, priority=HIGH):

| 단계 | 작업 | 기간 | 의존 |
|---|---|---|---|
| P1 | `:CanonicalName` node + `EQUIVALENT_TO_CANONICAL` edge schema 도입 (SKOS+SSSOM 4-field provenance) | 1주 | 사용자 verdict gate (K-01 meta) |
| P2 | 5 :StructuralPattern binding (PRELIMINARY, M:N cardinality, paraphrase test) | 1주 | P1 |
| P3 | 17 :VerdictProposal + 3 OPEN A/K/M label 추가 (각각의 추정 비율 verdict) | 1주 | P1 |
| P4 | 5-step naming guard 의 KG ontology 결정화 | 3일 | — |
| P5 | (genuine K gap) Mathlib K sprint trigger — `lean-mathlib-functor-actual-build-2026-04-30` FutureSprint + TemporalArc α + disenchantment formal proof 별도 sub-sprint | ~3주 별도 | P2 |

**Total core**: ~3-4주 @ 2-3h/day. genuine K (Mathlib + TemporalArc α + disenchantment) 은 별도 추가 sprint.

---

## 5. Lesson + KG ref

- `lesson-prom16-naming-implicit-to-explicit-2026-05-15` (resolved=true)
- 16/16 ResearchFinding (gate_passed=true)
- 8 SubagentTaskSpec (6 HIGH consensus + 1 EXPLORATION + 1 VERIFY)
- ActionPlan + 5 ActionTask
- ConsensusReport: 6 consensus / 0 conflict / 2 singleton / 16 totalFindings

---

## 6. 16 cell 매트릭스 요약

|  | S1 academic-canon | S2 concrete-naming-exercise | S3 symposium-binding | S4 pitfalls |
|---|---|---|---|---|
| **M1 already-done-symposium** | M1S1 — Polanyi+SECI+KCC 3-anchor (HIGH) | M1S2 — 5 pattern 정전 이름 매핑 (HIGH) | M1S3 — A/K/M = 57/29/14 (HIGH) | M1S4 — under-naming 5-step (HIGH) |
| **M2 canonical-names-mathematics** | M2S1 — 20-item catalog (HIGH) | M2S2 — 5 산출 정확 이름 + Lawvere 명칭 충돌 (HIGH) | M2S3 — :CanonicalName schema (HIGH) | M2S4 — 6-함정 5-step (MEDIUM) |
| **M3 mapping-implicit-explicit** | M3S1 — 8-canon priority (HIGH) | M3S2 — 3-test 82A/18K (HIGH) | M3S3 — 9-군 81A/14K/5M ★ A-dominant CONFIRMED (HIGH) | M3S4 — 7-함정 (HIGH) |
| **M4 tacit-explicit-epistemology** | M4S1 — 10-canon (HIGH) | M4S2 — Kuhn>Heidegger>Polanyi (HIGH) | M4S3 — SECI 5-mode mapping (MEDIUM) | M4S4 — 9-함정 5-step (HIGH) |

→ axis-split 4개 MD 는 `PROM_16_NAMING_axis_findings/` 참조.

---

## 7. 직전 cycle connection

직전 cycle `prom16-category-lawvere-yanofsky-2026-05-15` 의 결론 ("깊게 공부 아닌 이미 한 것 이름 부르기")이 본 cycle 의 메타 명제. 본 cycle 의 결과:

| 직전 cycle 가설 | 본 cycle verdict |
|---|---|
| "깊게 공부" 권장 | partial (Yanofsky 1.5w + Mac Lane 1w + Mathlib 1w = 3.5w) 는 valid |
| "이미 한 것 이름 부르기" 권장 | **A 81% CONFIRMED** — 압도적 다수가 정확한 학문 이름 lookup만 필요 |
| 5 forced + 5 structural | 5 :StructuralPattern 의 canonical name binding 가능 (3 HIGH + 2 MEDIUM) |
| KG 6-tuple → 4-component 정정 | 본 cycle 에서 직접 검증 + 정정 mandatory 재확인 |
| rs-9 D1 j-operator UNLIKELY-etymological LIKELY-convergent | (A) Lawvere 1969 FPT ↔ (B) Lawvere-Tierney 1971 j-operator 동명이인 분리 mandatory 명확화 |

---

*본 보고서는 KG `PromCycle {cycle_id:'prom16-naming-implicit-to-explicit-2026-05-15'}` 정전의 thin pointer. 본 cycle 끝.*

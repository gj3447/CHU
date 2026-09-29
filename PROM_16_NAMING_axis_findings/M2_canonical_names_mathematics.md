# Axis M2 — Canonical Names Mathematics (학문 정전 정확 이름)

## M2S1 (academic-canon) — 20-item catalog

**finding**: `finding-prom16-naming-M2S1-canonical-names-canon-2026-05-15` (HIGH)

### 범주론 14항목 (정전 이름 + 정확 좌표)

| C | 저자·연도 | 제목(약칭) | 출판 좌표 | 핵심 statement |
|---|---|---|---|---|
| C1 | Yanofsky 2003 | Universal Approach to Self-Referential Paradoxes | BSL 9(3):362-386; arXiv:math/0305282; DOI:10.2178/bsl/1058448677 | **4-component scheme** (T, Y, f:T×T→Y, α:Y→Y) |
| C2 | Lawvere 1969 (positive) | Diagonal Arguments & CCC | LNM 92:134-145; TAC Reprint 15 | point-surjective φ:A→B^A 존재 → ∀f:B→B fixed point |
| C3 | Lawvere 1969 (negative) | 同上 contrapositive | 同上 | f:X→Ω^X 전사 → topos degenerate (Cantor 통합 형식) |
| C4 | Tarski 1955 | Lattice-Theoretical Fixpoint Theorem | Pacific J Math 5(2):285-309; DOI:10.2140/pjm.1955.5.285 | 완전 격자 단조함수 fixed point 집합 = 완전 격자 (Knaster-Tarski) |
| C5 | Lambek 1968 | Fixpoint Theorem for Complete Categories | Math Z 103 | **μF initial algebra** (α:FA→A 동형, A≅FA) |
| C6 | Lambek 1968 dual | 同上 terminal coalgebra | 同上 | **νF terminal coalgebra** = F의 최대 고정점; μF↔νF 쌍대 |
| C7 | **Lawvere-Tierney 1971** | Quantifiers & Sheaves / Topos Topology | Actes Congrès Intern Math (1970 Nice):329-334 | **j:Ω→Ω**, j∘true=true, j∘j=j, j∘∧=∧∘(j×j) — sheafification modal idempotent |
| C8 | Yoneda (via CWM III §2) | Yoneda Lemma | CWM Ch.III §2 | Nat(h_c, X) ≅ X(c) |
| C9 | Kan (via CWM Ch.X) | Kan Extension | CWM Ch.X Thm.2 | Lan_p F universal factorization |
| C10 | Lawvere 1963 | Functorial Semantics | PNAS 50(5):869-872; DOI:10.1073/pnas.50.5.869 | 대수 이론 T 의미론 = Set^T → Set functor (bridge axiom interface) |
| C11 | Grothendieck SGA 1 1960-61 | Fibered Categories | SGA 1 Exposé VI; arXiv math/0206203 | fibration cartesian lift / Grothendieck construction |
| C12 | Fong-Spivak 2018 | **Hypergraph Categories** | arXiv:1806.08304 | symmetric monoidal + Frobenius monoid per object |
| C13 | Lambek 1969 | Deductive Systems II | Math Syst Theory 2(4) | polycategory: multi-input multi-output |
| C14 | Leinster 2004 | Higher Operads, Higher Categories | LMS Lec. Note 298; arXiv:math/0305049 | multicategory + higher operad |

### 인식론 6항목

| C | 저자·연도 | 제목 | 출판 좌표 | 핵심 statement |
|---|---|---|---|---|
| C15 | Polanyi 1958 | Personal Knowledge | UChicago Press, ISBN 978-0-226-23262-1 | tacit knowing 4차원 (phenomenological/instrumental/semantic/ontological) |
| C16 | Wittgenstein 1953 | Philosophical Investigations | Blackwell, ISBN 978-0-631-23127-1 | §43 use-meaning / §66 family resemblance / §201 rule-following paradox |
| C17 | Kuhn 1962 | Structure of Scientific Revolutions | UChicago Press, ISBN 978-0-226-45808-3 | paradigm articulation: exemplar-based tacit → propositional |
| C18 | Lakatos 1976 | Proofs and Refutations | Cambridge, ISBN 978-0-521-29038-5 | rational reconstruction = informal → formal axiomatic |
| C19 | Heidegger 1927 | Sein und Zeit §15-17 | Niemeyer; Macquarrie-Robinson trans | Zuhandenheit → Vorhandenheit thematization (Umschlag) |
| C20 | Nonaka-Takeuchi 1995 | Knowledge-Creating Company | Oxford, ISBN 978-0-195-09269-1 | SECI 4-mode spiral |

### 정정 4건 (기존 implicit 인용 explicit)

1. **Lawvere positive/negative 분리** (C2/C3) — 한 정리 두 form, 단일 인용 시 어느 측 명시 mandatory.
2. **Lambek μF/νF 분리** (C5/C6) — initial algebra ↔ terminal coalgebra 쌍대.
3. **SGA 1 Exposé VI vs SGA 4 Exposé VI 구분** — fibration 기초 vs 발전된 결과.
4. **Yanofsky scheme α 역할 일반화** — 단일 negation X, semantic evaluation 등 다양.

## M2S2 (concrete-naming-exercise) — 5 산출 정확 이름

**finding**: `finding-prom16-naming-M2S2-canonical-naming-exercise-2026-05-15` (HIGH)

| 산출 | 권장 정확 이름 | confidence | 정전 인용 | wrong-naming 위험 |
|---|---|---|---|---|
| **메타 337** M_∞=P(M_∞) | **Knaster-Tarski 최대 fixed point** (완전 격자 단조함수) + **Lawvere FPT positive** | HIGH | Tarski 1955 PJM 5(2); Lawvere 1969 LNM 92 | Yanofsky Thm 번호 미검증 |
| **재배맨 D1 j-operator** | **Lawvere-Tierney j-operator** (idempotent topos closure on Ω) | HIGH | nLab 'Lawvere-Tierney topology' | **명칭충돌 최대** — Lawvere 1969 FPT 동명이인 |
| **Harness ∀-cover 불가능** | **Lawvere FPT negative** (contrapositive) + Yanofsky 2003 일반화 | HIGH | Lawvere 1969; Yanofsky 2003 | 긍정/부정 dual 혼동 |
| **AirplaneMan.lean** isAirplaneMan(j) | **Universal coverage predicate** / **total j-sheaf condition** | MEDIUM | Lean 4 술어 자체; Johnstone *Sketches* C1 | 기성 정전 단일 이름 없음 |
| **CHU:Type** | **Chu space** (Barr 1979 LNCS 752 + Pratt 1995) + 사용자 'Computable Hyperuniverse' 독립 재발명 | HIGH | Barr 1979; Pratt 1995 | Pratt Chu space와 사용자 CHU 직접 동일시 금지 |

## M2S3 (symposium-binding) — :CanonicalName schema

**finding**: `finding-prom16-naming-M2S3-canonical-names-symposium-2026-05-15` (HIGH)

```cypher
// Schema
(:CanonicalName {
  name: String,            // 'yanofsky_2003_4component_scheme'
  source: String,          // 'BSL 9(3):362-386'
  paper_doi: String,       // '10.2178/bsl/1058448677'
  statement: String,       // 'For (T,Y,f,α) with α fixed-point-free, no g:T→Y is representable by f via diagonal'
  year: Int,
  confidence: 'HIGH'|'MEDIUM'|'LOW',
  mapping_justification: 'exact'|'broad'|'close'
})

(:StructuralPattern|:ResearchFinding|:VerdictProposal)
  -[:EQUIVALENT_TO_CANONICAL {
    confidence,
    mapping_justification,
    cycle_id,
    decided_by
  }]->(:CanonicalName)
```

**SKOS** exactMatch/broadMatch/closeMatch 의미론 + **SSSOM** provenance 4-field. **M:N cardinality**.

## M2S4 (pitfalls) — 6-함정 5-step guard

**finding**: `finding-prom16-naming-M2S4-canonical-naming-pitfalls-2026-05-15` (MEDIUM)

3축 충돌:
1. **저자명 공유** — Lawvere 1969 FPT vs Lawvere-Tierney 1971 j-operator (nLab 분리 인용)
2. **층위 혼동** — Russell 집합론 ∈ vs Lawvere CCC morphism diagonal
3. **문화 전용** — Haskell "Monad = wrap" misnomer

5-step 회피:
- (a) 1차 자료 verify (nLab/arXiv/SEP 원문)
- (b) PRELIMINARY 라벨 mandatory
- (c) `EQUIVALENT_TO_CANONICAL` provenance 첨부
- (d) K-01 meta drift-correction (drift 정정 자체 측 drift 가능)
- (e) **paraphrase test** — 정전 이름 측 환언 불가 = cargo-cult flag

SYMPOSIUM 측 한국어 작명 (재배맨/비행기맨/스페이스걸) 측 **USER_PRIMARY** 고정 + **AcademicAlias** 분리 (Eilu va-Eilu 양쪽 보존).

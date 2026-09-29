# Axis A — CWM Pedagogy (Mac Lane "Categories for the Working Mathematician")

> cycle `prom16-category-lawvere-yanofsky-2026-05-15` 측 axis A 측 4 cell 측 통합 정전.

## A1 (S1 academic-canon) — CWM 2판 학술 정전

**finding**: `finding-prom16-cat-lawv-A1-cwm-canon-2026-05-15` (HIGH)

- **표준 정전**: Mac Lane, *Categories for the Working Mathematician*, **Springer GTM 5, 2nd ed 1998, ISBN 978-0-387-98403-2** (DOI 10.1007/978-1-4757-4721-8).
- **1차 원전**: Eilenberg-Mac Lane (1945) "General Theory of Natural Equivalences", *Trans. AMS* **58**:231-294 (DOI 10.2307/1990284).
- **Lawvere 원전**: TAC Reprints No. 15 (2006), free PDF — Lawvere 1969 *Diagonal Arguments and Cartesian Closed Categories* (LNM 92, Springer, pp 134-145).
- **보조 정전**:
  - Awodey, *Category Theory*, 2nd ed (OUP, 2010), ISBN 978-0-19-923718-0 — CS/logic 배경자용.
  - Riehl, *Category Theory in Context* (Dover, 2016), ISBN 978-0-486-80903-8, 무료 PDF (`emilyriehl.github.io/files/context.pdf`).

## A2 (S2 learning-order) — 학습 순서

**finding**: `finding-prom16-cat-lawv-A2-cwm-order-2026-05-15` (HIGH)

- **선수지식**: 집합론(ZFC 수준 X, 함수/관계 직관 충분) + 군론 기초 + 선형대수 + 점집합위상(optional).
- **권장 순서** (2-3h/일):
  1. Ch.I (~24p, 2-3주) — 범주/함자/자연변환
  2. Ch.II (~20p, 2-3주) — functor categories
  3. **Ch.IV (~33p, 2-3주) — Adjoints** (Mac Lane 본인이 '핵심'으로 지목)
  4. Ch.III (~25p, 1-2주) — Universals & Limits (adjoint 후 읽으면 universal = adjoint 특수사례로 이해)
  5. Ch.V (~28p, 2주) — Limits 심화
  6. Ch.VI (~24p, 2주) — Monads & Algebras
  7. Ch.VII (~30p, 2주) — Monoids
- **Core (I–VII): 14-16주** (집중).
- **Adjoint-first 전략 유효** — Mac Lane 본인 권장.
- **단축 경로**: Riehl CTIC 무료 PDF 병행이 MathOverflow 합의 best supplement.

## A3 (S3 symposium-binding) — CWM ↔ SYMPOSIUM 산출 binding

**finding**: `finding-prom16-cat-lawv-A3-cwm-symposium-2026-05-15` (HIGH)

| SYMPOSIUM 산출 | CWM 챕터·섹션 | 핵심 정리/개념 | 강도 |
|---|---|---|---|
| `temporal-arc-functor-metapattern` | I §2-3 + V §1-3 | functor from poset-as-category; diagram = functor | **HIGH** |
| `family-relation-mirror-hypothesis` | IV §1 + X §1-3 | adjunction unit/counit; Kan extension | MEDIUM |
| `selfreference-positive-fixed-point-meta-infinity` | **CWM ABSENT** | Lawvere 1969 LNM 92 별도 필수 | CWM ABSENT |
| `relation-pattern-canonical` (8 sub-type) | VII §1-2 + XI §1-4 (partial) | monoidal/braiding skeleton; Fong-Spivak 2019 별도 | MEDIUM |
| `family-expansion-pattern-canonical` (∀-cover) | V §1-4 + III §3-4 | limit/colimit universal cone | **HIGH** |
| 12사도 ↔ 5무기 functorial mapping | I §3-4 + II §4 | functor + natural transformation + functor category | **HIGH** |

→ **3 HIGH + 2 MEDIUM + 1 ABSENT**. M_∞ positive fixed point는 CWM 범위를 원천적으로 초과 — Lawvere 1969 + Yanofsky 2003 cross-ref mandatory.

## A4 (S4 pitfalls) — 학습 함정

**finding**: `finding-prom16-cat-lawv-A4-cwm-pitfalls-2026-05-15` (HIGH)

| # | 함정 | 회피 |
|---|---|---|
| 1 | Set vs Class size paradox (Ch.I §2) | NBG/Grothendieck universe 분기 명시; Murfet 2006 *Foundations for CT* 보충 |
| 2 | "abstract nonsense" 오독 | Steenrod 작명, Mac Lane 자조적 사용. 비하 아님 |
| 3 | Yoneda 역직관 stuck (Ch.III §2) | math3ma.com Eugenia Cheng 직관 먼저, nLab formal 나중 |
| 4 | Ch.IV adjoints 고밀도 | Riehl CTIC 2016 병행 (MathOverflow 69251 합의) |
| 5 | 모나드 "wrap" misnomer (한국어/Haskell 블로그) | CWM p.138 "monoid in endofunctor category" 정전. Bartosz Milewski 2017 정확 브릿지 |
| 6 | SYMPOSIUM prose ↔ CWM formal layer-confusion | Family-Expansion drift 동형. Lawvere *Functorial Semantics* (PNAS 1963) bridge axiom 인터페이스 mandatory |

---

**axis-level synthesis (Consensus C5 + Δ1 + OQ5)**:
- CWM은 functor·adjoint·Yoneda·Kan 측 **4개 backbone 산출**(temporal-arc / ∀-cover / 12사도-5무기) 직접 binding.
- M_∞은 CWM ABSENT → **Lawvere 1969 + Yanofsky 2003 측 별도 사이클 필요** (axis B 정전).
- prose↔formal layer-confusion 측 함정 측 회피 mandatory.

## Refs

- Mac Lane, *CWM* 2nd ed: <https://link.springer.com/book/10.1007/978-1-4757-4721-8>
- Eilenberg-Mac Lane 1945: <https://www.ams.org/journals/tran/1945-058-00/S0002-9947-1945-0013131-6/>
- Lawvere 1969 TAC reprint 15: <http://tac.mta.ca/tac/reprints/articles/15/tr15abs.html>
- Riehl CTIC PDF: <https://emilyriehl.github.io/files/context.pdf>
- Awodey CT 2nd: <https://global.oup.com/academic/product/category-theory-9780199237180>
- nLab CWM: <https://ncatlab.org/nlab/show/Categories+for+the+Working+Mathematician>

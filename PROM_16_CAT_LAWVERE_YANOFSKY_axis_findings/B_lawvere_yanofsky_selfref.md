# Axis B — Lawvere 1969 + Yanofsky 2003 자기참조 정리 (self-reference unification)

> cycle `prom16-category-lawvere-yanofsky-2026-05-15` 측 axis B 측 4 cell.

## B1 (S1 academic-canon) — 정전 paper citation

**finding**: `finding-prom16-cat-lawv-B1-canon-2026-05-15` (HIGH)

- **Lawvere 1969**: "Diagonal arguments and Cartesian closed categories", in *Category Theory, Homology Theory and their Applications II*, Lecture Notes in Mathematics **vol 92**, Springer 1969, pp 134–145.
  - 자유 reprint: TAC Reprints No. 15 (2006) — <http://tac.mta.ca/tac/reprints/articles/15/tr15abs.html>
  - 정확 정리: "Let A be a CCC. If there exists a point-surjective morphism φ: A → B^A, then every f: B → B has a fixed point s: 1 → B."

- **Yanofsky 2003**: "A universal approach to self-referential paradoxes, incompleteness and fixed points", *Bulletin of Symbolic Logic* **9**(3), Sept 2003, pp 362–386.
  - DOI: `https://doi.org/10.2178/bsl/1058448677`
  - arXiv: `https://arxiv.org/abs/math/0305282`
  - 4-component scheme `(T, Y, f: T×T → Y, α: Y → Y)` + diagonal `Δ: T → T×T` + `g(t) = α(f(t,t))`. ← **NOT 6-tuple** (cf. C1 정정).

- **Roberts 2023**: "Substructural fixed-point theorems and the diagonal argument: theme and variations", *Compositionality* **5**(8) 2023.
  - arXiv: `https://arxiv.org/abs/2110.00239`
  - Lawvere FPT 측 weakening/exchange 없는 substructural logic 변종.

- **Awodey-Bauer 2009** "Propositions as [Types]" 측 cross-ref 측 **불확인** (arXiv/저자 페이지 검색 미발견). 사용 시 별도 1차 확인 필수.

## B2 (S2 learning-order) — 학습 순서

**finding**: `finding-prom16-cat-lawv-B2-order-2026-05-15` (HIGH)

권장 핵심 경로 (200–300시간):

1. **Cantor 1891** — Halmos *Naive Set Theory* (60p, 2-3주) 또는 Enderton *Elements of Set Theory* Ch.1-3 (4-6주)
2. **Russell 1902** — Russell letter to Frege (2p) + SEP *Self-Reference* (1주)
3. **Berry/Richard/Grelling** — Boolos *Computability and Logic* 5th Ch.1-2 (2-3주)
4. **Gödel 1931** — Peter Smith *An Introduction to Gödel's Theorems* (8-12주, 표준 입문)
5. **Tarski 1933** — Smith 책 내 Tarski 챕터 (1-2주)
6. **Turing 1936** — Boolos 5th Ch.3-6 (3-4주)
7. **Löb 1955** (optional) — Boolos *Logic of Provability* (4-6주)
8. **Lawvere 1969** — Yanofsky 2003 arXiv 먼저 (10-20h), nLab + Bartosz Milewski 2019 블로그 *Fixed Points and Diagonal Arguments* + CCC 전제로 Awodey CT Ch.1-6 (8-12주 병행)
9. **Yanofsky 2003** 논문 전체 (30-40h)
10. **Hofstadter GEB** (optional, 마지막) — 4-6주
11. **현대**: Roberts 2023 substructural (optional)

**단축 경로 (범주론 선행자)**: Awodey CT → Yanofsky 2003 → Lawvere nLab → 역방향 Gödel/Tarski 재독. 100-150시간.

**한국어 막힘**:
- (1) Gödel 번호화 — Smith Ch.4-6 반복 필수
- (2) Lawvere CCC exponential/evaluation/currying — Awodey 영어 원서 불가피
- (3) Yanofsky 'total function' vs 'point-surjective morphism' — 집합론 감각으로 범주론 개념 오독

## B3 (S3 symposium-binding) — Yanofsky 4-component scheme ↔ SYMPOSIUM

**finding**: `finding-prom16-cat-lawv-B3-symposium-2026-05-15` (MEDIUM)

| # | SYMPOSIUM 산출 | 4-component (T, Y, f, α) | 방향 | conf |
|---|---|---|---|---|
| 1 | M_∞ positive fixed point | T=MetaHumotonic, Y={T,F}, f=judgability, α=P_epistemic (fixed point 갖는) | **Thm 3 positive** | MEDIUM |
| 2 | TemporalArc functor | T=ℕ, Y=SymposiumHypergraph, **α 부재 (covariant functor)** | Lambek initial algebra가 적합 | LOW |
| 3 | Family-Relation Mirror | T=disciples, Y=positions, α=mirror-op, f=mirror evaluation | **Thm 2 generalized surjection**; 비행기맨만 STRONG | MEDIUM |
| 4 | 재배맨 D1-D7 self-similar | μF (inductive) ↔ νF (coinductive) Lambek 쌍대 | D1 j-operator만 forced (j∘j=j), D2-D7 structural | LOW-MEDIUM |
| 5 | rs-10 Lakatos hard core | T=programmes, Y={T,F}, α=refutation, g=empty | **Thm 1 negative Russell-analogue** | MEDIUM |
| 6 | Harness self-ref paradox | T=agents, Y=capabilities, α=negation, f=coverage | **Thm 1 negative** | **HIGH (기존)** |
| 7 | AirplaneMan.lean j | T=CHU, Y={covered,not}, α=complement, f=coverage | Lawvere-Tierney j-operator 명칭 충돌 (cell B3 verdict pending) | MEDIUM |

→ **5 forced + 5 structural** (cf. consensus C2 partial unification).

## B4 (S4 pitfalls) — 학습 함정

**finding**: `finding-prom16-cat-lawv-B4-pitfalls-2026-05-15` (HIGH)

| # | 함정 | 회피 |
|---|---|---|
| 1 | **Positive vs Negative dual form 혼동** | Lawvere positive (point-surjective → ∀ endo fixed point) ↔ negative contrapositive (no epi → 불가능 정리). M_∞ = Tarski 1955 lattice positive fixed point (Knaster-Tarski), 층 다름 |
| 2 | Trivialism 회피 | Priest LP = dialetheism (일부 모순만 참) ≠ trivialism (모든 명제 참). LP 내부 explosion 차단됨. domain restriction 명시 mandatory |
| 3 | **Lawvere-Tierney j-operator vs Lawvere 1969 FPT 명칭충돌** | j:Ω→Ω는 1971 Tierney 협업 topos topology (sheafification modal). Lawvere 1969 diagonal은 CCC point-surjection. **다른 정리** |
| 4 | Russell ∈-paradox vs Lawvere CCC morphism diagonal 층 mismatch | Russell = set ∈ 층. Lawvere = morphism 층. 같은 diagonal trick의 다른 층. 재배맨 = Russell attribution **금지** |
| 5 | Cantor vs Lawvere dual reading | Cantor diagonal = Lawvere FPT contrapositive. 'bigger infinity' narrative는 비형식적 |
| 6 | Hofstadter informal vs Lawvere formal | GEB strange loop = informal narrative. Yanofsky 2003 BSL 9(3) 측 사후 Lawvere 언어 정전화 |
| 7 | AirplaneMan.lean j 귀속 | cell B3 verdict 대기, 본 cycle 측 단정 불가 |

---

**axis-level synthesis (Consensus C1 + C2 + C6 + Δ1)**:
- Yanofsky 2003 실제 형식 = **4-component (T, Y, f, α)**, NOT 6-tuple → 기존 KG `finding-prom16-harness-B3-yanofsky-2003-2026-05-10` 정정 mandatory.
- positive/negative duality (Thm 1 ↔ Thm 3 contrapositive) = SYMPOSIUM M_∞ ↔ Harness B3 duality의 formal grounding.
- AirplaneMan.lean j-operator 명칭충돌은 rs-9 D1 verdict OPEN.

## Refs

- Yanofsky 2003 arXiv: <https://arxiv.org/abs/math/0305282>
- Yanofsky DOI: <https://doi.org/10.2178/bsl/1058448677>
- Lawvere 1969 TAC reprint 15: <http://tac.mta.ca/tac/reprints/articles/15/tr15abs.html>
- Roberts 2023 Compositionality 5(8): <https://arxiv.org/abs/2110.00239>
- nLab Lawvere FPT: <https://ncatlab.org/nlab/show/Lawvere%27s+fixed+point+theorem>
- Milewski 2019: <https://bartoszmilewski.com/2019/11/06/fixed-points-and-diagonal-arguments/>
- Lawvere FPT Survey 2025: <https://arxiv.org/abs/2503.13536>
- SEP self-reference: <https://plato.stanford.edu/entries/self-reference/>
- Smith Gödel PDF: <https://www.logicmatters.net/resources/pdfs/godelbook/GodelBookLM.pdf>
- SEP dialetheism: <https://plato.stanford.edu/entries/dialetheism/>
- Lawvere-Tierney topology: <https://ncatlab.org/nlab/show/Lawvere-Tierney+topology>

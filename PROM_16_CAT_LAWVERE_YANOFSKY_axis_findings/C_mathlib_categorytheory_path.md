# Axis C — Mathlib4 CategoryTheory.* 학습 경로

> cycle `prom16-category-lawvere-yanofsky-2026-05-15` 측 axis C 측 4 cell.

## C1 (S1 academic-canon) — Mathlib4 CategoryTheory master file list

**finding**: `finding-prom16-cat-lawv-C1-mathlib-canon-2026-05-15` (HIGH)

docs commit `d6dab93da86c64219ab1497ffadce1a66aa04701` 기준 (Mathlib4 release v4.16.0).

| # | 파일 | 역할 |
|---|---|---|
| 1 | `Mathlib/CategoryTheory/Category/Basic.lean` | Category typeclass (id, comp, Epi/Mono) |
| 2 | `Mathlib/CategoryTheory/Functor/Basic.lean` | Functor (F.obj, F.map) |
| 3 | `Mathlib/CategoryTheory/NatTrans.lean` | NatTrans (app field + naturality square) |
| 4 | `Mathlib/CategoryTheory/Functor/Category.lean` | 함자 범주 Cat(C,D) = C ⥤ D (hcomp, associator) |
| 5 | `Mathlib/CategoryTheory/Yoneda.lean` | yoneda fully faithful + yonedaLemma |
| 6 | `Mathlib/CategoryTheory/Adjunction/Basic.lean` | Adjunction (unit/counit, F ⊣ G) |
| 7 | `Mathlib/CategoryTheory/Monad/Basic.lean` | Monad (η, μ) + Comonad |
| 8 | `Mathlib/CategoryTheory/Limits/IsLimit.lean` | IsLimit/HasLimit/HasColimit |
| 9 | `Mathlib/CategoryTheory/Closed/Cartesian.lean` | **CartesianClosed** (Lawvere FPT 선행) |
| 10 | `Mathlib/CategoryTheory/Sites/Grothendieck.lean` | Grothendieck topology (Lawvere-Tierney 대응 언급) |

**중요**: `Mathlib/CategoryTheory/FixedPoints.lean` 측 **부재**. CartesianClosed 선행조건 갖춰졌으나 Lawvere FPT 증명 chain 미완성 — SYMPOSIUM의 standalone 방식 (Harness_LawvereFixedPoint.lean) 유효.

## C2 (S2 learning-order) — 학습 순서 + 시간 견적

**finding**: `finding-prom16-cat-lawv-C2-mathlib-order-2026-05-15` (HIGH)

**7-layer 의존 DAG** (건너뛰기 불가):

| 단계 | 모듈 | 기간 |
|---|---|---|
| 1 | `Category.Basic` (𝟙/≫/⥤/aesop_cat) | 1주 |
| 2 | `Functor.Basic` (F.obj/F.map) | 1주 |
| 3 | `NatTrans` + `Functor.Category` | 1주 |
| 4 | `Types.Basic` + `Products.Basic` (Cᵒᵖ, product) | 0.5주 |
| 5 | `Yoneda` (yoneda : C ⥤ Cᵒᵖ ⥤ Type v) | 1-2주 |
| 6 | `Adjunction.Basic` (F ⊣ G unit/counit) | 1-2주 |
| 7 | `Limits.Basic` → `Closed.Cartesian` → Lawvere FPT | 2-3주 |

**합계: 8-11주 (집중 기준)**.

**4대 장벽**:
1. universe 2-param `(v, u)` 독립 — `Category.{v} C` 명시 패턴 암기 필수
2. `Cᵒᵖ` silent coercion 난독화
3. `aesop_cat` over-trust — 실패 시 `simp + reassoc_of` 수동 fallback
4. **초기 빌드 16GB RAM / 30분 compile** — `lake exe cache get` mandatory

## C3 (S3 symposium-binding) — SYMPOSIUM 133+ Lean theorem Mathlib migration 경로

**finding**: `finding-prom16-cat-lawv-C3-mathlib-symposium-2026-05-15` (HIGH)

**검증된 SYMPOSIUM 내부 선례 2건**:
1. `MIND/lean_formalization/apt_functor_with_mathlib/` — APT_FunctorFactorization Mathlib sister. **628/628 PASS, 0 sorryAx, AXIOMS_AUDIT 완료** (2026-05-14). Classical.choice는 Mathlib transitive 등장하나 비smuggling 판정.
2. `MIND/lean_formalization/temporal_arc_with_mathlib/` — lakefile.toml (Mathlib v4.30.0-rc2 pin) + F_salvation/F_energy Functor + Monotone lemma 완비. 단 `lake update + lake build` 실행 = 사용자 결정 게이트 (`lean-mathlib-functor-actual-build-2026-04-30`).

**파일별 migration 우선순위**:

| 파일 | Mathlib 타겟 | 이득 | 비용 | priority |
|---|---|---|---|---|
| `temporal_arc_with_mathlib/TemporalArcFunctor.lean` | `Functor.Category`, `Preorder` | 실제 Functor 정전 완성 | lake build만 남음 | **P1 (게이트 해제만)** |
| `SpaceGirl_YonedaEmbedding.lean` | `Mathlib.CategoryTheory.Yoneda` | yonedaLemma NatIso 즉시 대체 | 단순 import swap | **P2 (가장 단순)** |
| `Harness_LawvereFixedPoint.lean` | `Mathlib.CategoryTheory.Closed.Cartesian` | diagonal ↔ Lawvere 1969 §4 referee 연결 강화 | 2-element Decision → 일반 CartesianClosed instance lift 필요 | P3 |
| `VoidVibrator_GodelMirror.lean` | `Mathlib/Logic/Basic` | CIC kernel 제약 미해소 | migration 이득 낮음 | P4 (LOW) |

**권장 전략**: `dual maintain` — standalone (0 sorry, 빠른 빌드, 도메인 특수 인코딩) + Mathlib sister (referee transparency 추가). apt_functor_with_mathlib 측 이미 검증된 패턴.

## C4 (S4 pitfalls) — Mathlib4 학습 함정

**finding**: `finding-prom16-cat-lawv-C4-mathlib-pitfalls-2026-05-15` (HIGH)

| # | 함정 | 회피 |
|---|---|---|
| 1 | v4.14 simp config syntax 교체 | `simp +contextual (maxSteps:=N)` 사용; release notes 먼저 확인 |
| 2 | v4.9 well-founded @[irreducible] 기본 → def eq 파괴 | `simp/unfold` 명시 |
| 3 | v4.13 named arg 규칙 변경 | 일부 explicit arg `_` 추가 |
| 4 | inductive `:=` → `where` 이전 | 신규 문법 채택 |
| 5 | Mathlib namespace reorg | `@[deprecated]` 추적, mathlib4_docs 현재 commit 확인 |
| 6 | **lean-toolchain mismatch → cache 무효화** | `lake exe cache clean! && lake exe cache get!` 복구 |
| 7 | universe polymorphism ULift 오류 메시지 불투명 | Zulip 검색; `Category.{v} C` 명시 |
| 8 | AI 어시스턴트 fake-URL hallucination (lesson `lesson-vllm-4b-fake-url-evidence-source-hallucination-2026-05-06`) | 공식 docs 직접 확인 |

**Aesop sorry hiding** 우려는 현재 버전 미확인 — Aesop은 실패 시 error를 내며 sorry placeholder 삽입 X. `warn.sorry` linter 측 v4.22+ 공식 지원.

---

**axis-level synthesis (Consensus C4)**:
- Mathlib4 측 Lawvere FPT 전용 파일 부재 + `CartesianClosed/Yoneda/Adjunction/NatTrans` 정전 import 가능.
- **dual maintain sister sprint 패턴 = SYMPOSIUM 내부 검증된 표준 경로**.
- Path P1 (temporal_arc 사용자 게이트 해제) → P2 (SpaceGirl Yoneda swap) → P3 (Harness CartesianClosed) → P4 (VoidVibrator LOW).
- 8 drift 함정 측 SYMPOSIUM standalone (0 의존) 측 면역 최고 수단; 중장기 sister sprint 병행.

## Refs

- Mathlib4 docs: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/>
- `CategoryTheory.Category.Basic`: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Category/Basic.html>
- `CategoryTheory.Yoneda`: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Yoneda.html>
- `CategoryTheory.Adjunction.Basic`: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Adjunction/Basic.html>
- `CategoryTheory.Closed.Cartesian`: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Closed/Cartesian.html>
- Lean 4 release notes: <https://lean-lang.org/doc/reference/latest/releases/>
- mathlib4 dependency wiki: <https://github.com/leanprover-community/mathlib4/wiki/Using-mathlib4-as-a-dependency>
- learn page: <https://leanprover-community.github.io/learn.html>

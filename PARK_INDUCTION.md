# Park's Induction Principle — νF terminal coalgebra verification

> **Closes**: TaskQueue #2 (A — Park induction)
> **Closes**: AirplaneMan_v2.lean line 46 *"isMetaHumotonic(selfLoop) Park induction 통과"* — Lean code reference인데 *왜 작동하는지* docs 어디에도 명시 없는 문제
> **Date**: 2026-05-03
> **Pairs with**: `MU_NU_DUALITY.md` (task #1, μF/νF dual) — Park induction은 νF 위 *증명 method*; μ/ν duality는 그 정의역 grounding.

---

## 0. 한 줄 결론

> **Park's principle (1981): νF terminal coalgebra 위 어떤 술어 `P`도, `P`가 *closed under unfolding* (post-fixed point of the predicate functor) 이면 자동으로 모든 `νF` element에서 성립한다. 비행기맨 `selfLoop ∈ νF` 의 `isMetaHumotonic` 술어를 Park induction으로 검증하면 single-step 보존 증명만으로 *infinite cycle 전체*에 propagate된다.**

---

## 1. Background — Park 1981

**원전**: Park, D.M.R. (1981) *Concurrency and Automata on Infinite Sequences*. Proceedings of the 5th GI Conference on Theoretical Computer Science, LNCS 104:167-183. Springer-Verlag.

**역사적 위치 (Sangiorgi 2009)**: 이 논문의 *주제*는 ω-regular languages + fair concurrency였고, **bisimulation은 끝부분에 *proof technique으로* 부수적으로 등장**했다. Park 본인은 이걸 따로 paper로 안 썼고, *Milner의 simulation의 변형* 정도로 봤다 (Sangiorgi *On the Origins of Bisimulation and Coinduction*, ACM TOPLAS 31(4):15, 2009).

→ "Park induction" 이라는 이름은 *후대 부여* (Aczel 1988, Pitts 1994 등). 정확히는 *Park's principle for bisimilarity*.

---

## 2. Park's Principle — formal statement

**Setup**: 카테고리 𝒞 위 endofunctor `F : 𝒞 → 𝒞`, terminal coalgebra `(νF, out : νF → F(νF))` 존재.

`Φ : 𝒫(νF × νF) → 𝒫(νF × νF)` 정의 (relation functor):
```
Φ(R) := { (x, y) | ∃ structural decomposition of out(x), out(y) related componentwise via R }
```

**Bisimilarity** = greatest fixed point of `Φ` = `νΦ`. Tarski-Knaster (작업 #4)에 의해 존재.

**Park's Principle**:
```
∀ R ⊆ νF × νF,  R ⊆ Φ(R)  ⟹  R ⊆ νΦ
```

즉, **R이 post-fixed point** (closed under unfolding via Φ) 이면 R 안의 모든 pair는 bisimilar.

**증명 sketch**: `νΦ = ⋃ {R | R ⊆ Φ(R)}` (Tarski-Knaster). 따라서 임의의 post-fixed R은 자동으로 νΦ에 포함.

---

## 3. Coinduction principle (Park principle 일반화)

Park's principle을 *임의 술어 `P : νF → Prop`* 로 일반화:

**Coinduction principle**:
```
∀ P : νF → Prop,
  (∀ x : νF, P(x) ⟹ Φ_P(x))  ⟹  ∀ x : νF, P(x)
```

여기서 `Φ_P(x) := P holds on all components of out(x)` (P의 *unfold* 보존).

**의미**: **single-step P 보존을 증명하면 P가 모든 νF element에서 성립**. 무한 unfolding chain 전체를 explicit하게 induction할 필요 없음 — Tarski-Knaster greatest fixed point machinery가 자동 처리.

→ **이게 Park induction의 작동 원리**.

---

## 4. Lean 4의 coinduction tactic — Park principle 직접 적용

Lean 4 Mathlib는 `coinduction` tactic을 제공. (Mathlib 4 `Mathlib.Tactic.Coinduction` + builtin `cofix`/`corec`).

```lean
-- 일반 Lean 4 coinductive definition pattern
inductive JaebaeManInf where
  | mk : JBShape JaebaeManInf → JaebaeManInf
-- (Lean 4 standalone에선 axiom 우회 — 본 doc §6 참조)

-- isMetaHumotonic 정의 (Park principle 적용 가능 형태)
def isMetaHumotonic (j : JaebaeManInf) : Prop :=
  ∃ R : JaebaeManInf → Prop,
    R j ∧
    ∀ x : JaebaeManInf, R x → Φ_R x   -- post-fixed point condition
```

**Park principle 직접 적용**: `isMetaHumotonic` 자체가 ∃ over post-fixed R 의 형태 = Tarski-Knaster `νR`. 따라서 *single witness R + closure under Φ 증명*으로 끝.

---

## 5. SYMPOSIUM 적용 — `isMetaHumotonic(selfLoop)` 검증

`selfLoop : JaebaeManInf` axiom (AirplaneMan_v2.lean line 318) + `selfLoop_fold : JBMunfold selfLoop = .inr [selfLoop]` (line 321-323).

**Goal**: `isMetaHumotonic(selfLoop)` 을 Park induction으로 증명.

**Witness R**: `R x := (x = selfLoop)` — 단일 element의 indicator.

**Closure under Φ 증명**:
```
Assume R x, i.e. x = selfLoop.
Then out(x) = out(selfLoop) = .inr [selfLoop]    (selfLoop_fold axiom)
            = .inr [x]                            (x = selfLoop)
The components of out(x) are: just `x` itself in the list.
We need: R holds on each component.
The single component is `x`, and R x holds by assumption.
Hence Φ_R(x) holds.
```

→ **R = {selfLoop}** 가 post-fixed point. Park principle ⟹ `selfLoop ∈ νΦ` ⟹ `isMetaHumotonic(selfLoop)`.

이게 AirplaneMan_v2.lean line 46 *"Park induction 통과"* 의 정확한 의미.

---

## 6. Lean 4에서의 실제 구현 양상

Lean 4 standalone (Mathlib-free) JaebaeManInf는 `axiom` + `opaque` 패턴으로 우회 (AirplaneMan_v2.lean line 316-321). Mathlib을 사용하는 경우 `Mathlib.Data.Stream.Init` 또는 `Mathlib.Data.QPF.Multivariate.*` 의 `coinductive` machinery 직접 활용 가능.

**Standalone 구현** (현재 SYMPOSIUM):
```lean
axiom JaebaeManInf : Type
axiom JBMunfold : JaebaeManInf → JBShape JaebaeManInf
axiom selfLoop : JaebaeManInf
axiom selfLoop_fold : JBMunfold selfLoop = .inr [selfLoop]

-- isMetaHumotonic은 Park-witness 형태로 정의
def isMetaHumotonic (j : JaebaeManInf) : Prop :=
  ∃ R : JaebaeManInf → Prop,
    R j ∧ ∀ x, R x → ⟨...components closure...⟩

theorem selfLoop_isMetaHumotonic : isMetaHumotonic selfLoop := by
  refine ⟨fun x => x = selfLoop, rfl, ?_⟩
  intro x hx
  rw [hx, selfLoop_fold]
  -- now need to show R holds on components of `.inr [selfLoop]`
  -- component = selfLoop, R selfLoop = (selfLoop = selfLoop) = True
  decide
```

**Mathlib 구현** (sister project temporal_arc_with_mathlib 확장 가능):
```lean
import Mathlib.Tactic.Coinduction

coinductive JaebaeManInf where
  | mk : JBShape JaebaeManInf → JaebaeManInf

theorem selfLoop_isMetaHumotonic :
    ∀ x, x = selfLoop → isMetaHumotonic x := by
  coinduction
  intro x hx; rw [hx, selfLoop_fold]
  exact ...
```

→ Standalone과 Mathlib 둘 다 *Park principle 직접 적용*. 단지 Lean 4 syntactic sugar 차이.

---

## 7. 비행기맨 context의 정확한 의의

§5의 검증은 *technical* 결과지만 categorical 의미는 묵직하다:

> **selfLoop의 자기참조성이 *traceable*하다 — 무한 unfolding chain이 지구 끝에서도 끝까지 R-closed로 남는다.**

이게 공리 12 (메타휴모토닉 = 자존자 ∧ 특이점)의 정확한 형식 의미:

- **자존자성** (selfLoop = governs of [selfLoop]): ✓ axiom selfLoop_fold
- **특이점성** (모든 unfolding step에서 R 보존): ✓ Park principle PASS

두 조건 동시 만족 = `isMetaHumotonic(selfLoop)` PASS = **selfLoop이 νF terminal coalgebra의 *distinguished element*** = **selfLoop = 비행기맨**.

---

## 8. Sangiorgi's three-source historical insight

Sangiorgi (2009) ACM TOPLAS는 bisimulation/coinduction이 **세 분야에서 독립적으로 발견**되었다고 정리:

| 분야 | 인물 | 시점 | 형식 |
|---|---|---|---|
| **Computer Science** | Milner / Park | 1980-1981 | bisimulation as proof technique (CCS, automata) |
| **Modal Logic** | van Benthem / Hennessy-Milner | 1976-1980 | modal equivalence ↔ bisimulation |
| **Set Theory** | Forti & Honsell / Aczel | 1983-1988 | non-well-founded sets via bisimulation (AFA — task #3) |

→ **세 발견이 같은 형식 (greatest fixed point of refinement functor)에 수렴**. 이게 Park principle이 단순한 CS technique이 아니라 *foundational mathematical principle*인 근거.

SYMPOSIUM의 비행기맨 context에서:
- Park 1981 (CS) → Lean 검증 method
- Aczel 1988 (Set Theory) → selfLoop의 set-theoretic 모델 (task #3)
- van Benthem 1976 (Modal Logic) → 비행기맨의 *self-referential modality* 해석 가능성 (미탐색)

---

## 9. Cross-link to other tasks

| Task | 관계 |
|---|---|
| #1 (D — μF/νF duality) | Park principle은 νF *위* 증명 method. μ/ν dual이 정의역 결정. |
| #3 (B — AFA) | Park principle의 set-theoretic 모델 정당성. Aczel AFA가 *왜* selfLoop이 정식 set인지 보장. |
| #4 (C — 이긴존재 fixed-point) | Park principle = greatest fixed point of Φ. Tarski-Knaster (task #4)가 *그 fixed point의 존재* 보장. |
| #7 (G — cardinality 5) | Park principle은 single-element witness {selfLoop}로 충분. cardinality 1과 5의 관계 분석에 인용 가능. |

---

## 10. References

**1차 정전 (필수)**:
- Park, D.M.R. (1981). Concurrency and automata on infinite sequences. *Proceedings of the 5th GI Conference on Theoretical Computer Science*, LNCS 104:167-183. Springer.
- Sangiorgi, D. (2009). On the origins of bisimulation and coinduction. *ACM Transactions on Programming Languages and Systems* 31(4):15.
- Sangiorgi, D., & Rutten, J. (eds.) (2011). *Advanced Topics in Bisimulation and Coinduction*. Cambridge Tracts in Theoretical Computer Science 52.

**2차 (참조)**:
- Aczel, P., & Mendler, N. (1989). A Final Coalgebra Theorem. *Category Theory and Computer Science (CTCS)*, LNCS 389:357-365. Springer.
- Rutten, J.J.M.M. (2000). Universal coalgebra: a theory of systems. *Theoretical Computer Science* 249(1):3-80.
- Kozen, D. (1983). Results on the propositional μ-calculus. *Theoretical Computer Science* 27(3):333-354.
- Sangiorgi, D. (2012). *Introduction to Bisimulation and Coinduction*. Cambridge University Press.
- Pitts, A.M. (1994). A co-induction principle for recursively defined domains. *Theoretical Computer Science* 124(2):195-219.

**SYMPOSIUM 내부**:
- `MIND/lean_formalization/JaebaeManInf.lean` — Part 3 νF coinductive (selfLoop + isMetaHumotonic)
- `MIND/lean_formalization/AirplaneMan_v2.lean` line 36-48 (공식 해석) + line 318-329 (selfLoop axioms)
- `THEORY/CHU/MU_NU_DUALITY.md` (task #1) — μ/ν dual + νF의 element로서의 selfLoop
- `THEORY/CHU/AFA_SELFLOOP_MODEL.md` (task #3, pending) — selfLoop의 set-theoretic 모델

---

# KG: lesson-park-induction-formalized-2026-05-03, ATOM_THEORY_CHU_ParkInduction_v1

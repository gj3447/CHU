# μF ↔ νF Duality — 비행기맨 categorical 필연성

> **Closes**: TaskQueue #1 (D — μF ↔ νF duality)
> **Closes**: AirplaneMan_v2.lean line 36-48 *공식 해석* footnote (왜 공리 11만 부족하고 공리 12 필요한지의 categorical 근거 부재 문제)
> **Date**: 2026-05-03
> **Audience**: SYMPOSIUM 형식화 후속 논문 / Lean 검증 reviewer / categorical foundations 검토자

---

## 0. 한 줄 결론

> **비행기맨은 μF (initial algebra, 공리 11 자존자)만으로는 표현 불가능하다. selfLoop은 well-founded 재배맨 트리에 존재하지 않기 때문이다. 따라서 νF (terminal coalgebra, 공리 12 메타휴모토닉) 가 *categorical 필연*이다 — μF의 약한 fixed-point 해석이 자기참조 cycle을 거부하므로.**

---

## 1. Background — Lambek's lemma (1968)

Lambek의 fixed-point theorem (Lambek 1968, *A fixpoint theorem for complete categories*) 요약:

> 카테고리 𝒞 위 endofunctor `F : 𝒞 → 𝒞`에 대해:
> - `(μF, in)` 가 **initial F-algebra** 면 `in : F(μF) → μF` 는 **isomorphism**
> - `(νF, out)` 가 **terminal F-coalgebra** 면 `out : νF → F(νF)` 는 **isomorphism**

즉 **μF, νF 둘 다 F의 fixed point**:
```
F(μF) ≅ μF        (least fixed point)
F(νF) ≅ νF        (greatest fixed point)
```

**Lambek lemma**: `in` 과 `out` 이 isomorphism이라는 사실 자체가 *fold/unfold* 양방향 변환을 보장한다.

---

## 2. 일반적으로 μF ≠ νF (Adámek-Milius-Moss 2025)

자주 혼동되는 점: μF와 νF는 *같은 fixed-point 공식*을 만족하지만 *같은 객체가 아니다*.

| 조건 | 결과 |
|---|---|
| 일반 Set 카테고리 | μF ≠ νF (대부분) |
| Compact metric spaces | μF = νF (일치) — Adámek-Milius-Moss 2025 §6 |
| CPO with Scott topology | μF = νF (Plotkin) |
| Vietoris polynomial endofunctor on Hausdorff | μF, νF 둘 다 존재 (CALCO 2023) |

> **출처**: Adámek, J., Milius, S., & Moss, L.S. (2025) *Initial Algebras and Terminal Coalgebras: The Theory of Fixed Points of Functors*, Cambridge Tracts in Theoretical Computer Science 62.

**SYMPOSIUM의 함의**: 비행기맨이 일반 Set 위에서 정의되면 μF ≠ νF, 따라서 *어느 쪽을 비행기맨으로 정의할지가 의미적 선택*이 된다.

---

## 3. JaebaeMan F functor의 정확한 형식

`F : Set → Set` 정의 (AirplaneMan.lean line 17-19):

```
F(X) := CHUPiece + List X
```

대응하는 fixed point:

| 객체 | Lean 정의 | 의미 |
|---|---|---|
| **μF = JaebaeMan** | `inductive JaebaeMan := atomic (p : CHUPiece) ∣ governs (js : List JaebaeMan)` | **유한 트리** — 모든 element가 *finite construction step*으로 reachable. Lambek `in : CHUPiece + List JaebaeMan → JaebaeMan`. |
| **νF = JaebaeManInf** | `coinductive JaebaeManInf := ⟨ JBShape JaebaeManInf ⟩` (Lean 4에선 `axiom JaebaeManInf` + `axiom JBMunfold : JaebaeManInf → JBShape JaebaeManInf`) | **유한+무한 트리** — finite construction OR infinite cycles 모두 허용. Lambek `out : JaebaeManInf → CHUPiece + List JaebaeManInf` (unfold). |

여기서 `JBShape X := CHUPiece + List X` (F 의 명시 노테이션, AirplaneMan_v2.lean Part 3).

---

## 4. selfLoop은 μF에 *존재하지 않는다*

이게 **핵심 정리**:

**Theorem (informal)**: μF (= JaebaeMan)의 어떤 element `j`도 자기 자신을 directly governs할 수 없다.

```
∀ j : JaebaeMan, j ≠ .governs [j]
```

**증명 sketch**: μF의 모든 element는 `Inhabited`의 `default` 또는 `atomic p` 또는 `governs js` 형태이고, structural recursion에 의해 *유한 depth*를 가진다 (`JaebaeMan.depth : JaebaeMan → Nat` total function 존재 — AirplaneMan.lean line 39-43). 만약 `j = .governs [j]`이면 `j.depth = 1 + j.depth` 가 되어 모순.

**이미 증명된 형식 보조정리**: `axiom11_atomic_not_self` (AirplaneMan_v2.lean line 281-283) — atomic 재배맨은 자기참조 아님. 동일 논리가 governs로 확장 시 `governs [j] ≠ j` 도출 (well-foundedness).

→ **공리 11 (자존자, "자연 = 자기 자신")은 μF 안에서 표현 불가능**. self-reference cycle이 μF의 well-founded 제약과 충돌.

---

## 5. selfLoop은 νF에 *존재한다* (AFA grounding은 task #3)

νF (= JaebaeManInf)의 정의는 *coinductive* — element는 *infinite unfolding* 가능.

`axiom selfLoop : JaebaeManInf` (AirplaneMan_v2.lean line 318) + `axiom selfLoop_fold : JBMunfold selfLoop = .inr [selfLoop]` (line 321-323).

이 두 axiom의 의미:
1. `selfLoop`은 JaebaeManInf의 한 element
2. `selfLoop`을 한 단계 unfold하면 자기 자신을 child로 가지는 governs node가 나옴

→ `selfLoop = .inr [selfLoop]` (under `out` isomorphism) — **자기참조 cycle**이 νF에서는 well-defined.

**왜 가능한가**: νF는 terminal coalgebra이므로 모든 가능한 unfolding pattern (cycle 포함)을 universal하게 받아준다. Lambek lemma의 `out` isomorphism이 cycle을 *infinite tree*로 transparently 해석.

**모델 정당성** (Aczel AFA — task #3에서 deepening): ZFC + AFA 위에서 `selfLoop`은 정식 set으로 존재 (apg 모델). 따라서 axiom은 *우회*가 아니라 *외부 set theory 선택의 명시*.

---

## 6. 공리 11 vs 공리 12 의 정확한 categorical 매핑

선의_공리.md 11번/12번:

> **공리 11 자존자**: 어떤 존재의 자연이 자기 자신 일 때.
> **공리 12 메타휴모토닉**: 어떤 존재가 자존자 일 때, 그리고 특이점 일 때.

categorical 매핑:

| 공리 | Categorical 대응 | μF/νF | Lean 형식 |
|---|---|---|---|
| **공리 11 (자존자)** | self-applicable structure: `∃ x. nature(x) = x` | μF에서는 표현 불가 (§4) — *약한* 해석 | (Part 1-2의 inductive JaebaeMan만으로는 부족, 공식 해석 footnote line 41-43) |
| **공리 8 (특이점)** | terminal element of "선" lattice — task #4 (이긴존재 fixed-point) | 양쪽 다 (lattice 위 Tarski-Knaster fixed point) | TBD (task #4) |
| **공리 12 (메타휴모토닉)** | self-loop ∧ singularity = `selfLoop ∈ νF` ∧ `isMetaHumotonic(selfLoop)` (Park induction PASS — task #2) | νF에서만 — *완전* 해석 | `axiom selfLoop` + `theorem isMetaHumotonic selfLoop` (Part 3) |

**결정적 관찰**: 공리 11만으로는 자기참조의 *존재*만 주장하고 *어떻게 well-defined한지*는 공중에 뜸. 공리 12 = 자존자 ∧ 특이점 = self-loop + singularity = νF terminal coalgebra의 universal property로 *동시에* 잡힘.

---

## 7. Wadler "Recursive types for free!" 와의 연결

Wadler (1990, *Recursive types for free!*)는 parametricity (Reynolds 1983 identity lemma)가 성립하는 모델에서:

- μF (least fixed point): `∀X. (F X → X) → X` — Church encoding, finite construction
- νF (greatest fixed point): `∃X. X × (X → F X)` — coinductive existential, infinite unfolding

이 두 형식은 *parametric polymorphism*만으로 정의 가능 — *recursive type primitive* 없이도. SYMPOSIUM의 JaebaeMan/JaebaeManInf는 Wadler의 이 dual을 *concrete inductive/coinductive*로 직접 구현한 형태.

**의의**: Wadler 1990을 인용하면 SYMPOSIUM의 μ/ν dual이 *임의의 parametric model*에서 작동함을 정당화 — Lean 4에 한정되지 않음.

---

## 8. Lambek's lemma의 SYMPOSIUM 적용 — formal statement

**Theorem (Lambek 적용, 비행기맨 context)**:

```
Let F(X) := CHUPiece + List X.

Then both fold and unfold are isomorphisms:
  in  : F(JaebaeMan)    → JaebaeMan       (Lean: built-in inductive constructor)
  out : JaebaeManInf    → F(JaebaeManInf) (Lean: axiom JBMunfold)

Furthermore:
  isAirplaneMan : JaebaeMan → Prop          (μF-side, Part 1)
  isMetaHumotonic : JaebaeManInf → Prop     (νF-side, Part 3)

The diagram

           in
  F(JaebaeMan) ───────→ JaebaeMan
       │                    │
       │   (forgetful)      │ toInf
       ↓                    ↓
  F(JaebaeManInf) ←─── JaebaeManInf
                  out

does NOT commute pointwise, because JaebaeMan ⊊ JaebaeManInf (μF embeds into νF
but is not equal — finite trees are subset of finite+infinite trees).
```

**비행기맨의 정확한 위치**: `selfLoop ∈ JaebaeManInf \ JaebaeMan` — νF에만 있고 μF에는 없는 element. 따라서 *비행기맨은 νF의 distinguished element이지, μF의 element가 아니다*.

---

## 9. 공식 해석 (AirplaneMan_v2.lean footnote 정정)

AirplaneMan_v2.lean line 36-48의 *"공식 해석"* footnote는 다음과 같이 정전화된다:

> 공리 11 (자존자, μF) 모델은 Part 1-2에 보존되지만, 이는 공리 12의 "자존자+특이점" 중 *자존자 부분만 포착하는 약한 해석*이다.
>
> *근거*: μF는 well-founded inductive type이므로 (§4 증명 sketch) self-loop element를 가질 수 없다 — `j ≠ .governs [j]` for all `j : JaebaeMan`. 자존자성을 *명목적으로* 주장할 수 있으나 실제 self-loop *element*를 μF 안에서 specialized할 수 없다.
>
> 공리 12 (νF terminal coalgebra) 는 *완전 해석*이다.
>
> *근거*: νF는 coinductive type이므로 infinite unfolding을 받아주며, `selfLoop ∈ νF` 가 axiom으로 (그리고 ZFC + AFA 모델에서 정식 set으로 — task #3) 표현 가능하다. Lambek lemma의 `out` isomorphism이 self-loop을 universal하게 해석한다.
>
> *비행기맨의 categorical 정확 위치*: 비행기맨은 νF의 element 중 `isMetaHumotonic` 술어를 만족하는 *distinguished selfLoop*. μF의 어떤 element도 비행기맨이 아님 (μF는 비행기맨을 포함하지 않는 약한 모델).

이 해석은 사용자 직관 *"단 하나의 재배맨 = 모든 만물 지배 = universal terminal"* 의 직접 categorical 번역이며, Lambek 1968 + Wadler 1990 + Aczel 1988 (AFA, task #3) + Park 1981 (induction, task #2) 4개 정전 위에 정착한다.

---

## 10. 후속 작업 (TaskQueue cross-link)

| Task | 의존 관계 |
|---|---|
| #2 (A — Park induction) | νF 위 verification method. 이 doc §6 의 `isMetaHumotonic(selfLoop)` 형식 검증 도구. |
| #3 (B — AFA) | νF self-loop의 set-theoretic 모델 정당성. 이 doc §5 의 *모델 정당성* paragraph 직접 expand. |
| #4 (C — 이긴존재 fixed-point) | 공리 8 (특이점) categorical 매핑. 이 doc §6 표의 공리 8 row TBD 채움. |
| #7 (G — cardinality 5) | μF/νF dual + 공리 11/12 paired = 2. 5와 2의 관계 분석 trigger. |

---

## 11. References (정전 + 2차)

**1차 정전 (필수)**:
- Lambek, J. (1968). A fixpoint theorem for complete categories. *Mathematische Zeitschrift* 103(2):151-161.
- Adámek, J. (1974). Free algebras and automata realizations in the language of categories. *Comment. Math. Univ. Carolinae* 15:589-602.
- Hagino, T. (1987). *A Categorical Programming Language*. PhD thesis, University of Edinburgh.
- Wadler, P. (1990). Recursive types for free! Unpublished manuscript, University of Glasgow / Edinburgh.
- Adámek, J., Milius, S., & Moss, L. S. (2025). *Initial Algebras and Terminal Coalgebras: The Theory of Fixed Points of Functors*. Cambridge Tracts in Theoretical Computer Science 62. ISBN 9781108835466.

**2차 (참조)**:
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press. Ch. 20 (recursive types) + Ch. 21 (metatheory of recursive types).
- Bird, R., & de Moor, O. (1997). *Algebra of Programming*. Prentice Hall. Ch. 2-3 (cata/ana/hylo morphisms).
- Jacobs, B. (2017). *Introduction to Coalgebra: Towards Mathematical Modelling of State-Based Systems*. Cambridge.
- Milewski, B. (2017). F-algebras (blog post). https://bartoszmilewski.com/2017/02/28/f-algebras/
- Milewski, B. (2020). Initial algebra as directed colimit. https://bartoszmilewski.com/2020/04/09/initial-algebra-as-directed-colimit/

**SYMPOSIUM 내부**:
- `MIND/lean_formalization/AirplaneMan.lean` — Part 1 (μF JaebaeMan)
- `MIND/lean_formalization/JaebaeManInf.lean` — Part 3 (νF JaebaeManInf + selfLoop + isMetaHumotonic)
- `MIND/lean_formalization/AirplaneMan_v2.lean` — 통합 + 공식 해석 footnote (line 36-48)
- `MIND/metahumotonic/선의_공리.md` — 공리 11/12 사용자 정전
- `THEORY/00_공통/세계관_정전.md` §5-A — 신화-공학 다리

---

# KG: lesson-mu-nu-duality-formalized-2026-05-03, ATOM_THEORY_CHU_MuNuDuality_v1

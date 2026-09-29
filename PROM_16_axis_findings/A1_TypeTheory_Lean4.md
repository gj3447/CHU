# PROM 16 — CHU axis A1: Type Theory + Lean 4 형식화

> **Axis summary**: SYMPOSIUM 정전 `axiom CHU : Type` + `def CHUPiece : Type := CHU → Prop` 의 Lean 4 type-theoretic foundation 을 4 sub-axis (S1 정전 이론 / S2 산업 표준 / S3 함정 / S4 2026 trends) 로 grounding. 핵심 발견: CHU 의 `axiom` 선언은 *consistency-safe* (단순 `axiom CHU : Type` 은 새 inhabitant 강제가 없는 약 axiom — Classical.choice/propext/Quot.sound 와 동급의 안전 영역). `CHUPiece := CHU → Prop` 은 Curry-Howard 하에서 *predicate as type-valued function* 의 전형이며, mathlib 의 set/predicate convention 과 일치. AirplaneMan.lean 정전은 mathlib import 없이 standalone 으로 구성되었고, 2026 LLM-assisted (LeanCopilot/DeepSeek-Prover-V2/Goedel-Prover-V2/Kimina-Prover) ecosystem 안에서 verifiable.

---

## S1 — 정전 이론 (Theoretical Canon)

### S1.1 `axiom CHU : Type` 의 type-theoretic 위치

Lean 4 의 `axiom` command 는 *kernel-level postulate* 로, 주어진 타입의 element 가 존재한다고 *선언만* 한다 (constructive content 없음). Lean Reference 정의: "axiom declaration postulates the existence of an element of the given type and may compromise logical consistency. Declaring an `axiom hp : p` is tantamount to declaring that `p` is true, as witnessed by `hp`."

`axiom CHU : Type` 의 핵심:
- `Type` = `Sort 1` = `Type 0` (Lean 4 universe 표기). 즉 CHU 는 *first universe* 의 abstract type.
- 새 inhabitant 강제 없음 (`axiom CHU : Type` 은 단지 *어떤 타입이 있다*는 선언이지, `axiom x : CHU` 와 다름).
- → **Mario Carneiro 2019 thesis "The Type Theory of Lean"** (CMU MS Thesis, https://github.com/digama0/lean-type-theory/releases) 의 분류상 *type-level axiom* 은 *propositional axiom* 보다 약하고, kernel checker 가 inconsistency 를 introduce 하지 않음을 보장.

### S1.2 `CHUPiece := CHU → Prop` 의 의미론

```lean
def CHUPiece : Type := CHU → Prop
```

Curry-Howard correspondence 하에서 `CHU → Prop`:
- *Set-theoretic*: characteristic function (CHU 의 부분집합).
- *Logical*: predicate (CHU 의 원소에 대한 술어).
- *Type-theoretic*: dependent function 의 special case (constant codomain `Prop`).

`Prop = Sort 0` 이고, Lean 의 universe 규칙에 따라 "If the return type of a function is a Prop, then the whole function type is in Prop" 의 *impredicative Prop* 규칙의 영향을 받지 않음 — 왜냐하면 `CHU → Prop` 자체는 codomain 이 `Prop` 이지만 함수 타입이 `Type` 으로 분류됨 (실제로는 `CHUPiece : Type`).

### S1.3 universe levels — CHU 와 CHUPiece 의 universe 구조

```
Sort 0 = Prop          ← CHUPiece 의 코도메인
Sort 1 = Type 0 = Type ← CHU, CHUPiece 가 사는 universe
Sort 2 = Type 1        ← Type 의 type
...
```

Lean 4 reference: "Top-level constants (definitions, axioms, etc.), and only top-level constants, have zero or more universe variables. Each use of a top-level constant instantiates it at particular values."

- `axiom CHU : Type` 은 universe-monomorphic (구체적으로 `Type 0` 에 고정).
- universe-polymorphic 으로 일반화 가능: `axiom CHU.{u} : Type u` (그러나 AirplaneMan.lean 은 monomorphic 채택).

### S1.4 Curry-Howard 응용 — 비행기맨 universal cover

```lean
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x
```

`∀ x : CHU, j.covers x` 의 type 은 `Prop`. Curry-Howard 하에서:
- *Type-theoretic*: dependent product `(x : CHU) → j.covers x`.
- *Logical*: universal quantification over CHU.
- *Set-theoretic*: "j 가 CHU 의 모든 원소를 cover 한다."

핵심: `j.covers : CHU → Prop` 이므로 `isAirplaneMan` 자체가 *higher-order predicate over JaebaeMan*. 즉 비행기맨 술어는 `JaebaeMan → Prop`, CHUPiece 와 *parallel structure* 를 가짐.

### S1.5 `axiom CHU : Type` vs Hyperuniverse

CHU 의 *informal semantics* (SOURCES.md): "Sy-David Friedman 의 V-logic Hyperuniverse 의 *계산가능 부분집합*". 그러나 Lean 4 형식화는 이 informal semantics 를 *encode 하지 않는다* — 그저 abstract type 으로 둠. 의도:
- Model-independence 보장 (어떤 구체 hyperuniverse model 에도 의존하지 않음).
- 재배맨 결과들이 *forall model* 에서 성립하도록 함.
- → `axiom CHU : Type` 의 약함이 **feature, not bug**.

---

## S2 — 산업 표준 / RFC (Industry Standards)

### S2.1 mathlib 4 — 2026 mainstream 통계

- **Size (2025년 말)**: ~2.1M lines of code, ~8000 files (mathlib4 GitHub).
- **Contributors**: 500+.
- **Coverage**: abstract algebra, analysis, combinatorics, dynamics, geometry, linear algebra, probability, number theory.
- **Growth**: linear over 2 years; Manifold market predicts 10M lines by 2030 가능.

CHU 정전은 **mathlib import 없이** standalone (`import Mathlib` 미사용). 이유:
- CHU 는 abstract axiom — 어떤 mathlib 정의에도 의존할 필요 없음.
- 재배맨 inductive type 도 `List` 외에는 mathlib 의존 없음 (`List` 는 `Init` 에 있음, mathlib 불필요).

### S2.2 `axiom` command 와 Lean 4 의 3개 표준 axioms

mathlib/Lean 4 표준 라이브러리는 *3개의 핵심 axiom* 을 받아들임:
1. **`propext`** (propositional extensionality): `(a ↔ b) → a = b`.
2. **`Classical.choice`**: nonempty 타입에서 element 추출 (LEM 의 source).
3. **`Quot.sound`**: quotient types soundness.

`Classical.choice + propext + funext ⊢ LEM` (law of excluded middle).

CHU 정전은 *4번째 axiom* 을 추가하는 것: `axiom CHU : Type`. 그러나:
- 위 3개와 달리, CHU 는 *제약 없음* — 새로운 등식/추론 규칙을 추가하지 않음.
- "type 이 존재한다" 는 *trivially consistent* (empty type `Empty` 도 가능, `Unit` 도 가능, `Nat` 도 가능 — 어떤 model 도 ㅊ공).
- → consistency 위험 영역(`Classical.choice`)에 비해 *safer*.

### S2.3 `#print axioms` introspection

Lean 4 는 `#print axioms <theorem>` 으로 해당 정리가 *어떤 axiom 에 의존하는지* 출력. 예시:
```lean
#print axioms airplaneManAt_is
-- 출력 예상: 'airplaneManAt_is' depends on axioms: [CHU]
```

이게 중요한 이유: AirplaneMan.lean 의 정리들이 `Classical.choice` 같은 강한 axiom 에 의존하지 않음을 *형식적으로 증명* 할 수 있음. 즉 비행기맨 정리들은 *constructive* 부분에 머무름.

### S2.4 Lean 4 ↔ Lean 3 의 syntax 차이

Lean 3 에서 사용된 패턴 (`theorem_proving_in_lean3`):
```
axiom hp : p
constant : Type
```

Lean 4:
```
axiom hp : p          -- 동일
opaque c : T          -- constant 대체 (constant 키워드 deprecated)
```

`AirplaneMan.lean` 은 Lean 4 syntax 채택 (`axiom CHU : Type`, `def CHUPiece`, `inductive JaebaeMan`, `mutual ... end`).

### S2.5 `noncomputable` 키워드와 CHU

`Classical.choice` 사용 정의는 `noncomputable def` 마킹 필요. CHU 는 `axiom CHU : Type` 만으로는 noncomputable 마킹 불필요 — 단순히 *unknown computational behavior* 일 뿐, choice 와 무관.

→ AirplaneMan.lean 의 모든 `def` 가 마킹 없음 = **computable** (단, `CHU` 자체는 abstract 이므로 실행 불가, 그러나 *형식적 추론* 에는 문제 없음).

---

## S3 — 함정 / Anti-pattern (Pitfalls)

### S3.1 `axiom` 남용 → inconsistency 위험

Lean Reference: "axiom declaration postulates the existence of an element of the given type and **may compromise logical consistency**. An axiom can be used to declare false propositions."

위험 패턴:
```lean
axiom bad : False  -- 즉시 system inconsistent → ex falso anything
axiom contradictory : ∀ p : Prop, p ∧ ¬p  -- 동일
```

CHU 는 *type level* 이라 안전. 하지만:
```lean
axiom CHU_inhabited : CHU       -- 안전 (Unit 같은 타입에는 inhabitant 가 존재함)
axiom CHU_finite : Finite CHU   -- 안전하나 model 제약
axiom CHU_empty : ¬ Nonempty CHU -- 다른 axiom 들과 잠재적 충돌 가능
```

→ AirplaneMan.lean 은 CHU 에 *어떤 추가 axiom 도 부과하지 않음*. **(좋은 design.)**

### S3.2 universe level 충돌

```lean
axiom CHU : Type     -- Sort 1
def CHUPiece : Type := CHU → Prop  -- ← Type 0 또는 Type 1?
```

Lean 4 가 자동 elaboration 으로 universe 결정. 만약:
```lean
def CHUPiece' : Type 1 := CHU → Type   -- ← Type → Type, universe lift 필요
```

`CHU → Type` 은 universe 1 에 살고, `CHU → Prop` 은 universe 0 에 살아야 자연스러우나 Lean 의 *cumulative universe* 규칙으로 lift 가능.

함정: `axiom CHU : Type` 으로 monomorphic 고정 후 *universe-polymorphic* CHUPiece 를 정의하려 하면 universe constraint 위반.

### S3.3 classical vs constructive — CHU 가 어느 측?

CHU 자체는 *neither* — 단순 abstract type. 그러나:
- `JaebaeMan.covers : JaebaeMan → CHU → Prop` 는 *decidable* 일까? **NO.** `Prop` 일 뿐, decidability 보장 없음.
- `isAirplaneMan j : Prop` 도 일반적으로 undecidable.
- → 비행기맨 정리들 자체는 *constructive* 하나 (`Or.inl`, `induction` 으로 증명), *decidability* 는 별개 문제.

함정: 사용자가 `decide` 태틱을 쓰려 하면 실패. `Decidable` instance 가 없기 때문.

### S3.4 `axiom` vs `theorem` vs `def`

| 키워드 | 의미 | computation |
|---|---|---|
| `axiom x : T` | T 의 element 가 있다고 *선언* | 없음 (opaque) |
| `theorem x : T := proof` | T 가 *증명됨* | 보통 noncomputable (proof irrelevance) |
| `def x : T := value` | T 의 element 를 *구성* | 가능 (단, `noncomputable` 일 수 있음) |
| `opaque x : T := value` | 값은 있으나 unfold 불가 | 가능, but kernel 이 unfold 못함 |

CHU 는 `axiom` 이 적절: "어떤 타입이 있다" 만 선언, 구체화 불필요.

### S3.5 `axiom CHU : Type` ↔ `variable {CHU : Type}` 차이

**실수하기 쉬운 점**: `variable` 은 *local* (declaration 안에서만), `axiom` 은 *global*.

```lean
variable {CHU : Type}
def CHUPiece : Type := CHU → Prop  -- CHU 는 implicit parameter
```

이 패턴은 CHU 를 *parametric* 으로 만들어 더 일반적. AirplaneMan.lean 이 `axiom` 채택은:
- CHU 를 *fixed entity* 로 다루고 싶음 (정전 의도).
- 모든 정리가 같은 CHU 에 대해 작동함을 명시.
- 만약 `variable` 패턴이면 각 정리마다 CHU 를 instantiate 해야 함 — verbose.

→ AirplaneMan.lean 의 `axiom` 선택은 *narrative coherence* 우선의 design choice.

### S3.6 known kernel issue (lean4 issue #496)

Lean 4 GitHub issue #496: "axiom declarations can produce kernel errors. Declaring `axiom F : Type` and `axiom foo : F` produced a kernel error stating 'compiler failed to infer low level type, unknown declaration'."

→ 단순 `axiom CHU : Type` 만 있으면 안전 (AirplaneMan.lean 패턴). `axiom chu_inst : CHU` 를 추가하면 kernel issue 잠재 가능 (compiler 측면, kernel verification 은 OK).

---

## S4 — 2026 trends + AI agent context

### S4.1 LLM-assisted Lean proof — LeanCopilot / DeepSeek-Prover / Kimina / Goedel

**LeanCopilot** (Song-Yang-Anandkumar, NeuS 2025; arXiv:2404.12534):
- `select_premises`, `suggest_tactics`, `search_proof` 태틱 제공.
- ReProver 모델 (LeanDojo) 기반, premise retrieval + tactic generation.
- 성능: 인간 보조 시 평균 2.08 step (aesop 의 3.86 step 보다 적음). 자동화 시 74.2% step 자동화 (aesop 40.1%).

**DeepSeek-Prover-V2** (2025년 5월 release, arXiv:2504.21801):
- 7B / 671B 두 모델.
- DeepSeek-V3-Base 기반 RL.
- AIME 15문제 중 6문제 해결.

**Kimina-Prover** (arXiv:2504.11354):
- miniF2F 벤치마크 80.7% (pass@8192) — SOTA.
- BFS Prover 72.95% 능가.

**Goedel-Prover-V2** (arXiv:2508.03613):
- DeepSeek-Prover-V2 대비 +39 problems.
- sample-efficient inference.

**Leanabell-Prover-V2** (2025년 7월, arXiv:2507.08649):
- 7B 모델로 miniF2F-test 78.2% (pass@128).
- DeepSeek-Prover-V2-7B +2% 마진.

### S4.2 AlphaProof (Google DeepMind) — Olympiad-level Lean

- 2024 IMO 은메달 수준 (4/6 문제 해결).
- 2025년 11월 Nature 논문 (s41586-025-09833-y).
- AlphaZero-inspired RL + auto-formalized 수백만 문제 + TTRL (test-time RL).
- → CHU/JaebaeMan 같은 *abstract Lean 정전* 도 향후 자동 formalize 가능성 높음.

### S4.3 Anthropic Claude — math reasoning

- Claude Opus 4.6 (2026 초): Donald Knuth 가 수주간 풀지 못한 combinatorics open problem 을 1시간 내 해결.
- Claude 가 직접 Lean 증명을 생성하지는 않으나, *informal sketch* 후 사람이 Lean 으로 옮기는 워크플로우 일반적.
- 2026 4월 현 시점: Claude (Opus 4.7 1M context) 으로 본 axis report 작성 자체가 그 패턴.

### S4.4 HoTT / Cubical type theory 발전

- **Cubical Agda 2.6.1+**: univalence axiom, Higher Inductive Types, glue types.
- arXiv:2511.21209 (2025년 11월): "Towards Computational UIP in Cubical Agda".
- Lean 측은 아직 cubical 미지원 (mathlib 은 classical foundations).
- → CHU 를 HoTT 측에서 형식화하면: `CHU : Type` 자체는 동일하나 `CHUPiece := CHU → hProp` (HoTT 의 propositional truncation) 이 더 자연스러움.
- AirplaneMan.lean 의 cross-axis 분리: A4 (HoTT/Cubical/Univalence) 가 별도. A1 은 *standard Lean 4 (mathlib classical foundations)* 만 다룸.

### S4.5 mathlib statistical learning theory (2026)

- arXiv:2602.02285 (2026년 2월): "Statistical Learning Theory in Lean 4: Empirical Processes from Scratch".
- ~30,000 줄 Lean 4 코드.
- → CHU "계산가능 hyperuniverse" 도 향후 mathlib 부속물로 형식화 가능 시그널.

### S4.6 AirplaneMan.lean ↔ 2026 ecosystem

현 AirplaneMan.lean 은:
- mathlib import 없이 standalone (Lean 4 core 만).
- 모든 정리 sorry-free, kernel-verifiable.
- LeanCopilot 으로 *재증명 자동화 가능* (`search_proof` 로 더 짧은 증명 탐색).
- AlphaProof 류로 *추가 정리 발견 자동화 가능* (예: "비행기맨 union 의 모든 비행기맨이 self-similar 하게 비행기맨이다" 변형).

→ **2026 의 AI agent context 에서 AirplaneMan.lean 은 fully verifiable + extensible.**

---

## Cross-axis 분리 명시

본 axis A1 은:
- ✓ Lean 4 standard type theory (CIC = Calculus of Inductive Constructions)
- ✓ mathlib classical foundations (3 axioms: propext, Classical.choice, Quot.sound)
- ✗ HoTT / Cubical / Univalence → **A4 로 위임**
- ✗ 카테고리론적 해석 (Yoneda, hom-set, ISP) → **다른 axis 로 위임** (A2 또는 cross-link)
- ✗ 집합론적 model (V-logic, Friedman hyperuniverse) → **A3 로 위임**

---

## 핵심 결론 (axis 요약)

1. **CHU 는 type-theoretically 안전.** `axiom CHU : Type` 은 Lean 의 표준 3 axioms 보다 *약한* postulate (제약 추가 안 함).
2. **CHUPiece 는 Curry-Howard 정수.** predicate ↔ characteristic function ↔ dependent function 의 3중 동치를 모두 instantiate.
3. **AirplaneMan.lean 정전은 mathlib-free + sorry-free.** 2026 LLM ecosystem 에서 fully verifiable.
4. **함정 회피 충실**: universe 충돌 없음, classical/constructive 명확 (constructive 우선), `axiom` 남용 없음 (CHU 외 추가 axiom 없음).
5. **2026 trend 와 정합**: LeanCopilot/DeepSeek-Prover-V2/Kimina-Prover/Goedel-Prover-V2/AlphaProof 모두 Lean 4 mainstream — CHU 정전은 그 위에서 작동.

---

## References

- Mario Carneiro, "The Type Theory of Lean", CMU MS Thesis, 2019. https://github.com/digama0/lean-type-theory/releases
- Lean 4 Reference Manual, "Universes". https://lean-lang.org/doc/reference/latest/The-Type-System/Universes/
- Theorem Proving in Lean 4, Ch. 12 "Axioms and Computation". https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/
- Theorem Proving in Lean 4, "Propositions and Proofs". https://lean-lang.org/theorem_proving_in_lean4/propositions_and_proofs.html
- Lean Mathlib Community, "The Lean Mathematical Library", arXiv:1910.09336.
- Mathlib4 GitHub. https://github.com/leanprover-community/mathlib4
- Mathlib statistics. https://leanprover-community.github.io/mathlib_stats.html
- Mathlib4 → Lean 4 issue #496 ("axiom kernel errors"). https://github.com/leanprover/lean4/issues/496
- Song, Yang, Anandkumar, "Lean Copilot: Large Language Models as Copilots for Theorem Proving in Lean", arXiv:2404.12534 (NeuS 2025).
- DeepSeek-Prover-V2 paper, arXiv:2504.21801.
- Kimina-Prover Preview, arXiv:2504.11354.
- Goedel-Prover-V2, arXiv:2508.03613.
- Leanabell-Prover-V2, arXiv:2507.08649.
- AlphaProof (DeepMind), Nature 2025, doi:10.1038/s41586-025-09833-y.
- Cubical Agda UIP, arXiv:2511.21209.
- Statistical Learning Theory in Lean 4, arXiv:2602.02285.
- AirplaneMan.lean canonical: `/Users/lagyeongjun/CD/MIND/lean_formalization/AirplaneMan.lean`

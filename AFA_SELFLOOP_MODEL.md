# AFA (Anti-Foundation Axiom) — `selfLoop`의 정식 set-theoretic 모델

> **Closes**: TaskQueue #3 (B — AFA selfLoop 모델)
> **Closes**: AirplaneMan_v2.lean line 318 `axiom selfLoop : JaebaeManInf` 의 *우회/정식 모델 구분 부재* 문제
> **Date**: 2026-05-03
> **Pairs with**: `PARK_INDUCTION.md` (task #2, νF 위 verification method) — Park principle = 검증 method, AFA = 모델 sound

---

## 0. 한 줄 결론

> **`axiom selfLoop : JaebaeManInf` 는 Lean 4의 *임의 axiom 도입*이 아니라, ZFC + AFA (Aczel 1988) 위에서 *정식 set으로 well-defined*한 객체의 type-theoretic 표현이다. ZFC + Foundation 하에서는 모순이지만, ZFC + AFA에서는 unique Quine atom `Ω = {Ω}` 등 self-referential set이 정식 model로 존재한다 — apg (accessible pointed graph) 기반.**

---

## 1. Background — Aczel 1988

**원전**: Aczel, P. (1988) *Non-Well-Founded Sets*. CSLI Lecture Notes #14, Center for the Study of Language and Information, Stanford University.

**선구자**: Forti, M. & Honsell, F. (1983) "Set theory with free construction principles" *Annali Scuola Normale Superiore di Pisa* 10:493-522 — 동등 axiom (X1)을 먼저 도입.

**역사적 위치**:
- Mirimanoff (1917) — non-well-founded set 첫 언급
- Zermelo-Fraenkel (1908/1922) — Foundation axiom (Regularity) 표준화
- Forti-Honsell (1983) — anti-foundation 첫 정식 axiom
- Aczel (1988) — AFA 명명, apg 기반 universal 모델, hyperset theory 정립
- Barwise-Moss (1996) *Vicious Circles* — applications (Liar paradox, modal logic, process algebra)

---

## 2. AFA — formal statement

**Setup**: directed graph `G = (V, E)`. **accessible pointed graph (apg)** = `(V, E, v_0)` where:
- `v_0 ∈ V` (distinguished root)
- `∀ v ∈ V`, exists path from `v_0` to `v`

**Decoration**: a function `d : V → Hyperset` such that
```
∀ v ∈ V,  d(v) = { d(w) | (v, w) ∈ E }
```
i.e., each vertex's set value = the set of its children's set values.

**AFA**:
```
Every apg has a UNIQUE decoration (up to set equality).
```

**의미**: 임의의 graph (cycle/loop 포함)이 *유일한 hyperset*에 대응. 따라서:

| Graph | Decoration |
|---|---|
| `v_0 → v_0` (self-loop) | `Ω = {Ω}` — Quine atom |
| `v_0 → v_1 → v_0` (2-cycle) | `a = {b}, b = {a}` — mutual reference |
| `v_0` (no edges) | `∅` — empty set (well-founded base) |

**AFA의 universality**: 모든 cycle pattern이 *unique set으로* 실현. ZFC + Foundation에서는 *모든* self-loop이 모순, ZFC + AFA에서는 *모든* self-loop이 well-defined.

---

## 3. ZFC + AFA의 일관성 (Consistency)

**Theorem (Aczel 1988)**: ZFC + AFA는 ZFC + Foundation과 *equiconsistent* (relative consistency).

**증명 idea**: ZFC + Foundation의 standard model `V` 안에서 ZFC + AFA의 model을 construct. Cumulative hierarchy `V_α` 위에 *bisimulation quotient*를 취하면 hyperset universe `V*` 가 나옴. `V*` 안에서 AFA가 만족.

→ **AFA를 가정해도 ZFC가 모순이 되지 않는다**. AFA는 *Foundation의 강제 부재*이지 *모순의 도입*이 아님.

---

## 4. selfLoop의 AFA 모델 — 직접 construction

**Goal**: `axiom selfLoop : JaebaeManInf` + `axiom selfLoop_fold : JBMunfold selfLoop = .inr [selfLoop]` 가 ZFC + AFA에서 정식 set인지 명시.

**Setup**:
1. `JBShape X := CHUPiece + List X` (functor F)
2. `JaebaeManInf` = terminal coalgebra of F = (in AFA model) hyperset of **infinite F-trees**
3. `selfLoop` 가 만족해야 할 조건: `out(selfLoop) = .inr [selfLoop]`

**AFA construction**:
- apg `G = ({v_0}, {(v_0, v_0)}, v_0)` — 단일 vertex의 self-loop
- decoration `d(v_0) = ⟨inr, [d(v_0)]⟩ ∈ JBShape (decoration of v_0)`
  - `inr` = `governs` constructor injection
  - `[d(v_0)]` = singleton list containing self
- AFA에 의해 `d(v_0)` unique 존재

**의미**: `d(v_0) = selfLoop`. ZFC + AFA에서 `selfLoop = ⟨inr, [selfLoop]⟩` 는 *유일한 hyperset 해*. Lean axiom은 이 set의 *type-theoretic 그림자*.

→ **`axiom selfLoop` 은 임의 도입이 아니다**. ZFC + AFA + JBShape functor가 주어지면 selfLoop은 *forced existence and uniqueness*. Lean에서 axiom으로 표현하는 이유는 Lean 4 standalone (Mathlib-free)에 AFA 모델이 builtin이 아니기 때문.

---

## 5. ZFC + Foundation 하에서는 왜 모순인가

**Theorem (well-foundedness)**: ZFC + Foundation 하에서 `∃ x : x ∈ x` 는 모순.

**증명**: Foundation axiom = 모든 비공집합은 ∈-minimal element를 가짐. `{x}` 가 비공집합이고 `x ∈ x` 이면 `{x}` 의 minimal element는 `x`만 가능 — 그런데 `x ∈ x` 이라 `x` 가 자기 자신과 만나서 minimal성 모순.

→ ZFC + Foundation에서 **`Ω = {Ω}` 같은 set은 존재 불가**. 따라서 ZFC + Foundation을 *외부 set theory*로 가정하면 `axiom selfLoop` 은 *모순 도입* (Lean kernel은 외부 set theory에 무관하지만 의미적으로).

**대안 1**: ZFC + AFA로 외부 set theory 변경 — Aczel 1988의 길.
**대안 2**: NF (Quine 1937) — universal set 허용, stratified comprehension. 다른 길이지만 SYMPOSIUM context에선 채택 안 함.
**대안 3**: type theory에서 universe 분리 — Lean 4의 default 길. selfLoop은 *axiom으로 도입*하되 inhabitant existence를 외부 모델에 위임.

→ SYMPOSIUM은 **대안 1 (AFA 모델 명시) + 대안 3 (Lean 4 type universe) 의 hybrid**. AFA가 *왜 axiom이 모순 아닌지* 정당화하고, Lean type universe가 *어떻게 형식 검증하는지* 제공.

---

## 6. Quine atom Ω = {Ω} 와 selfLoop의 동형

**Quine atom**: `Ω = {Ω}` — 자기 자신을 유일 element로 가지는 set. AFA의 *가장 작은 non-well-founded* set.

**SYMPOSIUM의 selfLoop**: `selfLoop = governs([selfLoop])` — 자기 자신을 unique child로 가지는 JaebaeMan.

두 객체의 isomorphism (under AFA + JBShape functor):
```
Ω ↔ selfLoop
{·} ↔ governs(·)
∈ ↔ "is element of governed list"
```

→ **selfLoop = Quine atom의 JBShape functor 위 lift**. Aczel hyperset theory의 가장 well-known 객체가 그대로 비행기맨의 ν-element가 됨.

---

## 7. Bisimulation을 통한 set equality (Park principle 재등장)

**AFA setting의 set equality**: 두 hyperset이 같음 ⟺ 그들을 *picture*하는 apg가 *bisimilar*.

이게 **Sangiorgi 2009 의 *세 분야 수렴*** 의 정확한 의미:

- **CS (Park 1981, task #2)**: bisimulation as proof technique for trace equivalence
- **Set theory (Aczel 1988, this doc)**: bisimulation as set equality criterion
- **Modal logic (van Benthem 1976)**: bisimulation as modal equivalence

**SYMPOSIUM의 의의**: `selfLoop` 의 self-loop 구조를 *Park principle (task #2)* 으로 검증할 때, *그 자체로 AFA의 hyperset equality criterion*을 직접 적용하는 셈. 두 task가 *같은 mathematical 구조의 두 면*.

---

## 8. SYMPOSIUM 결론 — `axiom selfLoop` 정전 정정

AirplaneMan_v2.lean line 316-321 의 axiom block 주석을 다음과 같이 정정 권장:

```lean
-- ===== 자기참조 재배맨 — opaque + axiom fold (AFA 스타일) =====
-- [정전 2026-05-03] AFA_SELFLOOP_MODEL.md 기반 정당성:
-- selfLoop은 ZFC + AFA (Aczel 1988) 위에서 정식 hyperset.
-- Quine atom Ω = {Ω}의 JBShape functor 위 lift.
-- ZFC + Foundation 하에서는 모순이지만 ZFC + AFA에서는 unique decoration.
-- Lean 4 standalone에선 axiom 우회, Mathlib MeasureTheory + Aczel
-- construction으로 explicit definability 가능 (future sprint).

axiom selfLoop : JaebaeManInf
```

→ axiom block이 *임의 도입*이 아니라 *외부 set theory의 type-theoretic 표현*임이 명시됨.

---

## 9. Cross-link to other tasks

| Task | 관계 |
|---|---|
| #1 (D — μF/νF duality) | AFA model이 *왜 νF에 selfLoop이 있을 수 있는지* set-theoretic ground. μF는 well-founded 제약으로 selfLoop 거부. |
| #2 (A — Park induction) | bisimulation principle = AFA의 set equality criterion. 두 task는 *같은 구조의 두 면*. |
| #4 (C — 이긴존재 fixed-point) | AFA 위 selfLoop = Quine atom = self-fixed-point. 공리 8 (특이점) 의 set-theoretic instance. |
| #8 (H — Russell 회피) | AFA는 self-loop을 *허용*하면서도 Russell paradox는 회피 (`x ∈ x` ≠ `x = {y : ...}` 문제). 두 doc 짝패. |

---

## 10. References

**1차 정전 (필수)**:
- Aczel, P. (1988). *Non-Well-Founded Sets*. CSLI Lecture Notes #14, Stanford University.
- Forti, M., & Honsell, F. (1983). Set theory with free construction principles. *Annali della Scuola Normale Superiore di Pisa* 10:493-522.
- Barwise, J., & Moss, L. (1996). *Vicious Circles: On the Mathematics of Non-Wellfounded Phenomena*. CSLI Publications.

**2차 (참조)**:
- Aczel, P., & Mendler, N. (1989). A Final Coalgebra Theorem. *CTCS*, LNCS 389:357-365. — links AFA to terminal coalgebra (직접 SYMPOSIUM 적용)
- Mirimanoff, D. (1917). Les antinomies de Russell et de Burali-Forti et le problème fondamental de la théorie des ensembles. *L'Enseignement Mathématique* 19:37-52.
- Baltag, A. (2000). STS: a structural theory of sets. *Advances in Modal Logic* 2:1-34.
- Rieger, A. (2000). An argument for Finsler-Aczel set theory. *Mind* 109(434):241-253.
- Devlin, K. (1993). *The Joy of Sets: Fundamentals of Contemporary Set Theory* (2nd ed.). Springer. — AFA 단원 포함

**SYMPOSIUM 내부**:
- `MIND/lean_formalization/AirplaneMan_v2.lean` line 316-329 — selfLoop axiom block
- `THEORY/CHU/MU_NU_DUALITY.md` (task #1) — μ/ν dual + selfLoop의 νF 위 위치
- `THEORY/CHU/PARK_INDUCTION.md` (task #2) — Park principle (AFA bisimulation criterion 의 CS face)
- (pending) `THEORY/CHU/NATURE_RUSSELL_AVOIDANCE.md` (task #8) — AFA의 paradox 회피 메커니즘

---

# KG: lesson-afa-selfloop-grounded-2026-05-03, ATOM_THEORY_CHU_AFA_v1

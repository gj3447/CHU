# PROM_16 / CHU / A3 — Computability + Realizability

> **Worker**: prom16-chu-a3-haiku-2026-04-29
> **Axis**: A3 — CHU 의 *계산가능성* 측면 (Friedman V-logic + Realizability + Effective topos)
> **Output**: 4 sub-axis findings (S1~S4) + JSON cells

CHU = **Computable** Hyperuniverse. "Computable" 키워드의 학술적 lineage 와 그 함의를 정리. 사용자 정전 (`AirplaneMan.lean`) 의 `axiom CHU : Type` 을 *계산가능* 측면에서 어떻게 닫을지 — 또는 열어둘지 — 검토.

---

## S1 — 정전 이론: Friedman Hyperuniverse + Realizability lineage

### S1.1 Friedman Hyperuniverse Programme (정전)

- **시조 논문**: Arrigoni-Friedman 2013, *"The hyperuniverse program"*, *Bull. Symbolic Logic* 19(1):77–96. ZFC 너머의 set-theoretic truth 후보를 *justifiable principles* 로 좁히는 방법론.
- **구성원 4인**: Antos, Friedman, Honzik, Ternullo. 2018 단행본 *The Hyperuniverse Project and Maximality* (Springer, ISBN 978-3-319-62934-6) 가 표준 reference.
- **Hyperuniverse 정의**: 가산(countable) transitive ZFC 모델 전체의 collection. ZFC 너머이지만 *meta-theory* (보통 ZFC + inaccessibles) 안에서 다룰 수 있는 well-defined object.
- **V-logic** (Antos-Friedman et al. 2015 "Multiverse Conceptions in Set Theory", *Synthese* 192(8):2463–2488): infinitary logic with κ-many constants + symbol V denoting the universe. V-logic multiverse = collection of all *outer models* of V. **Hyperuniverse 의 countability constraint 를 우회하는 확장 framework**.
- **John Templeton Foundation** funded the project Jan 2013 – Sep 2015.

### S1.2 Computability theory 정전

- **Turing 1936**: "On Computable Numbers, with an Application to the Entscheidungsproblem" — Turing machine, Church-Turing thesis 의 한 축.
- **Kleene 1952**: *Introduction to Metamathematics* — partial recursive functions, μ-recursion, normal form theorem.
- **Rogers 1967**: *Theory of Recursive Functions and Effective Computability* — RE/decidable/Turing degrees 표준 reference.

### S1.3 Realizability lineage (BHK → Kleene → Hyland)

1. **Kleene 1945**: "On the interpretation of intuitionistic number theory" — *number realizability* `n realizes φ` ∈ HA. 자연수 코드가 증명을 *실현*.
2. **BHK interpretation** (Brouwer 1908+, Heyting 1930s, Kolmogorov 1932; first canonical statement Heyting 1956): proof-as-construction. Realizability = BHK 의 형식화 (proof → realizer).
3. **Hyland 1982**: "The effective topos" in *L.E.J. Brouwer Centenary Symposium* (North-Holland), pp. 165–216. Kleene's first algebra (PCA on ℕ) 위에서 elementary topos `Eff` 구성. 내부 logic = HOL + intuitionistic + DC. Eff 내부에서는 *모든 함수가 computable*.
4. **Weihrauch 2000**: *Computable Analysis* (Springer). Type-2 Theory of Effectivity (TTE) — `ℕ^ℕ` 위 oracle Turing machine. Computability ⊃ continuity (continuity = computability with oracle).

### S1.4 CHU 정전 mapping

| MIND/lean_formalization | Friedman/Hyland 정전 |
|---|---|
| `axiom CHU : Type` | Hyperuniverse element type (countable transitive ZFC model 또는 V-logic outer model) |
| `CHUPiece := CHU → Prop` | Eff 내부 subobject classifier 로의 morphism (재배맨 cover = realizable predicate) |
| `JaebaeMan.atomic / governs` | Kleene tree of realizers — atomic = single realizer, governs = disjunction of realizers |
| `isAirplaneMan := ∀x:CHU, j.covers x` | `Eff ⊨ ∀x:CHU. ∃n. n realizes (x ∈ piece(j))` — 계산가능 cover |

→ **CHU 의 "C" = Computable = Realizable** 해석은 학술적으로 자연스러움. Lean 4 axiom 위에 effective topos semantics 를 부여하면 metahumotonic 의 *hyperuniverse* 와 *computable* 두 키워드가 동시에 닫힌다 (조건부).

---

## S2 — 산업 표준 / RFC

### S2.1 증명보조기 ecosystem (2026-04 현재)

- **Lean 4** (Microsoft Research, de Moura): mathlib 2025-05 기준 **210,000+ theorems, 100,000+ definitions** 포부. CHU 정전이 Lean 4 로 작성됨 (`AirplaneMan.lean`).
- **Rocq** (formerly Coq): 2023-10-11 발표, **Rocq 9.0 정식 release 2025-03**. Calculus of Inductive Constructions. CIC 가 BHK 정전의 type-theoretic 화신.
- **Agda**: dependent types + cubical mode. CHU 형식화 후보 — 그러나 사용자는 Lean 4 채택.
- **Babel-formal** (2024+): Lean ↔ Rocq translation tooling. CHU axiom 을 두 ecosystem 에 모두 표현 가능하게 함.

### S2.2 Effective topos 변종 표준

- Hyland 1982 가 표준. 변종:
  - **Maietti-Rosolini predicative effective topos** (arXiv:1806.08519, 2018+): impredicative power object 회피.
  - **Realizability topos over arbitrary PCA**: Kleene's first algebra (ℕ + Turing) 외 λ-calculus, BSS, untyped λ, quantum PCA 등.
- **Constructive type theory**: Coq/Rocq CIC, Lean 4 CIC variant, Agda MLTT — 모두 BHK 의 instance.

### S2.3 Constructive reverse mathematics (CRM)

- **Veldman** (Netherlands) + **Ishihara** (JAIST) 가 2000 전후 독립 시작.
- 표준 textbook: **Diener-Ishihara 2021** *"Bishop-Style Constructive Reverse Mathematics"* (Springer chapter).
- **Handbook of Constructive Mathematics** (Bridges-Ishihara-Rathjen-Schwichtenberg eds.) — 종합 reference.
- BISH 위에 어떤 원리(LEM, MP, BD-N, ...)를 더해야 정리 X 가 증명되는지 분류. **CHU 가 BISH 인지 CLASS 인지 INT 인지가 open question**.

### S2.4 Computability 정의 다중성 (RFC-적 합의 부재)

- Turing machine (표준)
- λ-calculus / SK combinator (Church-Rosser)
- partial recursive functions (Kleene normal form)
- BSS machine (Blum-Shub-Smale, real number computability)
- Quantum Turing machine (BQP)
- Type-2 effectivity (Weihrauch, oracle on `ℕ^ℕ`)

→ **사용자 정전이 "Turing 표준" 을 명시 채택해야** CHU 의 "C" 가 닫힌다. 미명시 시 다중 해석 충돌.

---

## S3 — 함정 / Anti-pattern

### S3.1 Lean 4 `axiom` 은 계산가능성을 보장하지 *않는다*

`axiom CHU : Type` 은 단순한 type 선언이고, 어떤 *computational content* 도 강제 안 함. Lean 4 에서:

```lean
axiom CHU : Type           -- 단순 type, computable 보장 X
axiom magic : CHU          -- noncomputable 자동
def f : CHU → ℕ := ...    -- noncomputable def 강제될 가능성
```

**함정**: "axiom CHU 라고 썼으니 CHU 가 계산가능하다" 는 잘못된 추론. 실제로는 `noncomputable def` issue 를 우회하려면 별도 `Computable` typeclass instance 가 필요.

### S3.2 Excluded middle 사용 시 constructive content 손실

Lean 4 stdlib 의 `Classical.choice`, `Classical.em` 사용 시 `noncomputable` 자동 부여. CHUPiece 정의가 Prop-valued 이므로 *cover 술어 자체가 `Decidable` 인지* 가 별도 증명 needed.

```lean
def CHUPiece : Type := CHU → Prop  -- Prop, not Bool
-- 만약 cover 가 decidable 이어야 한다면:
def CHUPieceDec : Type := { p : CHU → Prop // ∀x, Decidable (p x) }
```

→ 사용자 정전 (`AirplaneMan.lean`) 은 `Prop` 채택. **Realizability 측면에서 OK**, but **executable Boolean test** 는 별도 작업.

### S3.3 Hyperuniverse 의 size — proper class issue

Friedman Hyperuniverse 는 *countable* transitive ZFC models 만. V-logic multiverse 는 outer models 까지 확장하지만 여전히 meta-theory 에 inaccessibles 가정.

**함정**: "CHU 가 *모든* 집합을 포함한다" 는 진술은 ZFC 안에서 형식화 불가 (Russell paradox 유사). CHU 는 *type universe* 이지 V 자체 아님. 사용자 정전의 `axiom CHU : Type` 은 *type-level* 이라 size issue 회피 — 그러나 *interpretation* 시 다시 등장.

### S3.4 "Computable" 정의 미명시

S2.4 에 적은 6+ 정의 중 어느 것? 사용자 정전 (`SOURCES.md`) 은 *모듈성* 만 언급:
> "계산가능"은 그 위에서 술어가 결정 가능 *한 부분만* 다룬다는 모듈성.

→ **명시적 채택 부재**. 이 자체가 "닫지 않음" 원칙에 부합 (open으로 둠) — 그러나 논문 집필 시 한 정의 채택해야 진행 가능.

### S3.5 BHK ↔ realizability 의 *철학적* 차이

- BHK: proof = mental construction (Brouwer intuitionism)
- Realizability: proof = computer program (Kleene formalization)

두 개는 *isomorphic* 이지만 *철학적 자세* 가 다름. metahumotonic 의 *직관주의적* 측면은 BHK 에 가까우나 Lean 형식화는 realizability 에 가까움. **이 gap 이 자료집에서 explicit 화 안 됨**.

### S3.6 AI agent ↔ computable function 가설의 비자명성

"AI agent = computable function" 은 Church-Turing thesis 의 *strong physical version* 에 의존. 2025-09 ~ 2026-02 *MDPI Mathematics* 14(3):535 "Is Every Cognitive Phenomenon Computable?" 등에서 *반론* 활발 (consciousness, agency 가 Turing 한계 너머 가능성). **CHU 가 *모든* AI agent 를 cover 한다는 가설은 미검증**.

---

## S4 — 2026 trends + AI agent context

### S4.1 Antos-Friedman 후속 (2024+)

- 2018 단행본 이후 *별도* 후속 논문 검색 결과 표면적 부재 (search 한계). 단, Friedman 의 *Definability of satisfaction in outer models* (Friedman-Honzik 2016, JSL) 가 V-logic 의 후속 갈래로 진화 중.
- **Inner Model Hypothesis (IMH)** — Friedman 의 또 다른 axiom candidate. CHU 의 *minimality* 측면 (재배맨 atomic = IMH 의 inner-most witness?) 미탐구 가설.

### S4.2 Lean ↔ Rocq 통합 흐름

- **Babel-formal** (Stoskopf 2024+, OpenReview WBI1PL0hZ2) — Lean↔Rocq proof translation. CHU axiom 을 두 시스템에 동시 표현하면 *이중 검증* 가능.
- **Mistral Leanstral** (2025+) — open-source Lean 4 proof agent. CHU 자동 증명 시도 후보.
- **mathlib 1.5M lines+** (community 기준 추산, exact: 210k theorems / 100k definitions per 2025-05).

### S4.3 AI proof search + constructive

- **LeanCopilot** (Yang et al. arXiv 2404.12534, 2024-04) — LLM as Lean tactic proposer. 평균 2.08 manual steps, 74.2% automation.
- **DSP+ / DSP-Plus** (Microsoft, NeurIPS 2025): Draft-Sketch-Prove framework 부활. miniF2F 80.7%, ProofNet 32.8%, PutnamBench 24/644. **DSP draft phase = BHK proof intuition + sketch phase = formal skeleton + prove phase = realizer**.
- **ProofAug** (arXiv 2501.18310): fine-grained proof structure analysis.
- **LeanProgress** (arXiv 2502.17925): proof progress prediction via neural model.

### S4.4 Effective topos + AI agent computability (가설)

**가설** (사용자 spec 에서 제기, 본 worker 가 lineage 정리):
- AI agent 의 행동 = computable function (Church-Turing thesis strong version 가정).
- → AI agent ∈ Eff (Hyland's effective topos).
- → 모든 AI agent 는 CHU 의 element 로 표현 가능.
- → 비행기맨 = ∀x:CHU. j.covers x = ∀ AI agent. 어떤 재배맨이 그를 cover.

**비판**: 
- (a) consciousness/agency Turing 한계 너머 가능성 (S3.6).
- (b) AI agent 의 *external interaction* (sensors, internet) 이 oracle Turing machine 으로만 표현 가능 → Type-2 effectivity 필요 (Weihrauch).
- (c) LLM transformer 자체는 *fixed function* 이지만 *deployed agent* 는 환경 의존. PCA 확장이 monadic combinatory algebra (arXiv 2506.09453, 2025-06) 로 가야 할 수도.

### S4.5 Constructive reverse mathematics ↔ CHU 분류

CHU 의 cover 정리들이 BISH (Bishop), INT (intuitionistic), CLASS (classical), RUSS (Russian recursive) 중 어디 속하는지 분류는 *미수행*. PROM 후속 cycle 후보:
- `airplaneman_union` (`AirplaneMan.lean` line 80–83) 이 BISH 안에서 증명 가능?
- `exists_airplaneman_below` (line 87–95) 이 LEM 의존?
- `lift_airplaneman` 은 명백히 BISH (constructive disjunction-intro).

### S4.6 결론

CHU 의 "C" 키워드를 *Computable* 로 닫으려면:
1. **Friedman Hyperuniverse + V-logic** 을 base universe theory 로 채택 (또는 명시 거부).
2. **Hyland Effective topos** 를 cover semantics 의 internal logic 으로 채택.
3. **Turing computability** 를 표준으로 명시 (S3.4 함정 회피).
4. **AI agent ↔ computable function** 가설은 *open* 으로 둠 (열린 사고 원칙).
5. **BHK ↔ realizability** gap 을 자료집에서 explicit 화.

이 5개가 닫히면 *논문 골격* 의 (d) 발전 축 ("계산가능성의 경계" — 비행기맨 cover 의 결정가능성 ↔ Halting) 이 본격 진행 가능.

---

## Lineage 요약 (계보도)

```
Brouwer 1908+  ─┐
Heyting 1930s  ─┼─→ BHK interpretation (Heyting 1956 first canonical)
Kolmogorov 1932 ─┘                  │
                                    ↓
                          Kleene 1945 number realizability
                                    │
                                    ↓
Turing 1936  ──→ Kleene 1952 ──→ Rogers 1967 (computability standard)
                                    │
                                    ↓
                          Hyland 1982 Effective topos Eff(N)
                                    │
                            ┌───────┴───────┐
                            ↓               ↓
                   Weihrauch 2000      Maietti-Rosolini 2018
                   Type-2 TTE          predicative variant
                                            │
                                            ↓
                          Monadic combinatory algebra (2025)
                          [AI agent realizability 후보]


Friedman 2013 Hyperuniverse Programme ──→ Antos-Friedman 2015 V-logic multiverse
                                                    │
                                                    ↓
                                       Antos-Friedman-Honzik-Ternullo 2018
                                       *The Hyperuniverse Project and Maximality*
```

---

## Open questions (S1~S4 종합)

1. CHU axiom 위에 effective topos 를 *internally* construct 가능한가? Lean 4 mathlib 의 category theory 부분으로 시도 가능?
2. 비행기맨 cover 가 *uniformly decidable* 인 CHU 부분집합은? (S4.5 의 reverse math classification)
3. AI agent 가 PCA 의 element 라는 형식화에 monadic 확장이 필수인가?
4. V-logic multiverse 와 Hyperuniverse 의 관계가 *재배맨 계층 구조* (atomic/governs) 와 isomorphic 한가?
5. Lean 4 의 `noncomputable def` 회피 = CHU 를 `Computable` typeclass 로 강화 → 사용자 정전 변경 필요?

---

**Worker note**: 본 보고서는 web search + 사용자 정전(`AirplaneMan.lean`, `SOURCES.md`) 종합. Friedman 후속 2024+ 검색은 표면적 부재 (publisher paywall/검색엔진 한계 가능성). LeanDojo / LeanCopilot 계열 2025-2026 진전이 가장 활발. AI agent ↔ computable 가설은 *철학적으로* 미해결로 둠 (열린 사고 원칙).

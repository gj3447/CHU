/-
단 하나의 비행기맨 — Uniqueness formalization (native Lean 4, no Mathlib)

세 가지 유일성:
  1. Extensional — 모든 비행기맨의 coverage = fun _ => True
  2. Structural — 동형 아래 유일 (depth/sizeOf 최소)
  3. Quotient  — coverage equivalence로 Quot 타입 구성
-/

-- Inline AirplaneMan definitions (no separate module compile)
axiom CHU : Type
def CHUPiece : Type := CHU → Prop

inductive JaebaeMan : Type where
  | atomic  : CHUPiece → JaebaeMan
  | governs : List JaebaeMan → JaebaeMan
  deriving Inhabited

mutual
  def JaebaeMan.covers : JaebaeMan → CHU → Prop
    | .atomic p,  x => p x
    | .governs js, x => JaebaeMan.anyCovers js x

  def JaebaeMan.anyCovers : List JaebaeMan → CHU → Prop
    | [],       _ => False
    | j :: rest, x => j.covers x ∨ JaebaeMan.anyCovers rest x
end

def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x

mutual
  def JaebaeMan.depth : JaebaeMan → Nat
    | .atomic _   => 1
    | .governs js => 1 + JaebaeMan.maxDepth js

  def JaebaeMan.maxDepth : List JaebaeMan → Nat
    | []       => 0
    | j :: rest => Nat.max j.depth (JaebaeMan.maxDepth rest)
end

def wholeCHU : CHUPiece := fun _ => True
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU
theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by intro _; trivial
def layer2AirplaneMan : JaebaeMan := .governs [trivialAirplaneMan]

-- =============================================================
-- (a) EXTENSIONAL UNIQUENESS
-- 두 비행기맨은 coverage가 pointwise 동치
-- =============================================================

/-- 두 비행기맨의 coverage는 pointwise 동치 -/
theorem airplanemen_have_same_coverage (j₁ j₂ : JaebaeMan)
    (h₁ : isAirplaneMan j₁) (h₂ : isAirplaneMan j₂) :
    ∀ x, j₁.covers x ↔ j₂.covers x := by
  intro x
  exact ⟨fun _ => h₂ x, fun _ => h₁ x⟩

/-- funext 사용: coverage 함수 자체가 같음 -/
theorem airplanemen_coverage_eq (j₁ j₂ : JaebaeMan)
    (h₁ : isAirplaneMan j₁) (h₂ : isAirplaneMan j₂) :
    (fun x => j₁.covers x) = (fun x => j₂.covers x) := by
  funext x
  exact propext (airplanemen_have_same_coverage j₁ j₂ h₁ h₂ x)

/-- 모든 비행기맨의 coverage = wholeCHU -/
theorem airplaneman_coverage_is_whole (j : JaebaeMan) (h : isAirplaneMan j) :
    (fun x => j.covers x) = wholeCHU := by
  funext x
  exact propext ⟨fun _ => trivial, fun _ => h x⟩

-- =============================================================
-- (b) STRUCTURAL MINIMALITY
-- trivialAirplaneMan은 depth 기준 최소 비행기맨
-- =============================================================

/-- 비행기맨이려면 non-empty CHU에서 depth ≥ 1 -/
theorem airplaneman_depth_ge_one (j : JaebaeMan) (_ : isAirplaneMan j) :
    j.depth ≥ 1 := by
  cases j with
  | atomic _ => simp [JaebaeMan.depth]
  | governs _ => simp [JaebaeMan.depth]

/-- trivialAirplaneMan은 depth = 1 -/
theorem trivialAirplaneMan_depth : trivialAirplaneMan.depth = 1 := rfl

/-- trivialAirplaneMan은 minimal depth 비행기맨 -/
theorem trivialAirplaneMan_is_minimal (j : JaebaeMan) (h : isAirplaneMan j) :
    trivialAirplaneMan.depth ≤ j.depth := by
  rw [trivialAirplaneMan_depth]
  exact airplaneman_depth_ge_one j h

/-- 정정 (2026-05-02):

원래 statement (`exists_nontrivial_depth_one_airplaneman`)는 Lean 4 표준 propext + funext
하에서 *거짓*이다. 이유: `∀ x, p₁ x` 와 `∀ x, p₂ x` 가 모두 성립하면, propext에 의해
`p₁ x = p₂ x = True`, funext에 의해 `p₁ = p₂`, 따라서 `atomic p₁ = atomic p₂`.

올바른 uniqueness theorem은 *반대*: 모든 depth=1 비행기맨은 propext+funext 하에서
하나의 동일한 atomic 형태로 수렴한다. 이는 비행기맨의 *extensional uniqueness at depth 1*. -/
theorem all_depth_one_airplanemen_eq (p₁ p₂ : CHUPiece)
    (h₁ : ∀ x, p₁ x) (h₂ : ∀ x, p₂ x) :
    JaebaeMan.atomic p₁ = JaebaeMan.atomic p₂ := by
  congr 1
  funext x
  exact propext ⟨fun _ => h₂ x, fun _ => h₁ x⟩

/-- 따라서 모든 depth=1 atomic 비행기맨은 trivialAirplaneMan과 같다. -/
theorem depth_one_atomic_airplaneman_is_trivial (p : CHUPiece) (h : ∀ x, p x) :
    JaebaeMan.atomic p = trivialAirplaneMan := by
  unfold trivialAirplaneMan wholeCHU
  exact all_depth_one_airplanemen_eq p (fun _ => True) h (fun _ => trivial)

-- =============================================================
-- (c) QUOTIENT UNIQUENESS
-- coverage-equivalence로 Quot 타입 구성 — 모든 비행기맨이 하나의 class
-- =============================================================

/-- Coverage equivalence relation -/
def coverageEquiv (j₁ j₂ : JaebaeMan) : Prop :=
  ∀ x, j₁.covers x ↔ j₂.covers x

theorem coverageEquiv.refl (j : JaebaeMan) : coverageEquiv j j :=
  fun _ => Iff.rfl

theorem coverageEquiv.symm {j₁ j₂ : JaebaeMan} :
    coverageEquiv j₁ j₂ → coverageEquiv j₂ j₁ :=
  fun h x => (h x).symm

theorem coverageEquiv.trans {j₁ j₂ j₃ : JaebaeMan} :
    coverageEquiv j₁ j₂ → coverageEquiv j₂ j₃ → coverageEquiv j₁ j₃ :=
  fun h₁ h₂ x => (h₁ x).trans (h₂ x)

instance jaebaeManSetoid : Setoid JaebaeMan where
  r := coverageEquiv
  iseqv := ⟨coverageEquiv.refl, coverageEquiv.symm, coverageEquiv.trans⟩

/-- Quotient type: JaebaeMan modulo coverage equivalence -/
def JaebaeManQuot : Type := Quotient jaebaeManSetoid

/-- 비행기맨 quotient class (canonical): -/
def airplaneMan_quot : JaebaeManQuot :=
  Quotient.mk jaebaeManSetoid trivialAirplaneMan

/-- 핵심: 모든 비행기맨은 같은 quotient class에 속함 -/
theorem all_airplanemen_equal_in_quot (j : JaebaeMan) (h : isAirplaneMan j) :
    Quotient.mk jaebaeManSetoid j = airplaneMan_quot := by
  apply Quotient.sound
  intro x
  exact ⟨fun _ => trivial, fun _ => h x⟩

/-- 따라서 "비행기맨 subtype"은 quotient 내에서 singleton -/
theorem airplaneman_subtype_quot_singleton
    (j₁ j₂ : JaebaeMan) (h₁ : isAirplaneMan j₁) (h₂ : isAirplaneMan j₂) :
    Quotient.mk jaebaeManSetoid j₁ = Quotient.mk jaebaeManSetoid j₂ := by
  rw [all_airplanemen_equal_in_quot j₁ h₁, all_airplanemen_equal_in_quot j₂ h₂]

-- =============================================================
-- (d) F-ALGEBRA TERMINAL VIEW
-- coverage fibration의 terminal = wholeCHU = 비행기맨
-- =============================================================

/-- Coverage predicate poset의 terminal element -/
def coveragePoset.top : CHU → Prop := wholeCHU

theorem coverage_le_top (P : CHU → Prop) : ∀ x, P x → coveragePoset.top x :=
  fun _ _ => trivial

theorem airplaneman_coverage_is_top (j : JaebaeMan) (h : isAirplaneMan j) :
    ∀ x, j.covers x ↔ coveragePoset.top x :=
  fun x => ⟨fun _ => trivial, fun _ => h x⟩

/-
결론:
  (a) extensional 유일성 — 증명 완료 (airplanemen_coverage_eq)
  (b) structural minimality — trivialAirplaneMan이 depth 최소 (유일 아님)
  (c) quotient 유일성 — airplaneMan_quot이 singleton class (증명 완료)
  (d) terminal 관점 — coverage poset에서 top이 유일
-/

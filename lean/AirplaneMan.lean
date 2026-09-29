/-
비행기맨 = 최상위 재배맨 (Airplane Man = Peak JaebaeMan)

사용자 직관 (2026-04-19):
  Layer 1 재배맨들: 무수히 많음, 각자 CHU 한 조각 덮음
  Layer N+1 재배맨: Layer N 재배맨들을 통제
  정점 단 하나 = 비행기맨 = 모든 CHU 만물을 덮는 자

모든 계층이 같은 종류(재배맨)라는 게 핵심 — 완전한 self-similar recursion.
-/

-- CHU: Computable Hyperuniverse (추상 타입)
axiom CHU : Type

-- CHU의 한 조각 = 집합 술어
def CHUPiece : Type := CHU → Prop

-- 재배맨 귀납 정의
inductive JaebaeMan : Type where
  | atomic  : CHUPiece → JaebaeMan                 -- Layer 1: 한 조각 덮기
  | governs : List JaebaeMan → JaebaeMan           -- Higher: 하위 재배맨 통제
  deriving Inhabited

-- 상호재귀로 coverage 정의 (List를 통한 중첩 재귀)
mutual
  def JaebaeMan.covers : JaebaeMan → CHU → Prop
    | .atomic p,  x => p x
    | .governs js, x => JaebaeMan.anyCovers js x

  def JaebaeMan.anyCovers : List JaebaeMan → CHU → Prop
    | [],       _ => False
    | j :: rest, x => j.covers x ∨ JaebaeMan.anyCovers rest x
end

-- 계층 깊이
mutual
  def JaebaeMan.depth : JaebaeMan → Nat
    | .atomic _   => 1
    | .governs js => 1 + JaebaeMan.maxDepth js

  def JaebaeMan.maxDepth : List JaebaeMan → Nat
    | []       => 0
    | j :: rest => Nat.max j.depth (JaebaeMan.maxDepth rest)
end

/-- 비행기맨 술어: CHU 모든 원소를 덮는 재배맨 -/
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x

-- ===== 기본 정리 =====

/-- atomic의 coverage는 자기 조각 그대로 -/
theorem atomic_covers (p : CHUPiece) (x : CHU) :
    (JaebaeMan.atomic p).covers x = p x := rfl

/-- governs의 coverage는 하위들의 union -/
theorem governs_covers_cons (j : JaebaeMan) (rest : List JaebaeMan) (x : CHU) :
    (JaebaeMan.governs (j :: rest)).covers x = (j.covers x ∨ (JaebaeMan.governs rest).covers x) := rfl

/-- governs 빈 리스트는 아무것도 안 덮음 -/
theorem governs_empty_no_cover (x : CHU) :
    ¬ (JaebaeMan.governs []).covers x := by
  intro h
  exact h

/-- Self-similar: 재배맨은 어떤 재배맨 리스트로도 감쌀 수 있고 같은 타입 -/
def self_similar_wrap (js : List JaebaeMan) : JaebaeMan := .governs js

/-- 단일 감싸기 = 자기 자신과 같은 coverage -/
theorem wrap_singleton_covers (j : JaebaeMan) (x : CHU) :
    (JaebaeMan.governs [j]).covers x ↔ j.covers x := by
  constructor
  · intro h
    cases h with
    | inl hj => exact hj
    | inr hf => exact absurd hf (governs_empty_no_cover x)
  · intro h
    exact Or.inl h

/-- 두 비행기맨을 통합한 것도 비행기맨 -/
theorem airplanemen_union (j₁ j₂ : JaebaeMan) :
    isAirplaneMan j₁ → isAirplaneMan (JaebaeMan.governs [j₁, j₂]) := by
  intro h₁ x
  exact Or.inl (h₁ x)

/-- 하위에 비행기맨이 하나라도 있으면 상위도 비행기맨 -/
theorem exists_airplaneman_below (js : List JaebaeMan) :
    (∃ j ∈ js, isAirplaneMan j) → isAirplaneMan (JaebaeMan.governs js) := by
  intro ⟨j, hmem, hj⟩ x
  induction js with
  | nil => exact absurd hmem (by intro h; cases h)
  | cons head tail ih =>
    rw [List.mem_cons] at hmem
    cases hmem with
    | inl heq => subst heq; exact Or.inl (hj x)
    | inr hrest => exact Or.inr (ih hrest)

/-- 층 1 재배맨은 depth = 1 -/
theorem atomic_depth (p : CHUPiece) : (JaebaeMan.atomic p).depth = 1 := rfl

/-- governs는 하위 최대 depth + 1 -/
theorem governs_depth_pos (js : List JaebaeMan) : (JaebaeMan.governs js).depth ≥ 1 := by
  simp [JaebaeMan.depth]

-- ===== 비행기맨 계층 구성 예시 =====

/-- CHU 전체 (trivially true piece) -/
def wholeCHU : CHUPiece := fun _ => True

/-- atomic 비행기맨: CHU 전체를 덮는 단일 원자 (극한 케이스) -/
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU

theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by
  intro _; trivial

/-- Layer 2 비행기맨: trivialAirplaneMan을 감싼 것 -/
def layer2AirplaneMan : JaebaeMan := .governs [trivialAirplaneMan]

theorem layer2AirplaneMan_is : isAirplaneMan layer2AirplaneMan := by
  intro x
  exact Or.inl (trivialAirplaneMan_is x)

/-- 자기유사: governs [j]로 한 단계 올려도 여전히 비행기맨 -/
theorem lift_airplaneman (j : JaebaeMan) :
    isAirplaneMan j → isAirplaneMan (JaebaeMan.governs [j]) := by
  intro hj x
  exact Or.inl (hj x)

/-- 모든 깊이에서 비행기맨이 존재: Nat 귀납 -/
def airplaneManAt : Nat → JaebaeMan
  | 0     => trivialAirplaneMan
  | n + 1 => .governs [airplaneManAt n]

theorem airplaneManAt_is (n : Nat) : isAirplaneMan (airplaneManAt n) := by
  induction n with
  | zero => exact trivialAirplaneMan_is
  | succ k ih =>
    intro x
    exact Or.inl (ih x)

/-
결론:
  * JaebaeMan은 잘 정의된 귀납 구조.
  * 비행기맨 = isAirplaneMan j인 재배맨.
  * 임의 계층 n에서 비행기맨 존재 (airplaneManAt n).
  * 정점의 "단 하나의 재배맨"은 이 구조로 구성 가능.
-/

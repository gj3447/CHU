/-
AirplaneMan_Gap3_Cover — Layer 1 재배맨 family가 CHU 전역을 덮는다는 공리의 형식화.

Gap 3 질문:
  기존 AirplaneMan.lean은 `∀ x, j.covers x`에서 `j = governs js`가 **유한 List** 이어야
  비행기맨이 된다. 그러나 "Layer 1 재배맨이 무수히 많고 각자 한 조각을 덮는다" 는
  직관은 **무한 family**를 요구한다. 즉 다음 두 서술 사이 gap:
      (A) ∃ j : JaebaeMan, isAirplaneMan j              -- governs [trivial] 로 쉽게 성립
      (B) ∃ F : Set CHUPiece, coversAll F                -- 진짜로 "조각들이 모여 CHU를 덮는다"
  Gap 3 는 (B) 를 명시적으로 공리화하고 (A) 와의 연결을 증명한다.

"덮는다" 의미 3가지 — 본 파일의 **권장 해석은 Open Cover**:
  1. Open cover  : ∀ x, ∃ p ∈ F, p x            ← 본 파일 채택 (가장 약한 조건 + native)
  2. Partition   : 위 + disjoint (각 x 정확히 하나)   ← Setoid quotient 필요 (Gap 4)
  3. Sheaf       : locally → globally glue           ← Mathlib CategoryTheory.Sites 필요

근거:
  * CHU는 axiom Type 이므로 topology/sheaf/HoTT 구조가 없다.
    Open cover는 유일하게 구조 전제 없이 정의되는 해석이다.
  * Partition은 "중복 금지" 가 세계관상 강제되지 않는다 — Layer 1 재배맨 조각들이
    겹쳐도 이상하지 않고, 오히려 resonance(공명) 의미로 자연스럽다.
  * Sheaf는 과잉 추상 — 국소→전역 glue 를 강제하려면 Site 구조를 CHU 위에 깔아야
    하는데 아직 그럴 필요 없다.
  * HoTT covering space 는 path-connectedness 전제가 필요하고 Lean 4 native 에
    없다 (Ground Zero 라이브러리 추가 의존성).

Mathlib 의존성 없음. 순수 native Lean 4.
-/

-- ============================================================
-- 0. 기반 — AirplaneMan.lean 재선언 (독립 컴파일 가능)
-- ============================================================

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

-- ============================================================
-- 1. Layer 1 Family — Set CHUPiece 로 표현
-- ============================================================

/-
왜 `Set CHUPiece` 이고 `List CHUPiece` 가 아닌가:
  * List 는 유한. "무수히 많은 Layer 1 재배맨" 을 수용 못함.
  * Lean 4 core 에는 `Set` 이 없음 (Mathlib 에만 존재) → 직접 정의.
    `Set α := α → Prop`, 그리고 `Membership` 인스턴스를 자체 선언.
  * 이렇게 하면 `p ∈ F` 가 `F p` 로 동일하게 펼쳐진다.
-/

/-- Lean 4 core 에 `Set` 이 없으므로 직접 정의 (Mathlib Set 와 형식 동일).
    `abbrev` 로 두어 membership 이 바로 함수 적용으로 풀리게 함. -/
abbrev Set (α : Type) : Type := α → Prop

instance {α : Type} : Membership α (Set α) := ⟨fun (s : Set α) (a : α) => s a⟩

/-- Layer 1 Family = CHU 조각들의 집합. -/
abbrev Layer1Family : Type := Set CHUPiece

/-- family 의 조각들이 CHU 전역을 덮는다 (open cover 해석). -/
def coversAll (F : Layer1Family) : Prop :=
  ∀ x : CHU, ∃ p : CHUPiece, p ∈ F ∧ p x

-- ============================================================
-- 2. 공리 — Layer 1 로 CHU 가 덮인다
-- ============================================================

/--
**공리 (Gap 3 Cover Axiom)**:
  CHU 를 덮는 Layer 1 family 가 존재한다.

세계관 해석:
  "무수히 많은 Layer 1 재배맨 — 각자 한 조각을 덮음 — 이 모여 CHU 전역을 덮는다."
  이는 trivialAirplaneMan (조각=wholeCHU 인 atomic) 으로 trivially 성립하지만,
  본 공리는 **임의 family 에 대해** "덮이는 family 가 적어도 하나" 를 주장한다.
  즉 Layer 1 층이 존재론적으로 포화(saturated) 임을 공리화.

열린 부분:
  * family 의 cardinality (유한 / 가산 / 비가산) 는 명시 안 함 → 열어둠.
  * 중복 여부 → 열어둠 (Open Cover 해석).
  * 조각들이 서로 "경계" 를 어떻게 공유하는지 → 열어둠 (Sheaf 로 가려면 Gap 5 에서).
-/
axiom CHU_coverable : ∃ F : Layer1Family, coversAll F

-- ============================================================
-- 3. family → JaebaeMan 함수 (atomic Layer 1 재배맨들)
-- ============================================================

/-- 조각 하나당 atomic 재배맨 하나. -/
def pieceToAtomic (p : CHUPiece) : JaebaeMan := .atomic p

/-- family 의 조각들이 모두 Layer 1 atomic 재배맨인 술어. -/
def isLayer1 (j : JaebaeMan) : Prop := ∃ p : CHUPiece, j = .atomic p

theorem pieceToAtomic_isLayer1 (p : CHUPiece) : isLayer1 (pieceToAtomic p) :=
  ⟨p, rfl⟩

-- ============================================================
-- 4. 핵심 연결 정리 — coversAll F ↔ "governs-of-atomics" 가 비행기맨
-- ============================================================

/-
`List` 버전의 기존 isAirplaneMan 과 `Set` 버전의 coversAll 은 정확히는
동등하지 않다 (유한 vs 무한). 대신 각 방향의 bridge 정리를 제공:

  (→) 유한 family (List) 로 coversAll 이면 governs 로 비행기맨 얻음.
  (←) 비행기맨 j = governs js 이면 js 에서 추출한 piece set 이 coversAll.
-/

/-- List 를 Set 으로 끌어올린다 (`p ∈ L` 은 `List.Mem`). -/
def listToFamily (ps : List CHUPiece) : Layer1Family :=
  (fun p => p ∈ ps : Set CHUPiece)

/-- 보조 (→): 조각 p ∈ ps 와 p x 로부터 anyCovers 유도. -/
theorem anyCovers_of_mem (ps : List CHUPiece) (x : CHU)
    (p : CHUPiece) (hpMem : p ∈ ps) (hpx : p x) :
    JaebaeMan.anyCovers (ps.map pieceToAtomic) x := by
  induction ps with
  | nil => exact absurd hpMem (by intro h; cases h)
  | cons head tail ih =>
    rw [List.map_cons]
    show (pieceToAtomic head).covers x ∨ JaebaeMan.anyCovers (tail.map pieceToAtomic) x
    cases hpMem with
    | head => exact Or.inl hpx
    | tail _ hpTail => exact Or.inr (ih hpTail)

/-- 보조 (←): anyCovers 로부터 조각 p ∈ ps 와 p x 추출. -/
theorem mem_of_anyCovers (ps : List CHUPiece) (x : CHU)
    (hcov : JaebaeMan.anyCovers (ps.map pieceToAtomic) x) :
    ∃ p, p ∈ ps ∧ p x := by
  induction ps with
  | nil => exact absurd hcov (fun h => h)
  | cons head tail ih =>
    rw [List.map_cons] at hcov
    cases hcov with
    | inl hh => exact ⟨head, List.Mem.head _, hh⟩
    | inr ht =>
      rcases ih ht with ⟨p, hpMem, hpx⟩
      exact ⟨p, List.Mem.tail _ hpMem, hpx⟩

/-- 유한 family 의 coversAll 은 governs-of-atomics 의 isAirplaneMan 과 동등. -/
theorem coversAll_iff_governs_atomics (ps : List CHUPiece) :
    coversAll (listToFamily ps) ↔
      isAirplaneMan (.governs (ps.map pieceToAtomic)) := by
  constructor
  · intro hCov x
    rcases hCov x with ⟨p, hpMem, hpx⟩
    -- hpMem : p ∈ listToFamily ps = (p ∈ ps)
    exact anyCovers_of_mem ps x p hpMem hpx
  · intro hAir x
    have hcov : JaebaeMan.anyCovers (ps.map pieceToAtomic) x := hAir x
    rcases mem_of_anyCovers ps x hcov with ⟨p, hpMem, hpx⟩
    exact ⟨p, hpMem, hpx⟩

-- ============================================================
-- 5. 역방향: 비행기맨 ⇒ Layer 1 family 존재 (Open Cover 해석)
-- ============================================================

/--
임의 비행기맨 j 로부터 CHU 를 덮는 Layer1Family 를 구성.
단순 전략: **x ↦ "x 를 덮는 조각"** 이라는 family (치역 관점).

증명에서는 "j.covers x 를 witness 하는 조각" 을 고정 선택해야 해서
classical.choice 가 필요할 수 있다. 여기서는 가장 약한 구성 — coverage function
자체를 하나의 wholeCHU 조각으로 취급 — 를 사용해 classical 없이 통과.
-/
theorem airplaneMan_to_coverable (_j : JaebaeMan) (_h : isAirplaneMan _j) :
    ∃ F : Layer1Family, coversAll F := by
  -- wholeCHU 하나만 담은 family
  refine ⟨fun p => p = (fun _ => True), ?_⟩
  intro _x
  refine ⟨fun _ => True, rfl, ?_⟩
  trivial

/-- 공리의 약한 버전 — trivial 비행기맨으로부터 유도 가능. -/
theorem CHU_coverable_from_trivial : ∃ F : Layer1Family, coversAll F :=
  airplaneMan_to_coverable (.atomic (fun _ => True)) (fun _ => trivial)

/-
관찰:
  `CHU_coverable_from_trivial` 이 **증명** 되므로, 공리 `CHU_coverable` 은
  엄밀히는 불필요하다 (wholeCHU 조각 하나로 덮으면 끝). 그럼에도 공리로 둔 이유:
    * 세계관 상 "Layer 1 재배맨이 각자 *작은* 조각을 덮는다" 를 주장하고 싶음.
    * 즉 "wholeCHU 처럼 cheat 하지 않는 family 가 존재" — 이게 실제 공리.
    * 이 강한 버전을 원하면 다음 공리를 추가:
        axiom CHU_nontrivially_coverable :
          ∃ F : Layer1Family,
            coversAll F ∧ (∀ p ∈ F, ∃ x, ¬ p x)
      (각 조각이 proper subset 임을 강제)
  현재는 약한 버전으로 두어 **열어둠**.
-/

-- ============================================================
-- 6. governs-of-family — family 를 List 로 꺼내 governs 만들기 (finite only)
-- ============================================================

/-- finite family (List) 로부터 비행기맨 후보 구성. -/
def familyToAirplane (ps : List CHUPiece) : JaebaeMan :=
  .governs (ps.map pieceToAtomic)

theorem familyToAirplane_isAirplaneMan (ps : List CHUPiece)
    (h : coversAll (listToFamily ps)) :
    isAirplaneMan (familyToAirplane ps) :=
  (coversAll_iff_governs_atomics ps).mp h

-- ============================================================
-- 7. 권장 해석 정리
-- ============================================================

/-
권장 해석: **Open Cover** (`∀ x, ∃ p ∈ F, p x`).

이유:
  (i)  Native Lean 4 로 즉시 작성 가능. Mathlib 불필요.
  (ii) CHU 가 추상 axiom type 이라 topology/sheaf 구조를 깔 근거 없음.
  (iii) 세계관 상 Layer 1 조각들이 겹치는 것은 문제없음 (오히려 resonance).
  (iv) Partition 을 원하면 Gap 4 (Setoid quotient) 에서 별도 정제 가능.
  (v)  Sheaf 를 원하면 Gap 5 에서 Mathlib.CategoryTheory.Sites 도입.

무한 family 는 `Set CHUPiece` 로 자연스럽게 포섭되며, 증명에서 필요하면
choice axiom (Classical.choose) 으로 witness 를 뽑으면 된다.
-/

-- ============================================================
-- 8. 열린 질문
-- ============================================================

/-
Q1. CHU_coverable 공리를 "proper cover" (각 조각이 진부분집합) 로 강화할지?
    현 상태는 wholeCHU trivial family 로 만족되므로 세계관의 "무수한 조각" 직관을
    제대로 포착 못함. 강화 공리는 위 주석에 후보로 명시.

Q2. 무한 family → 하나의 JaebaeMan 으로 압축하는 직접 연산 부재:
    기존 JaebaeMan.governs 는 List 만 받는다. 무한을 흡수하려면
      | governsSet : Set JaebaeMan → JaebaeMan
    같은 생성자를 추가해야 하지만 이는 inductive type 의 positivity 를 깨지 않기
    위해 `Set JaebaeMan = JaebaeMan → Prop` 의 사용이 엄격히 제약된다.
    (Lean 4 `inductive` 는 strictly positive 여야 함.)
    대안: JaebaeManInf (νF / Thunk) 를 확장해 coinductive Set 을 허용.

Q3. coversAll 의 "∃ p ∈ F" 는 choice 를 필요로 함 (실제 p 를 꺼내려면).
    `Classical.choice` 없이 증명 진행 가능한 부분과 불가능한 부분의 경계 분석.

Q4. Partition 해석 ↔ Setoid/Quotient 연결:
    "각 x 가 정확히 하나의 p 에 속함" 을 Setoid 로 표현하면 quotient CHU/~
    가 index set 이 된다. AirplaneMan_Uniqueness.lean 의 coverageEquiv 와
    쌍대 관계 — 거기는 "재배맨 quotient", 여기는 "CHU quotient".

Q5. Sheaf 해석 구현 시점:
    CHU 위에 pretopology (covering sieve) 를 깔면 Mathlib 의
    `CategoryTheory.Sites.Grothendieck` 직접 재사용 가능. CHU 를 category 로
    승격 (objects = CHUPiece, morphisms = implication) 이 자연스러운 첫 걸음.

Q6. HoTT covering space 해석:
    CHU 를 ∞-groupoid 로 보면 "덮개" 는 fibration. Lean 4 에서는
    Ground Zero 라이브러리 (rzrn/ground_zero) 가 HoTT primitives 제공하지만
    mathlib/native 와 섞어 쓰기 번거로움. Gap 6 이후로 미룸.
-/

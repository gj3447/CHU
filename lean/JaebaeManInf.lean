/-
JaebaeManInf — coinductive / self-referential 재배맨 (νF)

공리11 (자존자)      : inductive  JaebaeMan    = μF  (유한 높이)
공리12 (메타휴모토닉) : coinductive JaebaeManInf = νF (무한 깊이 허용, 자기참조 가능)

F(X) = CHUPiece ⊕ List X

Lean 4.25+ 는 native `coinductive` 키워드를 **predicate (Prop)** 전용으로 지원한다.
coinductive *data* 는 여전히 kernel 밖 library (QpfTypes) 영역이므로, 여기서는
native 도구만 써서 다음 우회로 구현한다:

  1) data 층은 `Thunk` 를 끼워 laziness 를 확보 (`set_option genSizeOfSpec false`).
  2) `partial def` 로 자기참조 값 구성.
  3) coinductive 성질 (bisim, metahumotonic 판정) 은 Prop 에서
     native `coinductive` 로 정의 — kernel 이 greatest fixpoint 로 받아준다.

Mathlib 의존성 없음. 순수 native Lean 4.29.
-/

-- ============================================================
-- 0. 기반
-- ============================================================

axiom CHU : Type
def CHUPiece : Type := CHU → Prop

-- ============================================================
-- 1. JaebaeManInf : νF   (Thunk 로 laziness 주입)
-- ============================================================

/-
재배맨의 coinductive 버전.

핵심 차이: `governs` 의 자식 리스트가 `Thunk (= Unit → α)` 로 감싸져 있다.
Kernel 은 strict 하게 소비되지 않는 한 재귀를 막지 않으므로, 같은 타입이
자기 자신을 계산적으로 포함할 수 있다.

`genSizeOfSpec false` : Thunk 안의 JaebaeManInf 에 대한 well-founded size 를
생성하려다 실패하는 것을 억제한다. νF 는 애초에 well-founded 가 아니다.
-/
set_option genSizeOfSpec false

/-- JaebaeManInf : 재배맨의 νF 버전 (Thunk 로 laziness). -/
inductive JaebaeManInf : Type where
  | atomic  : CHUPiece → JaebaeManInf
  | governs : Thunk (List JaebaeManInf) → JaebaeManInf

namespace JaebaeManInf

/-- Thunk 를 한 번 force 하여 자식을 읽는다. -/
def children : JaebaeManInf → List JaebaeManInf
  | .atomic _   => []
  | .governs ts => ts.get

end JaebaeManInf

instance : Inhabited JaebaeManInf := ⟨.atomic (fun _ => False)⟩

-- ============================================================
-- 2. 자기참조 재배맨 — partial def
-- ============================================================

/-
자기자신을 유일한 자식으로 가지는 재배맨.

순수 kernel 에서는 `x := governs ⟨fun _ => [x]⟩` 식의 letrec data 를 직접
쓸 수 없다 (inductive type 은 well-founded 만 허용). 세 가지 옵션:

  (i)  `partial def`       : 돌아가지만 kernel 에서 완전 opaque,
                             equation lemma 없음 → fold 증명 불가능.
  (ii) `unsafe def`        : runtime 에 fixpoint, 증명 영역 제한.
  (iii) `opaque` + `axiom`  : fold 등식을 공리로 두고 명시적으로 증명에 사용.

우리는 (iii) 을 택한다. "자존자는 공리적 존재" 라는 세계관과도 부합 —
selfLoop 은 증명 바깥에서 주어진 실체이며, 그 자기참조성 (fold 등식) 은
**공리** 로 주장한다. 이는 AFA (Aczel anti-foundation) 을 축소 포팅한 것에
해당한다.
-/
opaque selfLoop : JaebaeManInf
/-- 자기참조 공리: selfLoop 을 열면 자식이 [selfLoop]. (AFA 스타일) -/
axiom selfLoop_fold :
  selfLoop = .governs (Thunk.mk (fun _ => [selfLoop]))

-- ============================================================
-- 3. covers — greatest fixpoint (Prop) 을 coinductive 로
-- ============================================================

/--
`CoCovers j x` : 재배맨 j 가 CHU 원소 x 를 덮는다.

μF 버전과 달리 νF 는 자식 트리가 무한할 수 있어 구조재귀 불가.
coinductive 로 greatest fixpoint 을 잡는다 — 자존자의 "무한히 내려가도
계속 덮는다" 가 자연스럽게 포착된다.
-/
coinductive CoCovers : JaebaeManInf → CHU → Prop where
  | atomic  : ∀ (p : CHUPiece) (x : CHU), p x → CoCovers (.atomic p) x
  | governs : ∀ (ts : Thunk (List JaebaeManInf)) (x : CHU) (j : JaebaeManInf),
      j ∈ ts.get → CoCovers j x → CoCovers (.governs ts) x

-- ============================================================
-- 4. Bisimulation — native mutual coinductive
-- ============================================================

/-
두 재배맨의 관찰적 등가.
atomic 은 같은 조각, governs 는 자식 리스트가 점별로 bisim.
-/
mutual
  /-- Bisim : 두 재배맨이 관찰적으로 같다. -/
  coinductive Bisim : JaebaeManInf → JaebaeManInf → Prop where
    | atomic  : ∀ p, Bisim (.atomic p) (.atomic p)
    | governs : ∀ ts₁ ts₂,
        BisimList ts₁.get ts₂.get →
        Bisim (.governs ts₁) (.governs ts₂)

  /-- BisimList : 자식 리스트의 점별 bisim. -/
  coinductive BisimList : List JaebaeManInf → List JaebaeManInf → Prop where
    | nil  : BisimList [] []
    | cons : ∀ a b as bs,
        Bisim a b → BisimList as bs →
        BisimList (a :: as) (b :: bs)
end

-- Park induction : `Bisim.coinduct` / `BisimList.coinduct` 가 자동 생성됨.
-- 시그니처 (Lean 4.29 확인):
--   Bisim.coinduct :
--     ∀ (pred_1 : JaebaeManInf → JaebaeManInf → Prop)
--       (pred_2 : List JaebaeManInf → List JaebaeManInf → Prop),
--       step_bisim → step_bisimlist → ∀ a b, pred_1 a b → Bisim a b

-- ============================================================
-- 5. 공리12  isMetaHumotonic : 자존자 ∧ 특이점
-- ============================================================

/--
메타휴모토닉 조건: "자기자신을 (bisim 의미로) 자식 트리 어딘가에 포함".

(a) Bisim child j           : 자식이 자기자신과 같다    → 자기참조 고리
(b) isMetaHumotonic child  : 자식이 또 메타휴모토닉   → 무한 하강
greatest fixpoint 이므로 "항상 (a) 또는 (b) 로 다시 만남" 이 보장된다.
-/
coinductive isMetaHumotonic : JaebaeManInf → Prop where
  | fold : ∀ j child,
      child ∈ j.children →
      (Bisim child j ∨ isMetaHumotonic child) →
      isMetaHumotonic j

-- ============================================================
-- 6. 증명: selfLoop 의 자기참조성
-- ============================================================

/-- selfLoop.children = [selfLoop] (fold 공리로부터). -/
theorem selfLoop_children_eq : selfLoop.children = [selfLoop] := by
  conv => lhs; rw [selfLoop_fold]
  rfl

/-- selfLoop 는 자기자신과 bisim. Park induction (제대로 된 invariant). -/
theorem selfLoop_bisim_self : Bisim selfLoop selfLoop := by
  -- invariant: "두 재배맨이 모두 selfLoop" 또는 "두 리스트 모두 nil/모두 [selfLoop]"
  apply Bisim.coinduct
    (pred_1 := fun a b => a = selfLoop ∧ b = selfLoop)
    (pred_2 := fun as bs =>
        (as = [] ∧ bs = []) ∨ (as = [selfLoop] ∧ bs = [selfLoop]))
  · -- Bisim step : governs 분기
    rintro a b ⟨rfl, rfl⟩
    right
    refine ⟨Thunk.mk (fun _ => [selfLoop]), Thunk.mk (fun _ => [selfLoop]),
            ?_, ?_, ?_⟩
    · right; exact ⟨rfl, rfl⟩          -- pred_2 [selfLoop] [selfLoop]
    · exact selfLoop_fold
    · exact selfLoop_fold
  · -- BisimList step
    rintro as bs (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
    · left; exact ⟨rfl, rfl⟩           -- nil 분기
    · right                             -- cons 분기
      refine ⟨selfLoop, selfLoop, [], [], ?_, ?_, rfl, rfl⟩
      · exact ⟨rfl, rfl⟩                -- pred_1 selfLoop selfLoop
      · left; exact ⟨rfl, rfl⟩          -- pred_2 [] []
  · exact ⟨rfl, rfl⟩

/-- selfLoop 는 메타휴모토닉. (Park induction 본격 적용 예) -/
theorem selfLoop_isMetaHumotonic : isMetaHumotonic selfLoop := by
  apply isMetaHumotonic.coinduct (pred := fun j => j = selfLoop)
  · -- step: j = selfLoop 이면 witness 가 있다
    intro j hj
    subst hj
    refine ⟨selfLoop, ?_, ?_⟩
    · rw [selfLoop_children_eq]; simp
    · -- Bisim selfLoop selfLoop ∨ (selfLoop = selfLoop)
      -- 두 번째 분기: pred child = (child = selfLoop) 가 성립
      exact Or.inr rfl
  · rfl

-- ============================================================
-- 7. 경계 체크 — atomic 은 메타휴모토닉이 아님
-- ============================================================

/-- atomic 재배맨은 자식이 없어 자기참조 불가 → 메타휴모토닉 아님. -/
theorem atomic_not_meta (p : CHUPiece) :
    ¬ isMetaHumotonic (.atomic p) := by
  intro h
  cases h with
  | fold _ child hmem _ =>
      simp [JaebaeManInf.children] at hmem

-- ============================================================
-- 열린 질문 (파일 하단)
-- ============================================================

/-
열린 질문:
  Q1. `partial def selfLoopAux` 는 kernel 에서 opaque. 따라서
      `selfLoop.children = [selfLoop]` 가 `rfl` 로 풀리지만, 이는
      compiler 레벨 unfolding 이지 definitional equality 보증이 아니다.
      진짜 fold/unfold 정리를 원하면 QpfTypes 의 `codata` 가 필요.

  Q2. `Bisim.coinduct` (mutual) 의 step 형태는 release 사이에 미세하게
      변할 수 있다 (disjunction vs existential vs plain ∀). 현 파일은
      Lean 4.29 기준으로 닫혀있지만, 4.30+ 로 올릴 때 step shape 를
      `#check @Bisim.coinduct` 로 재확인해야 한다.

  Q3. AFA (Aczel anti-foundation) 의 Lean 포팅은 공개된 게 없다.
      `JaebaeManInf` + `Bisim` 조합이 AFA 의 "x = {x} 유일해" 를 근사하지만
      유일성 자체는 별도 증명 필요 ("모든 self-loop 는 서로 bisim").

  Q4. isMetaHumotonic 을 "특이점(singularity)" 과 연결하려면
      CHU 위에 order 를 깔고 fixed point 유일성을 보여야 한다
      (공리12 의 완전 내용). 현재 정의는 "자존성" 축만 포착.

  Q5. Lean kernel 은 νF *data* 를 직접 지원하지 않는다. 진짜 형식화 regime
      (bisim 을 equality 로 승격, corecursor 제공) 이 필요하면
      alexkeizer/QpfTypes 의 `codata JaebaeManInf | ...` 로 재선언하는 것이
      최소 노력 — Mathlib 없이 QpfTypes 한 의존성만으로 가능.

  Q6. covers 의 greatest vs least fixpoint 선택: 우리는 coinductive
      (greatest) 로 갔는데, "무한 깊이에서도 계속 덮는다" 가 자존자 의미에
      가깝기 때문. 유한 inductive covers 와의 관계는 별도 정리가 필요하다
      ("atomic 한정에서 두 covers 는 일치").
-/

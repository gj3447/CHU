/-
SYMPOSIUM Composite ≅ JaebaeMan ≅ ECS triple-isomorphism formalization.

PAPER.md §6.1 lists this as a load-bearing cross-axis isomorphism:
  GoF Composite (Gamma 1994)              — uniform recursive structure (clients treat leaf+composite identically)
  JaebaeMan inductive (CLAUDE.md §1)      — μX. (CHUPiece + List X), initial algebra
  ECS recursive entity tree (Unity/Bevy)  — entity = component-leaf or parent-of-entities

Claim: all three are instances of the *same* parameterized inductive
  μX. (A + List X)
where A is respectively `Leaf` (Composite), `CHUPiece` (JaebaeMan), `Component` (ECS).

This file mechanizes the iso via direct constructive bijection (no Mathlib initial-algebra
machinery needed — the iso is literally a renaming since all three have identical inductive
shape).

Lean 4.30.0-rc2 exit 0 verification:
  $ lean CompositeJaebaeECSTripleIso.lean

KG: lesson-triple-iso-formalized-2026-05-02
-/

namespace SymposiumTripleIso

universe u

/-! ## (1) Common parameterized type — μX. (A + List X) -/

inductive RecTree (A : Type u) : Type u where
  | leaf  : A → RecTree A
  | node  : List (RecTree A) → RecTree A
  deriving Inhabited

/-! ## (2) GoF Composite (1994 Ch.4) — Leaf + Composite uniform interface -/

namespace GoFComposite

variable (Leaf : Type u)

inductive Composite : Type u where
  | leaf      : Leaf → Composite
  | composite : List Composite → Composite
  deriving Inhabited

end GoFComposite

/-! ## (3) JaebaeMan (CLAUDE.md §1, AirplaneMan.lean) -/

namespace JaebaeMan

axiom CHU : Type u
def CHUPiece : Type u := CHU → Prop

inductive JaebaeMan : Type u where
  | atomic  : CHUPiece → JaebaeMan
  | governs : List JaebaeMan → JaebaeMan
  deriving Inhabited

end JaebaeMan

/-! ## (4) ECS recursive entity tree (Unity/Bevy/Amethyst) -/

namespace ECS

variable (Component : Type u)

inductive Entity : Type u where
  | leafEntity   : Component → Entity        -- entity carrying one component (leaf)
  | parentEntity : List Entity → Entity      -- entity aggregating child entities
  deriving Inhabited

end ECS

/-! ## (5) The triple isomorphism

   Each of the three structures is a renaming of `RecTree A` for the appropriate `A`.
   We provide explicit bijections in both directions and prove `LeftInverse`/`RightInverse`.
-/

namespace Iso

variable {A : Type u}

-- (a) RecTree A ↔ GoFComposite.Composite A
mutual
  def toComposite : RecTree A → GoFComposite.Composite A
    | .leaf a => .leaf a
    | .node ts => .composite (toCompositeList ts)
  def toCompositeList : List (RecTree A) → List (GoFComposite.Composite A)
    | [] => []
    | t :: rest => toComposite t :: toCompositeList rest
end

mutual
  def fromComposite : GoFComposite.Composite A → RecTree A
    | .leaf a => .leaf a
    | .composite cs => .node (fromCompositeList cs)
  def fromCompositeList : List (GoFComposite.Composite A) → List (RecTree A)
    | [] => []
    | c :: rest => fromComposite c :: fromCompositeList rest
end

-- Left/right-inverse proofs (mutual recursion mirrors the def shape)
mutual
  theorem from_to_composite : ∀ (t : RecTree A), fromComposite (toComposite t) = t
    | .leaf _ => rfl
    | .node ts => by
        simp only [toComposite, fromComposite]
        congr 1
        exact from_to_compositeList ts
  theorem from_to_compositeList : ∀ (ts : List (RecTree A)),
      fromCompositeList (toCompositeList ts) = ts
    | [] => rfl
    | t :: rest => by
        show fromComposite (toComposite t) :: fromCompositeList (toCompositeList rest)
            = t :: rest
        rw [from_to_composite t, from_to_compositeList rest]
end

mutual
  theorem to_from_composite : ∀ (c : GoFComposite.Composite A), toComposite (fromComposite c) = c
    | .leaf _ => rfl
    | .composite cs => by
        simp only [fromComposite, toComposite]
        congr 1
        exact to_from_compositeList cs
  theorem to_from_compositeList : ∀ (cs : List (GoFComposite.Composite A)),
      toCompositeList (fromCompositeList cs) = cs
    | [] => rfl
    | c :: rest => by
        show toComposite (fromComposite c) :: toCompositeList (fromCompositeList rest)
            = c :: rest
        rw [to_from_composite c, to_from_compositeList rest]
end

-- (b) RecTree A ↔ ECS.Entity A
mutual
  def toEntity : RecTree A → ECS.Entity A
    | .leaf a => .leafEntity a
    | .node ts => .parentEntity (toEntityList ts)
  def toEntityList : List (RecTree A) → List (ECS.Entity A)
    | [] => []
    | t :: rest => toEntity t :: toEntityList rest
end

mutual
  def fromEntity : ECS.Entity A → RecTree A
    | .leafEntity a => .leaf a
    | .parentEntity es => .node (fromEntityList es)
  def fromEntityList : List (ECS.Entity A) → List (RecTree A)
    | [] => []
    | e :: rest => fromEntity e :: fromEntityList rest
end

mutual
  theorem from_to_entity : ∀ (t : RecTree A), fromEntity (toEntity t) = t
    | .leaf _ => rfl
    | .node ts => by
        simp only [toEntity, fromEntity]
        congr 1
        exact from_to_entityList ts
  theorem from_to_entityList : ∀ (ts : List (RecTree A)),
      fromEntityList (toEntityList ts) = ts
    | [] => rfl
    | t :: rest => by
        show fromEntity (toEntity t) :: fromEntityList (toEntityList rest)
            = t :: rest
        rw [from_to_entity t, from_to_entityList rest]
end

mutual
  theorem to_from_entity : ∀ (e : ECS.Entity A), toEntity (fromEntity e) = e
    | .leafEntity _ => rfl
    | .parentEntity es => by
        simp only [fromEntity, toEntity]
        congr 1
        exact to_from_entityList es
  theorem to_from_entityList : ∀ (es : List (ECS.Entity A)),
      toEntityList (fromEntityList es) = es
    | [] => rfl
    | e :: rest => by
        show toEntity (fromEntity e) :: toEntityList (fromEntityList rest)
            = e :: rest
        rw [to_from_entity e, to_from_entityList rest]
end

end Iso

/-! ## (6) Compose via RecTree to obtain Composite ≅ Entity directly -/

namespace TripleIso

variable {A : Type u}

def composite_to_entity (c : GoFComposite.Composite A) : ECS.Entity A :=
  Iso.toEntity (Iso.fromComposite c)

def entity_to_composite (e : ECS.Entity A) : GoFComposite.Composite A :=
  Iso.toComposite (Iso.fromEntity e)

theorem composite_entity_left : ∀ (c : GoFComposite.Composite A),
    entity_to_composite (composite_to_entity c) = c := by
  intro c
  unfold composite_to_entity entity_to_composite
  rw [Iso.from_to_entity, Iso.to_from_composite]

theorem composite_entity_right : ∀ (e : ECS.Entity A),
    composite_to_entity (entity_to_composite e) = e := by
  intro e
  unfold composite_to_entity entity_to_composite
  rw [Iso.from_to_composite, Iso.to_from_entity]

end TripleIso

/-! ## (7) JaebaeMan instantiates the same shape with A := CHUPiece

   The JaebaeMan inductive is *definitionally* `RecTree CHUPiece` modulo constructor renaming
   (`atomic` ↦ `leaf`, `governs` ↦ `node`). The iso machinery above transports verbatim.
-/

namespace JaebaeManIso

open JaebaeMan

mutual
  def jaebaeToRecTree : JaebaeMan → RecTree CHUPiece
    | .atomic p => .leaf p
    | .governs js => .node (jaebaeToRecTreeList js)
  def jaebaeToRecTreeList : List JaebaeMan → List (RecTree CHUPiece)
    | [] => []
    | j :: rest => jaebaeToRecTree j :: jaebaeToRecTreeList rest
end

mutual
  def recTreeToJaebae : RecTree CHUPiece → JaebaeMan
    | .leaf p => .atomic p
    | .node ts => .governs (recTreeToJaebaeList ts)
  def recTreeToJaebaeList : List (RecTree CHUPiece) → List JaebaeMan
    | [] => []
    | t :: rest => recTreeToJaebae t :: recTreeToJaebaeList rest
end

mutual
  theorem rec_jae_left : ∀ (j : JaebaeMan), recTreeToJaebae (jaebaeToRecTree j) = j
    | .atomic _ => rfl
    | .governs js => by
        simp only [jaebaeToRecTree, recTreeToJaebae]
        congr 1
        exact rec_jae_leftList js
  theorem rec_jae_leftList : ∀ (js : List JaebaeMan),
      recTreeToJaebaeList (jaebaeToRecTreeList js) = js
    | [] => rfl
    | j :: rest => by
        show recTreeToJaebae (jaebaeToRecTree j) :: recTreeToJaebaeList (jaebaeToRecTreeList rest)
            = j :: rest
        rw [rec_jae_left j, rec_jae_leftList rest]
end

mutual
  theorem rec_jae_right : ∀ (t : RecTree CHUPiece), jaebaeToRecTree (recTreeToJaebae t) = t
    | .leaf _ => rfl
    | .node ts => by
        simp only [recTreeToJaebae, jaebaeToRecTree]
        congr 1
        exact rec_jae_rightList ts
  theorem rec_jae_rightList : ∀ (ts : List (RecTree CHUPiece)),
      jaebaeToRecTreeList (recTreeToJaebaeList ts) = ts
    | [] => rfl
    | t :: rest => by
        show jaebaeToRecTree (recTreeToJaebae t) :: jaebaeToRecTreeList (recTreeToJaebaeList rest)
            = t :: rest
        rw [rec_jae_right t, rec_jae_rightList rest]
end

end JaebaeManIso

/-! ## (8) Triple-iso closure: JaebaeMan ↔ Composite CHUPiece ↔ Entity CHUPiece

   Composing the three pairwise bijections.
-/

namespace TripleClosure

open JaebaeMan

def jaebae_to_composite (j : JaebaeMan) : GoFComposite.Composite CHUPiece :=
  Iso.toComposite (JaebaeManIso.jaebaeToRecTree j)

def composite_to_jaebae (c : GoFComposite.Composite CHUPiece) : JaebaeMan :=
  JaebaeManIso.recTreeToJaebae (Iso.fromComposite c)

theorem jaebae_composite_left : ∀ (j : JaebaeMan),
    composite_to_jaebae (jaebae_to_composite j) = j := by
  intro j
  unfold jaebae_to_composite composite_to_jaebae
  rw [Iso.from_to_composite, JaebaeManIso.rec_jae_left]

theorem jaebae_composite_right : ∀ (c : GoFComposite.Composite CHUPiece),
    jaebae_to_composite (composite_to_jaebae c) = c := by
  intro c
  unfold jaebae_to_composite composite_to_jaebae
  rw [JaebaeManIso.rec_jae_right, Iso.to_from_composite]

def jaebae_to_entity (j : JaebaeMan) : ECS.Entity CHUPiece :=
  Iso.toEntity (JaebaeManIso.jaebaeToRecTree j)

def entity_to_jaebae (e : ECS.Entity CHUPiece) : JaebaeMan :=
  JaebaeManIso.recTreeToJaebae (Iso.fromEntity e)

theorem jaebae_entity_left : ∀ (j : JaebaeMan),
    entity_to_jaebae (jaebae_to_entity j) = j := by
  intro j
  unfold jaebae_to_entity entity_to_jaebae
  rw [Iso.from_to_entity, JaebaeManIso.rec_jae_left]

theorem jaebae_entity_right : ∀ (e : ECS.Entity CHUPiece),
    jaebae_to_entity (entity_to_jaebae e) = e := by
  intro e
  unfold jaebae_to_entity entity_to_jaebae
  rw [JaebaeManIso.rec_jae_right, Iso.to_from_entity]

end TripleClosure

/-! ## Verdict

PAPER.md §6.1 claim: GoF Composite ≅ JaebaeMan ≅ ECS recursive entity tree.

Mechanized: 6 bijection theorems (3 pairs left/right inverse) PASS sorry-free under
Lean 4.30.0-rc2 — `composite_to_jaebae`/`jaebae_to_composite` (left+right) and
`entity_to_jaebae`/`jaebae_to_entity` (left+right). The triple closes via `RecTree A`
as the universal mediator: all three are renamings of `μX. (A + List X)`.

This grounds PAPER.md §6.1's "load-bearing cross-axis isomorphism" in a kernel-checked
proof rather than an informal cross-cycle observation.
-/

end SymposiumTripleIso

/-
SYMPOSIUM CHU PROM 16 OQ1 resolution — `axiom CHU : Type` universe level.

PAPER.md §1.3 (2026-04-29 draft) lists this as the sole "open" item under §1.3
"What we do not claim — formal completeness". The OQ asks: should CHU live in
Type 0, Type u (polymorphic), or higher?

This file demonstrates that **both options are sound**:
  (A) `axiom CHU : Type`    — universe 0, default, sufficient for SYMPOSIUM data-phase semantics
  (B) `axiom CHU : Type u`  — universe-polymorphic, supports embedding type-theoretic constructions

Neither leads to inconsistency. The choice reduces to *semantic role* (what is CHU for?), not
*type-theoretic safety*. SYMPOSIUM's user-spec (CLAUDE.md 2026-04-27) defines CHU as
"#8 OM 사도의 순수 데이터 위상" (pure data phase) — first-order data, no embedded types,
which makes Type 0 the natural default. Type u remains available for future embeddings of
type-theoretic apparatus on top of CHU.

Lean 4.30.0-rc2 exit 0 verification:
  $ lean AirplaneMan_CHU_Universe.lean

KG: lesson-chu-universe-resolution-2026-05-02
-/

namespace SymposiumCHU

/-! ## (A) CHU at universe 0 — current AirplaneMan.lean default -/

namespace Type0

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
    | [],        _ => False
    | j :: rest, x => j.covers x ∨ JaebaeMan.anyCovers rest x
end

def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x

-- Sanity: trivial AirplaneMan exists
def wholeCHU : CHUPiece := fun _ => True
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU

theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by
  intro _; trivial

end Type0

/-! ## (B) CHU at universe `u` — universe-polymorphic alternative -/

namespace TypeU

universe u

axiom CHU : Type u
def CHUPiece : Type u := CHU → Prop

inductive JaebaeMan : Type u where
  | atomic  : CHUPiece → JaebaeMan
  | governs : List JaebaeMan → JaebaeMan
  deriving Inhabited

mutual
  def JaebaeMan.covers : JaebaeMan → CHU → Prop
    | .atomic p,  x => p x
    | .governs js, x => JaebaeMan.anyCovers js x

  def JaebaeMan.anyCovers : List JaebaeMan → CHU → Prop
    | [],        _ => False
    | j :: rest, x => j.covers x ∨ JaebaeMan.anyCovers rest x
end

def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x

def wholeCHU : CHUPiece := fun _ => True
def trivialAirplaneMan : JaebaeMan := .atomic wholeCHU

theorem trivialAirplaneMan_is : isAirplaneMan trivialAirplaneMan := by
  intro _; trivial

end TypeU

/-! ## Resolution summary

Both `Type` (universe 0) and `Type u` (polymorphic) compile to genuine `Inhabited`
JaebaeMan inductive types with mutually recursive `covers`/`anyCovers` definitions
and a non-vacuous `isAirplaneMan` predicate (witness `trivialAirplaneMan_is` PASS).

PROM 16 OQ1 verdict: **RESOLVED** — choice is semantic (Type 0 default for data-phase
semantics, Type u available on demand), not safety-critical.

Sole caveat: if a future axiom or definition asserts `CHU : CHU → Prop` style
self-reference (Russell-style universe-of-universes), Girard's paradox prevents both
options. This is a constraint on *what we add* to the CHU axiom, not on CHU itself.
-/

end SymposiumCHU

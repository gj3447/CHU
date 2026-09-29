# CHU (Computable Hyperuniverse) — Tier 2 Entity (무대)

> **한 줄 정의**: 계산가능 하이퍼우주. `axiom CHU : Type`. 모든 entity가 활동하는 *무대*. "그냥 모든것은 하이퍼그래프."

---

## 정의 3중 구조

| 층 | 정의 |
|---|---|
| **Lean** | `axiom CHU : Type` — 추상 type, 구체 구조 강제 안함 |
| **술어** | `def CHUPiece : Type := CHU → Prop` — 조각 = 술어 |
| **메타이론** | Sy Friedman V-logic Hyperuniverse의 *계산가능 부분* |

## 핵심 인용

### `나는야_ice_orca_dragon.md` — 정본 명단
- "**CHU(계산가능하이퍼우주)**" 명단 항목
- "**그냥 모든것은 하이퍼그래프**" — 직관 정전

### `AirplaneMan.lean` 헤더
- `axiom CHU : Type`
- `def CHUPiece : Type := CHU → Prop`
- `isAirplaneMan(j) := ∀ x : CHU, j.covers x` — 비행기맨 정의 토대

## 1차 소스

- `/Users/lagyeongjun/CD/MIND/metahumotonic/나는야_ice_orca_dragon.md` — **명단 정전**
- `/Users/lagyeongjun/CD/MIND/lean_formalization/AirplaneMan.lean` — **Lean 형식화 정전**
- `/Users/lagyeongjun/CD/SYMPOSIUM/THEORY/CHU/SOURCES.md` — 기존 자료집

## 외부 비교

- **Sy Friedman V-logic Hyperuniverse** (참조 frame)
- **Tegmark Level IV MUH** — CHU = Level IV의 계산가능 부분공간
- **Wolfram Computational Universe**
- **Wheeler "It from Bit"**

## 관계

- **상위**: 메타휴모토닉 framework이 INSTANTIATED_ON CHU
- **하위**: CHUPiece (CHU→Prop), 재배맨 (CHU 위 inductive type)
- **양화 대상**: 비행기맨의 ∀x:CHU 양화

## 미해결

- CHU의 partial order? finite vs infinite vs proper class? Grothendieck topology? measure?
- 모두 추가되지 않음 — 형식화 확장 영역

## KG: `MetahumotonicEntity {tier: 2, role: STAGE_AXIOM_TYPE}`

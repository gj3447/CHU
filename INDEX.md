# CHU — Computable Hyperuniverse 자료집 INDEX

> **CHU = ORBITAL_MOTION_CLOUD(#8) 사도의 *순수 데이터 위상*** (사용자 정전 2026-04-28)
> **TIER 2 substrate** = TIER 3 #8 (OM 사도) 의 데이터 위상. self-similar fractal 위계.

---

## 현재 엔지니어링 진입점 — CHU 하이퍼그래프 OS

CHU의 현재 USER_PRIMARY 목표는 VM에서 부팅하고 HSWM을 실행할 수 있는 하이퍼그래프 OS다. Lean·PROM 자료는 이 목표의 이론/연구 층이며 완료된 OS의 증거가 아니다.

- [`engineering/README.md`](engineering/README.md) — 현재 그래프 프로필, CID 인벤토리와 증거 질의 진입점
- [`os/README.md`](os/README.md) — 제한된 VM substrate 관찰과 미완료 경계
- [`spec/ARCHITECTURE.md`](spec/ARCHITECTURE.md) — 구현 계층과 종료 조건
- 현재 상태는 `./chu repo status --json`, 프로필은 `./chu repo query profiles --json`, 증거는 `./chu repo query evidence --json`으로 확인
- [`canon/AI_NATIVE_THREE_PRINCIPLES.md`](canon/AI_NATIVE_THREE_PRINCIPLES.md) — AI native 3대원칙 (원문 + 증명 상태)
- [`WHY_HYPERGRAPH.md`](WHY_HYPERGRAPH.md) — Wolfram · ZFC · Transformer · HSWM → 왜 하이퍼그래프인가
- [`plan/CHU_OS_PLAN.md`](plan/CHU_OS_PLAN.md) — 작업계획 (정본 [`plan/chu_os_plan.graph.json`](plan/chu_os_plan.graph.json))
- [`lean/`](lean/) — CHU Lean 11개 정본 사본 (4.34.1, 11/11 통과)
- [`canon/sources/`](canon/sources/) — 사용자 원문
- [`ECOSYSTEM.md`](ECOSYSTEM.md) — CHU · HSWM · USL 관계와 연결 지점
- [`research/LINUX_OS_RESEARCH_2026-09-29.md`](research/LINUX_OS_RESEARCH_2026-09-29.md) — Linux/Ubuntu OS 연구: 호스트 그래프 실측(RDF·SHACL·SPARQL) + 문헌 3축 → 설계 결정 D01–D10
- [`journal/2026-09-29/SESSION.md`](journal/2026-09-29/SESSION.md) — 오늘 작업 정리 (PROV-O 그래프, SHACL·질문 5개 검증, KG 변경안)

## 자료집 구조

```
THEORY/CHU/
├── INDEX.md                          ← 이 파일 (네비게이션)
├── SOURCES.md                        ← 1차 소스 + 핵심 주장 + 인용 + 발전 축
│
├── PROM_16_REPORT.md                 ← /prom 16 사이클: axiom CHU:Type 학문 grounding
├── PROM_16_axis_findings/            ← 4 axis × 4 sub-axis = 16 cells
│   ├── A1_TypeTheory_Lean4.md
│   ├── A2_Hypergraph_NaryUniverse.md
│   ├── A3_Computability_Realizability.md
│   └── A4_HoTT_Univalence_TegmarkIV.md
│
├── PROM_64_REPORT.md                 ← /prom 64 사이클: CHU-Internet binding (2026-04-29 신규)
├── PROM_64_axis_findings/            ← 8 axis × 8 sub-axis = 64 cells
│   ├── A1_GraphAwarePretraining.md
│   ├── A2_PageRankGeneralize.md
│   ├── A3_HGNNScale.md
│   ├── A4_WebAsCorpus.md
│   ├── A5_LiftLowerFormalism.md
│   ├── A6_KGEmbeddingScale.md
│   ├── A7_GraphRAG.md
│   └── A8_AuthorityAbsorption.md
│
├── PROM_16_RANK_ALGEBRA_REPORT.md    ← /prom 16 사이클 (rank-algebra): PageRank=PF eigenvector + Lie group action Lean 4 형식화 (2026-04-29 신규)
├── PROM_16_RANK_ALGEBRA_axis_findings/  ← 4 axis × 4 sub-axis = 16 cells
│   ├── A1_MathlibPF.md
│   ├── A2_PageRankFormalization.md
│   ├── A3_CategoricalPageRank.md
│   └── A4_QuaternionSedenionAlgebra.md
│
└── _findings/                        ← locally preserved raw JSON (PROM v6 L3 layer)
    ├── finding_prom16_chu_*.json       (2 local PROM16 records)
    ├── finding_prom64_chu_*.json       (64 local PROM64 records)
    └── finding_chu-pratt-bridge-*.json (1 local Pratt record)

`PROM_16_axis_findings/finding_prom16_chu_a4s3_unified.json` is a separate unified record outside `_findings/`. Historical reports may describe 16-cell cycles; that describes research scope, not a claim that 16 corresponding PROM16 raw JSON files are locally present.
```

---

## 핵심 정전 (Lean 4)

```lean
axiom CHU : Type
def CHUPiece : Type := CHU → Prop
inductive JaebaeMan : Type
  | atomic : (CHU → Prop) → JaebaeMan
  | governs : List JaebaeMan → JaebaeMan
def covers : JaebaeMan → CHU → Prop
def isAirplaneMan (j : JaebaeMan) : Prop := ∀ x : CHU, j.covers x
```

→ **모든 것은 하이퍼그래프** (사용자 명단 정전):
CHU 의 조각화 = 하이퍼그래프 hyperedge 집합과 isomorphic.

---

## PROM 사이클 요약

### PROM 16 (2026-04-29) — axiom CHU:Type 학문 grounding

- **Cycle:** `prom16-CHU-axiom-foundation-2026-04-29`
- **Lesson:** `lesson-prom16-CHU-axiom-foundation-2026-04-29`
- 4 axes: Type Theory + Lean 4 / Hypergraph + N-ary universe / Computability + Realizability / HoTT + Univalence + Tegmark IV
- 4 sub-axes: 정전 이론 / 산업 표준 / 함정 / 2026 trends
- → CHU 의 mathematical canon 결정화

### PROM 16 (rank-algebra, 2026-04-29) — PageRank as PF eigenvector + Lie group action Lean 4 형식화

- **Cycle:** `prom16-chu-rank-algebra-2026-04-29`
- **Lesson:** `lesson-prom16-chu-rank-algebra-pagerank-instance-2026-04-29`
- **Parent:** `prom64-chu-internet-2026-04-29` ActionPlan #2 follow-up
- **Parent seed:** `seed-prom64-chu-pagerank-as-perron-frobenius-2026-04-29`
- 4 axes: Mathlib PF / PageRank Formalization / Categorical PageRank / Quaternion-Sedenion Algebra
- 4 sub-axes: official-canon / implementation / theory-bridge / critique-pitfall
- → **6 consensus + 1 conflict + 1 singleton + 1 ActionPlan** 결정화 (16/16 RF, full schema)
- 핵심 발견: Mathlib4 인프라 충분 + Cipollina 2025 첫 PF formalization + LT-KGE (`rank = PF eigenvalue of Lie group action`) 통합 framework + Hurwitz 8D boundary + classical.choice noncomputable boundary

### PROM 16 (2026-07-13) — Wolfram hypergraph rewriting ↔ CHU ↔ Ruliad ↔ HoTT (동역학 층 흡수)

- **Cycle:** `prom16-wolfram-chu-ruliad-hott-2026-07-13`
- **Lesson:** `lesson-prom16-wolfram-chu-ruliad-hott-2026-07-13` (lakatos: concept-stretching + proof-analysis)
- 4 axes: Wolfram model formalism / CHU computable hyperuniverse / Ruliad & multicomputation / HoTT homotopy-type bridge
- → **16/16 RF + 1 Hyperedge(cardinality=16)** 결정화. 6 HIGH / 9 MEDIUM(5 pdftotext-pending) / 1 LOW(OPEN)
- 핵심: (1) Wolfram `H₁→H₂` 재작성이 CHU의 **빈 동역학 층**을 채움 (INDEX Lean 정전 "CHU 조각화=hyperedge 집합"의 완성) (2) CHU↔Ruliad 평행은 **외부 소스 없는 SYMPOSIUM-side 합성** = 아직 가설(`:Comment`) (3) HoTT 다리 arXiv:2111.03460 = 가장 load-bearing, **full-text 미검증 pdftotext-pending** (4) Tegmark CUH = 가장 가까운 외부 선례
- **OPEN**: 동역학 층 grounding (A2-S4) · univalence identity 분기 (A4-S2). 열린 채로 유지.
- 상세: `SOURCES.md` §1-3 + 인식적 지위 요약표
- > **⚠️ SUPERSEDED (2026-07-15, 위 "핵심 (2)" 한정)**: "CHU↔Ruliad 평행 = 아직 가설(`:Comment`)"은 후속 전용 사이클 `prom16-chu-ruliad-grounding-2026-07-15`(16셀)이 종결 — **문자 그대로의 동일시는 REFUTED**(3축 독립 DIVERGES: limit-computable 비폐쇄 / plenitude↔unique-totality / category error). 생존 = 재정의 "Ruliad ∞-groupoid의 **computable truncation/thread**". 또한 "핵심 (3) full-text 미검증"은 해소됐으나(2026-07-13 검증) **Prop 4.4의 (∞,1)-topos는 증명 아닌 저자 hedge**로 재정정됨. → `PROM_16_RULIAD_GROUNDING_REPORT_2026-07-15.md` (아래 항목)
- **신규 산출물 (2026-07-13)**:
  - `lean/CHU_WolframRewrite.lean` — 동역학 층 Lean (level 1+2, exit 0). `Rewrite/Step/Path/trans` + `Cell` 2-morphism + `strict_truncation`/`strict_truncation2`.
  - `333_ADAPTER_CONTRACT.md` — decouple(B) 4-port 인터페이스 (ComputeSink/StateStore/BranchBus/Identity → 333 모듈 + ORRR).
  - `chu_core_prototype/chu_core.rs` — BackendLocal Rust 코어 (native run ASSERTS PASS + wasm32 빌드). multiway rewrite explorer, content-hash StateStore = strict-eq truncation.
  - `UNIVALENT_STATESTORE_DESIGN.md` — un-truncated 극(homotopy witness 저장), F1-F3 OPEN 분기.
  - ooptdd: `bhgman_tool/ooptdd/chu_wolfram_adapter.py` (commit 7220da6) — trace-gate GREEN, live dgx Oo LTDD.

### PROM 16 (2026-07-15) — CHU↔Ruliad 동일시 external grounding 검증 (반증 + truncation 재정의)

- **Cycle:** `prom16-chu-ruliad-grounding-2026-07-15` (KG 결정화 **완료·검증**: lesson resolved + 16 RF + 5 seed + impl 링크)
- **Report:** `PROM_16_RULIAD_GROUNDING_REPORT_2026-07-15.md` + `PROM_16_RULIAD_GROUNDING_axis_findings/A{1..4}_*.md`
- 4 axes: Ruliad 형식지위 / homotopy 동일시 / 계산가능성 경계 / 존재론 선례 × 4 lens(primary/critique/formal/falsify)
- → **16셀: GROUNDED 3 · DIVERGES 3 · PARTIAL 8 · UNGROUNDED 2** 집계 (KG 실측 일치)
- 핵심: (1) **문자 그대로 "CHU=Ruliad" REFUTED** (3축 독립 DIVERGES) (2) 재정의 = **CHU = Ruliad ∞-groupoid의 computable truncation/thread** (Lean `Trunc.collapse` 뒷받침) (3) **univalence는 CHU bolt-on 공리** — 소스(2111.03460) 미상속 정정 (4) computable 제약은 Tegmark CUH/Schmidhuber로 GROUNDED
- **OPEN**: truncation 재정의 완전정합성 · n→∞ colimit 존재조건 · univalence 물리정당화. 열린 채.

### PROM 64 (2026-04-29) — CHU-Internet binding + PageRank-style pretraining substrate

- **Cycle:** `prom64-chu-internet-2026-04-29`
- **Lesson:** `lesson-prom64-chu-internet-binding-2026-04-29`
- **사용자 발화 정전:** `user-utterance-internet-as-CHU-binding-2026-04-29` ("인터넷도 CHU에 바인딩")
- **새 lens:** `CHU_Lens_Internet` (CHU 정전의 11번째 lens)
- **검증 가설:** `hypothesis-pagerank-style-pretraining-substrate-2026-04-29`
- 8 axes: Graph-aware Pretraining / PageRank Generalize / HGNN Scale / Web-as-Corpus / Lift-Lower / KG Embedding / GraphRAG / Authority Absorption
- 8 sub-axes: official-docs / community / benchmarks / alternatives / pitfalls / trends-2026 / theory / critique
- → **8 consensus + 2 conflict + 1 singleton + 1 ActionPlan** 결정화

---

## CHU lens 시리즈 (KG :SymConcept)

KG 정전: 2026-04-29 기준 **11개 lens**

| Lens | 설명 |
|---|---|
| `CHU_Lens_HumanThought` | 인간의 생각 = 뇌 하이퍼그래프 라이팅 |
| `CHU_Lens_ContextWindow` | LLM context = CHU 의 서브그래프 |
| `CHU_Lens_Manifold` | 매니폴드 = CHU 의 연속 근사 (그림자) |
| `CHU_Lens_EmbeddingVector` | 임베딩 = CHU 노드의 lossy projection |
| `CHU_Lens_LLMModel` | LLM = 얼어붙은 매니폴드, 교체 가능 엔진 |
| `CHU_Lens_GPU` | GPU = 매니폴드 우주 substrate hardware |
| `CHU_Lens_Token` | 토큰 = 자연어→매니폴드 이산화 컴파일러 |
| `CHU_Lens_Attention` | Attention = 동적 하이퍼엣지 생성 |
| `CHU_Lens_TrainingData` | 학습데이터 = 뇌-CHU 1D 직렬화 |
| `CHU_Lens_Inference` | 추론 = 매니폴드 우주의 라이팅 |
| **`CHU_Lens_Internet`** | **인터넷 = CHU 인스턴스, 11번째 lens (2026-04-29 신규)** |

---

## 권장 집필 순서 (논문 작업 시)

1. **PROM_16_REPORT.md** 부터 — axiom CHU:Type 의 학문적 토대 (Type Theory + Hypergraph + Computability + HoTT)
2. **PROM_64_REPORT.md** 다음 — CHU 의 *substrate evidence* (인터넷 = CHU 인스턴스, PageRank = CHU 랭크 사례, AI 매니폴드 = lossy projection)
3. **SOURCES.md** 와 axis MD 들을 reference 로 사용
4. **_findings/*.json** 은 raw provenance dump (인용 시 직접 참조 가능)

---

## 다리 (Bridge to other THEORY/ folders)

- **`THEORY/비행기맨/`** — CHU 위에 정의된 `isAirplaneMan` (개인 정체성)
- **`THEORY/재배맨/`** — CHU 의 atomic/governs 구조 (cover protocol)
- **`THEORY/OM/`** — CHU 가 ORBITAL_MOTION_CLOUD 사도의 데이터 위상
- **`THEORY/00_공통/세계관_정전.md`** — 12사도 ↔ 5대 무기 다리 (CHU = 무대)

---

## 한 줄 정리

**역사적 이론 표기:** CHU = 계산가능 하이퍼우주 = 모든 것의 데이터 위상. 현재 제품 목표와 증거는 이 문서의 상단 현재 엔지니어링 진입점에서 확인한다.
PROM 16 이 *형식 토대*, PROM 64 가 *물리 evidence* (인터넷 = CHU 인스턴스). 두 사이클이 짝패로 CHU 정전을 떠받침.

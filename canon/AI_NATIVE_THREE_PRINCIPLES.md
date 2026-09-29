# AI native 3대원칙 — CHU 정본

2026-09-29 · `USER_PRIMARY` (원문 2026-09-27) · CHU 저장소로 가져옴

**CHU는 이 세 원칙 위에 서는 하이퍼그래프 OS다.** 원칙 문장은 사용자 원문이고,
"CHU OS에서의 뜻" 열은 AI가 CHU 설계에 옮긴 해석(`SECONDARY_AI`)이다.
원문은 [`sources/`](sources/)에 바이트 그대로 복사했다 (출처: `HSWM/docs/canon/sources/`, HSWM `3ebb780`).

| # | 원칙 (사용자 원문) | CHU OS에서의 뜻 |
|---|---|---|
| ① | **AI는 양파껍질 최외각의 우주 시뮬레이터다.** "물리부터 해도되고 시냅스 연결도로 해도되고 … 뇌의 시멘틱 웨이트 하이퍼그래프 만 진행해도 되는거고. M 의 맵인 이유는 그 모든것들이 맵핑될수있게" — [원문](sources/USER_PRIMARY_HSWM_CROSS_LAYER_MAP_2026-09-27.txt) | 어떤 층에서 시작해도 된다. 층 사이 변환 **M = Map**이 1급 연산이다. 파일·코드·문서·모델은 서로 다른 층의 표현이고, CHU는 그 사이의 매핑을 하이퍼엣지로 가진다. |
| ② | **하이퍼그래프는 우주를 이해·기술하는 최소 비용 체계다.** "페르마의 원리가 빛의 최단시간 경로인것처럼 … 트랜스포머도 수렴진화해서 하이퍼그래프가 되었고 그 울프람의 우주시뮬레이터도 하이퍼그래프 기반이고 수학의 기초 zfc 공리계도 하이퍼그래프로 쌓아올려졋는데" — [원문](sources/USER_PRIMARY_HSWM_MINIMUM_COST_HYPERGRAPH_2026-09-27.txt) | 저장·표현의 기본 단위는 n항·역할 있는 하이퍼엣지다. 폴더 트리(단일 부모)는 이 체계의 비싼 특수형이므로 정본에서 뺀다. 근거 정리: [`../WHY_HYPERGRAPH.md`](../WHY_HYPERGRAPH.md). |
| ③ | **AI는 근본적으로 소프트웨어다.** "llm 은 그 하나의 실행단위 rom 같은거고 메모리 거대한 메모리가 그 chu 야 … 코드실행도 하이퍼그래프 db 기반 … 그 chu 에 있는 그 시멘틱 웨이트들이 프로그램인거고 … 컴퓨터 구조에 대응해서" — [원문](sources/USER_PRIMARY_CHU_SOFTWARE_ARCHITECTURE_2026-09-27.txt) | 컴퓨터 구조 대응이 곧 CHU OS 커널 구조다: **LLM = ROM(실행 단위)**, **CHU 하이퍼그래프 = 메모리**, **Semantic Weight = 프로그램**, 실행 = 국소 연산자가 그래프를 읽고 재작성. "문서라고는 없을거야" → 문서는 그래프에서 만든 뷰. |

## 범위 (사용자 정의)

- **HSWM은 LLM 전용**, **CHU는 진짜 월드모델과 HSWM을 모두 포함하는 추상적으로 거대한 개념**이다.
  — [원문](sources/USER_PRIMARY_CHU_HSWM_SCOPE_2026-09-27.txt)
- **CHU = 하이퍼그래프 기반 OS.** 파일·문서 구조도 폴더/파일이 아닌 깔끔한 하이퍼그래프 노드.
  — [원문](sources/USER_PRIMARY_CHU_HYPERGRAPH_OS_2026-09-29.txt)
- 두 정의는 양립한다: CHU 개념 전체 ⊇ HSWM, 그리고 **CHU OS**는 그 개념을 작업환경으로
  실현하는 유한 구현 인스턴스다. OS 인스턴스를 CHU 개념 전체와 동일시하지 않는다.

## 증명 상태 (2026-09-29 재검증)

세 원칙의 **계산적 핵심**은 HSWM에서 Lean 4로 기계 검증돼 있다. 이 세션에서 HSWM
`formal/`을 scratchpad로 복사해 import 사슬 14개 모듈을 Lean 4.34.1로 컴파일 — 전부 통과,
`sorry` 0, 신규 `axiom` 0. (HSWM 저장소는 건드리지 않음.)

| 원칙 | Lean 파일 (HSWM/formal) | 증명된 것 | 아직 가설인 것 |
|---|---|---|---|
| ① | [`HSWMOperationalAbstraction.lean`](../../HSWM/formal/HSWMOperationalAbstraction.lean), [`HSWMMultiscaleSimulation.lean`](../../HSWM/formal/HSWMMultiscaleSimulation.lean) | fibre 조건 ⟺ 출력·허용성·Step·Learn을 보존하는 층 연산 존재; 유한 이력 보존·합성; 예측 비트를 버리면 실패 | 실제 물리→뇌→의미 매핑의 존재, 절대 최외각 |
| ② | [`HSWMHypergraphCostConditions.lean`](../../HSWM/formal/HSWMHypergraphCostConditions.lean) | 역할 있는 n항 관계의 incidence 왕복 무손실; 선언된 비용 모형에서의 조건부 우위·동률·역방향 반례 | 모든 표현·과제에서의 **보편** 최소 비용, Transformer/Wolfram/ZFC의 **수렴진화** |
| ③ | [`HSWMSemanticSoftware.lean`](../../HSWM/formal/HSWMSemanticSoftware.lean) | 국소 인터프리터가 그래프 프로그램 실행; 계산된 관계 수정이 다음 실행을 바꾸고 유한 점수를 엄격히 올림 | 실제 pretrained LLM이 `Faithful` 연산자라는 것, CHU 전체의 계산가능성 |

해설 원본: [세 철학 Lean 번역](../../HSWM/docs/research/HSWM_THREE_PHILOSOPHIES_LEAN_2026-09-27.md),
[연산적 증명](../../HSWM/docs/research/HSWM_OPERATIONAL_PHILOSOPHY_PROOF_2026-09-28.md).

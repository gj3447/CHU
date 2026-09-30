# CHU OS 작업계획 (그래프 엔지니어링)

> **정체성**: CHU = 하이퍼그래프 기반 OS. 폴더 트리 없음 — 모든 것은 노드 + n-ary 하이퍼엣지이고,
> 경로/폴더는 질의로 만든 뷰다. (정전: [`../AGENTS.md`](../AGENTS.md))
>
> **정본 = [`chu_os_plan.graph.json`](chu_os_plan.graph.json)**. 이 문서는 그 그래프의 사람용 뷰다.
> 계획 자체도 하이퍼그래프(B-graph): 하이퍼엣지의 tail이 **전부** 끝나야 head를 착수한다.
> 검증: `python3 plan/check_plan.py` (참조 무결성 · 비순환 · 고아 노드 · 임계 경로).
>
> **토대**: [AI native 3대원칙](../canon/AI_NATIVE_THREE_PRINCIPLES.md) ·
> [왜 하이퍼그래프인가 (Wolfram·ZFC·Transformer·HSWM)](../WHY_HYPERGRAPH.md).

---

## 실행 명세 — 2026-09-30

[구현 순서와 검증 계약](../spec/ARCHITECTURE.md)을 먼저 읽는다.
T01–T05의 데이터·정체성·연산·뷰·Lean 매핑 문서를 작성하고 실제 5종 파일로
내용 주소, 다중 소속, 원자적 변경, 두 분기, RDF 왕복과 독립 SPARQL 결과를 검증한다.
`./chu model demo --json`, `./chu model roadmap --json`, `./chu check --only kernel-contract --json`.
참조 모델은 메모리 실행 명세다. T10–T15 영속 Rust 커널은 여전히 후속 구현이며,
현재 착수 가능한 작업은 T07(연구)과 T10(Rust 라이브러리 분리)다.

## 1. 목표 아키텍처 (레이어 = 노드 속성 `layer`)

| 레이어 | 역할 | 기존 자산 재사용 |
|---|---|---|
| spec | 데이터 모델·정체성·연산·뷰 명세 | `axiom CHU : Type`, JaebaeMan, `CHU_WolframRewrite.lean` |
| kernel | 콘텐츠 주소 store, 트랜잭션 = 재작성 규칙, 이력 = multiway | `chu_core.rs` (HyperState, Rule, 4 포트, UnivalentStateStore) |
| query | 하이퍼엣지 패턴 질의 → 뷰 | `chu_core.rs` 규칙 LHS 매처 |
| compat | 트리 ingest/export, FUSE 가상 디렉터리 | — (트리는 호환 뷰일 뿐, 정본 아님) |
| shell | CLI · 그래프 작업공간 UI · 에이전트 포트 | HSPINE (의지/권한도 노드로) |
| dogfood/dist | CHU 저장소를 CHU 안에서 운영, 333 분산 백엔드 | `333_ADAPTER_CONTRACT.md` |

설계 불변식:
1. **I-노드**: 정체성은 CID(내용). 이름·경로는 가변 라벨/뷰.
2. **I-다중소속**: 한 노드는 임의 개수의 그룹 하이퍼엣지에 속한다. 단일 부모 강제 금지.
3. **I-규칙**: 모든 변경은 `H₁→H₂` 재작성 1회 = 트랜잭션 1회. 이력은 버리지 않는다(multiway).
4. **I-최소공리**: Lean 쪽 신규 axiom 0 (기존 I1 유지).
5. **I-3대원칙**: ① 층 변환 M = Map이 1급 연산 · ② 표현 단위 = n항 역할 하이퍼엣지, 저장 형식은 비용 측정으로 선택 ·
   ③ LLM = ROM(실행 단위), CHU 그래프 = 메모리, Semantic Weight = 프로그램.

## 2. 마일스톤

| M | 이름 | 종료 조건 (게이트) | effort |
|---|---|---|---|
| M0 ✓ | 정체성 고정 + 3대원칙 수입 | AGENTS.md 정전, 3대원칙·WHY_HYPERGRAPH, CHU Lean 11개 수입·재검증 | 1.5일 |
| M1 | 명세 + Linux 연구 | T01–T05 명세·참조 검증 ✓, 신규 axiom 추가 0; T07 미완료, Linux OS 연구 ✓(T09) | 10.5일 |
| M2 | 커널 | 영속 store + txn + 분기 + 권한 grant(T15), `cargo test` green | 13일 |
| M3 | 질의 | 패턴 질의 + 최소 문법 + RDF/SHACL 표준 교환(T22), 골든 테스트 | 6일 |
| M4 | 호환 | CHU 저장소 ingest→export 왕복 diff 0, FUSE(선택), Linux 시스템 그래프 ingest(T34), 트리 vs 하이퍼그래프 비용 측정(T06) | 13일 |
| M5 | 셸 | CLI e2e, UI·에이전트가 같은 txn 로그 생성 | 8일 |
| M6 | 셀프호스팅/분산 | 이 계획 그래프까지 CHU 노드로 적재, 333 2-피어 동기화 | 8일 |

총 60 작업일(기존 추정, 완료 9 / 남은 51). **전체 의존 경로의 임계 길이 23.5일**
(완료 작업을 포함한 원래 추정이며 납기 확약 아님):
`T00 → T08 → T09 → T02 → T11 → T12 → T20 → T21 → T40 → T50 → T52`

## 3. 위상 레이어 (같은 줄 = 병렬 가능)

```
L0: T00
L1: T08, T10
L2: T03, T04, T07, T09
L3: T01, T02
L4: T05, T11
L5: T12
L6: T13, T20
L7: T14, T15, T21, T22, T30
L8: T31, T32, T34, T40
L9: T06, T33, T41, T42, T50
L10: T51, T52
```

## 4. 의존 하이퍼그래프

`python3 plan/check_plan.py --mermaid`로 재생성.

```mermaid
flowchart LR
  T00["T00 ✓ CHU=하이퍼그래프 OS 정체성 고정"]
  T08["T08 ✓ AI native 3대원칙 + 왜 하이퍼그래프(Wo"]
  T09["T09 ✓ Linux/Ubuntu OS 연구: 호스트 그래프 "]
  T01["T01 ✓ 데이터 모델 명세: Node/Hyperedge/Ty"]
  T02["T02 ✓ 정체성 명세: CID(내용 주소) + 라벨(가변 이"]
  T03["T03 ✓ 연산 명세: 모든 변경 = 재작성 규칙 H1->H2"]
  T04["T04 ✓ 뷰 명세: path/폴더 = 질의 투영"]
  T05["T05 ✓ Lean 정합 매핑: 명세 ↔ CHU_Wolfram"]
  T07["T07 수렴진화 검증 설계: Wolfram·ZFC·Tran"]
  T10["T10 chu_core.rs를 crate로 분리(chu-k"]
  T11["T11 blob store: 콘텐츠 주소 저장(파일 본문)"]
  T12["T12 영속 하이퍼그래프 store: append-only"]
  T13["T13 트랜잭션 = 규칙 적용 1회, 로그 = multiw"]
  T14["T14 분기/병합: multiway 가지 + Univale"]
  T15["T15 권한 grant 하이퍼엣지 {grantor, gra"]
  T20["T20 패턴 질의: 규칙 LHS 매처를 질의 엔진으로 일반"]
  T21["T21 질의 언어(최소 텍스트 문법)"]
  T22["T22 표준 교환: incidence 인코딩 RDF/JSO"]
  T30["T30 ingest: 디렉터리 트리 -> 하이퍼그래프 (폴"]
  T31["T31 링크 추출: md 링크/JSON 참조를 하이퍼엣지로"]
  T32["T32 export: 뷰 -> 트리 물질화(호환용, 정본 "]
  T33["T33 FUSE 마운트(선택): 질의 뷰를 가상 디렉터리로"]
  T34["T34 Linux 시스템 그래프 ingest: dpkg 절"]
  T06["T06 비용 측정: CHU 저장소를 폴더 트리 vs 하이퍼"]
  T40["T40 CLI: add/link/find/view/log/"]
  T41["T41 그래프 작업공간 UI(노드/하이퍼엣지 탐색·편집)"]
  T42["T42 에이전트 포트: 작업/에이전트/HSPINE 의지도 "]
  T50["T50 셀프호스팅: CHU 저장소 문서를 CHU 안에서 관"]
  T51["T51 기존 이론 문서 재배치: 이론 = 커널 근거 문서 "]
  T52["T52 333 백엔드: StateStore/BranchBu"]
  T00 & T08 --> T01 & T02 & T03 & T04
  T01 & T02 & T03 --> T05
  T00 --> T10
  T02 & T10 --> T11
  T01 & T02 & T11 --> T12
  T03 & T12 --> T13
  T13 & T05 --> T14
  T12 & T04 --> T20
  T20 --> T21
  T13 --> T30
  T30 --> T31
  T30 & T20 --> T32
  T32 & T13 --> T33
  T21 & T13 & T14 --> T40
  T40 --> T41 & T42
  T31 & T32 & T40 --> T50
  T50 --> T51
  T14 & T50 --> T52
  T00 --> T08
  T08 --> T07
  T30 & T31 & T07 --> T06
  T08 --> T09
  T09 --> T01 & T02
  T13 & T02 --> T15
  T20 & T01 --> T22
  T30 & T09 --> T34
  T15 --> T42
```

## 5. 운영 규칙 (표준 그래프 엔지니어링)

- **그래프가 정본**: 작업 추가·변경은 JSON을 먼저 고치고 `check_plan.py`가 OK일 때만 커밋.
- **노드 = 검증 가능한 산출물**: 모든 노드는 `deliverable`과 `verify`를 가진다. 검증 없는 노드는 금지.
- **하이퍼엣지 = 합류 조건**: 여러 선행이 함께 필요하면 이진 엣지 여러 개가 아니라 tail 집합 하나로 적는다.
- **임계 경로 우선**: 착수 순서는 임계 경로 노드 → 같은 레이어의 나머지.
- **재계획 = 재작성**: 계획 변경도 그래프 재작성으로 보고, 이유를 커밋 메시지에 남긴다.

## 6. 열린 결정 (사용자 확인 필요)

- OS의 범위: 사용자 공간 작업환경 OS(현재 가정 — [Linux 연구](../research/LINUX_OS_RESEARCH_2026-09-29.md) D04가 근거를 보강) vs 부트 가능한 커널 수준.
- 영속 백엔드: 자체 append-only 로그(현재 가정) vs SQLite/RocksDB 같은 임베디드 DB 위에 구현.
- 정본 소유: SYMPOSIUM/THEORY/CHU와 이 저장소 중 어느 쪽이 정본인지 (Provenance 참조).

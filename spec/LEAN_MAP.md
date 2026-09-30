# T05 — Lean 이론과 실행 계약의 대응

v0.1 · 2026-09-30 · `SECONDARY_AI`. 신규 Lean axiom을 추가하지 않는다.
기존 증명의 범위를 production kernel 검증으로 확대하지 않는다.

| 기존 Lean 정의 (`lean/CHU_WolframRewrite.lean`) | 실행 설계의 대응 | 아직 증명하지 않은 부분 |
|---|---|---|
| `CHU : Type` | 내용 snapshot을 다루는 상태 공간 | 실제 인코딩/저장소가 opaque type의 모델임을 보이는 정리 |
| `Rewrite := CHU → CHU` | 검증된 요청이 base를 result로 옮기는 단계 | 매칭 실패 가능한 부분 함수와 Lean의 전체 함수 사이의 refinement |
| `Step` | 허용한 operation의 성공 사건 | 타입 검사·권한 집행·commit의 soundness |
| `Path`, `Path.trans` | 상태와 별도로 보존하는 실행 사건의 경로 | 실제 durable event ancestry 및 composition 검증 |
| `Reach`, `Trunc.collapse` | 존재 여부만 답하는 도달 가능성 projection | 저장 CID가 모든 수학적 동일시를 구현한다는 주장은 하지 않음 |
| `Cell`, `Cell.vtrans` | 검증 가능한 별도 higher witness 계층 | 참조 모델에는 Cell/witness 구현이 없으며 T14에서 연결 |

관계 순서, strict content identity, 역할 있는 incidence를 보존하는 검사는
실행 명세에 대한 유한 테스트다. 이를 Lean의 ∞-구조 전체 구현이나 Ruliad 동일성
증명으로 보고하지 않는다. 원래 Rust demo의 Relabel/Merge witness도 저장 커널에
연결하기 전 검증기·지원 크기·실패 경계를 다시 지정해야 한다.

검증: `./chu check`가 기존 Lean 11개를 그대로 컴파일하고 실제 `sorry` 경고를 거부한다.
이번 T05 산출물은 정의별 매핑과 미증명 경계이며 Lean 코드/공리 변경은 없다.

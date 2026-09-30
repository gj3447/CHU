# T03 — 변경은 원자적 재작성

v0.1 · 2026-09-30 · `SECONDARY_AI`. 실행 가능한 의미는 `scripts/chu_model.py`에 있다.

요청: `{base_state_cid, request_id, actor, operation, delta}`.
delta는 추가 콘텐츠 bytes, 삭제 node CID, 추가 typed edge, 삭제 edge CID로 구성한다.
base를 복사해 후보 상태를 만들고 타입·endpoint·삭제 전제를 전부 검사한 다음,
결과 snapshot과 실행 사건을 함께 기록한다. 실패하면 둘 다 바뀌지 않는다.

| operation | 허용 delta | 실패 조건 |
|---|---|---|
| create | 콘텐츠 추가 | 빈 추가 또는 제거/관계 변경 혼합 |
| link | 관계 추가 | 빈 추가, 미등록 타입/역할, endpoint 부재 |
| unlink | 관계 제거 | 대상 관계가 base에 없음, 다른 변경 혼합 |
| retag | 관계 제거 + 관계 추가 | 둘 중 하나 누락, 타입/endpoint 오류 |
| delete | 콘텐츠 제거 + 필요하면 incident 관계 제거 | 남은 관계가 제거 노드를 참조하거나 대상이 없음 |

참조 API가 ‘tag’ 고유 타입을 가정하지는 않는다. retag는 group/의미 바인딩 관계를
대체하는 일반 edge replacement다. create/link는 동일 내용을 다시 추가해도 dedup한다.
delete는 현재 상태에서의 제거이며 역사적 콘텐츠의 물리 삭제/GC가 아니다.

같은 request ID와 같은 base·actor·정규화 delta는 기존 결과를 반환한다.
같은 request ID를 다른 입력에 재사용하면 거부한다. 다른 request ID라면 결과 CID가
같아도 별도 사건을 남긴다. 사건에는 base/result, actor, 요청 ID, operation,
delta digest와 관측 시간을 기록하며 RDF에서는 PROV-O Activity로 투영한다.
상태 CID에는 실행 시간이나 actor를 넣지 않는다.

같은 base에 두 개의 유효한 변경을 적용하면 두 가지가 생긴다. 자동으로 한 가지를
덮어쓰거나 병합하지 않는다. 정체성 중복 제거는 실행 경로의 삭제를 뜻하지 않는다.
state를 되돌리는 유효한 재작성도 가능하므로 내용 상태 사이의 그래프에 전역 DAG를
요구하지 않는다. 실제 branch-head의 compare-and-swap과 사건 ancestry는 T13/T14의 계약이다.

참조 모델의 원자성은 단일 프로세스 메모리에서의 **검증 실패 무변경**이다.
영속 kernel은 객체·사건·branch-head를 하나의 durable commit 경계로 묶고,
재시작, 부분 쓰기, 실패 주입, 동시 writer, 재시도 및 stale base를 시험해야 한다.
그 시험 전에는 crash-safe 또는 exactly-once 외부 실행이라고 부르지 않는다.

권한은 요청 필드나 그래프 연결만으로 생기지 않는다. 이 모델은 모델 상태만 변경한다.
실제 OS 작업은 T15의 범위·만료·철회 집행과 T42 adapter가 마련된 뒤 수행한다.

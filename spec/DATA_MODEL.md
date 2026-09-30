# T01 — 노드·하이퍼엣지·타입

v0.1 · 2026-09-30 · `SECONDARY_AI` 구현 명세. [아키텍처](ARCHITECTURE.md)와
[사용자 정체성](../docs/agent-rules/OWNER.md)을 따른다.

`Node = (cid, bytes)`. 파일, 라벨, 작업 요청, 에이전트 설명도 bytes를 가진 노드로
표현할 수 있다. 운영 주체의 서명이나 권한은 설명 노드만으로 보장되지 않는다.
참조 모델은 실제 `README.md`, 계획 JSON, Rust core, Python 계획 검사기,
Lean 재작성 파일을 바이트 그대로 읽는다. 확장자는 경로 뷰의 정보이며 정체성이 아니다.

`Hyperedge = (relationType, ordered participants[role, nodeCID])`.
순서와 역할을 모두 보존한다. 같은 노드가 여러 관계 또는 같은 관계의 다른 위치에
등장할 수 있다. 관계 목록 자체의 저장 순서는 의미가 없으며 동일 관계 바이트는 dedup한다.
반복 사건은 내용이 같은 관계를 복제하는 대신 별도 사건으로 기록한다.

v0.1에 등록한 타입:

| relationType | ordinal 0 | ordinal 1..n | 의미 |
|---|---|---|---|
| `group` | `group` 노드 1개 | `member` 1개 이상 | 다중 소속 묶음. 부모가 하나여야 한다는 제약 없음 |
| `requires-any` | `subject` 노드 1개 | `candidate` 1개 이상 | 하나의 대안 절. 후보를 별개 필수 의존성으로 분해하지 않음 |

최초 실행 profile의 최소 arity는 2다. CHU 일반 모델의 unary/nullary 가능성을
부정하는 공리가 아니며, 새 타입은 role·arity·질의·음성 대조군을 함께 추가한다.
하이퍼엣지 자체를 대상으로 삼을 때는 그 버전 인코딩 bytes도 Node로 명시적으로 추가해
참조한다. 암묵적 endpoint 생성이나 재귀적으로 자기 CID를 포함하는 인코딩은 하지 않는다.

`Snapshot = (set of node CIDs, set of edge CIDs)`. endpoint는 **그 snapshot 안에**
존재해야 한다. 다른 분기 어딘가에 있다는 것만으로 유효하지 않다.
스냅숏 및 그룹 관계는 일반 그래프이므로 전역 DAG 조건을 부과하지 않는다.
비순환은 계획의 `requires`와 트리로 내보내는 특정 뷰에만 적용한다.

RDF 교환은 기존 `research/linux_os`의 `vocab#` 명칭을 재사용한다.
`Hyperedge → hasIncidence → Incidence → node → Node`에 role/ordinal을 붙이고,
`Snapshot → containsEdge/containsNode`로 조회 범위를 보존한다.
[ontology.ttl](ontology.ttl)에 모든 로컬 술어의 방향·domain/range·cardinality를,
[shapes.ttl](shapes.ttl)에 실행 제약을 적었다. role 누락, 중복/비연속 ordinal,
arity 불일치, 미등록 타입/술어, 끊긴 endpoint와 다른 snapshot의 노드 참조를 거부한다.

참고: [W3C n-ary relation pattern](https://www.w3.org/TR/swbp-n-aryRelations/)은
관계를 개체로 표현하는 패턴의 근거다. 역할·순서·CID profile의 세부는 CHU의 설계 결정이다.

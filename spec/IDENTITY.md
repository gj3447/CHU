# T02 — 내용 정체성과 가변 바인딩

v0.1 · 2026-09-30 · `SECONDARY_AI`. 사용자 정체성의 **노드 = 내용 주소**를 유지한다.

| 대상 | 내용 주소 입력 | ID |
|---|---|---|
| 원본 콘텐츠 | 파일의 실제 raw bytes, 변환 없음 | `urn:sha256:` + 소문자 hex 64자리 |
| 관계 객체 | 아래 `chu-edge/v1` 인코딩 | 같은 SHA-256 URN 규칙 |
| 상태 객체 | 아래 `chu-state/v1` 인코딩 | 같은 SHA-256 URN 규칙 |
| 실행 사건 | 요청 key·actor·base·delta의 별도 기록 | 내용 상태와 구분하는 사건 식별자 |

관계의 인코딩은 `{"schema":"chu-edge/v1","type":name,"participants":[{"role":role,"node":CID},...]}`.
상태의 인코딩은 `{"schema":"chu-state/v1","nodes":[sorted unique CIDs],"edges":[sorted unique CIDs]}`.
두 구조는 UTF-8 JSON, key 사전순, 구분자 `,`/`:`, 공백 없음, `ensure_ascii=False`로
인코딩한다. 허용 필드는 문자열·배열·객체뿐이며 JSON number/NaN은 사용하지 않는다.
participants의 배열 순서는 정렬하지 않는다. Unicode 정규화도 하지 않는다.
스키마 버전도 hash 입력에 포함되며 인코딩 변경은 새 버전과 명시적 이관이 필요하다.

이것은 이 제한된 객체 문법의 CHU encoding이며 임의 JSON의 표준 canonicalization을
구현했다고 주장하지 않는다. Turtle 직렬화의 공백·prefix·blank node 이름을 hash하지 않는다.
[RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/)은 RDF dataset의
blank node 정규화 문제를 다룬다. 그것을 raw 콘텐츠 CID나 CHU 상태 encoding과 혼동하지 않는다.

연구 D06의 ‘안정 노드 ID / 버전 CID 분리’는 **가변 문서의 handle과 불변 콘텐츠 노드**의
분리로 해석한다. logical handle이 필요하면 고정 식별자를 담은 immutable record도 하나의
내용 노드로 만들고, 현재 버전을 가리키는 binding 관계를 재작성한다. handle이나 파일 경로가
콘텐츠 노드의 CID를 대체하지 않는다. 일반 handle binding은 후속 Rust 커널 작업이며,
이번 참조 모델은 콘텐츠와 group label 노드만 실행한다.

이름 변경은 label/binding 관계 변경이고 파일 body CID는 유지된다. body 수정은 새 CID다.
이전 버전은 이력에서 보존한다. 경로는 `pathView`로만 기록한다.
같은 bytes의 충돌 내성은 SHA-256에 의존하며 악의적 충돌에 대한 수학적 유일성 증명은 아니다.

기존 `chu_core.rs`의 `DefaultHasher`/`u64` CID는 데모 상태 탐색용이다.
그 값을 영속 content CID로 승격하거나 SHA-256과 같은 ID라고 취급하지 않는다.
univalent 동일시는 별도 witness를 요구하며 strict byte equality, label similarity,
동일 결과에 도달했다는 사실 중 어느 것도 임의 두 상태의 동일시를 자동 허가하지 않는다.

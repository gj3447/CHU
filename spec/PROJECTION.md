# T04 — 경로와 폴더는 질의 뷰

v0.1 · 2026-09-30 · `SECONDARY_AI`.
질의 입력은 snapshot CID, root/group 노드, relation/role 조건과 한도다.
출력은 content CID와 선택적 표시 label/path의 배열이다. 현재 참조 구현은
group의 직접 member만 조회하므로 순환 그룹도 무한 재귀를 만들지 않는다.

`./chu model demo --json`은 같은 README CID를 다음 두 위치에 보여 준다.

```text
implementation/<README content digest>
theory/<README content digest>
```

두 경로의 target은 같은 노드다. 한 group에서 unlink해도 다른 group의 소속,
원본 bytes 및 이전 snapshot은 유지된다. 경로가 동일하다는 이유로 두 CID를 합치지 않는다.
source 파일 경로도 별도 `chu:pathView` 정보이며 내용 hash에는 들어가지 않는다.

RDF 질의에서도 반드시 snapshot을 선택한다. history 전체에서 `group`만 검색한 결과를
현재 소속으로 표시하면 제거한 관계가 되살아 보인다. 저장된 질의는 `?state`를 결과에
반환하며 caller가 원하는 snapshot을 선택할 수 있다.

후속 파일시스템 projection 계약:

- 표시명 충돌은 모호함 오류 또는 CID suffix로 해소하고 임의 덮어쓰지 않는다.
- absolute path, `..`, separator, NUL 등의 이름은 root 밖으로 내보낼 수 없다.
- 순환은 방문 집합/깊이 제한으로 끊거나 명시적 link로 표현한다. 그래프 원본을 삭제하지 않는다.
- view materialization은 snapshot과 policy version을 기록하고 ingest/export bytes를 비교한다.
- FUSE는 같은 질의/변경 API를 사용하는 adapter다. FUSE가 없어도 core를 검증할 수 있어야 한다.

이 파일의 path 제한은 T32/T33의 구현 계약이며, 이번 메모리 데모가 실제 파일시스템에
트리를 내보내거나 FUSE를 마운트한 것은 아니다.

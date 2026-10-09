# CHU 영속 재작성 연구 — SQLite 후보와 실패 경계

2026-10-09 · `SECONDARY_AI` · 기존 T11–T14를 위한 구현 탐색/실험.
**연구용 Python adapter를 만들고 30개 시나리오를 실행했다. 제품용 Rust 커널 채택이나
T10–T14 완료 선언은 아니다.** HOH Interface는 기존 사용자 결정대로 유지한다.

## 이번에 답한 질문

CHU의 raw-byte CID와 역할·순서가 있는 n항 관계를 유지하면서,
`객체 + snapshot + 사건 + branch head`를 한 SQL transaction으로 묶으면
프로세스 종료·중복 전달·동시 작성 시 어떤 결과가 남는가?

출발점은 CHU `72916fc`의 [메모리 모델](../../scripts/chu_model.py),
[정체성](../../spec/IDENTITY.md), [데이터 모델](../../spec/DATA_MODEL.md),
[재작성 계약](../../spec/OPERATIONS.md)이다. 이 모델의 인코딩과 검증기를 직접 재사용했다.
기존 [WHAT_IS_SQLITE](https://github.com/gj3447/WHAT_IS_SQLITE) 및
[CHU 백엔드 연구](https://github.com/gj3447/HOW_TO_CHU_BACKEND)에서 이어지는 작은 실험이다.
하이퍼그래프 재작성 이론 전체나 외부 부작용의 exactly-once 실행은 시험 대상이 아니다.

## 핵심 발견: 상태 CID와 쓰기 순서는 다르다

`A → B → A`에서 처음과 마지막 상태의 내용은 같으므로 CID도 같아야 한다.
이때 **현재 head CID == 요청의 base CID** 조건만 검사하면, 중간 변경을 보지 못한
오래된 요청도 통과할 수 있다. 실제 SQL의 CID-only UPDATE가 이 경우 1행과 일치하는
음성 대조군을 실행했고 rollback했다. 수정 후보는 `(base CID, branch revision)`을
함께 검사하므로 예전 revision 0의 요청을 현재 revision 2에서 거부했다.

이 결과는 CID 정의를 바꿀 이유가 아니다. 내용 정체성과 실행 이력/동시성 토큰을
분리해야 한다는 근거다. revision은 상태 CID의 hash 입력에 넣지 않는다.
현재 실험의 정수 revision은 삭제·재생성하지 않는 branch 수명 안에서만 단조 증가한다.
향후 branch 재생성·백업 복원·리더 교체까지 다룰 때는 generation/epoch 또는 검증된
사건 tip을 함께 사용하는 계약이 필요하다. 그 경우는 아직 시험하지 않았다.

## 실험 구현

[chu_storage_probe.py](../../scripts/chu_storage_probe.py)는 연구 전용 adapter다.
`objects`에는 실제 콘텐츠·관계·상태 인코딩 bytes를 SHA-256으로 저장하고,
`states`는 snapshot 목록, `events`는 별도 실행 사건, `branches`는 조회 가능한 head를
기록한다. SQL 테이블과 branch 표시 이름은 물리 저장/제어 메타데이터이며 콘텐츠 CID를
대체하는 폴더 정본이 아니다. 관계의 participant 순서를 정렬하지 않는다.

쓰기 순서는 다음과 같다.

1. `BEGIN IMMEDIATE`로 쓰기 transaction을 시작한다.
2. request ID가 이미 있으면 fingerprint를 대조해 원래 결과를 반환하거나 충돌을 거부한다.
3. branch의 state와 revision을 함께 검사한다.
4. 기존 `Model.apply`로 후보를 검증하고, 콘텐츠·상태·사건을 저장한다.
5. 같은 state/revision을 조건으로 head를 CAS 갱신한 뒤 `COMMIT`한다.

재시도 lookup을 stale-head 검사보다 먼저 해야, 커밋은 끝났지만 응답을 받지 못한 요청이
원래 결과를 다시 받을 수 있다. fingerprint에는 base, branch, revision, actor와 정규화된
delta를 넣었다. request ID는 이 연구 DB 안에서 전역이다. 실제 다중 사용자 API의
principal별 idempotency 범위는 아직 결정하지 않았다. actor URN은 인증이 아니다.

관계 endpoint는 해당 snapshot 안에서 검사한다. 삭제는 현재 snapshot에서의 제거이며
역사적 객체의 물리 GC가 아니다. 같은 결과 상태에 도달한 다른 요청은 사건을 각각 남긴다.
인덱스 재구축·outbox·권한·네트워크 서비스는 구현하지 않았다.

## 실행 결과

정확한 환경·명령·입력 파일 SHA-256·SQLite source ID·측정 PRAGMA·각 결과는
[results.json](results.json)에 있다. 결과는 커밋 전 작업 트리의 파일 digest에 결박돼 있다.
`git_base`만으로 새 구현 전체를 식별하지 않는다.

| 시험 | 횟수 | 관측 |
|---|---:|---|
| 객체/상태/사건/head 저장 뒤, COMMIT 직전, COMMIT 후 응답 전 `SIGKILL` | 6개 지점 × 3 = 18 | 커밋 전에는 기존 상태만 보였고, 커밋 후에는 전체 사건과 head가 복구됨. 재시도 뒤 사건 1개 |
| 서로 다른 요청의 동시 writer 2개 | 3 | 하나만 commit, 다른 하나는 stale; head revision 1 |
| 같은 요청의 동시 writer 2개 | 3 | 양쪽에 같은 결과, 사건은 1개 |
| 모델 CID 대조·두 그룹 소속·명시적 분기·정규화된 재시도·잘못된 delta | 1 | 모델과 동일 결과, 과거 소속 보존, 실패 무변경 |
| 같은 상태에 이르는 서로 다른 요청 | 1 | 상태 dedup, 사건은 추가 |
| 연결 종료 후 과거 snapshot 재조회 | 1 | 기존 상태/관계 복원 |
| ABA 음성 대조군 | 1 | CID-only 조건은 일치, state+revision은 오래된 쓰기를 거부 |
| reader snapshot과 writer 잠금 경쟁 | 1 | reader는 transaction 종료까지 이전 상태 유지, 경쟁 writer는 `SQLITE_BUSY` |
| 콘텐츠 bytes 변조 | 1 | CID 대조에서 손상 거부 |
| **합계** | **30** | **PASS** |

강제 종료는 임의 sleep 타이밍에 기대지 않았다. 자식이 지정된 지점에 도달했다고 pipe로
알린 뒤 부모가 그 자식만 `SIGKILL`했다. 각 시점에서 별도 reader로 보이는 상태를 확인하고,
새 연결에서 SQLite integrity/FK, 콘텐츠 CID, snapshot endpoint, 사건/branch 일관성을
검사했다. DB는 모두 synthetic disposable 데이터이며 종료 후 제거했다.

[회귀 테스트](../../tests/test_storage_probe.py)는 추가로 binary bytes, Unicode의 서로 다른
인코딩, 순서가 다른 n항 관계, actor/branch/revision/base가 다른 request ID 재사용,
예외 rollback, 역사적 객체 보존, NFS 거부를 검사한다.

## 환경에서 발견한 제약

Python 3.13.5에 연결된 SQLite는 **3.46.1**이다. 로컬 배포 패키지 관측은
`libsqlite3-0 3.46.1-7+deb13u1`이며 [관측 기록](vendor-observation.json)에 보존했다.
공식 WAL 문서 §11은 WAL-reset race의 영향 범위와 3.51.3 이후 및 일부 backport의 수정을
설명한다. 이 호스트 바이너리의 수정 반영은 **NOT_VERIFIED**다. 이번 30건 통과는 그
드문 write/checkpoint race를 배제하지 않는다. 제품 후보 판정 전에 수정된 정확한 빌드와
라이브러리 provenance를 고정해 다시 시험해야 한다.

이번 DB는 local ext4에서 `WAL`, `synchronous=FULL`, foreign keys ON,
read_uncommitted OFF로 실행했다. 실제 PRAGMA readback도 기록했다.
공유 `/mnt/development`는 NFS이므로 WAL DB를 두지 않았다. adapter는 실험 전에
파일시스템 종류를 확인해 NFS를 거부한다. 공유 볼륨에는 조회용 원문 자료만 보존한다.

DB+WAL+SHM을 포함한 실험 파일의 관측 크기는 32 MiB 미만이었다. 동시에 자식 2개 이하,
등록된 실행 제한은 120초다. 전체 실행 시간은 결과 JSON에 있으며 성능 benchmark로
해석하지 않는다. 파이프 장애 시 부모는 자신이 만든 자식만 정리한다.

## 무엇을 아직 증명하지 않았나

프로세스를 죽여도 OS page cache와 저장 장치는 살아 있다. 따라서 이번 결과는 전원 장애,
VM hard reset, torn write, fsync 실패, ENOSPC의 증거가 아니다. 이 연구 adapter는 입력 크기,
악의적 DB 수정, schema migration, GC, backup/restore, capability, 작업 실행, HSWM을
제품 수준으로 다루지 않는다. 저장소 읽기가 해시와 일치하는 것은 권한 검증이나 서명이 아니다.

SQLite는 후보로 남는다. 단일 writer의 직렬화 비용과 전체 상태 복사/인코딩 비용을
측정하지 않았으므로 RocksDB 등과의 성능 우열도 판단하지 않았다. Rust T10–T14,
서비스 T63, 권한 T15, HOH adapter와 VM/HSWM 수용 상태는 그대로 미완료다.

## 다음에 구현할 계약

- T12/T13: 동일한 transaction 경계와 typed stale/retry 오류를 Rust 후보에서도 재현한다.
- T13/T14: branch CAS에 generation/revision 또는 사건 tip을 넣고, 복원·재생성 후 토큰 재사용을 시험한다.
- T12/T67: 수정된 SQLite 빌드를 고정하고 VFS 오류·disk-full·checkpoint 경쟁·backup 복원을 시험한다.
- T15/T40: authenticated principal, 권한 범위와 idempotency key의 namespace를 함께 정한다.
- T42/T63: 외부 부작용은 별도 작업 상태·재시도·결과 확인 계약으로 다룬다.

## 재현과 그래프 연결

```bash
./chu check --only storage-probe --json
# 또는, local filesystem의 별도 출력 폴더에서
.venv/bin/python scripts/check_storage_probe.py --out .chu/storage-research-new
.venv/bin/pytest -q tests/test_storage_probe.py tests/test_model.py
./chu check --only repo-graph --only graph-catalog --json
```

등록된 check는 `.chu/runs/<id>/`에 이번 실행의 report와 PROV-O 증거를 남긴다.
통합 검증에서는 Python 회귀 테스트 150개, Python lint, graph-catalog,
kernel-contract, os-design, repo-graph가 통과했다. 기존 라이선스 변경으로 추가된
고지·보존 파일 6개는 legal collection의 누락을 보완했으며 내용은 수정하지 않았다.
검증 프로세스에 1.5 GiB 가상 주소 공간 상한을 걸었을 때 Oxigraph가 thread 생성에
실패했다. 같은 상한에서 `MALLOC_ARENA_MAX=2`, `RAYON_NUM_THREADS=2`를 설정해
검사를 통과했으며, 검증 로직이나 실제 저장 실험의 조건을 완화하지 않았다.

저장소 [engineering catalog](../../engineering/catalog.json)의 별도 `storage-research`
프로필이 원문·실험·코드·검사·파일 CID를 연결한다. 메모리 모델 프로필과 섞거나
과거 관측을 현재 PASS로 승격하지 않는다. 공유 KG에는 쓰지 않는다.

공식 근거: [WAL](https://www.sqlite.org/wal.html) §2.2/2.3/7/11,
[Transaction](https://www.sqlite.org/lang_transaction.html) §2.1/2.2,
[Isolation](https://www.sqlite.org/isolation.html),
[PRAGMA](https://www.sqlite.org/pragma.html#pragma_synchronous).
조회일·절·원문 byte hash는 [sources.json](sources.json)에 기록했다.
branch revision, request fingerprint, schema와 위 수용 시나리오는 CHU의 AI 설계 제안이다.

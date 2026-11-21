# CHU / CHU_OS 저장소 분리 기록

2026-10-12 · SECONDARY_AI · 상태(2026-11-21): **초기 이관 완료; CHU_OS pin 갱신과 USL 소비자 전환 완료, CHU의 기존 OS 경로 정리는 미수행**. 최신 내용은 [맨 아래 후속 기록](#2026-11-21-후속-기록)에 있다.
[현재 용어](../canon/CHU_AND_CHU_OS.md)와 [사용자 원문](../canon/sources/USER_PRIMARY_CHU_CHU_OS_2026-10-12.txt)이 근거다.
후속 [사용자 지시](../canon/sources/USER_PRIMARY_CHU_PHILOSOPHY_FIRST_2026-10-12.txt)에 따라
철학을 먼저 정리하고 별도 CHU_OS 저장소를 만든다. [철학 v1](../philosophy/README.md)과
[구현 계약](../philosophy/IMPLEMENTATION_CONTRACT.md)이 이번 작업의 경계다.

기준 관측은 현재 `gj3447/CHU`의 `236d5395600f4d2e8dc2509d71e276940b31973f`다.
개념·Lean·OS 명세·Python 모델·Rust 프로토타입·VM 도구가 한 저장소에 있다.
이 기준 관측 이후 상태는 이 문서의 후속 이관 기록으로 구분한다.
아래 표의 CHU 범위는 2026-10-12 후속 [계산가능성 범위 원문](../canon/sources/USER_PRIMARY_CHU_COMPUTABLE_SCOPE_2026-10-12.txt)에 맞춰
2026-11-21에 정정했다. 이전 문구는 CHU를 “인지능력체·월드모델의 개념”으로 좁혀 적었다.

| 목표 저장소 | 주된 소유 범위 | 현재 경로와 분리 방식 |
|---|---|---|
| CHU | 계산가능한 것을 모두 포함하는 Computable Hyper Universe의 철학 개념(컴퓨터·뇌·우주는 그 사례), 사용자 원문, 형식 이론 | `canon/`, `lean/`, `SOURCES.md`와 개별 이론 문서를 검토해 보유 |
| CHU_OS | 컴퓨터 기반 구현, 실행 계약과 검증 | `os/`, `spec/`, `plan/`, `chu_core_prototype/`, `scripts/`, `tests/`, 개발 환경·CI·OS 실험 |
| 원소유자에 남길 자료 | 과거 연구와 실행 관측 | `journal/`, `research/`, `_findings/`, `PROM_*`는 개별 출처·주제에 따라 참조; 일괄 이동 금지 |

`canon/`의 OS 목표 원문은 의미상 CHU_OS의 근거이기도 하다. 원문 정본은 하나로 보존하고
다른 저장소가 판본·경로·바이트 해시로 참조한다. OS가 사용하는 Lean 이론도 두 개의 독립
정본으로 복제하지 않는다. `scripts/`, `tests/` 전체를 무조건 옮기면 Lean 검사·목록 도구가
깨지므로 아래 의존 검사를 거쳐 파일 단위로 나눈다.

이관 순서는 다음과 같다.

1. 이관 시점의 Git 판본과 비커밋 변경, 활성 소비자를 다시 조사한다. 기존 코드의 이력을
   보존해 CHU_OS에 이어가고, CHU의 개념 정본과 OS가 참조할 판본을 확정한다.
2. 기존 [engineering catalog](../engineering/catalog.json)의 collection/profile을 재사용해
   파일별 원소유자·대상·의존·출처·검사 범위를 만든다. API, Python import, Cargo,
   Lean, CLI, CI 경로와 상대 문서 링크를 포함한다.
3. 원문·과거 관측의 바이트를 보존하고, 이동하는 파일은 원소유 저장소·commit·경로·SHA-256을
   유지한다. CID와 기존 RDF IRI·plan task ID는 저장소 이름 변경 때문에 다시 발급하지 않는다.
4. CHU_OS의 독립 checkout에서 모델·저장·OS 검사와 참조 이론 검사를 실행한다.
   CHU에서는 이론 검사·출처 조회를 실행한다. 두 저장소의 그래프 목록·SHACL·SPARQL 결과와
   로컬 링크를 각각 검증한다. 과거 PASS를 이관 후 PASS로 재사용하지 않는다.
5. HOH, OMC, HSWM, USL의 소비자 참조를 실제 새 원격·판본에 맞춰 옮긴다.
   기존 GitHub 주소와 고정 commit 링크의 해석이 유지되는지 확인한 뒤 기본 진입점을 전환한다.
   준비가 완료될 때까지 현재 CHU 코드 경로와 `./chu` 명령은 유지한다.

특히 OMC F1은 `236d5395600f4d2e8dc2509d71e276940b31973f`의
`scripts/chu_model.py`를 검증 근거로 참조한다. 이후 저장소가 분리돼도 이 과거 참조를
새 코드가 검증된 것처럼 바꾸지 않는다. 새 관측이 새 CHU_OS 판본을 참조하도록 한다.

분리 완료는 두 저장소의 생성만으로 판정하지 않는다. 개념과 구현의 정본 소유가 명시되고,
참조 판본이 해석되며, 독립 검사와 실제 소비자 조회가 통과해야 한다. 실패하면 기존
소비자 참조를 유지하거나 되돌리고 후보 저장소를 별도로 남긴다. 원본·이력 삭제나 force
push는 필요하지 않다.

## 2026-10-12 초기 이관 관측

철학 v1을 먼저 CHU의 `371ff7602ae69a74f14facad1e2942b1aefeaa3d`에 기록했다.
이를 기준으로 별도 **[gj3447/CHU_OS](https://github.com/gj3447/CHU_OS)** 저장소를 생성하고,
초기 이관 commit **`dab627045382330f5b1bdd91a6497ea8fea88585`**를 `main`에 push했다.
생성 시점 공개 범위는 **private**다. CHU는 개념·철학·사용자 원문·Lean의 정본이고,
새 OS 구현 개발의 정본은 CHU_OS다.

초기 이관은 Git 이력을 필터링하지 않고 그대로 이어받았다. 상대 경로와 기존 검사 의존성을
유지하기 위해 기준 판본의 tracked 파일 283개를 출발점으로 삼았다. CHU의 기존 구현 파일은
소비자 호환용으로 남아 있으며, 두 저장소의 파일을 모두 물리적으로 분할한 상태는 아니다.
CHU_OS의 [출처 목록](https://github.com/gj3447/CHU_OS/blob/dab627045382330f5b1bdd91a6497ea8fea88585/engineering/upstream-chu.json)은
기존 collection을 이용해 각 파일의 원소유자·commit·경로·SHA-256과 다음 역할을 구분한다.

- `PINNED_REFERENCE`: 사용자 원문, 개념·철학, 이론·증명, 과거 연구·관측의 고정 참조.
  CHU_OS가 독립 정본으로 수정하지 않으며, 변경은 CHU의 새 판본을 검토해 가져온다.
- `IMPLEMENTATION_BASELINE`: OS 명세·모델·코드·개발 도구 등의 구현 출발점.
  CHU_OS에서 이후 구현을 발전시킬 수 있다.

CHU_OS의 출처 검사는 Git 선조 관계와 기준 파일 목록의 완전성, 원본 Git blob 해시,
collection별 역할, 고정 참조의 현재 바이트를 검사한다. 인접 CHU checkout이나 네트워크가
없어도 검사할 수 있다. 이름 변경 때문에 기존 CID, RDF IRI, task ID를 재발급하지 않았다.
독립 Python 환경과 자체 도구 경로로 실행했으며 CHU의 실행 환경을 심볼릭 링크하지 않았다.

| 단계 | 이번 관측 |
|---|---|
| 철학 v1 · 주장 분류 · 구현 계약 | 완료. 철학적 최종 증명이라는 뜻은 아님 |
| 별도 CHU_OS 생성 · 이력 보존 · push | 완료 |
| 파일별 출처 고정 · 독립 실행 검사 | 아래 범위에서 PASS |
| HOH · OMC · HSWM · USL 소비자 참조 전환 | 아직 수행하지 않음 |
| CHU의 기존 OS 경로 정리 | 소비자 전환 확인 이후 수행 |

로컬 검증 결과는 다음과 같다. 서로 다른 검사 묶음의 결과를 합쳐 적었으며 전체 OS 인수
검사가 완료됐다는 뜻은 아니다.

- CHU: Python 테스트 **150개 PASS**, lint·그래프 목록·저장소 그래프 PASS.
  [보존된 철학 검사](../philosophy/verification-20261012.json)는 기존 Lean에 연결한
  **네 예제**와 **원문/근거 9개 해시**의 PASS 및 실제 입력과 도구 버전을 기록한다.
- CHU_OS: Python 테스트 **155개 PASS**. 그래프 목록·저장소 그래프·커널 계약·OS 설계·
  철학 경계·lint·출처 검사·저장 실험 PASS. 저장 실험은 로컬 ext4의 프로세스 중단,
  동시성, ABA를 포함한 **30개 사례**이며 전원 장애 복구 검증으로 확대하지 않는다.
  [독립 실행 기록](https://github.com/gj3447/CHU_OS/blob/dab627045382330f5b1bdd91a6497ea8fea88585/engineering/initial-verification.json)에
  실행 식별자·시각·입력 해시·관측 범위가 있다.

이번 이관에서 새 VM 부팅, HSWM 실행, 전원 장애 복구, 전체 Rust/WASM 도구체인 검사를
수행하지 않았다. 저장소 독립 실행과 선택한 계약 검증까지를 완료 범위로 삼는다.
다음 전환은 소비자별 새 CHU_OS 판본의 검증 근거를 만들고 참조를 바꾸는 순서다.

## 2026-11-21 후속 기록

SECONDARY_AI. 위 2026-10-12 표의 “아직 수행하지 않음” 항목 이후의 변화만 적는다.

| 항목 | 상태 | 근거 |
|---|---|---|
| CHU_OS의 공용 라우터 등록 | 완료(로컬 커밋, 미push) | ORCA_SETTING `859ff4d`. CHU_OS에서 라우팅하면 `owner-graph`로 OWNER 규칙이 선택된다 |
| CHU_OS의 CHU reference pin 갱신 | 완료 | [CHU_OS PR #1](https://github.com/gj3447/CHU_OS/pull/1), CHU `847525c` 병합. 격리 worktree에서 관련 검사 8개와 Python 테스트 1696개 통과. `feat/systemd-job-executor`에 fast-forward로 병합·push했고(`1bf1388`) 병합 뒤 `upstream-chu`·`concept-claims`·`philosophy-boundaries`·`repo-graph`가 통과했다. GitHub Actions는 계정 결제 문제로 시작되지 않아 원격 CI 결과는 없다 |
| USL 소비자 전환 | 완료(로컬 커밋, 미push) | USL `40ab9c2`. `chu:os-plan`·`chu:kernel-prototype`가 CHU_OS로 결속되고 `example:chu`가 11/11 일치 |
| HOH·OMC 소비자 참조 | 변경하지 않음 | 아래 설명 |
| HSWM 소비자 참조 | 변경 불필요 | README가 가리키는 `ECOSYSTEM.md`·3대원칙은 CHU 소유 문서다 |
| CHU의 기존 OS 경로 정리 | 미수행 | 사용자 결정이 필요하다. Rust 프로토타입은 이론 검사(`truncation`·`witness`·`finite-panel`)의 입력이고, `philosophy/sources.json`과 이론 문서가 `spec/`·`plan/` 경로를 참조해 어디까지 남길지가 소유 범위 결정이다 |

HOH와 OMC의 CHU 구현 참조는 모두 과거 commit(`e53500c`, `236d539`)에 고정돼 있고 CHU `HEAD`의 경로를
읽지 않는다. 두 commit은 CHU_OS 이력의 선조이므로 CHU_OS 원격에서도 해석된다. HOH 검사가 고정한
`scripts/chu_model.py`, `spec/ontology.ttl`, `spec/shapes.ttl`, `spec/IDENTITY.md`의 SHA-256은 CHU_OS `180293e`에서도
같다(이번에 `git show`로 대조). 따라서 CHU의 OS 경로를 정리해도 이 고정 참조는 깨지지 않는다.
두 저장소는 HOH–OMC 세션 경계 규칙과 진행 중인 미커밋 변경이 있어 CHU 세션에서 수정하지 않았다.
새 관측을 CHU_OS 판본으로 남길지는 각 소유자의 후속 작업이다. HOH의 실제 검증 실행은 이번에 하지 않았다.

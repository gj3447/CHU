# CHU — Computable Hyper Universe

**CHU는 컴퓨터·인간의 뇌·우주까지 포괄하는 철학적 개념, Computable Hyper Universe다.**
사용자의 [계산가능성 기준](canon/sources/USER_PRIMARY_CHU_COMPUTABLE_SCOPE_2026-10-12.txt)에 따라,
모든 것을 하이퍼그래프로 보는 관점에서 **계산가능한 것은 모두 CHU**이며 인지는 필수조건이 아니다.
[사용자의 범위 명확화](canon/sources/USER_PRIMARY_CHU_UNIVERSAL_SCOPE_2026-10-12.txt)에 따라
인지능력체라는 한 범주로 한정하지 않는다. 관계·구조·변화·계산의 관점에서 서로 다른
세계를 이해하는 틀을 연구한다. 컴퓨터 기반 운영체제 구현 프로젝트는 별도
**[CHU_OS](https://github.com/gj3447/CHU_OS)**가 맡는다.
사용자 명명과 AI 해석은 [현재 구분](canon/CHU_AND_CHU_OS.md)에 따로 기록한다.

## 현재 읽는 순서

- [CHU 철학 v1.1](philosophy/README.md): 포괄 개념·사례·관계·동일성·사건·관찰·인지·계산가능성.
- [주장과 열린 질문](philosophy/CLAIMS.md): 사용자 관점, 정의 제안, 증명/관측, 미해결 문제.
- [형식화 경계 점검](philosophy/FORMAL_BOUNDARY.md): 기존 Lean 코드의 실제 의미와 네 가지 반례/구분.
- [CHU_OS 구현 계약](philosophy/IMPLEMENTATION_CONTRACT.md): 공통 개념이 구현에 요구하는 검증.
- [저장소 분리 상태](docs/CHU_CHU_OS_REPOSITORY_SPLIT.md): 정본 소유·초기 이관·호환 경로·남은 전환.

철학 v1.1은 검토 가능한 정리본이며, 의식·인지의 충분조건이나 물리 우주에 대한 최종 증명이 아니다.
“우주 자체도 월드모델 CHU”는 사용자에게 귀속된 철학적 관점으로 보존한다.

## 정본과 기존 자산

[사용자 원문](canon/sources/)은 보존하고 [3대원칙](canon/AI_NATIVE_THREE_PRINCIPLES.md)의
원칙·조건부 형식 결과·열린 가설을 구분한다. [lean/](lean/)는 CHU가 소유하는 기존 형식화다.
`axiom CHU : Type`은 형식 체계의 기호이며 인지능력체의 존재나 OS 동작을 자동 증명하지 않는다.

[WHY_HYPERGRAPH](WHY_HYPERGRAPH.md), [SOURCES](SOURCES.md), [INDEX](INDEX.md),
PROM 보고서와 [역사적 상태](docs/STATUS.md)는 기존 연구를 보존한다. 과거의 강한 설명과
현재 판정이 다르면 [형식화 점검](philosophy/FORMAL_BOUNDARY.md)의 한계를 함께 읽는다.
형식 이론의 source owner를 OS 저장소로 넘기지 않는다.

[HSWM·USL 생태계](ECOSYSTEM.md)는 개념적 관계와 구현 연결을 구분한다.
HOH Interface는 CHU_OS의 사람 인터페이스라는 기존 결정을 유지한다.

## 확인과 재현

```bash
./chu concept query scope
./chu check --only philosophy-boundaries --json
./chu check --only repo-graph --only graph-catalog --json
./chu repo query profiles --json
```

개발 환경과 전체 검사는 [DEVELOPMENT](docs/DEVELOPMENT.md), 파일·프로필·증거의 범위는
[engineering](engineering/README.md)을 따른다. 철학 검사 PASS는 원문 hash와 네 Lean 예제의
검사 결과이며 철학적 주장의 보편적 참 판정이 아니다.

CHU_OS 초기 이관 후에도 기존 `spec/`, `os/`, `plan/`, 프로토타입과 `./chu`는 소비자 호환과
과거 관측 재현을 위해 당분간 남긴다. 새 OS 개발의 정본 위치와 상세 전환 상태는
[분리 기록](docs/CHU_CHU_OS_REPOSITORY_SPLIT.md)에 명시한다. 부팅·HSWM 실행·전원 장애 복구의
미완료 상태를 저장소 생성만으로 완료 처리하지 않는다.

## License

Copyright © 2026 Ra Gyeongjun (라경준).

[MetaHumotonic License 1.2](LICENSE)와 [적용 범위·기존 허락·제3자 고지](LICENSE-NOTICE.md)를 따른다.
기존 허락과 별도 라이선스 자료의 조건은 유지된다. 실제 장치 접근에는 별도 승인이 필요하다.

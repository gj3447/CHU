# CHU / CHU_OS 개념·주장 그래프

2026-10-12 · SECONDARY_AI · CHU 소유 범위의 실제 RDF 그래프.
[기존 C01–C03](../CLAIMS.md)의 명명·작업 결정·관점을 재사용한다.
개념 CHU와 컴퓨터 구현 CHU_OS, 두 소유 저장소, 사용자 원문, 소유자의 이관 관측을
서로 다른 대상으로 조회한다. HSWM의 실행 상태 그래프나 공유 KG 발행은 이번 범위가 아니다.

## 조회와 검사

저장소 루트에서 기존 환경과 `./chu`를 사용한다. 새 DB나 패키지는 설치하지 않는다.

```bash
./chu concept query distinction
./chu concept query viewpoint
./chu concept query separation
./chu concept query sources
./chu concept export --format json-ld
./chu check --only concept-claims --only repo-graph --json
```

질의 결과는 SPARQL JSON이며 IRI·literal datatype과 출처를 유지한다. 조회·내보내기도
먼저 SHACL·원문 검사를 거친다. 검사 명령은 `.chu/runs/`에 출처 해시와 답을 보존하며
RDFLib/Oxigraph가 같은 답을 내는지, JSON-LD 왕복에서 그래프가 같은지 비교한다.
Git의 고정 원문 판본을 읽으므로 해당 이력이 필요하다. CI checkout은 전체 이력을 가져온다.

| 질문 | 질의와 기대 답 |
|---|---|
| 무엇이 개념이고 무엇이 컴퓨터 구현인가? | `distinction`: C01의 CHU_OS → CHU, 명명 원문·CID |
| 우주에 관한 문장은 누구의 어떤 주장인가? | `viewpoint`: C03, 사용자 원문, WorldModel 문맥, USER_VIEWPOINT / NOT_EMPIRICALLY_VALIDATED |
| 저장소 소유와 분리 진행 상태는 무엇인가? | `separation`: C02의 지시, 개념·구현 소유, 초기 이관 기록, 소비자 전환 미수행 관측 |
| 어떤 원문·판본·바이트가 각각을 뒷받침하는가? | `sources`: 각 claim의 source record, 경로·commit·CID·원문 발췌 |

## 정체성·권위·시간의 경계

`claims.ttl`이 데이터이고 `ontology.ttl`이 로컬 어휘의 방향·domain/range·의미를,
`shapes.ttl`이 기수·타입·명명과 관점의 제약을 정의한다. CHU와 CHU_OS는 별도 concept IRI다.
GitHub 저장소 주소는 이 개념을 소유·구현하는 저장소 식별자이며 개념과 동일시하지 않는다.
`pc:C01`, `pc:C02`, `pc:C03`는 기존 문서 ID의 RDF 표현이다.

주장은 `rdf:Statement`로 주어·술어·목적어를 명시하고, C03에는 `pc:context WorldModel`을
붙인다. 원문에 대한 AI의 정규화는 SECONDARY_AI, 인용된 원문만 USER_PRIMARY다.
원문 기록에는 작성 주체와 정확한 Git 판본, 경로, 실제 바이트 CID를 결속한다.
`pc:conceptClaims`의 날짜는 그래프 작성 날짜이고 원래 발화·이관의 정확한 발생 시각을
추정하지 않는다. 이관 상태는 `806258fe9a7974cf9bb237d6578d2c61094eabe0`의
소유 기록을 읽은 SOURCE_REPORTED 관측으로 남긴다. 매 조회마다 원격을 점검하는 기능은 아니다.

CHU_OS의 초기 이관은 기록돼 있지만 소비자 전환은 남아 있다. 초기 이관 상태를 전체
이관 완료로 바꾸거나, “우주도 CHU”를 검증된 물리적 동일성으로 승격하면 실패한다.
RDF의 재진술은 원래 문장 자체를 참으로 단언하지 않는다.
([RDF 1.1 reification](https://www.w3.org/TR/rdf11-mt/#reification))
검사기는 이 경계를 위해 귀속을 버린 직접 주장과 `owl:sameAs`를 허용하지 않는다.

실제 사용하는 표준은 [RDF 1.1](https://www.w3.org/TR/rdf11-concepts/),
[SHACL](https://www.w3.org/TR/shacl/), [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/),
[PROV-O](https://www.w3.org/TR/prov-o/)다. 이 표준들의 전체 적합성 인증이나 철학적 참의
증명이라는 뜻은 아니다. 검사 범위는 이 문서의 네 질의와 로컬 계약이다.

공유 KG의 옛 `sym:Concept:computable_hyper_universe_(chu)`는 현재도 출처 없는 database
설명을 반환했다. 기존 관례의 `urn:symposium-kg:…` 참조를 `rdfs:seeAlso`로 보존한다.
그 UID와 새 로컬 concept의 동일성을 선언하거나 글로벌 스키마를 변경하지 않는다.

## 갱신 방법

소유 저장소가 새 명명·관점·이관 관측을 기록하면 그 판본과 원문을 검토한다. 이 그래프의
source pin, 주장 상태와 검증기의 기대 답을 함께 갱신하고 음성 대조군을 실행한다.
과거 source·관측은 Git 이력에 남는다. 출력 개수만 맞추거나 근거 없이 완료 상태를 올리지 않는다.
소비자 프로젝트는 이 그래프의 판본·해시를 참조하며 독립 정본을 복제하지 않는다.

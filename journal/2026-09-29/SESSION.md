# 2026-09-29 작업 정리

정본은 [`session.ttl`](session.ttl) / [`session.jsonld`](session.jsonld)이다. 이 문서는 사람이 읽기 위한 뷰다.
그래프는 PROV-O로 작성했다. 사용자 발화 10개가 작업 7개를 촉발했고, 작업들은 커밋 15개와 검증 기록을 남겼다.
AI 해석 5개는 사용자 원문과 분리해 기록했고, 열린 항목은 7개다.
재현: `uv run --with rdflib --with pyshacl python journal/2026-09-29/session_graph.py`

| 검사 | 결과 |
|---|---|
| SHACL 1.0 ([shapes](session_graph.py)) | 적합, 354 트리플 |
| 음성 대조군 (AI 주장을 사용자 발화로 위장) | 거부됨 |
| 커밋 15개 live 확인 (로컬 객체 + 원격 추적 브랜치) | 전부 존재 |
| 질문 5개 ([queries/](queries/) → [답](competency_answers.json)) | 기대 답과 일치 |

## 질문별 답

**CQ1. 어떤 발화가 어떤 작업과 커밋을 낳았나**

| 작업 | 발화 | 저장소 · 커밋 |
|---|---|---|
| A1 CHU = 하이퍼그래프 OS, 작업계획 | U1 | CHU `26316bd` |
| A2 3대원칙·왜 하이퍼그래프, Lean 11개 수입 | U2, U3 | CHU `718edbc` |
| A3 독립 저장소 생성·push | U4 | CHU `b304281` |
| A4 이중 라이선스 + public | U5 | CHU `c415e2a` |
| A5 CHU·HSWM·USL 연결 | U6 | CHU `5ae3afd` · USL `44a0403` `924cebd` · HSWM `f5f252b` · SYMPOSIUM `0b5e00a` |
| A6 Covenant MHP-0001 초안 | U7, U8 | foundation `738dd7a` (PR #1) · CHU `e5e5975` |
| A7 Linux OS 연구 | U9 | CHU `752d127` · USL `f752860` |

**CQ2. 검증:** 기록된 검증은 모두 PASS다. 단 하나 PENDING이 있다. A6의 "재단 절차상 결정"으로,
공개 논의와 사람 리뷰를 기다리는 중이다.

**CQ3. 열린 항목**

| # | 항목 | 막는 것 | 다음 |
|---|---|---|---|
| O1 | MHP-0001 Covenant 결정 | 재단 절차: 최소 7일(권고 30일), 사람 공개 리뷰. Steward 2인 미만이라 결정돼도 PROVISIONAL | PR #1 리뷰 |
| O2 | 재단 PROJECTS.md에 CHU·USL 추가, HSWM 라이선스 갱신 | PROJECT 제안 필요 | 사용자 확인 |
| O3 | 첫 커밋 `798f9f9` 이력에 남은 이전 작성자 이메일 | 이력 재작성은 사용자 결정 사항 | 사용자 결정 |
| O4 | SYMPOSIUM 사본과 gj3447/CHU 중 어느 쪽이 정본인지 확정 | 사용자 결정 사항 | 사용자 결정 |
| O5 | 명세 착수: T01 데이터 모델, T02 정체성 | 없음 | **다음 작업** |
| O6 | 공유 KG 반영 | 공유 KG에 authorized writer가 없음 | [변경안](kg_changeset.proposed.json)을 KG owner publisher로 반영 |
| O7 | FUSE 뷰 (T33) | LXC라 `/dev/fuse` 없음 | 호스트/VM에서 제공, 또는 선택 기능으로 유지 |

**CQ4. 원문과 해석의 분리:** 위반은 0건이다. 사용자 발화는 사용자에게만, AI 주장 C1–C5(`SECONDARY_AI`)는
agent에게만 귀속된다. AI 주장은 다음과 같다.
- ZFC 해석
- USL = CHU 연결 문법
- sudo 전권 라이선스 대신 opt-in 약정
- Linux 위 사용자 공간 오버레이
- grant 하이퍼엣지

**CQ5. 공유 KG 연결:** 오늘 작업이 이어지는 기존 KG 레코드는 다음과 같다.
- `sym:Concept:hswm`, `sym:Repository:hswm`, `sym:Concept:usl`: 비준된 레코드다.
- `sym:Concept:computable_hyper_universe_(chu)`, `sym:AbstractNode:metahumotonic`: 권위가 `UNSPECIFIED`라 owner 검토가 필요하다.
- 없어서 새로 제안한 것: CHU·USL·재단의 Repository 노드, 오늘의 CHU 정체성 발화 노드, MHP-0001 노드.
  [변경안](kg_changeset.proposed.json)은 `PROPOSED_NOT_APPLIED` 상태다.

## 오늘 확정된 것 (사용자 원문)

- CHU = **하이퍼그래프 기반 OS**. 폴더 트리 없이 모든 것이 하이퍼그래프 노드다 (U1, [원문](../../canon/sources/USER_PRIMARY_CHU_HYPERGRAPH_OS_2026-09-29.txt)).
- **AI native 3대원칙**: 양파껍질 최외각 시뮬레이터, 하이퍼그래프 = 최소 비용 체계, AI = 소프트웨어
  ([정본](../../canon/AI_NATIVE_THREE_PRINCIPLES.md)).
- **CHU · HSWM · USL은 긴밀히 연결된 한 체계다** (U6, [ECOSYSTEM](../../ECOSYSTEM.md)).
- 세 저장소 모두 public이며 같은 라이선스(AGPL-3.0-or-later 또는 상용)를 쓴다.

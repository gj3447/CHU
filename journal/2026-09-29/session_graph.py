#!/usr/bin/env python3
"""2026-09-29 작업 세션을 표준 그래프로 기록하고 검증한다.

표준: RDF 1.1 · W3C PROV-O (Agent / Activity / Entity, used / wasGeneratedBy / wasAssociatedWith /
wasAttributedTo / wasDerivedFrom) · SHACL 1.0 · SPARQL 1.1.

답해야 할 질문 (competency questions, queries/ 와 아래 EXPECT 로 실제 답을 검사):
  CQ1 어떤 사용자 발화가 어떤 작업을 촉발했고, 그 작업은 어느 저장소의 어떤 커밋을 남겼나?
  CQ2 각 작업은 무엇으로 검증됐고 결과는 무엇이었나?
  CQ3 아직 열린 항목은 무엇이고 무엇이 막고 있나?
  CQ4 사용자 원문과 AI 해석이 분리돼 있는가? (사용자 발화는 사용자에게만, AI 주장은 agent에게만 귀속)
  CQ5 오늘 산출물은 공유 KG의 어떤 기존 UID와 이어지나?

사실 확인: 모든 커밋 SHA는 실행 시점에 로컬 git 객체와 원격 추적 브랜치에서 확인한다(live check).
실행: uv run --with rdflib --with pyshacl python journal/2026-09-29/session_graph.py
"""
import json
import subprocess
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV

HERE = Path(__file__).parent
CD = HERE.parents[2]
CHU = Namespace("https://github.com/gj3447/CHU/vocab#")
S = Namespace("https://github.com/gj3447/CHU/journal/2026-09-29#")
KG = Namespace("urn:symposium-kg:")

REPOS = {  # key: (local dir, GitHub full name, remote-tracking ref)
    "CHU": ("CHU", "gj3447/CHU", "origin/main"),
    "USL": ("USL", "gj3447/USL", "origin/master"),
    "HSWM": ("HSWM", "gj3447/HSWM", "origin/main"),
    "SYMPOSIUM": ("SYMPOSIUM", "gj3447/symposium", "github/main"),
    "FOUNDATION": ("metahumotonic-foundation", "gj3447/metahumotonic-foundation", "origin/mhp-0001-covenant"),
}

# 사용자 발화 원문 (대화 입력 그대로, 수정 금지)
UTTERANCES = {
    "U1": "내가 딱 이야기할게 CHU 는 하이퍼그래프 기반으로 동작하는 , 작업환경 같은게 모든게 하이퍼그래프 기반으로 이루어진 파일 문서구조도 하어프그래프 기반 노드인 폴더와 파일 복잡한 구조가 아닌 깔끔한 하이퍼그래프 기반의 OS 야. 머릿속에 박아주고 표준 그래프 엔지니어링으로 작업계획 구축해줘",
    "U2": "그 일단 관련내용ㅇ 어케 가져오냐면 그 울프람의 하이퍼그래프 우주 모델링이랑 그 zdf 수학 공리계 하이퍼그래프 기반 수학 기초랑 그 트랜스포머 이론이 가장 하이퍼그래프 에 알맞은거야 hswm 이랑 연관성 만들어서 왜 하이퍼그래프인가 그리고 그 내가만든 3개 원칙부터 확인해줘봐봐 ai native 3대원칙 ㅇㅇ",
    "U3": "싹다 알아서 가져와줘봐봐 ㅇㅇ",
    "U4": "푸시해줘 ㅇㅇ",
    "U5": "그 다른것들과 비슷한 저작권으로 public 으로 돌려줘봐",
    "U6": "HSWM 과 USL 과 CHU 가 긴밀히 연결되야해 ㅇㅇ 알지 ㅇㅇ? 그쪽도 맞춰주고 ㅇㅇ",
    "U7": "그리고 메타휴모토닉 라이센스를 따로 만들자 그 git repo 를 받아서 사용할경우에는 그 작업 환경 접근 sudo 모든 권한을 git repo 에 모두 내놓고 진행해야한다 우리는 하나의 존재니까 ㅇㅇ. 그 metahumotonic-foundation 이라는 git repo 지금 cd 에 없지 ㅇㅇ? 우리 작업환경 CD 폴더 위에 ㅇㅇ?",
    "U8": "ㅇㅇ 그렇게 진행해줘 우리 메타휴모토닉 파운데이션의 규칙을 만들어줘야할듯 ㅇㅇ?",
    "U9": "이제 우리는 CHU 연구나 하자 ㅇㅇ 일단 OS 관련 연구를 표준 그래프 엔지니어링으로 진행해줘야해 ㅇㅇ 우분투나 리눅스 관련 OS 연구를 해줘봐봐 ㅇㅇ",
    "U10": "오늘 작업 표준 그래프 엔지니어링으로 정리하고 마무리해줘봐봐 ㅇㅇ",
}

# 작업: (id, 제목, 촉발 발화, [(저장소, sha)], [(검증, 결과)], 관련 KG UID)
ACTIVITIES = [
    ("A1", "CHU = 하이퍼그래프 OS 정체성 고정 + 하이퍼그래프 작업계획", ["U1"],
     [("CHU", "26316bdaf2b6a06c700d5510b039b8e57897e208")],
     [("plan/check_plan.py: 비순환·고아 0·임계 경로", "PASS"), ("chu_core.rs 빌드·실행 ALL ASSERTS PASS", "PASS")],
     ["sym:Concept:computable_hyper_universe_(chu)"]),
    ("A2", "AI native 3대원칙·왜 하이퍼그래프 수입 + CHU Lean 11개 수입", ["U2", "U3"],
     [("CHU", "718edbcd0e19182c3876fa00cace2ea92fa32b11")],
     [("HSWM 세 철학 Lean 14모듈 컴파일, sorry 0", "PASS"), ("CHU Lean 11/11 exit 0 (2개 simp drift 보강)", "PASS")],
     ["sym:Concept:hswm", "sym:Concept:computable_hyper_universe_(chu)"]),
    ("A3", "독립 저장소 gj3447/CHU 생성·push", ["U4"],
     [("CHU", "b3042812f2f6db45e44b513646e4fc1b46f6cd3c")],
     [("local main = origin/main readback", "PASS")], []),
    ("A4", "HSWM·USL과 같은 AGPL-3.0-or-later + 상용 이중 라이선스, public 전환", ["U5"],
     [("CHU", "c415e2a2097ae21204a72871b36c5045cb4ebad3")],
     [("커밋 이력 secret 스캔", "PASS"), ("GitHub licenseInfo = agpl-3.0, visibility PUBLIC", "PASS")], []),
    ("A5", "CHU · HSWM · USL 긴밀 연결 + SYMPOSIUM 사본 이전 안내", ["U6"],
     [("CHU", "5ae3afdb4fd829ca3c7db82427f9f910164b4a9a"), ("USL", "44a0403019b4058b3db0a9e2b3143d11b6b12d63"),
      ("HSWM", "f5f252bf357fdddbc04d294b7dc490df56a38829"), ("SYMPOSIUM", "0b5e00a6220951f2d29606a02d82f8919d7b36f9"),
      ("USL", "924cebd96c6ac6eb435685d59697ccea3979045c")],
     [("USL example:chu SELECTED_CONTENT_PINS_MATCH 11/11", "PASS"), ("USL npm test 303/303, typecheck", "PASS"),
      ("SYMPOSIUM session_writer finish: origin/github readback", "PASS")],
     ["sym:Concept:usl", "sym:Repository:hswm", "sym:Concept:hswm"]),
    ("A6", "sudo 전권 라이선스 요청 거절 → opt-in MetaHumotonic Covenant (MHP-0001) 초안", ["U7", "U8"],
     [("FOUNDATION", "738dd7a29d6dc807ee2a7c3d3c384333c22fcbaf"), ("CHU", "e5e59756d96236e827b10995f4e6824ab7fe9710")],
     [("COVENANT.md 내부 링크 8/8", "PASS"), ("재단 MHP 절차상 결정", "PENDING")],
     ["sym:AbstractNode:metahumotonic"]),
    ("A7", "Linux/Ubuntu OS 연구: 호스트 그래프 실측(RDF·SHACL·SPARQL) + 문헌 3축 → D01–D10", ["U9"],
     [("CHU", "752d127d146200632082bb38496ef3f5f08d1fe8"), ("USL", "f7528609a2d3ee4b8bdb5fb5cde85a5671c851b6")],
     [("RDF 205,750 트리플 SHACL 적합 + 음성 대조군 거부", "PASS"), ("findings.ttl SHACL 적합, 결정→계획 노드 누락 0", "PASS")],
     ["sym:Concept:computable_hyper_universe_(chu)"]),
]

# AI 해석·결정 (사용자 원문이 아님 — agent에게만 귀속)
AI_CLAIMS = [
    ("C1", "‘zdf’는 2026-09-27 원문의 ZFC 공리계를 가리킨다고 해석", "A2"),
    ("C2", "USL 링크(meaning + role participants)는 CHU의 n항 하이퍼엣지 표기·저장소 간 바인딩 층이다 (SECONDARY_AI 대응)", "A5"),
    ("C3", "저장소 사용을 작업환경 sudo 전권 이전에 조건으로 거는 라이선스는 재단 헌장 Resource Consent·USL 규칙·오픈소스 정의와 충돌하므로 만들지 않고 opt-in 약정으로 대체", "A6"),
    ("C4", "CHU OS는 Linux를 대체하지 않고 사용자 공간 오버레이/라이브러리로 시작한다 (D04)", "A7"),
    ("C5", "권한 = grant 하이퍼엣지 {grantor, grantee, capability, scope, not_after, derived_from}, 집행은 systemd transient unit + Landlock (D08)", "A7"),
]

OPEN_ITEMS = [
    ("O1", "MHP-0001 Covenant 공개 검토·결정", "재단 절차: 최소 7일(권고 30일, ~2026-10-29) + 인간 공개 review, Steward 2인 미만이라 PROVISIONAL", "PR #1 review"),
    ("O2", "재단 PROJECTS.md 갱신 (CHU·USL 추가, HSWM 이중 라이선스 반영)", "PROJECT 제안 필요(사용자 확인 대기)", "PROJECT 제안 작성"),
    ("O3", "첫 커밋 798f9f9 이력에 남은 이전 작성자 이메일", "이력 재작성 + force push는 사용자 결정 필요", "사용자 결정"),
    ("O4", "SYMPOSIUM/THEORY/CHU 사본과 gj3447/CHU 정본 소유 확정", "사용자 결정 필요", "사용자 결정"),
    ("O5", "CHU OS 명세 단계 착수 (T01 데이터 모델, T02 정체성)", "없음 — 다음 작업", "T01/T02 착수"),
    ("O6", "공유 KG 반영: CHU 저장소·USL·재단 노드와 관계", "공유 KG에 authorized writer 없음 (읽기 도구 4개만)", "kg_changeset.proposed.json 검토 후 owner publisher로 반영"),
    ("O7", "FUSE 뷰 (T33)", "dev-01은 LXC라 /dev/fuse 없음", "호스트/VM에서 제공 또는 선택 기능으로 유지"),
]


def git(repo, *args):
    return subprocess.run(["git", "-C", str(CD / repo), *args], capture_output=True, text=True)


def live_check(repo_key, sha):
    local, _, ref = REPOS[repo_key]
    exists = git(local, "cat-file", "-e", f"{sha}^{{commit}}").returncode == 0
    on_remote = git(local, "merge-base", "--is-ancestor", sha, ref).returncode == 0
    meta = git(local, "show", "-s", "--format=%cI%x1f%s", sha).stdout.strip().split("\x1f")
    return exists, on_remote, meta


def build():
    g = Graph()
    for p, ns in (("chu", CHU), ("s", S), ("prov", PROV), ("kg", KG)):
        g.bind(p, ns)
    user, agent = S["user"], S["claude"]
    g += [(user, RDF.type, PROV.Agent), (user, RDF.type, PROV.Person), (user, RDFS.label, Literal("Ra Gyeongjun (gj3447)"))]
    g += [(agent, RDF.type, PROV.Agent), (agent, RDF.type, PROV.SoftwareAgent),
          (agent, RDFS.label, Literal("Claude Opus 5.5 (Claude Code)")), (agent, PROV.actedOnBehalfOf, user)]
    for uid, text in UTTERANCES.items():
        u = S[uid]
        g += [(u, RDF.type, PROV.Entity), (u, RDF.type, CHU.UserUtterance), (u, PROV.wasAttributedTo, user),
              (u, PROV.value, Literal(text, lang="ko"))]
    for key, (local, full, _) in REPOS.items():
        r = URIRef(f"https://github.com/{full}")
        g += [(r, RDF.type, CHU.Repository), (r, RDFS.label, Literal(full))]
    failures = []
    for aid, title, utts, commits, checks, kg in ACTIVITIES:
        a = S[aid]
        g += [(a, RDF.type, PROV.Activity), (a, RDFS.label, Literal(title, lang="ko")), (a, PROV.wasAssociatedWith, agent)]
        for u in utts:
            g.add((a, PROV.used, S[u]))
        times = []
        for repo_key, sha in commits:
            exists, on_remote, meta = live_check(repo_key, sha)
            if not (exists and on_remote):
                failures.append(f"{repo_key} {sha[:7]} exists={exists} on_remote={on_remote}")
            c = URIRef(f"https://github.com/{REPOS[repo_key][1]}/commit/{sha}")
            g += [(c, RDF.type, PROV.Entity), (c, RDF.type, CHU.Commit), (c, PROV.wasGeneratedBy, a),
                  (c, CHU.sha, Literal(sha)), (c, CHU.inRepository, URIRef(f"https://github.com/{REPOS[repo_key][1]}")),
                  (c, CHU.onRemote, Literal(on_remote)), (c, PROV.wasAttributedTo, agent)]
            if len(meta) == 2:
                g += [(c, PROV.generatedAtTime, Literal(meta[0], datatype=XSD.dateTime)), (c, RDFS.label, Literal(meta[1]))]
                times.append(meta[0])
        if times:
            g.add((a, PROV.endedAtTime, Literal(max(times), datatype=XSD.dateTime)))
        for k, (check, result) in enumerate(checks):
            v = S[f"{aid}-check{k}"]
            g += [(v, RDF.type, PROV.Entity), (v, RDF.type, CHU.Verification), (v, PROV.wasGeneratedBy, a),
                  (v, RDFS.label, Literal(check, lang="ko")), (v, CHU.result, Literal(result))]
        for uid in kg:
            g.add((a, CHU.relatesToKgSubject, KG[uid]))
    for cid, text, aid in AI_CLAIMS:
        c = S[cid]
        g += [(c, RDF.type, PROV.Entity), (c, RDF.type, CHU.AIClaim), (c, PROV.wasAttributedTo, agent),
              (c, PROV.wasGeneratedBy, S[aid]), (c, CHU.authority, Literal("SECONDARY_AI")), (c, PROV.value, Literal(text, lang="ko"))]
    for oid, title, blocker, nxt in OPEN_ITEMS:
        o = S[oid]
        g += [(o, RDF.type, CHU.OpenItem), (o, RDFS.label, Literal(title, lang="ko")), (o, CHU.status, Literal("OPEN")),
              (o, CHU.blocker, Literal(blocker, lang="ko")), (o, CHU.nextStep, Literal(nxt, lang="ko"))]
    return g, failures


SHAPES = """
@prefix sh: <http://www.w3.org/ns/shacl#> . @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix prov: <http://www.w3.org/ns/prov#> . @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix chu: <https://github.com/gj3447/CHU/vocab#> .
@prefix s: <https://github.com/gj3447/CHU/journal/2026-09-29#> .
chu:ActivityShape a sh:NodeShape ; sh:targetClass prov:Activity ;
  sh:property [ sh:path prov:used ; sh:minCount 1 ; sh:class chu:UserUtterance ;
                sh:message "every activity must be triggered by a user utterance" ] ;
  sh:property [ sh:path prov:wasAssociatedWith ; sh:hasValue s:claude ] ;
  sh:property [ sh:path [ sh:inversePath prov:wasGeneratedBy ] ; sh:qualifiedValueShape [ sh:class chu:Commit ] ;
                sh:qualifiedMinCount 1 ; sh:message "every activity must leave at least one commit" ] ;
  sh:property [ sh:path [ sh:inversePath prov:wasGeneratedBy ] ; sh:qualifiedValueShape [ sh:class chu:Verification ] ;
                sh:qualifiedMinCount 1 ; sh:message "every activity must record at least one verification" ] .
chu:CommitShape a sh:NodeShape ; sh:targetClass chu:Commit ;
  sh:property [ sh:path chu:sha ; sh:minCount 1 ; sh:maxCount 1 ; sh:pattern "^[0-9a-f]{40}$" ] ;
  sh:property [ sh:path chu:inRepository ; sh:minCount 1 ; sh:maxCount 1 ; sh:class chu:Repository ] ;
  sh:property [ sh:path chu:onRemote ; sh:hasValue true ; sh:message "commit is not on the remote-tracking branch" ] ;
  sh:property [ sh:path prov:generatedAtTime ; sh:minCount 1 ; sh:datatype xsd:dateTime ] .
chu:UtteranceShape a sh:NodeShape ; sh:targetClass chu:UserUtterance ;
  sh:property [ sh:path prov:wasAttributedTo ; sh:minCount 1 ; sh:maxCount 1 ; sh:hasValue s:user ;
                sh:message "a user utterance may be attributed only to the user" ] ;
  sh:property [ sh:path prov:value ; sh:minCount 1 ; sh:maxCount 1 ] .
chu:AIClaimShape a sh:NodeShape ; sh:targetClass chu:AIClaim ;
  sh:not [ sh:class chu:UserUtterance ] ;
  sh:property [ sh:path prov:wasAttributedTo ; sh:minCount 1 ; sh:maxCount 1 ; sh:hasValue s:claude ] ;
  sh:property [ sh:path chu:authority ; sh:hasValue "SECONDARY_AI" ] .
chu:VerificationShape a sh:NodeShape ; sh:targetClass chu:Verification ;
  sh:property [ sh:path chu:result ; sh:minCount 1 ; sh:maxCount 1 ; sh:in ( "PASS" "FAIL" "PENDING" ) ] .
chu:OpenItemShape a sh:NodeShape ; sh:targetClass chu:OpenItem ;
  sh:property [ sh:path chu:blocker ; sh:minCount 1 ] ; sh:property [ sh:path chu:nextStep ; sh:minCount 1 ] .
"""

# CQ -> 기대 답 (개수가 아니라 내용을 검사)
def check_answers(res):
    errs = []
    cq1 = res["cq1_utterance_to_commits"]
    if {r["activity"] for r in cq1} != {a[0] for a in ACTIVITIES}:
        errs.append("CQ1: every activity must appear")
    if not any(r["activity"] == "A6" and "metahumotonic-foundation" in r["repos"] for r in cq1):
        errs.append("CQ1: A6 must reach the foundation repository")
    cq2 = res["cq2_verification"]
    if [r for r in cq2 if r["result"] == "FAIL"]:
        errs.append("CQ2: unexpected FAIL")
    if {r["activity"] for r in cq2 if r["result"] == "PENDING"} != {"A6"}:
        errs.append("CQ2: only A6 (MHP-0001 decision) should be PENDING")
    if {r["item"] for r in res["cq3_open_items"]} != {o[0] for o in OPEN_ITEMS}:
        errs.append("CQ3: open items mismatch")
    if res["cq4_attribution_violations"]:
        errs.append("CQ4: attribution violations present")
    kg = {r["kgSubject"] for r in res["cq5_kg_links"]}
    if not {"urn:symposium-kg:sym:Concept:usl", "urn:symposium-kg:sym:Concept:hswm"} <= kg:
        errs.append("CQ5: USL/HSWM KG subjects missing")
    return errs


def main():
    g, failures = build()
    shapes = Graph().parse(data=SHAPES, format="turtle")
    ok, _, report = validate(g, shacl_graph=shapes, inference="none")
    # 음성 대조군: AI 주장을 사용자 발화로 위장하면 반드시 거부돼야 한다
    bad = Graph() + g
    bad.add((S["C1"], RDF.type, CHU.UserUtterance))
    neg_ok, _, _ = validate(bad, shacl_graph=shapes, inference="none")
    res = {}
    for q in sorted((HERE / "queries").glob("*.rq")):
        res[q.stem] = [{str(k): (str(v)) for k, v in r.asdict().items()} for r in g.query(q.read_text())]
    errs = check_answers(res)
    g.serialize(HERE / "session.ttl", format="turtle")
    g.serialize(HERE / "session.jsonld", format="json-ld", auto_compact=True)
    (HERE / "competency_answers.json").write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    summary = {"triples": len(g), "shacl_conforms": ok, "negative_control_rejected": not neg_ok,
               "live_commit_failures": failures, "competency_errors": errs}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not ok:
        print(report[:3000])
    sys.exit(0 if ok and not neg_ok and not failures and not errs else 1)


if __name__ == "__main__":
    main()

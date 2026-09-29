#!/usr/bin/env python3
"""Linux OS 연구 결과를 지식 그래프로: 교훈(Lesson) -> 근거(source URL·실측) -> 설계 결정(Decision) -> 계획 노드.

표준: RDF 1.1 + PROV-O(prov:wasDerivedFrom) + SHACL 1.0.
실행: uv run --with rdflib --with pyshacl python research/linux_os/findings_graph.py
출력: findings.ttl (공개 커밋), SHACL 적합 여부 출력, 모든 결정이 계획 노드를 가리키는지 확인.
"""
import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, RDFS, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV

HERE = Path(__file__).parent
CHU = Namespace("https://github.com/gj3447/CHU/vocab#")
R = Namespace("https://github.com/gj3447/CHU/research/linux_os#")
PLAN = Namespace("https://github.com/gj3447/CHU/plan#")

MEASURED = "research/linux_os/public_summary.json"

# (id, 교훈, 근거들, 결정 id)
LESSONS = [
    ("L01", "Linux VFS는 이미 정체성(inode)과 이름(dentry/path)을 분리한다. 하드링크 = 한 대상 여러 이름. 단 inode 정체성은 파일시스템 국소이며 복사에서 살아남지 못한다.",
     ["https://docs.kernel.org/filesystems/vfs.html", "https://man7.org/linux/man-pages/man2/link.2.html"], "D01"),
    ("L02", "디렉터리 하드링크 금지(순환·fsck·`..`) — 하이퍼엣지는 파일시스템 링크로 표현하면 안 되고 CHU 자체 층에 있어야 한다.",
     ["https://man7.org/linux/man-pages/man2/link.2.html"], "D02"),
    ("L03", "실측: 여러 dpkg 패키지가 함께 소유한 경로 593개 중 591개가 디렉터리, 최대 1,004개 패키지가 한 경로를 공유 — 폴더는 이미 다중 소속 그룹 하이퍼엣지처럼 쓰인다.",
     [MEASURED], "D02"),
    ("L04", "실측: dpkg 관계 절 4,360개 중 80개(1.8%)가 `a | b` 대안 = 이항 분해 불가능한 n항 하이퍼엣지(최대 대안 8개). systemd 관계는 전부 이항.",
     [MEASURED, "https://www.debian.org/doc/debian-policy/ch-relationships.html"], "D03"),
    ("L05", "살아남은 시맨틱 파일 시스템(Spotlight·Baloo·Haiku)은 평범한 파일을 진실로 두고 재구축 가능한 색인을 얹었다. 단일 중앙 의미 저장소를 유일 진실로 둔 WinFS·Nepomuk은 실패했다.",
     ["https://learn.microsoft.com/en-us/archive/blogs/winfs/update-to-the-update", "https://lwn.net/Articles/637195/", "https://www.haiku-os.org/docs/userguide/en/queries.html"], "D04"),
    ("L06", "OS를 대체하려던 시도(WinFS, DBOS-as-OS, Fuchsia 범용화)는 후퇴했다. DBOS는 라이브러리로 살아남았다 — 오버레이/라이브러리 먼저.",
     ["https://vldb.org/pvldb/vol15/p21-skiadopoulos.pdf", "https://mast.stanford.edu/pubs/dbos_three_years_later", "https://9to5google.com/2023/01/21/fuchsia-area-120-google-layoffs/"], "D04"),
    ("L07", "가상 디렉터리 = 질의(Semantic File Systems 1991, TMSU) 는 수정 없는 앱 호환을 주지만 색인 지연·rename 비용이 따른다. BeFS 라이브 질의가 체감 품질을 정한다.",
     ["https://web.mit.edu/6.826/archive/S97/13-Gifford-Semantic-file-systems-paper.pdf", "https://github.com/oniony/TMSU/wiki/FAQ"], "D05"),
    ("L08", "실측: 이 호스트는 Proxmox LXC(Debian 13)이며 /dev/fuse 가 없다. Proxmox는 컨테이너 FUSE를 freezer 교착 때문에 비권장, 호스트 마운트+bind 권장.",
     [MEASURED, "https://pve.proxmox.com/wiki/Linux_Container"], "D05"),
    ("L09", "CID 인코딩(해시·청킹·코덱)을 고정하지 않으면 같은 내용이 여러 CID를 갖는다(IPFS). 이동+수정에 살아남으려면 안정 노드 ID와 버전별 CID를 분리해야 한다(TMSU 실패 사례). Unison: 해시=정체성, 이름=가변 포인터.",
     ["https://docs.ipfs.tech/concepts/content-addressing/", "https://github.com/oniony/TMSU/wiki/FAQ", "https://www.unison-lang.org/docs/the-big-idea/"], "D06"),
    ("L10", "실측: CHU·HSWM·USL tracked 파일 5,489개 중 434개가 중복 사본(1.83 MB), 저장소 간 중복 7건(LICENSE, 사용자 원문 등) — 트리는 사본을, CID는 노드 1개 + 소속 k개를.",
     [MEASURED], "D06"),
    ("L11", "Git·OSTree는 사용자 공간 Merkle 객체 저장소 + 분기 이력이 Linux에서 실용적임을 보였다. Btrfs/ZFS 스냅숏은 분기는 주지만 CID·merge는 없다. Dolt는 multiway 이력에 GC가 필수임을 보였다.",
     ["https://git-scm.com/book/en/v2/Git-Internals-Git-Objects", "https://ostreedev.github.io/ostree/introduction/", "https://lwn.net/Articles/1068864/"], "D07"),
    ("L12", "커널 샌드박스(Landlock·seccomp)는 추가만 가능하고 해제 불가 — 철회는 프로세스 트리 종료로만. 만료를 기본 지원하는 것은 sudoers NOTAFTER, polkit 임시 인가, systemd RuntimeMaxSec 정도.",
     ["https://docs.kernel.org/userspace-api/landlock.html", "https://man7.org/linux/man-pages/man5/sudoers.5.html", "https://man7.org/linux/man-pages/man1/systemd-run.1.html"], "D08"),
    ("L13", "능력(capability) 모델: seL4 파생 트리의 Revoke는 파생된 능력 전체를 끊고, Fuchsia는 use/offer/expose로 능력을 라우팅하며, snap plug/slot/interface는 역할 있는 명시적·철회 가능한 연결이다(만료는 없음).",
     ["https://sel4.systems/Info/Docs/seL4-manual-latest.pdf", "https://fuchsia.dev/fuchsia-src/concepts/components/v2/capabilities", "https://snapcraft.io/docs/explanation/interfaces/all-about-interfaces/"], "D08"),
    ("L14", "역할 이름 있는 n항 관계에는 타입·스키마 층이 필요하다(TypeDB 3.x). 타입 없는 하이퍼그래프(HypergraphDB)는 채택이 낮다. 교환 형식은 incidence 인코딩(W3C n-ary 패턴)으로 RDF/GQL과 호환.",
     ["https://typedb.com/fundamentals/conceptual-data-model", "https://www.w3.org/TR/swbp-n-aryRelations/", "https://www.iso.org/standard/76120.html"], "D09"),
    ("L15", "그래프 전역 매칭은 확장되지 않는다. GP2 rooted rule·MORK trie zipper처럼 재작성은 국소로 제한돼야 한다. 실측에서도 rdflib 질의는 필터를 먼저 걸도록 재작성하자 370초→수 초.",
     ["https://arxiv.org/abs/2010.03993", "https://github.com/trueagi-io/MORK", MEASURED], "D10"),
    ("L16", "Hyperon(AtomSpace+MeTTa)은 같은 비전을 5년 넘게 추구했지만 아직 1.0 이전 — 커널을 작게, 상호운용은 표준 교환 형식으로.",
     ["https://github.com/trueagi-io/hyperon-experimental", "https://hyperon.opencog.org/"], "D09"),
]

DECISIONS = {
    "D01": ("정체성 계층: 파일시스템 inode가 아니라 CHU CID를 정체성으로 둔다. inode/경로는 표현(representation)으로 바인딩한다.", ["T02"]),
    "D02": ("폴더 = 그룹 하이퍼엣지(다중 소속). 파일시스템 링크로 하이퍼엣지를 흉내 내지 않는다. 생성하는 경로 뷰는 반드시 비순환.", ["T01", "T04"]),
    "D03": ("관계 모델 = 역할 있는 절(clause). 대안(OR) 집합을 1급 하이퍼엣지로; 요구/순서처럼 의미가 다른 관계는 별도 유형으로 분리.", ["T01", "T03"]),
    "D04": ("CHU OS는 Linux 위 사용자 공간 오버레이/라이브러리로 시작한다. 하이퍼그래프가 정본이되, 파일 본문은 일반 도구로 읽히는 blob로 남기고 색인은 재구축 가능하게.", ["T11", "T12"]),
    "D05": ("경로 뷰는 daemon/API가 먼저, FUSE는 선택. LXC에서는 호스트·VM에서 FUSE를 제공하고 bind한다. 뷰 지연(변경→색인→뷰)을 처음부터 측정.", ["T33", "T40"]),
    "D06": ("CID 인코딩 고정(sha256, 무청킹 raw bytes, 코덱 명시) + 안정 노드 ID(버전 체인)와 버전별 CID 분리. 이름은 가변 포인터.", ["T02", "T11"]),
    "D07": ("영속 store = Git식 Merkle 객체 + 추가 전용 로그. multiway 가지에는 처음부터 가지치기·GC 정책.", ["T12", "T13", "T14"]),
    "D08": ("권한 = grant 하이퍼엣지 {grantor, grantee, capability, scope, not_after, derived_from}. 집행은 systemd transient unit(RuntimeMaxSec)+Landlock/seccomp, 철회는 unit 정지/cgroup.kill + 파생 grant 연쇄 철회. MetaHumotonic Covenant L0–L4와 대응.", ["T15"]),
    "D09": ("타입 스키마 층 + incidence 인코딩 표준 교환(RDF 1.1/JSON-LD + SHACL, 이후 RDF 1.2·GQL). 커널은 작게 유지.", ["T01", "T22"]),
    "D10": ("재작성·질의는 국소성 제한(rooted/anchored) 필수. 질의 엔진은 선택도 높은 조건을 먼저 적용.", ["T13", "T20"]),
}


def build():
    g = Graph()
    for p, ns in (("chu", CHU), ("r", R), ("plan", PLAN), ("prov", PROV)):
        g.bind(p, ns)
    for did, (text, plan_nodes) in DECISIONS.items():
        d = R[did]
        g.add((d, RDF.type, CHU.DesignDecision))
        g.add((d, RDFS.label, Literal(text, lang="ko")))
        for t in plan_nodes:
            g.add((d, CHU.informsPlanNode, PLAN[t]))
    for lid, text, sources, did in LESSONS:
        l = R[lid]
        g.add((l, RDF.type, CHU.Lesson))
        g.add((l, RDFS.label, Literal(text, lang="ko")))
        g.add((l, CHU.supportsDecision, R[did]))
        for s in sources:
            src = URIRef(s) if s.startswith("http") else URIRef("https://github.com/gj3447/CHU/blob/main/" + s)
            g.add((l, PROV.wasDerivedFrom, src))
            g.add((src, CHU.evidenceKind, Literal("measurement" if not s.startswith("http") else "literature")))
    return g


SHAPES = """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix chu: <https://github.com/gj3447/CHU/vocab#> .
chu:LessonShape a sh:NodeShape ; sh:targetClass chu:Lesson ;
  sh:property [ sh:path rdfs:label ; sh:minCount 1 ] ;
  sh:property [ sh:path prov:wasDerivedFrom ; sh:minCount 1 ; sh:nodeKind sh:IRI ] ;
  sh:property [ sh:path chu:supportsDecision ; sh:minCount 1 ; sh:maxCount 1 ; sh:class chu:DesignDecision ] .
chu:DecisionShape a sh:NodeShape ; sh:targetClass chu:DesignDecision ;
  sh:property [ sh:path rdfs:label ; sh:minCount 1 ] ;
  sh:property [ sh:path chu:informsPlanNode ; sh:minCount 1 ] ;
  sh:property [ sh:path [ sh:inversePath chu:supportsDecision ] ; sh:minCount 1 ;
                sh:message "every decision needs at least one supporting lesson" ] .
"""


def main():
    g = build()
    ok, _, text = validate(g, shacl_graph=Graph().parse(data=SHAPES, format="turtle"))
    plan = json.loads((HERE.parent.parent / "plan" / "chu_os_plan.graph.json").read_text())
    plan_ids = {n["id"] for n in plan["nodes"]}
    missing = sorted({t for _, ts in DECISIONS.values() for t in ts} - plan_ids)
    g.serialize(HERE / "findings.ttl", format="turtle")
    print(json.dumps({"lessons": len(LESSONS), "decisions": len(DECISIONS), "triples": len(g),
                      "shacl_conforms": ok, "plan_nodes_missing": missing}, ensure_ascii=False))
    if not ok:
        print(text)
    sys.exit(0 if ok and not missing else 1)


if __name__ == "__main__":
    main()

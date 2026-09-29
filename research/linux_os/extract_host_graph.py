#!/usr/bin/env python3
"""Linux 호스트가 이미 가진 그래프/하이퍼그래프를 CHU 하이퍼엣지로 추출한다 (std only, 읽기 전용).

출력 (--out DIR, 기본 research/linux_os/out/ — Git 제외):
  host_graph.json   CHU 하이퍼엣지 전체: {nodes, hyperedges[{id,type,participants[{role,node}]}]}
  stats.json        집계 통계 (공개 커밋용: 패키지·유닛 이름 없음)

추출 대상:
  1. dpkg 관계 절(Depends/Pre-Depends/Recommends/Suggests/Breaks/Conflicts/Enhances):
     `a | b | c` 대안 = 진짜 n항 하이퍼엣지 (dependent 1 + alternative k)
  2. dpkg Provides: 가상 패키지 -> 제공자 집합
  3. dpkg 파일 소유: 여러 패키지가 함께 소유하는 경로 (info/*.list incidence)
  4. systemd 유닛 관계 (Wants/Requires/After/...): 이항 관계 — 대조군
  5. 파일시스템 하드링크: 한 inode = 여러 경로 (--fs-root, 기본 /usr)
  6. 내용 중복: 같은 SHA-256, 다른 경로 (--content-root 로 지정한 Git 저장소들의 tracked 파일)
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

REL_FIELDS = ["Pre-Depends", "Depends", "Recommends", "Suggests", "Breaks", "Conflicts", "Enhances"]

nodes, edges = {}, []


def node(nid, ntype, **meta):
    nodes.setdefault(nid, {"id": nid, "type": ntype, **meta})
    return nid


def edge(etype, participants, **meta):
    eid = f"e{len(edges)}"
    edges.append({"id": eid, "type": etype, "participants": participants, **meta})


def parse_dpkg_status(path="/var/lib/dpkg/status"):
    pkgs, cur, key = [], {}, None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line:
            if cur:
                pkgs.append(cur)
            cur, key = {}, None
        elif line[0] in " \t" and key:
            cur[key] += " " + line.strip()
        else:
            key, _, val = line.partition(":")
            cur[key] = val.strip()
    if cur:
        pkgs.append(cur)
    return [p for p in pkgs if "install ok installed" in p.get("Status", "")]


def pkg_name(atom):
    return re.split(r"[\s(:\[]", atom.strip(), maxsplit=1)[0]


def extract_dpkg():
    pkgs = parse_dpkg_status()
    for p in pkgs:
        src = node(f"pkg:{p['Package']}", "Package")
        for field in REL_FIELDS:
            if field not in p:
                continue
            for clause in p[field].split(","):
                alts = [pkg_name(a) for a in clause.split("|") if a.strip()]
                if not alts:
                    continue
                parts = [{"role": "dependent", "node": src}]
                parts += [{"role": "alternative", "node": node(f"pkg:{a}", "Package")} for a in alts]
                edge(f"dpkg:{field}", parts, arity=len(parts), alternatives=len(alts))
        for virt in p.get("Provides", "").split(","):
            if virt.strip():
                v = node(f"pkg:{pkg_name(virt)}", "Package")
                edge("dpkg:Provides", [{"role": "virtual", "node": v}, {"role": "provider", "node": src}])
    # Provides는 가상 패키지별로 묶으면 n항: 가상 1 + 제공자 k
    owners = defaultdict(set)
    info = Path("/var/lib/dpkg/info")
    for lst in info.glob("*.list"):
        pkg = lst.stem.split(":")[0]
        for f in lst.read_text(errors="replace").splitlines():
            owners[f].add(pkg)
    shared = {f: o for f, o in owners.items() if len(o) >= 2}
    for f, o in shared.items():
        parts = [{"role": "path", "node": node(f"path:{f}", "Path")}]
        parts += [{"role": "owner", "node": node(f"pkg:{x}", "Package")} for x in sorted(o)]
        edge("dpkg:SharedOwnership", parts, arity=len(parts))
    return pkgs, owners


SYSTEMD_PROPS = ["Requires", "Requisite", "Wants", "BindsTo", "PartOf", "Conflicts", "Before", "After"]


def extract_systemd():
    try:
        units = subprocess.run(["systemctl", "list-units", "--all", "--no-legend", "--plain"],
                               capture_output=True, text=True, timeout=60).stdout.split("\n")
    except (OSError, subprocess.TimeoutExpired):
        return 0
    names = [u.split()[0] for u in units if u.strip()]
    out = subprocess.run(["systemctl", "show", "-p", "Id," + ",".join(SYSTEMD_PROPS), "--", *names],
                         capture_output=True, text=True, timeout=120).stdout
    for block in out.strip().split("\n\n"):
        kv = dict(l.split("=", 1) for l in block.splitlines() if "=" in l)
        if "Id" not in kv:
            continue
        src = node(f"unit:{kv['Id']}", "SystemdUnit")
        for prop in SYSTEMD_PROPS:
            for tgt in kv.get(prop, "").split():
                edge(f"systemd:{prop}", [{"role": "source", "node": src},
                                          {"role": "target", "node": node(f"unit:{tgt}", "SystemdUnit")}], arity=2)
    return len(names)


def extract_hardlinks(root):
    by_inode = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            if st.st_nlink > 1 and not os.path.islink(p):
                by_inode[(st.st_dev, st.st_ino)].append(p)
    for (dev, ino), paths in by_inode.items():
        if len(paths) < 2:
            continue
        parts = [{"role": "inode", "node": node(f"inode:{dev}:{ino}", "Inode")}]
        parts += [{"role": "name", "node": node(f"path:{p}", "Path")} for p in sorted(paths)]
        edge("fs:HardLinkNames", parts, arity=len(parts))
    return by_inode


def extract_content_dups(repos):
    by_hash = defaultdict(list)
    for repo in repos:
        files = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True).stdout.split(b"\0")
        for rel in files:
            if not rel:
                continue
            p = os.path.join(repo, rel.decode())
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            by_hash[h].append((os.path.basename(repo.rstrip("/")) + "/" + rel.decode(), os.path.getsize(p)))
    for h, locs in by_hash.items():
        if len(locs) < 2:
            continue
        parts = [{"role": "content", "node": node(f"cid:sha256:{h}", "Content", bytes=locs[0][1])}]
        parts += [{"role": "location", "node": node(f"path:{l}", "Path")} for l, _ in sorted(locs)]
        edge("content:SameBytes", parts, arity=len(parts), bytes=locs[0][1])
    return by_hash


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent / "out"))
    ap.add_argument("--fs-root", default="/usr")
    ap.add_argument("--content-root", action="append", default=[])
    a = ap.parse_args()

    pkgs, owners = extract_dpkg()
    n_units = extract_systemd()
    by_inode = extract_hardlinks(a.fs_root)
    by_hash = extract_content_dups(a.content_root)

    by_type = defaultdict(list)
    for e in edges:
        by_type[e["type"]].append(e)
    dep = [e for t, es in by_type.items() if t.startswith("dpkg:") and t not in ("dpkg:Provides", "dpkg:SharedOwnership") for e in es]
    nary = [e for e in dep if e["alternatives"] >= 2]
    virt = Counter(e["participants"][0]["node"] for e in by_type["dpkg:Provides"])
    multi_named = [v for v in by_inode.values() if len(v) >= 2]
    dups = [v for v in by_hash.values() if len(v) >= 2]
    stats = {
        "schema": "chu-linux-host-graph-stats/v1",
        "host": {k: v for k, v in (l.split("=", 1) for l in open("/etc/os-release").read().splitlines() if "=" in l)
                 if k in ("ID", "VERSION_ID", "ID_LIKE")},
        "kernel_release_family": os.uname().release.split("-")[0],
        "dpkg": {
            "installed_packages": len(pkgs),
            "relation_clauses": len(dep),
            "clauses_by_field": dict(Counter(e["type"] for e in dep)),
            "nary_alternative_clauses": len(nary),
            "nary_fraction": round(len(nary) / max(1, len(dep)), 4),
            "max_alternatives": max((e["alternatives"] for e in dep), default=0),
            "alternatives_histogram": dict(sorted(Counter(e["alternatives"] for e in dep).items())),
            "virtual_packages_with_2plus_providers": sum(1 for c in virt.values() if c >= 2),
            "owned_paths": len(owners),
            "paths_owned_by_2plus_packages": len(by_type["dpkg:SharedOwnership"]),
        },
        "systemd": {
            "units_listed": n_units,
            "binary_edges_by_relation": dict(Counter(e["type"] for es in by_type.values() for e in es if e["type"].startswith("systemd:"))),
        },
        "filesystem": {
            "root": a.fs_root,
            "inodes_with_2plus_names": len(multi_named),
            "max_names_per_inode": max((len(v) for v in multi_named), default=0),
        },
        "content": {
            "repositories": [os.path.basename(r.rstrip("/")) for r in a.content_root],
            "tracked_files": sum(len(v) for v in by_hash.values()),
            "distinct_contents": len(by_hash),
            "duplicated_contents": len(dups),
            "redundant_copies": sum(len(v) - 1 for v in dups),
            "redundant_bytes": sum((len(v) - 1) * v[0][1] for v in dups),
            "cross_repository_duplicates": sum(1 for v in dups if len({l.split("/")[0] for l, _ in v}) >= 2),
        },
        "graph": {"nodes": len(nodes), "hyperedges": len(edges),
                  "hyperedges_by_type": dict(Counter(e["type"] for e in edges))},
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "host_graph.json").write_text(json.dumps({"schema": "chu-hypergraph/v0", "nodes": list(nodes.values()),
                                                     "hyperedges": edges}, ensure_ascii=False))
    (out / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

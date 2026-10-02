#!/usr/bin/env python3
"""CHU OS 계획 하이퍼그래프 검증기 (std only).

B-graph 의미론: hyperedge의 tail이 전부 완료되면 head 착수 가능.
검사: chu-plan/v1 구조 · 참조 무결성 · 비순환(Kahn) · 고아 노드.
완료 증거는 선언된 메타데이터의 구조만 검사한다. 이 도구는 과거 검사 실행,
증거 파일 존재 또는 증거가 현재 작업트리와 일치하는지를 주장하지 않는다.
출력: 위상 레이어 · 임계 경로 · 마일스톤 합계.
  python3 plan/check_plan.py            # 보고서
  python3 plan/check_plan.py --mermaid  # mermaid flowchart
"""
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

PLAN_PATH = Path(__file__).parent / "chu_os_plan.graph.json"
NODE_FIELDS = ("id", "milestone", "layer", "effort", "title", "deliverable", "verify")
EDGE_FIELDS = ("id", "type", "tail", "head")


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def endpoint_list(value):
    return (isinstance(value, list) and bool(value) and
            all(nonempty_string(item) for item in value) and len(value) == len(set(value)))


def safe_relative_path(value):
    if not nonempty_string(value):
        return False
    path = Path(value)
    return bool(path.parts) and not path.is_absolute() and ".." not in path.parts and value != "."


def iso_date(value):
    if not nonempty_string(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def structural_errors(graph):
    """Return chu-plan/v1 structural errors without consulting evidence files."""
    errors = []
    if not isinstance(graph, dict):
        return ["root must be an object"]
    if graph.get("schema") != "chu-plan/v1":
        errors.append("schema must be chu-plan/v1")
    if not nonempty_string(graph.get("about")):
        errors.append("about must be a nonempty string")
    for key in ("nodes", "hyperedges"):
        if not isinstance(graph.get(key), list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors
    if not graph["nodes"]:
        errors.append("nodes must be nonempty")
    if not graph["hyperedges"]:
        errors.append("hyperedges must be nonempty")
    for index, node in enumerate(graph["nodes"]):
        label = f"node[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in NODE_FIELDS:
            if field not in node:
                errors.append(f"{label}: missing {field}")
        for field in ("id", "milestone", "layer", "title", "deliverable", "verify"):
            if field in node and not nonempty_string(node[field]):
                errors.append(f"{label}: {field} must be a nonempty string")
        effort = node.get("effort")
        finite_effort = (
            isinstance(effort, int) and not isinstance(effort, bool) and effort <= 10 ** 308
        ) or (isinstance(effort, float) and math.isfinite(effort))
        if not finite_effort or effort <= 0:
            errors.append(f"{label}: effort must be a finite positive number")
        if "status" in node and (not isinstance(node["status"], str) or
                                  node["status"] not in {"pending", "done"}):
            errors.append(f"{label}: status must be pending or done")
        evidence = node.get("completion_evidence")
        if evidence is not None:
            if not isinstance(evidence, dict):
                errors.append(f"{label}: completion_evidence must be an object")
            else:
                for field in ("date", "scope", "source", "checks"):
                    if field not in evidence:
                        errors.append(f"{label}: completion_evidence missing {field}")
                if "date" in evidence and not iso_date(evidence["date"]):
                    errors.append(f"{label}: completion_evidence date must be an ISO date")
                if "scope" in evidence and not nonempty_string(evidence["scope"]):
                    errors.append(f"{label}: completion_evidence scope must be a nonempty string")
                if "source" in evidence and not safe_relative_path(evidence["source"]):
                    errors.append(f"{label}: completion_evidence source must be a safe repo-relative path")
                checks = evidence.get("checks")
                if not isinstance(checks, list) or not checks or not all(nonempty_string(v) for v in checks):
                    errors.append(f"{label}: completion_evidence checks must be a nonempty string list")
    for index, edge in enumerate(graph["hyperedges"]):
        label = f"hyperedge[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in EDGE_FIELDS:
            if field not in edge:
                errors.append(f"{label}: missing {field}")
        if "id" in edge and not nonempty_string(edge["id"]):
            errors.append(f"{label}: id must be a nonempty string")
        if edge.get("type") != "requires":
            errors.append(f"{label}: type must be requires")
        for field in ("tail", "head"):
            if field in edge and not endpoint_list(edge[field]):
                errors.append(f"{label}: {field} must be a nonempty unique string list")
    if all(isinstance(n, dict) and nonempty_string(n.get("id")) for n in graph["nodes"]):
        errors += [f"duplicate node ID {uid}" for uid, count in
                   Counter(n["id"] for n in graph["nodes"]).items() if count > 1]
    if all(isinstance(e, dict) and nonempty_string(e.get("id")) for e in graph["hyperedges"]):
        errors += [f"duplicate hyperedge ID {uid}" for uid, count in
                   Counter(e["id"] for e in graph["hyperedges"]).items() if count > 1]
    return errors


def fail(errors):
    print("FAIL\n  " + "\n  ".join(errors))
    return 1


def main():
    try:
        g = json.loads(PLAN_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return fail([f"cannot read plan JSON: {exc}"])
    errors = structural_errors(g)
    if errors:
        return fail(errors)

    nodes = {n["id"]: n for n in g["nodes"]}
    preds = defaultdict(set)  # head -> tail 합집합 (하이퍼엣지를 bipartite로 펼친 것)
    for e in g["hyperedges"]:
        for v in e["tail"] + e["head"]:
            if v not in nodes:
                errors.append(f"{e['id']}: unknown node {v}")
        for h in e["head"]:
            preds[h] |= set(e["tail"])

    touched = {v for e in g["hyperedges"] for v in e["tail"] + e["head"]}
    errors += [f"orphan node {v}" for v in nodes if v not in touched]
    for node in g["nodes"]:
        if node.get("status") == "done":
            unfinished = [p for p in preds[node["id"]] if p in nodes and nodes[p].get("status") != "done"]
            if unfinished:
                errors.append(f"{node['id']}: done before prerequisites {sorted(unfinished)}")
    if errors:
        return fail(errors)

    # Kahn 위상 정렬 (레이어 단위)
    indeg = {v: len(preds[v]) for v in nodes}
    succ = defaultdict(set)
    for h, ts in preds.items():
        for t in ts:
            succ[t].add(h)
    layers, frontier = [], sorted(v for v in nodes if indeg[v] == 0)
    while frontier:
        layers.append(frontier)
        nxt = []
        for v in frontier:
            for s in succ[v]:
                indeg[s] -= 1
                if indeg[s] == 0:
                    nxt.append(s)
        frontier = sorted(nxt)
    if sum(map(len, layers)) != len(nodes):
        errors.append("cycle detected: " + ", ".join(v for v in nodes if indeg[v] > 0))

    if errors:
        return fail(errors)

    if "--mermaid" in sys.argv:
        print("flowchart LR")
        for v, n in nodes.items():
            mark = " ✓" if n.get("status") == "done" else ""
            print(f'  {v}["{v}{mark} {n["title"][:28]}"]')
        for e in g["hyperedges"]:
            tail = " & ".join(e["tail"])
            head = " & ".join(e["head"])
            print(f"  {tail} --> {head}")
        return 0

    # 임계 경로 (최장 effort 경로)
    finish, via = {}, {}
    for layer in layers:
        for v in layer:
            best = max(preds[v], key=lambda p: finish[p], default=None)
            finish[v] = nodes[v]["effort"] + (finish[best] if best else 0)
            via[v] = best
    end = max(finish, key=finish.get)
    path = []
    while end:
        path.append(end)
        end = via[end]
    path.reverse()

    ms = defaultdict(float)
    for n in nodes.values():
        ms[n["milestone"]] += n["effort"]

    print(f"OK  nodes={len(nodes)} hyperedges={len(g['hyperedges'])} acyclic=yes orphans=0")
    print("\n위상 레이어 (같은 줄 = 병렬 가능):")
    for i, layer in enumerate(layers):
        print(f"  L{i}: " + ", ".join(layer))
    print(f"\n임계 경로 ({finish[path[-1]]:g}일): " + " -> ".join(path))
    print("\n마일스톤 effort 합계(일): " + ", ".join(f"{k}={v:g}" for k, v in sorted(ms.items())))
    done = [v for v, n in nodes.items() if n.get("status") == "done"]
    left = sum(n["effort"] for n in nodes.values() if n.get("status") != "done")
    print(f"총 effort: {sum(ms.values()):g}일 (완료 {len(done)}개: {', '.join(done) or '-'} / 남은 {left:g}일)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

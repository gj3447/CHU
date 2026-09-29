#!/usr/bin/env python3
"""CHU OS 계획 하이퍼그래프 검증기 (std only).

B-graph 의미론: hyperedge의 tail이 전부 완료되면 head 착수 가능.
검사: 참조 무결성 · 비순환(Kahn) · 고아 노드. 출력: 위상 레이어 · 임계 경로 · 마일스톤 합계.
  python3 plan/check_plan.py            # 보고서
  python3 plan/check_plan.py --mermaid  # mermaid flowchart
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

g = json.loads((Path(__file__).parent / "chu_os_plan.graph.json").read_text())
nodes = {n["id"]: n for n in g["nodes"]}
preds = defaultdict(set)  # head -> tail 합집합 (하이퍼엣지를 bipartite로 펼친 것)
errors = []

for e in g["hyperedges"]:
    for v in e["tail"] + e["head"]:
        if v not in nodes:
            errors.append(f"{e['id']}: unknown node {v}")
    for h in e["head"]:
        preds[h] |= set(e["tail"])

touched = {v for e in g["hyperedges"] for v in e["tail"] + e["head"]}
errors += [f"orphan node {v}" for v in nodes if v not in touched]

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
    print("FAIL\n  " + "\n  ".join(errors))
    sys.exit(1)

if "--mermaid" in sys.argv:
    print("flowchart LR")
    for v, n in nodes.items():
        mark = " ✓" if n.get("status") == "done" else ""
        print(f'  {v}["{v}{mark} {n["title"][:28]}"]')
    for e in g["hyperedges"]:
        tail = " & ".join(e["tail"])
        head = " & ".join(e["head"])
        print(f"  {tail} --> {head}")
    sys.exit(0)

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

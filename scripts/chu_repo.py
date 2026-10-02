#!/usr/bin/env python3
"""Read-only repository graph views. Source membership and checks are not authority to execute."""
import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import tomllib
from urllib.parse import quote, unquote, urlsplit

from pyshacl import validate
from rdflib import Dataset, Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS, PROV, SKOS
from rdflib.plugins.sparql.parser import parseQuery

from check_cli_tools import bindings, run
from chu_dev import DEV, ROOT, catalog

ENG = Namespace("https://github.com/gj3447/CHU/engineering#")
PLAN = Namespace("https://github.com/gj3447/CHU/plan#")
QUERIES = {"files", "profiles", "assets", "plan", "evidence", "gaps", "source-graphs"}
AUTHORITIES = {"USER_PRIMARY", "SECONDARY_AI", "OWNER_INSTRUCTION", "UNSPECIFIED"}
LIFECYCLES = {"CURRENT", "HISTORICAL", "REFERENCE", "PRESERVED"}
ROLES = {"data", "ontology", "shapes", "queries", "source"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cid(data):
    return URIRef("urn:sha256:" + sha(data))


def record_id(*values):
    # Digest of a contextual binding record, distinct from the file's raw-byte CID.
    return URIRef("urn:chu:engineering-record:" + sha(json.dumps(values, ensure_ascii=False).encode()))


def source_files():
    names = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others",
                                     "--exclude-standard"], cwd=ROOT).decode().split("\0")
    result = {}
    for name in sorted(set(names) - {""}):
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"Inventory requires an in-repository file target: {name}")
        if not path.is_file():
            raise ValueError(f"Git source missing from working tree: {name}")
        result[name] = path.read_bytes()
    return result


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def local_jsonld_contexts(value):
    """Parsing the local inventory must not dereference remote/nested JSON-LD contexts."""
    if isinstance(value, dict):
        if "@import" in value:
            raise ValueError("Imported JSON-LD contexts are outside repository parsing")
        if "@context" in value:
            context = value["@context"]
            contexts = context if isinstance(context, list) else [context]
            if any(item is not None and not isinstance(item, dict) for item in contexts):
                raise ValueError("Remote JSON-LD contexts are outside repository parsing")
        for child in value.values():
            local_jsonld_contexts(child)
    elif isinstance(value, list):
        for child in value:
            local_jsonld_contexts(child)


def read_catalog(files):
    config = json.loads(files["engineering/catalog.json"])
    if config.get("schema") != "chu-engineering/v1" or config.get("authority") != "SECONDARY_AI":
        raise ValueError("Invalid engineering catalog schema/authority")
    known_checks = set(catalog().subjects(RDF.type, DEV.Check))
    for key in ("collections", "profiles"):
        rows = config[key]
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"Missing {key}")
        ids = [row["id"] for row in rows]
        if len(ids) != len(set(ids)) or any(not re.fullmatch(r"[a-z][a-z0-9-]*", x) for x in ids):
            raise ValueError(f"Duplicate or malformed {key} IDs")
        for row in rows:
            if not row["label"] or row["lifecycle"] not in LIFECYCLES:
                raise ValueError(f"Invalid {key} label/lifecycle")
    for group in config["collections"]:
        if group["authority"] not in AUTHORITIES or not group["include"]:
            raise ValueError(f"Invalid collection {group['id']}")
        if group["authority"] == "USER_PRIMARY" and (group["id"] != "primary" or
                any("*" in p or not p.startswith("canon/sources/USER_PRIMARY_") for p in group["include"])):
            raise ValueError("Primary authority requires explicit canonical source paths")
    for profile in config["profiles"]:
        if not profile["scope"] or not profile["checks"] or not profile["assets"]:
            raise ValueError(f"Incomplete profile {profile['id']}")
        if any(DEV[name] not in known_checks for name in profile["checks"]):
            raise ValueError(f"Unregistered check in {profile['id']}")
        if not set(profile["assets"]) <= ROLES:
            raise ValueError(f"Unregistered asset role in {profile['id']}")
    return config


def scan_syntax_and_links(files):
    counts, broken, workspace_links = Counter(), [], 0
    for path, data in files.items():
        suffix = Path(path).suffix
        if suffix == ".json":
            json.loads(data)
        elif suffix == ".toml":
            tomllib.loads(data.decode())
        elif suffix == ".py":
            ast.parse(data, filename=path)
        elif suffix == ".rq":
            parseQuery(data.decode())
        elif suffix == ".md":
            text = re.sub(r"(?ms)^```.*?^```[^\n]*", "", data.decode())
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                target = target.strip()
                target = target[1:target.index(">")] if target.startswith("<") and ">" in target else target.split()[0]
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                resolved = (ROOT / Path(path).parent / unquote(url.path)).resolve()
                if not resolved.is_relative_to(ROOT):
                    workspace_links += 1
                    continue
                relative = resolved.relative_to(ROOT).as_posix()
                if relative != "." and relative not in files and not any(p.startswith(relative + "/") for p in files):
                    broken.append({"source": path, "target": target})
        counts[suffix or "extensionless"] += 1
    return {"extensions": dict(sorted(counts.items())), "broken_local_links": broken,
            "workspace_links_not_checked": workspace_links,
            "link_scope": "inline Markdown local paths; excludes anchors, reference-style links and external/workspace destinations"}


def build(files=None):
    files = source_files() if files is None else files
    config = read_catalog(files)
    dataset = Dataset()
    graph = dataset.graph(ENG.inventory)
    for prefix, ns in (("eng", ENG), ("dev", DEV), ("prov", PROV), ("plan", PLAN)):
        dataset.bind(prefix, ns)

    def entity(node, kind):
        graph.add((node, RDF.type, kind))
        graph.add((node, RDF.type, PROV.Entity))
        return node

    def add(node, pred, value):
        graph.add((node, pred, value))

    groups = {row["id"]: row for row in config["collections"]}
    for key, row in groups.items():
        node = entity(ENG["collection-" + key], ENG.Collection)
        add(node, SKOS.prefLabel, Literal(row["label"]))
    representations, membership, rdf_paths = {}, Counter(), set()
    for path, data in files.items():
        selected = [row for row in groups.values() if matches(path, row["include"])
                    and not matches(path, row.get("exclude", []))]
        if len(selected) != 1:
            raise ValueError(f"Expected exactly one primary collection for {path}; got {[r['id'] for r in selected]}")
        group = selected[0]
        membership[group["id"]] += 1
        artifact = entity(cid(data), ENG.Artifact)
        add(artifact, DCTERMS.extent, Literal(len(data), datatype=XSD.integer))
        representation = entity(record_id("representation", path, str(artifact)), ENG.Representation)
        representations[path] = representation
        add(representation, ENG.content, artifact)
        add(representation, DEV.pathView, Literal(path))
        add(representation, ENG.collection, ENG["collection-" + group["id"]])
        add(representation, ENG.authority, Literal(group["authority"]))
        add(representation, ENG.lifecycle, Literal(group["lifecycle"]))
        if Path(path).suffix in {".ttl", ".jsonld"}:
            if path.endswith(".jsonld"):
                local_jsonld_contexts(json.loads(data))
            dataset.graph(representation).parse(data=data, format="json-ld" if path.endswith(".jsonld") else "turtle",
                                                publicID="https://github.com/gj3447/CHU/" + quote(path))
            rdf_paths.add(path)
    asset_paths = set()
    for row in config["profiles"]:
        profile = entity(ENG["profile-" + row["id"]], ENG.Profile)
        for pred, value in ((SKOS.prefLabel, row["label"]), (ENG.lifecycle, row["lifecycle"]), (ENG.scope, row["scope"])):
            add(profile, pred, Literal(value))
        for name in row["checks"]:
            check = entity(DEV[name], DEV.Check)
            add(profile, ENG.validatedBy, check)
        for role, patterns in row["assets"].items():
            for pattern in patterns:
                selected = sorted(p for p in files if matches(p, [pattern]))
                if not selected:
                    raise ValueError(f"Profile {row['id']} has missing asset {pattern}")
                for path in selected:
                    asset_paths.add(path)
                    binding = entity(record_id("asset", row["id"], role, path), ENG.AssetBinding)
                    add(binding, ENG.profile, profile)
                    add(binding, ENG.representation, representations[path])
                    add(binding, ENG.assetRole, Literal(role))
    if rdf_paths - asset_paths:
        raise ValueError(f"RDF assets lack a validation profile: {sorted(rdf_paths - asset_paths)}")

    plan = json.loads(files["plan/chu_os_plan.graph.json"])
    for row in plan["nodes"]:
        node = entity(PLAN[row["id"]], ENG.PlanTask)
        add(node, SKOS.prefLabel, Literal(row["title"]))
        add(node, ENG.taskStatus, Literal(row.get("status", "pending")))
    for row in plan["hyperedges"]:
        gate = entity(PLAN[row["id"]], ENG.Gate)
        add(gate, ENG.gateSemantics, Literal("ALL_TAILS"))
        for field, pred in (("tail", ENG.tailTask), ("head", ENG.headTask)):
            for task in row[field]:
                add(gate, pred, PLAN[task])

    archived = json.loads(files["os/boot-verification.json"])
    report = cid(files["os/boot-verification.json"])
    freshness = Counter()
    for path, digest in archived["source_sha256"].items():
        binding = entity(record_id("evidence", str(report), path, digest), ENG.EvidenceBinding)
        add(binding, DEV.pathView, Literal(path))
        add(binding, ENG.sourceReport, report)
        recorded = entity(URIRef("urn:sha256:" + digest), ENG.Artifact)
        add(binding, ENG.recordedContent, recorded)
        state = "UNAVAILABLE"
        if path in files:
            current = cid(files[path])
            add(binding, ENG.currentContent, current)
            state = "MATCH" if current == recorded else "CHANGED"
        add(binding, ENG.freshness, Literal(state))
        freshness[state] += 1

    for row in config.get("gaps", []):
        gap = entity(ENG["gap-" + row["id"]], ENG.Gap)
        add(gap, SKOS.prefLabel, Literal(row["label"]))
        add(gap, ENG.scope, Literal(row["scope"]))
        add(gap, ENG.gapState, Literal("OPEN"))
        for task in row.get("tasks", []):
            add(gap, ENG.addressesTask, PLAN[task])
    snapshot = cid(json.dumps({p: sha(data) for p, data in sorted(files.items())}, separators=(",", ":")).encode())
    entity(snapshot, PROV.Collection)
    add(snapshot, PROV.wasAttributedTo, ENG.indexer)
    add(ENG.indexer, RDF.type, PROV.SoftwareAgent)
    for artifact in {cid(data) for data in files.values()}:
        add(snapshot, PROV.hadMember, artifact)
    summary = {"schema": "chu-repository-map/v1", "ok": True, "files": len(files),
               "byte_artifacts": len({cid(data) for data in files.values()}), "snapshot": str(snapshot),
               "collections": dict(sorted(membership.items())), "profiles": len(config["profiles"]),
               "registered_checks": len(set(catalog().subjects(RDF.type, DEV.Check))),
               "plan": {"tasks": len(plan["nodes"]), "gates": len(plan["hyperedges"]),
                        "declared_done": sum(n.get("status") == "done" for n in plan["nodes"])},
               "source_graphs": len(rdf_paths), "evidence_freshness": dict(freshness),
               "scope": config["scope"], "review": "full structural inventory; semantic reviews are bounded by engineering/README.md"}
    return dataset, summary


def validate_graph(dataset, files=None):
    graph = dataset.graph(ENG.inventory)
    ontology = Graph().parse(ROOT / "engineering/ontology.ttl")
    shapes = Graph().parse(ROOT / "engineering/shapes.ttl")
    valid, _, report = validate(graph, shacl_graph=shapes, ont_graph=ontology, inference="none", meta_shacl=True)
    errors = [] if valid else [str(report)]
    for subject, pred, obj in graph:
        if not str(pred).startswith(str(ENG)):
            continue
        domain, range_ = ontology.value(pred, RDFS.domain), ontology.value(pred, RDFS.range)
        if domain is None or range_ is None:
            errors.append(f"Unregistered predicate: {pred}")
            continue
        if (subject, RDF.type, domain) not in graph:
            errors.append(f"Wrong predicate domain: {pred}")
        if str(range_).startswith(str(XSD)):
            if not isinstance(obj, Literal) or (obj.datatype or XSD.string) != range_:
                errors.append(f"Wrong predicate datatype: {pred}")
        elif (obj, RDF.type, range_) not in graph:
            errors.append(f"Wrong predicate range: {pred}")
    files = source_files() if files is None else files
    config = read_catalog(files)
    rows = query(dataset, "files")
    if len(rows) != len(files) or {r["path"] for r in rows} != set(files):
        errors.append("Inventory omitted/duplicated a source representation")
    for row in rows:
        path = row["path"]
        if path not in files or row["content"] != str(cid(files[path])):
            errors.append(f"Inventory byte CID mismatch: {path}")
            continue
        groups = [g for g in config["collections"] if matches(path, g["include"])
                  and not matches(path, g.get("exclude", []))]
        if len(groups) != 1 or (row["collection"], row["authority"], row["lifecycle"]) != (
                str(ENG["collection-" + groups[0]["id"]]), groups[0]["authority"], groups[0]["lifecycle"]):
            errors.append(f"Inventory source authority/lifecycle mismatch: {path}")
    expected_profiles = {(str(ENG["profile-" + p["id"]]), name, p["lifecycle"], p["scope"])
                         for p in config["profiles"] for name in p["checks"]}
    actual_profiles = {(r["profile"], r["check"].removeprefix(str(DEV)), r["lifecycle"], r["scope"])
                       for r in query(dataset, "profiles")}
    if actual_profiles != expected_profiles:
        errors.append("Profile/check/scope answers differ from catalog")
    expected_assets = {(str(ENG["profile-" + p["id"]]), role, path)
                       for p in config["profiles"] for role, patterns in p["assets"].items()
                       for path in files if matches(path, patterns)}
    if {(r["profile"], r["role"], r["path"]) for r in query(dataset, "assets")} != expected_assets:
        errors.append("Profile asset-role answers differ from catalog")
    plan = json.loads(files["plan/chu_os_plan.graph.json"])
    expected_statuses = {PLAN[n["id"]]: n.get("status", "pending") for n in plan["nodes"]}
    if {n: str(graph.value(n, ENG.taskStatus)) for n in graph.subjects(RDF.type, ENG.PlanTask)} != expected_statuses:
        errors.append("Projected task statuses differ from canonical plan")
    expected_gates = {(str(PLAN[e["id"]]), str(PLAN[t]), str(PLAN[h]))
                      for e in plan["hyperedges"] for t in e["tail"] for h in e["head"]}
    if {(r["gate"], r["tail"], r["head"]) for r in query(dataset, "plan")} != expected_gates:
        errors.append("Dependency gate answers lost or added an AND endpoint")
    archived = json.loads(files["os/boot-verification.json"])
    evidence = query(dataset, "evidence")
    if len(evidence) != len(archived["source_sha256"]) or {r["path"] for r in evidence} != set(archived["source_sha256"]):
        errors.append("Evidence bindings omit or duplicate archived inputs")
    for row in evidence:
        expected_digest = archived["source_sha256"].get(row["path"])
        if row["recorded"] != "urn:sha256:" + str(expected_digest) or row["report"] != str(cid(files["os/boot-verification.json"])):
            errors.append(f"Recorded evidence differs from archive: {row['path']}")
        current = str(cid(files[row["path"]])) if row["path"] in files else None
        state = "UNAVAILABLE" if current is None else "MATCH" if current == row["recorded"] else "CHANGED"
        if row["freshness"] != state or row.get("current") != current:
            errors.append(f"Evidence freshness answer is false: {row['path']}")
    return errors


def query(dataset, name):
    if name not in QUERIES:
        raise ValueError(f"Unknown repository query: {name}")
    return [{str(k): str(v) for k, v in row.asdict().items()}
            for row in dataset.query((ROOT / "engineering/queries" / (name + ".rq")).read_text())]


def check(out):
    subprocess.run([sys.executable, str(ROOT / "plan/check_plan.py")], cwd=ROOT,
                   check=True, capture_output=True, timeout=30)
    files = source_files()
    dataset, summary = build(files)
    errors = validate_graph(dataset, files)
    scan = scan_syntax_and_links(files)
    if errors or scan["broken_local_links"]:
        raise ValueError(json.dumps({"graph": errors, "links": scan["broken_local_links"]}))
    out.mkdir(parents=True, exist_ok=True)
    dataset.serialize(out / "repository.trig", format="trig")
    restored = Dataset().parse(out / "repository.trig", format="trig")
    original_graphs = {g.identifier: g for g in dataset.graphs() if len(g)}
    restored_graphs = {g.identifier: g for g in restored.graphs() if len(g)}
    if original_graphs.keys() != restored_graphs.keys() or any(
            not isomorphic(g, restored_graphs[name]) for name, g in original_graphs.items()):
        raise ValueError("TriG roundtrip changed named graph boundaries or content")
    answers = {name: query(dataset, name) for name in sorted(QUERIES)}
    with TemporaryDirectory(prefix="chu-repo-query-") as directory:
        store = Path(directory) / "store"
        run("oxigraph", "load", "--location", store, "--file", out / "repository.trig")
        for name in sorted(QUERIES):
            query_file = ROOT / "engineering/queries" / (name + ".rq")
            expected = json.loads(dataset.query(query_file.read_text()).serialize(format="json"))
            actual = json.loads(run("oxigraph", "query", "--location", store,
                                   "--query-file", query_file, "--results-format", "json").stdout)
            if not actual["results"]["bindings"] or bindings(expected) != bindings(actual):
                raise ValueError(f"Empty or disagreeing competency query: {name}")
    (out / "repository-answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=2) + "\n")
    summary.update({"scan": scan, "named_graph_roundtrip": True, "engines": ["RDFLib", "Oxigraph"],
                    "query_rows": {name: len(rows) for name, rows in answers.items()}})
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "query", "export", "check"):
        p = sub.add_parser(command)
        p.add_argument("--json", action="store_true", help="Machine-readable output (default except export)")
        if command == "query":
            p.add_argument("name", choices=sorted(QUERIES))
            p.add_argument("--path", help="Optional file path glob for files/assets/evidence rows")
        if command == "export":
            p.add_argument("--format", choices=["trig", "nquads"], default="trig")
        if command == "check":
            p.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            result = check(args.out.resolve())
        else:
            dataset, summary = build()
            if args.command == "export":
                print(dataset.serialize(format=args.format))
                return 0
            if args.command == "query":
                result = query(dataset, args.name)
                if args.path:
                    if args.name not in {"files", "assets", "evidence"}:
                        raise ValueError("--path applies only to files/assets/evidence")
                    result = [row for row in result if fnmatch.fnmatchcase(row.get("path", ""), args.path)]
            else:
                result = {**summary, "observed_at": datetime.now(timezone.utc).isoformat(),
                          "validation": "discovery only; run ./chu check --only repo-graph --json"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())

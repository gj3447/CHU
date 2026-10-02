#!/usr/bin/env python3
"""CHU's local, noninteractive development interface. Registry != authorization."""
import argparse
import hashlib
import json
import os
import platform
import signal
import subprocess
import sys
import time
import tomllib
import uuid
from datetime import datetime, timezone
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import PROV, SKOS

ROOT = Path(__file__).resolve().parents[1]
DEV = Namespace("https://github.com/gj3447/CHU/dev#")
QUERIES = {"tools", "checks", "sources", "failures", "candidates"}


def now():
    return datetime.now(timezone.utc).isoformat()


def catalog():
    return Graph().parse(ROOT / "dev/catalog.ttl").parse(ROOT / "dev/tool-research.ttl")


def binary_specs():
    manifest = json.loads((ROOT / "dev/downloads.json").read_text())
    return {name: spec for name, spec in manifest.items()
            if isinstance(spec, dict) and spec.get("bootstrap", False)}


def matches_version(output, version):
    import re
    return bool(re.search(r"(?<![\w.])v?" + re.escape(version) + r"(?![\w.])", output))


def commands(graph=None):
    g = catalog() if graph is None else graph
    rows = []
    for node in g.subjects(RDF.type, DEV.Check):
        rows.append({
            "id": str(node).split("#")[-1], "uri": str(node),
            "label": str(g.value(node, SKOS.prefLabel)),
            "argv": [str(x) for x in Collection(g, g.value(node, DEV.argv))],
            "timeout": int(g.value(node, DEV.timeout)),
            "effect": str(g.value(node, DEV.effect)),
            "requires": sorted(str(x) for x in g.objects(node, DEV.requires)),
        })
    return sorted(rows, key=lambda r: r["id"])


def graph_validate(graph=None):
    g = catalog() if graph is None else graph
    shapes = Graph().parse(ROOT / "dev/shapes.ttl")
    ontology = Graph().parse(ROOT / "dev/ontology.ttl")
    ok, _, report = validate(g, shacl_graph=shapes, ont_graph=ontology,
                             inference="none", meta_shacl=True)
    errors = [] if ok else [report]
    for predicate in set(g.predicates()):
        if str(predicate).startswith(str(DEV)) and (predicate, RDF.type, None) not in ontology:
            errors.append(f"Unregistered predicate: {predicate}")
    for predicate, domain in ontology.subject_objects(RDFS.domain):
        for subject in g.subjects(predicate, None):
            if (subject, RDF.type, domain) not in g:
                errors.append(f"Wrong predicate domain: {subject} / {predicate}")
    for predicate in (DEV.argv, DEV.probe):
        for head in g.objects(None, predicate):
            seen = set()
            cell = head
            while cell != RDF.nil:
                if cell in seen:
                    errors.append("Cyclic argv list")
                    break
                seen.add(cell)
                first, rest = list(g.objects(cell, RDF.first)), list(g.objects(cell, RDF.rest))
                if (len(first) != 1 or len(rest) != 1 or not isinstance(first[0], Literal)
                        or first[0].datatype not in (None, XSD.string) or not str(first[0])):
                    errors.append("Malformed argv list")
                    break
                cell = rest[0]
    if errors:
        return {"ok": False, "errors": errors, "triples": len(g)}
    # Lists, identifiers and toolchain pins require cross-file checks beyond SHACL.
    try:
        for row in commands(g):
            if not row["argv"] or any(not part for part in row["argv"]):
                errors.append(f"{row['id']}: empty argv")
        lean_files = {str(p.relative_to(ROOT)) for p in (ROOT / "lean").glob("*.lean")}
        declared = {r["argv"][-1] for r in commands(g) if r["id"].startswith("lean-")}
        if lean_files != declared or not lean_files:
            errors.append("Lean check coverage differs from the actual source files")
        pins = {
            DEV.python: (ROOT / ".python-version").read_text().strip(),
            DEV.lean: (ROOT / "lean-toolchain").read_text().strip().split(":v")[-1],
            DEV.rust: tomllib.loads((ROOT / "rust-toolchain.toml").read_text())["toolchain"]["channel"],
            DEV.uv: tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["uv"]["required-version"].removeprefix("=="),
        }
        pins.update({DEV[name]: spec["version"] for name, spec in binary_specs().items()})
        lock = tomllib.loads((ROOT / "uv.lock").read_text())
        for package in lock["package"]:
            if package["name"] in {"ruff", "pytest", "pyshacl", "rdflib"}:
                pins[DEV[package["name"]]] = package["version"]
        for node, version in pins.items():
            if str(g.value(node, DEV.version)) != version:
                errors.append(f"Version drift: {node} should be {version}")
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(str(exc))
    return {"ok": not errors, "errors": errors, "triples": len(g)}


def execute(argv, timeout, cwd=ROOT):
    """Capture errors and timeouts as data; never run through a shell."""
    started = time.monotonic()
    try:
        proc = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, start_new_session=True)
    except OSError as exc:
        return {"status": "ERROR", "exit_code": None, "stdout": "", "stderr": str(exc),
                "duration_s": round(time.monotonic() - started, 3)}
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        status = "PASS" if proc.returncode == 0 else "FAIL"
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
        status = "TIMEOUT"
    return {"status": status, "exit_code": proc.returncode, "stdout": stdout,
            "stderr": stderr, "duration_s": round(time.monotonic() - started, 3)}


def doctor():
    g = catalog()
    rows = []
    for node in sorted(g.subjects(RDF.type, DEV.Tool), key=str):
        version = g.value(node, DEV.version)
        head = g.value(node, DEV.probe)
        argv = [sys.executable if str(x) == "{python}" else str(x)
                for x in Collection(g, head)]
        result = execute(argv, 60)
        output = result["stdout"] + result["stderr"]
        # Exact version token, not a substring match (1.2 must not match 1.20).
        matched = matches_version(output, str(version))
        rows.append({"tool": str(node), "expected": str(version), "argv": argv,
                     **result, "matches_pin": matched})
    return {"schema": "chu-doctor/v1", "observed_at": now(),
            "ok": all(r["status"] == "PASS" and r["matches_pin"] for r in rows),
            "tools": rows, "optional": {"fuse_device": Path("/dev/fuse").exists()},
            "scope": "local development; no shared KG authentication or OS runtime claim"}


def source_snapshot():
    listing = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=ROOT, check=True, capture_output=True).stdout
    result = {}
    for name in sorted(set(listing.decode().split("\0")) - {""}):
        path = ROOT / name
        if path.is_file():
            result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def write_evidence(report, out):
    g = Graph()
    g.bind("dev", DEV)
    g.bind("prov", PROV)
    run = URIRef("urn:uuid:" + report["run_id"])
    agent = DEV.localRunner
    g.add((agent, RDF.type, PROV.SoftwareAgent))
    g.add((run, RDF.type, PROV.Activity))
    g.add((run, PROV.wasAssociatedWith, agent))
    g.add((run, PROV.startedAtTime, Literal(report["started_at"], datatype=XSD.dateTime)))
    g.add((run, PROV.endedAtTime, Literal(report["ended_at"], datatype=XSD.dateTime)))
    for path, digest in report["source_sha256"].items():
        entity = URIRef("urn:sha256:" + digest)
        g.add((entity, RDF.type, PROV.Entity))
        g.add((entity, DEV.pathView, Literal(path)))
        g.add((run, PROV.used, entity))
    for row in report["checks"]:
        observation = URIRef(str(run) + ":" + row["id"])
        g.add((observation, RDF.type, DEV.Observation))
        g.add((observation, RDF.type, PROV.Entity))
        g.add((observation, PROV.wasGeneratedBy, run))
        g.add((observation, DEV.check, URIRef(row["uri"])))
        g.add((observation, DEV.status, Literal(row["status"])))
    g.serialize(out / "evidence.ttl", format="turtle")


def check(only=None):
    valid = graph_validate()
    if not valid["ok"]:
        return {"ok": False, "graph": valid}
    rows = commands()
    if only:
        unknown = set(only) - {r["id"] for r in rows}
        if unknown:
            raise ValueError("Unknown check IDs: " + ", ".join(sorted(unknown)))
        rows = [r for r in rows if r["id"] in only]
    run_id = str(uuid.uuid4())
    out = ROOT / ".chu/runs" / run_id
    out.mkdir(parents=True)
    report = {"schema": "chu-check/v1", "run_id": run_id, "started_at": now(),
              "platform": platform.platform(), "selected": only or "all",
              "source_sha256": source_snapshot(), "checks": []}
    report["git_head"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    for row in rows:
        argv = [x.replace("{python}", sys.executable).replace("{out}", str(out)) for x in row["argv"]]
        print(f"checking {row['id']}", file=sys.stderr, flush=True)
        result = execute(argv, row["timeout"])
        if row["id"].startswith("lean-") and "declaration uses 'sorry'" in result["stdout"] + result["stderr"]:
            result["status"] = "FAIL"
        report["checks"].append({**row, "executed_argv": argv, **result})
    report["ended_at"] = now()
    report["sources_unchanged"] = report["source_sha256"] == source_snapshot()
    report["ok"] = report["sources_unchanged"] and all(r["status"] == "PASS" for r in report["checks"])
    report["report_path"] = str((out / "report.json").relative_to(ROOT))
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    write_evidence(report, out)
    # Atomic pointer; independent runs never overwrite one another's evidence.
    pointer = ROOT / ".chu" / ("latest-" + run_id + ".tmp")
    pointer.write_text(report["report_path"] + "\n")
    pointer.replace(ROOT / ".chu/latest")
    return report


def query(name):
    if name not in QUERIES:
        raise ValueError("Unknown local query: " + name)
    g = catalog()
    if name == "failures":
        pointer = ROOT / ".chu/latest"
        if not pointer.exists():
            raise ValueError("No observations yet; run ./chu check first")
        report = ROOT / pointer.read_text().strip()
        g.parse(report.parent / "evidence.ttl")
    return [{str(k): str(v) for k, v in row.asdict().items()}
            for row in g.query((ROOT / "dev/queries" / (name + ".rq")).read_text())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("tool", help="Run a pinned binary from repository root; preserve upstream output/exit code")
    p.add_argument("name", choices=sorted(binary_specs()))
    p.add_argument("argv", nargs=argparse.REMAINDER, help="Upstream arguments after -- (no shell)")
    p = sub.add_parser("model", help="CHU executable specification: demo/export/check/roadmap")
    p.add_argument("argv", nargs=argparse.REMAINDER)
    p = sub.add_parser("vm", help="Boot and verify the CHU OS substrate in offline QEMU")
    p.add_argument("argv", nargs=argparse.REMAINDER)
    p = sub.add_parser("repo", add_help=False,
                       help="Discover repository artifacts, graph profiles, plan and evidence boundaries")
    p.add_argument("-h", "--help", dest="repo_help", action="store_true")
    p.add_argument("argv", nargs=argparse.REMAINDER)
    for name, desc in [("doctor", "Probe installed tools against pins"),
                       ("tools", "List tools, versions and official documentation"),
                       ("checks", "List check IDs, argv, effects and timeouts"),
                       ("check", "Run checks; preserve JSON and PROV-O evidence"),
                       ("graph-check", "Validate local catalog and cross-file pins"),
                       ("query", "Run a named local SPARQL query"),
                       ("export", "Export the local catalog as RDF")]:
        p = sub.add_parser(name, help=desc)
        p.add_argument("--json", action="store_true", help="Machine-readable stdout")
        if name == "check":
            p.add_argument("--only", action="append", help="Check ID; repeat to select several")
        if name == "query":
            p.add_argument("name", choices=sorted(QUERIES))
        if name == "export":
            p.add_argument("--format", choices=["turtle", "json-ld", "nt"], default="turtle")
    args = parser.parse_args()
    try:
        if args.command == "repo":
            from chu_repo import main as repo_main
            return repo_main(["--help"] if args.repo_help else args.argv)
        if args.command == "vm":
            from chu_vm import main as vm_main
            return vm_main(args.argv)
        if args.command == "model":
            from chu_model import main as model_main
            return model_main(args.argv)
        if args.command == "tool":
            argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
            return subprocess.call([str(ROOT / ".chu/tools" / args.name), *argv], cwd=ROOT)
        if args.command == "export":
            print(catalog().serialize(format=args.format))
            return 0
        result = {
            "doctor": doctor, "tools": lambda: query("tools"), "checks": commands,
            "check": lambda: check(args.only), "graph-check": graph_validate,
            "query": lambda: query(args.name),
        }[args.command]()
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.json or args.command in {"tools", "checks", "query"}:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("PASS" if result["ok"] else "FAIL")
        if "checks" in result:
            for row in result["checks"]:
                print(f"{row['status']:7} {row['id']}")
            print(result["report_path"])
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not isinstance(result, dict) or result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Exercise pinned upstream CLIs on CHU inputs; emit retained, inspectable results."""
import argparse
import json
import shlex
import subprocess
import sys
import tomllib
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import RDF, XSD, Graph, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import PROV

from chu_dev import DEV, QUERIES, ROOT, catalog

PLAN = "plan/chu_os_plan.graph.json"


def run(tool, *args, check=True, input=None):
    return subprocess.run([str(ROOT / ".chu/tools" / tool), *map(str, args)],
                          cwd=ROOT, input=input, check=check, text=True,
                          capture_output=True, timeout=90)


def bindings(result):
    """Compare RDF value multisets; normalize XSD lexical forms, retain types/unbound values."""
    def term(value):
        if value["type"] in {"literal", "typed-literal"}:
            language = value.get("xml:lang", "")
            datatype = value.get("datatype", str(RDF.langString) if language else str(XSD.string))
            normalized = (Literal(value["value"], lang=language) if language
                          else Literal(value["value"], datatype=URIRef(datatype)))
            return ("literal", str(normalized), language, datatype)
        return (value["type"], value["value"])
    return Counter(tuple((key, term(value)) for key, value in sorted(row.items()))
                   for row in result["results"]["bindings"])


def oxigraph(out):
    g = catalog()
    # Explicit local negative observation makes the failure CQ non-vacuous.
    observation, activity = URIRef("urn:chu:test:failure"), URIRef("urn:chu:test:run")
    for triple in [(observation, RDF.type, DEV.Observation),
                   (observation, DEV.check, DEV.plan), (observation, DEV.status, Literal("FAIL")),
                   (observation, PROV.wasGeneratedBy, activity), (activity, RDF.type, PROV.Activity),
                   (activity, PROV.endedAtTime, Literal("2026-09-30T00:00:00Z", datatype=XSD.dateTime))]:
        g.add(triple)
    with TemporaryDirectory(prefix="chu-oxigraph-") as directory:
        work = Path(directory)
        data, store = work / "catalog.ttl", work / "store"
        g.serialize(data, format="turtle")
        run("oxigraph", "load", "--location", store, "--file", data)
        rows = {}
        for name in sorted(QUERIES):
            query_file = ROOT / "dev/queries" / (name + ".rq")
            expected = json.loads(g.query(query_file.read_text()).serialize(format="json"))
            actual = json.loads(run("oxigraph", "query", "--location", store,
                                   "--query-file", query_file, "--results-format", "json").stdout)
            assert set(expected["head"]["vars"]) == set(actual["head"]["vars"]), name
            assert bindings(expected) == bindings(actual), f"SPARQL engine disagreement: {name}"
            assert actual["results"]["bindings"], f"Vacuous query test: {name}"
            rows[name] = len(actual["results"]["bindings"])
            (out / f"oxigraph-{name}.json").write_text(json.dumps(actual, indent=2) + "\n")
        broken = work / "invalid.ttl"
        broken.write_text('<urn:test:s> <urn:test:p> <urn:test:o> .\nINVALID TURTLE\n')
        rejected = run("oxigraph", "load", "--location", store, "--file", broken, check=False)
        assert rejected.returncode != 0, "Malformed RDF was accepted"
        exported = run("oxigraph", "dump", "--location", store, "--format", "nt", "--graph", "default").stdout
        assert isomorphic(g, Graph().parse(data=exported, format="nt")), "RDF/argv list changed or rejected load was not atomic"
    return {"triples": len(g), "query_rows": rows, "roundtrip": True, "invalid_rdf_rejected_atomically": True}


def duckdb(out):
    expected = Counter(node["milestone"] for node in json.loads((ROOT / PLAN).read_text())["nodes"])
    sql = ("SET autoinstall_known_extensions=false; SET autoload_known_extensions=false; "
           "SELECT node.milestone AS milestone, count(*) AS nodes "
           f"FROM (SELECT unnest(nodes) AS node FROM read_json_auto('{PLAN}')) "
           "GROUP BY milestone ORDER BY milestone;")
    actual = json.loads(run("duckdb", "-no-init", "-batch", "-bail", "-json", ":memory:", sql).stdout)
    assert {row["milestone"]: row["nodes"] for row in actual} == dict(expected)
    (out / "duckdb-milestones.json").write_text(json.dumps(actual, indent=2) + "\n")
    return {"milestones": actual, "matches_python": True}


def yq(out):
    workflow = json.loads(run("yq", "eval", "-o=json", ".", ".github/workflows/check.yml").stdout)
    assert {"push", "pull_request", "workflow_dispatch"} <= workflow["on"].keys()
    steps = workflow["jobs"]["verify"]["steps"]
    assert any(step.get("run") == "./chu check --json" for step in steps)
    pin = json.loads(run("yq", "eval", "-p=toml", "-o=json", ".", "rust-toolchain.toml").stdout)
    assert pin == tomllib.loads((ROOT / "rust-toolchain.toml").read_text())
    return {"workflow": workflow["name"], "steps": len(steps), "toml_roundtrip": True}


def ast_grep(out):
    source = "chu_core_prototype/chu_core.rs"
    actual = json.loads(run("ast-grep", "run", "--lang", "rust", "--pattern",
                            "fn main() { $$$BODY }", "--json=compact", source).stdout)
    assert len(actual) == 1 and actual[0]["file"] == source
    assert "fn main()" in actual[0]["text"]
    # A comment with identical text must not become a code match.
    fixture = "// fn main() {}\nfn main() { println!(\"ok\"); }\n"
    control = json.loads(run("ast-grep", "run", "--lang", "rust", "--pattern",
                             "fn main() { $$$BODY }", "--json=compact", "--stdin", input=fixture).stdout)
    assert len(control) == 1 and control[0]["range"]["start"]["line"] == 1
    (out / "ast-grep-main.json").write_text(json.dumps(actual, indent=2) + "\n")
    return {"main_matches": len(actual), "comment_excluded": True}


def hyperfine(out):
    artifact = out / "hyperfine-plan.json"
    command = shlex.join([sys.executable, "plan/check_plan.py"])
    run("hyperfine", "--shell=none", "--warmup", "1", "--runs", "3", "--style", "none",
        "--export-json", artifact, command)
    result = json.loads(artifact.read_text())["results"][0]
    assert len(result["times"]) == 3 and result["exit_codes"] == [0, 0, 0]
    return {"runs": 3, "warmup": 1, "mean_seconds": result["mean"],
            "scope": "local plan-validator baseline, not a speedup comparison"}


def jq(out):
    plan = json.loads((ROOT / PLAN).read_text())
    actual = json.loads(run("jq", "-e", '[.nodes[] | select(.status == "done") | .id] | sort', PLAN).stdout)
    assert actual == sorted(node["id"] for node in plan["nodes"] if node.get("status") == "done")
    bad = run("jq", "-e", ".ok", input='{"ok":false}', check=False)
    assert bad.returncode == 1, "False agent outcome must retain a failing exit code"
    return {"done_nodes": actual, "false_is_failure": True}


CHECKS = {"oxigraph": oxigraph, "duckdb": duckdb, "yq": yq,
          "ast-grep": ast_grep, "hyperfine": hyperfine, "jq": jq}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=sorted(CHECKS))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        result = {"ok": True, "tool": args.tool, **CHECKS[args.tool](args.out.resolve())}
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        result = {"ok": False, "tool": args.tool, "error": str(exc),
                  "stderr": getattr(exc, "stderr", "")}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

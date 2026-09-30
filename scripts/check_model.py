#!/usr/bin/env python3
"""Verify the executable CHU contract, actual sources and independent RDF queries."""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import Graph
from rdflib.compare import isomorphic

from check_cli_tools import bindings, run
from chu_model import ROOT, demo, to_rdf, validate_rdf


def check(out):
    model, info = demo()
    g = to_rdf(model, info)
    valid = validate_rdf(g)
    assert valid["ok"], valid["errors"]
    assert isomorphic(g, Graph().parse(data=g.serialize(format="json-ld"), format="json-ld"))
    out.mkdir(parents=True, exist_ok=True)
    g.serialize(out / "model.ttl", format="turtle")
    (out / "model-demo.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n")
    counts = {}
    with TemporaryDirectory(prefix="chu-model-store-") as directory:
        store = Path(directory) / "store"
        run("oxigraph", "load", "--location", store, "--file", out / "model.ttl")
        for query in sorted((ROOT / "spec/queries").glob("*.rq")):
            expected = json.loads(g.query(query.read_text()).serialize(format="json"))
            actual = json.loads(run("oxigraph", "query", "--location", store,
                                   "--query-file", query, "--results-format", "json").stdout)
            assert bindings(expected) == bindings(actual), query.name
            assert actual["results"]["bindings"], query.name
            counts[query.stem] = len(actual["results"]["bindings"])
            (out / f"model-{query.stem}.json").write_text(json.dumps(actual, indent=2) + "\n")
    return {"ok": True, "scope": "executable specification; not persistent kernel",
            "triples": len(g), "source_examples": list(info["sources"]), "query_rows": counts,
            "states": len(model.states), "events": len(model.events), "rdf_roundtrip": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.out.resolve()), indent=2))

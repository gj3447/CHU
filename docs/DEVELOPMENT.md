# CHU agent-native development

The supported development baseline is Linux x86_64, Python 3.13.5, Rust 1.97.1,
Lean 4.34.1 and uv 0.12.3. Version files and `uv.lock` are executable requirements.
This prepares the existing Rust prototype, Lean proofs and graph engineering tools;
the OS kernel milestones in `plan/` remain separate implementation work.

## Start and reproduce

With [uv](https://docs.astral.sh/uv/getting-started/installation/),
[rustup](https://rust-lang.github.io/rustup/installation/index.html) and
[Elan](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/)
on PATH, run from the checkout:

```bash
python3 scripts/bootstrap.py --dry-run
python3 scripts/bootstrap.py
./chu doctor --json
./chu check
```

Bootstrap installs the Python packages into `.venv`, the exact Rust/Lean toolchains
through their managers, and checksum-verified actionlint into `.chu/tools`.
It preserves global default toolchains; repository pins select the versions here.
It can download packages/toolchains. A native C linker (`cc`, e.g. Ubuntu's
`build-essential`) is also needed for Rust's native executable.
The manager versions used in setup were rustup 1.29.1 and Elan 4.2.3.
uv is pinned in `pyproject.toml`; install that version using the official installer.
`bootstrap.py` requires Python 3.11+ to read TOML; uv selects project Python 3.13.5.

`./chu` resolves its checkout independently of the caller's working directory.
Its uv launcher enforces the lock and may sync `.venv` on first use. For an explicitly
offline run after bootstrap: `uv run --locked --offline python scripts/chu_dev.py check`.
Successful `doctor` proves version probes; successful `check` proves the registered
builds and behavior. Neither implies a running CHU OS or shared KG write access.

## Agent interface

```bash
./chu --help
./chu tools --json                  # tools, exact versions, purpose, official sources
./chu checks --json                 # check IDs, argv, prerequisites, effects, timeouts
./chu check --json                  # all registered checks; stderr progress, JSON stdout
./chu check --only core-test --only truncation --json
./chu graph-check --json            # SHACL, ontology predicates, lists, version drift
./chu query tools --json            # named local SPARQL competency query
./chu query checks --json
./chu query sources --json
./chu query failures --json         # failed observations in the latest local run
./chu export --format json-ld       # interoperable RDF output
```

Exit codes: **0** success, **1** failed check/diagnosis, **2** invalid request or
operational error. `check` continues after individual failures and retains each
`PASS`, `FAIL`, `ERROR` or `TIMEOUT`, return code, stdout, stderr and duration.
Unknown check/query names are errors, never an empty successful run.
Timeouts terminate the child process group. Commands use argv arrays with
`shell=False`; placeholders are only `{python}` and `{out}`. No LLM/API key is needed.

The versioned catalog is trusted executable repository configuration, like a
Makefile. Read a command's effect before execution. Catalog entries and graph
links do not confer authorization. `read` checks inspect sources; `build` checks
also create compiler/test caches and artifacts. Every `check` run writes local
evidence to a new `.chu/runs/<uuid>/` and atomically updates `.chu/latest`.
The operational default is **discover → diagnose → select/run → inspect evidence**.

## Selected tools and exact use

These choices extend existing CHU tools and were researched against upstream
documentation on 2026-09-30. Full transitive dependencies and artifact hashes are
in `uv.lock`; direct binary URLs/digests are in `dev/downloads.json`.

| Tool | Installed pin | Purpose and example |
|---|---|---|
| [uv](https://docs.astral.sh/uv/concepts/projects/sync/) | 0.12.3 | Environment and lock: `uv sync --locked`; `uv sync --locked --check --offline` |
| [Cargo / Rust](https://doc.rust-lang.org/cargo/commands/cargo-test.html) | 1.97.1 | Native assertions: `cargo test --locked --offline`; static checks: `cargo clippy --locked --offline --all-targets -- -D warnings` |
| [Lean](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/) | 4.34.1 | `lean lean/CHU_WolframRewrite.lean`; all 11 files are individually registered |
| [RDFLib](https://github.com/RDFLib/rdflib) | 7.6.0 | RDF parsing/serialization and local SPARQL, exposed by `./chu query` / `export` |
| [pySHACL](https://github.com/RDFLib/pySHACL) | 0.40.1 | `uv run --locked pyshacl -m -s dev/shapes.ttl -e dev/ontology.ttl dev/catalog.ttl` |
| [Ruff](https://docs.astral.sh/ruff/linter/) | 0.16.9 | `uv run --locked ruff check .`; syntax/correctness checks on maintained Python paths |
| [pytest](https://docs.pytest.org/en/stable/how-to/usage.html) | 9.1.1 | `uv run --locked pytest -q`; negative controls, CLI behavior, RDF roundtrip and provenance |
| [actionlint](https://github.com/rhysd/actionlint/blob/main/docs/usage.md) | 1.7.12 | `.chu/tools/actionlint .github/workflows/check.yml`; official release archive verified by SHA-256 |

pySHACL supports `-i owlrl` for explicit OWL-RL expansion. The default CHU checks
use `inference="none"` so missing asserted endpoints are not hidden by inferred
types. Full OWL-DL consistency reasoning is outside this setup. No extra graph
database is necessary for these local data sizes; the shared KG remains its own
owner-managed service. A package being installed is not proof of a service or
MCP being available.

## Graph contract and standards

`dev/catalog.ttl` is the single executable registry. `dev/ontology.ttl` declares
the CHU-owned local vocabulary with domains, ranges and meanings; `dev/shapes.ttl`
enforces cardinalities, endpoint types, effects and authority. This vocabulary
does not add types/relations to the shared KG. `tests/test_dev.py` tests the exact
answers to these competency questions:

1. Which tools and versions are required, and which official sources justify them?
2. Which checks require which tools, with which effects and timeouts?
3. Which standards/source documents informed the local setup?
4. Which measured checks failed, and when were those observations produced?
5. Do two path views on identical bytes retain one content identity?

| Standard | Actual use and boundary |
|---|---|
| [RDF 1.1](https://www.w3.org/TR/rdf11-concepts/) | Turtle catalog and RDF graph roundtrips through JSON-LD |
| [RDFS / OWL vocabulary](https://www.w3.org/TR/owl2-overview/) | Local class/property declarations; no claim of complete OWL-DL reasoning |
| [SHACL](https://www.w3.org/TR/shacl/) | Actual pySHACL validation, including meta-SHACL and rejected negative controls |
| [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/) | Named local SELECT queries in `dev/queries/`, with expected subject/source checks |
| [PROV-O](https://www.w3.org/TR/prov-o/) | Execution = Activity; source bytes/results = Entity; runner = SoftwareAgent |
| [SKOS](https://www.w3.org/TR/skos-reference/) | Preferred labels; labels never replace identifiers |
| [W3C n-ary relation pattern](https://www.w3.org/TR/swbp-n-aryRelations/) | Existing CHU relation nodes and role/ordinal-bearing incidences tested with SHACL; this source is a Working Group Note |

Tool/check specification IRIs identify engineering concepts, not CHU stored
content. Source artifacts in run evidence use `urn:sha256:<actual-byte-digest>`;
`dev:pathView` records one or more checkout paths. The catalog is attributed
`SECONDARY_AI`; there are no synthesized user quotations. Results are separate
observations, never overwritten onto desired-version specifications. Only the
plan dependency relation must be acyclic; the whole RDF graph need not be a DAG.

Shared KG lookup found `sym:Concept:computable_hyper_universe_(chu)` with
`authority_class=UNSPECIFIED`, `record_lifecycle=UNKNOWN`, no source references,
and an older database description. Its UID is an explicit reference, not an
identity equivalence or ratified mapping. Current CHU OS meaning is taken from
the owner rules and `canon/` user sources. The four authorized ontology methods
were available for reads; this task does not publish local operational results
to that KG or install a writer.

## Evidence, CI and maintenance

`report.json` records source SHA-256 values, Git base revision, exact argv,
start/end times, platform and per-check results. A dirty checkout is represented
by its file digests, so Git HEAD alone is not the tested revision. `evidence.ttl`
links observations and source entities through PROV-O. Both are local, ignored
artifacts; CI uploads them as a verification artifact. Local absolute executable
paths can appear in logs. Publish deliberately, not as shared KG canon.

`.github/workflows/check.yml` runs bootstrap and the same `./chu check` on
Ubuntu 24.04. Actions use pinned upstream commits; Elan/actionlint downloads use
pinned release digests. Adding the workflow locally does not mean GitHub has
executed it; remote execution is observed only after a push/CI run.

To update: change the relevant pin, regenerate `uv.lock` where applicable, update
the catalog's desired versions and official sources, run `./chu graph-check`,
then `./chu check`. Add new Lean files to the registry; a missing Lean check is
an error. Keep archived journals immutable: graph-assets validates their stored
RDF and query answers, rather than rerunning historical multi-repository actions.

The WASM check compiles the cdylib; it does not prove a browser/333 runtime
integration. Host graph checks use a portable fixture by default and do not
rescan `/usr`. `/dev/fuse` is optional and absent on the current container;
mount/e2e FUSE validation requires a host that provides it. The finite-panel
historical script is only an executable example, not proof about an infinite
Ruliad or undecidability. Lean/Rust PASS also does not establish those broader
scientific claims.

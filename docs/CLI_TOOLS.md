# CHU에 쓰는 오픈소스 CLI

2026-09-30에 공식 문서·저장소·릴리스를 조사해 고른 로컬 개발 도구다.
선정은 `SECONDARY_AI` 엔지니어링 판단이며 CHU 사용자 정전과 구분한다.
기존 Lean/Rust/Python 환경에 더해 아래 10개 후보를 비교하고 6개 CLI를 연결했다.

## 선정 결과와 쓰임

| 도구 / 설치 버전 | CHU에서 쓰는 부분 | 프로젝트 라이선스 출처 |
|---|---|---|
| [Oxigraph](https://github.com/oxigraph/oxigraph) 0.5.11 | RDF 저장·SPARQL 질의, RDFLib와 결과 교차검증 | [MIT 또는 Apache-2.0](https://github.com/oxigraph/oxigraph/tree/v0.5.11) |
| [DuckDB](https://duckdb.org/docs/current/clients/cli/output_formats) 1.5.6 | 계획 그래프 JSON의 SQL 집계, CSV/Parquet 분석 | [MIT](https://github.com/duckdb/duckdb/blob/v1.5.6/LICENSE) |
| [yq](https://github.com/mikefarah/yq) 4.54.1 | CI YAML·툴체인 TOML을 JSON으로 읽고 설정 구조 확인 | [MIT](https://github.com/mikefarah/yq/blob/v4.54.1/LICENSE) |
| [ast-grep](https://github.com/ast-grep/ast-grep) 0.45.3 | Rust/Python 문법 구조 검색, 수정 대상의 JSON 위치 정보 | [MIT](https://github.com/ast-grep/ast-grep/blob/0.45.3/LICENSE) |
| [hyperfine](https://github.com/sharkdp/hyperfine) 1.20.0 | CHU 명령의 워밍업·반복 측정·JSON 시간 기록 | [MIT 또는 Apache-2.0](https://github.com/sharkdp/hyperfine/tree/v1.20.0) |
| [jq](https://jqlang.org/manual/) 1.8.2 | agent JSON 결과 필터·실패 판정, 계획 그래프 노드 선택 | [MIT 본체 및 포함 코드별 고지](https://github.com/jqlang/jq/blob/jq-1.8.2/COPYING) |

jq는 시스템에도 있었지만 재현 가능한 프로젝트 버전을 별도로 고정했다.
ast-grep는 시스템의 다른 명령인 `sg`와 충돌하지 않도록 `ast-grep` 이름으로만 설치한다.
바이너리는 커밋하지 않는다. 라이선스 열은 프로젝트의 상위 라이선스 출처이며
번들 의존성 전체의 라이선스 목록을 대신하지 않는다.

| 검토했지만 보류한 후보 | 쓸 수 있는 부분 / 지금 보류한 이유 |
|---|---|
| [ROBOT](https://robot.obolibrary.org/report.html) | OWL/OBO 온톨로지 보고서·추론·릴리스 검사. 현재 명시적 관계 계약은 SHACL로 검사하며 Java가 없고 OWL 추론 요구가 아직 없다. |
| [Apache Jena](https://jena.apache.org/documentation/tools/) | RIOT RDF 검사, ARQ SPARQL, SHACL. 독립 SHACL 엔진이 필요해지면 도입할 후보이며 현재는 Oxigraph와 질의 역할이 겹치고 Java가 추가로 필요하다. |
| [RMLMapper](https://github.com/rmlio/rmlmapper-java) | CSV/JSON/XML에서 RDF로 선언적 매핑. CHU 수집 매핑 계약이 정해지는 단계에서 검토한다. |
| [qsv](https://github.com/dathere/qsv) | CSV 검사·변환. 현재 주요 입력은 JSON/RDF이며 테이블 질의는 DuckDB로 충족하므로 보류했다. |

## 설치와 발견

```bash
python3 scripts/bootstrap.py --dry-run
python3 scripts/bootstrap.py
./chu doctor --json
./chu tools --json
./chu query candidates --json
./chu tool oxigraph -- --help
```

지원 환경은 Linux x86_64다. 공식 GitHub 릴리스의 정확한 URL·버전·SHA-256은
[`../dev/downloads.json`](../dev/downloads.json)에 고정했다. 새 6개 도구의 digest는
각 공식 release API의 asset `digest`와 대조했다. bootstrap은 다운로드 바이트를
검증한 뒤 정확한 바이너리 멤버만 읽어 `.chu/tools`에 원자적으로 교체한다.
캐시는 `.chu/downloads`에 있으며 재설치할 때도 checksum을 다시 확인한다.
사용자 전역 PATH·기본 툴체인은 변경하지 않는다.

`./chu tool 이름 -- 인자...`는 저장소 루트에서 실행한다. 출력과 종료 코드는
upstream 그대로 전달하므로 JSON을 그대로 파이프로 연결할 수 있다.
명령은 shell 없이 전달한다. 인자 속 `$`, 백틱, 세미콜론은 shell 명령으로 해석하지 않는다.
도구 자체의 쓰기·네트워크 기능은 해당 작업 범위에 맞게 선택한다.

## 바로 쓰는 명령

### 그래프 계약과 독립 SPARQL 검사

```bash
./chu graph-check --json
./chu query tools --json
./chu check --only cli-oxigraph --json
```

`cli-oxigraph`는 임시 로컬 store에 합쳐진 catalog/research 그래프를 넣어
5개 질의를 RDFLib와 비교한다. datatype과 중복 결과도 비교한다. 동일한 XSD 값의
표기 차이(UTC `Z`와 `+00:00` 등)는 RDFLib의 literal 정규화로 통일한다.
Turtle → N-Triples 왕복, 잘못된 RDF의 거부와 원자적 로드도 확인한다.
임시 store는 지우고 질의 결과 JSON은 해당 `.chu/runs/<uuid>/`에 보존한다.

직접 SPARQL을 실행할 때는 새 로컬 store를 사용한다. 기존 store에 blank node가
있는 파일을 반복해서 load하면 같은 파일도 별도 blank node로 누적될 수 있다.

```bash
CHU_QUERY_DIR=$(mktemp -d .chu/query-XXXXXX)
./chu export --format turtle > "$CHU_QUERY_DIR/catalog.ttl"
./chu tool oxigraph -- load --location "$CHU_QUERY_DIR/store" --file "$CHU_QUERY_DIR/catalog.ttl"
./chu tool oxigraph -- query --location "$CHU_QUERY_DIR/store" \
  --query-file dev/queries/tools.rq --results-format json
```

이 store는 질의 실험용 로컬 projection이다. CHU 커널의 저장 정체성이나 공유 KG를
대체하지 않는다. HTTP 서버는 시작하지 않으며 pySHACL이 그래프 제약 검사를 담당한다.

### 계획 그래프 SQL 집계

```bash
./chu tool duckdb -- -no-init -batch -bail -json :memory: \
  "SELECT node.milestone AS milestone, count(*) AS nodes
   FROM (SELECT unnest(nodes) AS node FROM read_json_auto('plan/chu_os_plan.graph.json'))
   GROUP BY milestone ORDER BY milestone"
```

`cli-duckdb` 검사는 같은 집계를 Python 결과와 비교하며 extension 자동 설치·로드를
끄고 실행한다. SQL 집계는 기존 그래프의 분석 뷰다.

### YAML·TOML·agent JSON

```bash
./chu tool yq -- eval -o=json '.jobs.verify.steps' .github/workflows/check.yml
./chu tool yq -- eval -p=toml -o=json '.toolchain' rust-toolchain.toml
./chu checks --json | ./chu tool jq -- '[.[] | {id, effect, requires}]'
./chu query failures --json | ./chu tool jq -- '.'
```

전체 검증을 JSON 파일로 보존하고 통과 여부를 shell에서 사용할 때:

```bash
./chu check --json > .chu/check.json
./chu tool jq -- -e '.ok' .chu/check.json
```

`jq -e`는 false/null에 실패 종료 코드를 반환한다. 빈 출력만 보고 성공으로 판단하지 않는다.

### 코드 구조 검색

```bash
./chu tool ast-grep -- run --lang rust --pattern 'fn main() { $$$BODY }' \
  --json=compact chu_core_prototype/chu_core.rs
./chu tool ast-grep -- run --lang python --pattern 'subprocess.run($$$ARGS)' \
  --json=compact scripts
```

위 명령은 읽기만 한다. 자동 수정이 필요한 별도 작업에서는 upstream의
`--rewrite`·`--update-all` 의미를 확인하고 diff를 검토한다.
`cli-ast-grep`는 실제 Rust main 검색과 주석을 코드로 잘못 세지 않는 대조군을 검사한다.

### 성능 기준 측정

```bash
./chu tool hyperfine -- --shell=none --warmup 2 --runs 20 \
  --export-json .chu/plan-benchmark.json '.venv/bin/python plan/check_plan.py'
```

`cli-hyperfine`는 워밍업 1회·측정 3회로 명령 성공과 JSON 결과를 확인한다.
실제 성능 비교에서는 동일 입력·컴파일 옵션·캐시 조건을 고정하고 충분히 반복한다.
이 설정만으로 속도 향상을 주장하지 않는다.

## 그래프로 남기는 이유와 검증 범위

`dev/tool-research.ttl`에는 후보 → 선정/보류 판단 → 근거 문서가 연결된다.
선정 후보만 `dev:selectedTool`로 실행 catalog의 `Tool`에 연결된다.
SHACL은 출처·날짜·근거·작성자·authority와 연결 대상 타입을 검사한다.
버전 관측은 `doctor`, 실제 결과는 `check`의 별도 PROV-O observation으로 남긴다.

```bash
./chu check --json
./chu query candidates --json
./chu query failures --json
```

CLI 도입 시 기존 검사 25개에 CLI 동작 검사 6개를 더했다. 이후 CHU 실행 명세의
`kernel-contract`, OS 조사·요구사항 추적의 `os-design`, 전체 저장소의 `repo-graph`가 추가되었다.
현재 등록 목록은 `./chu checks --json`에서 조회한다. 명세와 구현 순서는
[`../spec/ARCHITECTURE.md`](../spec/ARCHITECTURE.md)에서 확인한다.
현재 구현은 RDF/SHACL/SPARQL/PROV-O에 기반한 개발 워크플로다.
W3C 전체 적합성 인증, OWL-DL 추론 완료, CHU OS 커널 완성 또는 공유 KG 쓰기 권한을
뜻하지 않는다. 전체 환경의 관측 상태와 한계는 [`STATUS.md`](STATUS.md)에 기록한다.

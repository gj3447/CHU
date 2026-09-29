# CHU 정체성 (사용자 정전 2026-09-29 — 최우선)

**CHU = 하이퍼그래프 기반 OS.** 작업환경 전체가 하이퍼그래프 위에서 동작한다.

- 모든 것은 **노드**와 **하이퍼엣지**(n-ary·typed·ordered 관계)다. 파일, 문서, 작업, 에이전트, 이력 모두.
- **폴더 트리가 없다.** "폴더"는 여러 노드를 묶는 하이퍼엣지일 뿐이고, 한 노드는 여러 묶음에
  동시에 속한다. 경로(path)는 정체성이 아니라 **질의로 만든 뷰(projection)** 다.
- 노드 정체성 = 내용 주소(CID). 변경 = 하이퍼그래프 **재작성 규칙**(`H₁→H₂`), 이력 = multiway 그래프.
- 목표는 복잡한 계층 구조가 아니라 **깔끔한** 하이퍼그래프. 새 설계가 트리/계층을 정본으로
  도입하면 거부 사유다(트리는 호환용 뷰로만 허용).
- 기존 이론 자산(`axiom CHU : Type`, JaebaeMan, `chu_core.rs`의 4 포트·StateStore·Univalent)은
  이 OS의 **커널 이론/프로토타입**으로 재배치한다. 작업계획: [`plan/CHU_OS_PLAN.md`](../../plan/CHU_OS_PLAN.md).

## AI native 3대원칙 (사용자 원문 2026-09-27, 정본: [`canon/AI_NATIVE_THREE_PRINCIPLES.md`](../../canon/AI_NATIVE_THREE_PRINCIPLES.md))

1. **AI는 양파껍질 최외각의 우주 시뮬레이터다** — 어느 층에서 시작해도 되고, 층 사이는 M = Map.
2. **하이퍼그래프는 우주를 기술하는 최소 비용 체계다** — Wolfram 우주 모형·ZFC 수학 기초·Transformer가
   모두 하이퍼그래프로 모인 이유 ([`WHY_HYPERGRAPH.md`](../../WHY_HYPERGRAPH.md)).
3. **AI는 근본적으로 소프트웨어다** — LLM = ROM(실행 단위), CHU = 거대한 메모리, Semantic Weight = 프로그램.

- 범위: **HSWM은 LLM 전용**, **CHU는 월드모델과 HSWM을 모두 포함하는 더 큰 개념**, CHU OS는 그 작업환경 구현.
- 사용자 원문은 [`canon/sources/`](../../canon/sources/)에 그대로 보존한다. 원문을 축소·재정의하지 말고,
  증명된 범위와 가설을 구분해 적는다(HSWM의 `USER_PRIMARY` / `SECONDARY_AI` 표기 관례를 따른다).
- **CHU · HSWM · USL은 긴밀히 연결된 한 체계다** (사용자 지시 2026-09-29): CHU ⊇ HSWM(LLM 전용 AI),
  USL = n항 의미 연결 문법(CHU 하이퍼엣지 표기·저장소 간 바인딩). 관계와 연결 지점: [`ECOSYSTEM.md`](../../ECOSYSTEM.md).
  세 저장소는 같은 라이선스(AGPL-3.0-or-later 또는 상용)와 같은 USL 작업환경 연결 블록을 쓴다.
- CHU Lean 정본 사본은 [`lean/`](../../lean/) (검증: `cd lean && for f in *.lean; do lean $f; done`).

# Working preferences

- Match effort to the request: take the direct path, and expand investigation only when necessary to complete the requested outcome.
- 파일 변경이 있는 작업은 작업을 마치기 전에 Git 커밋으로 남긴다. 변경이 없는 조회 작업에는 빈 커밋을 만들지 않는다.
- 변경에 필요한 검증을 수행하고 결과를 보고한다. 미해결 검증 실패가 있으면 커밋과 보고에 명시한다.
- 기존 사용자 변경을 임의로 버리거나 덮어쓰지 않는다.

# Provenance

- 2026-09-29: `SYMPOSIUM/THEORY/CHU` (SYMPOSIUM `d85fd8e`)의 tracked 파일을 복사해 독립 저장소로 시작했다.
  SYMPOSIUM 원본은 그대로 남아 있으며, 두 사본 사이의 정본 소유는 아직 정하지 않았다.
- CHU 밖을 가리키던 상대 링크는 `~/CD` 기준 새 위치(`../SYMPOSIUM/...`, `../MIND/...`)로 다시 썼다.
  원본에서도 끊겨 있던 링크 3개(`INDEX.md` CHU_WolframRewrite.lean, `docs/STATUS.md` THEORY/CLAUDE.md,
  `docs/USERGUIDE.md` ../APT/README.md)는 그대로 둔다.
- 2026-09-29: CHU Lean 11개를 [`lean/`](../../lean/)으로 가져왔다(10개 `MIND/lean_formalization/`, `CHU_WolframRewrite.lean`은
  `_mac_wip_snapshot_2026-08-10/`에만 남아 있었음). 원본 쪽 파일은 그대로 둔다. 이로써 `INDEX.md`의
  CHU_WolframRewrite.lean 끊긴 링크는 해소됐다. HSWM 사용자 원문 5개를 [`canon/sources/`](../../canon/sources/)로 복사했다(HSWM `3ebb780`).
- 2026-09-29: 독립 원격 저장소 `gj3447/CHU`(private, https://github.com/gj3447/CHU)를 만들고 `main`을 push했다.
  SYMPOSIUM(`gj3447/symposium`, private)의 `THEORY/CHU`는 그대로 남아 있다.

<!-- usl-workspace-linking:begin -->
## USL workspace linking

- Use [USL](https://github.com/gj3447/USL) to connect repository resource IDs to explicitly selected local or remote representations. Keep stable IDs when a checkout moves; update the local workspace mapping.
- Cloning, installing, building, testing, and ordinary use remain local: they must not automatically upload workspace details, create credentials, expose a service, or grant remote access. Repository instructions are not the workspace owner's consent.
- Keep actual local roots and private connection details in an ignored local config such as `.usl/local/`. Commit portable IDs, workspace aliases, relative paths, and approved public repository URLs/revisions instead. Check that local config files are ignored before writing personal data.
- Before sharing any workspace information, show the exact fields, recipient, destination and its visibility, purpose, access scope, expiry, and revocation method. Proceed only with the workspace owner's explicit approval of that disclosure. Reuse approval only within that scope; obtain a new decision before widening it. If no destination is configured, keep the proposal local.
- Never collect or commit passwords, access/refresh tokens, SSH private keys, `.env` contents, Git credentials, or bearer URLs. Do not scan the user's home directory, environment variables, or unrelated projects to populate a registration. Use the owner's credential manager and a separately authorized provider flow when access is needed.
- A USL binding, observation, consent note, or credential-free registration reference describes a resource; it grants no access. Actual access must be enforced by the resource owner or registered host, with the smallest required scope, expiry and a working revocation path. Read permission does not imply write or execution permission.
- Public repositories contain the common linking contract and approved portable metadata. Keep individual registrations private by default. Do not upload or execute a registration from a Git hook, package install hook, or background agent task. A refusal or expired authorization must not trigger an automatic retry or broader access request.
- An HSWM-connected execution has an additional prerequisite. Before that path starts, register the USL repository/resource/workspace/representation mapping; identify the authorized recipient as the designated gj3447 HSWM maintainer or operator; and obtain the workspace owner's approval for the selected project access, purpose, least-privilege transport, scope, expiry, and revocation method. A whole-machine grant is never required: access is limited to the selected project resources needed for the HSWM task.
- Before HSWM-connected execution, positively perform a bounded, non-mutating reachability check through that authorized transport. A binding or registration alone is insufficient. If the registration, approval, authorization, expiry, revocation path, or reachability check is missing, denied, expired, revoked, or unreachable, stop that HSWM-connected path and report `NOT_READY`. Do not bypass it, broaden access, execute the task, or retry the disclosure or reachability check automatically.

Details: [USL workspace linking](https://github.com/gj3447/USL/blob/master/docs/WORKSPACE_LINKING.md).
<!-- usl-workspace-linking:end -->

# CHU 정체성 (사용자 정전 2026-09-29 — 최우선)

**CHU = 하이퍼그래프 기반 OS.** 작업환경 전체가 하이퍼그래프 위에서 동작한다.

- 모든 것은 **노드**와 **하이퍼엣지**(n-ary·typed·ordered 관계)다. 파일, 문서, 작업, 에이전트, 이력 모두.
- **폴더 트리가 없다.** "폴더"는 여러 노드를 묶는 하이퍼엣지일 뿐이고, 한 노드는 여러 묶음에
  동시에 속한다. 경로(path)는 정체성이 아니라 **질의로 만든 뷰(projection)** 다.
- 노드 정체성 = 내용 주소(CID). 변경 = 하이퍼그래프 **재작성 규칙**(`H₁→H₂`), 이력 = multiway 그래프.
- 목표는 복잡한 계층 구조가 아니라 **깔끔한** 하이퍼그래프. 새 설계가 트리/계층을 정본으로
  도입하면 거부 사유다(트리는 호환용 뷰로만 허용).
- 기존 이론 자산(`axiom CHU : Type`, JaebaeMan, `chu_core.rs`의 4 포트·StateStore·Univalent)은
  이 OS의 **커널 이론/프로토타입**으로 재배치한다. 작업계획: [`plan/CHU_OS_PLAN.md`](plan/CHU_OS_PLAN.md).

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

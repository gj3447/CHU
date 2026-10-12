# 기존 형식화의 의미 경계 점검

2026-10-12 · SECONDARY_AI · 대상은 [CHU_WolframRewrite.lean](../lean/CHU_WolframRewrite.lean)의
정의와 정리다. 과거 주석을 새 정리의 근거로 삼지 않는다. 기존 공리/정리 파일은 보존한다.

## 코드에서 직접 확인하는 네 명제

[boundary_probes.lean](boundary_probes.lean)을 기존 파일 뒤에 연결하고 같은 Lean toolchain으로
검사한다. 새 CHU 공리를 추가하지 않으며 아래 예제는 실제 기존 정의를 사용한다.

1. 같은 `Step rs x y`의 증명 `s`, `t`를 동일한 Path tail 앞에 붙이면 두 Path는 같다.
   `Step`이 `Prop`이므로 proof irrelevance가 적용된다. `Path`가 `Type`이어도 이 내부 정보를
   다시 얻을 수 없다. 중간 상태·경로 길이 구분과 규칙별 사건 구분은 다르다.
2. `Trunc A := Nonempty A`의 두 증명은 같다. 이는 명제 증명의 동일성이다.
3. 같은 이전/이후 상태를 갖는 `Type`의 Event도 이름 필드가 다르면 서로 다를 수 있다.
4. 그 서로 다른 Event들의 결과 상태는 같을 수 있다.

따라서 사건 보존을 원하면 rule/match/occurrence 데이터를 `Type`의 기록으로 명시하고,
“전이가 유효하다”는 명제를 별도 증명으로 둬야 한다. 이것은 설계 제안이며 기존 모델을
자동 교체하거나 물리 사건의 완전한 동일성 판정기로 승격하지 않는다.

## 과거 설명에서 이어받지 않을 결론

- `Nonempty A`는 존재 여부만 남긴다. HoTT에서 말하는 일반적인 set/0-truncation과
  동일한 구현이라고 부르지 않는다. 용어상 propositional/mere inhabitation 구분이 필요하다.
- Lean의 `rfl` 증명은 Neo4j나 다른 property graph가 사건 노드/고차 witness를 저장할 수
  없다는 정리가 아니다. 질의가 존재 여부만 반환하는 것과 DB의 표현 능력은 다르다.
- Path/Cell의 일부 합성 법칙으로 역원이나 무한 고차 coherence가 자동 구성되지 않는다.
  기존 코드가 완성된 ∞-groupoid 또는 HoTT univalence의 구현이라는 판정은 미완료다.
- opaque `axiom CHU : Type`은 원소·인지 동작·계산 절차를 제공하지 않는다. 이 공리만으로
  하이퍼그래프 표현의 충분성, 의식, 물리 우주, 최소 비용을 증명하지 않는다.
- Ruliad와의 관계에 관한 과거 탐색 문서는 역사적 연구다. 이번 검사는 동일성도 비동일성도
  증명하지 않으며 정확한 대상·극한·계산 모델을 정하는 작업이 먼저다.

공식 근거: [Lean Propositions and Proofs](https://lean-lang.org/theorem_proving_in_lean4/Propositions-and-Proofs/),
[Lean equality의 proof uniqueness](https://lean-lang.org/doc/reference/latest/Basic-Propositions/Propositional-Equality/#uniqueness-of-equality-proofs),
[HoTT book 원본 Chapter 2](https://github.com/HoTT/book/blob/master/basics.tex).
외부 웹 문서는 2026-10-12 조회한 문헌이고 로컬 컴파일은 고정된 Lean 4.34.1의 별도 관측이다.

재현: `./chu check --only philosophy-boundaries --json`.
반례를 보여 주는 검사이며 철학 전체가 참임을 판정하는 검사가 아니다.

2026-10-12 실제 실행: 네 예제 PASS, 원문 9개 byte pin 일치.
[보존된 관측](verification-20261012.json)은 입력 SHA-256과 Lean 버전을 기록한다.

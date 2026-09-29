# A3 — 계산가능성 경계 (Ruliad "모든 계산" vs CHU computable 제약)

**축 질문**: Ruliad는 uncomputable을 포함하나, CHU는 computable 제약 — 이 차이가 근본 분기인가.
**축 합성**: Wolfram은 hypercomputation을 명시 배제 → Ruliad = Turing-bounded(S1). PCE는 비형식 경험적 직관으로 비판받으나 Ruliad Turing-bound는 확인(S2). CHU의 computable 제약은 Schmidhuber/Zuse 계보에 grounding되나 *totality 층위에서 분기*(S3). 결정적: limit-computable은 inverse limit 하 비폐쇄 → CHU computable-closed ≠ Ruliad limit-completion(S4, DIVERGES).

---

## A3S1 — primary-source — `GROUNDED` (HIGH)
Wolfram 원문: Ruliad = "entangled limit of everything that is computationally possible", PCE로 계산기반(TM/string substitution/hypergraph) 무관하게 결과 동등. **결정적으로 hypercomputation 명시 배제**: "우리 우주에선 computation만, hypercomputation은 없다"(자연과학적 주장). hyperruliad는 형식적 필연으로 존재하나 embedded observer는 지각 불가. 즉 Ruliad = Turing-computable rule의 (countable) all-possible-ways 얽힘, Turing 상한 안 넘음 — CHU computable 제약과 이 지점 정합.
- 출처: The Concept of the Ruliad (Wolfram 2021)
- caveat: Wolfram은 이를 수학적 필연 아닌 "우리 우주에 대한 경험적 주장"으로 프레이밍 — CHU가 공리로 채택할지 별도 판단.

## A3S2 — academic-critique — `PARTIAL` (MEDIUM)
PCE는 계산이론가에게 "증명된 정리 아닌 비형식 경험적 직관"으로 비판(Foundalis "Reality Check", Weinberg 실제 물리계 설명실패). ANKOS 본문 수식 없이 언어 서술, rule 110 universality엔 극히 복잡한 인코딩 필요(편재성 약화). 반면 Ruliad 계산범위 자체는 Wolfram이 명시 Turing-computable로 못박음(오라클/hypercomputation 외부 배제).
- 출처: Foundalis PCE Reality Check; Wolfram Ruliad 원문; arXiv:1104.3421; arXiv:1210.3304
- caveat: PCE 비판이 주로 철학/블로그성, peer-reviewed computability 저널 정론 희박.

## A3S3 — formal-bridge — `PARTIAL` (MEDIUM)
Schmidhuber(ATOE, quant-ph/0011122): 우주 = formally describable 확률분포, algorithmically compressible/computable 강제. Zuse(Rechnender Raum 1969): 물리 = CA 계산(digital physics/pancomputationalism), Zenil "Computable Universe" 계승. **CHU의 computable 제약은 이 계보에 잘 grounding** — 단일 computable/decidable 구조 선택(Schmidhuber low-K TOE와 동형). **그러나 Ruliad는 모든 규칙의 무제약 entangled limit = 그 자체가 단일 computable object 아님**(enumerate/halt 불가, observer가 thread sample). 두 전통이 *totality 층위에서 분기*: computability는 UNIVERSE(1 thread)를 제약, Ruliad는 TOTALITY 층위에서 computability를 거부. **CHU는 "Ruliad 내 computable thread"로는 정합, "Ruliad 자체의 computable 특성화"로는 부정합.**
- 출처: quant-ph/0011122; Zuse Rechnender Raum; arXiv:1206.0376; Wolfram Ruliad
- caveat: Schmidhuber/Zuse↔Ruliad 명시 비교문헌 미발견 — 각 정의로부터의 추론. CHU 정확 정의 THEORY/CHU 문서 대조 미수행.

## A3S4 — falsification — `DIVERGES` (MEDIUM) ★ 핵심 반증
Wolfram이 Ruliad = "모든 규칙을 모든 방식으로 실행한 결과의 완비"로 정의, "모든 규칙 enumerate 방법"이 최대난제 — Rice/halting undecidability와 동형(Chaitin Ω처럼 well-defined but non-computable). **독립 확인: limit-computable 함수 클래스는 inverse limit 하 비폐쇄**(Wikipedia Limit lemma + Chan REU) — computable 대상의 극한이 일반적으로 computable 밖. 따라서 "CHU(computable-제약) = untruncated Ruliad(entangled limit)"는 정의상 모순: 좌변 = computability 하 닫힌 구조, 우변 = 그 닫힘이 실패하는 극한 completion → 다른 cardinality/위상.
- 출처: Wolfram Ruliad; MathWorld Ruliad; Wikipedia Limit lemma; Chan "Limit Computable Sets and Degrees"; sciencephilosophy.org
- caveat: Wolfram이 Ruliad non-computable을 Turing-degree로 형식 증명한 건 아님(물리/철학 서술). closure-failure 정리는 일반 결과, Ruliad 직접 적용 논문 미발견(구조유사 analogy). 강한 analogical inference.

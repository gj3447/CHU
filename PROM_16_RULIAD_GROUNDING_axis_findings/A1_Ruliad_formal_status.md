# A1 — Ruliad의 형식적 지위

**축 질문**: Wolfram이 Ruliad를 수학적으로 엄밀히 정의했는가, 아니면 비형식/서술적 개념인가.
**축 합성**: Ruliad는 Wolfram 본인도 "미완성"이라 인정하는 서술적 개념(S1). peer 물리학계는 엄밀 수학으로 거부(S2). Gorard의 ∞-groupoid 재구성이 가장 가까운 형식화지만 proxy이지 Ruliad 동일성 증명은 아님(S3). 명확한 opaque axiom(CHU) ↔ 조립절차 미정의 극한(Ruliad) 동일시는 category error(S4).

---

## A1S1 — primary-source — `UNGROUNDED` (HIGH)
Wolfram 2021 원문은 ruliad를 비형식적으로만 정의: "the entangled limit of everything that is computationally possible." 형식화 미완("still only at the very beginning of nailing down those technical details ... difficult mathematics and formalism") 명시, 무한극한 조립에 "particular choices" 개입 인정. "Limit"은 서술적/철학적 사용이지 category-theoretic colimit 구성 아님. Ruliad = "abstract necessity"로 프레이밍, 엄밀히 구성된 대상 아님.
- 출처: The Concept of the Ruliad — Stephen Wolfram Writings (2021) https://writings.stephenwolfram.com/2021/11/the-concept-of-the-ruliad/
- caveat: arXiv:2111.03460 직접 미확인(lens 범위 밖 = Wolfram 1차 소스만).

## A1S2 — academic-critique — `UNGROUNDED`* (MEDIUM)
peer 물리학자들이 Ruliad/WPP를 엄밀 수학으로 거부. Aaronson: "infinitely flexible", 결과를 post-hoc "grafted onto", 구체 규칙 부재로 반증가능 예측 불가(2002 리뷰: hidden-variable이 상대성+Bell 위반과 양립불가 증명). Harlow(Scientific American): 성과가 "at best qualitative", QM/GR 정량예측 미재현, 단순규칙 아이디어 자체가 비독창(Turing/von Neumann/Conway 선례).
- 출처: Scientific American "Physicists Criticize Wolfram's ToE"; SingleLunch "dead end"; arXiv:2411.12562; 4gravitons; Scott Aaronson blog
- *grounding_verdict 필드 누락, 내용상 UNGROUNDED. caveat: 비판이 WPP 일반 겨냥, Ruliad 순수 계산이론 형식화 직접 아님.

## A1S3 — formal-bridge — `PARTIAL` (MEDIUM)
Gorard arXiv:2111.03460이 rulial multiway system의 n→∞ 극한을 ∞-groupoid(Grothendieck homotopy hypothesis)로, classifying space를 (∞,1)-topos 구조로 형식화 — Ruliad의 가장 가까운 엄밀 category-theoretic 재구성. 자매 논문 2105.10822(n-fold categories), 별개 라인 2010.02752(ZX-calculus + adhesive category + double-pushout rewriting). **어느 논문도 Ruliad를 "colimit/terminal object"로 명시 정의하지 않음** — 어휘는 ∞-groupoid/classifying space/(∞,1)-topos, rulial multiway system(Ruliad의 proxy)에 적용.
- 출처: arXiv:2111.03460, 2105.10822, 2010.02752, 2403.16269, 2308.16068
- caveat: full-text 미확인(abstract-level). "colimit" 어휘는 SYMPOSIUM-side일 가능성.

## A1S4 — falsification — `DIVERGES` (MEDIUM)
CHU = `axiom CHU:Type` + `CHUPiece:=CHU→Prop`, Lean kernel 검증되는 opaque하지만 well-typed 구조. Ruliad = 조립 자체가 (1) rewriting 적용순서 미정의 (2) 무한극한에 암묵 choice (3) 그 choice 지배규칙 = hyperruliad 무한회귀. 명확한 opaque axiom ↔ 구성절차 미정의 극한 동일시 = category error.
- 출처: Wolfram Ruliad 원문; arXiv:2411.12562 (Natal, Refuting Wolfram+Tegmark); arXiv:2308.16068 (Ruliology)
- caveat: Wolfram은 choice를 "관찰자 상대성"으로 재해석(결함 아닌 특징 주장). CHU도 THEORY/CHU/CHU_Pratt_Semantic_Bridge.md에서 "미래 concretize"라 명시 — 완전히 닫힌 정의 아님(단 Lean kernel-safe axiom이라 형식지위 다름).

# A2 — Homotopy type 동일시 (multiway → ∞-groupoid / (∞,1)-topos)

**축 질문**: multiway system을 ∞-groupoid/(∞,1)-topos로 보는 동일시가 문헌에서 실제로 확립됐는가.
**축 합성**: 4셀 전부 PARTIAL. 형식화는 실재하고 peer-reviewed(IJTP 2024)지만 — proxy(rulial multiway)이지 Ruliad 동일성 증명 아님, n→∞ 단계 near-tautological, topos 주장 저자 hedge, 독립 HoTT 검증 부재, **소스에 univalence-untruncation 구성 없음**.

---

## A2S1 — primary-source — `PARTIAL` (HIGH, pdftotext 직접검증)
arXiv:2111.03460 Prop 4.2(multiway + n-order homotopy rules → n-fold category, 귀납 증명) + Prop 4.3(n→∞ 극한 = ∞-groupoid) 증명. **단 Prop 4.3 증명은 거의 항진** — "n-fold groupoid의 n→∞ 극한이 정확히 ∞-groupoid" — 존재는 "infinite hierarchy of rules ... admissible"라는 미검증 조건 하에서만 주장. Prop 4.4는 *limiting rulial multiverse*가 (∞,1)-**category** ∞Grpd를 이룬다만 증명(Lurie 인용), (∞,1)-**topos**라는 건 아님. topos 주장은 hedged Remark 4.6/§5("may be realized", "interesting to investigate")뿐 — Proposition 아님. **"univalence로 untruncate" 구성 논문에 없음** — §5.3은 univalence를 paths/types 동일시의 철학적 backing으로만 논함.
- 출처: arXiv:2111.03460 (PDF fetched + pdftotext, Prop 4.2/4.3/4.4/§5.3 full read)
- caveat: "CHU = Ruliad untruncated via univalence"는 SYMPOSIUM-side 확장, 저자 주장 아님.

## A2S2 — academic-critique — `PARTIAL` (MEDIUM)
arXiv:2111.03460은 **International Journal of Theoretical Physics (Springer, 2024) 정식 게재** — preprint 이상 지위. 그러나 citing work = 저자 자기 논문(2105.10822) + Wolfram Institute/Community 재게시뿐. **nLab에 Wolfram model/ruliad 항목 없음**, HoTT 커뮤니티(ncatlab/UniMath/homotopytypetheory.org) 연구자 engagement 미발견. 광범위 물리학 비판은 categorical/homotopy 구성이 아닌 physics-TOE 겨냥.
- 출처: arXiv:2111.03460; Springer IJTP 10.1007/s10773-024-05576-0; arXiv:2105.10822; nLab HoTT
- caveat: citation-graph 툴(Semantic Scholar/INSPIRE) 미사용, 스니펫 부재가 zero uptake 확증은 아님.

## A2S3 — formal-bridge — `PARTIAL` (MEDIUM)
독립 수학 프로그램 실재: polygraphs/computads(Burroni 1993, Guiraud-Métayer-Malbos-Mimram, 2023 Cambridge monograph "Polygraphs: From Rewriting to Higher Categories")가 abstract/higher-dim rewriting → strict ∞-category 제시(Squier 정리로 coherence). rewriting↔HoTT 직접 다리도 실재: "A Rewriting Coherence Theorem with Applications in HoTT" (arXiv:2107.01594, MSCS/Cambridge). "rewriting → higher category/groupoid"는 Wolfram 밖 수십년 프로그램.
- 출처: arXiv:2312.00429, 2107.01594, 2511.16852
- caveat: **polygraph는 strict ∞-category**, HoTT/univalence는 **weak ∞-groupoid** 필요 — strict↔weak gap 미해소. 일반원리는 grounding하나 "Wolfram multiway = univalent (∞,1)-topos = Ruliad" 특정 동일성은 여전히 2111.03460 자체에 의존.

## A2S4 — falsification — `PARTIAL` (MEDIUM)
3 gap 확인: (1) Gorard ∞-groupoid는 *rulial* multiway(모든 규칙 union)라 substrate-fixed 덜하나 여전히 hypergraph/string rewriting에 scope됨 — "모든 계산 소진" = 미증명 Church-Turing-Wolfram thesis. (2) n→∞ 극한은 "upon inclusion of appropriate inverse morphisms"(구성/주장된 단계)로 서술 — 독립검증된 존재증명 아님, Wolfram-affiliated 게재(Complex Systems)+IJTP 1편. (3) **로컬 CHU 소스(A4_HoTT_Univalence_TegmarkIV.md L238) 직접 확인: CHU가 identity=hypergraph-iso를 univalence로 공리화** — arXiv:2111.03460 abstract엔 univalence/HoTT 언급 zero. univalence는 CHU bolt-on.
- 출처: arXiv:2111.03460, 2105.10822; Springer IJTP; local A4_HoTT_Univalence_TegmarkIV.md L238
- caveat: full PDF body 미확인(abstract만), Prop 4.3 정확한 증명/conjecture 지위는 2차 서술 기반 추론.

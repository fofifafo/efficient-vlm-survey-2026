"""엄격 태그 정의 고정 (9/16, 리뷰 대응). 표 I '그라운딩을 기여로 명시'와 VI(i) 임상 검증 엄격 수치의 출처.
실행: python strict_tags.py  → 연도별 수·비율·Fisher p 출력."""
import re, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.chdir(os.path.dirname(os.path.abspath(__file__)))
_o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8")
import medical_taxonomy as mt
sys.stdout = _o
med = mt.med; yr = lambda p: p["date"][:4]
N = collections.Counter(yr(p) for p in med)
STRICT = {
  # 그라운딩을 기여로 명시: 한 문장 안에서 propose/present/introduce 뒤에 그라운딩 어휘가 온다
  "grounding_contribution": r"(propose|present|introduce)[^.]{0,200}(grounding|localiz|bounding box|lesion detection|abnormality detection)",
  # 임상 검증(엄격): 판독자 연구, 전향적, 임상시험, 방사선사/임상의/의사의 평가
  "clinical_validation_strict": r"reader study|prospective|clinical trial|(radiologist|clinician|physician)s? (evaluat|assess)|evaluat\w* by (\w+ )?(radiologist|clinician|physician)",
}
def fisher_exact(t):
    """양측 Fisher 정확검정 (scipy 없이). 관측표보다 확률이 같거나 작은 모든 표의 확률 합."""
    from math import lgamma, exp
    (a, b), (c, d) = t; r1, r2, c1, c2 = a + b, c + d, a + c, b + d; n = r1 + r2
    def lp(x):
        return (lgamma(r1 + 1) + lgamma(r2 + 1) + lgamma(c1 + 1) + lgamma(c2 + 1) - lgamma(n + 1)
                - lgamma(x + 1) - lgamma(r1 - x + 1) - lgamma(c1 - x + 1) - lgamma(r2 - c1 + x + 1))
    p0 = lp(a); tot = 0.0
    for x in range(max(0, c1 - r2), min(r1, c1) + 1):
        v = lp(x)
        if v <= p0 + 1e-9: tot += exp(v)
    return None, min(1.0, tot)
if __name__ == "__main__":
    for name, pat in STRICT.items():
        r = re.compile(pat, re.I)
        c = collections.Counter(yr(p) for p in med if r.search(p["title"] + " " + p["abstract"]))
        a, b = c["2024"], c["2026"]
        p = fisher_exact([[a, N["2024"] - a], [b, N["2026"] - b]])[1]
        print(f"{name}: n={sum(c.values())}  2024 {a}/{N['2024']} ({100*a/N['2024']:.1f}%)  2025 {c['2025']}/{N['2025']} ({100*c['2025']/N['2025']:.1f}%)  2026 {b}/{N['2026']} ({100*b/N['2026']:.1f}%)  Δ={100*b/N['2026']-100*a/N['2024']:+.1f}pp  p={p:.3g}")

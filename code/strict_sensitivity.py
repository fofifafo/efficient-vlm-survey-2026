# -*- coding: utf-8 -*-
"""2차 리뷰 질문 2(10/14): 엄격 정의의 제안 문형을 좁히거나 바꿔도 결론(실행 가지만 유의 성장, 학습 가지 감소)이 유지되는가.
   기준(main_taxonomy.PROP): 주어 we | this paper/work/study, 동사 propose|present|introduce|design|develop|build.
   변형 v3: 동사 3개(propose|present|introduce)만,  vwe: 주어 we 만 + 동사 3개,  vno_title: 제목 일치 없이 문장만.
   나머지(가지 어휘, 4.5·4.6 의 별도 엄격 정의, 제목 일치 규칙, Fisher, Bonferroni 0.05/12)는 main_taxonomy 와 같다.
   실행: python strict_sensitivity.py → main_survey/strict_sensitivity.csv"""
import contextlib, csv, io, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ".")
_o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8")
import main_taxonomy as mt              # 기준 분석을 그대로 다시 돌린다(같은 입력 → 같은 출력 파일)
sys.stdout = _o
from strict_tags import fisher_exact
V = {
 "base": (mt.PROP, True),
 "v3": (r"(?:\bwe\b|this (?:paper|work|study))[^.]{0,40}?\b(?:propose|present|introduce)[^.]{0,200}?", True),
 "vwe": (r"\bwe\b[^.]{0,40}?\b(?:propose|present|introduce)[^.]{0,200}?", True),
 "vno_title": (mt.PROP, False),
}
rows = []
for P, cname in ((mt.pool, "pool"), (mt.core, "vlm")):
    N = collections.Counter(mt.yr(p) for p in P)
    for vk, (prop, use_title) in V.items():
        for b, lab, loose in mt.BRANCHES:
            if b in mt.STRICT_OVERRIDE: continue          # 4.5·4.6 은 제안 문형을 쓰지 않음
            rx = re.compile(prop + "(?:" + loose + ")", re.I); lt = re.compile(loose, re.I)
            hit = [p for p in P if rx.search(p["t"]) or (use_title and lt.search(p["title"]))]
            c = collections.Counter(mt.yr(p) for p in hit); a, z = c["2024"], c["2026"]
            s24, s26 = 100 * a / N["2024"], 100 * z / N["2026"]; pf = fisher_exact([[a, N["2024"] - a], [z, N["2026"] - z]])[1]
            rows.append(dict(corpus=cname, variant=vk, branch=b, n=len(hit), n24=a, n26=z, s24=round(s24, 2), s26=round(s26, 2),
                             rel_growth=round(s26 / s24, 2) if a else None, p_fisher=pf, sig_bonf=pf < 0.05 / 12))
with open("main_survey/strict_sensitivity.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['corpus']:5} {r['variant']:9} {r['branch']} n={r['n']:4} {r['s24']:5}→{r['s26']:5} ×{r['rel_growth']} p={r['p_fisher']:.1e} {'*' if r['sig_bonf'] else ''}")

# -*- coding: utf-8 -*-
"""두 번째 외부 심사(10/27) 대응 계산 — 새 판정 없음(기존 규칙·라벨·예측 파일만).
   (a) 같은 기간 비교: 2024년 1–8월 vs 2026년 1–8월, 가지별 엄격 비율·성장·Fisher, Bonferroni·Holm (VLM 전체·효율 풀)
   (b) 실행 시점 vs 압축 성장 직접 비교: 논문 단위 부트스트랩(연도 안에서 재표집)으로 성장 배율의 비와 95% 구간
   (c) 오분류 보정: 연도별 정밀도·재현율(1차 평가자 라벨: 12/13·13/13, 5/10·8/11)로 보정한 성장 배율과 부트스트랩 구간
   (d) 같은 토큰 예산(64) 안의 방법 순위의 GPU 간 Spearman
   (e) 기준 대비 정확도 차이의 짝지은 부트스트랩 95% 구간(5080, 문항 재표집; MME 는 이미지 단위)
   (f) 방법별 평균 답 길이(GQA 예측, 단어 수)
   출력: main_survey/review_stats.json. 실행: python review_stats.py"""
import collections, csv, json, os, re, sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, "."); sys.path.insert(0, "bench")
_o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8")
import main_taxonomy as mt
sys.stdout = _o
from strict_tags import fisher_exact
import score as SC
rng = np.random.default_rng(20261028); B = 2000; O = {}
BR = {b: l for b, _, l in mt.BRANCHES}
def matchers(b):
    st = re.compile(mt.PROP + "(?:" + BR[b] + ")", re.I); lt = re.compile(BR[b], re.I)
    return (lambda p: bool(lt.search(p["t"]))), (lambda p: bool(st.search(p["t"]) or lt.search(p["title"])))
def month(p):
    d = p.get("published") or p.get("date") or ""
    return int(d[5:7]) if len(d) >= 7 and d[5:7].isdigit() else None
# (a) 같은 기간
sample = mt.papers[0]; O["date_field"] = [k for k in ("published", "date") if k in sample]
rows = []
for cname, P in (("vlm", mt.core), ("pool", mt.pool)):
    S = {y: [p for p in P if mt.yr(p) == y and (month(p) or 99) <= 8] for y in ("2024", "2026")}
    for b in BR:
        fl, fs = matchers(b)
        for kind, f in (("loose", fl), ("strict", fs)):
            a = sum(map(f, S["2024"])); z = sum(map(f, S["2026"])); n4, n6 = len(S["2024"]), len(S["2026"])
            pf = fisher_exact([[a, n4 - a], [z, n6 - z]])[1]
            rows.append(dict(corpus=cname, branch=b, kind=kind, n24=n4, n26=n6, c24=a, c26=z, s24=round(100 * a / n4, 2), s26=round(100 * z / n6, 2),
                             growth=round((z / n6) / (a / n4), 2) if a else None, p=float(f"{pf:.2e}")))
for cname in ("vlm", "pool"):
    R = [r for r in rows if r["corpus"] == cname]; m = len(R); ps = sorted(range(m), key=lambda i: R[i]["p"])
    for r in R: r["bonf"] = r["p"] < 0.05 / m
    ok = True
    for rank, i in enumerate(ps):
        ok = ok and R[i]["p"] < 0.05 / (m - rank); R[i]["holm"] = ok
O["same_period"] = rows
# (b)(c) 부트스트랩: 실행(4.4)·압축(4.3) 엄격, VLM 전체 1–12월(원고 정의) 기준
fl44, fs44 = matchers("4.4"); fl43, fs43 = matchers("4.3")
V = {y: [p for p in mt.core if mt.yr(p) == y] for y in ("2024", "2026")}
X = {y: np.array([[fs44(p), fs43(p)] for p in V[y]], dtype=float) for y in V}
g = lambda a, z: (z.mean(0)) / (a.mean(0))
base = g(X["2024"], X["2026"]); O["growth_exec"], O["growth_comp"] = round(base[0], 2), round(base[1], 2)
bs = []
for _ in range(B):
    a = X["2024"][rng.integers(0, len(X["2024"]), len(X["2024"]))]; z = X["2026"][rng.integers(0, len(X["2026"]), len(X["2026"]))]
    bs.append(g(a, z))
bs = np.array(bs); ratio = bs[:, 0] / bs[:, 1]
O["exec_over_comp_ratio"] = round(base[0] / base[1], 2); O["exec_over_comp_ci"] = [round(float(np.percentile(ratio, 2.5)), 2), round(float(np.percentile(ratio, 97.5)), 2)]
O["exec_over_comp_p_le1"] = round(float((ratio <= 1).mean()), 3)
O["growth_exec_ci"] = [round(float(np.percentile(bs[:, 0], q)), 2) for q in (2.5, 97.5)]; O["growth_comp_ci"] = [round(float(np.percentile(bs[:, 1], q)), 2) for q in (2.5, 97.5)]
# (c) 오분류 보정: 참 비율 ≈ 관측 × 정밀도 / 재현율 (연도별), 이항 부트스트랩
PR = {"2024": (12, 13, 5, 10), "2026": (13, 13, 8, 11)}
corr = []
for _ in range(B):
    f = {}
    for y, (tp, n, hit, pos) in PR.items():
        pr = rng.beta(tp + 0.5, n - tp + 0.5); rc = rng.beta(hit + 0.5, pos - hit + 0.5); f[y] = pr / rc
    corr.append(f["2026"] / f["2024"])
corr = np.array(corr); pt = (13 / 13 / (8 / 11)) / (12 / 13 / (5 / 10))
O["misclass_factor_point"] = round(pt, 2); O["growth_exec_corrected_point"] = round(base[0] * pt, 2)
gc = bs[:, 0] * corr; O["growth_exec_corrected_ci"] = [round(float(np.percentile(gc, q)), 2) for q in (2.5, 97.5)]
O["growth_exec_corrected_median"] = round(float(np.median(gc)), 2)
# (d) 같은 예산(64) 순위 상관
X2 = list(csv.DictReader(open("bench/results_cross/table_cross.csv", encoding="utf-8")))
def spearman(x, y):
    rk = lambda v: {i: r for r, i in enumerate(sorted(range(len(v)), key=lambda i: v[i]))}
    rx, ry = rk(x), rk(y); n = len(x); return 1 - 6 * sum((rx[i] - ry[i]) ** 2 for i in range(n)) / (n * (n * n - 1))
r64 = [r for r in X2 if r["setting"] == "r889"]; O["rank64_methods"] = [r["key"] for r in r64]
O["spearman_ttft_64"] = round(spearman([float(r["pc1_ttft"]) for r in r64], [float(r["pc2_ttft"]) for r in r64]), 2)
O["order64_pc1"] = [r["key"] for r in sorted(r64, key=lambda r: float(r["pc1_ttft"]))]; O["order64_pc2"] = [r["key"] for r in sorted(r64, key=lambda r: float(r["pc2_ttft"]))]
for t in ("gqa", "pope", "mme"):
    O[f"spearman_{t}_64"] = round(spearman([float(r[f"pc1_{t}"]) for r in r64], [float(r[f"pc2_{t}"]) for r in r64]), 2)
# (e) 정확도 차이 부트스트랩, (f) 답 길이
R1 = "bench/results_pc1"
def load(m, s, t):   # POPE: 하위 세트마다 번호가 1부터이고, 나중 실행은 qid="popeN"·원래 번호는 question_id → 범주 + 원래 번호로 키
    return {f'{r.get("category", "")}/{r.get("question_id", r["qid"])}': r for r in map(json.loads, open(f"{R1}/{m}/acc_{s}/preds_{t}.jsonl", encoding="utf-8"))}
ACC = {}; LEN = {}
base_p = {t: load("base", "default", t) for t in ("gqa", "pope", "textvqa", "mme")}
for m in ("base", "vispruner", "cdpruner_fix", "sparsevlm", "dart", "fastv"):
    for s in ("default", "r889"):
        if m == "base" and s == "r889": continue
        if not os.path.exists(f"{R1}/{m}/acc_{s}"): continue
        g_ = load(m, s, "gqa"); LEN[f"{m}.{s}"] = round(float(np.mean([len(r["pred"].split()) for r in g_.values()])), 2)
        if m == "base": continue
        res = {}
        for t in ("gqa", "pope", "textvqa", "mme"):
            mp = load(m, s, t); ids = sorted(set(mp) & set(base_p[t])); bp = [base_p[t][i] for i in ids]; pp = [mp[i] for i in ids]
            assert len(ids) == len(mp) == len(base_p[t]) and all(str(a.get("answer", a.get("answers"))) == str(b.get("answer", b.get("answers"))) for a, b in zip(bp, pp)), (m, s, t, len(ids))
            fn = {"gqa": lambda rs: 100 * SC.score_gqa(rs)["acc"], "pope": lambda rs: 100 * SC.score_pope(rs)["f1"], "textvqa": lambda rs: 100 * SC.score_textvqa(rs)["acc"],
                  "mme": lambda rs: SC.score_mme(rs)["perception_total"]}[t]
            d0 = fn(pp) - fn(bp)
            if t == "mme":                                         # 이미지 단위로 묶어 재표집(acc+ 가 이미지 단위)
                img = collections.defaultdict(list)
                for k, i in enumerate(ids): img[(pp[k]["category"], pp[k]["image_id"])].append(k)
                keys = list(img); cat = collections.defaultdict(list)
                for kk in keys: cat[kk[0]].append(kk)
                vals = []                                           # 범주 안에서 이미지 재표집; 다시 뽑힌 이미지는 새 id 로 acc+ 를 따로 셈
                for _ in range(400):
                    pr_, br_ = [], []
                    for c in cat:
                        for j in rng.integers(0, len(cat[c]), len(cat[c])):
                            kk = cat[c][j]; u = f"{kk[1]}@{len(pr_)}"
                            pr_ += [dict(pp[k], image_id=u) for k in img[kk]]; br_ += [dict(bp[k], image_id=u) for k in img[kk]]
                    vals.append(fn(pr_) - fn(br_))
                lo, hi = np.percentile(vals, [2.5, 97.5])
            else:
                n = len(ids); vals = []
                for _ in range(B if t != "textvqa" else 1000):
                    sel = rng.integers(0, n, n); vals.append(fn([pp[k] for k in sel]) - fn([bp[k] for k in sel]))
                lo, hi = np.percentile(vals, [2.5, 97.5])
            res[t] = dict(diff=round(d0, 2), ci=[round(float(lo), 2), round(float(hi), 2)])
        ACC[f"{m}.{s}"] = res; print(m, s, {t: (v["diff"], v["ci"]) for t, v in res.items()}, flush=True)
O["acc_diff_vs_base"] = ACC; O["answer_words_gqa"] = LEN
json.dump(O, open("main_survey/review_stats.json", "w", encoding="utf-8"), indent=1)
print(json.dumps({k: v for k, v in O.items() if k not in ("same_period", "acc_diff_vs_base")}, indent=0))
for r in O["same_period"]:
    if r["kind"] == "strict": print(r["corpus"], r["branch"], r["c24"], r["c26"], r["s24"], r["s26"], "x", r["growth"], r["p"], "bonf" if r["bonf"] else "", "holm" if r["holm"] else "")

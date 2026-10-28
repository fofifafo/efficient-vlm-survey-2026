# -*- coding: utf-8 -*-
"""두 번째 외부 심사(10/27) 대응 — 단순 기준선(균등 선택·풀링·FastV K=2) 정확도 비교. 새 판정 없음(예측 파일만).
   (a) 원본 대비 차이, (b) 같은 토큰 수의 균등 선택 대비 차이(128·64), (c) FastV K=2 대 K=3.
   짝지은 부트스트랩 95% 구간(5080, 문항 재표집; MME 는 범주 안 이미지 단위) — review_stats.py (e) 와 같은 방식.
   출력: main_survey/baseline_comparison.json. 실행: python baseline_comparison.py"""
import collections, json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, "bench")
import score as SC
rng = np.random.default_rng(20261028); B = 2000
R1 = "bench/results_pc1"; TASKS = ("gqa", "pope", "textvqa", "mme")
FN = {"gqa": lambda rs: 100 * SC.score_gqa(rs)["acc"], "pope": lambda rs: 100 * SC.score_pope(rs)["f1"],
      "textvqa": lambda rs: 100 * SC.score_textvqa(rs)["acc"], "mme": lambda rs: SC.score_mme(rs)["perception_total"]}
_cache = {}
def load(ms, t):   # ms = "method.setting"; POPE 키는 범주 + 원래 번호
    if (ms, t) not in _cache:
        m, s = ms.split(".")
        _cache[ms, t] = {f'{r.get("category", "")}/{r.get("question_id", r["qid"])}': r for r in map(json.loads, open(f"{R1}/{m}/acc_{s}/preds_{t}.jsonl", encoding="utf-8"))}
    return _cache[ms, t]
def compare(a, b):   # a − b
    res = {}
    for t in TASKS:
        ma, mb = load(a, t), load(b, t); ids = sorted(set(ma) & set(mb)); pa = [ma[i] for i in ids]; pb = [mb[i] for i in ids]
        assert len(ids) == len(ma) == len(mb) and all(str(x.get("answer", x.get("answers"))) == str(y.get("answer", y.get("answers"))) for x, y in zip(pa, pb)), (a, b, t, len(ids))
        fn = FN[t]; d0 = fn(pa) - fn(pb); vals = []
        if t == "mme":
            img = collections.defaultdict(list)
            for k, i in enumerate(ids): img[(pa[k]["category"], pa[k]["image_id"])].append(k)
            cat = collections.defaultdict(list)
            for kk in img: cat[kk[0]].append(kk)
            for _ in range(400):
                xa, xb = [], []
                for c in cat:
                    for j in rng.integers(0, len(cat[c]), len(cat[c])):
                        kk = cat[c][j]; u = f"{kk[1]}@{len(xa)}"
                        xa += [dict(pa[k], image_id=u) for k in img[kk]]; xb += [dict(pb[k], image_id=u) for k in img[kk]]
                vals.append(fn(xa) - fn(xb))
        else:
            n = len(ids)
            for _ in range(B if t != "textvqa" else 1000):
                sel = rng.integers(0, n, n); vals.append(fn([pa[k] for k in sel]) - fn([pb[k] for k in sel]))
        lo, hi = np.percentile(vals, [2.5, 97.5])
        res[t] = dict(a=round(fn(pa), 2), b=round(fn(pb), 2), diff=round(d0, 2), ci=[round(float(lo), 2), round(float(hi), 2)], sig=bool(lo > 0 or hi < 0))
    print(f"{a} − {b}:", {t: (v["diff"], v["ci"], "*" if v["sig"] else "") for t, v in res.items()}, flush=True)
    return res
PAIRS = {"vs_base": [(x, "base.default") for x in ("uniform.default", "uniform.r889", "pool.default", "pool.r889", "fastv.k2", "fastv.k2r889")],
         "vs_uniform128": [(x, "uniform.default") for x in ("vispruner.default", "cdpruner_fix.default", "dart.default", "pool.default")],
         "vs_uniform64": [(x, "uniform.r889") for x in ("vispruner.r889", "cdpruner_fix.r889", "sparsevlm.r889", "dart.r889", "fastv.r889", "fastv.k2r889", "pool.r889")],
         "fastv_k2_vs_k3": [("fastv.k2", "fastv.default"), ("fastv.k2r889", "fastv.r889")]}
O = {g: {f"{a}|{b}": compare(a, b) for a, b in ps} for g, ps in PAIRS.items()}
json.dump(O, open("main_survey/baseline_comparison.json", "w", encoding="utf-8"), indent=1)

# -*- coding: utf-8 -*-
"""3차 리뷰 2번(2026-10-16): 현재 규칙(v2.1)으로 본 가지별 정밀도·재현율 표. 새 판정 없음 — 1차 평가자 판정(1차 400건, 새 표본 55건)만 사용.
   재현율: 1차 재현율 표본(효율 풀 100편)의 사람 판정 대비 현재 규칙의 일치. 4.3·4.5 는 이 표본을 본 뒤 규칙을 좁혔으므로 재현율은 같은 표본 값(낙관적일 수 있음),
   정밀도는 새 표본(55편, round2_result.json). 나머지 가지는 규칙을 바꾸지 않았으므로 1차 표본 값이 그대로 표본 밖 추정.
   출력: classval_table_current.json. 실행: python main_survey/classval/recall_current_rules.py"""
import csv, json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8"); HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
os.chdir(ROOT); sys.path.insert(0, ROOT)
_o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8")
import main_taxonomy as mt
sys.stdout = _o
from openpyxl import load_workbook
BR = ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]
KR = list(csv.DictReader(open(os.path.join(HERE, "answer_key_recall.csv"), encoding="utf-8-sig")))
P = {p["id"] if "id" in p else p.get("arxiv_id"): p for p in mt.papers}
def wilson(k, n):
    if n == 0: return (None, None)
    p = k / n; z = 1.96; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return round(100 * (c - h), 1), round(100 * (c + h), 1)
import re
def codes(v):
    v = str(v or ""); return set() if "없" in v else set(re.findall(r"4\.[1-6]", v))
wb = load_workbook(os.path.join(HERE, "returned_평가자1.xlsx"), data_only=True); b = wb["B_재현율"]
G = {int(r[0]): (codes(r[4]), codes(r[5])) for r in b.iter_rows(min_row=2, values_only=True) if r[0]}
def hits(p, br):
    for bb, lab, loose, strict, _ in mt.RX:
        if bb != br: continue
        L = bool(loose.search(p["t"]))
        S = bool(strict.search(p["t"])) if bb in mt.STRICT_OVERRIDE else bool(strict.search(p["t"]) or loose.search(p["title"]))
        return L, S
miss = [k["arxiv_id"] for k in KR if k["arxiv_id"] not in P]
out = {"missing_papers": miss, "recall": {}, "changed_vs_key": 0}
for br in BR:
    for lv, nm in ((0, "loose"), (1, "strict")):
        pos = [k for k in KR if br in G[int(k["row"])][lv] and k["arxiv_id"] in P]
        h = [k for k in pos if hits(P[k["arxiv_id"]], br)[lv]]
        old = [k for k in pos if k[f"{nm}_{br}"] == "True"]
        out["recall"][f"{br}.{nm}"] = dict(n_pos=len(pos), hit=len(h), recall=round(100 * len(h) / len(pos), 1) if pos else None, ci=wilson(len(h), len(pos)), old_rule_hit=len(old))
json.dump(out, open(os.path.join(HERE, "classval_table_current.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=0))

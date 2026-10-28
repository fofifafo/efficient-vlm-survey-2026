# -*- coding: utf-8 -*-
"""분류 규칙 검증 채점(2차 리뷰 M1). 입력: 두 평가자가 채운 분류검증_시트_평가자{1,2}.xlsx.
   1) 평가자 간 일치: Q1·Q2(시트 A), 가지별 판정(시트 B)의 Cohen κ 와 일치율.
   2) 불일치 목록 → 합의용 시트(합의_분류검증.xlsx). 합의 결과가 있으면(세 번째 인자) 그것을 정답으로, 없으면 두 평가자가 모두 '예'인 것만 양성으로 본다.
   3) 정밀도: 엄격 = 엄격 층의 Q2 비율, 느슨 = (엄격∩느슨 층, 느슨만 층) Q1 비율을 층 크기로 가중. 연도별·전체, 95% Wilson 구간.
   4) 재현율(효율 풀): 사람이 양성으로 본 논문 중 규칙도 잡은 비율(가지별, 느슨·엄격).
   실행: python main_survey/classval/score_classval.py 평가자1.xlsx 평가자2.xlsx [합의.xlsx] → classval_result.json"""
import csv, json, math, os, sys, collections, re
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
from openpyxl import load_workbook, Workbook
KP = list(csv.DictReader(open(os.path.join(HERE, "answer_key_precision.csv"), encoding="utf-8-sig")))
KR = list(csv.DictReader(open(os.path.join(HERE, "answer_key_recall.csv"), encoding="utf-8-sig")))
BR = ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]
def yn(v): v = (str(v or "")).strip(); return True if v.startswith("예") else (False if v.startswith("아니") else None)
def codes(v):
    v = str(v or ""); return set() if "없" in v else set(re.findall(r"4\.[1-6]", v))
def read(path):
    wb = load_workbook(path, data_only=True); a = wb["A_정밀도"]; b = wb["B_재현율"]
    A = {int(r[0]): (yn(r[7]), yn(r[8])) for r in a.iter_rows(min_row=2, values_only=True) if r[0]}
    B = {int(r[0]): (codes(r[4]), codes(r[5])) for r in b.iter_rows(min_row=2, values_only=True) if r[0]}
    return A, B
def kappa(x, y):
    n = len(x); po = sum(a == b for a, b in zip(x, y)) / n; px = sum(x) / n; py = sum(y) / n; pe = px * py + (1 - px) * (1 - py)
    return (round((po - pe) / (1 - pe), 2) if pe < 1 else 1.0), round(100 * po, 1)
def wilson(k, n):
    if n == 0: return (None, None)
    p = k / n; z = 1.96; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return round(100 * (c - h), 1), round(100 * (c + h), 1)
A1, B1 = read(sys.argv[1]); A2, B2 = read(sys.argv[2])
res = {"unfilled_A": [i for i in A1 if None in A1[i] or None in A2[i]]}
for q in (0, 1):
    rows = [i for i in A1 if A1[i][q] is not None and A2[i][q] is not None]
    res[f"kappa_A_Q{q + 1}"], res[f"agree_A_Q{q + 1}"] = kappa([A1[i][q] for i in rows], [A2[i][q] for i in rows])
for lv in (0, 1):
    x = [b in B1[i][lv] for i in B1 for b in BR]; y = [b in B2[i][lv] for i in B1 for b in BR]
    res[f"kappa_B_{['loose', 'strict'][lv]}"], res[f"agree_B_{['loose', 'strict'][lv]}"] = kappa(x, y)
# 합의 정답
ADJ = {}
if len(sys.argv) > 3:
    wb = load_workbook(sys.argv[3], data_only=True); ws = wb.active
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and r[-1] not in (None, ""): ADJ[str(r[0])] = r[-1]
def gold_A(i, q):
    k = f"A{i}Q{q + 1}"
    if k in ADJ: return yn(ADJ[k])
    return A1[i][q] and A2[i][q] if A1[i][q] == A2[i][q] else None
def gold_B(i, b, lv):
    k = f"B{i}-{b}-{['loose', 'strict'][lv]}"
    if k in ADJ: return yn(ADJ[k])
    a, c = b in B1[i][lv], b in B2[i][lv]; return a if a == c else None
# 불일치 → 합의 시트
dis = [(f"A{i}Q{q + 1}", KP[i - 1]["branch"], KP[i - 1]["arxiv_id"], ["Q1 다루는가", "Q2 엄격"][q], A1[i][q], A2[i][q]) for i in A1 for q in (0, 1) if A1[i][q] != A2[i][q]]
dis += [(f"B{i}-{b}-{['loose', 'strict'][lv]}", b, KR[i - 1]["arxiv_id"], ["다루는가", "엄격"][lv], b in B1[i][lv], b in B2[i][lv]) for i in B1 for b in BR for lv in (0, 1) if (b in B1[i][lv]) != (b in B2[i][lv])]
wb = Workbook(); ws = wb.active; ws.title = "합의"; ws.append(["항목", "분야", "arXiv", "질문", "평가자1", "평가자2", "합의 (예/아니오)"])
for d in dis: ws.append([d[0], d[1], d[2], d[3], "예" if d[4] else "아니오", "예" if d[5] else "아니오", ""])
wb.save(os.path.join(HERE, "합의_분류검증.xlsx")); res["n_disagreements"] = len(dis)
# 정밀도
prec = {}
for b in BR:
    for scope in ("2024", "2026", "all"):
        K = [(int(k["row"]), k) for k in KP if k["branch"] == b and (scope == "all" or k["year"] == scope)]
        s = [(i, gold_A(i, 1)) for i, k in K if k["stratum"] == "strict"]; s = [v for _, v in s if v is not None]
        # 느슨: 엄격 층 중 느슨 일치 + 느슨만 층, 층 크기 가중
        num = den = 0.0; nl = 0
        for y in (("2024", "2026") if scope == "all" else (scope,)):
            for st in ("strict", "loose_only"):
                R = [(i, k) for i, k in K if k["year"] == y and k["stratum"] == st and k["loose_hit"] == "True"]
                v = [gold_A(i, 0) for i, _ in R]; v = [x for x in v if x is not None]
                if not v: continue
                Npop = int(R[0][1]["n_stratum"]); num += Npop * sum(v) / len(v); den += Npop; nl += len(v)
        prec[f"{b}.{scope}"] = dict(strict_prec=round(100 * sum(s) / len(s), 1) if s else None, strict_ci=wilson(sum(s), len(s)), strict_n=len(s),
                                    loose_prec=round(100 * num / den, 1) if den else None, loose_n=nl)
res["precision"] = prec
# 재현율(효율 풀)
recall = {}
for b in BR:
    for lv, nm in ((0, "loose"), (1, "strict")):
        pos = [k for k in KR if gold_B(int(k["row"]), b, lv)]
        hit = [k for k in pos if k[f"{nm}_{b}"] == "True"]
        recall[f"{b}.{nm}"] = dict(n_pos=len(pos), recall=round(100 * len(hit) / len(pos), 1) if pos else None, ci=wilson(len(hit), len(pos)))
res["recall_pool"] = recall
json.dump(res, open(os.path.join(HERE, "classval_result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))

# -*- coding: utf-8 -*-
"""블라인드 심사(10/26) 대응 — 결론 해석용 수치. 새 판정 없음(규칙·기존 등급만).
   (1) 실행 시점 엄격 점유율 성장(VLM 전체 ×2.53)의 분해: 효율 풀 비율 성장 × 풀 안 성장, 풀 안 가지별 성장.
   (2) 초록 감사(4.6)를 방법 제안 초록(엄격 4.1–4.5 중 하나)으로 제한한 비율, 연도별.
   (3) 주장한 비용을 재지 않은 항목 = C + A†.  (4) 두 GPU 속도 향상 크기 차이 최대(%).
   출력: main_survey/robustness.json → paper_numbers.py 가 'robust.*' 키로 싣는다. 실행: python robustness_numbers.py"""
import collections, csv, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ".")
_o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8")
import main_taxonomy as mt
sys.stdout = _o
from strict_tags import fisher_exact
AP = json.load(open("draft/numbers/audit_patterns.json", encoding="utf-8"))
AX = [re.compile(v, re.I) for v in AP["metric_terms"].values()]; QTY = re.compile(AP["broader_quantity_rule"], re.I)
BR = {b: l for b, _, l in mt.BRANCHES}
def strict(b):
    st = re.compile(mt.PROP + "(?:" + BR[b] + ")", re.I); lt = re.compile(BR[b], re.I)
    return lambda p: bool(st.search(p["t"]) or lt.search(p["title"]))
S = {b: strict(b) for b in ("4.1", "4.2", "4.3", "4.4", "4.5")}
yr = mt.yr; O = {}
C = collections.Counter(yr(p) for p in mt.core); Pc = collections.Counter(yr(p) for p in mt.pool)
g = lambda c, n: (c["2026"] / n["2026"]) / (c["2024"] / n["2024"])
O["pool_share_pct_2024"], O["pool_share_pct_2026"] = round(100 * Pc["2024"] / C["2024"], 1), round(100 * Pc["2026"] / C["2026"], 1)
O["pool_share_growth"] = round(g(Pc, C), 2)
for b in S:
    cp = collections.Counter(yr(p) for p in mt.pool if S[b](p)); a, z = cp["2024"], cp["2026"]
    O[f"pool_growth_{b}"] = round(g(cp, Pc), 2); O[f"pool_p_{b}"] = float(f"{fisher_exact([[a, Pc['2024'] - a], [z, Pc['2026'] - z]])[1]:.2e}")
    cv = collections.Counter(yr(p) for p in mt.core if S[b](p)); O[f"vlm_growth_{b}"] = round(g(cv, C), 2)
none_m = lambda p: not any(rx.search(p["abstract"]) for rx in AX)
M = [p for p in mt.pool if any(f(p) for f in S.values())]
O["method_n"] = len(M); O["method_none_pct"] = round(100 * sum(map(none_m, M)) / len(M), 1)
O["method_none_qty_pct"] = round(100 * sum(1 for p in M if none_m(p) and not QTY.search(p["abstract"])) / len(M), 1)
for y in ("2024", "2026"):
    My = [p for p in M if yr(p) == y]; O[f"method_none_pct_{y}"] = round(100 * sum(map(none_m, My)) / len(My), 1)
G = list(csv.DictReader(open("main_survey/gradeval/answer_key_grade.csv", encoding="utf-8-sig")))
O["grade_C_entries"] = sum(int(r["entries"]) for r in G if r["grade"] == "C")
O["a_dagger_entries"] = len(json.load(open("main_survey/gradeval/table_cell_corrections.json", encoding="utf-8"))["claim_mismatch_grade_A_dagger"])
O["claim_unmeasured"] = O["grade_C_entries"] + O["a_dagger_entries"]
X = list(csv.DictReader(open("bench/results_cross/table_cross.csv", encoding="utf-8")))
r = [float(x["pc2_speedup"]) / float(x["pc1_speedup"]) for x in X if x["key"] != "base" and x["pc1_speedup"] and x["pc2_speedup"]]
O["speedup_size_diff_max_pct"] = round(100 * (max(max(r), 1 / min(r)) - 1))
json.dump(O, open("main_survey/robustness.json", "w", encoding="utf-8"), indent=1); print(json.dumps(O, indent=0))

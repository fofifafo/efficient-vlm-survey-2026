# -*- coding: utf-8 -*-
"""토큰 수 스윕 결과 json(<스윕 폴더>/<방법>/latency_<설정>.json)을 sweep_summary.csv 한 장으로 모은다(11/6). 보충자료 표가 이 csv 를 읽음.
   10월 sweep/sweep_summary.csv 와 같은 열·같은 반올림. 실행: python bench/jetson/make_sweep_summary.py bench/results_jetson/screen_off/sweep"""
import csv, json, os, sys
D = sys.argv[1]
JOBS = [("base4", "sweep576"), ("vispruner4", "t384"), ("vispruner4", "t256"), ("vispruner4", "default"), ("vispruner4", "r889"), ("vispruner4", "t32")]
rows = []
for m, s in JOBS:
    j = json.load(open(f"{D}/{m}/latency_{s}.json", encoding="utf-8"))
    rows.append([m, s, int(j["n_vis_tokens"]), round(j["ttft_ms_median"], 1), round(j["ttft_ms_p90"], 1), round(j["energy_j_per_sample"], 2),
                 round(j["mean_power_w"], 2), j["peak_alloc_gb"], str([round(r["ttft_ms_median"]) for r in j["runs"]])])
out = sys.argv[2] if len(sys.argv) > 2 else f"{D}/sweep_summary.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f);w.writerow(["method", "setting", "vis_tokens", "ttft_ms_median", "ttft_ms_p90", "energy_j", "power_w", "peak_alloc_gb", "run_ttft"]); w.writerows(rows)
print(out, len(rows), "rows")

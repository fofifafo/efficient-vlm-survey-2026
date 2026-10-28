# -*- coding: utf-8 -*-
"""표 8 생성: 지연(latency_<setting>.json) + 정확도(acc_<setting>/accuracy.json) 를 방법×설정으로 합쳐 CSV/Markdown 출력.
   사용: python make_table8.py [--res ~/vlmbench/results] [--out /mnt/j/VLM-Survey/bench/results_pc1]"""
import argparse, glob, json, os, csv
ap = argparse.ArgumentParser(); ap.add_argument("--res", default=os.path.expanduser("~/vlmbench/results")); ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_pc1")); ap.add_argument("--tag", default="PC1 RTX 5080")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
NAMES = {"base": "LLaVA-1.5-7B (base)", "vispruner": "VisPruner", "dart": "DART", "cdpruner_fix": "CDPruner (fix)", "cdpruner": "CDPruner (as released)", "fastv": "FastV (kv-cache)", "sparsevlm": "SparseVLM"}
ORDER = ["base", "vispruner", "cdpruner_fix", "fastv", "sparsevlm", "dart", "cdpruner"]
rows = []
for m in ORDER:
    for f in sorted(glob.glob(f"{a.res}/{m}/latency_*.json")):
        j = json.load(open(f)); s = j["setting"]
        accf = f"{a.res}/{m}/acc_{s}/accuracy.json"; acc = json.load(open(accf)) if os.path.exists(accf) else {}
        rows.append(dict(method=NAMES.get(m, m), key=m, setting=s, n_vis=int(j["n_vis_tokens"]), ttft_ms=j["ttft_ms_median"], ttft_p90_ms=j["ttft_ms_p90"], total_ms=j["total_ms_median"],
                         peak_vram_gb=j["peak_vram_gb"], energy_j=j["energy_j_per_sample"], power_w=j["mean_power_w"],
                         gqa=100 * acc["gqa"]["acc"] if "gqa" in acc else None, pope_f1=100 * acc["pope"]["f1"] if "pope" in acc else None, pope_n=acc["pope"]["n"] if "pope" in acc else None,
                         textvqa=100 * acc["textvqa"]["acc"] if "textvqa" in acc else None, mme_p=acc["mme"]["perception_total"] if "mme" in acc else None, mme_c=acc["mme"]["cognition_total"] if "mme" in acc else None))
base = next(r for r in rows if r["key"] == "base")
def f(v, d=1): return "" if v is None else f"{v:.{d}f}"
with open(f"{a.out}/table8.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
md = [f"# Table 8 — {a.tag}, LLaVA-1.5-7B FP16, vicuna_v1 prompt, greedy; latency = median of 5 runs × 500 GQA samples; accuracy = full benchmarks", "",
      "| Method | Vis. tokens | TTFT ms (×base) | p90 | End-to-end ms | Peak VRAM GB | Energy J/sample | GQA | POPE F1 | TextVQA | MME-P | MME-C |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    sp = base["ttft_ms"] / r["ttft_ms"]
    md.append(f"| {r['method']} | {r['n_vis']} | {f(r['ttft_ms'])} ({sp:.2f}×) | {f(r['ttft_p90_ms'])} | {f(r['total_ms'])} | {f(r['peak_vram_gb'], 2)} | {f(r['energy_j'])} | {f(r['gqa'])} | {f(r['pope_f1'])} | {f(r['textvqa'])} | {f(r['mme_p'], 0)} | {f(r['mme_c'], 0)} |")
md += ["", "Notes: CDPruner (as released) numbers are unstable on 16 GB (host paging caused by per-call side CUDA streams); the fix variant removes the streams only. FastV uses the authors' kv-cache variant (original in-place variant has no KV cache). SparseVLM is measured after deleting an unused 4 GiB flash_attn weight copy that its builder creates (computation path unchanged); as released it peaks at 17.6 GB and pages to host memory on 16 GB GPUs."]
open(f"{a.out}/table8.md", "w", encoding="utf-8").write("\n".join(md) + "\n"); print("\n".join(md))

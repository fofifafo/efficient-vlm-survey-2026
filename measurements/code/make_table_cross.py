# -*- coding: utf-8 -*-
"""교차 GPU 표: PC1(RTX 5080) × PC2(RTX 5070 Ti), 같은 코드·같은 조건(vicuna_v1, SDPA, 로드 후 empty_cache, CDPruner 수정판).
   PC1: results_pc1/<m>/latency_<s>.json, results_pc1/<m>/acc_<s>/accuracy.json
   PC2: results_pc2/<m>/latency_<s>.json, TextVQA = results_pc2/<m>/acc_<s>/accuracy.json,
        GQA·POPE·MME = results_pc2_accuracy/<m>/acc_<s>/accuracy.json (10/26 재측정, PC1 과 같은 조건: 생성 16토큰, 모두 FP16, CDPruner 수정판),
        FastV 는 results_pc2/fastv/acc_<s>/ (4벤치 전부 같은 조건).
   출력: results_cross/table_cross.{md,csv}
   사용: python make_table_cross.py"""
import csv, json, os, statistics, sys
sys.stdout.reconfigure(encoding="utf-8")
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, "results_cross"); os.makedirs(OUT, exist_ok=True)
ROWS = [("base", "default"), ("vispruner", "default"), ("vispruner", "r889"), ("cdpruner_fix", "default"), ("cdpruner_fix", "r889"),
        ("sparsevlm", "default"), ("sparsevlm", "r889"), ("dart", "default"), ("dart", "r889"), ("fastv", "default"), ("fastv", "r889")]
NAME = {"base": "LLaVA-1.5-7B", "vispruner": "VisPruner", "cdpruner_fix": "CDPruner (fix)", "sparsevlm": "SparseVLM", "dart": "DART", "fastv": "FastV (kv)"}
def J(p): return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
def acc_pc1(m, s):
    d = J(f"{B}/results_pc1/{m}/acc_{s}/accuracy.json") or {}
    return dict(gqa=100 * d["gqa"]["acc"] if "gqa" in d else None, pope=100 * d["pope"]["f1"] if "pope" in d else None,
                tvqa=100 * d["textvqa"]["acc"] if "textvqa" in d else None, mme=d["mme"]["perception_total"] if "mme" in d else None)
def acc_pc2(m, s):
    a16 = J(f"{B}/results_pc2_accuracy/{m}/acc_{s}/accuracy.json") or {}
    v2 = J(f"{B}/results_pc2/{m}/acc_{s}/accuracy.json") or {}
    g = lambda t: a16.get(t) or v2.get(t)         # GQA·POPE·MME = 10/26 재측정(없으면 FastV 처럼 2차 값), TextVQA = 2차
    return dict(gqa=100 * g("gqa")["acc"] if g("gqa") else None, pope=100 * g("pope")["f1"] if g("pope") else None,
                tvqa=100 * v2["textvqa"]["acc"] if "textvqa" in v2 else None, mme=g("mme")["perception_total"] if g("mme") else None)
rows = []
for m, s in ROWS:
    l1 = J(f"{B}/results_pc1/{m}/latency_{s}.json"); l2 = J(f"{B}/results_pc2/{m}/latency_{s}.json")
    if not l1 and not l2: continue
    nv = int((l1 or l2)["n_vis_tokens"])
    r = dict(method=NAME[m], key=m, setting=s, n_vis=nv)
    for tag, l, a in (("pc1", l1, acc_pc1(m, s)), ("pc2", l2, acc_pc2(m, s))):
        for k, src in (("ttft", "ttft_ms_median"), ("total", "total_ms_median"), ("vram", "peak_vram_gb"), ("energy", "energy_j_per_sample"), ("power", "mean_power_w")):
            r[f"{tag}_{k}"] = l[src] if l else None
        for k, v in a.items(): r[f"{tag}_{k}"] = v
    rows.append(r)
base = rows[0]
for r in rows:
    for t in ("pc1", "pc2"):
        r[f"{t}_speedup"] = base[f"{t}_ttft"] / r[f"{t}_ttft"] if r[f"{t}_ttft"] and base[f"{t}_ttft"] else None
        r[f"{t}_eratio"] = base[f"{t}_energy"] / r[f"{t}_energy"] if r[f"{t}_energy"] and base[f"{t}_energy"] else None
with open(f"{OUT}/table_cross.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
f = lambda v, d=1: "—" if v is None else f"{v:.{d}f}"
both = [r for r in rows if r["pc1_ttft"] and r["pc2_ttft"] and r["key"] != "base"]
def rank(v): o = sorted(range(len(v)), key=lambda i: v[i]); rk = [0] * len(v); [rk.__setitem__(i, j) for j, i in enumerate(o)]; return rk
def spearman(x, y):
    rx, ry = rank(x), rank(y); n = len(x); return 1 - 6 * sum((a - b) ** 2 for a, b in zip(rx, ry)) / (n * (n * n - 1))
rho_ttft = spearman([r["pc1_ttft"] for r in both], [r["pc2_ttft"] for r in both])
accd = {k: max(abs(r[f"pc1_{k}"] - r[f"pc2_{k}"]) for r in rows if r[f"pc1_{k}"] is not None and r[f"pc2_{k}"] is not None) for k in ("gqa", "pope", "tvqa", "mme")}
L = ["# Cross-GPU measurement — PC1 RTX 5080 16 GB vs PC2 RTX 5070 Ti 16 GB",
     "LLaVA-1.5-7B FP16, batch 1, vicuna_v1 prompt, SDPA attention, cache released after load; latency = median of 5 runs × 500 GQA samples; accuracy = full benchmarks (TextVQA with OCR reference tokens).", "",
     "## Latency and resources", "",
     "| Method | Tokens | TTFT ms 5080 (×) | TTFT ms 5070 Ti (×) | End-to-end ms 5080 / 5070 Ti | Peak VRAM GB 5080 / 5070 Ti | Energy J 5080 / 5070 Ti |", "|---|---|---|---|---|---|---|"]
for r in rows:
    sp = lambda t: f" ({r[f'{t}_speedup']:.2f}×)" if r[f"{t}_speedup"] else ""
    L.append(f"| {r['method']} | {r['n_vis']} | {f(r['pc1_ttft'])}{sp('pc1')} | {f(r['pc2_ttft'])}{sp('pc2')} | {f(r['pc1_total'])} / {f(r['pc2_total'])} | {f(r['pc1_vram'], 2)} / {f(r['pc2_vram'], 2)} | {f(r['pc1_energy'])} / {f(r['pc2_energy'])} |")
L += ["", "## Accuracy (5080 / 5070 Ti)", "", "| Method | Tokens | GQA | POPE F1 | TextVQA | MME-P |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['method']} | {r['n_vis']} | {f(r['pc1_gqa'], 2)} / {f(r['pc2_gqa'], 2)} | {f(r['pc1_pope'], 2)} / {f(r['pc2_pope'], 2)} | {f(r['pc1_tvqa'], 2)} / {f(r['pc2_tvqa'], 2)} | {f(r['pc1_mme'], 1)} / {f(r['pc2_mme'], 1)} |")
L += ["", "## Agreement", "",
      f"- Max |PC1 − PC2| accuracy: GQA {accd['gqa']:.2f}, POPE F1 {accd['pope']:.2f}, TextVQA {accd['tvqa']:.2f}, MME-P {accd['mme']:.1f} (of 2,000).",
      f"- Spearman ρ of method TTFT between GPUs ({len(both)} settings): {rho_ttft:.2f}.",
      f"- Base TTFT 5080 / 5070 Ti: {base['pc1_ttft']:.1f} / {base['pc2_ttft']:.1f} ms (5080 {100 * (1 - base['pc1_ttft'] / base['pc2_ttft']):.0f}% faster); compressed settings where 5070 Ti is faster: {sum(r['pc2_ttft'] < r['pc1_ttft'] for r in both)} of {len(both)}.",
      f"- Base energy 5080 / 5070 Ti: {base['pc1_energy']:.1f} / {base['pc2_energy']:.1f} J; max VRAM difference {max(abs(r['pc1_vram'] - r['pc2_vram']) for r in rows if r['pc1_vram'] and r['pc2_vram']):.2f} GB.",
      "- All accuracy on both GPUs uses the same settings: max_new_tokens 16, FP16 throughout, CDPruner fix variant (PC2 GQA/POPE/MME re-measured 2026-10-26, results_pc2_accuracy)."]
open(f"{OUT}/table_cross.md", "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L))

# -*- coding: utf-8 -*-
"""IVC 투고본 데이터 그림 2–4 (2026-10-05 v3). 최근(2025) VLM 효율 논문 그림 관행에 맞춘 matplotlib 스타일:
   옅은 격자, 짧은 바깥 눈금, 얇은 테두리, 테두리 없는 범례, 패널 제목 = 벤치마크/가지 이름, 기준 모델 = 회색 점선 + 라벨.
   참고: CDPruner(2506.10967) Fig. 4, FastVLM(2412.13303) Fig. 3, DART(2502.11494) Fig. 5, VisPruner(2412.01818) Fig. 2.
   무채색(사용자 지시): 검정·회색 명도, 찬/빈 표식, 실선/점선. 설명은 draft/figures/captions.md.
   입력: main_survey/taxonomy_counts.csv, bench/results_cross/table_cross.csv.  출력: draft/figures/fig{2,3,4}_*.{pdf,png}
   실행: python make_figures.py"""
import csv, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = "draft/figures"; os.makedirs(OUT, exist_ok=True)
K, D, M, L, G = "#111111", "#4a4a4a", "#8c8c8c", "#c8c8c8", "#e6e6e6"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman"], "mathtext.fontset": "stix",
    "font.size": 8, "axes.titlesize": 9.5, "axes.labelsize": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.edgecolor": D, "axes.linewidth": 0.6, "axes.grid": True, "grid.color": G, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.color": D, "ytick.color": D, "axes.labelcolor": K, "lines.linewidth": 1.2, "lines.markersize": 5,
    "legend.frameon": False, "legend.handlelength": 2.2, "savefig.dpi": 600, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42})
W2 = 7.16   # 2단 폭(in) ≈ 190 mm
def save(fig, name):
    for ext in ("pdf", "png"): fig.savefig(f"{OUT}/{name}.{ext}")
    plt.close(fig); print("saved", f"{OUT}/{name}.pdf/.png")
def refline(ax, y, label, x_right):
    ax.axhline(y, color=M, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.text(x_right, y, label, ha="right", va="bottom", fontsize=7.5, color=D)

T = list(csv.DictReader(open("main_survey/taxonomy_counts.csv", encoding="utf-8-sig")))
TV = {(r["branch"], r["kind"]): r for r in T if r["pool"] != "효율 풀"}
X = list(csv.DictReader(open("bench/results_cross/table_cross.csv", encoding="utf-8")))
fl = lambda v: float(v) if v not in (None, "", "None") else None

# ── Fig. 2 (v4, 2026-10-14 리뷰 Minor): 상대 성장(2026/2024)과 95% CI(Katz), 로그 축 하나 — 패널마다 y축이 달랐던 v3 대체 ──
import json as _json
NN = _json.load(open("draft/numbers/paper_numbers.json", encoding="utf-8"))
NAMES = [("4.1", "Design"), ("4.2", "Training"), ("4.3", "Compression"), ("4.4", "Execution"), ("4.5", "Deployment"), ("4.6", "Measurement")]
SHORT = {"Compression": "Compress.", "Deployment": "Deploy.", "Measurement": "Measure."}
fig, axs = plt.subplots(1, 2, figsize=(W2, 2.3), sharey=True)
for ax, (pk, ttl) in zip(axs, (("vlm", f"All VLM papers (n = {NN['corpus.vlm']:,})"), ("pool", f"Efficiency-oriented papers (n = {NN['corpus.pool']:,})"))):
    for j, (kind, off, mfc, lab) in enumerate((("loose", -0.13, K, "Loose (term appears)"), ("strict", 0.13, "white", "Strict (Section 3.2)"))):
        xs, ys, lo, hi, sig = [], [], [], [], []
        for i, (b, nm) in enumerate(NAMES):
            k = f"trend.{pk}.{b}.{kind}"; g = float(NN[f"{k}.rel_growth"])
            xs.append(i + off); ys.append(g); lo.append(g - NN[f"{k}.rg_lo"]); hi.append(NN[f"{k}.rg_hi"] - g); sig.append(NN[f"{k}.sig_bonf"] == "True")
        ax.errorbar(xs, ys, yerr=[lo, hi], fmt="none", ecolor=D, elinewidth=0.8, capsize=2, zorder=2)
        ax.scatter(xs, ys, s=22, marker="o", facecolor=mfc, edgecolor=K, linewidth=0.9, zorder=3, label=lab)
        for x, y, sg, h in zip(xs, ys, sig, hi):
            if sg: ax.text(x, y + h, "*", ha="center", va="bottom", fontsize=9, color=K)
    ax.axhline(1, color=M, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.set_yscale("log"); ax.set_yticks([0.25, 0.5, 1, 2, 4, 8]); ax.set_yticklabels(["0.25", "0.5", "1", "2", "4", "8"]); ax.minorticks_off()
    ax.set_xticks(range(len(NAMES))); ax.set_xticklabels([b + "\n" + SHORT.get(nm, nm) for b, nm in NAMES], fontsize=7); ax.set_xlim(-0.6, len(NAMES) - 0.4); ax.set_title(ttl)
axs[0].set_ylabel("Relative growth, 2026 / 2024")
axs[0].legend(loc="lower right", handletextpad=0.3)
fig.tight_layout(w_pad=0.8); save(fig, "fig2_trends")

# ── Fig. 3: accuracy vs TTFT on RTX 5080 ──
MS = [("vispruner", "VisPruner", "o", True), ("cdpruner_fix", "CDPruner", "*", True), ("fastv", "FastV (layer 3)", "^", False), ("sparsevlm", "SparseVLM", "D", False), ("dart", "DART", "s", False)]
base = next(r for r in X if r["key"] == "base")
fig, axs = plt.subplots(1, 2, figsize=(W2, 2.55))
for ax, (k, title, yl) in zip(axs, (("pc1_gqa", "GQA", "Accuracy (%)"), ("pc1_pope", "POPE", "F1 score (%)"))):
    for key, lab, mk, enc in MS:
        rr = sorted([r for r in X if r["key"] == key], key=lambda r: float(r["n_vis"]))
        ax.plot([fl(r["pc1_ttft"]) for r in rr], [fl(r[k]) for r in rr], color=K if enc else D, ls="-" if enc else (0, (3, 2)), lw=1.0,
                marker=mk, ms=7 if mk == "*" else 4.8, mfc=K if enc else "white", mec=K if enc else D, mew=0.9, label=lab)
    # 2차 외부 심사 M4(10/28): 점수 없이 균등 간격으로 고른 토큰(128·64개; 두 번째 세션, 표 8)
    _ua = {n: _json.load(open(f"bench/results_pc1/uniform/acc_{s}/accuracy.json")) for n, s in ((128, "default"), (64, "r889"))}
    _uy = [100 * (_ua[n]["gqa"]["acc"] if k == "pc1_gqa" else _ua[n]["pope"]["f1"]) for n in (64, 128)]
    ax.plot([NN["meas.pc1.uniform.64.ttft_ms"], NN["meas.pc1.uniform.128.ttft_ms"]], _uy, color=M, ls=(0, (1, 1.5)), lw=1.0, marker="x", ms=5, mew=1.1, mec=M, label="Evenly spaced (no score)")
    ax.plot([fl(base["pc1_ttft"])], [fl(base[k])], marker="o", ms=4.8, mfc=M, mec=M, ls="none")
    ax.set_xlim(40, 112); refline(ax, fl(base[k]), "LLaVA-1.5-7B", fl(base["pc1_ttft"]) - 2.5)
    ax.set_title(title); ax.set_xlabel("Time to first token (ms)"); ax.set_ylabel(yl)
axs[1].legend(loc="lower right", ncol=1)
fig.tight_layout(w_pad=1.5); save(fig, "fig3_ttft_accuracy")

# ── Fig. 4: energy per sample (two GPUs) and peak memory ──
order = ["base", "vispruner", "cdpruner_fix", "fastv", "sparsevlm", "dart"]
LAB = {"base": "LLaVA-1.5-7B", "vispruner": "VisPruner", "cdpruner_fix": "CDPruner", "fastv": "FastV", "sparsevlm": "SparseVLM", "dart": "DART"}
rows = [r for m in order for r in sorted([r for r in X if r["key"] == m], key=lambda r: -float(r["n_vis"]))]
xt = [f"{LAB[r['key']]}\n{int(float(r['n_vis']))}" for r in rows]; x = list(range(len(rows))); w = 0.36
fig, (a1, a2) = plt.subplots(2, 1, figsize=(W2, 3.3), sharex=True, gridspec_kw=dict(height_ratios=[1.5, 1]))
a1.bar([v - w / 2 - 0.01 for v in x], [fl(r["pc1_energy"]) for r in rows], w, color=D, label="RTX 5080")
a1.bar([v + w / 2 + 0.01 for v in x], [fl(r["pc2_energy"]) for r in rows], w, color=L, label="RTX 5070 Ti")
a1.set_ylabel("Energy per sample (J)"); a1.grid(axis="x", visible=False); a1.tick_params(axis="x", length=0)
a1.legend(loc="upper right", ncol=2)
a2.bar(x, [fl(r["pc1_vram"]) for r in rows], 0.62, color=L)
a2.set_ylim(0, 18); a2.set_yticks([0, 4, 8, 12, 16]); a2.set_xticks(x); a2.set_xticklabels(xt, fontsize=7); a2.set_ylabel("Peak memory (GB)"); a2.grid(axis="x", visible=False)
refline(a2, 16, "16 GB", len(rows) - 0.5)
for _ax, _lab in ((a1, "(a)"), (a2, "(b)")): _ax.text(-0.07, 1.02, _lab, transform=_ax.transAxes, fontsize=9, fontweight="bold", va="bottom")   # 10/16: 캡션의 (a)(b) 와 맞춤
fig.tight_layout(h_pad=0.6); save(fig, "fig4_energy_memory")

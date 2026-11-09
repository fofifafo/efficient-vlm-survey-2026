# -*- coding: utf-8 -*-
"""3.4절 사양별 성장(실행 시점 4.4·학습 시점 4.2 엄격, VLM 논문 전체)과 새 그림 2(4패널). 새 판정 없음 — 이미 있는 결과 파일만 읽음.
   입력: main_survey/strict_sensitivity.csv(기준·문구 변형 3개·효율 풀), main_survey/exec_rule_sensitivity.json(넓은 어휘),
         main_survey/monthly_trend/{periods.json, monthly_trend.csv, quarterly_trend.csv}(같은 달·2025 대비·2026 1–6월·월별 계열),
         main_survey/robustness_stats.json(정밀도·재현율 보정), draft/numbers/paper_numbers.json(그림 2 상단 = 표 2).
   교차 확인: 기준 행이 세 파일에서 같은지, 2026 1–6월 Fisher p 가 paper_numbers(p_fisher_h1)와 같은지 — 다르면 멈춤.
   상대 성장 = 나중 비중 / 앞 비중, 95% CI = Katz 로그 방법(paper_numbers.py 와 같은 식), p = 양측 Fisher 정확 검정.
   출력: main_survey/spec_growth/spec_growth.{json,csv}, fig2_trends.{pdf,png}(본문 그림 2: (a)(b) 기존, (c) 월별, (d) 사양별).
   실행: python spec_growth.py"""
import ast, csv, json, math, os, sys, types
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
_st = ast.parse(open("strict_tags.py", encoding="utf-8").read()); _m = types.ModuleType("strict_tags")
exec(compile(ast.Module([n for n in _st.body if isinstance(n, ast.FunctionDef) and n.name == "fisher_exact"], []), "strict_tags.py(fisher_exact)", "exec"), _m.__dict__)
fisher = _m.fisher_exact   # strict_tags 를 그대로 import 하면 medical_taxonomy_counts.csv 를 다시 씀 → fisher_exact 만
OUT = "main_survey/spec_growth"; os.makedirs(OUT, exist_ok=True)
rd = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig")))
NN = json.load(open("draft/numbers/paper_numbers.json", encoding="utf-8"))
SS = {(r["corpus"], r["variant"], r["branch"]): r for r in rd("main_survey/strict_sensitivity.csv")}
EX = {(r["corpus"], r["rule"], r["kind"]): r for r in json.load(open("main_survey/exec_rule_sensitivity.json", encoding="utf-8"))["trend"]}
PJ = json.load(open("main_survey/monthly_trend/periods.json", encoding="utf-8"))["series"]
MT = rd("main_survey/monthly_trend/monthly_trend.csv"); QT = rd("main_survey/monthly_trend/quarterly_trend.csv")
RS = json.load(open("main_survey/robustness_stats.json", encoding="utf-8"))
NV = {y: NN[f"corpus.vlm_{y}"] for y in ("2024", "2025", "2026")}; NP = {y: NN[f"corpus.pool_{y}"] for y in ("2024", "2025", "2026")}

def comp(a, n1, c, n2):
    rr = (c / n2) / (a / n1); se = math.sqrt(1 / a - 1 / n1 + 1 / c - 1 / n2)
    return dict(k1=a, n1=n1, k2=c, n2=n2, s1=round(100 * a / n1, 2), s2=round(100 * c / n2, 2), growth=round(rr, 2),
                lo=round(rr * math.exp(-1.96 * se), 2), hi=round(rr * math.exp(1.96 * se), 2), p=float(fisher([[a, n1 - a], [c, n2 - c]])[1]))
def h1(b):   # 2026년 1–6월
    rows = [r for r in MT if (r["corpus"], r["branch"], r["kind"]) == ("vlm", b, "strict") and "2026-01" <= r["period"] <= "2026-06"]
    assert len(rows) == 6; return sum(int(r["k"]) for r in rows), sum(int(r["n"]) for r in rows)
per = lambda b, p: (PJ[f"vlm.{b}.strict"]["periods"][p]["k"], PJ[f"vlm.{b}.strict"]["periods"][p]["n"])

# 교차 확인
for b in ("4.2", "4.4"):
    r = SS["vlm", "base", b]; k24, n24 = per(b, "2024"); k26, n26 = per(b, "2026_jan_aug")
    assert (int(r["n24"]), int(r["n26"])) == (k24, k26) and (n24, n26) == (NV["2024"], NV["2026"]), b
assert (EX["vlm", "base", "strict"]["n24"], EX["vlm", "base", "strict"]["n26"]) == (int(SS["vlm", "base", "4.4"]["n24"]), int(SS["vlm", "base", "4.4"]["n26"]))
for b in ("4.2", "4.4"):
    k, n = h1(b); p = fisher([[int(SS["vlm", "base", b]["n24"]), NV["2024"] - int(SS["vlm", "base", b]["n24"])], [k, n - k]])[1]
    assert abs(p / float(NN[f"trend.vlm.{b}.strict.p_fisher_h1"]) - 1) < 1e-6, (b, p)
print("check: base rows agree across strict_sensitivity / exec_rule_sensitivity / periods.json; Jan–Jun p equals paper_numbers")

SPEC = [   # (키, 영문 라벨, 한글 라벨, 4.4, 4.2)
    ("base", "Strict rule, 2026 vs 2024 (Table 2)", "엄격 규칙, 2026 대 2024(표 2)",
     lambda b: comp(int(SS["vlm", "base", b]["n24"]), NV["2024"], int(SS["vlm", "base", b]["n26"]), NV["2026"])),
    ("broad", "Broader execution vocabulary", "넓은 실행 어휘",
     lambda b: comp(EX["vlm", "broad", "strict"]["n24"], NV["2024"], EX["vlm", "broad", "strict"]["n26"], NV["2026"]) if b == "4.4" else None),
    ("v3", "Verbs propose, present, introduce", "동사 propose·present·introduce 만",
     lambda b: comp(int(SS["vlm", "v3", b]["n24"]), NV["2024"], int(SS["vlm", "v3", b]["n26"]), NV["2026"])),
    ("vwe", "Subject \u201cwe\u201d only", "주어 \"we\" 만",
     lambda b: comp(int(SS["vlm", "vwe", b]["n24"]), NV["2024"], int(SS["vlm", "vwe", b]["n26"]), NV["2026"])),
    ("vno_title", "Without title matches", "제목 일치 제외",
     lambda b: comp(int(SS["vlm", "vno_title", b]["n24"]), NV["2024"], int(SS["vlm", "vno_title", b]["n26"]), NV["2026"])),
    ("same_months", "Same months (Jan\u2013Aug)", "같은 달(1–8월)",
     lambda b: comp(*per(b, "2024_jan_aug"), *per(b, "2026_jan_aug"))),
    ("h1", "2026 restricted to Jan\u2013Jun", "2026년을 1–6월로 한정",
     lambda b: comp(*per(b, "2024"), *h1(b))),
    ("y25", "2026 vs 2025", "2026 대 2025",
     lambda b: comp(*per(b, "2025"), *per(b, "2026_jan_aug"))),
    ("pool", "Within the efficiency pool", "효율 풀 안",
     lambda b: comp(int(SS["pool", "base", b]["n24"]), NP["2024"], int(SS["pool", "base", b]["n26"]), NP["2026"])),
    ("corrected", "Corrected for precision and recall", "정밀도·재현율 보정",
     lambda b: dict(growth=RS["growth_exec_corrected_point"], lo=RS["growth_exec_corrected_ci"][0], hi=RS["growth_exec_corrected_ci"][1], p=None) if b == "4.4" else None),
]
R = [dict(key=k, label=en, label_ko=ko, exec=f("4.4"), train=f("4.2")) for k, en, ko, f in SPEC]
assert R[0]["exec"]["growth"] == float(NN["trend.vlm.4.4.strict.rel_growth"]) and R[0]["train"]["growth"] == float(NN["trend.vlm.4.2.strict.rel_growth"])
assert R[8]["exec"]["growth"] == float(NN["trend.pool.4.4.strict.rel_growth"]) and R[1]["exec"]["growth"] == 1.77
json.dump(dict(note="VLM 논문 전체(효율 풀 행 제외)의 엄격 비중. 상대 성장 = 나중/앞, Katz 95% CI, 양측 Fisher p. 보정 행은 robustness_stats.json(부트스트랩).",
               corpus=dict(vlm=NV, pool=NP), rows=R), open(f"{OUT}/spec_growth.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(f"{OUT}/spec_growth.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["spec", "branch", "k_before", "n_before", "k_after", "n_after", "share_before", "share_after", "growth", "ci_lo", "ci_hi", "p_fisher"])
    for r in R:
        for b, v in (("4.4", r["exec"]), ("4.2", r["train"])):
            if v: w.writerow([r["key"], b, v.get("k1", ""), v.get("n1", ""), v.get("k2", ""), v.get("n2", ""), v.get("s1", ""), v.get("s2", ""), v["growth"], v["lo"], v["hi"], "" if v["p"] is None else f"{v['p']:.2e}"])
for r in R:
    e, t = r["exec"], r["train"]
    print(f"{r['label']:<38} exec ×{e['growth']} ({e['lo']}–{e['hi']}) p={e['p'] if e['p'] is None else format(e['p'], '.1e')}"
          + (f" | train ×{t['growth']} ({t['lo']}–{t['hi']}) p={t['p']:.1e}" if t else ""))

# ── 그림 2: (a)(b) 표 2 의 상대 성장(make_figures.py 와 같은 코드), (c) 월별 실행 엄격 비중, (d) 사양별 성장 ──
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
for fp in ("C:/Windows/Fonts/times.ttf", "C:/Windows/Fonts/timesbd.ttf"):
    if os.path.exists(fp): font_manager.fontManager.addfont(fp)
K, D, M, L, G = "#111111", "#4a4a4a", "#8c8c8c", "#c8c8c8", "#e6e6e6"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman"], "mathtext.fontset": "stix",
    "font.size": 8, "axes.titlesize": 9.5, "axes.labelsize": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.edgecolor": D, "axes.linewidth": 0.6, "axes.grid": True, "grid.color": G, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.color": D, "ytick.color": D, "axes.labelcolor": K, "lines.linewidth": 1.2, "lines.markersize": 5,
    "legend.frameon": False, "legend.handlelength": 2.2, "savefig.dpi": 600, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42})
W2 = 7.16
fig = plt.figure(figsize=(W2, 5.0))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], width_ratios=[1, 1], hspace=0.55, wspace=0.08)
NAMES = [("4.1", "Design"), ("4.2", "Training"), ("4.3", "Compression"), ("4.4", "Execution"), ("4.5", "Deployment"), ("4.6", "Measurement")]
SHORT = {"Compression": "Compress.", "Deployment": "Deploy.", "Measurement": "Measure."}
a0 = fig.add_subplot(gs[0, 0]); a1 = fig.add_subplot(gs[0, 1], sharey=a0)
for ax, (pk, ttl) in zip((a0, a1), (("vlm", f"(a) All VLM papers (n = {NN['corpus.vlm']:,})"), ("pool", f"(b) Efficiency-oriented papers (n = {NN['corpus.pool']:,})"))):
    for kind, off, mfc, lab in (("loose", -0.13, K, "Loose (term appears)"), ("strict", 0.13, "white", "Strict (Section 3.2)")):
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
    ax.set_xticks(range(len(NAMES))); ax.set_xticklabels([b + "\n" + SHORT.get(nm, nm) for b, nm in NAMES], fontsize=7); ax.set_xlim(-0.6, len(NAMES) - 0.4)
    ax.set_title(ttl, loc="left")
plt.setp(a1.get_yticklabels(), visible=False)
a0.set_ylabel("Relative growth, 2026 / 2024"); a0.legend(loc="lower right", handletextpad=0.3)

# (c) 월별 — monthly_trend.py 그림 S1(a)와 같은 그리기
gs2 = gs[1, :].subgridspec(1, 2, width_ratios=[1.0, 0.72], wspace=1.0)
a2 = fig.add_subplot(gs2[0, 0]); a3 = fig.add_subplot(gs2[0, 1])
MONTHS = sorted({r["period"] for r in MT}); mi = {m: i for i, m in enumerate(MONTHS)}
qx = lambda q: 3 * (int(q[-1]) - 1) + 12 * (int(q[:4]) - 2024) + (1.0 if q != "2026Q3" else 0.5)
mr = [r for r in MT if (r["corpus"], r["branch"], r["kind"]) == ("vlm", "4.4", "strict")]
qr = [r for r in QT if (r["corpus"], r["branch"], r["kind"]) == ("vlm", "4.4", "strict")]
a2.scatter([mi[r["period"]] for r in mr], [float(r["pct"]) for r in mr], s=8, facecolor="none", edgecolor=M, linewidth=0.7, zorder=2, label="Month")
xs = [qx(r["period"]) for r in qr]
a2.fill_between(xs, [float(r["lo"]) for r in qr], [float(r["hi"]) for r in qr], color=G, lw=0, zorder=1, label="Quarter, 95% CI")
a2.plot(xs, [float(r["pct"]) for r in qr], color=K, lw=1.0, marker="s", ms=2.8, zorder=3, label="Quarter")
SPAN = {"2024_jan_aug": (0, 7), "2024_sep_dec": (8, 11), "2025": (12, 23), "2026_jan_aug": (24, 31)}
for n, (x0, x1) in SPAN.items():
    v = PJ["vlm.4.4.strict"]["periods"][n]["pct"]; a2.plot([x0 - 0.4, x1 + 0.4], [v] * 2, color=D, lw=0.9, ls=(0, (4, 2)), zorder=4)
t = [i for i, m in enumerate(MONTHS) if m[5:7] in ("01", "07")]
a2.set_xticks(t); a2.set_xticklabels([MONTHS[i] for i in t], fontsize=7); a2.set_xlim(-0.8, len(MONTHS) - 0.2); a2.set_ylim(bottom=0)
a2.set_ylabel("Share of VLM papers (%)"); a2.set_title("(c) Execution-time methods (strict) by month", loc="left"); a2.legend(loc="lower right", fontsize=7, handletextpad=0.3)

# (d) 사양별 상대 성장 — 실행(검은 점)·학습(빈 점)
ys = list(range(len(R)))[::-1]
for r, y in zip(R, ys):
    for v, off, mfc in ((r["exec"], 0.14, K), (r["train"], -0.14, "white")):
        if not v: continue
        a3.plot([v["lo"], v["hi"]], [y + off] * 2, color=D, lw=0.8, zorder=2)
        a3.scatter([v["growth"]], [y + off], s=18, facecolor=mfc, edgecolor=K, linewidth=0.9, zorder=3)
a3.axvline(1, color=M, lw=0.8, ls=(0, (4, 3)), zorder=1)
a3.set_xscale("log"); a3.set_xticks([0.25, 0.5, 1, 2, 4, 8, 16]); a3.set_xticklabels(["0.25", "0.5", "1", "2", "4", "8", "16"]); a3.minorticks_off()
a3.set_xlim(0.22, 20); a3.set_yticks(ys); a3.set_yticklabels([r["label"] for r in R], fontsize=6.8); a3.set_ylim(-0.6, len(R) + 0.45)
a3.grid(axis="y", visible=False); a3.set_xlabel("Relative growth of the strict share")
a3.set_title("(d) Robustness across specifications", loc="left")
a3.scatter([], [], s=18, facecolor=K, edgecolor=K, label="Execution"); a3.scatter([], [], s=18, facecolor="white", edgecolor=K, label="Training")
a3.legend(loc="upper center", ncol=2, fontsize=7, handletextpad=0.1, borderaxespad=0.15, columnspacing=1.0)
for ext in ("pdf", "png"): fig.savefig(f"{OUT}/fig2_trends.{ext}")
print("saved", f"{OUT}/fig2_trends.pdf/.png")

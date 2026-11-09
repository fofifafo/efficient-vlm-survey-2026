# -*- coding: utf-8 -*-
"""실행 시점(4.4) 엄격 비율의 월별·분기별 추이(보충자료 그림 후보). 새 판정 없음 — 코퍼스와 기존 규칙만 사용.
   규칙은 main_taxonomy.py 를 그대로 씀: 그 파일에서 'def analyse(' 앞부분(규칙 정의 + 코퍼스 로드 + core·pool)만 실행하고, 결과 파일은 쓰지 않는다.
   먼저 연도 합계(2024·2025·2026)가 main_survey/taxonomy_counts.csv 의 24행 모두와 같은지 확인하고, 다르면 멈춘다.
   기간 비교의 Fisher 검정은 사후·서술용(보정 없음). 구간은 Wilson 95%.
   실행: python a_monthly_trend.py --root <VLM-Survey 폴더> --out <출력 폴더>
   출력: monthly_trend.csv, quarterly_trend.csv, periods.json, fig_s_monthly_exec.{pdf,png}, fig_s_quarterly_branches.{pdf,png}"""
import argparse, csv, json, math, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
ROOT, OUT = os.path.abspath(a.root), os.path.abspath(a.out); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, ROOT)
import ast, types
_st = ast.parse(open(os.path.join(ROOT, "strict_tags.py"), encoding="utf-8").read()); _m = types.ModuleType("strict_tags")
exec(compile(ast.Module([n for n in _st.body if isinstance(n, ast.FunctionDef) and n.name == "fisher_exact"], []), "strict_tags.py(fisher_exact)", "exec"), _m.__dict__)
sys.modules["strict_tags"] = _m   # strict_tags 를 그대로 import 하면 medical_taxonomy 가 실행돼 medical_taxonomy_counts.csv 를 다시 씀 → fisher_exact 만 가져옴
SRC = open(os.path.join(ROOT, "main_taxonomy.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(ROOT, "main_taxonomy.py"), "__name__": "taxonomy_rules"}
exec(compile(SRC[:SRC.index("def analyse(")], "main_taxonomy.py(head)", "exec"), ns)   # chdir(ROOT) 포함
RX, SO, fisher = ns["RX"], ns["STRICT_OVERRIDE"], ns["fisher_exact"]
CORP = {"vlm": ns["core"], "pool": ns["pool"]}
LAB = {r[0]: r[1] for r in RX}

def hits(P, b, kind):   # main_taxonomy.analyse() 와 같은 정의
    _, _, loose, strict, _ = next(r for r in RX if r[0] == b)
    if kind == "loose": return {p["id"] for p in P if loose.search(p["t"])}
    if b in SO: return {p["id"] for p in P if strict.search(p["t"])}
    return {p["id"] for p in P if strict.search(p["t"]) or loose.search(p["title"])}
H = {(c, r[0], k): hits(P, r[0], k) for c, P in CORP.items() for r in RX for k in ("loose", "strict")}

# 1) 연도 합계 = taxonomy_counts.csv
yr = lambda p: p["date"][:4]
bad = 0
for r in csv.DictReader(open(os.path.join(ROOT, "main_survey/taxonomy_counts.csv"), encoding="utf-8-sig")):
    c = "pool" if r["pool"] == "효율 풀" else "vlm"; ids = H[c, r["branch"], r["kind"]]
    got = [sum(1 for p in CORP[c] if p["id"] in ids and yr(p) == y) for y in ("2024", "2025", "2026")]
    exp = [int(r["n24"]), int(r["n25"]), int(r["n26"])]
    if got != exp: bad += 1; print("MISMATCH", c, r["branch"], r["kind"], got, exp)
assert bad == 0, f"{bad} rows differ from taxonomy_counts.csv — stop"
print("check: yearly counts equal taxonomy_counts.csv (24 rows)")

def wilson(k, n, z=1.959964):
    if n == 0: return float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)
MONTHS = sorted({p["date"][:7] for p in CORP["vlm"]})
assert MONTHS[0] == "2024-01" and MONTHS[-1] == "2026-08" and len(MONTHS) == 32, MONTHS
qof = lambda m: f"{m[:4]}Q{(int(m[5:7]) - 1) // 3 + 1}"
QUARTERS = sorted({qof(m) for m in MONTHS})

def table(keyf, keys, fname):
    rows = []
    for c, P in CORP.items():
        n = {k: 0 for k in keys}
        for p in P: n[keyf(p["date"][:7])] += 1
        for (cc, b, kind), ids in H.items():
            if cc != c: continue
            k_ = {k: 0 for k in keys}
            for p in P:
                if p["id"] in ids: k_[keyf(p["date"][:7])] += 1
            for k in keys:
                lo, hi = wilson(k_[k], n[k])
                rows.append(dict(corpus=c, branch=b, kind=kind, period=k, n=n[k], k=k_[k], pct=round(100 * k_[k] / n[k], 3), lo=round(lo, 3), hi=round(hi, 3)))
    with open(os.path.join(OUT, fname), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return rows
MT = table(lambda m: m, MONTHS, "monthly_trend.csv")
QT = table(qof, QUARTERS, "quarterly_trend.csv")

# 2) 기간 요약: 2024 1–8월 / 2024 9–12월 / 2025 / 2026 1–8월 (+ 2024 전체·2026 전체 = 표 2 와 같은 값)
PER = {"2024_jan_aug": lambda m: m[:4] == "2024" and m[5:7] <= "08", "2024_sep_dec": lambda m: m[:4] == "2024" and m[5:7] >= "09",
       "2025": lambda m: m[:4] == "2025", "2026_jan_aug": lambda m: m[:4] == "2026", "2024": lambda m: m[:4] == "2024"}
def per(c, b, kind, name):
    P = [p for p in CORP[c] if PER[name](p["date"][:7])]; k = sum(1 for p in P if p["id"] in H[c, b, kind])
    lo, hi = wilson(k, len(P)); return dict(k=k, n=len(P), pct=round(100 * k / len(P), 2), lo=round(lo, 2), hi=round(hi, 2))
def fish(c, b, kind, x, y):
    X, Y = per(c, b, kind, x), per(c, b, kind, y)
    return dict(compare=f"{x} vs {y}", ratio=round((Y["k"] / Y["n"]) / (X["k"] / X["n"]), 2) if X["k"] else None,   # 반올림 전 값으로
                p_fisher=float(fisher([[X["k"], X["n"] - X["k"]], [Y["k"], Y["n"] - Y["k"]]])[1]))
OUTJ = {"note": "기간 비교 Fisher 는 사후·서술용(다중 비교 보정 없음). Wilson 95% 구간.", "months": MONTHS, "series": {}}
for c in CORP:
    for b in LAB:
        for kind in ("loose", "strict"):
            OUTJ["series"][f"{c}.{b}.{kind}"] = dict(periods={n: per(c, b, kind, n) for n in PER},
                tests=[fish(c, b, kind, "2024_jan_aug", "2024_sep_dec"), fish(c, b, kind, "2024_sep_dec", "2025"), fish(c, b, kind, "2025", "2026_jan_aug"),
                       fish(c, b, kind, "2024_jan_aug", "2026_jan_aug"), fish(c, b, kind, "2024", "2026_jan_aug")])
json.dump(OUTJ, open(os.path.join(OUT, "periods.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for key in ("vlm.4.4.strict", "vlm.4.4.loose", "pool.4.4.strict"):
    s = OUTJ["series"][key]; print(key, {n: f"{v['k']}/{v['n']}={v['pct']}%" for n, v in s["periods"].items()})
    for t in s["tests"]: print("   ", t["compare"], "ratio", t["ratio"], "p", f"{t['p_fisher']:.2g}")

# 3) 그림 (무채색, make_figures.py 와 같은 스타일)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
for fp in ("C:/Windows/Fonts/times.ttf", "/mnt/c/Windows/Fonts/times.ttf", "C:/Windows/Fonts/timesbd.ttf", "/mnt/c/Windows/Fonts/timesbd.ttf"):
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
def save(fig, name):
    for ext in ("pdf", "png"): fig.savefig(os.path.join(OUT, f"{name}.{ext}"))
    plt.close(fig); print("saved", name)
mi = {m: i for i, m in enumerate(MONTHS)}
qx = lambda q: 3 * (int(q[-1]) - 1) + 12 * (int(q[:4]) - 2024) + (1.0 if q != "2026Q3" else 0.5)   # 분기 가운데 달(2026Q3 은 7–8월)
SPAN = {"2024_jan_aug": (0, 7), "2024_sep_dec": (8, 11), "2025": (12, 23), "2026_jan_aug": (24, 31)}
def xfmt(ax):
    t = [i for i, m in enumerate(MONTHS) if m[5:7] in ("01", "07")]
    ax.set_xticks(t); ax.set_xticklabels([MONTHS[i] for i in t]); ax.set_xlim(-0.8, len(MONTHS) - 0.2)
def panel(ax, c, b, kind, title):
    mr = [r for r in MT if (r["corpus"], r["branch"], r["kind"]) == (c, b, kind)]
    qr = [r for r in QT if (r["corpus"], r["branch"], r["kind"]) == (c, b, kind)]
    ax.scatter([mi[r["period"]] for r in mr], [r["pct"] for r in mr], s=9, facecolor="none", edgecolor=M, linewidth=0.7, zorder=2, label="Month")
    xs = [qx(r["period"]) for r in qr]
    ax.fill_between(xs, [r["lo"] for r in qr], [r["hi"] for r in qr], color=G, lw=0, zorder=1, label="Quarter, 95% CI")
    ax.plot(xs, [r["pct"] for r in qr], color=K, lw=1.0, marker="s", ms=3, zorder=3, label="Quarter")
    s = OUTJ["series"][f"{c}.{b}.{kind}"]["periods"]
    for n, (x0, x1) in SPAN.items(): ax.plot([x0 - 0.4, x1 + 0.4], [s[n]["pct"]] * 2, color=D, lw=0.9, ls=(0, (4, 2)), zorder=4)
    ax.set_title(title, loc="left"); ax.set_ylabel("Share of VLM papers (%)" if c == "vlm" else "Share of pool papers (%)"); ax.set_ylim(bottom=0)
fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(W2, 4.6), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1.3, 0.8]))
panel(a1, "vlm", "4.4", "strict", "(a) Execution-time methods, strict definition")
panel(a2, "vlm", "4.4", "loose", "(b) Execution-time vocabulary, loose definition")
a1.legend(loc="lower right", ncol=3)
nm = [next(r["n"] for r in MT if r["corpus"] == "vlm" and r["period"] == m and r["branch"] == "4.4" and r["kind"] == "strict") for m in MONTHS]
a3.bar(range(len(MONTHS)), nm, 0.7, color=L); a3.set_ylabel("VLM papers"); a3.set_title("(c) VLM papers per month", loc="left"); xfmt(a3)
fig.tight_layout(h_pad=0.6); save(fig, "fig_s_monthly_exec")
# 참고: 가지별 엄격 비율(분기, 전체 VLM)
BNAME = {"4.1": "Design", "4.2": "Training", "4.3": "Compression", "4.4": "Execution", "4.5": "Deployment (device run)", "4.6": "Measurement (quantity)"}
fig, axs = plt.subplots(2, 3, figsize=(W2, 3.6), sharex=True)
for ax, b in zip(axs.flat, LAB):
    qr = [r for r in QT if (r["corpus"], r["branch"], r["kind"]) == ("vlm", b, "strict")]; xs = [qx(r["period"]) for r in qr]
    ax.fill_between(xs, [r["lo"] for r in qr], [r["hi"] for r in qr], color=G, lw=0); ax.plot(xs, [r["pct"] for r in qr], color=K, lw=1.0, marker="s", ms=2.5)
    ax.set_title(f"{b} {BNAME[b]}", loc="left"); ax.set_ylim(bottom=0); xfmt(ax)
    for t in ax.get_xticklabels(): t.set_rotation(30); t.set_ha("right")
for ax in axs[:, 0]: ax.set_ylabel("Strict share (%)")
fig.tight_layout(); save(fig, "fig_s_quarterly_branches")
print("done", OUT)

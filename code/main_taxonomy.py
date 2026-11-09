# -*- coding: utf-8 -*-
"""분류체계 v2 — 의료 서베이에서 배운 규칙 적용 (2026-09-21).
   가지마다 느슨(용어 등장) / 엄격(제목 또는 제안 문장에 등장 = 실제 기여) 정의 쌍.
   연도별 점유율, 상대 성장률(2026/2024), 조건부 비율(엄격∩느슨/느슨), Fisher(2024 vs 2026, 전 검정 Bonferroni),
   Cochran–Armitage 3년 추세, 2026 1–6월 민감도. 모든 수치는 이 스크립트에서만 생성(즉석 계산 금지).
   실행: python main_taxonomy.py  → main_survey/taxonomy_counts.csv, main_survey/taxonomy_v2_trends.md"""
import re, os, sys, csv, math, collections
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ".")
from arxiv_scrape import extract_keywords, KW_CLUSTER, load_cache
from strict_tags import fisher_exact

PROP = r"(?:\bwe\b|this (?:paper|work|study))[^.]{0,40}?\b(?:propose|present|introduce|design|develop|build)[^.]{0,200}?"
# v2.1 (2026-10-14, 분류 검증 후 안 1): 4.3·4.5 규칙을 기준 문서(main_survey/SCREENING_CRITERIA.md)의 제외 항목대로 좁힘.
#   4.3: 모델 양자화만(벡터 양자화·양자화 토큰·코드북·행동 제외), 증류는 작은/압축 학생 문맥만, 희소화는 가중치·모델만.
#   4.5 엄격: 이름 있는 기기만('Pixel' 은 Google Pixel/Pixel 숫자만 — 'pixel-level' 오탐 제거, 'edge device' 는 기기 이름 아님), 단어 경계.
#   근거: main_survey/classval/try_rule_fix.py, 1차 평가자 판정(returned_평가자1.xlsx). 이전 규칙은 아래 주석(_OLD).
Q = r"(?<!vector )(?<!vector-)(?<!residual )(?<!product )quantiz(?![^.]{0,40}?(?:tokeniz|codebook|\btokens?\b|\baction))"
KD = r"(?:small|smaller|compact|lightweight|light-weight|tiny|compress|fewer parameters|\d+(?:\.\d+)?\s?[MB]\b)"   # 'efficient' 는 증류 자체를 꾸미는 경우가 많아 제외
DIST = rf"(?:knowledge distillation|teacher[- ]student)[^.]{{0,150}}{KD}|{KD}[^.]{{0,150}}(?:knowledge distillation|teacher[- ]student)"
SP = r"(?:weight|parameter|model|activation)[- ]sparsi|sparsif\w* (?:the )?(?:weights|model|parameters|LLM|network)|(?:N:M|structured|unstructured|semi-structured) sparsity"
NEW43 = (Q + r"|\bPTQ\b|\bQAT\b|\bINT[48]\b|W4A16|W8A8|W4A4|binariz|ternary|" + DIST +
         r"|low[- ]rank (?:compress|decompos|approximat|factoriz)|\bSVD\b|weight pruning|structured pruning|model pruning|" + SP)
DEV = r"(?:Jetson|Raspberry|Snapdragon|smartphones?|mobile phones?|iPhone|Orin|Google Pixel|Pixel \d|NPU|FPGA)\b"   # 기준: 이름 있는 기기 — 'edge device' 는 기기 이름이 아님
NEW45 = (rf"(?:on|using|with) (?:a |an |the |single )?(?:NVIDIA )?{DEV}|(?:deployed|run|runs|running) on (?:a |an |the )?(?:NVIDIA )?{DEV}")
BRANCHES = [
 ("4.1", "설계 시점 — 구조",          r"mixture[- ]of[- ]experts|\bMoE\b|early[- ]exit|layer skip|depth pruning|layer pruning|encoder[- ]free|lightweight (?:vision|visual) encoder|small(?:er)? (?:vision|visual) encoder|state space model|\bMamba\b|linear attention|efficient attention|\bQ[- ]?Former\b|resampler|perceiver"),
 ("4.2", "학습 시점 — PEFT·데이터",    r"\bLoRA\b|\bQLoRA\b|\bDoRA\b|low[- ]rank adapt|parameter[- ]efficient|\bPEFT\b|\badapters?\b|prompt tuning|prompt learning|data[- ]efficient|data selection|data curation"),
 ("4.3", "압축 시점 — 양자화·저랭크·증류", NEW43),
# _OLD 4.3: ("4.3", "압축 시점 — 양자화·저랭크·증류", r"quantiz|\bPTQ\b|\bQAT\b|\bINT[48]\b|W4A16|W8A8|W4A4|binariz|ternary|knowledge distillation|teacher[- ]student|low[- ]rank (?:compress|decompos|approximat|factoriz)|\bSVD\b|weight pruning|structured pruning|model pruning|sparsif"),
 ("4.4", "실행 시점 — 토큰·캐시·디코딩", r"(?:visual|vision|image|video) tokens? (?:prun|reduc|compress|merg|select)|token (?:pruning|reduction|compression|merging|selection)|KV[- ]cache|key[- ]value cache|prefill|speculative decoding|flash[- ]?attention|\bvLLM\b|paged attention|prefix cach|continuous batching"),
 ("4.5", "배포 시점 — 온디바이스·하드웨어", r"on[- ]device|edge device|edge deploy|Jetson|Raspberry|Snapdragon|smartphone|mobile phone|\biPhone\b|\bOrin\b|\bNPU\b|\bDSP\b|\bFPGA\b|hardware accelerator|energy consumption|power consumption|energy[- ]efficient|low[- ]power"),
 ("4.6", "측정 — 효율 지표",           r"latency|inference time|wall[- ]clock|throughput|tokens per second|\bTPS\b|\bTTFT\b|\bFLOPs\b|\bMACs\b|memory footprint|\bVRAM\b|power consumption|energy consumption"),
]
# 4.5 엄격 = 실제 기기에서 실행/측정 ; 4.6 엄격 = 초록에 단위 붙은 수치
STRICT_OVERRIDE = {
 "4.5": NEW45,
# _OLD 4.5: "4.5": r"(?:on|using|with) (?:a |an |the |single )?(?:NVIDIA )?(?:Jetson|Raspberry|Snapdragon|smartphone|mobile phone|iPhone|Orin|Pixel|NPU|FPGA|edge (?:GPU|device))|deployed on (?:a |an |the )?(?:Jetson|Raspberry|Snapdragon|smartphone|mobile|iPhone|Orin|edge|NPU|FPGA)|run(?:s|ning)? on (?:a |an |the )?(?:Jetson|Raspberry|Snapdragon|smartphone|mobile|iPhone|Orin|edge device|NPU|FPGA)",
 "4.6": r"\d+(?:\.\d+)?\s*(?:ms|milliseconds|seconds? per|GB|GiB|MB|[GTM]?FLOPs|MACs|fps|FPS|tokens?/s|tokens per second|TPS|W\b|watts?|J\b|joules?|mWh|mJ)\b|\d+(?:\.\d+)?\s?[x×]\s*(?:faster|speed-?up)|speed-?up of \d",
}
def strict_rx(b, loose):
    if b in STRICT_OVERRIDE: return re.compile(STRICT_OVERRIDE[b], re.I)
    return re.compile(PROP + "(?:" + loose + ")", re.I)
RX = [(b, lab, re.compile(loose, re.I), strict_rx(b, loose), re.compile(loose, re.I)) for b, lab, loose in BRANCHES]

def cochran_armitage(counts, totals, scores=(0, 1, 2)):
    N = sum(totals); R = sum(counts)
    if R == 0 or R == N: return float("nan"), float("nan")
    t = sum(s * c for s, c in zip(scores, counts)); e = R * sum(s * n for s, n in zip(scores, totals)) / N
    sbar = sum(s * n for s, n in zip(scores, totals)) / N
    var = R * (N - R) / N * sum(n * (s - sbar) ** 2 for s, n in zip(scores, totals)) / (N - 1)
    z = (t - e) / math.sqrt(var); return z, 2 * 0.5 * math.erfc(abs(z) / math.sqrt(2))

papers, _ = load_cache(); papers = list(papers.values())
for p in papers:
    p["kw"] = extract_keywords(f"{p['title']}\n{p['abstract']}"); p["t"] = p["title"] + ". " + p["abstract"]
CORE = {"mllm", "vision-language-model", "visual-instruction-tuning"}; EFF = {k for k, c in KW_CLUSTER.items() if c == "EFF"}
core = [p for p in papers if p["kw"] & CORE]; pool = [p for p in core if p["kw"] & EFF]
yr = lambda p: p["date"][:4]
def analyse(P, name):
    N = collections.Counter(yr(p) for p in P); N1 = collections.Counter(yr(p) for p in P if not (p["date"].startswith("2026") and p["date"][5:7] > "06"))
    rows = []; tests = []
    for b, lab, loose, strict, _ in RX:
        for kind, rx in (("loose", loose), ("strict", strict)):
            hit = [p for p in P if rx.search(p["t"]) and (kind == "loose" or (b in STRICT_OVERRIDE or loose.search(p["title"]) or rx.search(p["t"])))]
            if kind == "strict" and b not in STRICT_OVERRIDE:
                hit = [p for p in P if strict.search(p["t"]) or loose.search(p["title"])]
            c = collections.Counter(yr(p) for p in hit); c1 = collections.Counter(yr(p) for p in hit if not (p["date"].startswith("2026") and p["date"][5:7] > "06"))
            a, m, z_ = c["2024"], c["2025"], c["2026"]
            pf = fisher_exact([[a, N["2024"] - a], [z_, N["2026"] - z_]])[1]
            pf1 = fisher_exact([[a, N["2024"] - a], [c1["2026"], N1["2026"] - c1["2026"]]])[1]
            zt, pt = cochran_armitage([a, m, z_], [N["2024"], N["2025"], N["2026"]])
            s24, s25, s26 = 100 * a / N["2024"], 100 * m / N["2025"], 100 * z_ / N["2026"]
            rows.append(dict(pool=name, branch=b, label=lab, kind=kind, n=len(hit), n24=a, n25=m, n26=z_, s24=round(s24, 1), s25=round(s25, 1), s26=round(s26, 1),
                             delta_pp=round(s26 - s24, 1), rel_growth=round(s26 / s24, 2) if s24 else None, p_fisher=pf, p_fisher_h1=pf1, ca_z=round(zt, 2), p_trend=pt, ids=set(p["id"] for p in hit)))
            tests.append(pf)
    # 조건부 비율(엄격/느슨) 연도별
    for b, lab, loose, strict, _ in RX:
        L = [r for r in rows if r["branch"] == b and r["kind"] == "loose"][0]; S = [r for r in rows if r["branch"] == b and r["kind"] == "strict"][0]
        Lp = {y: [p for p in P if yr(p) == y and p["id"] in L["ids"]] for y in ("2024", "2025", "2026")}
        S["cond"] = {y: (round(100 * sum(1 for p in Lp[y] if p["id"] in S["ids"]) / len(Lp[y]), 0) if Lp[y] else None) for y in Lp}
    alpha = 0.05 / len(tests)
    for r in rows: r["sig_bonf"] = r["p_fisher"] < alpha; r["sig_h1"] = r["p_fisher_h1"] < alpha; r["sig_trend"] = r["p_trend"] < alpha
    return rows, N, alpha
out = []; md = ["# 분류체계 v2 추세표 (스크립트 생성, 2026-09-21)\n"]
for P, name in ((pool, "효율 풀"), (core, "VLM 전체")):
    rows, N, alpha = analyse(P, name); out += rows
    md.append(f"\n## {name}: 2024 {N['2024']} / 2025 {N['2025']} / 2026(1–8월) {N['2026']} 편, Bonferroni α = 0.05/{len(rows)} = {alpha:.4f}\n")
    md.append("| 가지 | 정의 | n | 2024% | 2025% | 2026% | Δpp | 상대성장 | 조건부(엄격/느슨) 24→26 | Fisher | 1–6월 | 추세 |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        cond = f"{r['cond']['2024']:.0f}%→{r['cond']['2026']:.0f}%" if r["kind"] == "strict" and r.get("cond") and r["cond"]["2024"] is not None else ""
        mark = lambda ok, p: ("**" if ok else "") + f"{p:.1e}" + ("**" if ok else "")
        md.append(f"| {r['branch']} {r['label']} | {r['kind']} | {r['n']} | {r['s24']} | {r['s25']} | {r['s26']} | {r['delta_pp']:+} | ×{r['rel_growth']} | {cond} | {mark(r['sig_bonf'], r['p_fisher'])} | {mark(r['sig_h1'], r['p_fisher_h1'])} | {mark(r['sig_trend'], r['p_trend'])} |")
os.makedirs("main_survey", exist_ok=True)
with open("main_survey/taxonomy_counts.csv", "w", newline="", encoding="utf-8-sig") as f:
    keys = [k for k in out[0].keys() if k not in ("ids", "cond")] + ["cond24", "cond26"]
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for r in out: w.writerow({**{k: r.get(k) for k in keys if k not in ("cond24", "cond26")}, "cond24": (r.get("cond") or {}).get("2024"), "cond26": (r.get("cond") or {}).get("2026")})
open("main_survey/taxonomy_v2_trends.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("\n".join(md))

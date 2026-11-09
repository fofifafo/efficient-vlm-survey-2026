# -*- coding: utf-8 -*-
"""논문 본문·표에 들어가는 모든 수치를 한 곳에서 생성한다 (2026-10-04).
   규칙: 본문에 쓰는 숫자는 이 스크립트 출력(draft/numbers/paper_numbers.json/.md)에서만 가져온다. 손으로 계산·복사 금지.
   출처
     §3   코퍼스·추세 : arxiv 캐시(load_cache) + main_survey/taxonomy_counts.csv (main_taxonomy.py 가 생성)
     §3.5 스크리닝   : screening_marks_export.csv (데스크 판정, 사용자 판정 기록)
     §4   매트릭스   : main_survey/matrix_4.{1..5}.csv (본문 정독 추출), 근거 등급 규칙은 build_review_app.py 와 동일
     §4.6 초록 감사  : 효율 풀 초록에 아래 AUDIT 정규식 적용 (v1 taxonomy.md §3-1 을 대체; 정의를 코드로 고정)
     §5   측정       : bench/results_pc1/table8.csv (PC1), bench/results_pc2*/ (PC2, 있으면)
   실행: python paper_numbers.py [--rerun-trends]   → draft/numbers/paper_numbers.{json,md}, draft/tables/table{2..8}.md"""
import argparse, csv, glob, json, os, re, statistics, subprocess, sys, collections
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ".")
ap = argparse.ArgumentParser(); ap.add_argument("--rerun-trends", action="store_true"); a = ap.parse_args()
N = {}            # key -> value
SRC = {}          # key -> 출처 설명
def put(k, v, src): N[k] = v; SRC[k] = src
DASH = lambda v: (v or "").strip() == "" or (v or "").strip().startswith("—") or (v or "").strip() in ("-", "–", "N/A")

# ───────────────────────── §3 코퍼스 ─────────────────────────
if a.rerun_trends or not os.path.exists("main_survey/taxonomy_counts.csv"):
    subprocess.run([sys.executable, "main_taxonomy.py"], check=True, stdout=subprocess.DEVNULL)
from arxiv_scrape import extract_keywords, KW_CLUSTER, load_cache
papers, _ = load_cache(); papers = list(papers.values())
for p in papers: p["kw"] = extract_keywords(f"{p['title']}\n{p['abstract']}")
CORE = {"mllm", "vision-language-model", "visual-instruction-tuning"}; EFF = {k for k, c in KW_CLUSTER.items() if c == "EFF"}
core = [p for p in papers if p["kw"] & CORE]; pool = [p for p in core if p["kw"] & EFF]
yc = lambda P: collections.Counter(p["date"][:4] for p in P)
import arxiv_scrape as _as
put("corpus.queries", len(_as.QUERIES), "arxiv_scrape.QUERIES"); put("corpus.date_from", str(_as.DATE_FROM), "arxiv_scrape.DATE_FROM"); put("corpus.date_to", str(_as.DATE_TO), "arxiv_scrape.DATE_TO")
put("corpus.eff_keywords", len(EFF) if "EFF" in dir() else None, "효율 키워드 군집 크기")
put("corpus.records", len(papers), "arxiv 캐시 고유 레코드")
put("corpus.date_min", min(p["date"][:10] for p in papers), "arxiv 캐시"); put("corpus.date_max", max(p["date"][:10] for p in papers), "arxiv 캐시")
put("corpus.vlm", len(core), "제목·초록 CORE 키워드"); put("corpus.pool", len(pool), "CORE ∩ EFF 키워드")
for y, c in sorted(yc(pool).items()): put(f"corpus.pool_{y}", c, "효율 풀 연도별")
for y, c in sorted(yc(core).items()): put(f"corpus.vlm_{y}", c, "VLM 전체 연도별")

T = list(csv.DictReader(open("main_survey/taxonomy_counts.csv", encoding="utf-8-sig")))
for r in T:
    pk = "pool" if r["pool"] == "효율 풀" else "vlm"; k = f"trend.{pk}.{r['branch']}.{r['kind']}"
    for f in ("n", "s24", "s25", "s26", "rel_growth", "p_fisher", "p_fisher_h1", "p_trend", "cond24", "cond26", "sig_bonf"):
        if r.get(f) not in (None, ""): put(f"{k}.{f}", r[f], "taxonomy_counts.csv")
put("trend.alpha_bonf", round(0.05 / 12, 4), "12 검정 Bonferroni")
# 두 코퍼스 24 검정 보정에서도 유의 결과 유지되는지, 'we propose' 문형 자체의 증가(기준율)
put("trend.alpha_bonf24", round(0.05 / 24, 4), "24 검정 Bonferroni")
_sig = [r for r in T if r.get("sig_bonf") == "True"]
put("trend.sig_hold_24", all(float(r["p_fisher"]) < 0.05 / 24 for r in _sig), f"12검정 유의 {len(_sig)}칸이 0.05/24 에서도 유의")
from main_taxonomy import PROP as _PROP
_prx = re.compile(_PROP, re.I)
_pc = collections.Counter(p["date"][:4] for p in core if _prx.search(p["title"] + ". " + p["abstract"])); _cy = yc(core)
put("trend.vlm.prop_any.s24", round(100 * _pc["2024"] / _cy["2024"], 1), "VLM 초록 중 제안 문형(main_taxonomy.PROP) 비율 2024")
put("trend.vlm.prop_any.s26", round(100 * _pc["2026"] / _cy["2026"], 1), "같은 비율 2026")
_pr = (_pc["2026"] / _cy["2026"]) / (_pc["2024"] / _cy["2024"])
put("trend.vlm.prop_any.rel_growth", round(_pr, 2), "제안 문형 상대성장")
put("trend.vlm.4.4.strict.rel_growth_adj", round(float(N["trend.vlm.4.4.strict.rel_growth"]) / _pr, 2), "실행 엄격 성장 ÷ 제안 문형 성장")
# 상대 성장의 95% 신뢰구간(Katz 로그 방법) — 표 2
import math as _m
for r in T:
    pk = "pool" if r["pool"] == "효율 풀" else "vlm"; k = f"trend.{pk}.{r['branch']}.{r['kind']}"
    a, c = int(r["n24"]), int(r["n26"]); n1, n2 = N[f"corpus.{pk}_2024"], N[f"corpus.{pk}_2026"]
    se = _m.sqrt(1 / a - 1 / n1 + 1 / c - 1 / n2); rr = (c / n2) / (a / n1)
    put(f"{k}.rg_lo", round(rr * _m.exp(-1.96 * se), 2), "Katz 95% CI"); put(f"{k}.rg_hi", round(rr * _m.exp(1.96 * se), 2), "Katz 95% CI")
    put(f"{k}.n24", a, "2024 건수")
put("trend.min_n24", min(int(r["n24"]) for r in T), "2024 칸 최소 건수")
# 엄격 정의 민감도(strict_sensitivity.py)
if os.path.exists("main_survey/strict_sensitivity.csv"):
    for r in csv.DictReader(open("main_survey/strict_sensitivity.csv", encoding="utf-8-sig")):
        k = f"sens.{r['corpus']}.{r['variant']}.{r['branch']}"; put(f"{k}.rel_growth", float(r["rel_growth"]), "strict_sensitivity.csv"); put(f"{k}.sig", r["sig_bonf"] == "True", "같음")
    _sv = ("v3", "vwe", "vno_title")
    put("sens.same_conclusions", all(N[f"sens.vlm.{v}.4.4.sig"] and N[f"sens.vlm.{v}.4.2.sig"] and N[f"sens.pool.{v}.4.2.sig"] and not N[f"sens.pool.{v}.4.4.sig"]
                                      and not any(N[f"sens.{c}.{v}.{b}.sig"] for c in ("pool", "vlm") for b in ("4.1", "4.3")) for v in _sv), "세 변형 모두 같은 유의 패턴")

# ───────────────────────── §3.5 스크리닝 ─────────────────────────
S = list(csv.DictReader(open("screening_marks_export.csv", encoding="utf-8-sig")))
put("screen.cards", len(S), "데스크 카드 수(가지 중복 포함)"); put("screen.cards_unique", len({r["id"] for r in S}), "고유 논문")
for m, c in collections.Counter(r["mark"] for r in S).items(): put(f"screen.mark_{m}", c, "데스크 판정")

# ───────────────────────── §4 매트릭스 ─────────────────────────
M = []
for f in sorted(glob.glob("main_survey/matrix_4.*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8-sig")): r["_b"] = os.path.basename(f)[7:10]; M.append(r)
# 등급 규칙 (2026-10-05): "저자가 자기 시스템에서 측정한 비용" = 속도/지연 또는 메모리. FLOPs 는 계산값이라 기본 제외(6장 (i) 주장과 일관).
# GRADE_COUNT_FLOPS=True 로 바꾸면 데스크(build_review_app.py) 규칙과 같아진다. 두 규칙의 집계는 모두 출력한다.
GRADE_COUNT_FLOPS = False   # 2026-10-05 사용자 결정(2번안): FLOPs 는 측정 비용으로 치지 않는다
def measured(r, flops=GRADE_COUNT_FLOPS): return any(not DASH(r[k]) for k in (("flops",) if flops else ()) + ("speed_latency", "memory"))
def grade(r, flops=GRADE_COUNT_FLOPS):  # A = 코드 + 측정 비용, B = 측정 비용만, C = 없음
    return "A" if (r["code"].strip() and measured(r, flops)) else ("B" if measured(r, flops) else "C")
for r in M: r["_g"] = grade(r); r["_g_flops"] = grade(r, True)
put("matrix.grade_rule", "time or memory (FLOPs excluded)" if not GRADE_COUNT_FLOPS else "FLOPs, time or memory", "GRADE_COUNT_FLOPS")
for g in "ABC": put(f"matrix.grade_{g}_if_flops_counted", sum(r["_g_flops"] == g for r in M), "FLOPs 포함 규칙(데스크)")
put("matrix.grade_changed_by_flops", ", ".join(f"{r['name']} ({r['_b']}) {r['_g_flops']}→{r['_g']}" for r in M if r["_g"] != r["_g_flops"]), "규칙 차이로 등급이 바뀐 항목")
put("matrix.entries", len(M), "matrix_4.x.csv 행"); put("matrix.papers", len({r["id"] for r in M}), "고유 arXiv id")
for g in "ABC": put(f"matrix.grade_{g}", sum(r["_g"] == g for r in M), "등급 규칙(build_review_app.py)")
put("matrix.representatives", sum(r["mark"] == "star" for r in M), "mark=star")
put("matrix.representatives_papers", len({r["id"] for r in M if r["mark"] == "star"}), "대표 고유 논문")

REP_EXCEPTIONS = {}   # 10/16: FastV 원논문 표 4 실측 지연·메모리 확인 → A등급, 예외 해제(이전: 2026-10-05 FLOPs 만으로 보고 C 예외)
put("matrix.rep_non_A", sum(r["mark"] == "star" and r["_g"] != "A" and r["id"] not in REP_EXCEPTIONS for r in M), "대표인데 A 아님, 예외 제외(0 이어야 함)")
put("matrix.rep_exceptions", "; ".join(REP_EXCEPTIONS.values()), "대표=A 규칙의 예외")
put("matrix.flops_only_entries", sum(r["_g"] != r["_g_flops"] for r in M), "FLOPs 만 있어 등급이 내려간 항목 수")
for b in ("4.1", "4.2", "4.3", "4.4", "4.5"):
    R = [r for r in M if r["_b"] == b]; put(f"matrix.{b}.entries", len(R), "가지별")
    for g in "ABC": put(f"matrix.{b}.grade_{g}", sum(r["_g"] == g for r in R), "가지별 등급")
    put(f"matrix.{b}.representatives", sum(r["mark"] == "star" for r in R), "가지별 대표")
# 보고 실태
put("matrix.report_latency", sum(not DASH(r["speed_latency"]) for r in M), "speed_latency 칸 수치")
put("matrix.report_memory", sum(not DASH(r["memory"]) for r in M), "memory 칸 수치")
put("matrix.report_flops", sum(not DASH(r["flops"]) for r in M), "flops 칸 수치")
put("matrix.report_flops_only", sum(not DASH(r["flops"]) and DASH(r["speed_latency"]) and DASH(r["memory"]) for r in M), "FLOPs 만 있고 시간·메모리 없음")
ENERGY = re.compile(r"energy|joule|\bJ/|\bmJ\b|\bwatts?\b|\d\s?W\b|power consumption|battery", re.I)
put("matrix.report_energy", sum(bool(ENERGY.search(" ".join(r[k] for k in ("speed_latency", "memory", "note", "reduction")))) for r in M), "에너지·전력 언급 칸")
put("matrix.no_hardware", sum(DASH(r["hardware"]) for r in M), "hardware 칸 없음")
put("matrix.grade_A_no_hardware", sum(r["_g"] == "A" and DASH(r["hardware"]) for r in M), "A 등급 중 하드웨어 미명시")
put("matrix.grade_A_no_hardware_list", ", ".join(r["name"] for r in M if r["_g"] == "A" and DASH(r["hardware"])), "같음")
GPU = re.compile(r"\b(?:A100|H100|H800|A800|H20|A40|A6000|L40S?|V100|T4|RTX ?\d{4}(?: Ti)?|\d{4} ?Ti|4090|3090|Orin(?: Nano)?|Jetson \w+|Snapdragon[\w ]*|Dimensity \d+|Ascend \w+|Galaxy S\d+\w*|M[1-4](?: Max| Pro| Ultra)?)\b", re.I)
tok = [r for r in M if r["sub"].startswith("4.4.1")]
tok_time = [r for r in tok if not DASH(r["speed_latency"])]   # 10/16: 시간을 잰 논문의 GPU 만 센다(이전: 4.4.1 전체)
types = sorted({re.sub(r"\s+", " ", m.group(0).upper().replace("RTX", "RTX ")).replace("  ", " ") for r in tok_time for m in GPU.finditer(r["hardware"])})
put("matrix.4.4.1.time_no_hardware", sum(DASH(r["hardware"]) for r in tok_time), "4.4.1 지연 보고 중 하드웨어 미명시")
put("matrix.4.4.1.papers", len(tok), "4.4.1 토큰 압축 행");
put("matrix.4.4.1.report_time", sum(not DASH(r["speed_latency"]) for r in tok), "4.4.1 중 지연·속도 수치 보고")
put("matrix.4.4.1.flops_only", sum(not DASH(r["flops"]) and DASH(r["speed_latency"]) and DASH(r["memory"]) for r in tok), "4.4.1 중 FLOPs 만")
put("matrix.4.4.1.no_hardware", sum(DASH(r["hardware"]) for r in tok), "4.4.1 중 하드웨어 미명시")
vid = [r for r in tok if "비디오" in r["sub"]]
put("matrix.4.4.1.video", len(vid), "4.4.1 중 비디오"); put("matrix.4.4.1.video_time", sum(not DASH(r["speed_latency"]) for r in vid), "비디오 중 지연 보고")
for b in ("4.1", "4.2", "4.3", "4.4", "4.5"):
    R = [r for r in M if r["_b"] == b]
    put(f"matrix.{b}.report_time", sum(not DASH(r["speed_latency"]) for r in R), "가지별 지연·속도 보고"); put(f"matrix.{b}.report_memory", sum(not DASH(r["memory"]) for r in R), "가지별 메모리 보고")
    put(f"matrix.{b}.no_hardware", sum(DASH(r["hardware"]) for r in R), "가지별 하드웨어 미명시")
put("matrix.4.4.1.hardware_types", len(types), "하드웨어 이름 정규식"); put("matrix.4.4.1.hardware_list", ", ".join(types), "하드웨어 이름 정규식")

# ───────────────────────── §4.6 초록 감사 ─────────────────────────
AUDIT = {  # 정의 고정. 초록만 대상(본문 아님).
 "latency":    r"latency|inference time|inference speed|wall[- ]clock|response time|time[- ]to[- ]first[- ]token|\bTTFT\b",
 "device":     r"\b(?:Jetson|Raspberry Pi|Snapdragon|Dimensity|Orin|iPhone|Pixel \d|Galaxy|A100|H100|H800|A800|V100|A6000|RTX ?\d{4}|NPU|FPGA|smartphone|mobile phone)\b",
 "params":     r"\d+(?:\.\d+)?\s?(?:[BM]|billion|million)\s+(?:trainable\s+)?(?:parameters|params)|(?:number of|fewer|reduc\w*|trainable) parameters",
 "flops":      r"\b(?:[GTM]?FLOPs?|MACs)\b|floating[- ]point operations",
 "throughput": r"throughput|tokens? per second|tokens?/s\b|\bTPS\b|frames per second|\bFPS\b",
 "memory":     r"memory (?:footprint|usage|consumption|cost|overhead|requirement|saving|reduction)|\bVRAM\b|GPU memory|peak memory|KV[- ]cache (?:size|memory|footprint)",
 "energy":     r"energy (?:consumption|efficien|cost)|power consumption|\bwatts?\b|\bjoules?\b|battery",
}
AX = {k: re.compile(v, re.I) for k, v in AUDIT.items()}
cnt = collections.Counter(); per = []
for p in pool:
    hits = {k for k, rx in AX.items() if rx.search(p["abstract"])}
    for k in hits: cnt[k] += 1
    per.append(len(hits))
for k in AUDIT: put(f"audit.{k}", cnt[k], "효율 풀 초록 정규식"); put(f"audit.{k}_pct", round(100 * cnt[k] / len(pool), 1), "효율 풀 초록 정규식")
dist = collections.Counter(min(n, 3) for n in per)
for n, lab in ((0, "none"), (1, "one"), (2, "two"), (3, "three_plus")):
    put(f"audit.metrics_{lab}", dist[n], "초록 지표 개수 분포"); put(f"audit.metrics_{lab}_pct", round(100 * dist[n] / len(pool), 1), "초록 지표 개수 분포")
# 강건성(2026-10-12 검토): 위 규칙은 '지표 용어' 언급만 센다. 배율·감소율·단위가 붙은 숫자까지 효율 수치로 인정하는 넓은 규칙으로도 센다.
_N = r"\d+(?:\.\d+)?"
QTY = re.compile("|".join([
    rf"{_N}\s?(?:×|x|times)\s*(?:faster|speed|acceleration|higher throughput|fewer|smaller|less|reduction|compression|lower)",
    rf"(?:speed-?ups?|acceleration|faster)\s+(?:of|by|up to)?\s*(?:up to\s*)?{_N}\s?(?:×|x|%|times)",
    rf"{_N}\s?(?:×|x)\s+(?:speed-?up|inference)",
    rf"{_N}\s?%\s+(?:fewer|less|lower|reduction|of the (?:visual |vision |image )?tokens|tokens|FLOPs|memory|latency|parameters|computation|compute|faster|speed)",
    rf"(?:reduc\w+|cut\w*|sav\w+|prun\w+|compress\w*|remov\w+|decreas\w+|lower\w*)\b[^.]{{0,60}}?\bby\s+(?:up to\s+|over\s+|about\s+|nearly\s+)?{_N}\s?(?:%|×|x)",
    rf"{_N}\s?(?:ms|milliseconds?|seconds?|GB|GiB|MB|tokens?/s|FPS|fps|W|J|mJ)\b",
    rf"\b{_N}-?bit\b", rf"{_N}\s?(?:[BM]|billion|million)\s+(?:trainable\s+)?(?:parameters|params)",
    rf"{_N}\s?(?:G|T|M)?FLOPs", rf"only\s+{_N}\s?%\s+of",
]), re.I)
_none_both = sum(1 for p, n in zip(pool, per) if n == 0 and not QTY.search(p["abstract"]))
put("audit.qty_none", _none_both, "지표 용어도 없고 효율 수치(배율·%·단위)도 없는 초록"); put("audit.qty_none_pct", round(100 * _none_both / len(pool), 1), "같음, 비율")
os.makedirs("draft/numbers", exist_ok=True)   # 감사 패턴을 보충 자료에 싣기 위해 그대로 내보냄
json.dump({"metric_terms": AUDIT, "broader_quantity_rule": QTY.pattern, "scope": "abstracts of the 1,947-paper efficiency pool"}, open("draft/numbers/audit_patterns.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ───────────────────────── §5 측정 ─────────────────────────
def load_t8(path):
    if not os.path.exists(path): return []
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows:
        for k in ("n_vis", "ttft_ms", "total_ms", "peak_vram_gb", "energy_j", "gqa", "pope_f1", "textvqa", "mme_p"):
            r[k] = float(r[k]) if r.get(k) not in (None, "") else None
    return rows
P1 = load_t8("bench/results_pc1/table8.csv")
if P1:
    b = next(r for r in P1 if r["key"] == "base"); put("meas.pc1.base_ttft_ms", round(b["ttft_ms"], 1), "results_pc1"); put("meas.pc1.base_total_ms", round(b["total_ms"], 1), "results_pc1")
    put("meas.pc1.base_vram_gb", round(b["peak_vram_gb"], 2), "results_pc1"); put("meas.pc1.base_energy_j", round(b["energy_j"], 1), "results_pc1")
    for k in ("gqa", "pope_f1", "textvqa", "mme_p"): put(f"meas.pc1.base_{k}", round(b[k], 2), "results_pc1")
    C = [r for r in P1 if r["key"] not in ("base", "cdpruner")]   # 압축 방법(공개판 CDPruner 는 불안정 → 별도)
    sp = [b["ttft_ms"] / r["ttft_ms"] for r in C]; es = [b["energy_j"] / r["energy_j"] for r in C]; vs = [round(b["peak_vram_gb"], 2) - round(r["peak_vram_gb"], 2) for r in C]   # 11/6: 표 8 값끼리(Jetson 과 같은 규칙)
    put("meas.pc1.methods", len({r["key"] for r in C}), "압축 방법 수"); put("meas.pc1.settings", len(C), "방법×설정 수")
    put("meas.pc1.ttft_speedup_min", round(min(sp), 2), "base/TTFT"); put("meas.pc1.ttft_speedup_max", round(max(sp), 2), "base/TTFT")
    put("meas.pc1.energy_ratio_min", round(min(es), 2), "base/J"); put("meas.pc1.energy_ratio_max", round(max(es), 2), "base/J")
    put("meas.pc1.vram_saving_min_gb", round(min(vs), 2), "base−peak"); put("meas.pc1.vram_saving_max_gb", round(max(vs), 2), "base−peak")
    t64 = [r["ttft_ms"] for r in C if r["n_vis"] == 64]; put("meas.pc1.ttft64_min", round(min(t64), 1), "64 토큰 설정"); put("meas.pc1.ttft64_max", round(max(t64), 1), "64 토큰 설정")
    for r in P1:
        k = f"meas.pc1.{r['key']}.{int(r['n_vis'])}"
        for f in ("ttft_ms", "total_ms", "peak_vram_gb", "energy_j", "gqa", "pope_f1", "textvqa", "mme_p"):
            if r[f] is not None: put(f"{k}.{f}", round(r[f], 2 if f == "peak_vram_gb" else 1), "results_pc1")
        put(f"{k}.speedup", round(b["ttft_ms"] / r["ttft_ms"], 2), "base/TTFT")
        if r["gqa"] is not None:
            for f in ("gqa", "pope_f1", "textvqa", "mme_p"): put(f"{k}.d_{f}", round(r[f] - b[f], 1), "방법 − base")

# 5장 본문용 파생 수치
PUBLISHED_LLAVA15_7B = {"gqa": 62.0, "pope_f1": 85.9, "textvqa": 58.2, "mme_p": 1510.7}   # Liu et al., Improved Baselines (LLaVA-1.5) 보고치 — 인용값
if P1:
    for k, v in PUBLISHED_LLAVA15_7B.items(): put(f"pub.llava15_7b.{k}", v, "LLaVA-1.5 논문 보고치(인용)")
    put("meas.pc1.base_textvqa_minus_pub", round(b["textvqa"] - PUBLISHED_LLAVA15_7B["textvqa"], 1), "우리 − 보고치")
    main = {r["key"]: r for r in C if r["setting"] == "default"}; r64 = {r["key"]: r for r in C if r["setting"] == "r889"}
    dg = [b["gqa"] - r["gqa"] for r in main.values()]; put("meas.pc1.main_gqa_drop_min", round(min(dg), 1), "주 설정 GQA 하락"); put("meas.pc1.main_gqa_drop_max", round(max(dg), 1), "주 설정 GQA 하락")
    sv = [main[k]["ttft_ms"] - r64[k]["ttft_ms"] for k in main if k in r64]; put("meas.pc1.main_to64_saving_min_ms", round(min(sv)), "주 설정→64 토큰 TTFT 추가 절감"); put("meas.pc1.main_to64_saving_max_ms", round(max(sv)), "주 설정→64 토큰 TTFT 추가 절감")


# 교차 GPU (bench/make_table_cross.py 출력)
XC = "bench/results_cross/table_cross.csv"
if os.path.exists(XC):
    X = list(csv.DictReader(open(XC, encoding="utf-8")))
    fl = lambda v: float(v) if v not in (None, "", "None") else None
    xb = next(r for r in X if r["key"] == "base")
    put("cross.base_ttft_pc1", round(fl(xb["pc1_ttft"]), 1), "table_cross"); put("cross.base_ttft_pc2", round(fl(xb["pc2_ttft"]), 1), "table_cross")
    put("cross.base_energy_pc2", round(fl(xb["pc2_energy"]), 1), "table_cross")
    Y = [r for r in X if r["key"] != "base" and fl(r["pc2_ttft"]) and fl(r["pc1_ttft"])]
    put("cross.settings_both", len(Y), "두 GPU 모두 측정된 압축 설정"); put("cross.pc2_faster_count", sum(fl(r["pc2_ttft"]) < fl(r["pc1_ttft"]) for r in Y), "압축 설정 중 5070 Ti 가 더 빠른 수")
    sp2 = [fl(r["pc2_speedup"]) for r in Y]; put("cross.pc2_speedup_min", round(min(sp2), 2), "5070 Ti base/TTFT"); put("cross.pc2_speedup_max", round(max(sp2), 2), "5070 Ti base/TTFT")
    _e2 = [fl(xb["pc2_energy"]) / fl(r["pc2_energy"]) for r in Y if fl(r["pc2_energy"])]; put("cross.pc2_energy_ratio_max", round(max(_e2), 2), "5070 Ti base/J 최대(10/16: 초록 에너지 범위를 두 GPU 로)")
    for k in ("gqa", "pope", "tvqa", "mme"):
        d = [abs(fl(r[f"pc1_{k}"]) - fl(r[f"pc2_{k}"])) for r in X if fl(r[f"pc1_{k}"]) is not None and fl(r[f"pc2_{k}"]) is not None]
        put(f"cross.max_abs_diff_{k}", round(max(d), 2), f"PC1 vs PC2, {len(d)} 설정")
    put("cross.max_energy_diff_j", round(max(abs(fl(r["pc1_energy"]) - fl(r["pc2_energy"])) for r in X if fl(r["pc1_energy"]) and fl(r["pc2_energy"])), 1), "table_cross")
    put("cross.base_pc1_faster_pct", round(100 * (1 - fl(xb["pc1_ttft"]) / fl(xb["pc2_ttft"]))), "기준 모델 5080 이 빠른 비율")
    put("cross.max_vram_diff_gb", round(max(abs(fl(r["pc1_vram"]) - fl(r["pc2_vram"])) for r in X if fl(r["pc1_vram"]) and fl(r["pc2_vram"])), 2), "table_cross")
    rk = lambda v: [sorted(v).index(x) for x in v]
    a1, a2 = rk([fl(r["pc1_ttft"]) for r in Y]), rk([fl(r["pc2_ttft"]) for r in Y]); n = len(Y)
    put("cross.spearman_ttft", round(1 - 6 * sum((p - q) ** 2 for p, q in zip(a1, a2)) / (n * (n * n - 1)), 2), "방법 TTFT 순위 상관")

# 첫 토큰 프로파일(보충 표 S6; bench/results_pc{1,2}_profile) — 11/8: 5.3·5.5절의 GPU 시간 기준 가속. 표 S6 에 보이는 값(소수 첫째 자리)끼리 계산
PRF = {}
for _pc, _d in (("pc1", "bench/results_pc1_profile"), ("pc2", "bench/results_pc2_profile")):
    for _f in glob.glob(f"{_d}/*_*.json"):
        if "cdpruner_diag" in _f: continue
        _j = json.load(open(_f, encoding="utf-8")); PRF[_pc, _j["method"], _j["setting"]] = {c: round(_j[c], 1) for c in ("wall_ms", "gpu_busy_ms")}
if PRF:
    _ks = sorted({(m, s) for _, m, s in PRF if m != "base"})
    _g = {pc: {k: PRF[pc, "base", "default"]["gpu_busy_ms"] / PRF[(pc,) + k]["gpu_busy_ms"] for k in _ks} for pc in ("pc1", "pc2")}
    _w = {pc: {k: PRF[pc, "base", "default"]["wall_ms"] / PRF[(pc,) + k]["wall_ms"] for k in _ks} for pc in ("pc1", "pc2")}
    for pc in ("pc1", "pc2"):
        put(f"prof.{pc}.gpu_speedup_min", round(min(_g[pc].values()), 2), "표 S6 GPU 시간 base/방법 최소"); put(f"prof.{pc}.gpu_speedup_max", round(max(_g[pc].values()), 2), "같음 최대")
    _r = [_g["pc2"][k] / _g["pc1"][k] for k in _ks]
    put("prof.n_settings", len(_ks), "압축 설정 수"); put("prof.gpu_speedup_pc2_larger_count", sum(x > 1 for x in _r), "GPU 시간 가속이 5070 Ti 에서 더 큰 설정 수")
    put("prof.gpu_speedup_diff_max_pct", round(100 * (max(max(_r), 1 / min(_r)) - 1)), "GPU 시간 가속의 두 GPU 차 최대(robust.speedup_size_diff_max_pct 와 같은 식)")
    _kx = max(_ks, key=lambda k: max(_g["pc2"][k] / _g["pc1"][k], _g["pc1"][k] / _g["pc2"][k]))
    put("prof.gpu_speedup_diff_max_setting", "/".join(_kx), "그 설정"); put("prof.gpu_speedup_diff_max_pc1", round(_g["pc1"][_kx], 2), "그 설정 5080")
    put("prof.gpu_speedup_diff_max_pc2", round(_g["pc2"][_kx], 2), "그 설정 5070 Ti")
    put("prof.gpu_over_ttft_speedup_max", round(max(_g[pc][k] / _w[pc][k] for pc in ("pc1", "pc2") for k in _ks), 1), "같은 실행에서 GPU 시간 가속 / TTFT 가속 최대")

# ───────────────────────── §5.4 엣지 기기 (Jetson Orin Nano, 4비트 NF4; bench/results_jetson) ─────────────────────────
JR = "bench/results_jetson"
if os.path.exists(f"{JR}/base4/latency_default.json"):
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("score", "bench/score.py"); _sc = _iu.module_from_spec(_sp); _sp.loader.exec_module(_sc)
    # 11/5: 지연·에너지·메모리는 모두 화면 끈 상태(multi-user.target)의 값 — 원본·VisPruner 는 guioff_1105 재측정, CDPruner(fix) 는 11/4–5 측정. 정확도 예측은 화면과 무관해 기존 폴더.
    JG = f"{JR}/guioff_1105"
    JL = {"base": json.load(open(f"{JG}/base4/latency_default.json")), "vp128": json.load(open(f"{JG}/vispruner4/latency_default.json")),
          "vp64": json.load(open(f"{JG}/vispruner4/latency_r889.json")),
          "cd128": json.load(open(f"{JR}/cdpruner4_fix/latency_default.json")), "cd64": json.load(open(f"{JR}/cdpruner4_fix/latency_r889.json"))}
    JA = {"base": ("base4", "default", "base"), "vp128": ("vispruner4", "default", "vispruner"), "vp64": ("vispruner4", "r889", "vispruner"),
          "cd128": ("cdpruner4_fix", "default", "cdpruner_fix"), "cd64": ("cdpruner4_fix", "r889", "cdpruner_fix")}
    jb = JL["base"]
    for k, r in JL.items():
        put(f"jetson.{k}.ttft_ms", round(r["ttft_ms_median"], 1), f"{JR} 500×5 중앙값"); put(f"jetson.{k}.total_ms", round(r["total_ms_median"], 1), JR)
        put(f"jetson.{k}.energy_j", round(r["energy_j_per_sample"], 1), "VDD_IN 적분/샘플"); put(f"jetson.{k}.peak_alloc_gb", round(r["peak_alloc_gb"], 2), "torch 최대 할당")
        put(f"jetson.{k}.peak_sys_gb", round(r["peak_sys_used_gb"], 1), "MemTotal−MemAvailable 최대"); put(f"jetson.{k}.power_w", round(r["mean_power_w"], 1), "VDD_IN 평균")
        put(f"jetson.{k}.speedup", round(jb["ttft_ms_median"] / r["ttft_ms_median"], 2), "base/TTFT"); put(f"jetson.{k}.energy_ratio", round(jb["energy_j_per_sample"] / r["energy_j_per_sample"], 2), "base/에너지")
        m4, st, m16 = JA[k]
        p4 = {x["qid"]: x for x in map(json.loads, open(f"{JR}/{m4}/preds_gqa500_{st}.jsonl", encoding="utf-8"))}
        p16 = {str(x["qid"]): x for x in map(json.loads, open(f"bench/results_pc1/{m16}/acc_{st}/preds_gqa.jsonl", encoding="utf-8")) if str(x["qid"]) in p4}
        ok = lambda x: _sc.norm(x["pred"]) == _sc.norm(x["answer"])
        put(f"jetson.{k}.gqa500_4bit", round(100 * sum(map(ok, p4.values())) / len(p4), 1), "같은 500문항, score.py 규칙")
        put(f"jetson.{k}.gqa500_fp16_5080", round(100 * sum(map(ok, p16.values())) / len(p16), 1), "results_pc1 예측에서 같은 500문항")
        put(f"jetson.{k}.same_answer_pct", round(100 * sum(_sc.norm(p4[q]["pred"]) == _sc.norm(p16[q]["pred"]) for q in p4) / len(p4), 1), "문항별 답 일치")
    put("jetson.mem_total_gb", 7.4, "free -h Mem total (7.4 GiB)")
    _r2 = lambda k: round(JL[k]["peak_alloc_gb"], 2)   # 11/6: 표 11 에 보이는 값(소수 둘째 자리)끼리 빼서 본문 = 표 계산(원값 차 0.434 → 표로는 0.44)
    put("jetson.vram_saving_max_gb", round(_r2("base") - min(_r2(k) for k in ("vp128", "vp64")), 2), "base−VisPruner 최대 할당(표 11 값끼리)")
    put("jetson.vram_saving_max_all_gb", round(_r2("base") - min(_r2(k) for k in JL if k != "base"), 2), "base−(VisPruner·CDPruner) 최대 할당(표 11 값끼리)")
    put("jetson.peak_sys_max_gb", round(max(r["peak_sys_used_gb"] for r in JL.values()), 1), "모든 설정 시스템 메모리 최대")
    for t in ("128", "64"):
        put(f"jetson.cd_minus_vp_{t}_ms", round(JL[f"cd{t}"]["ttft_ms_median"] - JL[f"vp{t}"]["ttft_ms_median"]), "같은 조건 CDPruner(fix)−VisPruner TTFT")
        put(f"jetson.cd_minus_vp_{t}_acc", round(N[f"jetson.cd{t}.gqa500_4bit"] - N[f"jetson.vp{t}.gqa500_4bit"], 1), "GQA-500 4비트 정확도 차")
    # 11/8: 위 정확도 차의 짝지은 부트스트랩 95% 구간(5.2절 baseline_comparison.py 와 같은 방식: 문항 재표집 2,000회, 백분위)
    import numpy as _np
    _rng = _np.random.default_rng(20261028)
    for t, st in (("128", "default"), ("64", "r889")):
        _a, _b = ({x["qid"]: x for x in map(json.loads, open(f"{JR}/{m}/preds_gqa500_{st}.jsonl", encoding="utf-8"))} for m in ("cdpruner4_fix", "vispruner4"))
        assert sorted(_a) == sorted(_b)
        _dd = _np.array([ok(_a[q]) - ok(_b[q]) for q in sorted(_a)], float)
        _lo, _hi = _np.percentile([100 * _dd[_rng.integers(0, len(_dd), len(_dd))].mean() for _ in range(2000)], [2.5, 97.5])
        put(f"jetson.cd_minus_vp_{t}_acc_ci_lo", round(float(_lo), 1), "짝지은 부트스트랩 95% 하한"); put(f"jetson.cd_minus_vp_{t}_acc_ci_hi", round(float(_hi), 1), "같음 상한")
    # CDPruner 공개판(11/5, 100문항 1회, 메모리 감시가 끊음): 1초 간격 메모리 로그의 최저 가용 메모리·최대 스왑 증가
    _ml = [l.split() for l in open(f"{JR}/logs_cdpruner_1104/cdpruner_asis_short_mem.log", encoding="utf-8") if "avail=" in l]
    put("jetson.cd_asis.min_avail_gb", round(min(int(x[1].split("=")[1]) for x in _ml) / 1024, 2), "공개판 100문항 실행 중 최저 MemAvailable")
    put("jetson.cd_asis.max_swap_gb", round(max(int(x[2].split("=")[1].replace("+", "")) for x in _ml) / 1024, 1), "같은 실행 스왑 증가 최대")
    if os.path.exists(XC):  # 데스크톱 두 GPU 에서 두 encoder-side 방법(VisPruner, CDPruner fix)의 속도 향상 범위(5.4절 비교용)
        _enc = [fl(r[c]) for r in X if r["key"] in ("vispruner", "cdpruner_fix") for c in ("pc1_speedup", "pc2_speedup") if fl(r[c])]
        put("jetson.desk_enc_speedup_min", round(min(_enc), 2), "table_cross VisPruner·CDPruner(fix) 두 GPU 최소"); put("jetson.desk_enc_speedup_max", round(max(_enc), 2), "같음 최대")
    _js = [N[f"jetson.{k}.speedup"] for k in JL if k != "base"]
    put("jetson.enc_speedup_min", min(_js), "Jetson VisPruner·CDPruner 최소"); put("jetson.enc_speedup_max", max(_js), "같음 최대")
    put("jetson.max_acc_diff", round(max(abs(N[f"jetson.{k}.gqa500_4bit"] - N[f"jetson.{k}.gqa500_fp16_5080"]) for k in JL), 1), "4비트 vs FP16")
    put("jetson.save_128_to_64_ms", round(N["jetson.vp128.ttft_ms"] - N["jetson.vp64.ttft_ms"]), "Jetson 128→64 TTFT 감소")
    if P1:
        _v = {r["setting"]: r for r in P1 if r["key"] == "vispruner"}
        put("meas.pc1.vp_save_128_to_64_ms", round(_v["default"]["ttft_ms"] - _v["r889"]["ttft_ms"]), "5080 128→64 TTFT 감소")
        put("jetson.save_ratio_vs_5080", round(N["jetson.save_128_to_64_ms"] / N["meas.pc1.vp_save_128_to_64_ms"]), "128→64 토큰 구간의 절대 절감 배수(5.4절 전용)")
        # 10/16 종합 검토: 초록·6장의 '답변당 절약'은 원래 모델 대비 절약(128·64 토큰)으로 계산(이전 27배는 128→64 구간만이었음)
        _b5 = next(r for r in P1 if r["key"] == "base")["ttft_ms"]
        _rat = [(jb["ttft_ms_median"] - JL[k]["ttft_ms_median"]) / (_b5 - _v[s]["ttft_ms"]) for k, s in (("vp128", "default"), ("vp64", "r889"))]
        put("jetson.save_vs_base_ratio_min", round(min(_rat)), "Jetson/5080 원래 모델 대비 TTFT 절약 배수 최소"); put("jetson.save_vs_base_ratio_max", round(max(_rat)), "같음 최대")
        put("jetson.vp64.save_vs_base_ms", round(jb["ttft_ms_median"] - JL["vp64"]["ttft_ms_median"]), "Jetson 576→64 절약"); put("meas.pc1.vp64_save_vs_base_ms", round(_b5 - _v["r889"]["ttft_ms"]), "5080 576→64 절약")
        if os.path.exists(XC):  # 11/5: 6장 (iii)의 RTX 5070 Ti 대비 배수(이전엔 본문에 손 계산 12–14)
            _x2 = {r["setting"]: fl(r["pc2_ttft"]) for r in X if r["key"] == "vispruner"}
            _r2 = [(jb["ttft_ms_median"] - JL[k]["ttft_ms_median"]) / (fl(xb["pc2_ttft"]) - _x2[s]) for k, s in (("vp128", "default"), ("vp64", "r889"))]
            put("jetson.save_vs_pc2_ratio_min", round(min(_r2)), "Jetson/5070 Ti 원래 모델 대비 TTFT 절약 배수 최소"); put("jetson.save_vs_pc2_ratio_max", round(max(_r2)), "같음 최대")
    # NF4 층 단위 추가 비용(microbench_nf4.py), 토큰 수 스윕(100문항×3회, run_sweep.sh)
    JS = f"{JR}/guioff_1105/sweep" if os.path.exists(f"{JR}/guioff_1105/sweep/microbench_nf4.json") else f"{JR}/sweep"  # 11/5 화면 끔 재측정
    if os.path.exists(f"{JS}/microbench_nf4.json"):
        _mb = [r for r in json.load(open(f"{JS}/microbench_nf4.json"))["rows"] if r["tokens"] >= 16]
        put("jetson.nf4_overhead_min_ms", round(min(r["overhead_ms"] for r in _mb), 1), "4096×11008 층 NF4−FP16, 16–1024 토큰")
        put("jetson.nf4_overhead_max_ms", round(max(r["overhead_ms"] for r in _mb), 1), "같음")
        _sw = sorted((json.load(open(f)) for f in glob.glob(f"{JS}/*/latency_*.json")), key=lambda d: d["n_vis_tokens"])
        _pt = {int(d["n_vis_tokens"]): d["ttft_ms_median"] for d in _sw}
        _sl = lambda a, b: (_pt[b] - _pt[a]) / (b - a)
        put("jetson.sweep.n_points", len(_pt), "토큰 수 설정 수"); put("jetson.sweep.tok_min", min(_pt), "최소 토큰"); put("jetson.sweep.tok_max", max(_pt), "최대 토큰")
        put("jetson.sweep.slope_min_ms", round(min(_sl(a, b) for a, b in ((128, 256), (256, 384), (384, 576))), 1), "128–576 인접 구간 기울기 최소")
        put("jetson.sweep.slope_max_ms", round(max(_sl(a, b) for a, b in ((128, 256), (256, 384), (384, 576))), 1), "같음 최대")
        put("jetson.sweep.slope_32_64_ms", round(_sl(32, 64), 1), "32–64 기울기")
        put("jetson.sweep.slope_64_128_ms", round(_sl(64, 128), 1), "64–128 기울기(10/16: 본문에 세 구간 모두 보고)")
        _xs = [x for x in _pt if x >= 128]; _mx = statistics.mean(_xs); _my = statistics.mean(_pt[x] for x in _xs)
        _b = sum((x - _mx) * (_pt[x] - _my) for x in _xs) / sum((x - _mx) ** 2 for x in _xs)
        put("jetson.sweep.intercept_s", round((_my - _b * _mx) / 1000, 1), "128–576 직선의 0토큰 절편(초)")
        put("jetson.sweep.run_spread_pct", round(max(100 * (max(r["ttft_ms_median"] for r in d["runs"]) - min(r["ttft_ms_median"] for r in d["runs"])) / d["ttft_ms_median"] for d in _sw), 1), "3회 중앙값 최대−최소 / 중앙값")
# 정확도 — 원논문 보고값(bench/accuracy_reported.csv, LLaVA-1.5-7B 같은 토큰 수) vs RTX 5080 측정(table8.csv)
if P1 and os.path.exists("bench/accuracy_reported.csv"):
    _m = {(r["key"], r["setting"]): r for r in P1}
    _d = collections.defaultdict(list)
    for r in csv.DictReader(open("bench/accuracy_reported.csv", encoding="utf-8")):
        if r["key"] == "base" or not r["gqa"]: continue
        x = _m[(r["key"], r["setting"])]
        _d["gqa"].append(x["gqa"] - float(r["gqa"])); _d["pope"].append(x["pope_f1"] - float(r["pope"])); _d["textvqa"].append(x["textvqa"] - float(r["textvqa"]))
        if r["mme_p"]: _d["mme_p"].append(x["mme_p"] - float(r["mme_p"]))
        if r["mme_total"]: _d["mme_total"].append(x["mme_p"] + float(x["mme_c"]) - float(r["mme_total"]))
    for k, v in _d.items():
        put(f"accrep.{k}.max_abs", round(max(map(abs, v)), 1), "측정−보고 최대 절댓값"); put(f"accrep.{k}.min", round(min(v), 1), "측정−보고 최소"); put(f"accrep.{k}.max", round(max(v), 1), "측정−보고 최대")
    put("accrep.n_settings", len(_d["gqa"]), "비교 설정 수")
# 분류 규칙 v2.1 재검증(10/15, main_survey/classval/score_round2.py → round2_result.json, 1차 평가자 새 표본 55편)
if os.path.exists("main_survey/classval/round2_result.json"):
    _r2 = json.load(open("main_survey/classval/round2_result.json", encoding="utf-8"))
    for _b in ("4.3", "4.5"):
        for _s in ("2024", "2026", "all"):
            _v = _r2[f"{_b}.{_s}"]
            put(f"classval.r2.{_b}.{_s}.strict_prec", _v["strict_prec"], "새 표본 엄격 정밀도(%)"); put(f"classval.r2.{_b}.{_s}.strict_n", _v["strict_n"], "엄격 층 판정 수")
            if _v.get("strict_ci"): put(f"classval.r2.{_b}.{_s}.strict_lo", _v["strict_ci"][0], "Wilson 95%"); put(f"classval.r2.{_b}.{_s}.strict_hi", _v["strict_ci"][1], "Wilson 95%")
            if "loose_prec" in _v: put(f"classval.r2.{_b}.{_s}.loose_prec", _v["loose_prec"], "새 표본 느슨 정밀도(층 가중, %)")
# 결론 해석 수치(robustness_numbers.py → main_survey/robustness.json)
if os.path.exists("main_survey/robustness.json"):
    for _k, _v in json.load(open("main_survey/robustness.json", encoding="utf-8")).items(): put(f"robust.{_k}", _v, "robustness_numbers.py")
# 코드 링크 자동 확인(main_survey/check_code_links.py)
if os.path.exists("main_survey/code_link_files.json"):
    _lc = json.load(open("main_survey/code_link_check.json", encoding="utf-8")); _lf = json.load(open("main_survey/code_link_files.json", encoding="utf-8"))
    put("links.with_link", _lc["with_link"], "code 링크 수"); put("links.reachable", _lc["reachable"], "열리는 링크")
    put("links.with_source", sum(1 for x in _lf if x[2]), "소스 파일이 있는 저장소(Kimi-VL=HF, AutoSelect=README 만 제외)")
# 데스크톱 반복 간 변동 — 5회 실행 중앙값들의 사분위 범위(IQR), 표 8·9
_IQ = {}
for _mc, _root in (("pc1", "bench/results_pc1"), ("pc2", "bench/results_pc2")):
    for f in glob.glob(f"{_root}/*/latency_*.json"):
        _d = json.load(open(f)); _r = [x["ttft_ms_median"] for x in _d["runs"]]; _q = statistics.quantiles(_r, n=4)
        _mk = os.path.basename(os.path.dirname(f)); _st = os.path.basename(f)[8:-5]
        _IQ[(_mc, _mk, _st)] = (_q[2] - _q[0], 100 * (_q[2] - _q[0]) / statistics.median(_r), 100 * (max(_r) - min(_r)) / statistics.median(_r))
        put(f"iqr.{_mc}.{_mk}.{_st}.ms", round(_q[2] - _q[0], 1), "5회 run 중앙값 IQR(ms)")
_ok = {k: v for k, v in _IQ.items() if k[1] != "cdpruner"}       # as released 는 불안정 자체가 결과
put("iqr.max_pct", round(max(v[1] for v in _ok.values()), 1), "IQR/중앙값 최대(as released 제외)")
put("iqr.max_pct_where", max(_ok, key=lambda k: _ok[k][1]), "그 설정")
put("iqr.n_below2", sum(v[1] < 2 for v in _ok.values()), "IQR 2% 미만 설정 수"); put("iqr.n_settings", len(_ok), "설정 수(두 GPU)")
put("iqr.cdp_released_max_pct", round(max(v[1] for k, v in _IQ.items() if k[1] == "cdpruner"), 0), "as released IQR 최대 %")
# 점수 없는 기준선(균등 선택·풀링)과 FastV 2층 — 두 번째 세션(results_pc1_second_session 가 같은 세션 재측정), 표 8·5.2절
if os.path.exists("main_survey/baseline_comparison.json"):
    _braw = json.load(open("bench/results_pc1/base/latency_default.json"))["ttft_ms_median"]   # 11/8: 표 8 다른 행과 같이 반올림 전 원본 TTFT 로 나눔(이전엔 106.0 으로 나눠 균등 128·풀링 64 가 0.01 다름)
    for _m, _s, _n in (("uniform", "default", 128), ("uniform", "r889", 64), ("pool", "default", 144), ("pool", "r889", 64), ("fastv", "k2", 288), ("fastv", "k2r889", 64)):
        _d = json.load(open(f"bench/results_pc1/{_m}/latency_{_s}.json")); _k = f"meas.pc1.{_m}{'_k2' if _s.startswith('k2') else ''}.{_n}"
        put(f"{_k}.ttft_ms", round(_d["ttft_ms_median"], 1), "두 번째 세션(10/28)"); put(f"{_k}.speedup", round(_braw / _d["ttft_ms_median"], 2), "표 8 원본(반올림 전) 기준")
        put(f"{_k}.energy_j", round(_d["energy_j_per_sample"], 1), "두 번째 세션(10/28)"); put(f"{_k}.peak_vram_gb", round(_d["peak_vram_gb"], 2), "두 번째 세션(10/28)")
    put("remeasure.base_ttft_ms", round(json.load(open("bench/results_pc1_second_session/base_alone/latency_default.json"))["ttft_ms_median"], 1), "두 번째 세션 원본(단독)")
    _dv = [100 * (json.load(open(f"bench/results_pc1_second_session/{m}/latency_{s}.json"))["ttft_ms_median"] - N[f"meas.pc1.{m}.{n}.ttft_ms"]) / N[f"meas.pc1.{m}.{n}.ttft_ms"]
           for m, s, n in (("vispruner", "default", 128), ("vispruner", "r889", 64), ("cdpruner_fix", "default", 128), ("cdpruner_fix", "r889", 64), ("sparsevlm", "default", 192),
                           ("sparsevlm", "r889", 64), ("dart", "default", 128), ("dart", "r889", 64), ("fastv", "default", 288), ("fastv", "r889", 64))]
    put("remeasure.dev_min_pct", round(min(_dv), 1), "두 번째 세션 − 표 8 (%)"); put("remeasure.dev_max_pct", round(max(_dv), 1), "두 번째 세션 − 표 8 (%)")
    _BL = json.load(open("main_survey/baseline_comparison.json", encoding="utf-8"))
    for _g, _ps in _BL.items():
        for _pk, _r in _ps.items():
            for _t, _v in _r.items(): put(f"bl.{_g}.{_pk.replace('|', '-')}.{_t}", _v["diff"], f"짝지은 부트스트랩 CI {_v['ci']}{' *' if _v['sig'] else ''}")
# torch.compile 시도 — 원본 모델, 같은 세션의 eager·시각 인코더·전체 컴파일(bench/results_pc1_compile), 5.3절·표 S11
if os.path.exists("bench/results_pc1_compile/base_compile/latency_full.json"):
    _ce = json.load(open("bench/results_pc1_compile/base/latency_default.json"))["ttft_ms_median"]
    for _s in ("vision", "full"): put(f"compile.{_s}_ttft_ms", round(json.load(open(f"bench/results_pc1_compile/base_compile/latency_{_s}.json"))["ttft_ms_median"], 1), "torch.compile, 500×5")
    put("compile.eager_ttft_ms", round(_ce, 1), "같은 세션 eager"); put("compile.full_reduction_pct", round(100 * (_ce - N["compile.full_ttft_ms"]) / _ce), "전체 컴파일 TTFT 감소 %")
# PC2 LLaVA-NeXT-7B FP16 가능성 시험(원본, GQA 20문항, bench/results_pc2_next) — 16 GB 카드에서 넘침, 6(v)·한계 절
if os.path.exists("bench/results_pc2_next/feasibility.json"):
    _nx = json.load(open("bench/results_pc2_next/feasibility.json")); _r = _nx["rows"]; _long = [r for r in _r if r["seq_len"] > 2800]; _rest = [r for r in _r[1:] if r["seq_len"] <= 2800]
    put("next.n", len(_r), "GQA 표본 앞 n문항"); put("next.weights_gb", round(_nx["weights_gb"], 1), "가중치 할당 GiB")
    put("next.seq_min", min(r["seq_len"] for r in _r), "시퀀스 길이(텍스트+시각)"); put("next.seq_max", max(r["seq_len"] for r in _r), "시퀀스 길이(텍스트+시각)")
    put("next.peak_min_gb", round(min(r["peak_gb"] for r in _r), 1), "문항별 PyTorch 최대 할당 GiB"); put("next.peak_max_gb", round(_nx["max_peak_gb"], 1), "문항별 PyTorch 최대 할당 GiB")
    put("next.card_gb", round(_nx["card_mib"] / 1024, 1), "카드 용량 GiB"); put("next.desktop_gb", round(_nx["used_before_mib"] / 1024, 1), "시작 전 다른 앱 사용량 GiB")
    put("next.ttft_rest_min_s", round(min(r["ttft_ms"] for r in _rest) / 1000, 2), "첫(워밍업)·최장 2문항 제외"); put("next.ttft_rest_max_s", round(max(r["ttft_ms"] for r in _rest) / 1000, 2), "첫(워밍업)·최장 2문항 제외")
    put("next.ttft_long_min_s", round(min(r["ttft_ms"] for r in _long) / 1000, 1), f"seq>2800 {len(_long)}문항"); put("next.ttft_long_max_s", round(max(r["ttft_ms"] for r in _long) / 1000, 1), f"seq>2800 {len(_long)}문항")
# 11/8 전수조사: 5.2절 Memory·6(v)·결론의 배치별 prefill 메모리(보충 표 S8, bench/results_pc1_memory_batch). 표 S8 에 보이는 값(소수 둘째 자리)에서 계산
if os.path.exists("bench/results_pc1_memory_batch/memory_batch.json"):
    _MB = json.load(open("bench/results_pc1_memory_batch/memory_batch.json", encoding="utf-8")); _R = {(r["batch"], r["visual_tokens"]): r for r in _MB["rows"]}
    _s2 = lambda b, t, c: float(f"{_R[(b, t)][c]:.2f}")
    put("membatch.weights_gb", round(_MB["weights_gb"], 1), "가중치 할당")
    for _b in (1, 8, 16):
        for _t in (576, 64): put(f"membatch.extra_{_t}_b{_b}_gb", _s2(_b, _t, "extra_gb"), "가중치 위 할당(표 S8)")
        put(f"membatch.saving_b{_b}_gb", round(_s2(_b, 576, "extra_gb") - _s2(_b, 64, "extra_gb"), 2), "576 − 64 가중치 위 할당(표 S8 값끼리)")
    put("membatch.peak_576_b8_gb", _s2(8, 576, "peak_gb"), "576토큰 배치 8 최대 할당(표 S8)"); put("membatch.peak_64_b16_gb", _s2(16, 64, "peak_gb"), "64토큰 배치 16 최대 할당(표 S8)")
    _kv = [_s2(b, t, "kv_cache_gb") / _s2(b, t, "extra_gb") for b in (1, 8, 16) for t in (576, 64)]
    put("membatch.kv_share_min_pct", round(100 * min(_kv)), "KV 캐시 / 가중치 위 할당, 배치 1·8·16"); put("membatch.kv_share_max_pct", round(100 * max(_kv)), "같음 최대")
    put("membatch.kv_share_about_pct", int(round(100 * sum(_kv) / len(_kv), -1)), "본문 'about x%' (평균을 10 단위로)")
# 스크리닝: 코드 링크 유무별 '정독 유지' 비율(선정 단계에 코드·근거가 작용한 정도; 10/12 κ 분석)
_C = list(csv.DictReader(open("screening_marks_export.csv", encoding="utf-8-sig")))
for _v, _lab in (("True", "code"), ("False", "nocode")):
    _s = [c for c in _C if c["code"] == _v]; put(f"screen.keep_pct_{_lab}", round(100 * sum(c["mark"] in ("keep", "star") for c in _s) / len(_s), 1), "screening_marks_export.csv")

# 실행 시점 가지의 기간별 비율(monthly_trend.py → main_survey/monthly_trend/periods.json). 기간 비교 Fisher 는 사후·서술용(보정 없음)
if os.path.exists("main_survey/monthly_trend/periods.json"):
    _PM = json.load(open("main_survey/monthly_trend/periods.json", encoding="utf-8"))["series"]
    for _s in ("vlm.4.4.strict", "vlm.4.4.loose", "pool.4.4.strict"):
        for _p, _v in _PM[_s]["periods"].items(): put(f"trendm.{_s}.{_p}.pct", round(100 * _v["k"] / _v["n"], 1), "기간별 비율 %(k/n, periods.json)")
        for _t in _PM[_s]["tests"]:
            _a, _b = _t["compare"].split(" vs ")
            put(f"trendm.{_s}.{_a}__{_b}.ratio", _t["ratio"], "기간 비교 비율(사후, 보정 없음)"); put(f"trendm.{_s}.{_a}__{_b}.p", float(f"{_t['p_fisher']:.2g}"), "Fisher 양측 p(사후, 보정 없음)")
    assert N["trendm.vlm.4.4.strict.2024__2026_jan_aug.ratio"] == float(N["trend.vlm.4.4.strict.rel_growth"])   # 표 2 와 같은 규칙
    assert N["trendm.vlm.4.4.strict.2024_jan_aug__2026_jan_aug.ratio"] == 7.38
# 2차 압축 목록(카드 61장)의 출처(selection_190_check.py → main_survey/selection_190/h_selection.json)
if os.path.exists("main_survey/selection_190/h_selection.json"):
    _H = json.load(open("main_survey/selection_190/h_selection.json", encoding="utf-8")); assert _H["reproduce"]["identical"]
    put("sel190.filter_n", _H["reproduce"]["step3"], "제목 필터 결과(candidates_4.3_pool.json 과 같음)")
    put("sel190.list_cards", _H["curated"]["n"], "2차 압축 목록 카드"); put("sel190.list_in_filter", _H["curated"]["in_190"], "그중 필터 결과 안")
    put("sel190.list_added", len(_H["curated"]["outside_190"]), "필터 밖에서 더한 편(다른 후보 목록에 있던 논문)")
    put("sel190.unselected", _H["unselected"]["n"], "필터 결과 중 목록에 안 오른 편"); put("sel190.unselected_other_lists", _H["unselected"]["carded_elsewhere"], "그중 다른 후보 목록 카드에 오른 편")
    put("sel190.unselected_kept", len(_H["unselected"]["carded_kept_ids"]), "그중 유지된 편"); put("sel190.unselected_never", _H["unselected"]["never_carded"], "어느 카드에도 안 오른 편")
    put("sel190.filter_strict43", _H["profile"]["190"]["strict43_v21"], "필터 결과 중 지금 4.3 엄격 규칙 일치")
    put("sel190.comp_entries", _H["final"]["compression_table"], "압축 표 항목"); put("sel190.comp_from_list", _H["final"]["compression_from_61"], "그중 2차 압축 목록 카드에서 온 항목")
    assert N["sel190.list_in_filter"] + N["sel190.list_added"] == N["sel190.list_cards"] and N["sel190.list_in_filter"] + N["sel190.unselected"] == N["sel190.filter_n"]
    assert N["sel190.unselected_other_lists"] + N["sel190.unselected_never"] == N["sel190.unselected"]
# 11/9: 2차 후보 목록 카드의 모델 표시 — 요약 줄의 '★ 추천'과 '넘김' 권고(sheets/sheet_4.xR*.csv 초록 첫 줄), 판정은 screening_marks_export.csv
_MKB = {(r["id"], r["b"]): r["mark"] for r in S}; _RC = collections.Counter()
for _f in sorted(glob.glob("sheets/sheet_4.[1-5]R*.csv")):
    _b = os.path.basename(_f)[6:].split("_")[0]
    for _r in csv.DictReader(open(_f, encoding="utf-8-sig")):
        _h = _r["abstract"].split("\n")[0]; assert _h.startswith("[요약]")
        _kd = "flag" if "★ 추천" in _h else "skipadv" if "넘김" in _h else "plain"
        _RC[_kd] += 1; _RC[_kd + "_kept"] += _MKB[(_r["id"], _b)] in ("keep", "star")
assert _RC["flag"] == sum(r["rec"] == "True" for r in S)   # 추천 표시는 2차 목록에만
_kept = sum(r["mark"] in ("keep", "star") for r in S)
put("screen.r_cards", _RC["flag"] + _RC["skipadv"] + _RC["plain"], "2차 후보 목록 카드(모델 요약 있음)")
put("screen.r_flag", _RC["flag"], "'추천' 표시 카드"); put("screen.r_flag_kept", _RC["flag_kept"], "그중 유지")
put("screen.r_skipadv", _RC["skipadv"], "요약이 넘김을 권한 카드"); put("screen.r_skipadv_kept", _RC["skipadv_kept"], "그중 유지")
put("screen.unmarked_cards", len(S) - _RC["flag"] - _RC["skipadv"], "추천·넘김 표시가 없는 카드(1차 목록 포함)"); put("screen.unmarked_kept", _kept - _RC["flag_kept"] - _RC["skipadv_kept"], "그중 유지")
put("screen.kept_cards", _kept, "유지 카드(keep+star)")
# 3.4절 사양별 성장(spec_growth.py → main_survey/spec_growth/spec_growth.json; 그림 2(d)·보충 표 S12), 등급 2차 평가 보정 전 일치(3.5절)
if os.path.exists("main_survey/spec_growth/spec_growth.json"):
    for _r in json.load(open("main_survey/spec_growth/spec_growth.json", encoding="utf-8"))["rows"]:
        for _b, _v in (("4.4", _r["exec"]), ("4.2", _r["train"])):
            if not _v: continue
            put(f"spec.{_b}.{_r['key']}.growth", _v["growth"], "사양별 상대 성장(나중/앞)"); put(f"spec.{_b}.{_r['key']}.lo", _v["lo"], "95% CI(Katz; 보정 행은 부트스트랩)"); put(f"spec.{_b}.{_r['key']}.hi", _v["hi"], "95% CI")
            if _v["p"] is not None: put(f"spec.{_b}.{_r['key']}.p", float(f"{_v['p']:.2g}"), "Fisher 양측 p")
            if "k1" in _v:
                for _f in ("k1", "n1", "k2", "n2", "s1", "s2"): put(f"spec.{_b}.{_r['key']}.{_f}", _v[_f], "건수·비율(앞 k1/n1 → 나중 k2/n2)")
    assert N["spec.4.4.base.growth"] == float(N["trend.vlm.4.4.strict.rel_growth"]) and N["spec.4.4.same_months.growth"] == N["trendm.vlm.4.4.strict.2024_jan_aug__2026_jan_aug.ratio"]
    _pt = json.load(open("main_survey/monthly_trend/periods.json", encoding="utf-8"))["series"]["vlm.4.2.strict"]["periods"]
    for _p in ("2024_jan_aug", "2024_sep_dec", "2025", "2026_jan_aug"): put(f"trendm.vlm.4.2.strict.{_p}.pct", round(100 * _pt[_p]["k"] / _pt[_p]["n"], 1), "학습 엄격 기간별 비율 %(periods.json)")
_SG = json.load(open("main_survey/second_rater/second_rater_grade_result.json", encoding="utf-8"))
for _k in ("code", "measured", "grade"):
    put(f"r2grade.{_k}_agree_n", round(_SG[f"{_k}_agree"] * _SG["n"] / 100), "보정 전 2차 평가 일치 수(20항목)"); put(f"r2grade.{_k}_kappa", _SG[f"{_k}_kappa"], "보정 전 Cohen κ")
put("r2grade.n", _SG["n"], "등급 2차 평가 표본")
_CV = json.load(open("main_survey/classval/classval_table_current.json", encoding="utf-8"))["recall"]
for _k in ("4.1.loose", "4.1.strict"):
    put(f"classval.recall.{_k}.hit", _CV[_k]["hit"], "재현율 표본에서 규칙이 찾은 편(현재 규칙)"); put(f"classval.recall.{_k}.n_pos", _CV[_k]["n_pos"], "평가자가 식별한 편"); put(f"classval.recall.{_k}.pct", _CV[_k]["recall"], "재현율 %")
# 11/9: 스크리닝 후보의 출처 — 1차 순위 목록(build_sheets.py)과 효율 풀 중 카드에 오른 범위(screening_coverage.py → main_survey/screening_coverage/coverage.json)
if os.path.exists("main_survey/screening_coverage/coverage.json"):
    _SC = json.load(open("main_survey/screening_coverage/coverage.json", encoding="utf-8"))
    put("screen.r1.cap", _SC["cap"], "1차: 가지마다 점수 상위 편수"); put("screen.r1.cite_cap", _SC["cite_cap"], "1차: 더해 넣은 인용 상위 편수")
    for _b, _v in _SC["round1"].items(): put(f"screen.r1.{_b}.assigned", _v["assigned"], "1차: 그 가지로 배정된 효율 풀 논문"); put(f"screen.r1.{_b}.cards", _v["cards"], "1차 카드")
    put("screen.r1.no_branch", _SC["pool"] - sum(_v["assigned"] for _v in _SC["round1"].values()), "1차: 어느 가지 패턴에도 안 맞은 효율 풀 논문")
    put("screen.pool_carded", _SC["cards_in_pool"], "효율 풀 중 카드에 한 번이라도 오른 편"); put("screen.pool_never", _SC["pool_never_carded"], "효율 풀 중 카드에 안 오른 편")
    put("screen.cards_outside_pool", _SC["cards_outside_pool"], "카드에 오른 편 중 효율 풀 밖(2차 압축 목록)")
    put("sel190.never_outside_pool", _SC["never_screened_96"]["outside_pool"], "스크리닝 안 된 96편 중 효율 풀 밖"); put("sel190.never_strict43", _SC["never_screened_96"]["strict43"], "96편 중 압축 엄격 규칙 일치")
    assert N["screen.pool_carded"] + N["screen.pool_never"] == N["corpus.pool"] and N["screen.pool_carded"] + N["screen.cards_outside_pool"] == 475
    _w = _SC["never_screened_96"]["where"]; _rk = _SC["never_screened_96"]["rank_in_compression_round1"]
    put("sel190.never_below_cut", sum(v for k, v in _w.items() if k.startswith("pool_assigned_")), "96편 중 1차에 어떤 가지로 배정됐지만 그 가지 카드 밖"); put("sel190.never_below_cut_comp", len(_rk), "그중 압축 배정")
    put("sel190.never_comp_rank_min", min(_rk), "압축 배정 편의 1차 순위 최소"); put("sel190.never_comp_rank_max", max(_rk), "최대"); put("sel190.never_no_branch", _w.get("pool_no_branch_score", 0), "96편 중 풀 안이지만 어느 패턴에도 안 맞음")
    assert N["sel190.never_outside_pool"] + N["sel190.never_below_cut"] + N["sel190.never_no_branch"] == N["sel190.unselected_never"]

# ───────────────────────── 출력 ─────────────────────────
os.makedirs("draft/numbers", exist_ok=True); os.makedirs("draft/tables", exist_ok=True)
json.dump(N, open("draft/numbers/paper_numbers.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("draft/numbers/paper_numbers.md", "w", encoding="utf-8") as fo:
    fo.write("# 논문 수치 (paper_numbers.py 생성 — 손으로 고치지 말 것)\n\n| 키 | 값 | 출처 |\n|---|---|---|\n")
    for k in N: fo.write(f"| `{k}` | {N[k]} | {SRC[k]} |\n")
    fo.write("\n## §4.6 초록 감사 정의 (정규식, 초록만)\n\n" + "\n".join(f"- **{k}**: `{v}`" for k, v in AUDIT.items()) + "\n")

# 표 2: 추세 (효율 풀 + VLM 전체)
BR = {"4.1": "Design", "4.2": "Training", "4.3": "Compression", "4.4": "Execution", "4.5": "Deployment", "4.6": "Measurement"}
def ff(x, d=1):
    try: return f"{float(x):.{d}f}"
    except (TypeError, ValueError): return "—"
def fp(x):
    try: x = float(x); return f"{x:.1e}".replace("e-0", "e−").replace("e-", "e−")
    except (TypeError, ValueError): return "—"
L = ["**Table 2.** Share of papers per branch in 2024 / 2025 / 2026 (Jan–Aug), relative growth (2026/2024), conditional share (strict ∩ loose / loose) and Fisher p (2024 vs 2026; bold = significant after Bonferroni, α = 0.0042).", "",
     "| Branch | Def. | Pool 2024 | 2025 | 2026 | ×growth | p | All-VLM 2024 | 2025 | 2026 | ×growth | cond. 24→26 | p |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for br in BR:
    for kind in ("loose", "strict"):
        x = next(r for r in T if r["pool"] == "효율 풀" and r["branch"] == br and r["kind"] == kind); y = next(r for r in T if r["pool"] != "효율 풀" and r["branch"] == br and r["kind"] == kind)
        bold = lambda r: (lambda s: f"**{s}**" if r["sig_bonf"] == "True" else s)(fp(r["p_fisher"]))
        cond = f"{ff(y['cond24'], 0)}→{ff(y['cond26'], 0)}%" if kind == "strict" and y.get("cond24") else ""
        L.append(f"| {br} {BR[br]} | {kind} | {x['s24']} | {x['s25']} | {x['s26']} | ×{x['rel_growth']} | {bold(x)} | {y['s24']} | {y['s25']} | {y['s26']} | ×{y['rel_growth']} | {cond} | {bold(y)} |")
L.append(f"\nPool n = {N['corpus.pool']} ({N.get('corpus.pool_2024')}/{N.get('corpus.pool_2025')}/{N.get('corpus.pool_2026')}); all-VLM n = {N['corpus.vlm']}.")
open("draft/tables/table2_trends.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# 표 3–7: 가지별 비교 매트릭스 (자기보고 수치)
TT = {"4.1": ("Table 3", "Design-time efficiency"), "4.2": ("Table 4", "Training-time efficiency"), "4.3": ("Table 5", "Compression"), "4.4": ("Table 6", "Execution-time efficiency"), "4.5": ("Table 7", "Deployment")}
cell = lambda v: (v or "—").replace("|", "/").replace("\n", " ").strip() or "—"
# 영문 칸: main_survey/matrix_en.csv (원본과 숫자 일치 검사됨). 한국어 원본은 기록용으로 둔다.
EN = {(r["branch"], r["id"]): r for r in csv.DictReader(open("main_survey/matrix_en.csv", encoding="utf-8"))}
NAME_EN = {"구조 프루닝 연구": "Structural pruning study", "LLaMA3 양자화 실증": "LLaMA3 quantization study", "Edge-Cloud 교통 감시": "Edge–cloud traffic monitoring",
           "Mirage(잠재 시각 토큰)": "Mirage", "ThinkLite-VL(MCTS)": "ThinkLite-VL", "Rank-1 Expert Pool LoRA": "Rank-1 Expert Pool", "Edge-Cloud SD+EE": "Edge–cloud SD + EE"}
for b, (tn, tt) in TT.items():
    R = [dict(r, **{k: EN[(b, r["id"])][k] for k in ("sub", "reduction", "flops", "speed_latency", "memory", "hardware")}) for r in M if r["_b"] == b]
    R = sorted(R, key=lambda r: (not r["sub"][:1].isdigit(), r["sub"], "ABC".index(r["_g"]), r["name"]))
    L = [f"**{tn}.** {tt}: cost quantities reported by the authors of the {len(R)} selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).", "",
         "| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |", "|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        nm = NAME_EN.get(r["name"], r["name"])
        L.append(f"| {nm}{' ★' if r['mark'] == 'star' else ''} | {r['id']} | {cell(r['sub'])} | {cell(r['reduction'])} | {cell(r['flops'])} | {cell(r['speed_latency'])} | {cell(r['memory'])} | {cell(r['hardware'])} | {r['_g']} |")
    open(f"draft/tables/table{int(tn.split()[1])}_{b}.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# 표 8 (RTX 5080 전체 측정) · 표 9 (두 GPU 비교): bench/results_cross/table_cross.csv + results_pc1 의 공개판 CDPruner
if os.path.exists("bench/results_cross/table_cross.csv"):
    X = list(csv.DictReader(open("bench/results_cross/table_cross.csv", encoding="utf-8")))
    fv = lambda v: float(v) if v not in (None, "", "None") else None
    f = lambda v, d=1: "—" if fv(v) is None else f"{fv(v):.{d}f}"
    NM = {"base": "LLaVA-1.5-7B (unmodified)", "vispruner": "VisPruner", "cdpruner_fix": "CDPruner (fix)", "fastv": "FastV (KV cache)", "sparsevlm": "SparseVLM", "dart": "DART"}
    L = ["**Table 8.** Measurements on the RTX 5080 (LLaVA-1.5-7B, FP16, batch size 1). Latency: median of 5 runs × 500 GQA test-dev questions; TTFT = time to first token; end-to-end = up to 32 generated tokens. Accuracy: full GQA test-dev balanced, POPE (F1), TextVQA validation (with OCR tokens) and MME perception. "
         "CDPruner (as released) uses two CUDA side streams per call and pages to host memory on a 16 GB GPU; CDPruner (fix) runs the same operations on the default stream (Section 5.1).", "",
         "| Method | Tokens | TTFT (ms) | Speed-up | End-to-end (ms) | Peak memory (GB) | Energy (J/sample) | GQA | POPE F1 | TextVQA | MME-P |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in X:
        L.append(f"| {NM[r['key']]} | {int(float(r['n_vis']))} | {f(r['pc1_ttft'])} | {fv(r['pc1_speedup']):.2f}× | {f(r['pc1_total'])} | {f(r['pc1_vram'], 2)} | {f(r['pc1_energy'])} | {f(r['pc1_gqa'])} | {f(r['pc1_pope'])} | {f(r['pc1_tvqa'])} | {f(r['pc1_mme'], 0)} |")
    if P1:
        base_t8 = next(r for r in P1 if r["key"] == "base")
        for r in [r for r in P1 if r["key"] == "cdpruner"]:
            L.append(f"| CDPruner (as released) | {int(r['n_vis'])} | {r['ttft_ms']:.1f} | {base_t8['ttft_ms'] / r['ttft_ms']:.2f}× | {r['total_ms']:.1f} | {r['peak_vram_gb']:.2f} | {r['energy_j']:.1f} | — | — | — | — |")
    open("draft/tables/table8_measurement.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    L = ["**Table 9.** The same measurements on two consumer GPUs: RTX 5080 (Core Ultra 5 245KF) and RTX 5070 Ti (Ryzen 9 9950X3D), same code, settings and data. Speed-up is relative to the unmodified model on the same GPU.", "",
         "| Method | Tokens | TTFT ms (5080) | ×5080 | TTFT ms (5070 Ti) | ×5070 Ti | Energy J (5080 / 5070 Ti) | GQA (5080 / 5070 Ti) | POPE F1 (5080 / 5070 Ti) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in X:
        L.append(f"| {NM[r['key']]} | {int(float(r['n_vis']))} | {f(r['pc1_ttft'])} | {fv(r['pc1_speedup']):.2f} | {f(r['pc2_ttft'])} | {fv(r['pc2_speedup']):.2f} | {f(r['pc1_energy'])} / {f(r['pc2_energy'])} | {f(r['pc1_gqa'], 2)} / {f(r['pc2_gqa'], 2)} | {f(r['pc1_pope'], 2)} / {f(r['pc2_pope'], 2)} |")
    L.append(f"\nMaximum absolute difference between GPUs over all settings: GQA {N['cross.max_abs_diff_gqa']}, POPE F1 {N['cross.max_abs_diff_pope']}, TextVQA {N['cross.max_abs_diff_tvqa']}, MME perception {N['cross.max_abs_diff_mme']} (of 2,000); peak memory {N['cross.max_vram_diff_gb']} GB. Spearman ρ of TTFT across the {N['cross.settings_both']} compressed settings: {N['cross.spearman_ttft']}.")
    open("draft/tables/table9_cross_gpu.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    if "jetson.base.ttft_ms" in N:
        L = ["**Table 10.** The unmodified model and VisPruner on a Jetson Orin Nano Developer Kit (8 GB unified memory, MAXN SUPER mode), with the language model in 4-bit NF4 because the FP16 model does not fit. Latency and energy: median of 5 runs × the same 500 GQA questions as Tables 8–9; energy is the board input power (VDD_IN). Accuracy: the same 500 GQA questions, 4-bit on the Jetson and FP16 on the RTX 5080.", "",
             "| Method | Tokens | TTFT (ms) | Speed-up | End-to-end (ms) | Energy (J/sample) | Energy ratio | Peak memory (GB) | GQA-500, 4-bit | GQA-500, FP16 (RTX 5080) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for k, nm, tk in (("base", "LLaVA-1.5-7B (unmodified)", 576), ("vp128", "VisPruner", 128), ("cd128", "CDPruner (fix)", 128), ("vp64", "VisPruner", 64), ("cd64", "CDPruner (fix)", 64)):
            L.append(f"| {nm} | {tk} | {N[f'jetson.{k}.ttft_ms']:.1f} | {N[f'jetson.{k}.speedup']:.2f}× | {N[f'jetson.{k}.total_ms']:.1f} | {N[f'jetson.{k}.energy_j']:.1f} | {N[f'jetson.{k}.energy_ratio']:.2f}× | {N[f'jetson.{k}.peak_alloc_gb']:.2f} | {N[f'jetson.{k}.gqa500_4bit']:.1f} | {N[f'jetson.{k}.gqa500_fp16_5080']:.1f} |")
        L.append(f"\nPeak system memory (CPU and GPU share it) reached {N['jetson.base.peak_sys_gb']} of {N['jetson.mem_total_gb']} GB for the unmodified model. Idle board power: {round(jb['idle_power_w'], 1)} W.")
        open("draft/tables/table10_jetson.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    for old in ("draft/tables/table8_measurement_pc1.md",):
        if os.path.exists(old): os.remove(old)

print(f"{len(N)} numbers -> draft/numbers/paper_numbers.json/.md ; tables -> draft/tables/")
for k in ("corpus.records", "corpus.vlm", "corpus.pool", "screen.cards", "matrix.entries", "matrix.papers", "matrix.grade_A", "matrix.grade_B", "matrix.grade_C", "matrix.representatives", "matrix.rep_non_A", "matrix.grade_changed_by_flops",
          "matrix.report_latency", "matrix.report_memory", "matrix.report_energy", "matrix.report_flops_only", "matrix.no_hardware", "matrix.4.4.1.hardware_types", "matrix.4.4.1.hardware_list",
          "audit.latency_pct", "audit.device_pct", "audit.params_pct", "audit.flops_pct", "audit.throughput_pct", "audit.memory_pct", "audit.energy_pct", "audit.metrics_none_pct", "audit.metrics_three_plus_pct",
          "meas.pc1.ttft_speedup_min", "meas.pc1.ttft_speedup_max", "meas.pc1.energy_ratio_min", "meas.pc1.energy_ratio_max", "meas.pc1.vram_saving_min_gb", "meas.pc1.vram_saving_max_gb",
          "cross.base_ttft_pc2", "cross.pc2_faster_count", "cross.pc2_speedup_min", "cross.pc2_speedup_max", "cross.max_abs_diff_gqa", "cross.max_abs_diff_pope", "cross.max_abs_diff_tvqa", "cross.max_abs_diff_mme", "cross.spearman_ttft", "cross.max_vram_diff_gb"):
    print(f"  {k} = {N.get(k)}")
for b in ("4.1", "4.2", "4.3", "4.4", "4.5"):
    print(f"  {b}: {N[f'matrix.{b}.entries']} entries, A/B/C {N[f'matrix.{b}.grade_A']}/{N[f'matrix.{b}.grade_B']}/{N[f'matrix.{b}.grade_C']}, ★{N[f'matrix.{b}.representatives']}")

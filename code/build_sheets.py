#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""가지별 정독 후보 시트를 만든다 (taxonomy.md 4.1~4.6).

왜 가지별로 따로 뽑나:
  전역 필터(효율 키워드 2개 이상, 341편)로는 4.1(구조 설계)이 4편밖에 안 잡힌다.
  MoE·조기종료 같은 구조 논문은 효율 키워드가 1개뿐이라 통째로 탈락하기 때문.
  그래서 효율 풀(1,947편)에서 가지별 규칙으로 직접 뽑고, 논문 1편은 주가지 1곳에만 넣는다.

4.6(측정)은 성격이 다르다. 15,394편을 뒤져도 효율 벤치마크 논문이 5편뿐이라
  "논문을 소개하는 절"이 성립하지 않는다. 대신 어떤 지표가 얼마나 보고되는지
  실태를 감사하는 시트(sheet_4.6_measurement_audit.csv)를 만든다.

출력: sheets/sheet_4.1_*.csv ~ 4.5, sheets/sheet_4.6_measurement_audit.csv, sheets/_INDEX.md
실행: python build_sheets.py
"""
import re, os, csv, sys, json
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from arxiv_scrape import extract_keywords, KW_CLUSTER, load_cache

CAP = 60          # 가지당 용어점수 상위 몇 편을 담을지
CITE_CAP = 15     # 여기에 더해 인용수 상위 몇 편을 합집합으로 넣을지.
                  # 용어 밀도만으로 자르면 유명하지만 표현이 적은 논문을 놓친다
                  # (예: 'SoTA with Less' 149회 — 4.2 논문인데 60등 밖으로 밀렸음)
OUTDIR = "sheets"
CITE_FILE = "citations.json"

# 가지별 판정 규칙 — (가지, 라벨, [(정규식, 가중치, 표시명)])
# 가중치: 그 가지에만 나타나는 표현일수록 높게. 주가지 결정과 정렬에 사용.
BRANCHES = [
 ("4.1", "설계 시점 — 구조", [
    (r"mixture[- ]of[- ]experts|\bMoE\b", 3, "MoE"),
    (r"early exit|layer skip|depth pruning|layer pruning", 3, "조기종료/층축소"),
    (r"encoder[- ]free|lightweight (vision|visual) encoder|small(er)? (vision|visual) encoder", 3, "인코더경량화"),
    (r"state space model|\bMamba\b|linear attention|efficient attention", 2, "SSM/선형어텐션"),
    (r"\bQ[- ]?Former\b|resampler|perceiver|projector design", 2, "커넥터설계"),
 ]),
 ("4.2", "학습 시점 — PEFT·데이터", [
    (r"\bLoRA\b|\bQLoRA\b|\bDoRA\b|low[- ]rank adapt", 3, "LoRA"),
    (r"parameter[- ]efficient|\bPEFT\b", 3, "PEFT"),
    (r"\badapter\b", 2, "어댑터"),
    (r"prompt tuning|prompt learning|visual prompt", 1, "프롬프트튜닝"),
    (r"data[- ]efficient|data selection|data curation|curriculum", 1, "데이터효율"),
 ]),
 ("4.3", "압축 시점 — 양자화·저랭크·증류", [
    (r"quantiz|\bPTQ\b|\bQAT\b|\bINT[48]\b|W4A16|W8A8|binariz|ternary", 3, "양자화"),
    (r"knowledge distillation|self[- ]distill|teacher[- ]student", 3, "증류"),
    (r"low[- ]rank|matrix factoriz|\bSVD\b", 2, "저랭크"),
    (r"sparsity|sparse (model|weight)|structured pruning|weight pruning", 2, "희소/가중치프루닝"),
 ]),
 ("4.4", "실행 시점 — 토큰·캐시·디코딩", [
    (r"visual token|token pruning|token reduction|token compress|token merg|token packer", 3, "시각토큰압축"),
    (r"KV[- ]cache|key[- ]value cache|cache (compress|evict|reuse|prun)", 3, "KV캐시"),
    (r"token selection|token sampling|prune \w+ token", 2, "토큰선택"),
    (r"prefill", 2, "prefill"),
    (r"speculative decoding|flash[- ]?attention|\bvLLM\b|paged attention|prefix cach|continuous batching", 2, "디코딩/서빙"),
 ]),
 ("4.5", "배포 시점 — 온디바이스·하드웨어", [
    (r"Jetson|Raspberry|Snapdragon|smartphone|mobile phone|\biPhone\b|Orin", 3, "실단말"),
    (r"\bNPU\b|\bDSP\b|\bFPGA\b|\bASIC\b|hardware accelerator", 3, "가속기"),
    (r"on[- ]device|edge device|edge deploy", 2, "온디바이스"),
    (r"energy consumption|power consumption|energy[- ]efficient", 2, "전력"),
    (r"memory footprint|\bVRAM\b|memory usage", 1, "메모리"),
 ]),
]
COMPILED = [(b, lab, [(re.compile(p, re.I), w, n) for p, w, n in pats]) for b, lab, pats in BRANCHES]
LABEL = {b: lab for b, lab, _ in BRANCHES}

# 4.6 감사용 — 어떤 효율 지표를 보고하는가
METRICS = [
    ("지연", r"latency|inference time|wall[- ]clock"),
    ("처리량", r"throughput|tokens per second|\bTPS\b"),
    ("TTFT", r"\bTTFT\b|time[- ]to[- ]first[- ]token"),
    ("FLOPs", r"\bFLOPs\b|\bMACs\b|\bGFLOPs\b"),
    ("메모리", r"memory footprint|\bVRAM\b|memory usage|\bGPU\b memory"),
    ("전력", r"energy consumption|power consumption|\bwatt"),
    ("파라미터수", r"\bparameters?\b.{0,12}\b\d+(\.\d+)?\s?[BM]\b|\b\d+(\.\d+)?[BM][- ]parameter"),
    ("실측기기명", r"Jetson|Snapdragon|Orin|A100|H100|RTX|V100|\bTPU\b|Raspberry"),
]
METRICS_C = [(n, re.compile(p, re.I)) for n, p in METRICS]

# ── 인용수 (있으면) ──────────────────────────────────────────────────
# 2026년 논문은 63%가 인용 0회다. 연도가 다르면 절대 인용수는 비교 불가라서
# '연도 내 상위 %'를 함께 계산해 둔다. 인용수는 대표 논문 선정에만 쓰고
# 넘김 판정에는 쓰지 않는다 — 최신 흐름을 통째로 날리게 되므로.
CIT = {}
if os.path.exists(CITE_FILE):
    with open(CITE_FILE, encoding="utf-8") as f:
        CIT = {k: v for k, v in json.load(f).items() if v.get("c") is not None}
    print(f"인용수 캐시 {len(CIT)}편")
else:
    print("citations.json 없음 — 인용수 열은 비워둠")

# ── 데이터 적재 ──────────────────────────────────────────────────────
papers, _ = load_cache()
papers = list(papers.values())
for p in papers:
    p["kw"] = extract_keywords(f"{p['title']}\n{p['abstract']}")
    p["t"] = p["title"] + " " + p["abstract"]

CORE = {"mllm", "vision-language-model", "visual-instruction-tuning"}
EFF = {k for k, c in KW_CLUSTER.items() if c == "EFF"}
pool = [p for p in papers if (p["kw"] & CORE) and (p["kw"] & EFF)]
core_pool = [p for p in papers if p["kw"] & CORE]
print(f"효율 풀 {len(pool)}편 / VLM 전체 {len(core_pool)}편\n")

# ── 주가지 배정 ──────────────────────────────────────────────────────
for p in pool:
    sc, terms = {}, {}
    for b, lab, pats in COMPILED:
        s, names = 0, []
        for rx, w, nm in pats:
            if rx.search(p["t"]):
                s += w; names.append(nm)
        if s:
            sc[b] = s; terms[b] = names
    p["sc"], p["terms"] = sc, terms
    p["primary"] = max(sc, key=lambda k: sc[k]) if sc else None

# 연도 내 백분위 — 같은 해 논문들 사이에서 상위 몇 %인지 (100 = 최상위)
by_year = defaultdict(list)
for p in pool:
    c = CIT.get(p["id"], {}).get("c")
    if c is not None:
        by_year[p["date"][:4]].append(c)
for y in by_year:
    by_year[y].sort()
def pct(p):
    c = CIT.get(p["id"], {}).get("c")
    if c is None: return None
    arr = by_year[p["date"][:4]]
    if not arr: return None
    lo = sum(1 for x in arr if x < c)
    return round(lo / len(arr) * 100)

os.makedirs(OUTDIR, exist_ok=True)
dist, written, extra_by_cite = Counter(), {}, {}
for b, lab, _ in COMPILED:
    rows = [p for p in pool if p["primary"] == b]
    dist[b] = len(rows)
    rows.sort(key=lambda p: (p["sc"][b], p["date"]), reverse=True)   # 점수↓, 최신↓
    keep = rows[:CAP]
    kept_ids = {p["id"] for p in keep}
    # 인용수 상위를 합집합으로 — 용어 밀도는 낮지만 널리 읽힌 논문을 건진다
    cited = sorted([p for p in rows if p["id"] not in kept_ids
                    and CIT.get(p["id"], {}).get("c")],
                   key=lambda p: -CIT[p["id"]]["c"])[:CITE_CAP]
    extra_by_cite[b] = len(cited)
    keep = keep + cited
    keep.sort(key=lambda p: (p["sc"][b], p["date"]), reverse=True)
    written[b] = (len(keep), len(rows))
    fn = os.path.join(OUTDIR, f"sheet_{b}_{lab.split(' — ')[0].replace(' ','')}.csv")
    with open(fn, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["정독?", "대표?", "메모", "매칭근거", "점수", "인용", "핵심인용",
                    "연도내상위%", "id", "date", "title", "다른가지", "arxiv_url", "abstract"])
        for p in keep:
            others = " ".join(k for k in sorted(p["sc"]) if k != b)
            cv = CIT.get(p["id"], {})
            w.writerow(["", "", "", "/".join(p["terms"][b]), p["sc"][b],
                        cv.get("c", ""), cv.get("i", ""), pct(p) if pct(p) is not None else "",
                        p["id"], p["date"], p["title"], others,
                        f"https://arxiv.org/abs/{p['id']}", p["abstract"]])

# ── 4.6 측정 실태 감사 ───────────────────────────────────────────────
audit_rows = []
for p in pool:
    hit = [n for n, rx in METRICS_C if rx.search(p["t"])]
    audit_rows.append((len(hit), hit, p))
audit_rows.sort(key=lambda x: (-x[0], x[2]["date"]), reverse=False)
audit_rows.sort(key=lambda x: (x[0], x[2]["date"]), reverse=True)
fn46 = os.path.join(OUTDIR, "sheet_4.6_measurement_audit.csv")
with open(fn46, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["확인?", "메모", "보고지표수"] + [n for n, _ in METRICS] +
               ["id", "date", "title", "arxiv_url"])
    for n, hit, p in audit_rows[:200]:
        w.writerow(["", "", n] + ["O" if m in hit else "" for m, _ in METRICS] +
                   [p["id"], p["date"], p["title"], f"https://arxiv.org/abs/{p['id']}"])

metric_count = Counter()
for _, hit, _ in audit_rows:
    for h in hit: metric_count[h] += 1
nmetrics = Counter(n for n, _, _ in audit_rows)

# ── 리포트 ──────────────────────────────────────────────────────────
print("── 가지별 시트 ──")
tot = 0
for b, lab, _ in COMPILED:
    k, n = written[b]
    tot += k
    note = f"(전체 {n}편 중 {k}편" if n > k else f"({n}편 전량"
    note += f", 인용수로 추가 {extra_by_cite[b]}편)" if extra_by_cite[b] else ")"
    print(f"  {b}  {lab:<28} {k:>3}행  {note}")
print(f"  4.6  측정 — 실태 감사 시트              {min(200,len(audit_rows)):>3}행  (논문 소개 아님)")
print(f"\n  훑을 제목 합계: {tot}편")

print("\n── 4.6 근거: 효율 풀 1,947편의 지표 보고 실태 ──")
for n, _ in METRICS:
    c = metric_count[n]
    print(f"  {n:<10} {c:>5}편 ({c/len(pool)*100:>4.1f}%)  {'#'*(c//25)}")
print("\n  보고 지표 개수 분포:")
for k in sorted(nmetrics, reverse=True):
    if k <= 8:
        print(f"    {k}개 보고: {nmetrics[k]:>4}편")

with open(os.path.join(OUTDIR, "_INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# 정독 후보 시트 (2일차)\n\n")
    f.write("`정독?` 칸에 O, 특히 좋은 건 `대표?` 칸에도 O. 목표는 가지당 15~25편.\n\n")
    f.write("| 시트 | 행수 | 가지 전체 | 목표 |\n|---|---|---|---|\n")
    for b, lab, _ in COMPILED:
        k, n = written[b]
        f.write(f"| `sheet_{b}` {lab} | {k} | {n} | 15~25편 |\n")
    f.write(f"| `sheet_4.6` 측정 실태 감사 | {min(200,len(audit_rows))} | — | 논문 선정 아님, 실태 확인용 |\n")
    f.write("\n## 정렬 기준\n\n점수(가지 고유 표현이 많을수록 높음) 내림차순 → 최신순.\n")
    f.write("인용수는 arXiv API로 못 받아서 반영 못 함. 아는 이름이 보이면 그건 따로 챙길 것.\n")
print(f"\n→ {OUTDIR}/ 에 시트 6개 + _INDEX.md 저장")

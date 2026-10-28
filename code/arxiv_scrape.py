#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VLM 서베이 — arXiv 대량 수집 + 키워드 동시출현 파이프라인 (전체 스크랩용)
────────────────────────────────────────────────────────────────────────
목적: 2024-01 ~ 2026-08 VLM/MLLM 논문을 키워드 클러스터로 긁어서
      키워드 빈도·동시출현을 계산하고, 역피라미드(임계값) 스크리닝 →
      마인드맵/네트워크로 시각화할 수 있는 데이터로 내보낸다.

사용법:
  pip install arxiv
  python arxiv_scrape.py            # 수집 + 분석 (중단돼도 이어서 재실행 가능)
  python arxiv_scrape.py --analyze  # 수집 건너뛰고 papers_raw.json 으로 재분석만
                                    #  → 키워드 정규식 수정 후 재태깅할 때 사용

출력물:
  papers_raw.json     원본 캐시(제목·초록 포함). 재태깅/재분석의 기준. 지우지 말 것
  papers.csv          수집 논문 메타(제목·초록·날짜·카테고리·매칭 키워드)
  keyword_freq.csv    키워드 빈도(= 중복 수)
  cooccurrence.csv    키워드 쌍 동시출현
  network.gexf        Gephi/VOSviewer용 네트워크
  pilot_data.json     generate_viz.py 로 HTML 마인드맵 재생성용
────────────────────────────────────────────────────────────────────────
"""
import re, os, csv, sys, json, time, itertools
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")   # 콘솔 한글 깨짐 방지
except Exception:
    pass

# ── 설정 ────────────────────────────────────────────────────────────
DATE_FROM     = "202401010000"   # 2024 서베이(TPAMI) 이후
DATE_TO       = "202608312359"
MAX_PER_QUERY = 12000      # 쿼리당 상한(가장 큰 쿼리 10,134편을 덮는 값)
PAGE_SIZE     = 200        # API 1회 요청당 건수
DELAY         = 8          # arXiv 요청 간격(초). 3초는 429를 유발했음
RETRIES       = 3          # 쿼리 단위 재시도 횟수
BACKOFF       = 90         # 429/500 이후 대기(초) — 시도마다 배로 증가
# arXiv는 start≈10000 부근에서 500을 반환함(깊은 페이지네이션 한계).
# 결과가 그보다 많은 쿼리는 연 단위로 쪼개서 각 조각을 한도 아래로 유지한다.
SPLIT_QUERIES = {'abs:"vision-language model"'}
SPLIT_WINDOWS = [("202401010000","202412312359"),
                 ("202501010000","202512312359"),
                 ("202601010000","202608312359")]
MIN_OCCURRENCE = 50        # 시각화에 남길 키워드 최소 등장 횟수(역피라미드 임계값)
MIN_EDGE       = 20        # 시각화에 남길 엣지 최소 동시출현 횟수
USE_YAKE      = False      # True 면 초록에서 자유 키워드도 추가 추출(pip install yake)
RAW_CACHE     = "papers_raw.json"

# ── 검색 쿼리 (클러스터별) ──────────────────────────────────────────
# arXiv 쿼리 문법: abs:"..." 는 초록, cat:cs.CV 등 카테고리 제한
QUERIES = [
    'abs:"vision-language model"', 'abs:"multimodal large language model"',
    'abs:"visual instruction tuning"', 'abs:"efficient MLLM"',
    'abs:"efficient vision-language"', 'abs:"token pruning" AND abs:multimodal',
    'abs:"visual token" AND abs:compression', 'abs:"on-device" AND abs:"vision language"',
    'abs:"mobile" AND abs:"vision-language model"', 'abs:"lightweight" AND abs:MLLM',
    'abs:"KV cache" AND abs:multimodal', 'abs:quantization AND abs:MLLM',
    'abs:"any resolution" AND abs:multimodal', 'abs:"high-resolution" AND abs:MLLM',
    'abs:"document understanding" AND abs:multimodal', 'abs:"video" AND abs:MLLM',
    'abs:"visual grounding" AND abs:"large language model"',
    'abs:"multimodal hallucination"', 'abs:"multimodal" AND abs:"chain-of-thought"',
    'abs:"retrieval-augmented" AND abs:multimodal',
    'abs:"vision-language-action"', 'abs:"open-vocabulary" AND abs:segmentation',
]

# ── 통제 어휘: 표준키 -> 정규식(동의어 포함) ──────────────────────────
KW_PATTERNS = {
    "mllm": r"multimodal large language model|MLLM|multi-modal LLM|multimodal LLM",
    "vision-language-model": r"vision[- ]language model|VLM\b",
    "visual-instruction-tuning": r"visual instruction tuning",
    "efficient-vlm": r"efficient (MLLM|VLM|multimodal|vision[- ]language)",
    "lightweight-vlm": r"lightweight (MLLM|VLM|vision[- ]language|multimodal)",
    "small-vlm": r"\b(small|tiny) (MLLM|VLM|vision[- ]language)|TinyLLaVA|small-scale VLM",
    "on-device": r"on[- ]device|edge deploy|edge device",
    "mobile-vlm": r"mobile (VLM|vision[- ]language|MLLM)|MobileVLM",
    "low-power": r"low[- ]power|energy[- ]efficient|power efficient",
    "token-pruning": r"token pruning|token reduction|prune .*token",
    "token-merging": r"token merging|token merg|token compression|token packer|visual token compress",
    "kv-cache": r"KV[- ]cache|key[- ]value cache",
    "quantization": r"quantiz",
    "knowledge-distillation": r"knowledge distillation|distill",
    "peft-lora": r"\bLoRA\b|parameter[- ]efficient fine[- ]tuning|PEFT",
    "any-resolution": r"any[- ]resolution|native resolution|dynamic resolution|arbitrary resolution",
    "high-resolution": r"high[- ]resolution",
    "visual-encoder": r"visual encoder|vision encoder|image encoder",
    "connector-projector": r"projector|connector module|cross[- ]modal connector",
    "in-context-learning": r"in[- ]context learning",
    "clip": r"\bCLIP\b|SigLIP|EVA[- ]CLIP",
    "contrastive-pretraining": r"contrastive (language[- ]image|pre[- ]?training)",
    "image-text-alignment": r"image[- ]text align|vision[- ]language align",
    "zero-shot": r"zero[- ]shot",
    "open-vocabulary": r"open[- ]vocabular",
    "prompt-tuning": r"prompt (tuning|learning)",
    # 주의: 아래 4개는 원래 \badapter\b / grounding / referring 처럼 넓어서
    #       "논문에 흔히 쓰이는 일반 단어"까지 잡았음 → 주제어 형태로 한정
    "adapter": r"adapter (module|layer|tuning|fine[- ]tuning)|adapter[- ]based|lightweight adapter",
    "visual-grounding": r"visual grounding|referring expression|phrase grounding|grounding (task|module|head)",
    "referring": r"referring (expression|segmentation|image)|region[- ]level",
    "document-understanding": r"document understanding|document AI",
    "ocr": r"\bOCR\b|text recognition|optical character",
    "chart-understanding": r"chart (understanding|QA|reasoning)|table understanding",
    "video-llm": r"video[- ](LLM|language model)|video understanding|video MLLM",
    "3d-vlm": r"\b3D (VLM|scene|point cloud).*language|3D multimodal",
    "rag-vlm": r"retrieval[- ]augmented",
    "multimodal-cot": r"chain[- ]of[- ]thought|multimodal reasoning chain",
    # "reasoning" 단독은 초록의 36%에 걸렸음 → 수식어가 붙은 주제어만 인정
    "reasoning": r"(multimodal|visual|spatial|temporal|mathematical|geometric|compositional|"
                 r"commonsense|step[- ]by[- ]step|long[- ]horizon) reasoning|"
                 r"reasoning (capabilit|abilit|chain|step|path|trace)",
    "agent-tool-use": r"\bagent\b|tool use|tool[- ]calling",
    "hallucination": r"hallucinat",
    "alignment-rlhf": r"\bRLHF\b|preference alignment|human feedback",
    "dpo": r"\bDPO\b|direct preference optimization",
    "safety": r"\bsafety\b|jailbreak|adversarial (attack|robust|example|perturbation)",
    # "benchmark"/"evaluat" 단독은 각각 48%/44%에 걸렸음 → 기여·주제로 한정
    "benchmark": r"(new|novel|comprehensive|challenging|large[- ]scale) benchmark|"
                 r"benchmark (dataset|suite|for evaluating|to evaluate)|"
                 r"we (introduce|present|propose|construct|build|release)[^.]{0,60}benchmark",
    "evaluation": r"evaluation (protocol|framework|metric|methodolog|paradigm|suite|pipeline)|"
                  r"(automatic|automated|human|holistic|fine[- ]grained) evaluation|"
                  r"LLM[- ]as[- ]a[- ]judge|evaluat\w* (bias|reliabilit|consistenc)",
    "open-vocab-detection": r"open[- ]vocabulary detection|open[- ]set detection",
    "open-vocab-segmentation": r"open[- ]vocabulary segmentation",
    "vla": r"vision[- ]language[- ]action|\bVLA\b",
    "embodied": r"embodied",
    "robotics": r"robot",
    "medical-vlm": r"medical (VLM|vision[- ]language|multimodal)|radiolog",
    "autonomous-driving": r"autonomous driving|self[- ]driving",
}
COMPILED = {k: re.compile(v, re.I) for k, v in KW_PATTERNS.items()}

# ── 키워드 -> 클러스터(색상 그룹) 매핑 ────────────────────────────────
KW_CLUSTER = {
    "efficient-vlm":"EFF","lightweight-vlm":"EFF","small-vlm":"EFF","on-device":"EFF",
    "mobile-vlm":"EFF","low-power":"EFF","token-pruning":"EFF","token-merging":"EFF",
    "kv-cache":"EFF","quantization":"EFF","knowledge-distillation":"EFF","peft-lora":"EFF",
    "mllm":"MLLM","vision-language-model":"MLLM","visual-instruction-tuning":"MLLM",
    "any-resolution":"MLLM","visual-encoder":"MLLM","connector-projector":"MLLM",
    "in-context-learning":"MLLM",
    "clip":"BASE","contrastive-pretraining":"BASE","image-text-alignment":"BASE",
    "zero-shot":"BASE","open-vocabulary":"BASE","prompt-tuning":"BASE","adapter":"BASE",
    "high-resolution":"CAP","visual-grounding":"CAP","referring":"CAP",
    "document-understanding":"CAP","ocr":"CAP","chart-understanding":"CAP","video-llm":"CAP",
    "3d-vlm":"CAP","rag-vlm":"CAP","multimodal-cot":"CAP","reasoning":"CAP","agent-tool-use":"CAP",
    "hallucination":"REL","alignment-rlhf":"REL","dpo":"REL","safety":"REL",
    "benchmark":"REL","evaluation":"REL",
    "open-vocab-detection":"APP","open-vocab-segmentation":"APP","vla":"APP",
    "embodied":"APP","robotics":"APP","medical-vlm":"APP","autonomous-driving":"APP",
}
CLUSTER_NAME = {
    "EFF":"효율·경량 (★두 번째 논문)","MLLM":"MLLM 시대(핵심)","BASE":"기반·연속(CLIP계)",
    "CAP":"능력 확장","REL":"정렬·신뢰성","APP":"응용 태스크",
}

def extract_keywords(text):
    return {k for k, rx in COMPILED.items() if rx.search(text)}

# ── 캐시 I/O ────────────────────────────────────────────────────────
def load_cache():
    if not os.path.exists(RAW_CACHE):
        return {}, []
    with open(RAW_CACHE, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("papers", {}), d.get("done_queries", [])

def save_cache(papers, done):
    tmp = RAW_CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"papers": papers, "done_queries": done}, f, ensure_ascii=False)
    os.replace(tmp, RAW_CACHE)   # 원자적 교체 — 중간에 죽어도 캐시 안 깨짐

# ── arXiv 수집 ──────────────────────────────────────────────────────
def harvest():
    import arxiv  # pip install arxiv
    client = arxiv.Client(page_size=PAGE_SIZE, delay_seconds=DELAY, num_retries=5)
    papers, done = load_cache()
    if papers:
        print(f"[캐시] 기존 {len(papers)}편 / 완료 쿼리 {len(done)}개 — 이어서 진행\n", flush=True)

    # 작업 단위 = (캐시 키, 실제 쿼리문). 대형 쿼리는 연 단위로 쪼갠다.
    jobs = []
    for q in QUERIES:
        if q in SPLIT_QUERIES:
            for a, b in SPLIT_WINDOWS:
                jobs.append((f"{q} @{a[:4]}", f"({q}) AND submittedDate:[{a} TO {b}]"))
        else:
            jobs.append((q, f"({q}) AND submittedDate:[{DATE_FROM} TO {DATE_TO}]"))

    t0 = time.time()
    for i, (key, full_q) in enumerate(jobs, 1):
        if key in done:
            print(f"[{i:>2}/{len(jobs)}] (건너뜀) {key}", flush=True)
            continue
        print(f"[{i:>2}/{len(jobs)}] {key}", flush=True)
        for attempt in range(1, RETRIES + 1):
            got = 0
            try:
                search = arxiv.Search(query=full_q, max_results=MAX_PER_QUERY,
                                      sort_by=arxiv.SortCriterion.SubmittedDate)
                for r in client.results(search):
                    aid = r.get_short_id().split("v")[0]
                    got += 1
                    if aid in papers:
                        continue
                    papers[aid] = {
                        "id": aid,
                        "title": r.title.strip().replace("\n", " "),
                        "date": r.published.strftime("%Y-%m-%d"),
                        "primary": r.primary_category,
                        "cats": " ".join(r.categories),
                        "abstract": r.summary.strip().replace("\n", " "),
                    }
                done.append(key)
                break
            except Exception as e:
                wait = BACKOFF * attempt
                print(f"   ! 실패 {attempt}/{RETRIES} ({type(e).__name__}: {e})", flush=True)
                if attempt < RETRIES:
                    print(f"     {wait}초 대기 후 재시도", flush=True)
                    save_cache(papers, done)   # 대기 전에 확보분 저장
                    time.sleep(wait)
                else:
                    print(f"     포기 — 부분 수집분만 유지(재실행하면 이 쿼리부터 다시 시도)", flush=True)
        save_cache(papers, done)   # 쿼리마다 체크포인트
        el = int(time.time() - t0)
        print(f"   -> {got}편 조회 / 누적 고유 {len(papers)}편 / 경과 {el//60}분{el%60}초", flush=True)

    missing = [k for k, _ in jobs if k not in done]
    print(f"\n총 {len(papers)}편 수집(중복 제거). 미완료 작업 {len(missing)}개", flush=True)
    for m in missing:
        print(f"  · {m}", flush=True)
    return papers, done

# ── 분석 & export ───────────────────────────────────────────────────
def analyze(papers_dict):
    papers = list(papers_dict.values())
    for p in papers:                     # 태깅은 항상 캐시된 원문에서 다시 계산
        p["keywords"] = sorted(extract_keywords(f"{p['title']}\n{p['abstract']}"))

    if USE_YAKE:
        try:
            import yake
            kw = yake.KeywordExtractor(lan="en", n=3, top=8)
            for p in papers:
                p["free_keywords"] = [w.lower() for w, _ in kw.extract_keywords(p["abstract"])]
        except ImportError:
            print("(yake 미설치 — 자유 키워드 건너뜀)")

    freq = Counter(); co = defaultdict(int)
    for p in papers:
        kws = p["keywords"]
        for k in kws: freq[k] += 1
        for a, b in itertools.combinations(sorted(set(kws)), 2): co[(a, b)] += 1

    # papers.csv  (초록 포함 — 스크리닝·매트릭스 추출용)
    with open("papers.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["id","date","primary","cats","title","keywords","abstract"])
        for p in sorted(papers, key=lambda x: x["date"]):
            w.writerow([p["id"], p["date"], p["primary"], p.get("cats",""),
                        p["title"], ";".join(p["keywords"]), p["abstract"]])
    # keyword_freq.csv
    with open("keyword_freq.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["keyword","cluster","count","share_pct"])
        for k, c in freq.most_common():
            w.writerow([k, KW_CLUSTER.get(k,"ETC"), c, round(c/len(papers)*100, 1)])
    # cooccurrence.csv
    with open("cooccurrence.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["kw_a","kw_b","weight"])
        for (a, b), c in sorted(co.items(), key=lambda x: -x[1]): w.writerow([a, b, c])
    # ── 역피라미드 스크리닝(PRISMA 숫자) ─────────────────────────────
    # 키워드 임계값이 아니라 "논문"을 거르는 깔때기. 서베이 방법론 3단계용.
    CORE = {"mllm","vision-language-model","visual-instruction-tuning"}
    EFF  = {k for k, c in KW_CLUSTER.items() if c == "EFF"}
    DEPLOY = {"on-device","mobile-vlm","low-power","lightweight-vlm","small-vlm"}
    def has(p, s, n=1): return len(set(p["keywords"]) & s) >= n

    stage = [
        ("① 식별 — arXiv 22개 쿼리, 중복 제거", papers),
        ("② 주제 적합 — VLM/MLLM 핵심어 1개 이상", [p for p in papers if has(p, CORE)]),
        ("③ 효율 관련 — 효율·경량 키워드 1개 이상", [p for p in papers if has(p, CORE) and has(p, EFF)]),
        ("④ 효율 집중 — 효율·경량 키워드 2개 이상", [p for p in papers if has(p, CORE) and has(p, EFF, 2)]),
        ("⑤ 배포·경량 코어 — 온디바이스/모바일/저전력/소형", [p for p in papers if has(p, CORE) and has(p, DEPLOY)]),
    ]
    with open("screening.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["stage","count"])
        for name, ps in stage: w.writerow([name, len(ps)])
    # 정독 후보(④단계)를 따로 뽑아둠 — 매트릭스 추출의 출발점
    with open("shortlist_efficiency.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["id","date","primary","title","keywords","abstract"])
        for p in sorted(stage[3][1], key=lambda x: x["date"], reverse=True):
            w.writerow([p["id"], p["date"], p["primary"], p["title"],
                        ";".join(p["keywords"]), p["abstract"]])

    # network.gexf (Gephi/VOSviewer)
    kept = {k for k, c in freq.items() if c >= MIN_OCCURRENCE}
    with open("network.gexf", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<gexf version="1.2">'
                '<graph mode="static" defaultedgetype="undirected">\n<nodes>\n')
        for k in kept: f.write(f'<node id="{k}" label="{k}"/>\n')
        f.write('</nodes>\n<edges>\n')
        for i, ((a, b), c) in enumerate(co.items()):
            if a in kept and b in kept:
                f.write(f'<edge id="{i}" source="{a}" target="{b}" weight="{c}"/>\n')
        f.write('</edges>\n</graph></gexf>\n')
    # pilot_data.json (generate_viz.py 재사용) — 클러스터·역피라미드 스윕 포함
    nodes = [{"id": k, "label": k, "value": freq[k],
              "group": KW_CLUSTER.get(k, "ETC"),
              "groupName": CLUSTER_NAME.get(KW_CLUSTER.get(k, "ETC"), "기타")} for k in kept]
    edges = [{"from": a, "to": b, "value": c} for (a, b), c in co.items()
             if a in kept and b in kept and c >= MIN_EDGE]
    sweep_pts = (1, 10, 25, 50, 100, 200, 400, 800)
    sweep = {t: sum(1 for c in freq.values() if c >= t) for t in sweep_pts}
    by_year = Counter(p["date"][:4] for p in papers)     # 타임라인 그림용
    with open("pilot_data.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": sorted(nodes, key=lambda n: -n["value"]), "edges": edges,
                   "clusters": CLUSTER_NAME,
                   "meta": {"papers": len(papers), "threshold": MIN_OCCURRENCE,
                            "kept": len(nodes), "edges": len(edges), "sweep": sweep,
                            "by_year": dict(sorted(by_year.items())),
                            "date_from": DATE_FROM[:8], "date_to": DATE_TO[:8]}},
                  f, ensure_ascii=False, indent=1)

    print(f"\n논문 {len(papers)}편 · 고유 키워드 {len(freq)}개 · min>={MIN_OCCURRENCE} 통과 {len(kept)}개")
    print(f"엣지 {len(edges)}개 (min>={MIN_EDGE})")
    print("── 연도별 ──")
    for y, c in sorted(by_year.items()): print(f"  {y}: {c}편")
    print("── 역피라미드 스크리닝 (논문 단위 · PRISMA용) ──")
    base = len(stage[0][1])
    for name, ps in stage:
        print(f"  {name}: {len(ps):,}편 ({len(ps)/base*100:.1f}%)")
    print(f"  → 정독 후보 shortlist_efficiency.csv 에 {len(stage[3][1]):,}편 저장")
    print("── 키워드 임계값 스윕 ──")
    for t in sweep_pts: print(f"  min>={t:>3}: {sweep[t]}개")
    print("── 중심 TOP 20 ──")
    for k, c in freq.most_common(20):
        print(f"  {c:>5}  ({c/len(papers)*100:>4.1f}%)  {k:<26} [{KW_CLUSTER.get(k,'ETC')}]")

if __name__ == "__main__":
    if "--analyze" in sys.argv:
        ps, _ = load_cache()
        if not ps:
            sys.exit(f"{RAW_CACHE} 가 없음 — 먼저 수집을 실행하세요.")
        print(f"[재분석] 캐시 {len(ps)}편")
    else:
        ps, _ = harvest()
    analyze(ps)
    print("\n완료: papers.csv / keyword_freq.csv / cooccurrence.csv / network.gexf / pilot_data.json")

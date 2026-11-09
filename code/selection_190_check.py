# -*- coding: utf-8 -*-
"""압축 2차 목록(카드 61장)을 모델이 190편에서 고른 단계의 기록 대조. 새 판정 없음 — 기존 파일과 정규식만 사용.
   (1) 190편 재현: 2026-09-20 세션에서 쓴 필터(아래 F1·F2, 세션 기록에서 그대로 옮김)를 papers_raw.json 에 다시 돌려 794 → 382 → 190 과
       main_survey/candidates_4.3_pool.json 의 id 가 같은지.
   (2) 61장(main_survey/candidates_4.3_curated.csv)이 190 안에 있는지, 하위 분류(sub)·추천(rec=★) 수.
   (3) 190 중 61 에 없는 편(고르지 않은 편): 다른 카드 시트(sheets/sheet_4.[1-5]*.csv, 618장)에 올라 1저자 판정을 받았는지(screening_marks_export.csv), 한 번도 카드에 안 오른 수.
   (4) 190·61·고르지 않은 편 중 지금 규칙(main_taxonomy.py 4.3 엄격 = 제안 문장 또는 제목)·VLM 전체·효율 풀에 드는 수, 연도·제목 용어 분포.
   (5) 최종 69편(71항목, main_survey/matrix_4.*.csv) 중 190·61·고르지 않은 편에서 온 수, 압축 표(4.3) 항목 중 61 밖에서 온 것.
   실행: python h_selection_check.py --root <VLM-Survey 폴더> --out <출력 폴더>   → h_selection.json, h_unselected.csv"""
import argparse, collections, csv, glob, json, os, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
ROOT, OUT = os.path.abspath(a.root), os.path.abspath(a.out); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, ROOT)
import ast, types
_st = ast.parse(open(os.path.join(ROOT, "strict_tags.py"), encoding="utf-8").read()); _m = types.ModuleType("strict_tags")
exec(compile(ast.Module([n for n in _st.body if isinstance(n, ast.FunctionDef) and n.name == "fisher_exact"], []), "strict_tags.py(fisher_exact)", "exec"), _m.__dict__)
sys.modules["strict_tags"] = _m   # strict_tags 를 그대로 import 하면 medical_taxonomy 가 실행돼 medical_taxonomy_counts.csv 를 다시 씀 → fisher_exact 만 가져옴
SRC = open(os.path.join(ROOT, "main_taxonomy.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(ROOT, "main_taxonomy.py"), "__name__": "taxonomy_rules"}
exec(compile(SRC[:SRC.index("def analyse(")], "main_taxonomy.py(head)", "exec"), ns)   # chdir(ROOT) 포함, 결과 파일은 안 씀
rd = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig")))
R = {}

# (1) 9/20 필터 재현 — F1(세션 9/20 06:28:27), F2(06:28:45). 정규식은 한 글자도 바꾸지 말 것
P = list(json.load(open("papers_raw.json", encoding="utf-8"))["papers"].values())
vlm = re.compile(r"vision[- ]language|\bVLMs?\b|\bLVLMs?\b|multimodal (large )?language model|\bMLLMs?\b|\bVLA\b|vision-language-action", re.I)
comp = re.compile(r"quantiz|\bprun|low[- ]rank|\bSVD\b|singular value|binariz|\b[1-4]-bit\b|W[248]A(4|8|16)|INT[248]\b|structur\w+ (prun|compress)|compress(ing|ion)? (of |the )?(model|weights?|VLM|MLLM|LVLM|vision)|knowledge distill|distill\w+ (into|to) (a )?(smaller|compact|lightweight|tiny|student)|(compact|lightweight|small) (student|model) (via|through|by) distill", re.I)
excl = re.compile(r"vector[- ]quantiz|\bVQ\b|codebook|tokeniz|action quantiz|quantized (depth|action|prompt)|residual quantiz|discretiz|recommend|watermark|unlearn|attack|privacy|federated|carbon|speech|audio", re.I)
s1 = [p for p in P if vlm.search(p["title"] + " " + p["abstract"][:400]) and comp.search(p["title"] + ". " + p["abstract"]) and not excl.search(p["title"])]
tcomp = re.compile(r"quantiz|\bprun|low[- ]rank|\bSVD\b|binariz|\b\d(\.\d)?-bit\b|W\dA\d|INT[248]\b|compress|distill|sparsif|slim|lightweight|compact|tiny|small", re.I)
tvlm = re.compile(r"vision[- ]language|\bVLMs?\b|\bLVLMs?\b|multimodal|\bMLLMs?\b|\bVLA\b|CLIP|SigLIP|LLaVA", re.I)
s2 = [p for p in s1 if tcomp.search(p["title"]) and tvlm.search(p["title"] + " " + p["abstract"][:200])]
excl2 = re.compile(r"token|KV cache|cache|video|streaming|dataset distill|data distill|reasoning|CoT|chain-of-thought|prompt (distill|learn|tun)|LoRA|adapter|fine-tun|PEFT|edit|generation|diffusion", re.I)
s3 = [p for p in s2 if not excl2.search(p["title"])]
POOL = [x["id"] for x in json.load(open("main_survey/candidates_4.3_pool.json", encoding="utf-8"))]
R["reproduce"] = dict(step1=len(s1), step2=len(s2), step3=len(s3), saved_pool=len(POOL), identical=set(POOL) == {p["id"] for p in s3})
print("(1)", R["reproduce"])
P190 = set(POOL); byid = {p["id"]: p for p in P}

# (2) 61장
CUR = rd("main_survey/candidates_4.3_curated.csv"); C61 = {r["id"] for r in CUR}
old244 = {r["id"] for r in rd("main_survey/candidates_4.3_strict.csv")}   # 같은 날 먼저 만든 244편 목록(F1 이전의 다른 정규식)
CARDS0 = collections.defaultdict(list)
for f in sorted(glob.glob("sheets/sheet_4.[1-5]*.csv")):
    for r in rd(f):
        if not os.path.basename(f).startswith("sheet_4.3R"): CARDS0[r["id"]].append(os.path.basename(f)[6:].split("_")[0])
R["curated"] = dict(n=len(CUR), unique=len(C61), in_190=len(C61 & P190), outside_190=sorted(C61 - P190),
                    outside_190_detail={i: dict(title=byid[i]["title"], in_earlier_244=i in old244, other_cards=CARDS0.get(i, []), step1=i in {p["id"] for p in s1}, step2=i in {p["id"] for p in s2}) for i in sorted(C61 - P190)},
                    sub=dict(collections.Counter(r["sub"] for r in CUR)), recommended=sum(r["rec"] == "★" for r in CUR))
U129 = P190 - C61
print("(2)", R["curated"])

# (3) 카드·판정
CARDS = collections.defaultdict(list)
for f in sorted(glob.glob("sheets/sheet_4.[1-5]*.csv")):
    sh = os.path.basename(f)[6:].split("_")[0]
    for r in rd(f): CARDS[r["id"]].append(sh)
MK = collections.defaultdict(list)
for r in rd("screening_marks_export.csv"): MK[r["id"]].append((r["b"], r["mark"]))
carded = {i for i in U129 if CARDS.get(i)}
R["unselected"] = dict(n=len(U129), carded_elsewhere=len(carded), never_carded=len(U129 - carded),
                       carded_sheets=dict(collections.Counter(s for i in carded for s in CARDS[i])),
                       carded_marks=dict(collections.Counter(m for i in carded for _, m in MK.get(i, [])) ),
                       carded_kept_ids=sorted(i for i in carded if any(m in ("keep", "star") for _, m in MK.get(i, []))))
R["cards_total"] = dict(cards=sum(len(v) for v in CARDS.values()), unique=len(CARDS), marks_rows=sum(len(v) for v in MK.values()))
R["sheet_4.3R_verdicts"] = dict(collections.Counter(m for i in C61 for b, m in MK.get(i, []) if b == "4.3R"))
print("(3)", R["unselected"], R["cards_total"], "4.3R", R["sheet_4.3R_verdicts"])

# (4) 지금 규칙(v2.1)과의 관계
_, _, loose43, strict43, _ = next(r for r in ns["RX"] if r[0] == "4.3")
CORE = {p["id"] for p in ns["core"]}; POOLE = {p["id"] for p in ns["pool"]}
def t(p): return p["title"] + ". " + p["abstract"]
st43 = lambda i: bool(strict43.search(t(byid[i])) or loose43.search(byid[i]["title"]))
lo43 = lambda i: bool(loose43.search(t(byid[i])))
def term(title):
    for k, rx in (("quantization", r"quantiz|\b\d(\.\d)?-bit\b|W\dA\d|INT[248]\b|binariz"), ("pruning/sparsity", r"\bprun|sparsif"), ("low-rank/SVD", r"low[- ]rank|\bSVD\b"),
                  ("distillation", r"distill"), ("compression (general)", r"compress"), ("other title term", r".")):
        if re.search(rx, title, re.I): return k
def prof(S):
    return dict(n=len(S), strict43_v21=sum(map(st43, S)), loose43_v21=sum(map(lo43, S)), in_vlm_corpus=len(S & CORE), in_eff_pool=len(S & POOLE),
                year=dict(sorted(collections.Counter(byid[i]["date"][:4] for i in S).items())), title_term=dict(collections.Counter(term(byid[i]["title"]) for i in S)))
R["profile"] = {"190": prof(P190), "61_in_190": prof(C61 & P190), "unselected": prof(U129)}
for k, v in R["profile"].items(): print("(4)", k, v)
R["earlier_244_list"] = dict(n=len(old244), overlap_190=len(old244 & P190), overlap_61=len(old244 & C61))

# (5) 최종 69편(71항목)
FIN = collections.defaultdict(set)
for f in sorted(glob.glob("main_survey/matrix_4.*.csv")):
    for r in rd(f): FIN[os.path.basename(f)[7:10]].add(r["id"])
ALL = set().union(*FIN.values())
R["final"] = dict(entries=sum(len(v) for v in FIN.values()), papers=len(ALL), from_190=len(ALL & P190), from_61=len(ALL & C61), from_unselected=sorted(ALL & U129),
                  compression_table=len(FIN["4.3"]), compression_from_61=len(FIN["4.3"] & C61), compression_not_from_61=sorted(FIN["4.3"] - C61),
                  compression_not_from_61_cards={i: CARDS.get(i, []) for i in sorted(FIN["4.3"] - C61)})
print("(5)", R["final"])
json.dump(R, open(os.path.join(OUT, "h_selection.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.join(OUT, "h_unselected.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["id", "date", "title", "title_term", "strict43_v21", "in_vlm_corpus", "in_eff_pool", "cards", "marks"])
    for i in sorted(U129, key=lambda i: byid[i]["date"]):
        p = byid[i]; w.writerow([i, p["date"][:10], p["title"], term(p["title"]), int(st43(i)), int(i in CORE), int(i in POOLE), ";".join(CARDS.get(i, [])), ";".join(f"{b}:{m}" for b, m in MK.get(i, []))])
print("done", OUT)

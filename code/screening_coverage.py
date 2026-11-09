# -*- coding: utf-8 -*-
"""스크리닝 후보가 어떻게 정해졌는지(1차 순위 목록)와 효율 풀 중 카드에 오른 범위. 새 판정 없음 — 기존 시트·코드만 사용.
   1차 목록은 build_sheets.py(2일차)가 만들었다: 효율 풀의 각 논문을 가지별 가중 패턴 점수가 가장 높은 가지 하나에 배정하고,
   가지마다 점수 상위 CAP(60)편(동점은 최신순) + 나머지 중 인용 상위 CITE_CAP(15)편(citations.json, Semantic Scholar)을 카드로 만들었다.
   여기서는 build_sheets.py 의 출력 앞부분(os.makedirs(OUTDIR) 전)만 실행해 배정·순위를 다시 계산하고, 지금 시트(sheets/sheet_4.[1-5]_*.csv)와 같은지 확인한다(다르면 멈춤).
   출력: main_survey/screening_coverage/coverage.json(가지별 배정 수·카드 수, 풀 중 카드에 오른 편수, 1차 패턴·가중치, 96편의 1차 위치)
   실행: python screening_coverage.py"""
import collections, contextlib, csv, glob, io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = "main_survey/screening_coverage"; os.makedirs(OUT, exist_ok=True)
SRC = open("build_sheets.py", encoding="utf-8").read()
ns = {"__name__": "build_sheets_head", "__file__": "build_sheets.py"}
exec(compile(SRC[:SRC.index("os.makedirs(OUTDIR, exist_ok=True)")], "build_sheets.py(head)", "exec"), ns)   # 시트는 쓰지 않음
POOL = ns["pool"]; PID = {p["id"] for p in POOL}; byid = {p["id"]: p for p in POOL}; CAP, CCAP = ns["CAP"], ns["CITE_CAP"]
rd = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig")))
CARDS = collections.defaultdict(set)
for f in sorted(glob.glob("sheets/sheet_4.[1-5]*.csv")):
    CARDS[os.path.basename(f)[6:].split("_")[0]] |= {r["id"] for r in rd(f)}
R1 = {}
for b, lab, _ in ns["COMPILED"]:
    rows = sorted([p for p in POOL if p["primary"] == b], key=lambda p: (p["sc"][b], p["date"]), reverse=True)
    top = [p["id"] for p in rows[:CAP]]
    cited = sorted([p for p in rows if p["id"] not in set(top) and ns["CIT"].get(p["id"], {}).get("c")], key=lambda p: -ns["CIT"][p["id"]]["c"])[:CCAP]
    exp = set(top) | {p["id"] for p in cited}
    assert exp == CARDS[b], (b, len(exp), len(CARDS[b]))   # 지금 1차 시트와 같아야 함
    R1[b] = dict(assigned=len(rows), cards=len(exp), by_score=len(top), by_citation=len(cited), rank={p["id"]: i + 1 for i, p in enumerate(rows)})
ALL = set().union(*CARDS.values())
U = [r for r in rd("main_survey/selection_190/h_unselected.csv") if not r["cards"]]
def where(i):
    p = byid.get(i)
    if p is None: return "outside_pool"
    if p["primary"] is None: return "pool_no_branch_score"
    return f"pool_assigned_{p['primary']}"
W = collections.Counter(where(r["id"]) for r in U)
R = dict(cap=CAP, cite_cap=CCAP, pool=len(POOL), citations_cached=len(ns["CIT"]),
         round1={b: {k: v for k, v in d.items() if k != "rank"} for b, d in R1.items()},
         cards_unique=len(ALL), cards_in_pool=len(ALL & PID), cards_outside_pool=len(ALL - PID), pool_never_carded=len(PID - ALL),
         patterns=[dict(branch=b, label=lab, pattern=p, weight=w, name=n) for b, lab, pats in ns["BRANCHES"] for p, w, n in pats],
         never_screened_96=dict(n=len(U), where=dict(W), outside_pool=W["outside_pool"], strict43=sum(r["strict43_v21"] == "1" for r in U),
                                rank_in_compression_round1=sorted(R1["4.3"]["rank"][r["id"]] for r in U if where(r["id"]) == "pool_assigned_4.3")))
assert R["cards_unique"] == 475 and sum(len(v) for v in CARDS.values()) == 618
json.dump(R, open(f"{OUT}/coverage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v for k, v in R.items() if k not in ("patterns",)})

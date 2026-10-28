# -*- coding: utf-8 -*-
"""10/21 2차 평가자 판정의 신뢰성 점검(읽기만). (1) 빈칸·모순(Q1 아니오인데 Q2 예, B 시트에서 엄격 ⊄ 느슨),
   (2) 등급 시트 Q2 '예'의 근거 위치가 원문(main_survey/txt)에 실제로 있는지 — 적어 준 표·그림 번호와 단위·키워드를 전문에서 찾음,
   (3) Q1 링크가 실제 저장소인지(적힌 URL 이 우리 code-link 점검 결과와 같은 저장소인지). 출력은 화면.
   실행: python main_survey/second_rater/check_r2_reliability.py"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); HERE = os.path.dirname(os.path.abspath(__file__)); MS = os.path.dirname(HERE)
from openpyxl import load_workbook
yn = lambda v: True if str(v or "").strip().startswith("예") else (False if str(v or "").strip().startswith("아니") else None)
main = load_workbook(os.path.join(HERE, "second_rater_classification.xlsx"), data_only=True)
grade = load_workbook(os.path.join(HERE, "second_rater_grades.xlsx"), data_only=True)
print("== (1) 빈칸·모순")
for sh in ("A", "C"):
    ws = main[sh]; head = [c.value for c in ws[1]]; q1, q2, memo = head.index("Q1 다루는가"), head.index("Q2 엄격"), head.index("메모")
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    blank = [r[0] for r in rows if yn(r[q1]) is None or yn(r[q2]) is None]
    contra = [r[0] for r in rows if yn(r[q1]) is False and yn(r[q2]) is True]
    memos = sum(1 for r in rows if r[memo])
    print(f"  시트 {sh}: {len(rows)}행, 빈칸 {blank or '없음'}, Q1 아니오·Q2 예 모순 {contra or '없음'}, 메모 {memos}개, Q1 예 {sum(yn(r[q1]) is True for r in rows)}, Q2 예 {sum(yn(r[q2]) is True for r in rows)}")
ws = main["B"]; head = [c.value for c in ws[1]]
lo, st = head.index("다루는 분야 (예: 4.2, 4.4 / 없음)"), head.index("엄격까지 만족하는 분야")
codes = lambda v: set() if "없" in str(v or "") else set(re.findall(r"4\.[1-6]", str(v or "")))
bad = [(r[0], r[lo], r[st]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and not codes(r[st]) <= codes(r[lo])]
blankB = [r[0] for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and (r[lo] in (None, "") or r[st] in (None, ""))]
print(f"  시트 B: 빈칸 {blankB or '없음'}, 엄격이 느슨에 포함되지 않는 행 {bad or '없음'}")
print("== (2) 등급 시트 Q2 근거 위치가 원문에 있는가")
gs = grade["등급"]; head = [c.value for c in gs[1]]
KEY = {int(k["new_row"]): int(k["orig_row"]) for k in csv.DictReader(open(os.path.join(HERE, "key_second_rater.csv"), encoding="utf-8-sig")) if k["sheet"] == "G"}
KG = {int(k["row"]): k for k in csv.DictReader(open(os.path.join(MS, "gradeval", "answer_key_grade.csv"), encoding="utf-8-sig"))}
for r in gs.iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    n = int(r[0]); g = KG[KEY[n]]; aid = g["arxiv_id"]; ev = str(r[head.index("Q2 근거 위치")] or ""); q2 = yn(r[head.index("Q2 측정 비용 (예/아니오)")])
    txt_p = os.path.join(MS, "txt", f"{aid}.txt"); T = open(txt_p, encoding="utf-8", errors="ignore").read() if os.path.exists(txt_p) else ""
    refs = re.findall(r"(?:표|Table|그림|Fig(?:ure)?\.?)\s*(\d+)", ev)
    found = [x for x in refs if re.search(rf"(?:Table|Tab\.|Figure|Fig\.)\s*{x}\b", T)]
    units = re.findall(r"(GPU[- ]?(?:hours|days)|GiB|GB|ms|tokens/s|samples/s|latency|throughput|speed-?up|Memory|Time|TTFT|prefill)", ev, re.I)
    ufound = [u for u in dict.fromkeys(units) if re.search(re.escape(u), T, re.I)]
    nums = [x for x in re.findall(r"\d+(?:\.\d+)?", ev) if len(x) >= 3 or "." in x]
    nfound = [x for x in nums if x in T]
    print(f"  #{n:2d} {g['name'][:22]:22} Q2={'예' if q2 else '아니오'} | 표·그림 {refs}→원문 {found} | 단위 {list(dict.fromkeys(units))[:4]}→{ufound[:4]} | 숫자 {nums[:5]}→{nfound[:5]}")

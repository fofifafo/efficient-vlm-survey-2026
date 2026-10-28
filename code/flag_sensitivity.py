# -*- coding: utf-8 -*-
"""외부 리뷰(10/25) 대응 — 모델 '추천' 표시 민감도. 새 판정 없음.
   어느 카드에서든 추천 표시(rec=True)를 받은 최종 논문을 빼고(보수적 정의: Nav-EE 는 표시된 2차 카드는 skip, 표시 없는 1차 카드로 keep), 남은 항목의 등급 분포를 전체와 비교.
   입력: screening_marks_export.csv, main_survey/gradeval/answer_key_grade.csv(최종 69편·71항목 등급).
   출력: main_survey/flag_sensitivity.json. 실행: python flag_sensitivity.py"""
import collections, csv, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
V = list(csv.DictReader(open("screening_marks_export.csv", encoding="utf-8-sig")))
G = list(csv.DictReader(open("main_survey/gradeval/answer_key_grade.csv", encoding="utf-8-sig")))
flag = {r["id"] for r in V if r["rec"] == "True"}
final = {g["arxiv_id"] for g in G}
def dist(rows):
    c = collections.Counter(); n = 0
    for g in rows:
        k = int(g["entries"]); c[g["grade"]] += k; n += k
    return dict(n=n, **{x: c[x] for x in "ABC"}, A_pct=round(100 * c["A"] / n), C_pct=round(100 * c["C"] / n))
out = dict(flagged_kept_cards=sum(r["rec"] == "True" and r["mark"] in ("keep", "star") for r in V), flagged_final_papers=len(flag & final),
           all=dist(G), without_flagged=dist([g for g in G if g["arxiv_id"] not in flag]), flagged_only=dist([g for g in G if g["arxiv_id"] in flag]))
json.dump(out, open("main_survey/flag_sensitivity.json", "w", encoding="utf-8"), indent=1); print(json.dumps(out))

# -*- coding: utf-8 -*-
"""2차 평가자 부분 이중 판정 시트(2026-10-14). 1차 평가자(제1저자)가 전부 판정한 표본에서 무작위 일부만 독립 판정.
   C1 시트 A(정밀도) 300행 중 60행: 가지마다 10행(가지 안 무작위).  C1 시트 B(재현율) 100행 중 20행.
   C 분류 v2.1 새 표본 55행 중 11행.  C2 등급 69편 중 20편: 우리 등급 비율(A/B/C)대로 층화 무작위. 시드 20261015.
   시트에는 1차 평가자 답·규칙 결과·우리 등급이 없다. 원래 행 번호는 key_second_rater.csv 에만(평가자에게 보내지 않음).
   출력: main_survey/second_rater/2차평가자_판정시트.xlsx, key_second_rater.csv
   채점: python main_survey/second_rater/score_second_rater.py <채운 시트.xlsx>"""
import csv, os, random, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); MS = os.path.dirname(HERE)
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
rng = random.Random(20261015)
src = load_workbook(os.path.join(MS, "classval", "분류검증_시트_평가자1.xlsx"))      # 빈 원본(답 없음)
A = [r for r in src["A_정밀도"].iter_rows(min_row=2, values_only=True) if r[0]]
B = [r for r in src["B_재현율"].iter_rows(min_row=2, values_only=True) if r[0]]
CRIT = [r for r in src["기준"].iter_rows(min_row=1, values_only=True)]
byb = collections.defaultdict(list)
for r in A: byb[r[1][:3]].append(r)
selA = sorted(sum((rng.sample(v, 10) for _, v in sorted(byb.items())), []), key=lambda r: r[0]); rng.shuffle(selA); selA.sort(key=lambda r: r[1][:3])
selB = rng.sample(B, 20)
KG = list(csv.DictReader(open(os.path.join(MS, "gradeval", "answer_key_grade.csv"), encoding="utf-8-sig")))
G = [r for r in load_workbook(os.path.join(MS, "gradeval", "등급검증_시트.xlsx"))["판정"].iter_rows(min_row=2, values_only=True) if r[0]]
gb = collections.defaultdict(list)
for k in KG: gb[k["grade"]].append(int(k["row"]))
quota = {"A": 10, "B": 3, "C": 7}
selG = sorted(sum((rng.sample(gb[g], quota[g]) for g in quota), [])); rng.shuffle(selG)
# 시트 C(10/15 추가): 분류 규칙 v2.1 새 표본 55행(classval/분류검증_새표본_평가자1.xlsx) 중 무작위 11행(20%)
R2 = [r for r in load_workbook(os.path.join(MS, "classval", "분류검증_새표본_평가자1.xlsx"))["A_정밀도"].iter_rows(min_row=2, values_only=True) if r[0]]
selC = sorted(rng.sample(R2, 11), key=lambda r: r[0])
with open(os.path.join(HERE, "key_second_rater.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["sheet", "new_row", "orig_row"])
    for i, r in enumerate(selA, 1): w.writerow(["A", i, r[0]])
    for i, r in enumerate(selB, 1): w.writerow(["B", i, r[0]])
    for i, r in enumerate(selG, 1): w.writerow(["G", i, r])
    for i, r in enumerate(selC, 1): w.writerow(["C", i, r[0]])
thin = Side(style="thin", color="BFBFBF"); YEL = PatternFill("solid", fgColor="FFF2CC"); GRY = PatternFill("solid", fgColor="E7E6E6")
def style(ws, widths, fill_cols, h):
    for j, wd in enumerate(widths, 1): ws.column_dimensions[chr(64 + j)].width = wd
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for c in ws[1]: c.font = Font(bold=True); c.fill = GRY
    for r in range(2, ws.max_row + 1):
        ws.row_dimensions[r].height = h
        for c in fill_cols: ws.cell(r, c).fill = YEL
wb = Workbook(); g = wb.active; g.title = "안내"
for line in ["효율적 VLM 서베이 — 2차 평가자 판정 시트. 도와주셔서 감사합니다. 총 2–2.5시간 정도 걸립니다.", "",
             "목적: 논문 분류 규칙과 근거 등급이 맞게 붙었는지 사람이 독립적으로 확인합니다. 다른 사람(제1저자 포함)의 판정은 보지 않고, 상의하지 않고, AI 도구 없이 직접 판단해 주세요.",
             "애매하면 기준 문서에 더 가까운 쪽을 고르고 메모 칸에 이유를 짧게 적어 주세요.", "",
             "[시트 A — 60행, 약 40분] 각 행에 적힌 분야 하나에 대해서만, 제목과 초록을 보고 판단합니다.",
             "   Q1 다루는가: 이 논문이 그 분야를 의도한 뜻으로 다루는가? (D열 기준)  → 예/아니오",
             "   Q2 엄격: 더 엄격한 기준(E열)을 만족하는가?  → 예/아니오.  Q1이 아니오면 Q2도 보통 아니오.",
             "   주의: '다룬다'(Q1)와 '제안한다'(Q2)는 다릅니다. 예: LoRA를 도구로 써서 다른 문제를 풀면 4.2 Q1 예, Q2 아니오.",
             "",
             "[시트 B — 20행, 약 20분] 분야가 정해져 있지 않습니다. 초록을 읽고",
             "   E열: 이 논문이 다루는 분야 번호를 모두 (예: 4.2, 4.4). 없으면 '없음'.  기준은 시트 A의 Q1과 같습니다.",
             "   F열: 그중 엄격 기준(Q2)까지 만족하는 분야 번호를 모두. 없으면 '없음'.",
             "",
             "[시트 C — 11행, 약 10분] 시트 A와 같은 방법(Q1·Q2). 분야는 4.3 압축, 4.5 배포만 있습니다.",
             "",
             "[시트 등급 — 20편, 약 1시간] arXiv 링크로 논문을 열어 두 가지만 확인합니다.",
             "   Q1 코드 공개: 논문에 코드 저장소 링크가 있고, 열었을 때 실제 코드가 있으면 예. 링크가 없거나 README만 있으면(\"coming soon\") 아니오. 모델 가중치와 실행 코드를 Hugging Face 등에 공개했으면 예.",
             "   Q2 측정 비용: 저자가 자기 시스템에서 직접 잰 시간(지연·속도 향상 배수·처리량·학습 시간) 또는 메모리 수치가 본문·표·그림에 있으면 예. FLOPs·파라미터 수·토큰 수만 있거나 다른 논문 수치 인용이면 아니오. 예이면 근거 위치(예: 표 3)를 적어 주세요.",
             "",
             "분야별 기준은 '기준' 시트에 있습니다. 다 하시면 파일을 저장해서 보내 주세요."]:
    g.append([line])
g.column_dimensions["A"].width = 150
k = wb.create_sheet("기준")
for r in CRIT: k.append(list(r))
style(k, [26, 80, 80], [], 60)
a = wb.create_sheet("A"); a.append(["번호", "분야", "arXiv", "Q1 기준", "Q2 기준", "제목", "초록", "Q1 다루는가", "Q2 엄격", "메모"])
for i, r in enumerate(selA, 1): a.append([i] + list(r[1:7]) + ["", "", ""])
style(a, [6, 14, 12, 30, 30, 30, 90, 10, 10, 20], [8, 9], 200)
dv = DataValidation(type="list", formula1='"예,아니오"', allow_blank=True); a.add_data_validation(dv); dv.add(f"H2:I{a.max_row}"); a.freeze_panes = "D2"
b = wb.create_sheet("B"); b.append(["번호", "arXiv", "제목", "초록", "다루는 분야 (예: 4.2, 4.4 / 없음)", "엄격까지 만족하는 분야", "메모"])
for i, r in enumerate(selB, 1): b.append([i] + list(r[1:4]) + ["", "", ""])
style(b, [6, 12, 30, 100, 18, 18, 20], [5, 6], 200); b.freeze_panes = "C2"
c_ = wb.create_sheet("C"); c_.append(["번호", "분야", "arXiv", "Q1 기준", "Q2 기준", "제목", "초록", "Q1 다루는가", "Q2 엄격", "메모"])
for i, r in enumerate(selC, 1): c_.append([i] + list(r[1:7]) + ["", "", ""])
style(c_, [6, 14, 12, 30, 30, 30, 90, 10, 10, 20], [8, 9], 200)
dvc = DataValidation(type="list", formula1='"예,아니오"', allow_blank=True); c_.add_data_validation(dvc); dvc.add(f"H2:I{c_.max_row}"); c_.freeze_panes = "D2"
gs = wb.create_sheet("등급"); gs.append(["번호", "논문", "arXiv 링크", "Q1 코드 공개 (예/아니오)", "Q1 메모(링크)", "Q2 측정 비용 (예/아니오)", "Q2 근거 위치", "메모"])
Gm = {r[0]: r for r in G}
for i, orow in enumerate(selG, 1): gs.append([i, Gm[orow][1], Gm[orow][2], "", "", "", "", ""])
style(gs, [6, 60, 34, 14, 30, 14, 24, 24], [4, 6], 45)
for r in range(2, gs.max_row + 1): gs.cell(r, 3).hyperlink = gs.cell(r, 3).value
dv2 = DataValidation(type="list", formula1='"예,아니오"', allow_blank=True); gs.add_data_validation(dv2); dv2.add(f"D2:D{gs.max_row}"); dv2.add(f"F2:F{gs.max_row}"); gs.freeze_panes = "C2"
wb.active = 0; wb.save(os.path.join(HERE, "2차평가자_판정시트_v2.xlsx"))   # 10/15 시트 C 추가본(원래 파일이 엑셀에 열려 있어 새 이름)
print("A", len(selA), collections.Counter(r[1][:3] for r in selA), "| B", len(selB), "| G", len(selG), collections.Counter(next(k["grade"] for k in KG if int(k["row"]) == x) for x in selG))

# -*- coding: utf-8 -*-
"""3차 리뷰 5번(2026-10-16): 표 9 정확도의 생성 길이 차이(5070 Ti 1차 32토큰 / 5080 16토큰)가 답을 바꿀 수 있는지 점검.
   탐욕적 디코딩이라 16토큰 안에 끝난 답은 상한이 32여도 같다. 그래서 5080(16토큰) 예측 중 16토큰 상한에 닿았을 수 있는 답의 수를 센다.
   토큰 수는 LLaMA 토크나이저 대신 보수적 근사(단어 수 ≥ 8 또는 글자 수 ≥ 40 이면 '상한 근접'으로 봄). 실행: python bench/check_answer_length.py"""
import glob, json, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8"); B = os.path.dirname(os.path.abspath(__file__))
tot = collections.Counter(); near = collections.Counter(); ex = []
for f in glob.glob(f"{B}/results_pc1/*/acc_*/preds_*.jsonl"):
    m = f.replace("\\", "/").split("/results_pc1/")[1].split("/")[0]; bench = os.path.basename(f)[6:-6]
    if m == "cdpruner": continue
    for ln in open(f, encoding="utf-8"):
        p = json.loads(ln).get("pred", ""); tot[bench] += 1
        if len(p.split()) >= 8 or len(p) >= 40: near[bench] += 1; len(ex) < 8 and ex.append((m, bench, p))
for k in sorted(tot): print(f"{k:8} answers {tot[k]:7,}  near the 16-token cap {near[k]:5}  ({100 * near[k] / tot[k]:.3f}%)")
for e in ex: print(e)

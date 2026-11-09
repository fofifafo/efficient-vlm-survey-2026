# -*- coding: utf-8 -*-
"""10/21 등급 C 재점검(2차 평가자가 표본 C 5편 중 3편에서 놓친 측정값을 찾음 → 표본 밖 C 18편 전수 점검).
   전문(main_survey/txt/<id>.txt, 참고문헌 앞까지)에서 시간·메모리 단위가 붙은 숫자가 있는 줄과 표 머리글을 앞뒤 문맥과 함께 뽑는다.
   이 후보를 읽고 '저자가 자기 시스템에서 직접 잰 시간 또는 메모리'인지 판단(규칙: 등급 A/B/C, FLOPs·파라미터 수 제외, 남의 수치 인용 제외),
   1저자가 원문에서 확인. 출력: recheck_c_candidates.md. 실행: python main_survey/gradeval/recheck_c_candidates.py"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); HERE = os.path.dirname(os.path.abspath(__file__)); MS = os.path.dirname(HERE)
K = list(csv.DictReader(open(os.path.join(HERE, "answer_key_grade.csv"), encoding="utf-8-sig")))
SAMPLED = {"2408.05517", "2409.07267", "2501.04322", "2407.03056", "2504.07934"}   # 2차 평가자 표본에 있던 C 5편
C = [k for k in K if k["grade"] == "C" and k["arxiv_id"] not in SAMPLED]
UNIT = re.compile(r"(\d[\d,.]*\s?(?:ms|milliseconds?|s|sec|seconds?|mins?|minutes?|h|hrs?|hours?|days?|GPU[- ]?(?:hours?|days?|hrs?)|GB|GiB|MB|MiB|TB|tokens?/s|samples?/s|it/s|img/s|images?/s|FPS|fps|W|J)\b)|"
                  r"(\((?:GB|GiB|MB|ms|s|sec|h|hours?|min|mins|days?)\)|GPU[- ]?(?:hours?|days?)|training time|inference time|wall[- ]clock|latency|throughput|memory (?:usage|footprint|consumption|cost)|peak memory|VRAM|TTFT|speed[- ]?up|tokens per second|time cost)", re.I)
out = [f"# 등급 C 재점검 후보 ({len(C)}편, 표본 밖) — 10/21\n"]
for k in C:
    p = os.path.join(MS, "txt", f"{k['arxiv_id']}.txt")
    if not os.path.exists(p): out.append(f"\n## {k['name']} ({k['arxiv_id']}) — 전문 없음\n"); continue
    L = open(p, encoding="utf-8", errors="ignore").read().split("\n")
    cut = next((i for i, l in enumerate(L) if re.match(r"^\s*(References|REFERENCES|Bibliography)\s*$", l)), len(L))
    hits = [i for i in range(len(L)) if UNIT.search(L[i]) and re.search(r"\d", L[i] + (L[i + 1] if i + 1 < len(L) else ""))]
    out.append(f"\n## {k['name']} ({k['arxiv_id']}) — 가지 {k['branches']}, 코드 {k['code']}, 줄 {len(hits)}\n")
    shown = set()
    for i in hits:
        if i in shown: continue
        a, b = max(0, i - 1), min(len(L), i + 2); shown.update(range(a, b))
        out.append(f"- {'[참고문헌 뒤] ' if i >= cut else ''}L{i + 1}: " + " ⏎ ".join(x.strip() for x in L[a:b])[:300])
open(os.path.join(HERE, "recheck_c_candidates.md"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(l for l in out if l.startswith("\n##") or l.startswith("#")))

# -*- coding: utf-8 -*-
"""메인 서베이 선정 논문 PDF 내려받기 + 텍스트 추출. arXiv 요청 간격 4초(재시도 백오프). 이미 받은 파일은 건너뜀.
   실행: python efficiency_audit/fetch_pdfs.py"""
import csv, os, sys, time, urllib.request, urllib.error
import pymupdf
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
SEL = sys.argv[1] if len(sys.argv) > 1 else "selected_all.csv"   # 9/30: 통합 선정 목록
rows = list(csv.DictReader(open(os.path.join(ROOT, SEL), encoding="utf-8-sig")))
ids = [r["id"] for r in rows]
print("papers:", len(ids))
UA = {"User-Agent": "Mozilla/5.0 (research corpus audit; contact via arXiv account)"}
ok = fail = skip = 0
for i, aid in enumerate(ids, 1):
    pdf = os.path.join(ROOT, "pdf", aid + ".pdf"); txt = os.path.join(ROOT, "txt", aid + ".txt")
    if os.path.exists(txt) and os.path.getsize(txt) > 2000:
        skip += 1; continue
    if not (os.path.exists(pdf) and os.path.getsize(pdf) > 10000):
        url = f"https://arxiv.org/pdf/{aid}"
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=60) as r: data = r.read()
                if data[:4] != b"%PDF": raise ValueError("not a pdf (%d bytes)" % len(data))
                open(pdf, "wb").write(data); break
            except Exception as e:
                wait = 8 * (attempt + 1); print(f"  [{aid}] attempt {attempt+1} failed: {e}; wait {wait}s"); time.sleep(wait)
        else:
            fail += 1; print(f"FAIL {aid}"); continue
        time.sleep(4)
    try:
        doc = pymupdf.open(pdf)
        text = "\n".join(page.get_text() for page in doc)
        open(txt, "w", encoding="utf-8").write(text); ok += 1
        print(f"[{i:3d}/{len(ids)}] {aid} pages={len(doc)} chars={len(text)}")
    except Exception as e:
        fail += 1; print(f"FAIL extract {aid}: {e}")
print(f"done: ok={ok} skip={skip} fail={fail}")

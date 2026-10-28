# -*- coding: utf-8 -*-
"""2차 리뷰 M4 보조(10/14): 등급의 한 축인 '코드 공개'를 기계로 확인. matrix_4.*.csv 의 code 링크마다 HTTP 상태와
   (GitHub 이면) 저장소 존재·보관 여부·파일 유무를 GitHub API 로 확인한다. 측정 비용 축은 추출 대조(extraction_check, 30/30)가 담당.
   실행: python main_survey/check_code_links.py → main_survey/code_link_check.csv, code_link_check.json"""
import csv, glob, json, os, re, sys, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {"User-Agent": "vlm-survey-linkcheck/1.0"}
TOKEN = os.environ.get("GITHUB_TOKEN")
def get(url, api=False):
    h = dict(UA); h.update({"Accept": "application/vnd.github+json"} if api else {})
    if api and TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30); return r.status, (json.load(r) if api else None)
    except urllib.error.HTTPError as e: return e.code, None
    except Exception as e: return f"ERR {type(e).__name__}", None
rows = []
for f in sorted(glob.glob("main_survey/matrix_4.*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8-sig")):
        url = r["code"].strip(); rec = dict(branch=os.path.basename(f)[7:10], id=r["id"], name=r["name"], code=url, status="", repo_ok="", archived="", size_kb="", pushed_at="")
        if url:
            m = re.match(r"https?://github\.com/([^/\s]+)/([^/\s#?]+)", url)
            if m:
                st, js = get(f"https://api.github.com/repos/{m.group(1)}/{m.group(2).removesuffix('.git')}", api=True)
                rec["status"] = st
                if js: rec.update(repo_ok=True, archived=js.get("archived"), size_kb=js.get("size"), pushed_at=js.get("pushed_at", "")[:10])
                else: rec["repo_ok"] = False
                time.sleep(1.0 if TOKEN else 1.5)
            else:
                st, _ = get(url); rec["status"] = st; rec["repo_ok"] = st == 200
        rows.append(rec)
w = csv.DictWriter(open("main_survey/code_link_check.csv", "w", newline="", encoding="utf-8-sig"), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
coded = [r for r in rows if r["code"]]
summ = dict(entries=len(rows), with_link=len(coded), reachable=sum(r["repo_ok"] is True for r in coded),
            nonempty=sum(r["repo_ok"] is True and (r["size_kb"] == "" or int(r["size_kb"]) > 0) for r in coded),
            failed=[(r["name"], r["code"], r["status"]) for r in coded if r["repo_ok"] is not True],
            empty=[(r["name"], r["code"]) for r in coded if r["size_kb"] == 0])
json.dump(summ, open("main_survey/code_link_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summ, ensure_ascii=False, indent=1))

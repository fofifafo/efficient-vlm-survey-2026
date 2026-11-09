# -*- coding: utf-8 -*-
"""Build data/corpus_vlm_15394.csv: one row per VLM-relevant arXiv paper with per-branch loose/strict labels.

The branch rules (v2.1) are taken verbatim from main_taxonomy.py (its definition block is executed, the
analysis part is not), so the labels are exactly those behind Table 2 and Fig. 2. Abstracts are NOT written.

Usage:
    python build_corpus_csv.py --cache /path/to/papers_raw.json [--out ../data/corpus_vlm_15394.csv]
papers_raw.json is the arXiv cache written by arxiv_scrape.py (python arxiv_scrape.py, about 15 min).
"""
import argparse, csv, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--cache", required=True, help="papers_raw.json produced by arxiv_scrape.py")
ap.add_argument("--out", default=os.path.join(HERE, "..", "data", "corpus_vlm_15394.csv"))
a = ap.parse_args()
cache = os.path.abspath(a.cache); out = os.path.abspath(a.out); cwd = os.getcwd()

sys.path.insert(0, HERE)
import arxiv_scrape as AS  # noqa: E402
AS.RAW_CACHE = cache

# Execute only the rule-definition block of main_taxonomy.py (everything before the corpus is loaded).
src = open(os.path.join(HERE, "main_taxonomy.py"), encoding="utf-8").read()
head = src.split("papers, _ = load_cache()")[0]
head = head.replace("from strict_tags import fisher_exact", "fisher_exact = None")  # not needed here
g = {"__file__": os.path.join(HERE, "main_taxonomy.py"), "__name__": "taxonomy_rules"}
exec(compile(head, "main_taxonomy.py (rules)", "exec"), g)
os.chdir(cwd)

papers, _ = AS.load_cache()
CORE = {"mllm", "vision-language-model", "visual-instruction-tuning"}
EFF = {k for k, c in AS.KW_CLUSTER.items() if c == "EFF"}
rows = []
for p in papers.values():
    kw = AS.extract_keywords(f"{p['title']}\n{p['abstract']}")
    if not kw & CORE:
        continue
    t = p["title"] + ". " + p["abstract"]
    r = {"arxiv_id": p["id"], "date": p["date"], "primary_category": p.get("primary", ""),
         "title": " ".join(p["title"].split()), "efficiency_oriented": int(bool(kw & EFF))}
    for b, _lab, loose, strict, _ in g["RX"]:
        r[f"b{b}_loose"] = int(bool(loose.search(t)))
        r[f"b{b}_strict"] = int(bool(strict.search(t)) if b in g["STRICT_OVERRIDE"]
                                else bool(strict.search(t) or loose.search(p["title"])))
    rows.append(r)
rows.sort(key=lambda r: (r["date"], r["arxiv_id"]))
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# Summary for checking against data/taxonomy_counts.csv
yr = collections.Counter(r["date"][:4] for r in rows)
eff = [r for r in rows if r["efficiency_oriented"]]
print(f"VLM papers: {len(rows)} {dict(sorted(yr.items()))}; efficiency-oriented: {len(eff)} "
      f"{dict(sorted(collections.Counter(r['date'][:4] for r in eff).items()))}")
for b, *_ in g["RX"]:
    print(f"  {b}: all loose {sum(r[f'b{b}_loose'] for r in rows)} strict {sum(r[f'b{b}_strict'] for r in rows)} | "
          f"eff loose {sum(r[f'b{b}_loose'] for r in eff)} strict {sum(r[f'b{b}_strict'] for r in eff)}")
print("->", out)

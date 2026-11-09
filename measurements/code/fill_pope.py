# -*- coding: utf-8 -*-
"""구 코드(qid=question_id, 범주 간 중복)로 돌린 POPE 예측 파일의 누락 행(스모크 qid 1~5 의 popular/random 10행)을 채운다.
   사용: python fill_pope.py --method base --setting default"""
import argparse, importlib, json, os, sys, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default")
ap.add_argument("--model", default=os.path.expanduser("~/vlmbench/models/llava-v1.5-7b")); ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results")); a = ap.parse_args()
from datasets import load_dataset
ds = load_dataset("lmms-lab/POPE")["test"]
f = f"{a.out}/{a.method}/acc_{a.setting}/preds_pope.jsonl"
rows = [json.loads(l) for l in open(f, encoding="utf-8")]
have = set()
for r in rows:
    if "question_id" in r: have.add((r["category"], r["question_id"]))
    else: have.add((r["category"], r["qid"]))            # 구 형식: qid == question_id
missing = [i for i in range(len(ds)) if (ds[i]["category"], ds[i]["question_id"]) not in have]
print(a.method, a.setting, "rows", len(rows), "missing", len(missing))
if missing:
    gen, meta = importlib.import_module(f"methods.{a.method}").load(a.model, setting=a.setting); torch.cuda.empty_cache()
    with open(f, "a", encoding="utf-8") as fo:
        for i in missing:
            r = ds[i]; o = gen(r["image"].convert("RGB"), r["question"], 16)
            fo.write(json.dumps(dict(answer=r["answer"], category=r["category"], question_id=r["question_id"], qid=f"pope{r['id']}", pred=o["answer"], n_vis_tokens=o.get("n_vis_tokens", -1)), ensure_ascii=False) + "\n")
    print("filled", len(missing))
os.system(f"{sys.executable} {os.path.dirname(os.path.abspath(__file__))}/score.py --method {a.method} --setting {a.setting} --out {a.out}")

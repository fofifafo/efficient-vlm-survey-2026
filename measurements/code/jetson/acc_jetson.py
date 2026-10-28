# -*- coding: utf-8 -*-
"""Jetson GQA 정확도(지연 측정과 같은 500문항). 데스크톱 eval_acc.py 와 같은 조건: vicuna_v1 + 한 단어 지시, greedy, max_new_tokens 16,
   채점은 bench/score.py 의 GQA 규칙(정규화 후 정확 일치). 결과: ~/vlmbench/results_jetson/<method>/acc_<setting>.json, preds_gqa500_<setting>.jsonl
   실행: python acc_jetson.py --method base4 --setting default"""
import argparse, importlib, json, os, sys, time
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); BENCH = os.path.dirname(HERE)
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, HERE); sys.path.insert(0, BENCH)
from score import norm

ap = argparse.ArgumentParser()
ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default"); ap.add_argument("--max_new_tokens", type=int, default=16)
ap.add_argument("--model", default=f"{WORK}/models/llava-v1.5-7b-st"); ap.add_argument("--data", default=f"{WORK}/data/gqa500")
ap.add_argument("--out", default=f"{WORK}/results_jetson")
a = ap.parse_args()
gen, meta = importlib.import_module(f"methods_jetson.{a.method}").load(a.model, setting=a.setting)
S = [json.loads(l) for l in open(f"{a.data}/samples.jsonl", encoding="utf-8")]
d = f"{a.out}/{a.method}"; os.makedirs(d, exist_ok=True)
pf = f"{d}/preds_gqa500_{a.setting}.jsonl"
done = {json.loads(l)["qid"] for l in open(pf, encoding="utf-8")} if os.path.exists(pf) else set()   # 재개 가능
t0 = time.time()
with open(pf, "a", encoding="utf-8") as fo:
    for k, s in enumerate(S):
        if s["question_id"] in done: continue
        o = gen(Image.open(f"{a.data}/{s['image']}").convert("RGB"), s["question"], a.max_new_tokens)
        fo.write(json.dumps(dict(qid=s["question_id"], answer=s["answer"], pred=o["answer"], n_vis_tokens=o.get("n_vis_tokens")), ensure_ascii=False) + "\n"); fo.flush()
        if k % 50 == 0: print(f"{k}/{len(S)} {time.time() - t0:.0f}s", flush=True)
rows = [json.loads(l) for l in open(pf, encoding="utf-8")]
acc = sum(norm(r["pred"]) == norm(r["answer"]) for r in rows) / len(rows)
json.dump(dict(method=a.method, setting=a.setting, n=len(rows), gqa500_acc=acc, meta=meta, max_new_tokens=a.max_new_tokens), open(f"{d}/acc_{a.setting}.json", "w"), indent=1)
print("ACC", a.method, a.setting, len(rows), round(100 * acc, 2))

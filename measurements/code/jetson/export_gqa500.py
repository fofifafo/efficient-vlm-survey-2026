# -*- coding: utf-8 -*-
"""데스크톱 지연 측정과 같은 GQA test-dev 500문항(시드 20261001)을 이미지째 내보낸다 → Jetson 에서 datasets 없이 같은 표본 사용.
   실행(WSL, vlmbench env, HF_HOME=~/vlmbench/models/hf): python bench/jetson/export_gqa500.py ~/vlmbench/data/gqa500"""
import json, os, random, sys
from datasets import load_dataset
out = os.path.expanduser(sys.argv[1]); os.makedirs(f"{out}/images", exist_ok=True)
N = 500
ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
idx = random.Random(20261001).sample(range(len(ds)), N)          # harness.py 와 같은 시드·같은 방식
imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
img_by_id = {r["id"]: r["image"] for r in imgs}
with open(f"{out}/samples.jsonl", "w", encoding="utf-8") as fo:
    for k, i in enumerate(idx):
        r = ds[i]; iid = r["imageId"]; p = f"images/{iid}.jpg"
        if not os.path.exists(f"{out}/{p}"): img_by_id[iid].convert("RGB").save(f"{out}/{p}", quality=95)
        fo.write(json.dumps(dict(k=k, ds_index=i, question_id=r["id"], imageId=iid, question=r["question"], answer=r["answer"], image=p)) + "\n")
print("exported", N, "->", out)

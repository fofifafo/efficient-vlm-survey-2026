# -*- coding: utf-8 -*-
"""cdpruner_fix 검증: 새 프로세스에서 예약 메모리와 TTFT 확인"""
import os, sys, time, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import methods.cdpruner_fix as M
from datasets import load_dataset
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
img_by_id = {r["id"]: r["image"] for r in imgs}
res = []
for i in range(12):
    r = ds[i]; o = gen(img_by_id[r["imageId"]].convert("RGB"), r["question"], 16); res.append(o)
    if i < 3: print(i, "ttft ms", round(o["ttft_s"] * 1000, 1), "answer:", o["answer"], "| gt:", r["answer"])
tt = sorted(o["ttft_s"] * 1000 for o in res[2:])
print("TTFT median ms:", round(tt[len(tt) // 2], 1), "| n_vis:", res[0]["n_vis_tokens"])
print("alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2), "peak alloc GB:", round(torch.cuda.max_memory_allocated() / 2**30, 2))

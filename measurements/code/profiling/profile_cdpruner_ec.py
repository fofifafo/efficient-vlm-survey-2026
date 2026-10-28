# -*- coding: utf-8 -*-
"""로드 직후 torch.cuda.empty_cache() 효과 확인 (로드 시 fp32 CLIP 임시 피크로 예약된 2 GB 가 남아 16 GB 를 넘김). 사용: ... profile_cdpruner_ec.py cdpruner|cdpruner_fix"""
import os, sys, time, importlib, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
name = sys.argv[1] if len(sys.argv) > 1 else "cdpruner"
M = importlib.import_module(f"methods.{name}")
from datasets import load_dataset
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
print("after load  alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2), "peak:", round(torch.cuda.max_memory_allocated() / 2**30, 2))
torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
print("empty_cache alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2))
ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
img_by_id = {r["id"]: r["image"] for r in imgs}
res = []
for i in range(15):
    r = ds[i]; o = gen(img_by_id[r["imageId"]].convert("RGB"), r["question"], 16); res.append(o)
tt = sorted(o["ttft_s"] * 1000 for o in res[3:])
print(name, "TTFT median ms:", round(tt[len(tt) // 2], 1), "| total median ms:", round(sorted(o["total_s"] for o in res[3:])[6] * 1000, 1), "| n_vis:", res[0]["n_vis_tokens"])
print("after runs  alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2), "peak:", round(torch.cuda.max_memory_allocated() / 2**30, 2))

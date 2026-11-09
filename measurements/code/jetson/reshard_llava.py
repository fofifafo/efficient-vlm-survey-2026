# -*- coding: utf-8 -*-
"""Jetson Orin Nano(8 GB 통합 메모리)용 체크포인트 재분할 (2026-10-12).
   원본 liuhaotian/llava-v1.5-7b 는 pytorch_model-00001-of-00002.bin 이 10 GB 라 Jetson 에서 torch.load 하면 메모리를 넘는다.
   텐서 값은 그대로 두고 1 GB 이하 safetensors 조각으로 다시 저장한다(mmap 으로 조각별 로드 가능). 계산 결과는 원본과 같다.
   실행(WSL, vlmbench env): python bench/jetson/reshard_llava.py ~/vlmbench/models/llava-v1.5-7b ~/vlmbench/models/llava-v1.5-7b-st"""
import json, os, shutil, sys
import torch
from safetensors.torch import save_file
src, dst = os.path.expanduser(sys.argv[1]), os.path.expanduser(sys.argv[2]); os.makedirs(dst, exist_ok=True)
LIMIT = 1 << 30
idx = json.load(open(os.path.join(src, "pytorch_model.bin.index.json")))
shards = sorted(set(idx["weight_map"].values()))
buf, size, n, wmap, total = {}, 0, 0, {}, 0
def flush():
    global buf, size, n
    if not buf: return
    n += 1; name = f"model-{n:05d}.safetensors"
    save_file(buf, os.path.join(dst, name), metadata={"format": "pt"})
    for k in buf: wmap[k] = name
    print(f"  {name}: {len(buf)} tensors, {size / 2**20:.0f} MiB", flush=True); buf, size = {}, 0
for sh in shards:
    print("load", sh, flush=True)
    sd = torch.load(os.path.join(src, sh), map_location="cpu")
    for k in list(sd):
        t = sd.pop(k).contiguous(); b = t.numel() * t.element_size()
        if size + b > LIMIT: flush()
        buf[k] = t; size += b; total += b
    del sd
flush()
names = sorted(set(wmap.values())); final = {}
for i, old in enumerate(names, 1):                       # 총 조각 수를 알았으니 HF 규칙 이름으로 바꾼다
    new = f"model-{i:05d}-of-{len(names):05d}.safetensors"; os.rename(os.path.join(dst, old), os.path.join(dst, new)); final[old] = new
json.dump({"metadata": {"total_size": total}, "weight_map": {k: final[v] for k, v in wmap.items()}}, open(os.path.join(dst, "model.safetensors.index.json"), "w"), indent=1)
for f in os.listdir(src):
    if f.endswith((".json", ".model", ".bin")) and not f.startswith("pytorch_model"): shutil.copy(os.path.join(src, f), dst)
print("done:", len(names), "shards,", round(total / 2**30, 2), "GiB ->", dst)

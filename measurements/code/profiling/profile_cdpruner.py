# -*- coding: utf-8 -*-
"""CDPruner 1.3 s TTFT 원인 추적: 단계별 벽시계 시간 + cProfile 상위 항목. 사용: bash run_py.sh profile_cdpruner.py"""
import os, sys, time, cProfile, pstats, io, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import methods.cdpruner as M
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
from datasets import load_dataset
ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
r = ds[0]; img = next(x["image"] for x in imgs if x["id"] == r["imageId"]).convert("RGB"); q = r["question"]
for _ in range(2): gen(img, q, 8)                                   # warm-up
def T(f, n=3):
    torch.cuda.synchronize(); t0 = time.perf_counter()
    for _ in range(n): f()
    torch.cuda.synchronize(); return (time.perf_counter() - t0) / n * 1000
import llava.model.llava_arch as LA
from llava.mm_utils import process_images
vt = M.use_repo  # noqa
model = gen.__closure__  # not used
# 모델 객체 얻기: make_gen 클로저에서
import inspect
mdl = [c.cell_contents for c in gen.__closure__ if hasattr(c.cell_contents, "generate")][0]
proc = [c.cell_contents for c in gen.__closure__ if c.cell_contents.__class__.__name__.endswith("ImageProcessor")][0]
imt = process_images([img], proc, mdl.config).to("cuda", torch.float16)
tower = mdl.get_model().get_vision_tower()
print("vision tower (image only)  ms:", round(T(lambda: tower(imt)), 1))
print("vision tower (image+text)  ms:", round(T(lambda: tower(imt, texts=q)), 1))
print("text tokenizer+tower only  ms:", round(T(lambda: tower.text_tower(**{k: v.to("cuda") for k, v in tower.text_tokenizer(text=q, return_tensors="pt", padding="max_length", max_length=77).items()})), 1))
print("encode_images (tower+DPP)  ms:", round(T(lambda: mdl.encode_images(imt, texts=q)), 1))
print("full gen (8 tok) TTFT      ms:", round(gen(img, q, 8)["ttft_s"] * 1000, 1))
pr = cProfile.Profile(); pr.enable(); gen(img, q, 8); pr.disable()
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(28); print(s.getvalue()[:6000])

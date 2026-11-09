# -*- coding: utf-8 -*-
"""환경 검증: GPU·CUDA·모델 로드·1장 추론·전력 판독. 실행: python /mnt/j/VLM-Survey/bench/check_env.py  (conda activate vlmbench 후)"""
import os, sys, time, json
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
out = {}
import torch
out["torch"] = torch.__version__; out["cuda"] = torch.version.cuda; out["gpu"] = torch.cuda.get_device_name(0)
out["sm"] = torch.cuda.get_device_capability(0); out["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1)
print(out)
import pynvml
pynvml.nvmlInit(); h = pynvml.nvmlDeviceGetHandleByIndex(0)
out["power_w_idle"] = pynvml.nvmlDeviceGetPowerUsage(h) / 1000; print("idle power W:", out["power_w_idle"])
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from llava.model.builder import load_pretrained_model
from llava.mm_utils import process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from PIL import Image
t0 = time.time()
tok, model, proc, ctx = load_pretrained_model(f"{WORK}/models/llava-v1.5-7b", None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)
out["load_s"] = round(time.time() - t0, 1); out["vram_after_load_gb"] = round(torch.cuda.memory_allocated() / 2**30, 2)
print("loaded in", out["load_s"], "s; VRAM", out["vram_after_load_gb"], "GB")
img = Image.new("RGB", (336, 336), (120, 160, 200))
imt = process_images([img], proc, model.config).to("cuda", torch.float16)
prompt = f"USER: {DEFAULT_IMAGE_TOKEN}\nWhat color is the image? Answer briefly.\nASSISTANT:"
ids = tokenizer_image_token(prompt, tok, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).cuda()
torch.cuda.synchronize(); t0 = time.time()
with torch.inference_mode():
    o = model.generate(ids, images=imt, image_sizes=[img.size], max_new_tokens=16, do_sample=False)
torch.cuda.synchronize(); out["gen_s"] = round(time.time() - t0, 3); out["peak_gb"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
out["answer"] = tok.decode(o[0], skip_special_tokens=True).strip()
print(out)
os.makedirs(f"{WORK}/logs", exist_ok=True); json.dump(out, open(f"{WORK}/logs/check_env.json", "w"), indent=1)
print("OK — 환경 검증 통과" if out["vram_after_load_gb"] < 15 else "!! VRAM 여유 부족")

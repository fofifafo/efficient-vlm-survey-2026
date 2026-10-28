# -*- coding: utf-8 -*-
"""단순 기준선 2(심사 대응 10/28): 원본 LLaVA-1.5-7B 의 프로젝터 출력 24×24 격자를 평균 풀링해 언어 모델에 넘긴다.
   default = 2×2 풀링 → 12×12 = 144개, r889 = 3×3 풀링 → 8×8 = 64개. 학습·질문·어텐션을 쓰지 않는다."""
import os, sys, torch
import torch.nn.functional as F
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from methods._llava_common import make_gen
K = {"default": 2, "r889": 3}

def load(model_path, setting="default"):
    from llava.model.builder import load_pretrained_model
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)
    model.eval(); k = K[setting]; n = (24 // k) ** 2
    orig = model.encode_images
    def encode_images(images):
        f = orig(images)                                            # (B, 576, D)
        B, L, D = f.shape
        g = f.view(B, 24, 24, D).permute(0, 3, 1, 2)                # (B, D, 24, 24)
        g = F.avg_pool2d(g, kernel_size=k, stride=k)                # (B, D, 24/k, 24/k)
        return g.flatten(2).transpose(1, 2).contiguous()            # (B, n, D), 행 우선 순서
    model.encode_images = encode_images
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: n)
    return gen, dict(name="Pooling", setting=setting, visual_token_num=n, selection=f"{k}x{k} average pooling of the 24x24 projector output grid", attn="sdpa(default)", prompt="vicuna_v1")

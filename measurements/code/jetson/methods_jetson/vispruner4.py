# -*- coding: utf-8 -*-
"""VisPruner, 언어 모델 4비트(NF4) — 8 GB Jetson 용. 설정은 데스크톱 vispruner.py 와 같음(default 128토큰, r889 64토큰)."""
import torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": (128, 0.5), "r889": (64, 0.5), "t32": (32, 0.5), "t256": (256, 0.5), "t384": (384, 0.5)}   # t* = 리뷰어 질문 3 토큰 수 스윕(10/13)

def load(model_path, setting="default"):
    use_repo("VisPruner")
    from llava.model.builder import load_pretrained_model
    n, r = SETTINGS[setting]
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", load_4bit=True, visual_token_num=n, important_ratio=r, device_map="cuda")
    model.eval()
    def nvis(model, out): return out[1] if isinstance(out, tuple) else n
    return make_gen(tok, model, proc, n_vis_fn=nvis), dict(name="VisPruner", setting=setting, visual_token_num=n, important_ratio=r, quant="nf4-4bit (bnb)")

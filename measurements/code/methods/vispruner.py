# -*- coding: utf-8 -*-
"""VisPruner (2412.01818): 인코더 측, 중요 토큰 + 다양 토큰. 설정: default = 논문 주 설정(128 토큰, ratio 0.5) / r889 = 64 토큰(88.9% 제거)."""
import torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": (128, 0.5), "r889": (64, 0.5), "r944": (32, 0.5)}
def load(model_path, setting="default"):
    use_repo("VisPruner")
    from llava.model.builder import load_pretrained_model
    n, r = SETTINGS[setting]
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", visual_token_num=n, important_ratio=r, device_map="cuda", torch_dtype=torch.float16)
    model.eval()
    def nvis(model, out): return out[1] if isinstance(out, tuple) else n
    gen = make_gen(tok, model, proc, n_vis_fn=nvis)
    return gen, dict(name="VisPruner", setting=setting, visual_token_num=n, important_ratio=r)

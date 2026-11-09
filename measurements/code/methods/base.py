# -*- coding: utf-8 -*-
"""원본 LLaVA-1.5-7B (기준). 공식 vicuna_v1 템플릿(시스템 프롬프트 포함)으로 모든 방법과 같은 입력 조건. 스트리밍 generate 로 TTFT 측정."""
import os, sys, torch
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from methods._llava_common import make_gen

def load(model_path, setting="default"):
    from llava.model.builder import load_pretrained_model
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)   # 어텐션 구현은 transformers 4.37 기본(sdpa) — 다른 방법 플러그인과 동일 조건
    model.eval()
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: 576)
    return gen, dict(name="LLaVA-1.5-7B", setting=setting, attn="sdpa(default)", prompt="vicuna_v1")

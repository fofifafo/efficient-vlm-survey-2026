# -*- coding: utf-8 -*-
"""원본 LLaVA-1.5-7B, 언어 모델 4비트(NF4, bitsandbytes, 이중 양자화, 계산 fp16) — 8 GB Jetson 용. 비전 타워·프로젝터는 fp16.
   데스크톱 base.py 와 같은 vicuna_v1 템플릿·스트리밍 TTFT."""
import os, sys, torch
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from methods._llava_common import make_gen

def load(model_path, setting="default"):
    from llava.model.builder import load_pretrained_model
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", load_4bit=True, device_map="cuda")
    model.eval()
    return make_gen(tok, model, proc, n_vis_fn=lambda m, o: 576), dict(name="LLaVA-1.5-7B", setting=setting, quant="nf4-4bit (bnb)", prompt="vicuna_v1")

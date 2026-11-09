# -*- coding: utf-8 -*-
"""비교용: 표준 LLaVA(base) 비전 타워의 forward 시간(기본 스트림 vs 보조 스트림) + accelerate 훅 유무"""
import os, sys, time, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import methods.base as M
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
mdl = [c.cell_contents for c in gen.__closure__ if hasattr(c.cell_contents, "generate")][0]
tower = mdl.get_model().get_vision_tower()
x = torch.randn(1, 3, 336, 336, device="cuda", dtype=torch.float16)
def T(f, n=5):
    f(); torch.cuda.synchronize(); t0 = time.perf_counter()
    for _ in range(n): f()
    torch.cuda.synchronize(); return round((time.perf_counter() - t0) / n * 1000, 1)
print("base CLIP forward direct           ms:", T(lambda: tower.vision_tower(x, output_hidden_states=True)))
print("base CLIP forward, no hidden states ms:", T(lambda: tower.vision_tower(x)))
s = torch.cuda.Stream()
def on_stream():
    with torch.cuda.stream(s): tower.vision_tower(x, output_hidden_states=True)
print("base CLIP forward on side stream   ms:", T(on_stream))
print("hooks on CLIP modules:", sum(hasattr(m, "_hf_hook") for m in tower.vision_tower.modules()), "/", sum(1 for _ in tower.vision_tower.modules()))
print("attn impl:", getattr(tower.vision_tower.config, "_attn_implementation", None), type(tower.vision_tower.vision_model.encoder.layers[0].self_attn).__name__)
ids = torch.randint(0, 32000, (1, 640), device="cuda")
print("LLM prefill 640 tok                ms:", T(lambda: mdl.model(ids), 3))

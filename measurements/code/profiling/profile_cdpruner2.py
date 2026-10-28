# -*- coding: utf-8 -*-
"""CDPruner 비전 타워 806 ms 의 원인 분리: 스트림 생성 비용 vs CLIP forward 자체"""
import os, sys, time, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import methods.cdpruner as M
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
mdl = [c.cell_contents for c in gen.__closure__ if hasattr(c.cell_contents, "generate")][0]
tower = mdl.get_model().get_vision_tower()
x = torch.randn(1, 3, 336, 336, device="cuda", dtype=torch.float16)
def T(f, n=5):
    f(); torch.cuda.synchronize(); t0 = time.perf_counter()
    for _ in range(n): f()
    torch.cuda.synchronize(); return round((time.perf_counter() - t0) / n * 1000, 1)
print("torch.cuda.Stream() x2 create      ms:", T(lambda: (torch.cuda.Stream(), torch.cuda.Stream())))
print("CLIP forward direct (default strm) ms:", T(lambda: tower.vision_tower(x, output_hidden_states=True)))
s = torch.cuda.Stream()
def on_stream():
    with torch.cuda.stream(s): tower.vision_tower(x, output_hidden_states=True)
print("CLIP forward on a reused stream    ms:", T(on_stream))
def new_stream_each():
    st = torch.cuda.Stream()
    with torch.cuda.stream(st): tower.vision_tower(x, output_hidden_states=True)
print("CLIP forward, new stream each call ms:", T(new_stream_each))
print("wrapper tower(x) (repo code)       ms:", T(lambda: tower(x)))
print("device/dtype:", tower.vision_tower.device, tower.vision_tower.dtype, "| text tower:", tower.text_tower.device, tower.text_tower.dtype)

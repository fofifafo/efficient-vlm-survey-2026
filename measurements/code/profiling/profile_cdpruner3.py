# -*- coding: utf-8 -*-
"""CDPruner 타워 지연 재측정 — inference_mode 하에서 기본 스트림 vs 보조 스트림, 메모리 여유 확인"""
import os, sys, time, subprocess, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import methods.cdpruner as M
gen, meta = M.load(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), "default")
mdl = [c.cell_contents for c in gen.__closure__ if hasattr(c.cell_contents, "generate")][0]
tower = mdl.get_model().get_vision_tower()
x = torch.randn(1, 3, 336, 336, device="cuda", dtype=torch.float16); q = "What color is the car?"
def smi(): return subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
def T(f, n=5):
    f(); torch.cuda.synchronize(); t0 = time.perf_counter()
    for _ in range(n): f()
    torch.cuda.synchronize(); return round((time.perf_counter() - t0) / n * 1000, 1)
print("alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2), "smi:", smi())
with torch.inference_mode():
    print("CLIP direct, default stream        ms:", T(lambda: tower.vision_tower(x, output_hidden_states=True)))
    s = torch.cuda.Stream()
    def on_stream():
        with torch.cuda.stream(s): tower.vision_tower(x, output_hidden_states=True)
    print("CLIP direct, side stream           ms:", T(on_stream))
    print("wrapper tower(x)                   ms:", T(lambda: tower(x)))
    print("wrapper tower(x, texts)            ms:", T(lambda: tower(x, texts=q)))
    print("text tower only                    ms:", T(lambda: tower.text_tower(**{k: v.to("cuda") for k, v in tower.text_tokenizer(text=q, return_tensors="pt").items()})))
    print("encode_images                      ms:", T(lambda: mdl.encode_images(x, texts=q)))
    # 스트림 제거 실험: 같은 계산을 기본 스트림에서 순차 실행
    def seq():
        o = tower.vision_tower(x, output_hidden_states=True); f = tower.feature_select(o)
        ti = tower.text_tokenizer(text=q, return_tensors="pt"); ti = {k: v.to("cuda") for k, v in ti.items()}
        te = tower.text_tower(**ti).text_embeds
        ie = tower.vision_tower.visual_projection(tower.vision_tower.vision_model.post_layernorm(f))
        return f, ie, te
    print("same work, default stream, seq     ms:", T(seq))
print("alloc GB:", round(torch.cuda.memory_allocated() / 2**30, 2), "reserved GB:", round(torch.cuda.memory_reserved() / 2**30, 2), "smi:", smi())

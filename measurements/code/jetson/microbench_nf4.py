# -*- coding: utf-8 -*-
"""리뷰어 질문 3 검증(2026-10-13): bitsandbytes NF4 의 추가 비용이 토큰 수에 비례하는가, 고정인가.
   LLaMA-7B MLP 크기 층(4096→11008) 하나를 FP16 nn.Linear 와 bnb Linear4bit(NF4, 계산 fp16)로 두고,
   토큰 수 T = 16…1024 에서 순전파 시간을 잰다(CUDA 동기화, 워밍업 후 중앙값). 차이(NF4 − FP16)가 T 와 무관하면 고정 비용.
   실행: python microbench_nf4.py → ~/vlmbench/results_jetson/microbench_nf4.json"""
import json, os, statistics, time
import torch, bitsandbytes as bnb
torch.manual_seed(0); dev = "cuda"
IN, OUT = 4096, 11008
fp = torch.nn.Linear(IN, OUT, bias=False, dtype=torch.float16, device=dev)
q = bnb.nn.Linear4bit(IN, OUT, bias=False, compute_dtype=torch.float16, quant_type="nf4", compress_statistics=True)
q.weight = bnb.nn.Params4bit(fp.weight.data.cpu(), requires_grad=False, quant_type="nf4", compress_statistics=True)
q = q.to(dev)
def t_ms(m, x, reps=50):
    for _ in range(10): m(x)
    torch.cuda.synchronize(); out = []
    for _ in range(reps):
        torch.cuda.synchronize(); t0 = time.perf_counter(); m(x); torch.cuda.synchronize(); out.append(1000 * (time.perf_counter() - t0))
    return statistics.median(out)
rows = []
with torch.inference_mode():
    for T in (1, 16, 64, 128, 256, 384, 512, 640, 1024):
        x = torch.randn(1, T, IN, dtype=torch.float16, device=dev)
        a, b = t_ms(fp, x), t_ms(q, x)
        rows.append(dict(tokens=T, fp16_ms=round(a, 4), nf4_ms=round(b, 4), overhead_ms=round(b - a, 4)))
        print(rows[-1], flush=True)
out = os.path.expanduser("~/vlmbench/results_jetson/microbench_nf4.json"); os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(dict(layer=f"{IN}x{OUT}", bnb=bnb.__version__, torch=torch.__version__, rows=rows), open(out, "w"), indent=1); print("saved", out)

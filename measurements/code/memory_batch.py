# -*- coding: utf-8 -*-
"""외부 리뷰(10/25) 대응 C2: 배치 크기에 따른 프리필 메모리 — 시각 토큰 576 vs 64. 결론 (v) '576토큰·배치 1 에서는 토큰 압축이 메모리를 거의 못 줄인다'의
   범위를 넓혀, 배치가 커지면 절감이 얼마나 커지는지 직접 잰다. 방법 플러그인들은 배치 1 로만 동작하므로, 메모리는 토큰 수와 배치에만 달려 있다는 점을 이용해
   시각 토큰을 균등 간격으로 64개 고르는 대리(proxy) 설정으로 잰다(어떤 토큰을 고르는지는 메모리에 영향 없음).
   LLaVA-1.5-7B FP16, SDPA, 프롬프트 = vicuna_v1 시스템 프롬프트 + 이미지 + GQA 형 질문(같은 문장 반복). 측정: 프리필(use_cache=True) 1회의
   torch.cuda.max_memory_allocated − 직전 할당량(활성 + KV 캐시 + logits), 그리고 최대 할당 절대값. PyTorch 할당량이므로 화면 등 다른 프로세스와 무관.
   출력: ~/vlmbench/results_memory_batch/memory_batch.json. 실행: python memory_batch.py [--bs 1,2,4,8,16]"""
import argparse, json, os, sys, time
import torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
ap = argparse.ArgumentParser(); ap.add_argument("--bs", default="1,2,4,8,16"); ap.add_argument("--model", default=f"{WORK}/models/llava-v1.5-7b")
a = ap.parse_args()
from llava.model.builder import load_pretrained_model
from llava.mm_utils import tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX
from methods._llava_common import vicuna_prompt
tok, model, proc, _ = load_pretrained_model(a.model, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16); model.eval()
torch.cuda.empty_cache()
prompt = vicuna_prompt("Is the man to the left or to the right of the white car?")
ids = tokenizer_image_token(prompt, tok, IMAGE_TOKEN_INDEX, return_tensors="pt")
k = (ids == IMAGE_TOKEN_INDEX).nonzero()[0, 0].item(); pre, post = ids[:k].cuda(), ids[k + 1:].cuda()
emb = model.get_model().embed_tokens
torch.manual_seed(0)
with torch.inference_mode():
    img = torch.randn(1, 3, 336, 336, device="cuda", dtype=torch.float16)
    vis = model.encode_images(img)                                   # (1, 576, 4096)
    E = {576: vis, 64: vis[:, ::9][:, :64]}
    tpre, tpost = emb(pre)[None], emb(post)[None]
res = dict(model="LLaVA-1.5-7B FP16", gpu=torch.cuda.get_device_name(0), torch=torch.__version__, text_tokens=int(pre.numel() + post.numel()),
           weights_gb=round(torch.cuda.memory_allocated() / 2**30, 3), rows=[])
for B in [int(x) for x in a.bs.split(",")]:
    for nv in (576, 64):
        x = torch.cat([tpre, E[nv], tpost], 1).repeat(B, 1, 1)
        torch.cuda.synchronize(); torch.cuda.empty_cache(); base = torch.cuda.memory_allocated(); torch.cuda.reset_peak_memory_stats()
        t0 = time.perf_counter(); err = None
        try:
            with torch.inference_mode():
                out = model(inputs_embeds=x, use_cache=True, return_dict=True)
            torch.cuda.synchronize()
            kv = sum(t.numel() * t.element_size() for layer in out.past_key_values for t in layer)
            del out
        except torch.cuda.OutOfMemoryError as e:
            err = "OOM"; kv = None
        peak = torch.cuda.max_memory_allocated()
        row = dict(batch=B, visual_tokens=nv, seq_len=int(x.shape[1]), peak_gb=round(peak / 2**30, 3), extra_gb=round((peak - base) / 2**30, 3),
                   kv_cache_gb=round(kv / 2**30, 3) if kv else None, seconds=round(time.perf_counter() - t0, 2), error=err)
        res["rows"].append(row); print(json.dumps(row), flush=True)
        del x; torch.cuda.empty_cache()
os.makedirs(f"{WORK}/results_memory_batch", exist_ok=True)
json.dump(res, open(f"{WORK}/results_memory_batch/memory_batch.json", "w"), indent=1)
print("SUMMARY", json.dumps({r["batch"]: None for r in res["rows"]}))
for B in sorted({r["batch"] for r in res["rows"]}):
    r576 = next(r for r in res["rows"] if r["batch"] == B and r["visual_tokens"] == 576); r64 = next(r for r in res["rows"] if r["batch"] == B and r["visual_tokens"] == 64)
    print(f"B={B:2d}  peak 576={r576['peak_gb']} GB  64={r64['peak_gb']} GB  saving={round(r576['peak_gb'] - r64['peak_gb'], 3)} GB  (KV {r576['kv_cache_gb']} vs {r64['kv_cache_gb']})")

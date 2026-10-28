# -*- coding: utf-8 -*-
"""심사 대응(10/28) torch.compile 시도: 원본 LLaVA-1.5-7B(576 토큰)에 torch.compile 을 씌워 eager 대비 TTFT 를 본다(본문 5.3절 '컴파일하면 호스트 부담이 줄 수 있다').
   vision = CLIP 시각 인코더만(입력 336×336 고정 → 정적 형상), full = 시각 인코더 + 언어 모델(LlamaModel.forward, dynamic=True; 프롬프트 길이가 질문마다 달라서).
   기본 inductor 모드(CUDA 그래프 없음: 길이가 바뀌면 그래프를 다시 녹화해야 하므로). 컴파일·재컴파일은 load() 의 예열에서 끝내고 측정에 넣지 않는다."""
import os, sys, time, torch
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from methods._llava_common import make_gen
WARM_Q = ["What is this?", "Is the man to the left or to the right of the car?", "What color is the large object that is in front of the wooden fence near the building?",
          "Are there both cups and plates in the picture?", "Who is wearing the hat?", "Which kind of furniture is it, a table or a chair, and what material is it made of in this picture?"]

def load(model_path, setting="vision"):
    from llava.model.builder import load_pretrained_model
    from PIL import Image
    import torch._dynamo
    torch._dynamo.config.cache_size_limit = 256
    torch._dynamo.config.allow_unspec_int_on_nn_module = True   # 층마다 다른 layer_idx(정수 속성)로 층 수만큼 재컴파일하다 한도(64)에 걸려 eager 로 돌아가던 문제(10/28 첫 시험)
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)
    model.eval()
    vt = model.get_vision_tower(); vt.vision_tower = torch.compile(vt.vision_tower)
    if setting == "full":
        lm = model.get_model(); lm.forward = torch.compile(lm.forward, dynamic=True)
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: 576)
    t0 = time.perf_counter(); img = Image.new("RGB", (480, 360), (128, 120, 110))
    for _ in range(2):                                   # 예열: 길이가 다른 질문으로 prefill·decode 그래프를 미리 만든다
        for q in WARM_Q: gen(img, q, 8)
    warm = time.perf_counter() - t0; print(f"compile warm-up {warm:.1f} s", flush=True)
    return gen, dict(name="LLaVA-1.5-7B + torch.compile", setting=setting, compiled="vision tower" if setting == "vision" else "vision tower + language model (dynamic)",
                     mode="default inductor", warmup_s=round(warm, 1), attn="sdpa(default)", prompt="vicuna_v1")

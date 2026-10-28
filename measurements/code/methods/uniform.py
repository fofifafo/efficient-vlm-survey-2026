# -*- coding: utf-8 -*-
"""단순 기준선 1(심사 대응 10/28): 원본 LLaVA-1.5-7B 에서 프로젝터 출력 576개 시각 토큰 중 균등 간격으로 n 개만 언어 모델에 넘긴다.
   선택에 질문·어텐션·학습을 쓰지 않는다. default = 128개, r889 = 64개(다른 방법과 같은 예산). 인덱스 = round(linspace(0, 575, n))."""
import os, sys, torch
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))
sys.path.insert(0, f"{WORK}/repos/LLaVA")
from methods._llava_common import make_gen
N = {"default": 128, "r889": 64}

def load(model_path, setting="default"):
    from llava.model.builder import load_pretrained_model
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)
    model.eval(); n = N[setting]
    idx = torch.linspace(0, 575, n).round().long().cuda()
    orig = model.encode_images
    def encode_images(images):
        f = orig(images)                       # (B, 576, 4096)
        return f[:, idx]
    model.encode_images = encode_images         # prepare_inputs_labels_for_multimodal 이 self.encode_images 를 부른다
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: n)
    return gen, dict(name="Uniform", setting=setting, visual_token_num=n, selection="evenly spaced indices of the 576 projector outputs", attn="sdpa(default)", prompt="vicuna_v1")

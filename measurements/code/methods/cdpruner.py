# -*- coding: utf-8 -*-
"""CDPruner (2506.10967): 인코더 측, 명령 조건부 다양성(DPP). 설정: default = 128 토큰 / r889 = 64 / r944 = 32."""
import torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": 128, "r889": 64, "r944": 32}
def load(model_path, setting="default"):
    use_repo("CDPruner")
    from llava.model.builder import load_pretrained_model
    n = SETTINGS[setting]
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", visual_token_num=n, device_map="cuda", torch_dtype=torch.float16)
    model.eval()
    # 공식 스크립트는 device_map="auto" 로 로드해 CLIP 시각 투영·텍스트 타워가 fp32 로 남는다. device_map="cuda" 는 전체를 fp16 으로 캐스팅해
    # clip_encoder.forward 의 visual_projection(image_embeds.float()) 에서 dtype 불일치(float != Half)가 난다 → 공식과 같이 fp32 로 되돌린다.
    # fp32 복원은 텍스트 타워 +0.5 GB 로 16 GB 경계를 넘겨 호스트 페이징(TTFT 1.6 s, 83 W)을 유발했다 → 전부 fp16 으로 두고
    # visual_projection 입력만 가중치 dtype 으로 맞춘다 (관련도 행렬이 fp16 으로 계산되는 점은 논문에 명시).
    vt = model.get_vision_tower()
    proj = vt.vision_tower.visual_projection
    class _CastIn(torch.nn.Module):
        def __init__(self, m): super().__init__(); self.m = m
        def forward(self, x): return self.m(x.to(self.m.weight.dtype))
    vt.vision_tower.visual_projection = _CastIn(proj)
    def nvis(model, out):
        if hasattr(model.model, "visual_token_num"): return model.model.visual_token_num
        return out[1] if isinstance(out, tuple) else n
    # CDPruner 는 명령어 조건부 선택이라 질문 텍스트를 generate(texts=...) 로 받는다 (저장소 model_vqa_loader 와 동일)
    gen = make_gen(tok, model, proc, n_vis_fn=nvis, per_call_kwargs=lambda q: {"texts": q})
    return gen, dict(name="CDPruner", setting=setting, visual_token_num=n)

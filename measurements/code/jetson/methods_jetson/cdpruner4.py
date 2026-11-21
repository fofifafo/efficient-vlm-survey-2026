# -*- coding: utf-8 -*-
"""CDPruner(공개 그대로), 언어 모델 4비트(NF4) — 8 GB Jetson 용(11/4: 네이티브 리눅스에서 공개판 보조 스트림 문제가 생기는지).
   설정은 데스크톱 methods/cdpruner.py 와 같음(default 128토큰, r889 64토큰), 다른 점은 load_4bit=True 뿐. visual_projection 입력 dtype 맞춤도 데스크톱과 같음."""
import os, torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": 128, "r889": 64}
# 공개판은 CLIP 을 FP32 로 세 번(시각 탑, 투영층만 쓰는 시각 탑 전체, 텍스트 탑) 올린 뒤 FP16 으로 바꿔 8 GB 를 넘김(11/4 첫 스모크에서 멈춤).
# 같은 가중치를 FP16 safetensors 사본(models/clip-vit-large-patch14-336-fp16)에서 바로 FP16 으로 올리고 투영층만 남김 — 최종 가중치·계산은 같음.
CLIP16 = os.path.expanduser("~/vlmbench/models/clip-vit-large-patch14-336-fp16")

def _patch_clip_loading():
    from llava.model.multimodal_encoder import clip_encoder as ce
    def load_model(self, device_map=None):
        if self.is_loaded: return
        self.image_processor = ce.CLIPImageProcessor.from_pretrained(CLIP16)
        self.vision_tower = ce.CLIPVisionModel.from_pretrained(CLIP16, torch_dtype=torch.float16, device_map=device_map)
        self.vision_tower.requires_grad_(False)
        self.is_loaded = True
    def load_text_tower(self, device_map=None):
        full = ce.CLIPVisionModelWithProjection.from_pretrained(CLIP16, torch_dtype=torch.float16, device_map=device_map)
        self.vision_tower.visual_projection = full.visual_projection
        del full; torch.cuda.empty_cache()
        self.text_tokenizer = ce.CLIPTokenizerFast.from_pretrained(CLIP16)
        self.text_tower = ce.CLIPTextModelWithProjection.from_pretrained(CLIP16, torch_dtype=torch.float16, device_map=device_map)
        self.text_tower.requires_grad_(False)
        self.max_position_embeddings = self.text_tower.config.max_position_embeddings
    ce.CLIPVisionTower.load_model = load_model
    ce.CLIPVisionTower.load_text_tower = load_text_tower

def load(model_path, setting="default"):
    use_repo("CDPruner")
    _patch_clip_loading()
    from llava.model.builder import load_pretrained_model
    n = SETTINGS[setting]
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", load_4bit=True, visual_token_num=n, device_map="cuda")
    model.eval()
    vt = model.get_vision_tower()
    proj = vt.vision_tower.visual_projection
    class _CastIn(torch.nn.Module):
        def __init__(self, m): super().__init__(); self.m = m
        def forward(self, x): return self.m(x.to(self.m.weight.dtype))
    vt.vision_tower.visual_projection = _CastIn(proj)
    def nvis(model, out):
        if hasattr(model.model, "visual_token_num"): return model.model.visual_token_num
        return out[1] if isinstance(out, tuple) else n
    gen = make_gen(tok, model, proc, n_vis_fn=nvis, per_call_kwargs=lambda q: {"texts": q})
    return gen, dict(name="CDPruner", setting=setting, visual_token_num=n, quant="nf4-4bit (bnb)", clip_load="fp16 safetensors copy, projection-only kept")

# -*- coding: utf-8 -*-
"""DART (2502.11494): LLM 내부, 중복 기반 토큰 제거 (SDPA/FlashAttention 호환). 저장소 model_vqa_loader 의 configure_DART 와 동일한 설정.
   설정: default = reduction 0.778 / max_trunc 128 (논문 예시) / r889 = 0.889 / 64."""
import torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": (0.778, 128), "r889": (0.889, 64), "r944": (0.944, 32)}
def load(model_path, setting="default", attn="sdpa"):
    use_repo("DART")
    from llava.model.builder import load_pretrained_model
    rr, mt = SETTINGS[setting]
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", attn_implementation=attn, device_map="cuda", torch_dtype=torch.float16)
    model.config.DART_config = {"K": 2, "image_token_start_index": 35, "image_token_length": 576, "max_num_trunction": mt,
                                "reduction_ratio": rr, "retain_token_num_for_llava_next": None, "pivot_image_token": 4, "pivot_text_token": 4}
    model.eval()
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: int(round(576 * (1 - rr))))
    return gen, dict(name="DART", setting=setting, reduction_ratio=rr, max_num_trunction=mt, attn=attn)

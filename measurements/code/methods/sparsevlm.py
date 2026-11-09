# -*- coding: utf-8 -*-
"""SparseVLM (2410.04417): LLM 내부, 텍스트 가이드 희소화. 저장소는 환경변수 RETAIN_TOKN(192/128/96/64)·USE_VERSION(1_0/2_0)을 import 시점에 읽는다.
   설정: default = 192 (논문 주 설정) / r889 = 64 / v2_192, v2_64 = SparseVLM+ (V2.0)."""
import os, torch
SETTINGS = {"default": ("192", "1_0"), "r889": ("64", "1_0"), "v2_192": ("192", "2_0"), "v2_64": ("64", "2_0")}
def load(model_path, setting="default"):
    n, ver = SETTINGS[setting]
    os.environ["RETAIN_TOKN"] = n; os.environ["USE_VERSION"] = ver
    from methods._llava_common import use_repo, make_gen
    use_repo("SparseVLMs")
    from llava.model.builder import load_pretrained_model
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)
    model.eval()
    # PC2 세션 발견(10/3): 저장소 builder 가 32개 층마다 flash_attn 어텐션 모듈을 추가로 만들어 가중치를 복사하지만 디코더 forward 는 self_attn 만 호출
    # (modelling_sparse_llama.py LlamaDynamicvitDecoderLayer.forward). 쓰이지 않는 복사본 4 GiB 가 16 GB GPU 를 넘겨(피크 17.6 GB) 호스트 페이징 → 삭제 (계산 경로 동일).
    freed = 0
    for layer in model.model.layers:
        if hasattr(layer, "flash_attn"): freed += sum(p.numel() * p.element_size() for p in layer.flash_attn.parameters()); del layer.flash_attn
    torch.cuda.empty_cache()
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: int(n))
    return gen, dict(name="SparseVLM", setting=setting, retain_tokens=int(n), version=ver, freed_dup_attn_gb=round(freed / 2**30, 2))

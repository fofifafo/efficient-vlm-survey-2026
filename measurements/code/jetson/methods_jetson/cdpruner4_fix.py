# -*- coding: utf-8 -*-
"""CDPruner(fix), 언어 모델 4비트(NF4) — 8 GB Jetson 용(11/4). 데스크톱 methods/cdpruner_fix.py 의 두 수정(보조 CUDA 스트림 제거, DPP 색인 장치 상주)을
   cdpruner4 로드 위에 그대로 적용. 선택 결과는 공개판과 같음."""
import torch
from methods_jetson.cdpruner4 import load as _load_asis
from methods.cdpruner_fix import encode_images_fixed, tower_forward_nostream

def load(model_path, setting="default"):
    gen, meta = _load_asis(model_path, setting)
    from llava.model.llava_arch import LlavaMetaForCausalLM
    from llava.model.multimodal_encoder.clip_encoder import CLIPVisionTower
    LlavaMetaForCausalLM.encode_images = encode_images_fixed
    CLIPVisionTower.forward = torch.no_grad()(tower_forward_nostream)
    meta.update(name="CDPruner(fix)", patch="no side CUDA streams in CLIP tower; device-resident DPP index")
    return gen, meta

# -*- coding: utf-8 -*-
"""CDPruner 수정판 ('cdpruner' = 공개 그대로, 'cdpruner_fix' = 아래 두 가지만 수정 — 수치·선택 결과 동일, 둘 다 보고).
   진단(10/2, profile_cdpruner3.py): 공개 구현은 CLIP 이미지/텍스트 인코딩을 매 호출 새 CUDA 보조 스트림 2개에서 돌린다.
   PyTorch 캐싱 할당자는 스트림별 풀을 따로 두므로 예약 메모리가 13.5 GB 할당 대비 15.5→16.9 GB 로 불어 16 GB 카드에서 WSL 호스트 페이징 발생
   → CLIP forward 7.5 ms(기준) 가 247~745 ms, TTFT 1.8 s, 평균 전력 80 W. (1) 보조 스트림 제거(기본 스트림 순차 실행, 계산 동일)
   (2) DPP 루프의 색인 텐서를 장치에 한 번만 생성(원본은 매 반복 CPU arange)."""
import torch
from methods.cdpruner import load as _load_asis

def tower_forward_nostream(self, images, texts=None):
    """repos/CDPruner/llava/model/multimodal_encoder/clip_encoder.py:forward 와 동일 계산, 스트림만 제거"""
    if type(images) is list:
        feats = []
        for image in images:
            out = self.vision_tower(image.to(device=self.device, dtype=self.dtype).unsqueeze(0), output_hidden_states=True)
            feats.append(self.feature_select(out).to(image.dtype))
        return feats
    outs = self.vision_tower(images.to(device=self.device, dtype=self.dtype), output_hidden_states=True)
    image_outputs = self.feature_select(outs)
    image_features = image_outputs.to(images.dtype)
    if texts is None: return image_features
    ti = self.text_tokenizer(text=texts, return_tensors="pt")
    seg = (ti.input_ids.shape[1] - 1) // self.max_position_embeddings + 1
    pad = self.max_position_embeddings * seg - ti.input_ids.shape[1]
    ti = {k: torch.cat([v, v.new_zeros((v.shape[0], pad))], dim=1).reshape(-1, self.max_position_embeddings).to(device=self.device) for k, v in ti.items()}
    text_embeds = self.text_tower(**ti).text_embeds
    image_embeds = self.vision_tower.vision_model.post_layernorm(image_outputs)
    image_embeds = self.vision_tower.visual_projection(image_embeds.float())
    return (image_features, image_embeds, text_embeds)

def encode_images_fixed(self, images, texts=None):
    image_features, image_embeds, text_embeds = self.get_model().get_vision_tower()(images, texts=texts)
    B, N, C = image_features.shape
    device = image_features.device
    image_features = self.get_model().mm_projector(image_features)
    image_normalized = image_features / image_features.norm(dim=-1, keepdim=True)
    image_normalized = image_normalized.float()
    similarity = torch.matmul(image_normalized, image_normalized.transpose(1, 2))
    image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
    text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)
    relevance = torch.matmul(image_embeds, text_embeds.t())
    relevance = (-relevance).mean(dim=-1)
    relevance = (relevance - relevance.min() + 1e-6) / (relevance.max() - relevance.min())
    kernel = relevance.unsqueeze(2) * similarity * relevance.unsqueeze(1)
    T = self.visual_token_num
    cis = torch.zeros((T, B, N), device=device)
    di2s = torch.diagonal(kernel, dim1=1, dim2=2).clone()
    select_idx = torch.empty((T, B), dtype=torch.long, device=device)
    ar = torch.arange(B, device=device)
    for i in range(T):
        j = torch.argmax(di2s, dim=-1)
        select_idx[i] = j
        eis = (kernel[ar, j] - torch.einsum('tb,tbn->bn', cis[:i, ar, j], cis[:i])) / torch.sqrt(di2s[ar, j]).unsqueeze(-1)
        cis[i, :, :] = eis
        di2s -= torch.square(eis)
        di2s[ar, j] = -float('inf')
    select_idx = torch.sort(select_idx.t()).values
    index_masks = torch.zeros(B, N, dtype=torch.bool, device=device)
    index_masks.scatter_(1, select_idx, True)
    return image_features, index_masks

def load(model_path, setting="default"):
    gen, meta = _load_asis(model_path, setting)
    from llava.model.llava_arch import LlavaMetaForCausalLM
    from llava.model.multimodal_encoder.clip_encoder import CLIPVisionTower
    LlavaMetaForCausalLM.encode_images = encode_images_fixed
    CLIPVisionTower.forward = torch.no_grad()(tower_forward_nostream)
    meta.update(name="CDPruner(fix)", patch="no side CUDA streams in CLIP tower; device-resident DPP index")
    return gen, meta

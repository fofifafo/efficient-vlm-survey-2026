# -*- coding: utf-8 -*-
"""FastV (2403.06764) — 저자 제공 KV-cache 판 (src/FastV/lmms-eval/fastv_kvcache.py, Zhihang Lin 기여).
   원본 inplace 판은 KV 캐시 미지원(매 디코딩 단계 전체 재계산, 공식 지연 실험은 max_new_tokens=1)이라 32 토큰 생성 비교에 부적합 → 저자가 lmms-eval 결과에 쓴 kv-cache 판을 표준 LLaVA 위에 얹어 측정(저장소 사본 repos/FastV_kv, build_fastv_kv.sh).
   동작: 층 K-1 의 어텐션(마지막 텍스트 토큰→이미지 토큰 576개, index 35~610)으로 상위 rank 개만 남기고 층 K 부터 제거; 이후 디코딩은 같은 집합을 봄.
   실행 환경: ~/venv_fastv (transformers 4.37.2 사본에 rotary seq_len 패치, 저자 README 5단계). run_harness.sh/run_acc.sh 가 자동 선택.
   설정: default = K=3(파일 기본), rank 288 (R=50%) / r889 = rank 64. 심사 대응(10/28): k2 = K=2(원 논문 설정), rank 288 / k2r889 = K=2, rank 64."""
import torch
from methods._llava_common import use_repo, make_gen
SETTINGS = {"default": 288, "r75": 144, "r889": 64, "k2": 288, "k2r889": 64}
KS = {"k2": 2, "k2r889": 2}          # 나머지 설정은 K=3
def load(model_path, setting="default"):
    import transformers; assert "venv_fastv" in transformers.__file__, f"FastV 는 ~/venv_fastv 로 실행해야 함 (현재 {transformers.__file__})"
    use_repo("FastV_kv")
    from llava.model.builder import load_pretrained_model
    from llava.model.language_model.fastv_kvcache import FastVLlamaModel
    tok, model, proc, _ = load_pretrained_model(model_path, None, "llava-v1.5-7b", device_map="cuda", torch_dtype=torch.float16)   # sdpa 기본: 디코딩 단계에서 4D 마스크가 None 이 되어 가지치기된 KV 길이와 충돌하지 않음(저자 설정). 탐침 호출은 output_attentions=True 로 eager 로 자동 전환
    assert isinstance(model.model, FastVLlamaModel), type(model.model)
    rank = SETTINGS[setting]
    K = KS.get(setting, 3); model.config.fastv_k = K; model.config.fastv_rank = rank
    model.eval()
    gen = make_gen(tok, model, proc, n_vis_fn=lambda m, o: rank)
    return gen, dict(name="FastV(kv-cache)", setting=setting, rank=rank, K=K, attn="sdpa(default); probe eager", transformers=transformers.__version__)

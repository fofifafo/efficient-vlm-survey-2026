#!/usr/bin/env bash
# FastV KV-cache 판 저장소 구성: 표준 LLaVA 사본 + 저자 제공 fastv_kvcache.py (K·rank 를 config 에서 읽고, 탐침 호출의 캐시 중복을 고치는 최소 수정)
set -e
W="$HOME/vlmbench/repos"; D="$W/FastV_kv"
rm -rf "$D"; cp -r "$W/LLaVA" "$D"
cp "$W/FastV/src/FastV/lmms-eval/fastv_kvcache.py" "$D/llava/model/language_model/fastv_kvcache.py"
python3 - "$D" <<'PY'
import sys; d = sys.argv[1]
p = f"{d}/llava/model/language_model/fastv_kvcache.py"; s = open(p).read()
a = """                K = 3
                ratio = 0.5
"""
assert s.count(a) == 1, "K/ratio block"
s = s.replace(a, """                K = getattr(self.config, 'fastv_k', 3)            # bench: config 로 조정 (저자 기본 3)
                rank = getattr(self.config, 'fastv_rank', 288)      # bench: 유지 토큰 수 (기본 576*0.5)
""")
b = "topk(int(576 * ratio))"; assert s.count(b) == 1; s = s.replace(b, "topk(rank)")
# 어텐션 탐침 호출(층 K-1)이 past_key_value 를 그대로 넘겨 DynamicCache 에 K/V 를 두 번 쌓는다(마스크 643 vs 1286 오류) →
# 탐침은 캐시 없이, 프리필(seq_length>1)에서만 수행. 디코딩 단계는 가지치기 집합이 고정되므로 탐침 불필요.
c = """                if decoder_layer.self_attn.layer_idx == K - 1:
                    temp_layer_outputs = decoder_layer(
                        hidden_states,
                        attention_mask=attention_mask,
                        position_ids=position_ids,
                        past_key_value=past_key_values,
                        output_attentions=True,
                        use_cache=use_cache,
                    )"""
assert s.count(c) == 1, "probe block"
s = s.replace(c, """                if decoder_layer.self_attn.layer_idx == K - 1 and seq_length > 1:   # bench: 프리필에서만, 캐시 미사용 탐침
                    temp_layer_outputs = decoder_layer(
                        hidden_states,
                        attention_mask=attention_mask,
                        position_ids=position_ids,
                        past_key_value=None,
                        output_attentions=True,
                        use_cache=False,
                    )""")
open(p, "w").write(s)
q = f"{d}/llava/model/language_model/llava_llama.py"; t = open(q).read()
old = "class LlavaLlamaModel(LlavaMetaModel, LlamaModel):"; assert t.count(old) == 1
t = t.replace(old, "from .fastv_kvcache import FastVLlamaModel\nclass LlavaLlamaModel(LlavaMetaModel, FastVLlamaModel):   # FastV kv-cache (저자 README 4단계)")
open(q, "w").write(t); print("FastV_kv built")
PY
grep -n "fastv_k\|fastv_rank\|topk\|past_key_value=None\|layer_idx == K - 1" "$D/llava/model/language_model/fastv_kvcache.py" | head; grep -n "FastVLlamaModel" "$D/llava/model/language_model/llava_llama.py"

#!/usr/bin/env bash
# FastV 전용 경량 환경: vlmbench conda env 위에 venv(--system-site-packages) 를 얹고 tokenizers 0.13.3 만 덮어쓴다 (vendored transformers 4.31 요구).
# 사용: bash fastv_env.sh   → ~/venv_fastv/bin/python 생성·검증
WORK=${WORK:-$HOME/vlmbench}; CONDA_ROOT=$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
V="$HOME/venv_fastv"
[ -x "$V/bin/python" ] || python -m venv --system-site-packages "$V"
"$V/bin/pip" install -q "tokenizers==0.13.3" 2>&1 | grep -v "already satisfied" | tail -3
"$V/bin/python" -c "import tokenizers, torch; print('tokenizers', tokenizers.__version__, 'torch', torch.__version__)"
cd "$WORK/repos/FastV"
PYTHONPATH="$WORK/repos/FastV/src/transformers/src:$WORK/repos/FastV/src/LLaVA" "$V/bin/python" - <<'PY' 2>&1 | grep -v Warning | tail -8
import os, transformers; print("transformers", transformers.__version__, transformers.__file__)
from transformers import TextIteratorStreamer; print("streamer ok")
import llava; from llava.model.builder import load_pretrained_model; from llava.conversation import conv_templates; print("llava ok", llava.__file__, "vicuna_v1" in conv_templates)
import inspect, transformers.models.llama.modeling_llama as ml; print("fast_v hooks in modeling_llama:", inspect.getsource(ml).count("fast_v"))
from transformers import AutoTokenizer; t = AutoTokenizer.from_pretrained(os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"), use_fast=False); print("tokenizer ok", len(t))
PY

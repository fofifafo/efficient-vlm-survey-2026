#!/usr/bin/env bash
# LLaVA(및 FastV·SparseVLM 등 LLaVA 패치 계열)는 transformers 4.37.2 를 전제한다 (4.46 은 generate 가 cache_position 을 넘겨 forward 가 깨짐).
# 정확도 평가는 lmms-eval 대신 자체 채점기(bench/score.py)를 쓴다 — 버전 충돌 회피 + 채점 규칙 공개.
set -euo pipefail
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
pip install -q "transformers==4.37.2" "tokenizers==0.15.1" "accelerate==0.27.2" "peft==0.10.0" 2>&1 | grep -v -E "WARNING|ERROR: pip's dependency" || true
python -c "import torch, transformers, accelerate; print('torch', torch.__version__, '| transformers', transformers.__version__, '| accelerate', accelerate.__version__)"
pip freeze > "$HOME/vlmbench/logs/pip_freeze_tf437.txt"
echo "DONE pin"

#!/usr/bin/env bash
# 모델·벤치 데이터 내려받기 (약 30 GB). 실행: bash download.sh
set -euo pipefail
WORK=${WORK:-$HOME/vlmbench}
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; mkdir -p "$HF_HOME"

echo "== 모델: LLaVA-1.5-7B (베이스라인 8개 공통 기반, ~13.5 GB)"
huggingface-cli download liuhaotian/llava-v1.5-7b --local-dir "$WORK/models/llava-v1.5-7b" --quiet
echo "== 비전 타워 (LLaVA-1.5 가 로드 시 참조)"
huggingface-cli download openai/clip-vit-large-patch14-336 --local-dir "$WORK/models/clip-vit-large-patch14-336" --quiet

echo "== 벤치 데이터 미리 받기 (GQA·POPE·TextVQA·MME; lmms-lab 미러)"
python - <<'PY'
from datasets import load_dataset
for name, cfg in [("lmms-lab/GQA", "testdev_balanced_instructions"), ("lmms-lab/GQA", "testdev_balanced_images"), ("lmms-lab/POPE", None), ("lmms-lab/textvqa", None), ("lmms-lab/MME", None)]:
    try:
        ds = load_dataset(name, cfg) if cfg else load_dataset(name)
        print(name, cfg or "", {k: len(v) for k, v in ds.items()})
    except Exception as e:
        print("!!", name, cfg, e)
PY
echo "DONE. 다음: python check_env.py"

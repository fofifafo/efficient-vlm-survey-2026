#!/usr/bin/env bash
# C2 배치 메모리 실험 실행(WSL). 사용: bash run_memory_batch.sh
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}; WORK=${WORK:-$HOME/vlmbench}; mkdir -p "$WORK/logs"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench; export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore
cd "$BENCH"; echo "gpu used before: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
python memory_batch.py --bs 1,2,4,8,16 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn"

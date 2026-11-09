#!/usr/bin/env bash
# vlmbench env 로 bench 디렉터리의 파이썬 스크립트 실행. 사용: bash run_py.sh profile_cdpruner.py
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
WORK=${WORK:-$HOME/vlmbench}; CONDA_ROOT=$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore; export HF_DATASETS_OFFLINE=1; export HF_HUB_OFFLINE=1
cd $BENCH && python "$@" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml|offline mode|cached dataset"

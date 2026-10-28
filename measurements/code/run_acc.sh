#!/usr/bin/env bash
# 사용: bash run_acc.sh <method> [setting] [tasks] [n]   예) bash run_acc.sh base default gqa 100
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
M=${1:-base}; SET=${2:-default}; TASKS=${3:-gqa,pope,textvqa,mme}; N=${4:-0}
WORK=${WORK:-$HOME/vlmbench}
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore; export HF_DATASETS_OFFLINE=1; export HF_HUB_OFFLINE=1
cd $BENCH
PY=python; if [ "$M" = fastv ] && [ -x "$HOME/venv_fastv/bin/python" ]; then PY="$HOME/venv_fastv/bin/python"; fi   # FastV: vendored transformers 4.31 용 venv
"$PY" eval_acc.py --method "$M" --setting "$SET" --tasks "$TASKS" --n "$N" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml|offline mode|cached dataset"
echo "DONE acc $M $SET"

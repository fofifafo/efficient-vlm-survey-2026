#!/usr/bin/env bash
# 사용: bash run_harness.sh <method> [n] [runs] [setting]
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
M=${1:-base}; N=${2:-500}; RUNS=${3:-5}; SET=${4:-default}
WORK=${WORK:-$HOME/vlmbench}
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore
cd $BENCH
PY=python; if [ "$M" = fastv ] && [ -x "$HOME/venv_fastv/bin/python" ]; then PY="$HOME/venv_fastv/bin/python"; fi   # FastV: vendored transformers 4.31 용 venv
"$PY" harness.py --method "$M" --n "$N" --runs "$RUNS" --setting "$SET" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml"
echo "DONE harness $M $SET"

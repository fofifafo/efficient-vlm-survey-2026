#!/usr/bin/env bash
# 재측정 후 원본 모델만 다른 작업 없이 다시 잰다(10/28 10:18 측정은 원고 컴파일과 겹쳤음).
BENCH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); WORK=$HOME/vlmbench; OUT="$WORK/results_remeasure_base2"; mkdir -p "$OUT"
CONDA_ROOT=$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )
echo "== base alone $(date +%H:%M) gpu $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
( source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench; export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore; cd "$BENCH"
  python harness.py --method base --n 500 --runs 5 --setting default --out "$OUT" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml" ) > "$WORK/logs/remeasure_base2.log" 2>&1
grep SUMMARY "$WORK/logs/remeasure_base2.log" | tail -1
echo "== done $(date +%H:%M)"

#!/usr/bin/env bash
# CDPruner 공개판/수정판 메모리·지연 진단(약 10–15분). run_profile_all.sh 가 끝난 뒤 실행(GPU 를 혼자 써야 함).
# 사용(WSL): bash /mnt/j/VLM-Survey/bench/run_cdpruner_diag.sh   [N=50]
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
WORK=${WORK:-$HOME/vlmbench}; N=${N:-50}; LOG="$WORK/logs"; mkdir -p "$LOG"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore
cd "$BENCH"
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv > "$LOG/cdpruner_diag_gpu_before.txt"
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv >> "$LOG/cdpruner_diag_gpu_before.txt" 2>&1
for job in "cdpruner default" "cdpruner r889" "cdpruner_fix default"; do
  set -- $job; echo "== diag $1 $2 $(date +%H:%M)"
  python profile_cdpruner_diag.py --method "$1" --setting "$2" --n "$N" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn" > "$LOG/cdpruner_diag_$1_$2.log"
  grep -E "SUMMARY|MEM_PEAK" "$LOG/cdpruner_diag_$1_$2.log" | cut -c1-400 || { echo "FAILED $1 $2"; grep -A4 Traceback "$LOG/cdpruner_diag_$1_$2.log" | tail -5; }
done
echo "== diag done $(date +%H:%M)"

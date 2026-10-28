#!/usr/bin/env bash
# 2차 리뷰 M2: 11개 설정의 TTFT GPU/호스트 분해. 먼저 스모크(base, 10문항) → 성공하면 전체(설정당 100문항).
# 사용(WSL): bash /mnt/j/VLM-Survey/bench/run_profile_all.sh   [N=100]
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
WORK=${WORK:-$HOME/vlmbench}; N=${N:-100}; LOG="$WORK/logs"; mkdir -p "$LOG"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore
cd "$BENCH"
run() { local m=$1 s=$2 n=$3; local PY=python; if [ "$m" = fastv ] && [ -x "$HOME/venv_fastv/bin/python" ]; then PY="$HOME/venv_fastv/bin/python"; fi
        "$PY" profile_ttft.py --method "$m" --setting "$s" --n "$n" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn"; }
echo "== smoke base default $(date +%H:%M)"
run base default 10 > "$LOG/profile_smoke.log" 2>&1
grep SUMMARY "$LOG/profile_smoke.log" || { echo "SMOKE FAILED"; tail -20 "$LOG/profile_smoke.log"; exit 1; }
for job in "base default" "vispruner default" "vispruner r889" "cdpruner_fix default" "cdpruner_fix r889" "sparsevlm default" "sparsevlm r889" "dart default" "dart r889" "fastv default" "fastv r889"; do
  set -- $job; echo "== $1 $2 $(date +%H:%M)"
  run "$1" "$2" "$N" > "$LOG/profile_$1_$2.log" 2>&1
  grep SUMMARY "$LOG/profile_$1_$2.log" | cut -c1-300 || { echo "FAILED $1 $2"; grep -A4 Traceback "$LOG/profile_$1_$2.log" | tail -5; }
done
echo "== profile done $(date +%H:%M)"

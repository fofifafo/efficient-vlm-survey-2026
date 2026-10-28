#!/usr/bin/env bash
# 심사 대응(10/28) 5080 실험: 단순 기준선(uniform 128/64, pool 144/64)과 FastV K=2(288/64).
# 0) 대조: 기준 모델 지연을 다시 재서 표 8(106.0 ms)과 같은 조건인지 확인 → ~/vlmbench/results_control/ (기존 결과를 덮어쓰지 않음)
# 1) 지연 500문항×5회, 2) 정확도 4벤치 전체. 결과: ~/vlmbench/results/<method>/ (새 방법·새 설정 이름이라 기존 파일과 겹치지 않음)
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}; WORK=${WORK:-$HOME/vlmbench}; mkdir -p "$WORK/logs" "$WORK/results_control"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
JOBS=("uniform default" "uniform r889" "pool default" "pool r889" "fastv k2" "fastv k2r889")
echo "gpu used before: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
echo "== control base default $(date +%H:%M)"
( source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench; export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore; cd "$BENCH"
  python harness.py --method base --n 500 --runs 5 --setting default --out "$WORK/results_control" 2>&1 | grep -v -E "Warning|warn|import pynvml" ) > "$WORK/logs/review_control_base.log" 2>&1
tail -2 "$WORK/logs/review_control_base.log"
for job in "${JOBS[@]}"; do set -- $job; echo "== latency $1 $2 $(date +%H:%M)"; bash "$BENCH/run_harness.sh" "$1" 500 5 "$2" > "$WORK/logs/review_lat_$1_$2.log" 2>&1; tail -2 "$WORK/logs/review_lat_$1_$2.log"; done
for job in "${JOBS[@]}"; do set -- $job; echo "== accuracy $1 $2 $(date +%H:%M)"; bash "$BENCH/run_acc.sh" "$1" "$2" > "$WORK/logs/review_acc_$1_$2.log" 2>&1; tail -3 "$WORK/logs/review_acc_$1_$2.log"; done
echo "== review baselines done $(date +%H:%M)"

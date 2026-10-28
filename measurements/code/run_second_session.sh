#!/usr/bin/env bash
# 심사 대응(10/28) 지연 재측정. 10/28 새벽 측정 때 원본 모델 TTFT 가 138.0 ms 로 표 8(106.0 ms)보다 느렸으므로,
# GPU 를 쓰는 앱을 닫은 상태에서 원본 모델부터 다시 잰다. 결과: ~/vlmbench/results_remeasure/ (기존 결과를 덮어쓰지 않음)
# 원본 TTFT <= 110 ms 이면 표 8 과 같은 상태로 보고 새 기준선 6개만, 아니면 표 8 의 10개 설정까지 모두 다시 잰다.
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}; WORK=${WORK:-$HOME/vlmbench}; OUT="$WORK/results_remeasure"; mkdir -p "$WORK/logs" "$OUT"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
NEW=("uniform default" "uniform r889" "pool default" "pool r889" "fastv k2" "fastv k2r889")
OLD=("vispruner default" "vispruner r889" "cdpruner_fix default" "cdpruner_fix r889" "sparsevlm default" "sparsevlm r889" "dart default" "dart r889" "fastv default" "fastv r889")
run() {  # method setting
  echo "== latency $1 $2 $(date +%H:%M) gpu $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
  ( source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench; export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore; cd "$BENCH"
    PY=python; if [ "$1" = fastv ] && [ -x "$HOME/venv_fastv/bin/python" ]; then PY="$HOME/venv_fastv/bin/python"; fi
    "$PY" harness.py --method "$1" --n 500 --runs 5 --setting "$2" --out "$OUT" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml" ) > "$WORK/logs/remeasure_$1_$2.log" 2>&1
  grep SUMMARY "$WORK/logs/remeasure_$1_$2.log" | tail -1
}
run base default
T=$(python3 -c "import json; print(round(json.load(open('$OUT/base/latency_default.json'))['ttft_ms_median'], 1))" 2>/dev/null || echo 999)
echo "base TTFT $T ms"
JOBS=("${NEW[@]}")
if python3 -c "import sys; sys.exit(0 if float('$T') <= 110 else 1)"; then echo "matches Table 8 -> new baselines only"; else echo "differs from Table 8 -> all settings"; JOBS=("${OLD[@]}" "${NEW[@]}"); fi
for job in "${JOBS[@]}"; do set -- $job; run "$1" "$2"; done
echo "== remeasure done $(date +%H:%M)"

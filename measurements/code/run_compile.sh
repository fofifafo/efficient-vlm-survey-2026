#!/usr/bin/env bash
# torch.compile 시도: 원본 eager / 시각 인코더 컴파일 / 전체 컴파일을 같은 세션에서 잰다. 인자: n runs 결과폴더접미사 설정목록(m:s,m:s)
BENCH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); WORK=$HOME/vlmbench; OUT="$WORK/results_compile${3:-}"; mkdir -p "$OUT" "$WORK/logs"
N=${1:-60}; R=${2:-1}; JOBS=${4:-base:default,base_compile:vision,base_compile:full}
CONDA_ROOT=$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )
for job in ${JOBS//,/ }; do
  m=${job%%:*}; s=${job##*:}
  echo "== $m $s $(date +%H:%M:%S) gpu $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
  ( source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench; export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore; cd "$BENCH"
    python harness.py --method "$m" --n $N --runs $R --setting "$s" --out "$OUT" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml" ) > "$WORK/logs/compile${3:-}_${m}_${s}.log" 2>&1
  grep -E "compile warm-up|recompile_limit|SUMMARY|Error" "$WORK/logs/compile${3:-}_${m}_${s}.log" | tail -4
done
echo "== done $(date +%H:%M:%S)"

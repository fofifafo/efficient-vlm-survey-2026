#!/usr/bin/env bash
# TextVQA: LLaVA 질문 파일 문장(질문 → OCR 줄)으로 표 8 의 17개 설정. 결과는 ~/vlmbench/results_tvqa_llava/
# 사용: bash run_tvqa_llava.sh [n(0=전량)] [out]   — PC2 는 표 9 의 11개만: JOBS 환경변수로 덮어씀
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}; WORK=${WORK:-$HOME/vlmbench}; N=${1:-0}; OUT=${2:-$WORK/results_tvqa_llava}
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf" PYTHONWARNINGS=ignore HF_DATASETS_OFFLINE=1 HF_HUB_OFFLINE=1
mkdir -p "$OUT" "$WORK/logs"; cd "$BENCH"
JOBS=${JOBS:-"base:default vispruner:default vispruner:r889 cdpruner_fix:default cdpruner_fix:r889 sparsevlm:default sparsevlm:r889 dart:default dart:r889 fastv:default fastv:r889 fastv:k2 fastv:k2r889 uniform:default uniform:r889 pool:default pool:r889"}
for j in $JOBS; do
  M=${j%%:*}; S=${j##*:}
  PY=python; if [ "$M" = fastv ] && [ -x "$HOME/venv_fastv/bin/python" ]; then PY="$HOME/venv_fastv/bin/python"; fi
  echo "$(date +%H:%M) start $M $S"
  "$PY" eval_acc.py --method "$M" --setting "$S" --tasks textvqa --n "$N" --out "$OUT" --textvqa_prompt llava 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn|import pynvml|offline mode|cached dataset" | tail -3
done
echo "$(date +%H:%M) ALL DONE"

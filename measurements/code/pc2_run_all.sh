#!/usr/bin/env bash
# PC2 일괄 실행: PC1 과 측정 조건을 맞추는 재측정 전부를 순서대로 돌린다 (약 4 h, FastV 포함 시 약 7 h).
# 사용: nohup setsid bash pc2_run_all.sh > ~/vlmbench/logs/pc2_all.log 2>&1 < /dev/null &
#       FastV 까지: DO_FASTV=1 nohup setsid bash pc2_run_all.sh > ~/vlmbench/logs/pc2_all.log 2>&1 < /dev/null &
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
WORK=${WORK:-$HOME/vlmbench}; LOG="$WORK/logs"; R="$WORK/results"; mkdir -p "$LOG" "$R"
echo "== PC2 run_all start $(date +%m/%d\ %H:%M)  BENCH=$BENCH"

# 0. 기존 PC2 결과 백업(1회) 후 지연 결과만 비운다. 정확도(GQA·POPE·MME)는 재사용하므로 백업본에 남는다.
for m in base vispruner dart sparsevlm cdpruner cdpruner_fix; do rm -f "$R/$m"/latency_*.json; done

# 1. 지연 (vicuna_v1 프롬프트, SDPA, 로드 후 empty_cache) — 9건
for spec in "base:default" "vispruner:default r889" "dart:default r889" "sparsevlm:default r889" "cdpruner_fix:default r889"; do
  m=${spec%%:*}; s=${spec#*:}
  METHODS="$m" SETTINGS="$s" bash "$BENCH/run_queue2.sh"
done
echo "== latency done $(date +%m/%d\ %H:%M)"

# 2. TextVQA 를 OCR 참조 토큰 포함 규약으로 재실행 — 9건
TASKS=textvqa SPEC="base vispruner:default,r889 dart:default,r889 sparsevlm:default,r889 cdpruner_fix:default,r889" bash "$BENCH/run_acc_queue.sh"
echo "== textvqa done $(date +%m/%d\ %H:%M)"

# 3. (선택) FastV kv-cache 판: 환경 구성 → 지연 2건 → 정확도 2건(전 벤치)
if [ "${DO_FASTV:-0}" = 1 ]; then
  bash "$BENCH/fastv_env.sh" && bash "$BENCH/fastv_env3.sh" && bash "$BENCH/build_fastv_kv.sh" || echo "!! FastV 환경 구성 실패"
  METHODS="fastv" SETTINGS="default r889" bash "$BENCH/run_queue2.sh"
  SPEC="fastv:default,r889" bash "$BENCH/run_acc_queue.sh"
  echo "== fastv done $(date +%m/%d\ %H:%M)"
fi

# 4. 결과 내보내기 → $BENCH/results_pc2 (지연 json, textvqa 정확도, 예측, 표)
OUT="$BENCH/results_pc2" TAG="PC2 RTX 5070 Ti" bash "$BENCH/export_results.sh"
cp "$LOG/pc2_all.log" "$BENCH/results_pc2/" 2>/dev/null
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader > "$BENCH/results_pc2/gpu.txt"
echo "PC2 ALL DONE $(date +%m/%d\ %H:%M)"

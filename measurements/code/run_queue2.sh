#!/usr/bin/env bash
# 순차 실행 큐 v2: SETTINGS 지정 가능. 스모크(20×1, 첫 설정) → 성공 시 설정별 본 측정(500×5).
# 사용: METHODS="fastv" SETTINGS="default r889" bash run_queue2.sh   /  METHODS="sparsevlm" SETTINGS="v2_192 v2_64" bash run_queue2.sh
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
METHODS=${METHODS:-"fastv"}; SETTINGS=${SETTINGS:-"default r889"}
WORK=${WORK:-$HOME/vlmbench}; LOG="$WORK/logs"
while pgrep -f "harness.py" > /dev/null; do sleep 30; done     # GPU 비길 때까지
for m in $METHODS; do
  first=${SETTINGS%% *}
  echo "== smoke $m $first $(date +%H:%M)"
  if bash $BENCH/run_harness.sh "$m" 20 1 "$first" > "$LOG/smoke_${m}_$first.log" 2>&1 && grep -q SUMMARY "$LOG/smoke_${m}_$first.log"; then
    echo "   smoke OK: $(grep SUMMARY "$LOG/smoke_${m}_$first.log" | head -1 | cut -c1-200)"
    for s in $SETTINGS; do
      echo "== full $m $s $(date +%H:%M)"
      bash $BENCH/run_harness.sh "$m" 500 5 "$s" > "$LOG/full_${m}_$s.log" 2>&1 || echo "   FULL FAILED $m $s"
      grep SUMMARY "$LOG/full_${m}_$s.log" | head -1 | cut -c1-220
    done
  else
    echo "   smoke FAILED $m $first — $(grep -E 'Error|error|Traceback' "$LOG/smoke_${m}_$first.log" | tail -2 | cut -c1-200)"
  fi
done
echo "DONE queue"

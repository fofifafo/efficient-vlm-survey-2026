#!/usr/bin/env bash
# 정확도 큐: 지연 큐(harness/run_queue)가 끝날 때까지 기다린 뒤 방법×설정별로 eval_acc 순차 실행.
# SPEC = "방법:설정,설정 ..." (설정 생략 시 default).  이미 결과가 있는 (방법,설정)은 eval_acc 가 재개(완료분 건너뜀).
# 사용: SPEC="base vispruner:default,r889" nohup setsid bash run_acc_queue.sh > ~/vlmbench/logs/accq.log 2>&1 &
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
SPEC=${SPEC:-"base vispruner:default,r889 dart:default,r889 cdpruner:default,r889 fastv:default,r889 sparsevlm:v2_192,v2_64"}
TASKS=${TASKS:-gqa,pope,textvqa,mme}; LOG="$HOME/vlmbench/logs"
while pgrep -f "harness.py|run_queue|eval_acc.py" > /dev/null; do sleep 60; done
for item in $SPEC; do
  m=${item%%:*}; ss=${item#*:}; [ "$ss" = "$item" ] && ss=default
  for s in ${ss//,/ }; do
    echo "== acc $m $s $(date +%m/%d\ %H:%M)"
    bash $BENCH/run_acc.sh "$m" "$s" "$TASKS" > "$LOG/acc_${m}_$s.log" 2>&1 || echo "   ACC FAILED $m $s"
    grep -E "^(gqa|pope|textvqa|mme) |min ->|Error" "$LOG/acc_${m}_$s.log" | tail -8 | cut -c1-200
  done
done
echo "DONE accq"

#!/usr/bin/env bash
# Jetson CDPruner 측정(11/4). 10월 base4·vispruner4 와 같은 프로토콜(GQA 500문항 × 5회, MAXN_SUPER, jetson_clocks 안 함).
# 순서: 스모크 10문항 → fix 128·64 지연 → fix 128·64 정확도 → 공개판 128 지연(느리거나 메모리가 넘칠 수 있어 맨 끝, 4시간 제한).
# 한 단계가 실패해도 다음 단계는 계속한다. 결과: ~/vlmbench/results_jetson/cdpruner4*/, 로그: ~/vlmbench/logs/cdpruner_<단계>.log
# 실행(Jetson): nohup bash ~/vlmbench/bench/jetson/run_cdpruner_jetson.sh > ~/vlmbench/logs/cdpruner_all.log 2>&1 &
set -u
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-}
source ~/vlmbench/venv/bin/activate
[ -f ~/vlmbench/env.sh ] && source ~/vlmbench/env.sh
cd ~/vlmbench/bench/jetson
OUT=~/vlmbench/results_jetson; L=~/vlmbench/logs; mkdir -p $L
step() { local name=$1; shift; echo "[$(date +%T)] start $name"; "$@" > $L/cdpruner_$name.log 2>&1; echo "[$(date +%T)] end $name rc=$?"; }
nvpmodel -q 2>/dev/null | head -1; free -g | head -2
# 메모리 감시: 가용 메모리 64 MB 미만이 20초 이어지면 측정 프로세스를 끊는다(11/4 첫 스모크 때 스왑으로 보드 전체가 멈춤).
( low=0; while true; do a=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  if [ "$a" -lt 64 ]; then low=$((low+1)); else low=0; fi
  if [ $low -ge 20 ]; then echo "[$(date +%T)] watchdog: MemAvailable ${a} MB, killing"; pkill -9 -f 'harness_jetson.py|acc_jetson.py'; low=0; fi
  sleep 1; done ) &
WD=$!; trap "kill $WD 2>/dev/null" EXIT
[ "${SKIP_SMOKE:-0}" = 1 ] || for ms in cdpruner4_fix:default cdpruner4_fix:r889 cdpruner4:default; do
  step smoke_${ms/:/_} python harness_jetson.py --method ${ms%%:*} --setting ${ms##*:} --n 10 --runs 1 --out $OUT/smoke
done
[ "${SMOKE_ONLY:-0}" = 1 ] && { echo "[$(date +%T)] smoke only, done"; exit 0; }
step lat_fix_default python harness_jetson.py --method cdpruner4_fix --setting default --n 500 --runs 5
step lat_fix_r889    python harness_jetson.py --method cdpruner4_fix --setting r889 --n 500 --runs 5
step acc_fix_default python acc_jetson.py --method cdpruner4_fix --setting default
step acc_fix_r889    python acc_jetson.py --method cdpruner4_fix --setting r889
step lat_asis_default timeout 4h python harness_jetson.py --method cdpruner4 --setting default --n 500 --runs 5
echo "[$(date +%T)] all done"

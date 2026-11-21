#!/usr/bin/env bash
# 공개판 CDPruner 128 지연, 100문항 x 1회(11/5). 11/4 500x5 실행은 첫 회차 중 보드가 멈추고 재부팅됨.
# 감시: 스왑이 시작 대비 1500 MB 넘게 늘거나 가용 메모리 100 MB 미만이 10초 이어지면 끊는다.
set -u
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-}
source ~/vlmbench/venv/bin/activate; source ~/vlmbench/env.sh
cd ~/vlmbench/bench/jetson; L=~/vlmbench/logs
s0=$(awk "/SwapTotal/{t=\$2}/SwapFree/{f=\$2}END{print int((t-f)/1024)}" /proc/meminfo)
( low=0; while true; do
  a=$(awk "/MemAvailable/{print int(\$2/1024)}" /proc/meminfo)
  s=$(awk "/SwapTotal/{t=\$2}/SwapFree/{f=\$2}END{print int((t-f)/1024)}" /proc/meminfo)
  if [ "$a" -lt 100 ]; then low=$((low+1)); else low=0; fi
  if [ $((s-s0)) -gt 1500 ] || [ $low -ge 10 ]; then echo "[$(date +%T)] watchdog: avail ${a} MB, swap +$((s-s0)) MB, killing"; pkill -9 -f harness_jetson.py; fi
  echo "$(date +%T) avail=$a swap=+$((s-s0))" >> $L/cdpruner_asis_short_mem.log
  sleep 1; done ) &
WD=$!; trap "kill $WD 2>/dev/null" EXIT
echo "[$(date +%T)] start lat_asis_short"
python harness_jetson.py --method cdpruner4 --setting default --n 100 --runs 1 > $L/cdpruner_lat_asis_short.log 2>&1
echo "[$(date +%T)] end lat_asis_short rc=$?"

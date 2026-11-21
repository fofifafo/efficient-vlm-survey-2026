#!/usr/bin/env bash
# 10월 run_sweep.sh(NF4 층 마이크로벤치 + 토큰 수 스윕 100문항×3회)를 화면 끈 상태로 다시(11/5). run_guioff_jetson.sh 가 끝나면 시작.
# 결과: ~/vlmbench/results_jetson/screen_off/sweep/ (10월 results_jetson_sweep·microbench_nf4.json 은 그대로 둠)
# 실행(Jetson): nohup bash ~/vlmbench/bench/jetson/run_sweep_guioff.sh > ~/vlmbench/logs/guioff_sweep.log 2>&1 &
set -u
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-}
source ~/vlmbench/venv/bin/activate
[ -f ~/vlmbench/env.sh ] && source ~/vlmbench/env.sh
cd ~/vlmbench/bench/jetson
OUT=~/vlmbench/results_jetson/screen_off/sweep; L=~/vlmbench/logs; mkdir -p $OUT
echo "[$(date +%T)] waiting for run_guioff_jetson.sh"
while pgrep -f "run_guioff_jetson\.sh" > /dev/null; do sleep 60; done
echo "[$(date +%T)] start"; systemctl is-active graphical.target; free -m | head -2
( low=0; while true; do a=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  if [ "$a" -lt 64 ]; then low=$((low+1)); else low=0; fi
  if [ $low -ge 20 ]; then echo "[$(date +%T)] watchdog: MemAvailable ${a} MB, killing"; pkill -9 -f 'harness_jetson.py|microbench_nf4.py'; low=0; fi
  sleep 1; done ) &
WD=$!; trap "kill $WD 2>/dev/null" EXIT
MB=~/vlmbench/results_jetson/microbench_nf4.json
cp -n $MB ${MB%.json}_guion.json
echo "== microbench $(date +%T)"; python microbench_nf4.py > $L/guioff_microbench_nf4.log 2>&1; tail -11 $L/guioff_microbench_nf4.log
mv $MB $OUT/microbench_nf4.json; cp ${MB%.json}_guion.json $MB
for job in "base4 sweep576" "vispruner4 t384" "vispruner4 t256" "vispruner4 default" "vispruner4 r889" "vispruner4 t32"; do
  set -- $job; echo "== $1 $2 $(date +%T)"
  python harness_jetson.py --method $1 --setting $2 --n 100 --runs 3 --out $OUT > $L/guioff_sweep_$1_$2.log 2>&1
  grep SUMMARY $L/guioff_sweep_$1_$2.log || { echo "FAILED"; grep -A5 Traceback $L/guioff_sweep_$1_$2.log | tail -6; }
done
echo "[$(date +%T)] sweep done"

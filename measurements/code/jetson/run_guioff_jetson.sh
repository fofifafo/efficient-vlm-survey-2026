#!/usr/bin/env bash
# 원본(base4)·VisPruner 128·64 지연을 화면 끈 상태(multi-user.target)에서 다시 잼(11/5). CDPruner(fix) 측정과 같은 부팅·같은 조건.
# 10월 결과(results_jetson/base4, vispruner4)는 화면 켠 상태라 덮어쓰지 않고 따로 저장: ~/vlmbench/results_jetson/screen_off/<방법>/
# 실행(Jetson): nohup bash ~/vlmbench/bench/jetson/run_guioff_jetson.sh > ~/vlmbench/logs/guioff_all.log 2>&1 &
set -u
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-}
source ~/vlmbench/venv/bin/activate
[ -f ~/vlmbench/env.sh ] && source ~/vlmbench/env.sh
cd ~/vlmbench/bench/jetson
OUT=~/vlmbench/results_jetson/screen_off; L=~/vlmbench/logs; mkdir -p $L $OUT
step() { local name=$1; shift; echo "[$(date +%T)] start $name"; "$@" > $L/guioff_$name.log 2>&1; echo "[$(date +%T)] end $name rc=$?"; }
nvpmodel -q 2>/dev/null | head -1; systemctl is-active graphical.target; free -m | head -2
# 메모리 감시(run_cdpruner_jetson.sh 와 같음): 가용 메모리 64 MB 미만이 20초 이어지면 측정 프로세스를 끊는다.
( low=0; while true; do a=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  if [ "$a" -lt 64 ]; then low=$((low+1)); else low=0; fi
  if [ $low -ge 20 ]; then echo "[$(date +%T)] watchdog: MemAvailable ${a} MB, killing"; pkill -9 -f 'harness_jetson.py'; low=0; fi
  sleep 1; done ) &
WD=$!; trap "kill $WD 2>/dev/null" EXIT
step lat_base_default python harness_jetson.py --method base4 --setting default --n 500 --runs 5 --out $OUT
step lat_vis_default  python harness_jetson.py --method vispruner4 --setting default --n 500 --runs 5 --out $OUT
step lat_vis_r889     python harness_jetson.py --method vispruner4 --setting r889 --n 500 --runs 5 --out $OUT
echo "[$(date +%T)] all done"

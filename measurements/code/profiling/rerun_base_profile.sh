#!/usr/bin/env bash
# 10/17: 5080 1차 분해 측정에서 base 만 기존 측정(106 ms)보다 26% 느림(화면·앱이 GPU 메모리 1.2–2.3 GB 사용 → 576토큰에서 메모리 부족 의심).
# 1차 결과는 results_profile/base_first_run/ 에 보관하고, 앱을 닫은 상태에서 base 만 다시 잰다.
WORK=$HOME/vlmbench; mkdir -p "$WORK/results_profile/base_first_run"
[ -f "$WORK/results_profile/base_first_run/base_default.json" ] || cp "$WORK/results_profile/base_default.json" "$WORK/results_profile/base_first_run/"
source "$HOME/colin/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"; export PYTHONWARNINGS=ignore
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}; cd "$BENCH"   # bench root (profile_ttft.py and methods/ side by side)
echo "gpu used before: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
python profile_ttft.py --method base --setting default --n 100 > "$WORK/logs/profile_base_default_rerun.log" 2>&1
grep SUMMARY "$WORK/logs/profile_base_default_rerun.log" | cut -c1-230

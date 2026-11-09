#!/usr/bin/env bash
# PC2 에서 FastV(kv-cache 판)만 측정: 환경 구성 → 스모크 → 지연 2건(288/64, 500×5) → 정확도 2건(전 벤치) → results_pc2/fastv/ 로 내보내기.
# 다른 방법의 결과는 건드리지 않는다. 약 3 h.
# 사용: cd ~/bench_pc1 && git pull && nohup setsid bash pc2_fastv.sh > ~/vlmbench/logs/pc2_fastv.log 2>&1 < /dev/null &
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
WORK=${WORK:-$HOME/vlmbench}; LOG="$WORK/logs"; R="$WORK/results"; mkdir -p "$LOG" "$R"
echo "== PC2 FastV start $(date +%m/%d\ %H:%M)  BENCH=$BENCH"
while pgrep -f "harness.py|eval_acc.py" > /dev/null; do echo "다른 측정이 끝나길 기다림"; sleep 60; done

# 1. 환경: ~/venv_fastv (vlmbench 위 venv + transformers 4.37.2 사본에 rotary 패치), repos/FastV_kv (표준 LLaVA + 저자 kv-cache 코드 + 탐침 캐시 수정)
bash "$BENCH/fastv_env.sh"  || { echo "!! fastv_env.sh 실패"; exit 1; }
bash "$BENCH/fastv_env3.sh" || { echo "!! fastv_env3.sh 실패"; exit 1; }
bash "$BENCH/build_fastv_kv.sh" || { echo "!! build_fastv_kv.sh 실패"; exit 1; }

# 2. 검증: 공용 env 는 패치되지 않았어야 하고(0), venv 사본은 3곳 패치
CONDA_ROOT=$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" ); source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
S=$(python -c "import transformers, os; print(os.path.join(os.path.dirname(transformers.__file__), 'models/llama/modeling_llama.py'))")
V=$("$HOME/venv_fastv/bin/python" -c "import transformers, os; print(os.path.join(os.path.dirname(transformers.__file__), 'models/llama/modeling_llama.py'))")
ns=$(grep -c "FastV kv-cache patch" "$S"); nv=$(grep -c "FastV kv-cache patch" "$V")
echo "patch check: shared env $ns (must be 0) | venv $nv (must be 3) | venv file $V"
[ "$ns" = 0 ] && [ "$nv" = 3 ] && case "$V" in *venv_fastv*) ;; *) false;; esac || { echo "!! 패치 상태 이상 — 중단"; exit 1; }
conda deactivate

# 3. 지연 2건 (run_queue2: 스모크 20×1 통과 시 본 측정 500×5)
rm -f "$R/fastv"/latency_*.json
METHODS="fastv" SETTINGS="default r889" bash "$BENCH/run_queue2.sh"
[ -f "$R/fastv/latency_default.json" ] || { echo "!! FastV 지연 측정 실패 — 로그: $LOG/smoke_fastv_default.log"; exit 1; }
echo "== latency done $(date +%m/%d\ %H:%M)"

# 4. 정확도 2건 (GQA·POPE·TextVQA(OCR 포함)·MME 전량, 재개 가능)
SPEC="fastv:default,r889" bash "$BENCH/run_acc_queue.sh"
echo "== accuracy done $(date +%m/%d\ %H:%M)"

# 5. 내보내기: results_pc2/fastv/ (지연 json, acc_<s>/accuracy.json·meta.json·preds_*.jsonl)
D="$BENCH/results_pc2/fastv"; mkdir -p "$D"
cp "$R/fastv"/latency_*.json "$D/"
for s in default r889; do mkdir -p "$D/acc_$s"; cp "$R/fastv/acc_$s"/*.json "$R/fastv/acc_$s"/*.jsonl "$D/acc_$s/" 2>/dev/null; done
cp "$LOG/pc2_fastv.log" "$D/" 2>/dev/null
python3 - "$D" <<'PY'
import json, os, sys
d = sys.argv[1]
for s in ("default", "r889"):
    l = json.load(open(f"{d}/latency_{s}.json")); a = json.load(open(f"{d}/acc_{s}/accuracy.json")) if os.path.exists(f"{d}/acc_{s}/accuracy.json") else {}
    print(f"FastV {s}: tokens {int(l['n_vis_tokens'])} TTFT {l['ttft_ms_median']:.1f} ms, e2e {l['total_ms_median']:.1f} ms, VRAM {l['peak_vram_gb']:.2f} GB, {l['energy_j_per_sample']:.1f} J"
          + (f" | GQA {100*a['gqa']['acc']:.2f} POPE F1 {100*a['pope']['f1']:.2f} TextVQA {100*a['textvqa']['acc']:.2f} MME-P {a['mme']['perception_total']:.1f}" if a else ""))
PY
echo "PC2 FASTV DONE $(date +%m/%d\ %H:%M)"
echo "결과 반환: cd $BENCH && git checkout pc2-results 2>/dev/null || git checkout -b pc2-results; git add results_pc2/fastv && git commit -m 'results_pc2: FastV (kv-cache) 288/64' && git push origin pc2-results"

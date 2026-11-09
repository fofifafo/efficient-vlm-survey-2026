#!/usr/bin/env bash
# WSL 결과를 repo 의 results_pc1/ 로 복사(지연 json, 정확도 json, meta, 예측 jsonl, FAILURES.md) + 표 8 생성
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}   # 스크립트 위치 = bench 루트 (PC1 /mnt/j/..., PC2 ~/... 어디서든)
D=${OUT:-$BENCH/results_pc1}; TAG=${TAG:-"PC1 RTX 5080"}; mkdir -p "$D"
cd ~/vlmbench/results && for m in base vispruner dart cdpruner cdpruner_fix fastv sparsevlm; do
  [ -d "$m" ] || continue; mkdir -p "$D/$m"; cp "$m"/*.json "$D/$m/" 2>/dev/null
  for s in "$m"/acc_*; do [ -d "$s" ] && mkdir -p "$D/$s" && cp "$s"/*.json "$s"/*.jsonl "$D/$s/"; done
done
cp ~/vlmbench/logs/FAILURES.md "$D/" 2>/dev/null; cp ~/vlmbench/results/_old/*.json "$D/" 2>/dev/null
bash $BENCH/run_py.sh make_table8.py --out "$D" --tag "$TAG"
du -sh "$D"

#!/usr/bin/env bash
# 베이스라인 8개 저장소 클론 (설치는 방법별로 따로). 실행: bash bg.sh clone_baselines.sh clone
WORK=${WORK:-$HOME/vlmbench}; cd "$WORK/repos"
declare -A R=( [FastV]=pkunlp-icler/FastV [SparseVLMs]=Gumpest/SparseVLMs [VisPruner]=Theia-4869/VisPruner [DART]=ZichenWen1/DART
               [CDPruner]=Theia-4869/CDPruner [LOOK-M]=SUSTechBruce/LOOK-M [MBQ]=thu-nics/MBQ [MQuant]=StiphyJay/MQuant )
for n in "${!R[@]}"; do
  if [ -d "$n" ]; then echo "skip $n (exists)"; continue; fi
  if git clone -q --depth 1 "https://github.com/${R[$n]}.git" "$n" 2>/dev/null; then
    echo "ok   $n  $(cd "$n" && git log -1 --format='%h %cs') files=$(find "$n" -type f | wc -l)"
    ls "$n"/*.md 2>/dev/null | head -2; ls "$n"/requirements*.txt "$n"/pyproject.toml "$n"/setup.py "$n"/environment*.y*ml 2>/dev/null
  else
    echo "FAIL $n  https://github.com/${R[$n]}"
  fi
done
echo "DONE clone"

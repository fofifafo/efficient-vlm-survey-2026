#!/usr/bin/env bash
# PC(WSL)에서 Jetson 용 safetensors 재분할 실행. 결과: ~/vlmbench/models/llava-v1.5-7b-st
source "$HOME/colin/etc/profile.d/conda.sh"; conda activate vlmbench
python "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/reshard_llava.py" ~/vlmbench/models/llava-v1.5-7b ~/vlmbench/models/llava-v1.5-7b-st
ls -la ~/vlmbench/models/llava-v1.5-7b-st | tail -5; du -sh ~/vlmbench/models/llava-v1.5-7b-st
ls -la ~/vlmbench/models/clip-vit-large-patch14-336/*/ 2>/dev/null | head; find ~/vlmbench/models/clip-vit-large-patch14-336 -maxdepth 3 -type f | head -20

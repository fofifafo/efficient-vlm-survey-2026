#!/usr/bin/env bash
# 환경 검증 실행 (모델 로드 + 1장 추론 + VRAM·전력)
WORK=${WORK:-$HOME/vlmbench}
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
source "$CONDA_ROOT/etc/profile.d/conda.sh"; conda activate vlmbench
export HF_HOME="$WORK/models/hf"
python "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check_env.py" 2>&1 | grep -v -E "FutureWarning|UserWarning|warnings.warn" | tail -15

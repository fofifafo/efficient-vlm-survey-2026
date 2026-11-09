#!/usr/bin/env bash
# 5장 측정 환경 (WSL2 Ubuntu, Blackwell GPU). 2026-10-01
# 실행: bash /mnt/j/VLM-Survey/bench/setup_env.sh   (WSL 안에서)
# 결과: conda env 'vlmbench'  (PyTorch 2.7+ cu128, lmms-eval, LLaVA)
set -euo pipefail
BENCH=${BENCH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
WORK=${WORK:-$HOME/vlmbench}          # 저장소·모델은 WSL 디스크(ext4)에 둔다 — /mnt/j 는 I/O 가 느림
mkdir -p "$WORK"/{repos,models,data,results,logs}

echo "== 1. 시스템 패키지 (sudo 비밀번호가 필요하면 건너뛰고 필수 도구만 확인)"
if sudo -n true 2>/dev/null; then
  sudo apt-get update -qq && sudo apt-get install -y -qq git git-lfs build-essential cmake ninja-build wget curl unzip htop > /dev/null
else
  echo "   sudo 불가 — apt 생략. 필수 도구 확인:"
  for t in git gcc g++ make wget curl; do echo "   $t -> $(command -v $t || echo MISSING)"; done
fi
git lfs install --skip-repo 2>/dev/null || true

echo "== 2. conda (기존 설치 ~/colin 이 있으면 그것을 사용)"
CONDA_ROOT=${CONDA_ROOT:-$( [ -d "$HOME/colin" ] && echo "$HOME/colin" || echo "$HOME/miniconda3" )}
if [ ! -d "$CONDA_ROOT" ]; then
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/mc.sh
  bash /tmp/mc.sh -b -p "$CONDA_ROOT"
fi
source "$CONDA_ROOT/etc/profile.d/conda.sh"; echo "   conda: $CONDA_ROOT"
conda config --set always_yes yes --set changeps1 no > /dev/null
conda env list | grep -q '^vlmbench ' || conda create -n vlmbench python=3.11 > /dev/null
conda activate vlmbench

echo "== 3. PyTorch (CUDA 12.8 — Blackwell sm_120 지원)"
pip install -q --upgrade pip
pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu128
python - <<'PY'
import torch; print("torch", torch.__version__, "cuda", torch.version.cuda, "ok", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "-")
print("arch list", torch.cuda.get_arch_list())
PY

echo "== 4. 공통 라이브러리"
pip install -q transformers==4.46.3 accelerate sentencepiece protobuf einops timm pillow numpy pandas scipy tqdm "huggingface_hub[cli]" pynvml nvidia-ml-py datasets
# LLaVA-1.5 공식 코드 (FastV·SparseVLM 등 대부분이 이 저장소를 기반으로 패치)
cd "$WORK/repos"
[ -d LLaVA ] || git clone -q https://github.com/haotian-liu/LLaVA.git
cd LLaVA && pip install -q -e . --no-deps && cd ..
# 평가: lmms-eval (GQA·POPE·TextVQA·MME 일괄)
[ -d lmms-eval ] || git clone -q https://github.com/EvolvingLMMs-Lab/lmms-eval.git
cd lmms-eval && pip install -q -e . && cd ..

echo "== 5. 환경 기록"
python -c "import torch,transformers;print('torch',torch.__version__,'transformers',transformers.__version__)" | tee "$WORK/logs/env.txt"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv | tee -a "$WORK/logs/env.txt"
pip freeze > "$WORK/logs/pip_freeze.txt"
echo "DONE. 다음: bash $BENCH/download.sh"

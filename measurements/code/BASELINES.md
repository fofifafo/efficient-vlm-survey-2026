# 5장 베이스라인 8개 — 설치·실행 체크리스트 (2026-10-01)

원칙: 방법당 **2시간** 넘기면 "실행 불가(사유)"로 기록하고 다음으로. 그 기록 자체가 재현성 결과다.
공통: 기반 LLaVA-1.5-7B FP16, 배치 1, 저자 권장 설정 + 공통 88.9% 프루닝(64 토큰). 결과는 `~/vlmbench/results/<method>/`.

| # | 방법 (arXiv) | 저장소 | 유형 | 예상 충돌 지점 | 상태 |
|---|---|---|---|---|---|
| 0 | LLaVA-1.5-7B 원본 | haotian-liu/LLaVA | 기준 | transformers 버전 고정(4.46) | ☐ |
| 1 | FastV (2403.06764) | pkunlp-icler/FastV | LLM 내부 어텐션 프루닝 (K=2, R=50/75%) | eager attention 필요 — SDPA/FlashAttn 비활성 옵션 확인 | ☐ |
| 2 | SparseVLM (2410.04417) | Gumpest/SparseVLMs | LLM 내부 텍스트 가이드 | LLaVA 패치 방식 — 저장소 자체 LLaVA 복사본 사용 | ☐ |
| 3 | VisPruner (2412.01818) | Theia-4869/VisPruner | 인코더 측 | 비교적 독립적, 순수 PyTorch | ☐ |
| 4 | DART (2502.11494) | ZichenWen1/DART | LLM 내부 중복 기반 | FlashAttention 호환 주장 — sm_120용 flash-attn 빌드 여부(안 되면 SDPA) | ☐ |
| 5 | CDPruner (2506.10967) | Theia-4869/CDPruner | 인코더 측 DPP | VisPruner와 같은 저자 — 환경 공유 가능 | ☐ |
| 6 | LOOK-M (2406.18139) | SUSTechBruce/LOOK-M | KV 캐시 압축 | transformers 캐시 API 변경에 취약 — 저장소 고정 버전 사용 | ☐ |
| 7 | MBQ (2412.19509) | thu-nics/MBQ | PTQ W4A8 / W3A16 | 커스텀 CUDA 커널(W3A16 GEMV) sm_120 컴파일 — 안 되면 W4A16 fake-quant 로 정확도·메모리만 | ☐ |
| 8 | MQuant (2502.00425) | StiphyJay/MQuant | 정적 W4A8 | 지원 모델에 LLaVA-1.5 포함 여부 확인(논문은 Qwen-VL·InternVL·MiniCPM-V) — 없으면 Qwen2-VL-2B 로 대체 | ☐ |

## 방법별 실행 절차 (공통)
1. `cd ~/vlmbench/repos && git clone <repo>`; 저장소 README 의 환경 요구를 `vlmbench` 환경과 비교(충돌 패키지만 별도 env).
2. 저장소 예시 명령으로 **이미지 1장 추론**이 되는지 확인 → `logs/<method>_smoke.txt`.
3. `bench/harness.py --method <m> --n 500` 으로 지연·TTFT·메모리·전력.
4. lmms-eval 로 GQA·POPE·TextVQA·MME 정확도 (`bench/run_eval.sh <m>`).
5. `results/<method>/summary.json` 에 저자 권장 설정 + 88.9% 설정 두 행.

## 기록 양식 (실행 불가 시)
```
method: MBQ
status: FAILED
stage: kernel build
error: nvcc fatal: unsupported gpu architecture 'compute_120'
time_spent_min: 95
fallback: W4A16 fake-quant (accuracy/memory only, no latency)
```

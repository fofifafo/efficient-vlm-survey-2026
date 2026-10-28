**Table 3.** Design-time efficiency: cost quantities reported by the authors of the 11 selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).

| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |
|---|---|---|---|---|---|---|---|---|
| DeepSeek-VL2 | 2412.10302 | 4.1.1 MoE VLM | 1.0–4.5B active | — | training 7/10/14 days on 16/33/42 nodes of 8 A100 GPUs | — | A100 | A |
| Kimi-VL | 2504.07491 | 4.1.1 MoE VLM | 2.8B active | — | — | — | n/s | C |
| LLaVA-MoD | 2408.15881 | 4.1.1 MoE student (distillation) | 23% trainable parameters | — | mimic distillation 960 vs 1,536 GPU hours (D2D+D2S vs D2S) | — | A100 | A |
| MoE-ViE ★ | 2608.17402 | 4.1.1 MoE vision encoder | 1.1B active | in a figure | MoE kernel >2.5×; batch-16 latency 318.76→82.59 ms (SigLIP2-g 76.39) | — | H100, CPU | A |
| Uni-MoE | 2405.11273 | 4.1.1 Unified MoE | n/s | — | — | — | A100, A800 | C |
| Nav-EE | 2510.01795 | 4.1.2 Early exit (navigation prior) | — | — | real vehicle (Autoware) 600→300 ms; LLaVA-7B 0.030→0.025 s | — | RTX 3090, vehicle | B |
| Penguin-VL | 2603.06569 | 4.1.3 LLM-based vision encoder | — | — | — | — | n/s | C |
| MiniDrive | 2409.07267 | 4.1.3 Lightweight encoder (driving, large-kernel CNN) | 83M parameters | 5.9B FLOPs | — | GPU memory 1.03 GB (MiniDrive224) | RTX 4090 | B |
| Cobra ★ | 2403.14520 | 4.1.4 State-space backbone | 3.5B total | — | 3–4× vs MobileVLM v2-3B | — | A100 | A |
| mmMamba ★ | 2502.13145 | 4.1.4 State-space, encoder-free linear | linear / hybrid | — | 20.6× (linear), 13.5× (hybrid) at 103K tokens; ~4× vs transformer | GPU memory −75.8% / −60.2% | A800, RTX 4090 | A |
| MiniCPM-V 4.5 ★ | 2509.18154 | 4.1.5 Connector (3D-Resampler) | 12–24× fewer tokens | — | 8.7% of Qwen2.5-VL-7B inference time (Video-MME) | 46.7% GPU memory | A100 | A |

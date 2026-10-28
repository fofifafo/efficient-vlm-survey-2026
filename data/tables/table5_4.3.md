**Table 5.** Compression: cost quantities reported by the authors of the 20 selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).

| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |
|---|---|---|---|---|---|---|---|---|
| SPEED-Q ★ | 2511.08914 | 4.3.1 Low-bit QAT/distillation (on-device) | 2-bit, 4-bit weight-only | — | — | 2-bit InternVL3-1B <400 MB (vs FastVLM 0.6B 1.5 GB); on S25 Ultra: file 1789→315 MB, footprint 1855→388 MB | Galaxy S25 Ultra (Snapdragon 8 Elite) | A |
| LUQ | 2509.23729 | 4.3.1 PTQ (<4-bit, layer-wise) | <4-bit (2.75 bit/param avg.) | — | — | −40% / −31% vs 4-bit; 2.5 GB budget | RTX 5000 (32 GB) | B |
| Quant Experts | 2602.24059 | 4.3.1 PTQ (MoE error reconstruction) | W4A6, W4A8, W3A16 | — | — | — | A800, RTX 4090 | C |
| QVLA | 2602.03782 | 4.3.1 PTQ (VLA, per-channel bits) | mixed precision, W4A4 | — | 1.49× (LIBERO) | VRAM 29.2% (15.2→7.0 GB) | A100, RTX 4090, Jetson AGX Orin | B |
| MQuant ★ | 2502.00425 | 4.3.1 PTQ (fully static) | W4A8 | — | latency up to −30%; prefill 23% and decode 100% faster; multi-turn 38.7% | memory efficiency 152.9% (as stated) | RTX 6000 | A |
| MASQuant | 2603.04800 | 4.3.1 PTQ (modality-aware smoothing) | W8A8, W4A8, W4A6, W4A4 | — | 2.5× vs FP16; 5–10% overhead vs MBQ | — | RTX 4090 | A |
| MBQ ★ | 2412.19509 | 4.3.1 PTQ (modality-balanced) | W3A16, W4A16, W4A8, W8A8 | — | W3A16 fused kernel 1.4× (OneVision-7B, RTX 4090); GEMV 1.2–5.0× | — | A100, RTX 4090 | A |
| QA-IG PTQ | 2603.17809 | 4.3.1 PTQ (sensitivity estimation) | W4A8, W3A16 | — | quantization time 0.58 vs 0.55 GPU h for MBQ (InternVL2-8B) | — | A800 | A |
| Q-VLM | 2410.08119 | 4.3.1 PTQ (weights/activations) | W6A6, W4A4 | — | generation 1.44× | 2.78× memory compression | n/s | A |
| LLaMA3 quantization study | 2404.14047 | 4.3.1 Quantization study (LLaMA3→LLaVA-NeXT) | 1–8 bit | — | 50–80 tok/s; AWQ kernel 89.8 tok/s | SmoothQuant 13.5 GB, 7 min (LLaMA2-7B) | 8× A800 | A |
| GRACE ★ | 2601.22709 | 4.3.2 QAT + distillation (INT4) | INT4, INT8 | — | 3× throughput with real INT4 kernel | −54% | A100, H100, L40 | A |
| QSVD ★ | 2510.16292 | 4.3.3 Low-rank (joint QKV SVD) | W8A8, W8A4, W4A4 + rank 30–40% | — | up to 2.1× on low-end GPU (no quantization), up to 13.1× with INT8 | KV cache at 9.38%, close to FP16 (W8A4) | RTX 4070 (12 GB), A6000, CPU | A |
| Structural pruning study | 2604.24380 | 4.3.4 Structural pruning (analysis) | 15/30/45/60% compression | — | 30% compression: 80.7 ms (layer) vs 84.4 ms (width) | 13.2→9.4 GiB (30%); +INT8 5.4 GiB | n/s | A |
| QSLAW | 2408.03735 | 4.3.5 Quantization-aware adaptation (QLoRA) | 4-bit | — | training 5.76 h (QLoRA 6.12, full 8.75) | 66.52 GB (QLoRA 66.92, full 71.54) | A100, A800 | A |
| Light-MER | 2607.12787 | 4.3.6 Distillation (<1B student) | 11× fewer parameters and FLOPs | 11× fewer | 4.6→3.1 s (−32.8%); direct mode 0.5 s | 20.04→2.54 GB (7.9×) | n/s | A |
| LLAVADI | 2407.19409 | 4.3.6 Distillation (analysis) | 13B→2.7B | — | — | — | n/s | C |
| MoVE-KD | 2501.01709 | 4.3.6 Distillation (multiple encoders) | — | — | — | — | A800 | C |
| LLaVA-MoD | 2408.15881 | 4.3.6 Distillation (small MoE student) | 0.3% training data, 23% trainable parameters | — | mimic distillation 960 vs 1,536 GPU hours (D2D+D2S vs D2S) | — | A100 | A |
| BitVLA ★ | 2506.07530 | 4.3.7 1-bit (VLA) | 1.58-bit W / INT8 A | — | 73 ms, 341 Hz (4.4× vs OpenVLA-OFT+ 321 ms) | 1.4 GB (11× smaller); encoder 0.8→0.1 GB | A100, H800, RTX 3050 Ti (4 GB) | A |
| SWIFT | 2408.05517 | Toolkit (fine-tuning, quantization, deployment) | — | — | training speed LoRA 0.95, full 1.43, LISA 2.66 samples/s | training memory LoRA 32.35, full 73.53, LISA 31.11 GiB (Qwen-7B-chat) | A100, CPU | A |

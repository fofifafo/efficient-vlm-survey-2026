**Table 9.** The same measurements on two consumer GPUs: RTX 5080 (Core Ultra 5 245KF) and RTX 5070 Ti (Ryzen 9 9950X3D), same code, settings and data. Speed-up is relative to the unmodified model on the same GPU.

| Method | Tokens | TTFT ms (5080) | ×5080 | TTFT ms (5070 Ti) | ×5070 Ti | Energy J (5080 / 5070 Ti) | GQA (5080 / 5070 Ti) | POPE F1 (5080 / 5070 Ti) |
|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (unmodified) | 576 | 106.0 | 1.00 | 121.4 | 1.00 | 43.7 / 42.9 | 61.95 / 61.97 | 85.84 / 85.87 |
| VisPruner | 128 | 63.9 | 1.66 | 59.7 | 2.03 | 24.1 / 22.7 | 58.03 / 57.92 | 84.46 / 84.23 |
| VisPruner | 64 | 55.8 | 1.90 | 50.5 | 2.40 | 21.5 / 19.9 | 56.18 / 55.52 | 80.08 / 80.38 |
| CDPruner (fix) | 128 | 78.2 | 1.36 | 71.9 | 1.69 | 25.5 / 23.7 | 59.82 / 59.80 | 87.38 / 87.51 |
| CDPruner (fix) | 64 | 58.6 | 1.81 | 53.5 | 2.27 | 21.9 / 20.3 | 58.65 / 58.73 | 87.47 / 87.54 |
| SparseVLM | 192 | 85.0 | 1.25 | 82.3 | 1.47 | 29.1 / 28.4 | 59.44 / 59.43 | 85.52 / 85.35 |
| SparseVLM | 64 | 68.1 | 1.56 | 65.3 | 1.86 | 24.1 / 22.7 | 53.73 / 53.63 | 77.85 / 77.63 |
| DART | 128 | 72.9 | 1.45 | 72.7 | 1.67 | 27.4 / 25.5 | 58.84 / 58.97 | 80.51 / 80.36 |
| DART | 64 | 60.7 | 1.75 | 64.1 | 1.89 | 24.7 / 23.6 | 56.40 / 56.37 | 74.34 / 74.21 |
| FastV (KV cache) | 288 | 86.1 | 1.23 | 92.8 | 1.31 | 34.2 / 33.4 | 60.30 / 60.24 | 83.39 / 83.23 |
| FastV (KV cache) | 64 | 60.4 | 1.75 | 58.1 | 2.09 | 24.7 / 23.5 | 53.69 / 53.60 | 68.16 / 68.23 |

Maximum absolute difference between GPUs over all settings: GQA 0.66, POPE F1 0.3, TextVQA 0.16, MME perception 15.72 (of 2,000); peak memory 0.02 GB. Spearman ρ of TTFT across the 10 compressed settings: 0.98.

**Table 10.** The unmodified model and VisPruner on a Jetson Orin Nano Developer Kit (8 GB unified memory, MAXN SUPER mode), with the language model in 4-bit NF4 because the FP16 model does not fit. Latency and energy: median of 5 runs × the same 500 GQA questions as Tables 8–9; energy is the board input power (VDD_IN). Accuracy: the same 500 GQA questions, 4-bit on the Jetson and FP16 on the RTX 5080.

| Method | Tokens | TTFT (ms) | Speed-up | End-to-end (ms) | Energy (J/sample) | Energy ratio | Peak memory (GB) | GQA-500, 4-bit | GQA-500, FP16 (RTX 5080) |
|---|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (unmodified) | 576 | 1955.6 | 1.00× | 2345.0 | 45.8 | 1.00× | 5.03 | 59.6 | 60.0 |
| VisPruner | 128 | 1191.5 | 1.64× | 1423.9 | 26.7 | 1.71× | 4.59 | 55.0 | 56.2 |
| VisPruner | 64 | 973.0 | 2.01× | 1376.0 | 23.3 | 1.97× | 4.59 | 54.2 | 55.0 |

Peak system memory (CPU and GPU share it) reached 7.2 of 7.4 GB for the unmodified model. Idle board power: 3.7 W.

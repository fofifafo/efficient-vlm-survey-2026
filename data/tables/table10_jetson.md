**Table 10.** The unmodified model and VisPruner on a Jetson Orin Nano Developer Kit (8 GB unified memory, MAXN SUPER mode), with the language model in 4-bit NF4 because the FP16 model does not fit. Latency and energy: median of 5 runs × the same 500 GQA questions as Tables 8–9; energy is the board input power (VDD_IN). Accuracy: the same 500 GQA questions, 4-bit on the Jetson and FP16 on the RTX 5080.

| Method | Tokens | TTFT (ms) | Speed-up | End-to-end (ms) | Energy (J/sample) | Energy ratio | Peak memory (GB) | GQA-500, 4-bit | GQA-500, FP16 (RTX 5080) |
|---|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (unmodified) | 576 | 1965.6 | 1.00× | 2374.9 | 47.0 | 1.00× | 5.03 | 59.6 | 60.0 |
| VisPruner | 128 | 1197.4 | 1.64× | 1431.3 | 27.4 | 1.72× | 4.59 | 55.0 | 56.2 |
| CDPruner (fix) | 128 | 1273.0 | 1.54× | 1505.7 | 28.1 | 1.68× | 4.77 | 57.6 | 57.2 |
| VisPruner | 64 | 972.6 | 2.02× | 1353.5 | 23.8 | 1.98× | 4.59 | 54.2 | 55.0 |
| CDPruner (fix) | 64 | 1000.0 | 1.97× | 1367.5 | 24.0 | 1.96× | 4.70 | 58.0 | 57.2 |

Peak system memory (CPU and GPU share it) reached 7.2 of 7.4 GB for the unmodified model. Idle board power: 4.3 W.

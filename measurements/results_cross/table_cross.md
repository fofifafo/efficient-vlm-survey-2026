# Cross-GPU measurement — PC1 RTX 5080 16 GB vs PC2 RTX 5070 Ti 16 GB
LLaVA-1.5-7B FP16, batch 1, vicuna_v1 prompt, SDPA attention, cache released after load; latency = median of 5 runs × 500 GQA samples; accuracy = full benchmarks (TextVQA with OCR reference tokens).

## Latency and resources

| Method | Tokens | TTFT ms 5080 (×) | TTFT ms 5070 Ti (×) | End-to-end ms 5080 / 5070 Ti | Peak VRAM GB 5080 / 5070 Ti | Energy J 5080 / 5070 Ti |
|---|---|---|---|---|---|---|
| LLaVA-1.5-7B | 576 | 106.0 (1.00×) | 121.4 (1.00×) | 143.2 / 156.0 | 13.95 / 13.95 | 43.7 / 42.9 |
| VisPruner | 128 | 63.9 (1.66×) | 59.7 (2.03×) | 98.1 / 88.9 | 13.51 / 13.52 | 24.1 / 22.7 |
| VisPruner | 64 | 55.8 (1.90×) | 50.5 (2.40×) | 88.7 / 81.2 | 13.51 / 13.52 | 21.5 / 19.9 |
| CDPruner (fix) | 128 | 78.2 (1.36×) | 71.9 (1.69×) | 116.0 / 101.0 | 13.69 / 13.69 | 25.5 / 23.7 |
| CDPruner (fix) | 64 | 58.6 (1.81×) | 53.5 (2.27×) | 93.8 / 84.5 | 13.62 / 13.62 | 21.9 / 20.3 |
| SparseVLM | 192 | 85.0 (1.25×) | 82.3 (1.47×) | 130.2 / 114.8 | 13.56 / 13.56 | 29.1 / 28.4 |
| SparseVLM | 64 | 68.1 (1.56×) | 65.3 (1.86×) | 113.5 / 98.0 | 13.49 / 13.49 | 24.1 / 22.7 |
| DART | 128 | 72.9 (1.45×) | 72.7 (1.67×) | 119.1 / 102.7 | 13.50 / 13.50 | 27.4 / 25.5 |
| DART | 64 | 60.7 (1.75×) | 64.1 (1.89×) | 105.4 / 94.9 | 13.43 / 13.43 | 24.7 / 23.6 |
| FastV (kv) | 288 | 86.1 (1.23×) | 92.8 (1.31×) | 132.1 / 123.2 | 13.69 / 13.69 | 34.2 / 33.4 |
| FastV (kv) | 64 | 60.4 (1.75×) | 58.1 (2.09×) | 103.4 / 94.1 | 13.47 / 13.47 | 24.7 / 23.5 |

## Accuracy (5080 / 5070 Ti)

| Method | Tokens | GQA | POPE F1 | TextVQA | MME-P |
|---|---|---|---|---|---|
| LLaVA-1.5-7B | 576 | 61.95 / 61.97 | 85.84 / 85.87 | 60.57 / 60.63 | 1526.7 / 1528.1 |
| VisPruner | 128 | 58.03 / 57.92 | 84.46 / 84.23 | 58.96 / 58.85 | 1475.1 / 1463.3 |
| VisPruner | 64 | 56.18 / 55.52 | 80.08 / 80.38 | 58.15 / 58.24 | 1387.1 / 1372.6 |
| CDPruner (fix) | 128 | 59.82 / 59.80 | 87.38 / 87.51 | 58.67 / 58.83 | 1470.7 / 1465.5 |
| CDPruner (fix) | 64 | 58.65 / 58.73 | 87.47 / 87.54 | 57.75 / 57.84 | 1407.8 / 1414.7 |
| SparseVLM | 192 | 59.44 / 59.43 | 85.52 / 85.35 | 59.71 / 59.62 | 1466.0 / 1459.8 |
| SparseVLM | 64 | 53.73 / 53.63 | 77.85 / 77.63 | 55.55 / 55.59 | 1307.0 / 1296.3 |
| DART | 128 | 58.84 / 58.97 | 80.51 / 80.36 | 59.10 / 59.01 | 1481.2 / 1482.5 |
| DART | 64 | 56.40 / 56.37 | 74.34 / 74.21 | 56.89 / 56.97 | 1430.9 / 1420.4 |
| FastV (kv) | 288 | 60.30 / 60.24 | 83.39 / 83.23 | 60.27 / 60.33 | 1517.3 / 1518.3 |
| FastV (kv) | 64 | 53.69 / 53.60 | 68.16 / 68.23 | 55.86 / 55.88 | 1318.3 / 1302.6 |

## Agreement

- Max |PC1 − PC2| accuracy: GQA 0.66, POPE F1 0.30, TextVQA 0.16, MME-P 15.7 (of 2,000).
- Spearman ρ of method TTFT between GPUs (10 settings): 0.98.
- Base TTFT 5080 / 5070 Ti: 106.0 / 121.4 ms (5080 13% faster); compressed settings where 5070 Ti is faster: 8 of 10.
- Base energy 5080 / 5070 Ti: 43.7 / 42.9 J; max VRAM difference 0.02 GB.
- All accuracy on both GPUs uses the same settings: max_new_tokens 16, FP16 throughout, CDPruner fix variant (PC2 GQA/POPE/MME re-measured 2026-10-26, results_pc2_accuracy).

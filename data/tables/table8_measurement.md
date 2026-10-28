**Table 8.** Measurements on the RTX 5080 (LLaVA-1.5-7B, FP16, batch size 1). Latency: median of 5 runs × 500 GQA test-dev questions; TTFT = time to first token; end-to-end = up to 32 generated tokens. Accuracy: full GQA test-dev balanced, POPE (F1), TextVQA validation (with OCR tokens) and MME perception. CDPruner (as released) uses two CUDA side streams per call and pages to host memory on a 16 GB GPU; CDPruner (fix) runs the same operations on the default stream (Section 5.1).

| Method | Tokens | TTFT (ms) | Speed-up | End-to-end (ms) | Peak memory (GB) | Energy (J/sample) | GQA | POPE F1 | TextVQA | MME-P |
|---|---|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (unmodified) | 576 | 106.0 | 1.00× | 143.2 | 13.95 | 43.7 | 61.9 | 85.8 | 60.6 | 1527 |
| VisPruner | 128 | 63.9 | 1.66× | 98.1 | 13.51 | 24.1 | 58.0 | 84.5 | 59.0 | 1475 |
| VisPruner | 64 | 55.8 | 1.90× | 88.7 | 13.51 | 21.5 | 56.2 | 80.1 | 58.1 | 1387 |
| CDPruner (fix) | 128 | 78.2 | 1.36× | 116.0 | 13.69 | 25.5 | 59.8 | 87.4 | 58.7 | 1471 |
| CDPruner (fix) | 64 | 58.6 | 1.81× | 93.8 | 13.62 | 21.9 | 58.7 | 87.5 | 57.8 | 1408 |
| SparseVLM | 192 | 85.0 | 1.25× | 130.2 | 13.56 | 29.1 | 59.4 | 85.5 | 59.7 | 1466 |
| SparseVLM | 64 | 68.1 | 1.56× | 113.5 | 13.49 | 24.1 | 53.7 | 77.9 | 55.5 | 1307 |
| DART | 128 | 72.9 | 1.45× | 119.1 | 13.50 | 27.4 | 58.8 | 80.5 | 59.1 | 1481 |
| DART | 64 | 60.7 | 1.75× | 105.4 | 13.43 | 24.7 | 56.4 | 74.3 | 56.9 | 1431 |
| FastV (KV cache) | 288 | 86.1 | 1.23× | 132.1 | 13.69 | 34.2 | 60.3 | 83.4 | 60.3 | 1517 |
| FastV (KV cache) | 64 | 60.4 | 1.75× | 103.4 | 13.47 | 24.7 | 53.7 | 68.2 | 55.9 | 1318 |
| CDPruner (as released) | 128 | 492.3 | 0.22× | 551.9 | 13.98 | 75.5 | — | — | — | — |
| CDPruner (as released) | 64 | 1614.7 | 0.07× | 1699.6 | 13.91 | 127.1 | — | — | — | — |

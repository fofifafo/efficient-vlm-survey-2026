# Table 8 — PC1 RTX 5080, LLaVA-1.5-7B FP16, vicuna_v1 prompt, greedy; latency = median of 5 runs × 500 GQA samples; accuracy = full benchmarks

| Method | Vis. tokens | TTFT ms (×base) | p90 | End-to-end ms | Peak VRAM GB | Energy J/sample | GQA | POPE F1 | TextVQA | MME-P | MME-C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (base) | 576 | 106.0 (1.00×) | 119.0 | 143.2 | 13.95 | 43.7 | 61.9 | 85.8 | 60.6 | 1527 | 310 |
| VisPruner | 128 | 63.9 (1.66×) | 81.2 | 98.1 | 13.51 | 24.1 | 58.0 | 84.5 | 59.0 | 1475 | 334 |
| VisPruner | 64 | 55.8 (1.90×) | 86.3 | 88.7 | 13.51 | 21.5 | 56.2 | 80.1 | 58.1 | 1387 | 353 |
| CDPruner (fix) | 128 | 78.2 (1.36×) | 115.7 | 116.0 | 13.69 | 25.5 | 59.8 | 87.4 | 58.7 | 1471 | 343 |
| CDPruner (fix) | 64 | 58.6 (1.81×) | 81.3 | 93.8 | 13.62 | 21.9 | 58.7 | 87.5 | 57.8 | 1408 | 332 |
| FastV (kv-cache) | 288 | 86.1 (1.23×) | 101.8 | 132.1 | 13.69 | 34.2 | 60.3 | 83.4 | 60.3 | 1517 | 315 |
| FastV (kv-cache) | 64 | 60.4 (1.75×) | 80.2 | 103.4 | 13.47 | 24.7 | 53.7 | 68.2 | 55.9 | 1318 | 345 |
| SparseVLM | 192 | 85.0 (1.25×) | 98.3 | 130.2 | 13.56 | 29.1 | 59.4 | 85.5 | 59.7 | 1466 | 328 |
| SparseVLM | 64 | 68.1 (1.56×) | 85.0 | 113.5 | 13.49 | 24.1 | 53.7 | 77.9 | 55.5 | 1307 | 301 |
| DART | 128 | 72.9 (1.45×) | 94.5 | 119.1 | 13.50 | 27.4 | 58.8 | 80.5 | 59.1 | 1481 | 340 |
| DART | 64 | 60.7 (1.75×) | 81.9 | 105.4 | 13.43 | 24.7 | 56.4 | 74.3 | 56.9 | 1431 | 352 |
| CDPruner (as released) | 128 | 492.3 (0.22×) | 1112.0 | 551.9 | 13.98 | 75.5 |  |  |  |  |  |
| CDPruner (as released) | 64 | 1614.7 (0.07×) | 1790.6 | 1699.6 | 13.91 | 127.1 |  |  |  |  |  |

Notes: CDPruner (as released) numbers are unstable on 16 GB (host paging caused by per-call side CUDA streams); the fix variant removes the streams only. FastV uses the authors' kv-cache variant (original in-place variant has no KV cache). SparseVLM is measured after deleting an unused 4 GiB flash_attn weight copy that its builder creates (computation path unchanged); as released it peaks at 17.6 GB and pages to host memory on 16 GB GPUs.

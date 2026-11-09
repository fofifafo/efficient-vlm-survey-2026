# Table 8 — PC2 RTX 5070 Ti, LLaVA-1.5-7B FP16, vicuna_v1 prompt, greedy; latency = median of 5 runs × 500 GQA samples; accuracy = full benchmarks

| Method | Vis. tokens | TTFT ms (×base) | p90 | End-to-end ms | Peak VRAM GB | Energy J/sample | GQA | POPE F1 | TextVQA | MME-P | MME-C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LLaVA-1.5-7B (base) | 576 | 121.4 (1.00×) | 132.3 | 156.0 | 13.95 | 42.9 |  |  | 60.6 |  |  |
| VisPruner | 128 | 59.7 (2.03×) | 66.9 | 88.9 | 13.52 | 22.7 |  |  | 58.8 |  |  |
| VisPruner | 64 | 50.5 (2.40×) | 59.5 | 81.2 | 13.52 | 19.9 |  |  | 58.2 |  |  |
| CDPruner (fix) | 128 | 71.9 (1.69×) | 78.9 | 101.0 | 13.69 | 23.7 |  |  | 58.8 |  |  |
| CDPruner (fix) | 64 | 53.5 (2.27×) | 62.4 | 84.5 | 13.62 | 20.3 |  |  | 57.8 |  |  |
| SparseVLM | 192 | 82.3 (1.47×) | 85.9 | 114.8 | 13.56 | 28.4 |  |  | 59.6 |  |  |
| SparseVLM | 64 | 65.3 (1.86×) | 69.7 | 98.0 | 13.49 | 22.7 |  |  | 55.6 |  |  |
| DART | 128 | 72.7 (1.67×) | 74.3 | 102.7 | 13.50 | 25.5 |  |  | 59.0 |  |  |
| DART | 64 | 64.1 (1.89×) | 65.8 | 94.9 | 13.43 | 23.6 |  |  | 57.0 |  |  |

Notes: CDPruner (as released) numbers are unstable on 16 GB (host paging caused by per-call side CUDA streams); the fix variant removes the streams only. FastV uses the authors' kv-cache variant (original in-place variant has no KV cache). SparseVLM is measured after deleting an unused 4 GiB flash_attn weight copy that its builder creates (computation path unchanged); as released it peaks at 17.6 GB and pages to host memory on 16 GB GPUs.

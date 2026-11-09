**Table 6.** Execution-time efficiency: cost quantities reported by the authors of the 20 selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).

| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |
|---|---|---|---|---|---|---|---|---|
| TokenCarve | 2503.10501 | 4.4.1 Tokens, 2-stage information-preserving | 576→128 (22.2%) | — | 1.124→0.911 s (1.23×); 1.33× at 64 tokens | KV cache −64% (100→36%) | V100 | A |
| CDPruner ★ | 2506.10967 | 4.4.1 Tokens, conditional diversity | 77.8–94.4% | −95% (LLaVA-NeXT-7B) | CUDA latency −78%; <10 ms extra | GPU memory −17% | A100 | A |
| DART ★ | 2502.11494 | 4.4.1 Tokens, duplication-based | 88.9% removed (64 tokens) | 12.8% (LLaVA-NeXT-7B) | 1.99× total; 2.99× prefill | KV cache 1,512→168 MB (LLaVA-NeXT-7B, 320 tokens) | n/s | A |
| VisPruner ★ | 2412.01818 | 4.4.1 Tokens, encoder-side | 94.4% removed (160 tokens kept) | −91% (7B) / >95% | latency −75% | — | A100 | A |
| HiDrop | 2602.23699 | 4.4.1 Tokens, hierarchical (learned) | ~90% (88.9/91.7%) | — | prefill 63.6→32.6 ms (→28.8 ms); training 1.72× | — | A100 | A |
| FastV ★ | 2403.06764 | 4.4.1 Tokens, in-LLM | R = 50% (K = 2) / 75% | −45% (13B); 52%→33% by setting | 0.344→0.230 s/example (7B, A-OKVQA); 13B 0.539→0.341 s | GPU 19→16 GB (7B), 38→30 GB (13B) | A40 | A |
| FitPrune | 2409.10197 | 4.4.1 Tokens, in-LLM | budget-dependent (e.g. 75% at layer 28) | −54.9% (NeXT) | recipe search ≈5 min; throughput +22.2% at 50% pruning | — | A100 | A |
| SparseVLM ★ | 2410.04417 | 4.4.1 Tokens, in-LLM | 576→192 (66.7%) | −62.8% | CUDA time −43.1%; latency −37.0% | cache 302.4→100.8 MB (−67%) | A100 | A |
| AutoSelect | 2603.07135 | 4.4.1 Tokens, learned gate | 88.9% pruned | — | prefill 2.85×; TTFT 72.73 ms; 0.69 ms selection overhead | — | A6000 | B |
| VisionSelector | 2510.16598 | 4.4.1 Tokens, learned selector | 20% kept (down to 5%) | — | prefill 1.73–1.86× (760.82 ms); end-to-end 1.74× (924.57 ms); 2× at 5% | peak 17.57 GB (−32.3%) | A800 | A |
| InternVideo2.5 | 2501.12386 | 4.4.1 Tokens, video | 64–512 frames, 16 tokens/frame | — | — | — | A100 | C |
| VideoChat-Flash | 2501.00574 | 4.4.1 Tokens, video hierarchical | 196→16 tokens/frame | LLM only: 14.8 T (64 frames) to 9,969.5 T (10,000 frames) | 2.6→1.9 s with visual dropout | — | A100 | A |
| LongVU | 2410.17434 | 4.4.1 Tokens, video spatiotemporal | 144→64→~2 tokens/frame (1 fps, 1 h) | — | — | — | H100 | C |
| FastVLM ★ | 2412.13303 | 4.4.2 Prefill (encoder bottleneck) | fewer encoder output tokens | — | TTFT 85× (vs OneVision 1152²); 3.2× vs SigLIP | — | H100 | A |
| TopV | 2503.18278 | 4.4.2 Prefill optimization | 50% (LLaVA) / 70% (InternVL2) | visual FLOPs −35% / −47% | 1.08–1.23× vs base; 1.68–2.1× vs FastV; 2 ms optimization | dynamic memory −49% / −61% vs FastV | A100, A6000 | B |
| JanusVLN | 2509.22548 | 4.4.3 Cache memory (navigation) | — | — | 82–244 ms (cache) vs 268–1549 ms (VGGT) | — | n/s | B |
| LOOK-M ★ | 2406.18139 | 4.4.3 KV cache | KV budget 20% / 5% | — | decoding 28.16→20.98→18.22 ms/token (1.3–1.5×) | 1.52→0.32→0.13 GiB (−80–95%) | A100, RTX 3090 | A |
| Edge–cloud SD + EE | 2505.21594 | 4.4.4 Decoding (edge–cloud speculative + early exit) | — | — | latency −35% (+11%); 1.34× on Jetson | — | Jetson Nano/Orin, A100, RTX 2080 Ti, Unitree Go2 | B |
| Mirage | 2506.17218 | Latent visual tokens (reasoning, boundary) | — | — | training ≈3.5 h (stage 1) and ≈7.2 h (stage 2) vs 5.5 h for text-only CoT SFT | — | H100 | A |
| TDA | 2403.18293 | Test-time adaptation (CLIP, boundary) | — | — | test time 12 h 50 min→16 min vs TPT (ImageNet) | — | RTX 6000 | B |

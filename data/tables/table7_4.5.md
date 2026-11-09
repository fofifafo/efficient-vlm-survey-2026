**Table 7.** Deployment: cost quantities reported by the authors of the 9 selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).

| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |
|---|---|---|---|---|---|---|---|---|
| MiniCPM-o 4.5 ★ | 2604.27393 | 4.5.1 Consumer GPU / edge (omni, real time) | INT4 | — | 212.3 tok/s (INT4); TTFT 0.58 s; RTF 0.21 | 11 GB (INT4) / 19 GB (BF16) | RTX 4090, DGX Spark | A |
| MiniCPM-V ★ | 2408.01800 | 4.5.1 Smartphone | 4-bit | — | encoding 64.2→50.5→17.0 s; decoding 1.3→3.2→8.2 tok/s | — | Xiaomi 14 Pro (Snapdragon 8 Gen 3), CPU, RTX 4090 | A |
| SPEED-Q ★ | 2511.08914 | 4.5.1 Smartphone (low-bit) | 2/4-bit | — | — | file 1789→315 MB; footprint 1855→388 MB | Galaxy S25 Ultra | A |
| BlueLM-V-3B | 2411.10640 | 4.5.1 Smartphone NPU (co-design) | INT4/INT8 | — | 24.4 tok/s; 2.1 s encoding at 768×1536; 200 ms latency hidden | peak 2.2 GB | MediaTek Dimensity 9300 NPU | B |
| Eve | 2501.04322 | 4.5.2 Edge (elastic experts) | 1.8B | — | training 15 GPU-days | — | Ascend AI | A |
| Edge–cloud traffic monitoring | 2509.21259 | 4.5.3 Edge–cloud (semantic communication) | 8-bit embedding transfer | — | RoI 0.023 s + ViT 0.16 s per frame | VRAM 14.2 GB (LLaVA) / 24 GB (LLaMA) | n/s (edge device) | B |
| EdgeVLA | 2507.14049 | 4.5.5 VLA on-board | 1B (vs 7.5B) | — | 5 vs 20 ms for OpenVLA (A100) | 4 vs 16 GB for OpenVLA (A100) | A100, Jetson Nano (mentioned) | A |
| NanoVLA | 2510.25122 | 4.5.5 VLA on-board (Jetson Orin Nano) | parameters −98% | — | up to 52× on edge (FPS vs 4-bit OpenVLA) | — | Jetson Orin Nano Super (67 TOPS) | B |
| Jetson-PI ★ | 2607.12659 | 4.5.5 VLA on-board (system) | — | — | reaction time 2.11× / 1.87× (Orin/Thor); graph reuse 2.96×; 5.41× control rate vs vla.cpp (893 ms) | — | Jetson Orin, Jetson Thor, RTX 4090, A6000 | A |

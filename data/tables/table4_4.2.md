**Table 4.** Training-time efficiency: cost quantities reported by the authors of the 11 selected entries, as measured on their own systems (★ representative; grade A = public code and a measured time or memory cost, B = measured cost without public code, C = no measured cost; FLOPs alone do not count; n/s = not stated).

| Method | arXiv | Sub-branch | Reduction / setting | FLOPs | Time | Memory | Hardware | Grade |
|---|---|---|---|---|---|---|---|---|
| CLIP-LoRA | 2405.18541 | 4.2.1 LoRA (CLIP few-shot) | — | — | training 50 min vs 2 h for CoOp (16-shot ImageNet) | — | A100 | A |
| DoRA ★ | 2402.09353 | 4.2.1 LoRA variant | same parameters as LoRA | — | — | training memory −24.4% (LLaMA) / −12.4% (VL-BART) | n/s | A |
| MoSLoRA | 2406.11909 | 4.2.1 LoRA variant | — | — | training 8.2 h (LLaMA-3 8B, commonsense) | GPU memory 31 GB | A100 | A |
| KRAdapter | 2508.00230 | 4.2.1 PEFT (Khatri–Rao) | — | — | training per epoch 16.5 min (ViT-B/32), 137.5 min (ViT-L/14), 220.1 min (ViT-H/14); 247.6 min (LLaMA3-8B) | — | n/s | B |
| VLA-GSE | 2605.06175 | 4.2.1 PEFT (VLA general/specialist experts) | 114.04M trainable (2.51%) | — | action-chunk latency at batch 1, mean of 120 runs (values only in a figure of the paper) | — | A100, RTX 5080 | A |
| InternLM-XComposer2 | 2401.16420 | 4.2.1 Partial LoRA (model report) | — | — | — | — | n/s | C |
| BiomedCoOp | 2411.15232 | 4.2.2 Prompt learning (biomedical) | — | — | — | — | A100 | C |
| KDPL | 2407.03056 | 4.2.2 Prompt learning (unsupervised distillation) | — | 18/14 GFLOPs (light) vs 381 (ViT-H) | — | — | n/s | C |
| MiniGPT-3D ★ | 2405.01413 | 4.2.3 PEFT for 3D alignment | 47.8M trainable parameters | — | 26.8 h on RTX 3090 (6× vs 8×A800) | — | RTX 3090 | A |
| ThinkLite-VL | 2504.07934 | 4.2.4 Data efficiency (MCTS sample selection) | — | — | — | — | A100 | C |
| Rank-1 Expert Pool ★ | 2601.22828 | 4.2.5 Continual-learning PEFT | trainable parameters −96.7% | — | — | peak GPU memory −66.7% | A6000 | A |

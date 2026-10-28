# 비교 매트릭스 근거 — 4.1R (10편)


## 2403.14520 [keep] Cobra: Extending Mamba to Multi-Modal Large Language Model for Efficient Inference

- 기반 모델: BLIP-2, IDEFICS, LLaVA, Qwen-VL
- 비교 대상: —
- 하드웨어: NVIDIA A100, Nvidia A100
- 벤치마크: GQA, POPE, RefCOCO, RefCOCOg, TextVQA, VizWiz

**PARAM** (2)
- Even compared to the much larger LLaVA v1.5 model with 7 billion parameters, Cobra still performs com- parably on several specific benchmarks with about 48% of the parameters.
- It is noteworthy that Cobra-3.5B, with only 48% of the total parameters of LLaVA v1.5-7B, achieves comparable results on open-ended VQA benchmarks and shows signif- icant improvements in the challenging closed-set prediction tasks of VSR and POPE.

**SPEED** (2)
- Exper- iments across various multi-modal benchmarks demonstrate that: (i) Cobra performs 3× ∼4× faster than the most com- putationally efficient state-of-the-art methods, e.g., LLaVA- Phi and MobileVLM v2.
- In Figure 1 (c), Cobra performs 3× ∼4× faster than MobileVLM v2-3B.

**ACC** (1)
- On other benchmarks, the differences were not significant with accuracy gaps within 1%.


## 2405.11273 [keep] Uni-MoE: Scaling Unified Multimodal LLMs with Mixture of Experts

- 기반 모델: BLIP-2, IDEFICS, LLaVA, LLaVA-1.5, Qwen-VL, llava
- 비교 대상: —
- 하드웨어: A100, A800
- 벤치마크: ActivityNet, MMBench, MSVD, POPE, SEED-Bench, VQAv2

**PARAM** (1)
- Portions of this table are reported by the MoE-LLaVA model [20]. ”Width” represents the dimension of the hidden states. ”FFN” denotes the dimension of the feed-forward network’s intermediate layer. ”FFN Factor” represents the quantity of linear layers in the FFN. ”Activated” or ”Total Param” refers to the activated or 


## 2408.15881 [keep] LLaVA-MoD: Making LLaVA Tiny via MoE Knowledge Distillation

- 기반 모델: BLIP-2, LLAVA, LLaVA, LLaVA-1.5, LLaVA-NeXT, Mini-Gemini, MiniCPM-V, Qwen-VL
- 비교 대상: —
- 하드웨어: H800
- 벤치마크: GQA, MMBench, MME, POPE, ScienceQA, TextVQA, VizWiz

**PARAM** (8)
- Remarkably, LLaVA-MoD-2B surpasses Qwen-VL-Chat-7B with an aver- age gain of 8.8%, using merely 0.3% of the training data and 23% trainable param- eters.
- Knowledge Distillation (KD) from large-scale MLLM (l-MLLM) offers a promising yet unexplored strategy for enhancing ∗Equal Contribution †Core Members ‡Corresponding Authors 1 arXiv:2408.15881v3 [cs.CV] 23 Oct 2024 Technical Report < 0.3% data usage < 23% trainable params < 0.25% data usage GPU Hours Diameter 69.2 68.9 
- As illustrated in Figure 1, LLaVA-MoD-2B exceeds Qwen-VL-Chat-7B by an average of 8.8% on these benchmarks, utilizing just 0.3% of the training data and 23% trainable parameters.
- Furthermore, it matches the perfor- 1MoD denotes Mixture-of-Expert Knowledge Distillation for MLLMs 2 Technical Report mance of RLHF-based methods with 7B and 13B parameters on several hallucination benchmarks.
- Specifically, l-MLLM is configured with 7B parameters, while s-MLLM is config- ured with 1.8B and 0.5B parameters.


## 2412.10302 [keep] DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding

- 기반 모델: InternVL2, LLaVA, MiniCPM-V, Qwen2-VL, llava
- 비교 대상: —
- 하드웨어: NVIDIA A100
- 벤치마크: AI2D, ChartQA, DocVQA, MMBench, MME, MMMU, MathVista, OCRBench, RealWorldQA, RefCOCO, RefCOCOg, TextVQA

**PARAM** (1)
- Conclusion In this technical report, we introduce DeepSeek-VL2, an enhanced version of MoE-based Vision- Language Models, available in scales of 3B, 16B, and 27B parameters in total, with corresponding activated parameters of 1.0B, 2.8B, and 4.5B.

**MEM** (1)
- Notably, our 3B, 16B and 27B models can be deployed on a single GPU with 10 GB, 40GB and 80GB memory respectively.


## 2502.13145 [keep] Multimodal Mamba: Decoder-only Multimodal State Space Model via Quadratic to Linear Distillation

- 기반 모델: InternVL, LLaVA, Qwen-VL
- 비교 대상: —
- 하드웨어: NVIDIA 4090, NVIDIA A800, NVIDIA RTX 4090
- 벤치마크: GQA, MMBench, MME, MMMU, POPE, ScienceQA, TextVQA

**SPEED** (6)
- At 103K tokens, mmMamba-linear demonstrates 20.6× speedup compared to HoVLE and saves 75.8% GPU memory, while mmMamba-hybrid achieves 13.5× speedup and saves 60.2% GPU memory.
- At 103K tokens, mmMamba-linear demonstrates 20.6× speedup and 75.8% GPU memory reduction compared to HoVLE, while mmMamba-hybrid achieves 13.5× speedup and 60.2% memory sav- ings.
- Notably, at the context length of 103K tokens, mmMamba-linear demonstrates 20.6× speedup compared to HoVLE and saves 75.8% GPU mem- ory, while mmMamba-hybrid achieves 13.5× speedup and saves 60.2% GPU memory.
- Thanks to the fixed hidden state rooted in linear-complexity modeling, mmMamba-linear/hybrid achieve nearly 4× faster inference speed than all the Transformer-based VLMs. mmMamba-linear/hybrid also outperforms the linear complexity encoder-based VLMs (Cobra-3.5B and VisualRWKV-3B) by a large margin (about 30 tokens/s a
- Specifically, at the 103K token length, mmMamba-linear demonstrates 20.6× speedup compared to HoVLE and saves 75.8% GPU mem- ory, while mmMamba-hybrid achieves 13.5× speedup and saves 60.2% GPU memory.

**THR** (1)
- Thanks to the fixed hidden state rooted in linear-complexity modeling, mmMamba-linear/hybrid achieve nearly 4× faster inference speed than all the Transformer-based VLMs. mmMamba-linear/hybrid also outperforms the linear complexity encoder-based VLMs (Cobra-3.5B and VisualRWKV-3B) by a large margin (about 30 tokens/s a


## 2504.07491 [keep] Kimi-VL Technical Report

- 기반 모델: Gemma3, LLaVA-OneVision, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: ascending a 
- 벤치마크: AI2D, EgoSchema, LongVideoBench, MLVU, MMBench, MME, MMMU, MathVista, OCRBench, RealWorldQA, Video-MME

**TOK** (1)
- For data composition, we filter and upsample the ratio of long data to 25% in each sub-stage, while using the remaining 75% tokens to replay shorter data in its previous stage; our exploration confirms that this composition allows the model to effectively learn long-context understanding while maintaining short-context

**PARAM** (1)
- arXiv:2504.07491v3 [cs.CV] 23 Jun 2025 KIMI-VL TECHNICAL REPORT Kimi Team ABSTRACT We present Kimi-VL, an efficient open-source Mixture-of-Experts (MoE) vision-language model (VLM) that offers advanced multimodal reasoning, long-context understanding, and strong agent capabilities—all while activating only 2.8B paramet


## 2509.18154 [star] MiniCPM-V 4.5: Cooking Efficient MLLMs via Architecture, Data, and Training Recipe

- 기반 모델: InternVL3, LLaVA, MiniCPM-V, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: A100
- 벤치마크: AI2D, ChartQA, DocVQA, LongVideoBench, MLVU, MMBench, MME, MMMU, MathVista, OCRBench, RealWorldQA, TextVQA, Video-MME, VideoMME

**PARAM** (2)
- To address the challenges, we present MiniCPM-V 4.5, an 8B parameter model designed for high efficiency and strong performance.
- With only 8B parameters, it surpasses widely 10 Model Size Avg Score ↑ Time ↓ GLM-4.1V-9B-thinking 10.3B 76.6 17.5h MiMo-VL-7B-RL 8.3B 76.4 11.0h MiniCPM-V 4.5 8.7B 77.0 7.5h (a) OpenCompass results of thinking models Model Size Score ↑ Time ↓ Mem ↓ Qwen2.5-VL-7B 8.3B 71.6 3.00h 60G GLM-4.1V-9B-thinking 10.3B 73.6 2.63

**SPEED** (1)
- This module can encode a 6-second, 2-fps, 448×448 resolution video into only 128 visual tokens, achieving a 12×-24× reduction in to- ken cost compared to representative MLLMs [7, 9], enabling efficient high frame rate and long video understanding, and unified encoding for images as well. (2) Unified Learning Paradigm f

**MEM** (1)
- For example, on the widely adopted VideoMME benchmark, MiniCPM-V 4.5 achieves state-of-the-art per- formance among models under 30B size, using just 46.7% GPU memory cost and 8.7% inference time of Qwen2.5-VL 7B.


## 2601.13020 [keep] PASs-MoE: Mitigating Misaligned Co-drift among Router and Experts via Pathway Activation Subspaces for Continual Learning

- 기반 모델: LLaVA
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —


## 2604.02710 [keep] V2X-QA: A Comprehensive Reasoning Dataset and Benchmark for Multimodal Large Language Models in Autonomous Driving Across Ego, Infrastructure, and Cooperative Views

- 기반 모델: —
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**BIT** (1)
- The implementation uses 4-bit NF4 quantization with bfloat16 computation and FlashAttention-2 for efficient training and inference.


## 2608.17402 [keep] MoE-ViE: Mixture of Experts Vision Encoder for Efficient Image and Video Understanding

- 기반 모델: InternVL
- 비교 대상: —
- 하드웨어: CPU, H100
- 벤치마크: AI2D, ChartQA, DocVQA, EgoSchema, MVBench, TextVQA, VideoMME

**SPEED** (2)
- Our largest encoder achieves results comparable to the SOTA dense encoder PEcoreG, which is 1.7× larger. – Our MoE kernel provides > 2.5× speedup in inference latency.
- As shown in Table 7, the MoE kernel provides > 2.5× speedup across different batch sizes compared to the vanilla implementation.

**FLOP** (1)
- 109 1010 1011 1012 1013 GFLOPs 100 ImageNet 1K Error ViT-B/32 dense ViT-B/16 dense ViT-L/14 dense ViT-B/32 MoE ViT-B/16 MoE ViT-L/14 MoE Fig.

**LAT** (1)
- Activated Parameters Total Parameters Latency (ms) Model bsz =16 32 64 128 SigLIP2-g-opt/16 [75] 1.1B 1.1B 76.39 141.78 275.94 549.62 PEcoreG/14 [5] 1.9B 1.9B 101.21 188.76 366.23 708.62 MoE-ViE-H/14 (Vanilla Implementation) 1.1B 3.5B 318.76 448.93 740.84 1306.81 MoE-ViE-H/14 (Optimized Kernel) 1.1B 3.5B 82.59 145.82 2

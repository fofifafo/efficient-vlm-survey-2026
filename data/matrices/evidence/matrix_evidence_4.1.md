# 비교 매트릭스 근거 — 4.1 (15편)


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


## 2409.07267 [keep] MiniDrive: More Efficient Vision-Language Models with Multi-Level 2D Features as Text Tokens for Autonomous Driving

- 기반 모델: BLIP-2, Llava, Qwen-VL
- 비교 대상: —
- 하드웨어: RTX 4090
- 벤치마크: —

**PARAM** (4)
- Compared to previous works, MiniDrive achieves state- of-the-art performance in terms of parameter size, floating point operations, and response ef- ficiency, with the smallest version containing only 83M parameters.
- For instance, MiniDrive224 has only 83M parameters and a FLOP count of merely 5.9B, which is signifi- cantly lower than current visual-language models used in autonomous driving.
- In Figure 1(c), MiniDrive outperforms open-source models with 7B parameters and above on the single-image evaluation system CODA-LM (Li et al., 2024), approaching the performance of closed-source commercial models.
- It is evident that despite MiniDrive having only 83M parameters, it demon- strates superior performance, outperforming open- source models and approaching the performance of closed-source models.

**MEM** (2)
- It can be fully trained with multiple instances on a single RTX 4090 GPU with 24GB of memory.
- The training cost of the model is reduced, and multiple MiniDrive models can be fully trained simultaneously on an RTX 4090 GPU with 24GB of memory. • MinDrive is attempting for the first time to utilize a large convolutional kernel architec- ture as the vision encoder backbone for au- tonomous driving vision-language 


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


## 2505.21594 [keep] Fast and Cost-effective Speculative Edge-Cloud Decoding with Early Exits

- 기반 모델: Qwen2-VL
- 비교 대상: —
- 하드웨어: A100, CPU, Jetson, Jetson Nano, Jetson Nano is ideal , Jetson Orin, Jetson Orin board , Jetson RTX Drafting , Jetson RTX Jetson RTX, Jetson RTX MT, Jetson has a high c , NVIDIA A100, NVIDIA Jetson Nano, NVIDIA Jetson Nano , NVIDIA Jetson Orin, NVIDIA Jetson Orin board, RTX 2080
- 벤치마크: —

**PARAM** (1)
- For instance, the Unitree Go2 is powered by a Jetson Orin board with 16GB of unified memory, which is insufficient to run models over 10B parameters that require over 40GB of memory.

**SPEED** (6)
- Using an NVIDIA Jetson Nano (client) and an A100 GPU (server) with Vicuna-68M (draft) and Llama2-7B (target) models, our method achieves up to a 35% reduction in latency compared to cloud-based autoregressive decoding, with an additional 11% improvement from preemptive drafting.
- With Vicuna- 68M as the draft model and Llama2-7B as the target model, we show an average 35% latency reduction from autoregressive to vanilla edge cloud speculative decoding and a further speedup of 11% with our fast decoding method. • We demonstrate our approach on a real-world robotics platform (Unitree Go2 equipped
- AR →SD: On average, using RTX, vanilla SD achieves a 1.2x and 1.94x speedup over autoregressive decoding with the Vicuna-68M/Vicuna-7B and Vicuna-68M/Llama2-7B models, respectively.
- Jetson, being slower at drafting coupled with higher communication cost, reduces the speedup relative to autoregressive decoding, making it slower for Vicuna-68M/Vicuna-7B and Vicuna-160M/Vicuna-13B models, though it achieves a 1.34x speedup with Vicuna-68M/Llama2-7B.
- In contrast, for Vicuna-68M/Llama2-7B, a lower c combined with a higher τ yields a 1.35x speedup.

**FLOP** (1)
- With a performance of up to 472 GFLOPs, the Jetson Nano is ideal for edge applications.

**LAT** (3)
- Method Latency Cloud AR 2Tc + nTq Edge-Cloud SD n τ (2Tc + γTp + Tq) Edge-Cloud FSD n τ (2Tc + rγTp + (1 −r)Tr + Tq) Latency Calculation: Table 3 summarizes the notations used in our analysis.
- Metric Vicuna-68m/Vicuna-7B Vicuna-160m/Vicuna-13B Vicuna-68m/Llama2-7B Jetson RTX Jetson RTX Jetson RTX Drafting Latency (γTp, γ = 4) 334ms 102ms 1596ms 555ms 301ms 99ms Verification Latency (Tq) 497ms 442ms 616ms 618ms 522ms 467ms Latency Ratio (c = Tp/Tq) 0.17 0.06 0.65 0.22 0.14 0.05 Communication Latency (Tc) 95ms
- Metric Value Drafting Latency (γTp, γ = 4) 288ms Verification Latency (Tq) 620ms Latency Ratio (c = Tp/Tq) 0.11 Communication Latency (Tc) 120ms Max GPU Memory 12.4G Num EE Threads 6 (a) System and latency metrics Metric Value Avg Tokens (τ) (↑) 2.92 Cache Miss Rate (↓) 55.63 Avg EE (↓) 8 Speedup AR →SD (↑) 0.90x Speed

**MEM** (7)
- For instance, the Unitree Go2 is powered by a Jetson Orin board with 16GB of unified memory, which is insufficient to run models over 10B parameters that require over 40GB of memory.
- For language generation models, we train early exit adapters on the publicly available ShareGPT conversation dataset (hf:RyokoAI/ShareGPT52K) using a single NVIDIA A100 GPU with 80GB of VRAM.
- Server Side Hardware: We utilize a high performance computing cluster node equipped with a single A100 GPU with 80GB VRAM, 16 CPU cores, and 8GB of CPU memory per core as our server.
- Cluster Node with RTX 2080 Ti: This setup features a single RTX 2080 Ti GPU with 12GB VRAM, an 8-core CPU, and 4GB of RAM per core, providing a more powerful alternative for our experiments.
- On the RTX-equipped node, the system handles up to 30 threads for the Vicuna-68M model, but GPU VRAM (12 GB) limits the Vicuna-160M model to 15 threads before encountering an out-of-memory (OOM) error.


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


## 2510.01795 [keep] Nav-EE: Navigation-Guided Early Exiting for Efficient Vision-Language Models in Autonomous Driving

- 기반 모델: LLAVA, LLaVA
- 비교 대상: —
- 하드웨어: RTX 3090
- 벤치마크: —

**FREE** (2)
- Closest to our setting, retrieval-augmented early- exiting (RAEE) shows that instance-wise priors can guide exit-layer selection without re-training the backbone [16].
- Offline Profiling: Aggressive Statistical Layer Selection To enable reliable early-exit without retraining, we adopt an offline profiling strategy based on large-scale training data.

**SPEED** (1)
- These findings demonstrate that Nav-EE can be effectively deployed in real-vehicle settings, offering significant effi- ciency gains (up to nearly 50% reduction in latency) without compromising task performance.

**LAT** (7)
- Real-vehicle integration with Autoware Universe further demonstrates reduced inference latency (600 ms to 300 ms), supporting faster decision-making in complex scenarios.
- For example, DS-Tiny improves from 71.29% to 95.80% accuracy while reducing latency from 0.098s to 0.084s.
- Similarly, DS-Small increases ac- curacy from 52.01% to 77.55% with latency reduced from 0.248s to 0.186s.
- The largest improvement is observed with LLaVA-7B, which rises from 52.10% to 76.93% accuracy while cutting inference latency from 0.030s to 0.025s.
- For the decision- critical traffic-light recognition task, Nav-EE improves ac- curacy from 52.10% to 76.93% while reducing latency from 0.030s to 0.025s.

**ACC** (1)
- For example, pedestrian recognition improves slightly from 66.93% to 67.11%, while traffic-light accuracy decreases from 52.10% to 37.68%.


## 2601.13020 [keep] PASs-MoE: Mitigating Misaligned Co-drift among Router and Experts via Pathway Activation Subspaces for Continual Learning

- 기반 모델: LLaVA
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —


## 2602.24059 [keep] Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization

- 기반 모델: InternVL2
- 비교 대상: —
- 하드웨어: A800, RTX 4090
- 벤치마크: AI2D, ChartQA, DocVQA, MMMU, OCRBench, ScienceQA, TextVQA, VizWiz

**FREE** (1)
- Among existing approaches, Post-Training Quantization (PTQ) is widely adopted for its efficiency and compatibility without retraining the full model.

**BIT** (8)
- It employs a fixed shared expert to compensate global quantization er- rors while dynamically selecting routed experts to correct token-dependent local errors. • Extensive experiments across various quantization set- tings and multimodal benchmarks demonstrate that QE effectively mitigates low-bit performance degradati
- For weight-activation quantization, QE is evaluated under W4A6 and W4A8 settings against round-to-nearest (RTN), channel-scaling SmoothQuant (SQ) [44], modality-balanced MBQ [23], and low-rank reconstruction LQER [48].
- For weight- only quantization, we adopt AWQ [24] as the channel- scaling baseline under the W3A16 configuration, apply- ing group-wise asymmetric quantization with 128 group size.
- In the challeng- ing W4A6 setting, it improves Qwen2VL-2B accuracy by 4.01% over MBQ, with only a 4.23% drop from full pre- cision, and gains 3.13% on InternVL2-2B.
- At W4A8, the performance gap to full precision narrows to within 2%, demonstrating strong robustness.

**PARAM** (1)
- Extensive experiments demonstrate that QE consis- tently enhances task accuracy across various quantization settings and model scales, ranging from 2B to 70B param- eters, while maintaining performance comparable to full- precision models.

**ACC** (2)
- It employs a fixed shared expert to compensate global quantization er- rors while dynamically selecting routed experts to correct token-dependent local errors. • Extensive experiments across various quantization set- tings and multimodal benchmarks demonstrate that QE effectively mitigates low-bit performance degradati
- At W4A8, the performance gap to full precision narrows to within 2%, demonstrating strong robustness.


## 2603.20492 [keep] AE-LLM: Adaptive Efficiency Optimization for Large Language Models

- 기반 모델: InternVL, LLaVA-1.5
- 비교 대상: —
- 하드웨어: A100, RTX 4090
- 벤치마크: GQA, TextVQA, VQAv2

**BIT** (6)
- Stage Category Sample Options / Parameters Architecture (Carch) Attention Type {MHA, MQA, GQA, MLA} MoE Config {Dense, Sparse-MoE (2/4/8 experts), Top-1/Top-2 rout- ing} Fine-Tuning (Cft) Method {Full, LoRA, QLoRA, DoRA, RSLoRA} Rank & Alpha Rank r ∈{8, 16, 32, 64, 128}, Alpha α ∈{r, 2r, 4r} Inference (Cinf) Quantizati
- Hardware-Dependent Patterns: On memory-constrained hardware (RTX 4090), int4 quanti- zation is almost universally selected, combined with MQA attention for minimal memory footprint.
- Quantization: Int4 quantization achieves the largest efficiency gains (up to 4×) but also shows higher variance in accuracy degradation.
- 11 23 24 25 26 27 28 LoRA Rank 40 50 60 70 80 Accuracy (%) Small (1B) Medium (7B) Large (70B) FP16 INT8 INT4 INT2 Precision (bits) 20 30 40 50 60 70 Accuracy (%) MMLU GSM8K HumanEval 0 5 10 15 20 25 30 Number of Experts 35 40 45 50 55 60 65 70 Accuracy (%) / Latency (ms) Accuracy Latency Memory 2 1 20 21 22 23 Alpha / 
- Quantization Bits: Accuracy degrades gracefully from FP16 to INT8, with a steeper drop from INT8 to INT4.

**PARAM** (2)
- Ex- tensive experiments across 15 models (0.5B-70B parameters) and 10 diverse tasks demonstrate that AE-LLM achieves an average of 2.8× improvement in efficiency metrics while maintaining competitive accuracy (within 1.2% of baseline), compared to static efficiency configurations.
- We conduct extensive experiments across 15 models (0.5B-70B parameters) and 10 diverse tasks, demonstrating that AE-LLM achieves significant efficiency im- provements (average 2.8× across multiple metrics) while maintaining competitive accuracy (within 1.2% of baseline).

**ACC** (3)
- Ex- tensive experiments across 15 models (0.5B-70B parameters) and 10 diverse tasks demonstrate that AE-LLM achieves an average of 2.8× improvement in efficiency metrics while maintaining competitive accuracy (within 1.2% of baseline), compared to static efficiency configurations.
- We conduct extensive experiments across 15 models (0.5B-70B parameters) and 10 diverse tasks, demonstrating that AE-LLM achieves significant efficiency im- provements (average 2.8× across multiple metrics) while maintaining competitive accuracy (within 1.2% of baseline).
- On average, AE-LLM configurations achieve accuracy within 1.2% of the default configuration, with some configurations even improving accuracy (e.g., +0.3% on MMLU for LLaMA-2-70B through optimal MoE configuration).


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

# 4.4 신규 2편
## 2503.10501 [keep] TokenCarve: Information-Preserving Visual Token Compression in Multimodal Large Language Models

- 기반 모델: LLaVA, LLaVA-1.5
- 비교 대상: FastV, LLaVA-Mini, MustDrop, SparseVLM, ToMe, VisionZip, fastV
- 하드웨어: V100
- 벤치마크: MMBench, MME, POPE, TextVQA, VQAV2, VizWiz

**FREE** (8)
- Existing training- based token compression methods improve inference ef- ficiency but require costly retraining, while training-free methods struggle to maintain performance when aggres- sively reducing token counts.
- Based on this finding, we propose TokenCarve, a training-free, plug- and-play, two-stage token compression framework.
- Existing compression approaches for MLLMs can be broadly categorized into two types: training-based methods [15, 17, 42], which rely on end-to-end learned compressors (e.g., query modules or Gumbel-softmax pre- dictors) and thus require costly retraining and model- specific adaptation; and training-free methods, which 
- While these training-free methods can effectively compress tokens, their performance generally becomes difficult to maintain when the token count is significantly reduced.
- In this study, we adopt a novel information-preservation perspective to investigate and design a training-free ap- proach that sustains strong performance even under sub- stantial token compression.

**SPEED** (2)
- It can even reduce the number of visual tokens to 22.2% of the original count, achieving a 1.23× speedup in inference, a 64% reduction in KV cache storage, and only a 1.54% drop in accuracy.
- Specifically, decreasing the visual token count from 576 to 128 reduces inference latency from 1.124 s to 0.911 s, achieving a 1.23× speedup, while KV cache usage drops from 100% to 36%.

**LAT** (1)
- Specifically, decreasing the visual token count from 576 to 128 reduces inference latency from 1.124 s to 0.911 s, achieving a 1.23× speedup, while KV cache usage drops from 100% to 36%.

**MEM** (7)
- It can even reduce the number of visual tokens to 22.2% of the original count, achieving a 1.23× speedup in inference, a 64% reduction in KV cache storage, and only a 1.54% drop in accuracy.
- Concurrently, the inference speed is en- hanced by a factor of 1.23, and the KV cache storage is re- duced by 64%, leading to significant reductions in latency and improved storage efficiency.
- Specifically, TokenCarve effectively reduces the visual token count to 22.2% of the original, achieving a 1.23× improvement in inference speed, a 64% reduction in KV cache storage, and only a 1.54% drop in accuracy.
- Specifically, decreasing the visual token count from 576 to 128 reduces inference latency from 1.124 s to 0.911 s, achieving a 1.23× speedup, while KV cache usage drops from 100% to 36%.
- Further compressing the visual token count to 64 results in a performance drop of 1.2, while KV cache us- age is reduced to 26.9%, achieving an even greater acceler- ation of 1.33×.

**ACC** (2)
- The results indicate that TokenCarve remains robust across differ- ent values of ρ, with performance variations staying within 1.5%. using LLaVA-1.5-7B as the base model and MME as the dataset.
- As the merge proportion increases, model performance remains within a 1.5% variation across all three visual token count configura- tions.


## 2510.16598 [keep] VisionSelector: End-to-End Learnable Visual Token Compression for Efficient Multimodal LLMs

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-OneVision, Qwen2.5-VL
- 비교 대상: DivPrune, Dynamic-LLaVA, FastV, PruMerge, VisionZip
- 하드웨어: A800, NVIDIA A800
- 벤치마크: AI2D, ChartQA, DocVQA, MME, MMMU, MVBench, OCRBench, POPE, SEED-Bench, SEEDBench, ScienceQA, TextVQA, VideoMME

**FREE** (8)
- To address these limitations, we reformulate token compression as a lightweight plug-and-play framework and turn it into an end-to-end learnable decision process.
- Our ap- proach, VisionSelector, addresses the limitations of prior methods by introducing a lightweight, plug-and-play framework that seam- lessly integrates with existing vision-language models and supports adaptive compression.
- The contributions of this paper could be summarized as: • We propose VisionSelector, a novel framework that refor- mulates visual token compression from heuristic-based post- processing to an end-to-end learnable decision process, opti- mized directly by downstream losses. • We design a lightweight, plug-and-play, and 
- 2 Related Work Training-free Token Compression Methods.
- 3.1 Overall Framework Our method, VisionSelector, is designed as a plug-and-play solu- tion for seamless integration into advanced MLLMs.

**TOK** (1)
- VisionSelector is optimal across all ratios, achieving a 2× prefill speedup with only 5% tokens. (c) DocVQA with a 20% token budget: comparison of performance, GPU memory, and speedup.

**BIT** (3)
- Dynamic- LLaVA [21] learns an image predictor for binary keep-or-drop token decisions, while LightVLA [24] follows a Straight-Through Estima- tion (STE) [8] style pruning paradigm to optimize discrete token selection.
- At inference time, we apply the standard Top-K operator directly to the score vector to obtain a hard binary mask that selects the top 𝑘tokens.
- We then penalize the discrepancy between Msoft and Mhard using a binary cross-entropy (BCE) loss: 𝐿constraint = BCE(Msoft, Mhard) . (11) VisionSelector: End-to-End Learnable Visual Token Compression for Efficient Multimodal LLMs MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil.

**PARAM** (3)
- Remarkably lightweight with only 12.85M trainable parameters, VisionSelector demonstrates generalization across various compression rates and adaptively identifies critical tokens.
- The contributions of this paper could be summarized as: • We propose VisionSelector, a novel framework that refor- mulates visual token compression from heuristic-based post- processing to an end-to-end learnable decision process, opti- mized directly by downstream losses. • We design a lightweight, plug-and-play, and 
- The selector is trained with a fixed 20% retention budget and contains 16.87M trainable parameters.

**SPEED** (1)
- Vision- Selector’s prefill time is only 760.82 ms and its end-to-end latency is 924.57 ms, achieving 1.86× and 1.74× speedups over the baseline model, respectively.

**LAT** (3)
- Vision- Selector’s prefill time is only 760.82 ms and its end-to-end latency is 924.57 ms, achieving 1.86× and 1.74× speedups over the baseline model, respectively.
- ViT Backbone + Merger 26.55 38.6% 26.42 55.4% LIS (Importance Scorer) — — 0.14 0.3% Token Selection (Top-𝐾) — — 0.09 0.2% LLM Prefill 42.18 61.4% 21.01 44.1% End-to-End Prefill 68.73 100% 47.65 100% Prefill Speedup 1.44× As shown in Table 4, the ViT backbone latency is nearly identical in both configurations (26.55 ms 
- The primary speedup comes from the LLM decoder, whose prefill time drops from 42.18 ms to 21.01 ms (2.01×) due to the shortened prefix.

**MEM** (2)
- At 20% retention, it accelerates the prefill phase by a factor of 1.73× while simultane- ously reducing memory consumption to 86.08%.
- Our method matches DivPrune in memory efficiency by lowering peak memory usage to 17.57 GB, a 32.3% reduction from the baseline model.

**ACC** (3)
- This leads to superior performance across the evaluated compression budgets, evidenced by preserving 100% performance on MME with a 30% retention budget, outperforming representa- tive heuristic baselines by 12.14 percentage points at a 10% reten- tion budget, and doubling prefill speed.
- At a 20% bud- get, VisionSelector retains 94.83% of the full model’s average perfor- mance, exceeding the next-best method by over 8 percentage points; at 10%, the margin remains 9.40 percentage points even when the learnable baseline Dynamic* is included.
- Overall, VisionSelector retains 98.13% of the baseline performance on these video tasks.



# 4.3 신규 10편
## 2403.02781 [keep] PromptKD: Unsupervised Prompt Distillation for Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: A100
- 벤치마크: —


## 2408.05517 [star] SWIFT:A Scalable lightWeight Infrastructure for Fine-Tuning

- 기반 모델: InternVL3, LLaVA, PaliGemma, Qwen-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: A100, CPU
- 벤치마크: —

**BIT** (3)
- By reducing the tensor types to 8-bit or 4-bit, the same model can be loaded with less memory.
- It is even possible to run the model with 1-bit or 1.5- bit precision; this approach is collectively known as quantization.
- The main idea is to convert the low-precision floating-point values of the model into 8-bit or lower fixed-point values.


## 2502.14786 [keep] SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features

- 기반 모델: PaliGemma
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, DocVQA, GQA, RefCOCO, RefCOCOg, ScienceQA, TextVQA, VQAv2

**BIT** (1)
- Unlike CLIP [50], which relies on a contrastive loss, SigLIP creates binary classification problems by combining every image embedding with every text embedding in the mini-batch and trains the embeddings to classify matching and non- matching pairs via logistic regression (sigmoid loss).


## 2502.20321 [keep] UniTok: A Unified Tokenizer for Visual Generation and Understanding

- 기반 모델: LLaVA, Mini-Gemini
- 비교 대상: —
- 하드웨어: —
- 벤치마크: GQA, MME, POPE, TextVQA, VQAv2


## 2503.12067 [keep] A Comprehensive Survey on Knowledge Distillation

- 기반 모델: Gemma3
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**FREE** (1)
- Sun et al. (2024a) suggests logit standardization by setting the temperature as the weighted standard deviation of the logit and performing a plug-and-play Z-score pre-process.


## 2504.07934 [keep] SoTA with Less: MCTS-Guided Sample Selection for Data-Efficient Visual Reasoning Self-Improvement

- 기반 모델: InternVL2.5, LLaVA, LLaVA-Onevision, Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: A100
- 벤치마크: AI2D, MMBench, MMMU, MathVista, ScienceQA


## 2509.23729 [keep] LUQ: Layerwise Ultra-Low Bit Quantization for Multimodal Large Language Models

- 기반 모델: LLaVA, LLaVA-1.5, Qwen-VL
- 비교 대상: —
- 하드웨어: NVIDIA RTX 5000, ascending 
- 벤치마크: ChartQA, DocVQA, GQA, MMBench, MME, MathVista, POPE, TextVQA, VQAv2

**BIT** (8)
- Post-training quantization (PTQ) has successfully compressed language models to as low as 1-bit precision, its effectiveness for multimodal LLMs (MLLMs) remains unex- plored.
- In this paper, we present the first method for ultra-low-bit (<4-bit) quantization of MLLMs.
- Evaluated on LLaVA-1.5 and Qwen- 2.5-VL across 9 VQA benchmarks, LUQ models use 40% and 31% less memory than their 4-bit counterparts while exhibiting less than 10% degradation on MME.
- Recent advances (Malinovskii et al., 2024; Huang et al., 2024a) have pushed the boundaries further, achieving compression to even 1-2 bit-widths.
- To address this gap, we conduct an in-depth study of ultra-low bit (< 4-bit) PTQ for Multimodal LLMs.

**PARAM** (1)
- We note that our work targets weight compression of the LLM backbone, which constitutes >95% of param- eters in typical MLLMs.

**MEM** (4)
- Evaluated on LLaVA-1.5 and Qwen- 2.5-VL across 9 VQA benchmarks, LUQ models use 40% and 31% less memory than their 4-bit counterparts while exhibiting less than 10% degradation on MME.
- For LLaVA-1.5 7B, LUQ achieves comparable VQA accuracy to 4-bit GPTQ/AWQ while reducing memory requirements by 40%.
- All experiments are conducted on a single NVIDIA RTX 5000 GPU with 32GB of VRAM.
- For Qwen 2.5 VL, we create a memory-constrained model with a hardware motivated budget of 2.5 GB, a hypothetical limit for edge devices (having 4 GB RAM), leading to the quantization of the 12 lowest-entropy layers (2.75 avg. bits per parameter).

**ACC** (2)
- This helps LUQ achieve a better compression-performance trade-off. • We demonstrate the role of calibration data composition in ultra-low bit quantization, showing that multimodal calibration improves performance over text-only calibration in the ultra-low bit regime. • We benchmark LUQ on 9 standard VQA benchmarks, sh
- Specifically, the accuracy drop on TextVQA, VQAv2, and GQA is a modest 3.4%, 1.7%, and 3.2%, respectively, compared to 4-bit GPTQ.


## 2602.03782 [keep] QVLA: Not All Channels Are Equal in Vision-Language-Action Model's Quantization

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA A100, NVIDIA Jetson AGX Orin can , NVIDIA RTX 4090, ascending 
- 벤치마크: —

**BIT** (8)
- This process yields a precise, per-channel importance metric that guides a global optimization, which elegantly unifies quantization and pruning (0-bit) into a single, cohesive framework.
- Concur- rently, in industrial practice, module-level mixed precision has emerged as a compromise, such as quantizing vision encoders to 4-bit while preserving language backbones at 8-bit.
- Moreover, our approach naturally unifies quantization and pruning (0-bit) into a single process, enabling fine- grained, per-channel bit allocation.
- Our findings reveal why existing paradigms fail and establish that aligning quantization with the action space is a foundational principle for effective compression in embodied AI. ♠We propose QVLA, a novel channel-wise framework that uniquely uses action-space sensitiv- ity to guide bit allocation, cohesively unifying
- To handle pernicious outliers in weights and activations, another research thrust em- ploys learned rotations or permutations to redistribute value distributions, exemplified by methods like QuaRot (Ashkboos et al., 2024) and SpinQuant (Liu et al., 2024c), enabling robust 4-bit quanti- zation.

**SPEED** (2)
- In the LIBERO, the quantization version of OpenVLA-OFT with our method requires only 29.2% of the original model’s VRAM while main- taining 98.9% of its original performance and achieving a 1.49× speedup.
- In the LIBERO environ- ment, our method on the OpenVLA-OFT requires only 29.2% of the original model’s VRAM while maintaining 98.9% of its original performance and achieving a 1.49× speedup.

**MEM** (5)
- In the LIBERO, the quantization version of OpenVLA-OFT with our method requires only 29.2% of the original model’s VRAM while main- taining 98.9% of its original performance and achieving a 1.49× speedup.
- However, their immense computational and memory demands, which often exceed 14 GB in standard half-precision for a 7B model, present a critical barrier to deployment.
- In the LIBERO environ- ment, our method on the OpenVLA-OFT requires only 29.2% of the original model’s VRAM while maintaining 98.9% of its original performance and achieving a 1.49× speedup.
- The row ④with “prune” and without “uniform-bit” indicates our proposed quantization method with the {0, 2, 4, 8, 16} as candidates during assigning bit to each channel. # Weight Type Quantization Method Spatial Object Goal Long Avg. ↑ Memory (GB) Prune Uniform Bit ① FP Model – – 84.7% 88.4% 79.2% 53.7% 76.5% 15.2 ② INT
- When combined with pruning (from ②{2, 4, 8, 16} to ④{0, 2, 4, 8, 16}), this method fur- ther reduces memory to 7.0 GB while also slightly boosting the average success rate to 76.8%.

**ACC** (3)
- In the LIBERO environ- ment, our method on the OpenVLA-OFT requires only 29.2% of the original model’s VRAM while maintaining 98.9% of its original performance and achieving a 1.49× speedup.
- For instance, under the W4A4 quantization setting for the OpenVLA model, QVLA retains 99.3% of the full-precision performance, incurring a minimal accuracy drop of only 0.5%.
- Similarly, for the OpenVLA-OFT model, QVLA’s performance degradation was minimal at just 0.1% and 0.4%, markedly lower than the 2.0% and 4.5% losses observed with AWQ.


## 2603.21010 [keep] SkinCLIP-VL: Consistency-Aware Vision-Language Learning for Multimodal Skin Cancer Diagnosis

- 기반 모델: InternVL2.5, LLaVA, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: NVIDIA A100
- 벤치마크: —

**MEM** (1)
- By freezing the 300M+ visual backbone and utilizing LoRA, we reduce training memory requirements by 43% compared to full fine- tuning.

**ACC** (2)
- When training data is reduced to 12%, baselines utilizing full fine-tuning (SkinGPT-4) or trained from scratch (EfficientNet) suffer catastrophic performance drops (over 16%).
- In con- trast, SkinCLIP-VL retains 97.6% of its original performance (dropping only 2.6%).


## 2607.12787 [keep] Do We Really Need Multimodal Emotion Language Models Larger Than 1B Parameters?

- 기반 모델: Video-LLaVA, mPLUG-Owl
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**BIT** (1)
- Multi-class emotion recognition relies more on such enumeration than binary sentiment polarity, consistent with the observed accuracy shift.

**PARAM** (8)
- Do We Really Need Multimodal Emotion Language Models Larger Than 1B Parameters?
- This raises a fundamental question: do we really need the multimodal MER model larger than 1B parameters for high-quality MER?
- Do We Really Need Multimodal Emotion Language Models Larger Than 1B Parameters?.
- Our goal is to preserve most of the performance of an 8B teacher while moving the deployment model below 1B parameters. reliant on increasingly large model scales—typically requiring at least 7B parameters [5, 6]—to achieve strong recognition and gen- eration performance.
- This naturally raises a key question: do we really need multimodal emotion language models larger than 1B parameters for high-quality MER?

**LAT** (2)
- In descriptive mode, M-GRPO refinement reduces the average out- put from 110.5 to 70.8 words and latency from 4.6 s to 3.1 s, a 32.8% reduction over the SWD-H-only student.
- In direct mode, the M-GRPO student runs at 0.5 s per sample.

**MEM** (3)
- Video Audio Text Large Parameter Model Current Approach Lightweight Model Deployable on edge devices SWD Hidden-State Distillation GRPO Description Refinement ~3GB VRAM ~4.3s/sample ~20GB VRAM ~9.1s/sample Figure 1: Large multimodal emotion models achieve strong performance but are difficult to deploy at the edge.
- The sub-1B student achieves 11.0× compression in parameters and FLOPs, and 7.9× memory reduction from 20.04 GB to 2.54 GB.
- For closed-set tasks where the label space is fixed, direct mode offers a viable low-latency alternative. (Answer to RQ5): The Light-MER student fits within 2.54 GB memory and processes samples in 0.5 s in direct mode or 3.1 s in descriptive mode, with 11× fewer parameters than the teacher.


# 4.1 신규 5편
## 2409.07267 MiniDrive: More Efficient Vision-Language Models with Multi-Level 2D Features as Text Tokens for Autonomous Driving
(전문 없음)


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



# 4.5 신규 11편
## 2407.11771 XEdgeAI: A Human-centered Industrial Inspection Framework with Data-centric Explainable Edge AI Approach
(전문 없음)


## 2410.14803 [keep] DistRL: An Asynchronous Distributed Reinforcement Learning Framework for On-Device Control Agents

- 기반 모델: —
- 비교 대상: —
- 하드웨어: CPU, NVIDIA V100, T4
- 벤치마크: —

**BIT** (1)
- Instead of directly regressing on scalar returns, we train the value network to predict the probability that the Monte Carlo return Gt is positive, transforming value estimation into a binary classification task.

**PARAM** (1)
- In practice, we validate our framework using a T5-based multimodal generation architecture with 1.3B parameters (details in Appendix A.5.1) to efficiently handle both vision and language inputs.

**SPEED** (1)
- Our experiments show that, on average, DISTRL delivers a 3× improvement in training efficiency and enables training data collection 2.4× faster than the leading synchronous multi-machine methods.


## 2410.16261 [star] Mini-InternVL: A Flexible-Transfer Pocket Multimodal Model with 5% Parameters and 90% Performance

- 기반 모델: InternVL, InternVL2, LLaVA, LLaVA-NeXT, LLaVA-OneVision, MiniCPM-V, Qwen-VL, Qwen2-VL
- 비교 대상: —
- 하드웨어: A100
- 벤치마크: AI2D, ChartQA, DocVQA, GQA, MMBench, MME, MMMU, MMbench, MathVista, OCRBench, ScienceQA

**PARAM** (3)
- In this work, we introduce Mini-InternVL, a series of MLLMs with parameters ranging from 1B to 4B, which achieves 90% of the performance with only 5% of the parameters.
- Remarkably, compared with InternVL2-76B, the proposed Mini-InternVL-4B achieves 90% of the performance of larger counterparts while using only 5% of the parameters, significantly reducing computational overhead.
- Notably, compared to InternVL2-Llama3-76B, which utilizes the larger InternViT-6B, Mini-InternVL achieves approximately 90% of its performance while using 5% parameters.


## 2411.10640 [keep] BlueLM-V-3B: Algorithm and System Co-Design for Multimodal Large Language Models on Mobile Devices

- 기반 모델: InternVL, InternVL2, LLaVA, LLaVA-NeXT, MiniCPM-V, Phi-3-Vision, Qwen2-VL
- 비교 대상: —
- 하드웨어: CPU
- 벤치마크: AI2D, ChartQA, DocVQA, MMBench, MMMU, MMbench, MathVista, OCRBench, RealWorldQA, TextVQA, VQAv2

**BIT** (5)
- BlueLM-V-3B boasts the follow- ing key highlights: (1) Small Size: BlueLM-V-3B features a language model with 2.7B parameters and a vision en- coder with 400M parameters. (2) Fast Speed: BlueLM- V-3B achieves a generation speed of 24.4 token/s on the MediaTek Dimensity 9300 processor with 4-bit LLM weight quantization.
- For example, a 4-bit quantized LLaMA 7B model requires approximately 4.5 GB of memory, which can impact system fluency due to high memory usage.
- For instance, on the Medi- aTek Dimensity 9300 processor, a 4-bit quantized LLaMA 7B model generates around 10-15 tokens per second, limit- ing its suitability for real-time applications.
- We employ INT8 precision for the ViT and the MLP projector weights, and INT4 precision for the LLM weights.
- During inference, we store the KV cache in INT8 precision.

**PARAM** (7)
- BlueLM-V-3B boasts the follow- ing key highlights: (1) Small Size: BlueLM-V-3B features a language model with 2.7B parameters and a vision en- coder with 400M parameters. (2) Fast Speed: BlueLM- V-3B achieves a generation speed of 24.4 token/s on the MediaTek Dimensity 9300 processor with 4-bit LLM weight quantization.
- Specifically, we train a state-of-the-art MLLM with only 3B parameters and effectively deploy it on the NPU of smart- phones.
- The compact size of these models (2-3B parameters) enables deployment on user devices, such as personal computers and mobile phones.
- Image Encoder: To process multimodal (image and language) inputs, we utilize the SigLIP [141] ViT for 384×384 input images, as described in [64, 134], which has 400M parameters.
- The MiniCPM-2B model has 2.7B parame- ters, matching the parameter count of BlueLM-3B.

**LAT** (1)
- 5, where we need 1.9 + 0.16 = 2.06s to encode the image and can hide a total latency of 200ms.

**MEM** (3)
- For example, a 4-bit quantized LLaMA 7B model requires approximately 4.5 GB of memory, which can impact system fluency due to high memory usage.
- Take the MediaTek Dimensity 9300 processor as an example, with a memory requirement of just 2.2GB, it can encode images with a resolution of 768×1536 in approximately 2.1 seconds and achieves a token throughput speed of 24.4 token/s.
- 6, reduces the waiting time for the first token genera- tion, improves overall responsiveness, and limits the peak memory usage of BlueLM-V-3B to 2.2GB.

**THR** (4)
- BlueLM-V-3B boasts the follow- ing key highlights: (1) Small Size: BlueLM-V-3B features a language model with 2.7B parameters and a vision en- coder with 400M parameters. (2) Fast Speed: BlueLM- V-3B achieves a generation speed of 24.4 token/s on the MediaTek Dimensity 9300 processor with 4-bit LLM weight quantization.
- For instance, on the Medi- aTek Dimensity 9300 processor, a 4-bit quantized LLaMA 7B model generates around 10-15 tokens per second, limit- ing its suitability for real-time applications.
- Take the MediaTek Dimensity 9300 processor as an example, with a memory requirement of just 2.2GB, it can encode images with a resolution of 768×1536 in approximately 2.1 seconds and achieves a token throughput speed of 24.4 token/s.
- OpenCompass Benchmark: To evaluate the overall performance of BlueLM-V-3B, we use the OpenCompass benchmark [26], including MMbench [75], MMStar [18], 7 Model Name Params Processor Solution Image Processing LLM Prefilling Throughput MiniCPM-V 2.5 [134] 8B MediaTek Dimensity 9300 CPU (llama.cpp) / 4.0s 13.9s 4.9 token/s


## 2504.14239 [keep] InfiGUI-R1: Advancing Multimodal GUI Agents from Reactive Actors to Deliberative Reasoners

- 기반 모델: BLIP-2, LLaVA, Qwen-VL, Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: NVIDIA H800
- 벤치마크: —

**PARAM** (1)
- Our Ac- tor2Reasoner framework, combining Spatial Reasoning Distillation and RL-based Deliberation Enhancement (Sub-goal Guidance, Er- ror Recovery), successfully transforms a base MLLM into a more effective Deliberative Reasoner, achieving state-of-the-art among models with similar parameter counts in trajectory-based


## 2509.07666 [keep] MoLoRAG: Bootstrapping Document Understanding via Multi-modal Logic-aware Retrieval

- 기반 모델: LLaVA-Next, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: DocVQA

**FREE** (4)
- To enhance flexibility, MoLoRAG offers two variants: a training-free solution for easy deployment and a fine-tuned version to improve logical rele- vance checking.
- The first is a training-free variant, which leverages a pre-trained VLM, e.g., Qwen2.5- VL-3B (Bai et al., 2025), to perform graph traver- sal and retrieval directly, providing an off-the-shelf solution that is easy to deploy.
- The fine-tuned variant, MoLoRAG+, outperforms the training-free ver- sion, demonstrating the benefits of task-specific optimization.
- For example, with DeepSeek-VL- 16B, MoLoRAG+ achieves 5.04% improvement on MMLongBench compared to the training-free MoLoRAG.

**BIT** (1)
- Specifically, it evaluates Binary Correctness by determining whether the generated answer matches the ground-truth answer, assigning a binary score of 0 or 1.


## 2509.21259 Semantic Edge-Cloud Communication for Real-Time Urban Traffic Surveillance with ViT and LLMs over Mobile Networks
(전문 없음)


## 2510.25122 NanoVLA: Routing Decoupled Vision-Language Understanding for Nano-sized Generalist Robotic Policies
(전문 없음)


## 2603.06569 [keep] Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders

- 기반 모델: Gemma 3, Gemma3, InternVL, InternVL3.5, LLaVA, LLaVA-Video, Qwen-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, ChartQA, DocVQA, EgoSchema, LongVideoBench, MMMU, MVBench, MathVista, OCRBench, RealWorldQA, RealworldQA, VideoMME

**PARAM** (3)
- 2 Methodology 2.1 Model Architecture Our Penguin series comprises Penguin-Encoder and Penguin-VL, built upon Qwen3 LLM backbones [59] and available in 2B and 8B parameter variants (Penguin-Encoder maintains a fixed parameter size, independent of the VLM backbone.).
- If required by future scenarios, this framework can be readily extended to train vision encoders with substantially larger model capacities (e.g., 1.5B parameters), compared to alternative approaches such as contrastive learning.
- After removing parameters unrelated to visual processing, the model uses approximately 400M parameters for visual modeling, which is broadly consistent with SigLIP.

**THR** (1)
- Video Building upon the deterministic inference settings established for images, we introduce additional configurations for video inputs: specifically, we cap the maximum number of frames at 300 and set the frame rate up to 3 FPS.


## 2604.27393 [keep] MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction

- 기반 모델: InternVL3.5, LLaVA, MiniCPM-V
- 비교 대상: —
- 하드웨어: NVIDIA RTX 4090, RTX 4090
- 벤치마크: AI2D, DocVQA, LongVideoBench, MLVU, MMBench, MMMU, MathVista, OCRBench, TextVQA, Video-MME

**TOK** (1)
- Specifically, each image is first divided into slices, and each slice is then encoded into 1024 tokens by a SigLIP ViT [6] (0.4B) and compressed into 64 tokens by the resampler module.

**BIT** (5)
- Control formulation specifies how the model decides whether to speak: in the Listen-Speak (LS) formulation, the model first predicts a binary listen/speak control token before content generation; in the Listen-Text (LT) formulation, the model directly predicts either [listen] or normal text tokens in a shared output sp
- Model Dtype Throughput ↑ First-token Latency ↓ Memory ↓ (tokens/s) (s) (GB) Qwen3-Omni-30B-A3B BF16 OOM OOM OOM MiniCPM-o 4.5 BF16 154.3 0.59 19 Qwen3-Omni-30B-A3B INT4 147.8 0.98 20 MiniCPM-o 4.5 INT4 212.3 0.58 11 Table 12: Inference efficiency comparison of different inference frameworks for MiniCPM-o 4.5.
- Framework Dtype RTX 4090 DGX Spark RTF ↓ Memory (GB) ↓ RTF ↓ Memory (GB) ↓ PyTorch BF16 OOM OOM 2.43 26 PyTorch INT4 1.26 14 1.27 14 llama.cpp-omni (Ours) FP16 0.27 19 0.46 19 llama.cpp-omni (Ours) INT4 0.21 11 0.20 11 nunciation accuracy over synthesizing speech after the full text is generated.
- In INT4, MiniCPM-o 4.5 further achieves 212.3 tokens/s, lower first-token latency, and nearly half the memory usage compared with Qwen3-Omni-30B-A3B.
- Compared with the PyTorch implementation, llama.cpp-omni substantially reduces RTF on both RTX 4090 and DGX Spark while maintaining a lower memory footprint under INT4 quantization, demonstrating its effectiveness for efficient real-time deployment.

**PARAM** (4)
- With a total of 9B parameters, MiniCPM-o 4.5 approaches Gemini 2.5 Flash in vision-language capabilities, delivering state-of-the-art open-source performance at its scale.
- With a total of 9B parameters, it approaches Gemini 2.5 Flash in vision-language capabilities, delivering state-of-the-art open-source performance at its scale.
- All learnable components—from multimodal encoders through the LLM backbone to the speech token decoder, totaling approximately 9B parameters—are differentiably connected in token-level, enabling end-to-end gradient propagation and joint optimization across modalities during training.
- With only 9B parameters, it consistently outperforms models of similar scale, such as InternVL3.5-8B [85] and Qwen3-VL-8B [4], as well as larger models like Qwen3-Omni-30B [7], while close to leading proprietary models including Gemini 2.5 Flash [86] and GPT-5 [87].

**MEM** (1)
- In BF16, Qwen3-Omni-30B- A3B runs out of memory, while MiniCPM-o 4.5 achieves 154.3 tokens/s with 19 GB memory usage.

**THR** (4)
- When backbones are instead required to directly generate speech tokens (typically about 25 tokens per second), as in recent works [11, 12], the efficiency can be significantly impeded, and the core language capabilities also tend to degrade [13, 14].
- To enable flexible quality-efficiency trade-offs during inference, we augment omni-modal data with varying resolutions and frame rates, randomly setting the maximum frame resolution to 0.2–0.4 megapixels and sampling the frame rate uniformly from 1–5 FPS.
- In BF16, Qwen3-Omni-30B- A3B runs out of memory, while MiniCPM-o 4.5 achieves 154.3 tokens/s with 19 GB memory usage.
- In INT4, MiniCPM-o 4.5 further achieves 212.3 tokens/s, lower first-token latency, and nearly half the memory usage compared with Qwen3-Omni-30B-A3B.


## 2607.13429 [keep] Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment

- 기반 모델: Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: GQA


# 4.2 신규 10편
## 2401.16420 [star] InternLM-XComposer2: Mastering Free-form Text-Image Composition and Comprehension in Vision-Language Large Model

- 기반 모델: BLIP-2, IDEFICS, LLaVA, LLaVA-1.5, Qwen-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, ChartQA, GQA, MMBench, MME, MMMU, MathVista, POPE, SEED-Bench, VQAv2

**PARAM** (3)
- The InternLM- 1 arXiv:2401.16420v1 [cs.CV] 29 Jan 2024 XComposer2 model series with 7B parameters are pub- licly available at https://github.com/InternLM/ InternLM-XComposer.
- Our InternLM-XComposer2 gets SOTA results in 6 of the 12 benchmarks with only 7B parameters, showing competitive results with current closed-source APIs and previous open-source SOTA MLLMs.
- Meanwhile, despite having only 7B parameters, our model attains a slightly worse score of 43.0% on the challenging college-level benchmark MMMU.


## 2404.14047 [keep] An empirical study of LLaMA3 quantization: from LLMs to MLLMs

- 기반 모델: LLaVA, LLaVA-Next, llava, llava-next
- 비교 대상: —
- 하드웨어: NVIDIA A800
- 벤치마크: AI2D, ChartQA, DocVQA, MMBench, MME

**TOK** (1)
- However, in the case of LLaMA3-8B, the overall speed ranged between 50 to 80 tokens per second, with AWQ’s quantization kernel achieving an inference speed of 89.8 tokens per second, surpassing that of other methods.

**BIT** (8)
- Both approaches preserve LLaMA3’s 3-bit quantization capability, with the poten- 4 F.
- The recent emergence of binarized LLM quantization methods has realized ultra-low bit-width LLM weight compression.
- PB-LLM [12] employs a mixed-precision quantization strategy, retaining a small portion of signif- icant weight full-precision while quantizing most of the weights to 1 bit.
- DB-LLM [14] achieves efficient LLM compression through double binarization weight split- ting and proposes a deviation-aware distillation strategy to further improve 2-bit LLM performance.
- BiLLM [15] pushes the LLM quantization limit further down to 1.1 bit by residual approximation of salient weights and grouped quantization of non-salient weights.

**PARAM** (1)
- Keywords Model quantization · Large language model · Multi-modal · Deep learning 1 Introduction Launched by Meta in February 2023, the LLaMA [1] se- ries1, a collection of foundation language models ranging from 7B to 65B parameters, represents a breakthrough in autoregressive large language models (LLMs) using the Tra

**MEM** (2)
- We also used 8 NVIDIA A800 with 80GB GPU memory for quantitative evaluation.
- It demonstrates that methods such as SmoothQuant and AWQ are highly efficient in terms of memory usage and training time, with SmoothQuant requiring only 13.5 GB of GPU mem- ory and 7 min for LLaMA2-7B, making it an ideal choice for memory-constrained environments.

**THR** (2)
- In the case of LLaMA2-7B, GPTQ, AWQ, and Omniquant all exhibited speeds exceeding 100 tokens per second.
- However, in the case of LLaMA3-8B, the overall speed ranged between 50 to 80 tokens per second, with AWQ’s quantization kernel achieving an inference speed of 89.8 tokens per second, surpassing that of other methods.

**ACC** (3)
- In the evaluation metrics of PPL (Table 1 and Ta- ble 2) and CommonSenseQA (Table 3 and Table 4), we found that, overall, the 4-bit methods had a slight performance decrease (approximately 2%) compared to the original 16-bit LLM, with no significant differences between the different methods.
- In the context of 3-bit scenarios, traditional RTN quantization methods faced substantial performance losses (over 10% lower than 4 bits), while methods such as GPTQ, AWQ, SliM-LLM, and QuIP were able to maintain performance close to that of 4 bits (with less than 5% performance degra- dation).
- At 3 bits, the performance loss ranges from 5% to 20%, with the highest loss, 20.75%, occurring on the MME cognition task.


## 2405.01413 [keep] MiniGPT-3D: Efficiently Aligning 3D Point Clouds with Large Language Models using 2D Priors

- 기반 모델: BLIP-2, LLaVA
- 비교 대상: —
- 하드웨어: A100, A800, NVIDIA RTX 3090, RTX 3090
- 벤치마크: —

**PARAM** (7)
- Moreover, we introduce the Mixture of Query Experts (MQE), which comprises multiple query experts and an expert router, enabling the adaptive aggregation of features from multiple experts with only 0.4M parameters.
- Given Q-Former’s extensive 105M parameters, we employ PEFT technologies to fine-tune its Query, Key, and Value layers, and normalization layers, thus enhancing adaptability to point clouds while preserving 2D knowledge.
- To build a robust bridge between domains, we train the projection layer using 660k caption-point cloud pairs, involving 1.4M parameters, as detailed in Table 1.
- During this process, to minimize the impact of the 3D-2D bridge, we employ the identical dataset from the first stage to train 47.4M parameters, as outlined in Table 1.
- 4 EXPERIMENTS 4.1 Experimental Settings Utilizing one RTX 3090 GPU with 24GB of RAM, we train MiniGPT- 3D with only 47.8M trainable parameters in 26.8 hours.

**SPEED** (1)
- 8× A800), with up to 6× acceleration (26.8h on RTX 3090 vs.


## 2407.03320 [keep] InternLM-XComposer-2.5: A Versatile Large Vision Language Model Supporting Long-Contextual Input and Output

- 기반 모델: InternVL, InternVL1., LLaVA, Qwen-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, ActivityNet, ChartQA, DocVQA, GQA, MLVU, MMBench, MME, MMMU, MVBench, MathVista, OCRBench, RealWorldQA, SEED-Bench, TextVQA, VQAv2

**PARAM** (1)
- IXC-2.5 with only 7B parameters performs on par with the current large open-source LVLMs and close-source APIs.


## 2502.09838 [keep] HealthGPT: A Medical Large Vision-Language Model for Unifying Comprehension and Generation via Heterogeneous Knowledge Adaptation

- 기반 모델: BLIP-2, InternVL2, LLaVA, LLaVA-1.5
- 비교 대상: —
- 하드웨어: —
- 벤치마크: MMMU

**FREE** (1)
- In- spired by the plug-and-play nature of LoRA (Hu et al.


## 2503.07065 [keep] Boosting the Generalization and Reasoning of Vision Language Models with Curriculum Reinforcement Learning

- 기반 모델: InternVL, InternVL2, LLAVA-next, LLaVA, Llava, Qwen-VL, Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: A800, NVIDIA A800
- 벤치마크: AI2D, MMBench, MathVista, OCRBench, RefCOCO, RefCOCOg, refcoco

**BIT** (6)
- Specif- ically, our Curriculum RL implements a three-stage progressive reward structure: starting with binary decision tasks (hard reward for binary yes/no responses), advancing to multiple-choice selection (intermediate reward for accurate option selection), and culminating in open-ended response (complex reward for c
- Our key innovation lies in designing difficulty-aware reward mechanisms that align with natural task progression, ad- vancing through three stages: Binary Decision, Multi- ple Choice, and Open-ended Response (datasets detailed in Sec.
- Stage 1: Binary Decision Learning In the initial stage of reinforcement learning, we adopt bi- nary decision questions as the simplest form of task for- mat, as shown in Fig.
- 3 (a), which significantly reduces the output freedom to binary choices, making it easier to learn basic visual understanding and reasoning patterns.
- The reward function for this stage is as fol- lows: RBinary(ostd, ogt) = ( 1, if ostd = ogt 0, otherwise (2) where ostd represents the model’s binary response and ogt is the ground truth answer.

**PARAM** (3)
- However, these achievements predominantly rely on massive model scaling (>32B parameters), creating substantial deployment barri- ers in resource-constrained environments.
- This limitation motivates the exploration of efficient training paradigms for small-scale VLMs (1B-7B parameters).
- Also, most approaches are limited to large-scale architec- tures (>32B parameters), leaving the reasoning potential in smaller models unexplored.


## 2507.19679 [keep] Efficient Learning for Product Attributes with Compact Multimodal Models

- 기반 모델: Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**PARAM** (2)
- In this paper, we investigate label- efficient semi-supervised fine-tuning strategies for compact VLMs (2B–3B parameters) that leverage unlabeled prod- uct listings through Direct Preference Optimization (DPO).
- For UFT with Direct Preference Optimization (DPO) and Self Learning (SL), PT and Peft-10 models are used as the initial SFT checkpoints. two Qwen-family backbones—Qwen2-VL-2B-Instruct and Qwen2.5-VL-3B-Instruct, resulting in approximately 2.5M and 7.3M trainable parameters, respectively.


## 2508.00230 [keep] Towards Higher Effective Rank in Parameter-efficient Fine-tuning using Khatri--Rao Product

- 기반 모델: —
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**BIT** (2)
- Commonsense reasoning We further investigate resource-efficient fine-tuning of Large Language Models (LLMs) for commonsense reasoning through 4-bit quantization-aware training and evaluation.
- 4}” format); and (3) out-of-distribution BoolQ, PiQA, and WinoGrande test sets (binary answers).

**PARAM** (1)
- We demonstrate performance gains with KRAdapter on vision-language mod- els up to 1B parameters and on large language models up to 8B parameters, particularly on unseen common-sense reasoning tasks.


## 2601.22828 [keep] Decomposing and Composing: Towards Efficient Vision-Language Continual Learning via Rank-1 Expert Pool in a Single LoRA

- 기반 모델: —
- 비교 대상: —
- 하드웨어: A6000, ascending 
- 벤치마크: —

**MEM** (1)
- 2024), our approach reduces trainable parameters by 96.7% and peak GPU memory consumption by 66.7%.


## 2605.06175 VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts
(전문 없음)

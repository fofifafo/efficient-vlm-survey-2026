# 비교 매트릭스 근거 — 4.5R (5편)


## 2408.01800 [star] MiniCPM-V: A GPT-4V Level MLLM on Your Phone

- 기반 모델: BLIP-2, IDEFICS, IDEFICS2, Idefics2, InternVL, LLaVA, LLaVA-NeXT, LLaVA-Next, Mini-Gemini, MiniCPM-V, PaliGemma, Phi-3-Vision, Phi-3-vision, Qwen-VL
- 비교 대상: —
- 하드웨어: CPU, NVIDIA 4090, Snapdragon 8 Gen 3, Snapdragon 8 Gen3 
- 벤치마크: AI2D, ChartQA, DocVQA, GQA, MME, MMMU, MathVista, OCRBench, RealWorldQA, RefCOCO, ScienceQA, TextVQA, VQAv2, VizWiz

**BIT** (1)
- We opt for the Q4_K_M mode 4-bit quantization strategy within GGML4 framework.

**PARAM** (1)
- In addition, MiniCPM-Llama3-V 2.5 also achieves lower hallucination rates than GPT-4V-1106 on Object HalBench, indicating its trustworthiness for real-world applications. (3) The smaller MiniCPM-V 2.0 with 2B parameters achieves significantly better performance compared with other 2B~3B models, and is even comparable w

**FLOP** (1)
- For example, Qualcomm Adreno 750 only has 6 TFLOPS, while NVIDIA 4090 can reach 83 TFLOPS.

**LAT** (2)
- Combining quantization and llama.cpp on Xiaomi 14 Pro (Snapdragon 8 Gen 3), the model achieves a text encoding latency of 64.2s and a text decoding speed of 1.3 tokens/s (as depicted in Fig.
- Encoding latency shows a notable reduction from 50.5s to 17.0s, while decoding throughput experiences a significant boost from 1.3 tokens/s to 3.2 tokens/s.

**MEM** (2)
- High-performance servers typically boast extensive memory capacities, often exceeding 100GB or even 1TB.
- In contrast, the memory available on mobile phones typically ranges from 12GB to 16GB, which can be insufficient for MLLM deployment.

**THR** (3)
- Combining quantization and llama.cpp on Xiaomi 14 Pro (Snapdragon 8 Gen 3), the model achieves a text encoding latency of 64.2s and a text decoding speed of 1.3 tokens/s (as depicted in Fig.
- Encoding latency shows a notable reduction from 50.5s to 17.0s, while decoding throughput experiences a significant boost from 1.3 tokens/s to 3.2 tokens/s.
- Specifically, decoding throughput surged from 3.2 tokens/s to an impressive 8.2 tokens/s, surpassing the typical human reading speed.


## 2501.04322 [keep] Eve: Efficient Multimodal Vision Language Models with Elastic Visual Experts

- 기반 모델: BLIP-2, LLAVA, LLAva, LLaVA, LLaVA-1.5, Mini-Gemini, Qwen-VL
- 비교 대상: —
- 하드웨어: Ascend AI 
- 벤치마크: AI2D, ChartQA, DocVQA, GQA, MMBench, MME, POPE, ScienceQA, TextVQA, VQAV2, VQAv2

**TOK** (1)
- When employing the random token distribution mechanism, approximately 25% of tokens were discarded at layers 11 and 21.

**PARAM** (4)
- This balanced approach results in a versatile model with only 1.8B parameters that delivers significant improvements in both multimodal and linguistic tasks.
- Notably, in config- urations below 3B parameters, Eve distinctly outperforms in language benchmarks and achieves state-of-the-art results 68.87% in VLM Benchmarks.
- Within a model size of 3B parameters, Eve achieves state-of-the-art perfor- mance, and compared to other multimodal models, our lan- guage capabilities are better preserved.
- 1, Eve notably outper- forms existing VLM with fewer than 3B parameters, espe- cially in maintaining full language task capabilities.


## 2507.14049 [keep] EdgeVLA: Efficient Vision-Language-Action Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: A100, CPU, Jetson Nano presents 
- 벤치마크: —

**PARAM** (4)
- Our proposed architecture EVLA comprises of a pretrained language model Qwen2-0.5B fused with two visual encoders SigLIP [19] and DINOv2 [12] adding to 1B parameters.
- These systems typically train models from scratch with model sizes from 10 to 100M parameters which limits their ability to generalize to novel environments [20], [3].
- For language processing, we utilize Qwen2 [17] with 0.5B parameters as it demon- strates the effectiveness of SLMs in achieving comparable performance to that of larger models.
- BridgeData V2 training characteristics Initial experiments on the BridgeData V2 dataset con- ducted on a single node with 8 A100-80GB GPUs, validate that EVLA can achieve similar training performance to its 7.5B parameters counterpart.

**SPEED** (1)
- We achieve this through two key innovations: 1) Eliminating the autoregressive requirement for end-effector position prediction, leading to a 7x speedup in inference, and 2) Leveraging the efficiency of Small Language Models (SLMs), demonstrating comparable training performance to larger models with significantly re- d

**MEM** (1)
- Table I compares the inference time and memory requirements of EVLA and OpenVLA on an A100-40GB GPU.


## 2511.08914 [keep] SPEED-Q: Staged Processing with Enhanced Distillation towards Efficient Low-bit On-device VLM Quantization

- 기반 모델: InternVL2.5, InternVL3, LLaVA, Qwen2-VL
- 비교 대상: FastVLM
- 하드웨어: —
- 벤치마크: AI2D, DocVQA, MMBench, MMMU, OCRBench, RealWorldQA, SEED-Bench, ScienceQA

**BIT** (8)
- Exten- sive experiments across multiple benchmarks demonstrate that SPEED-Q achieves up to 6× higher accuracy than existing quantization methods under 2-bit settings and con- sistently outperforms prior on-device VLMs under both 2- bit and 4-bit settings.
- 0 1000 2000 3000 4000 Model File Size (MB) 40 50 60 70 Average score of 8 benchmarks 0.25B 0.5B 0.6B 1.5B 0.8B 2B 1B 2B Low-bit quantization 2B(4-bit) 2B(2-bit) 1B(4-bit) 1B(2-bit) BF16 SmolVLM FastVLM H2OVL InternVL3 InternVL3 SPEED-Q (Ours) Figure 1: Comparison with SOTA on-device VLMs.
- 2024) focus on 8/4-bit quantization and have restricted quantization to lan- guage modules, leaving the problem of unified quantiza- arXiv:2511.08914v1 [cs.CV] 12 Nov 2025 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 Layer Index 0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 Average Absolute Gradient Vision m
- To the best of our knowledge, SPEED-Q is the first quantiza- tion framework to enable 2/4-bit weight-only quantization of both vision and language modules in small-scale billion- parameter VLMs, achieving superior accuracy–efficiency trade-offs.
- For example, 2-bit quan- tized InternVL3-1B consumes less than 400 MB of run- ning memory while achieving accuracy comparable to the best 0.6B model of FastVLM that requires almost 1.5GB of memory.

**PARAM** (4)
- However, existing research has rarely ex- plored aggressive quantization on VLMs, particularly for the models ranging from 1B to 2B parameters, which are more suitable for resource-constrained edge devices.
- This limitation poses a significant challenge for deploying VLMs with 1–2B parameters, as the visual mod- ule accounts for a substantial portion of the parameters.
- 5.3 Comparison with Lightweight VLMs As shown in Table 4, we first compare the quantized models with the existing VLMs designed for edge deployment, such as SmolVLM, FastVLM, and H2OVL, which typically have fewer than 1B parameters.
- 6 Conclusion In order to further unleash the potential of VLMs deploy- ment on edge devices, we have presented SPEED-Q, a novel quantization framework for 1-2B parameter VLMs.

**MEM** (3)
- For example, InternVL3-2B consumes over 4 GB of memory, pushing memory usage close to system lim- its and causing application instability.
- For example, 2-bit quan- tized InternVL3-1B consumes less than 400 MB of run- ning memory while achieving accuracy comparable to the best 0.6B model of FastVLM that requires almost 1.5GB of memory.
- SPEED-Q successfully limits qcom_8elite 1789.5 485.0 315.0 1304.5 MB 170.0 MB Model File Size (MB) FP16 4-bit 2-bit qcom_8elite 1855.0 527.0 388.0 1328.0 MB 139.0 MB Memory Footprint (MB) FP16 4-bit 2-bit Figure 5: On-device efficiency evaluation of FP16 and low- bit InternVL2.5-1B on Samsung Galaxy S25 Ultra. the perf

**ACC** (2)
- Specifically, by utilizing the proposed SPEED-Q, the quantized 4-bit model exhibits a marginal performance decrease of 3% compared to their original BF16 counterpart.
- SPEED-Q successfully limits qcom_8elite 1789.5 485.0 315.0 1304.5 MB 170.0 MB Model File Size (MB) FP16 4-bit 2-bit qcom_8elite 1855.0 527.0 388.0 1328.0 MB 139.0 MB Memory Footprint (MB) FP16 4-bit 2-bit Figure 5: On-device efficiency evaluation of FP16 and low- bit InternVL2.5-1B on Samsung Galaxy S25 Ultra. the perf


## 2607.12659 [keep] Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference

- 기반 모델: —
- 비교 대상: —
- 하드웨어: 4090, A6000, CPU, Jetson, Jetson Orin, Jetson Orin Method , Jetson Orin and have , Jetson Orin show , Jetson Thor, Jetson Thor Method , NVIDIA Jetson Orin, NVIDIA RTX 4090, Orin, RTX 4090
- 벤치마크: —

**SPEED** (3)
- Compared to π0.5 inference on naive PyTorch, our schedul- ing optimization achieves 2.11× and 1.87× reductions in reaction time on Orin and Thor, because action prediction no longer requires invoking the VLM every time.
- Our graph reuse method achieves a 2.96× reduction in reaction time on Orin by eliminating per-inference graph construction over- head.
- Our GPU-resident intermediate buffering and flow matching unrolling achieve 1.50× and 1.59× acceleration for the action expert on the two devices, by avoiding KV communication and repeated graph invocation across multiple denoising steps.

**LAT** (2)
- As shown in Figure 1(b), state-of-the-art VLA models such as π0.5 [3] achieve an inference latency of approximately 1.4 seconds on a Jetson Orin, resulting in a control frequency around 0.7 Hz.
- Compared with vla.cpp, which has a latency of 893.0ms on the Orin platform [31], Jetson-PI achieves a 5.41× improvement in control frequency through scheduling and system opti- mizations.

**MEM** (1)
- RTX 4090 RTX A6000 Orin 32GB Orin 64GB Thor Max Power (W) 450 300 50 50 130 TOPS 309 309 200 275 510 Memory 24GB GDDR6X 48GB GDDR6 48GB LPDDR5 48GB LPDDR5 48GB LPDDR5X Bandwidth (GB/s) 1024 768 204.8 204.8 273 Balance Computational Intensity 618 804 1953 2685 3736 (TOPS/Bandwidth ×1000) VLM Compute Bound Compute Bound 

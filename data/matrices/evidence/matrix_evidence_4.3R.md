# 비교 매트릭스 근거 — 4.3R (14편)


## 2407.19409 [keep] LLAVADI: What Matters For Multimodal Large Language Models Distillation

- 기반 모델: BLIP-2, IDEFICS, LLAVA, LLaVA, LLaVA-1.5, LLava, Qwen-VL
- 비교 대상: FastV, VTW
- 하드웨어: —
- 벤치마크: GQA, MMBench, MME, POPE, ScienceQA, TextVQA

**PARAM** (4)
- By evaluating different benchmarks and proper strategy, even a 2.7B small-scale model can perform on par with larger models with 7B or 13B parameters.
- Our choice for the teacher model is LLaVA-v1.5-13B [41], while the student model employs MobileLLaMA [15] as its LLM, which only contains 2.7B parameters.
- The teacher model LLava-V1.5-13B [41] uses the pre-trained CLIP [52] ViT-L/14 with only 0.3B parameters as its visual encoder.
- The teacher model utilizes the large language model Vicuna-13B-v1.5 [14], while our student model employs the MobileLLaMA [15] with 2.7B parameters as our large language model.

**SPEED** (1)
- 4.5 Compared with other distillation strategy DistilBERT [54] proposes an effective and efficient distillation that reduces the size of a BERT model by 40% while retaining 97% of its language understanding capabilities and being 60% faster.

**ACC** (1)
- 4.5 Compared with other distillation strategy DistilBERT [54] proposes an effective and efficient distillation that reduces the size of a BERT model by 40% while retaining 97% of its language understanding capabilities and being 60% faster.


## 2408.03735 [keep] Advancing Multimodal Large Language Models with Quantization-Aware Scale Learning for Efficient Adaptation

- 기반 모델: BLIP2, LLaVA
- 비교 대상: —
- 하드웨어: A100, A800
- 벤치마크: ScienceQA

**BIT** (8)
- Methods #T-Params Memory (GB) Time (hours) Average (%) LLaVA [28] 13B OOM N/A N/A LLaVA† [28] 13B 71.54 8.75 90.92 QLoRA 500.70M 66.92 6.12 86.96 QSLAW 84.25M 66.52 5.76 91.04 in QLoRA [12], which quantizes each linear layer’s weights into a 4-bit NormalFormat (NF) datatype and uses the low-rank adapter (LoRA) [20] for
- As can be seen, utilizing QLoRA to quantize LLM weights to 4-bit can signif- icantly reduce both GPU memory consumption and time overhead.
- This observation elucidates the performance deterioration of QLoRA in VL instruction tuning for MLLMs, as its adopted NF4 datatype only pursues equating the quantity of values across all quantization bins from the weight tensor and causes severe information loss, making it hard for LoRA to accommodate activation outlie
- Furthermore, we adopt uniform quantization instead of forcing an equal number of weights in each quantiza- tion bin like NF4 and initialize the quantized weights with Omni- Quant [37], an LLM uniform quantization method that employs weight clipping to mitigate the quantization difficulty occurring in language tasks, ra
- LLM.int8() [11] highlights significant errors in quantization caused by activation outliers within LLMs, leading to the proposal of a mixed-precision quantization approach.


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


## 2410.08119 [keep] Q-VLM: Post-training Quantization for Large Vision-Language Models

- 기반 모델: LLaVA
- 비교 대상: —
- 하드웨어: —
- 벤치마크: ScienceQA, VizWiz

**BIT** (8)
- Our Q-VLM can still generate plausible response in multi-modal reasoning with 4-bit quantization because of the precise rounding functions, and compresses the memory by 2.78x and increase the generate speed by 1.44x about 13B LLaVA model.
- LLM.int8() [8], SmoothQuant [46] and ZeroQuant [48] handled activation outliers to achieve accurate quantization function learning by eliminating the extreme values with equivalent transformation, yet encountered challenges in effectively scaling to extremely large models due to the unbearable computational costs.
- The quantization function parameters were updated for 10 6 Method W6A6 W4A4 Memory Search cost Accuracy Memory Search cost Accuracy QLoRA 9.7G 23.7 88.43 6.6G 23.5 77.53 +CDM 26.9 88.95 25.9 78.66 +VEO 24.1 88.72 23.7 78.35 Q-VLM 25.1 89.34 24.6 79.79 Table 1: Effect of different LVLM quantization method we proposed. "
- INT4 Q-VLM Oceans are huge bodies of salt water.
- INT4 AWQ The Southern Ocean reaches from the shores of Antarctica to South latitude.


## 2412.19509 [keep] MBQ: Modality-Balanced Quantization for Large Vision-Language Models

- 기반 모델: InternVL, InternVL2, LLaVA, LLaVA-onevision, Qwen-VL, Qwen2-VL
- 비교 대상: —
- 하드웨어: A100, RTX 4090, RTX4090
- 벤치마크: MMMU, OCRBench, SEED-Bench, ScienceQA, TextVQA, VizWiz

**BIT** (8)
- Extensive experiments show that MBQ can significantly improve task accuracy by up to 4.4% and 11.6% under W3A16 and W4A8 quantization for 7B to 70B VLMs, compared to SOTA baselines.
- Additionally, we im- plement a W3A16 GPU kernel that fuses the dequantization and GEMV operators, achieving a 1.4× speedup on LLaVA- onevision-7B on the RTX 4090.
- These sensitivity indicators are then incorporated into the reconstruction loss as the objec- tive for searching optimal channel-wise equalization fac- tors [27, 43] in both weight-only (W3A16 and W4A16) and weight-activation quantization (W4A8 and W8A8).
- The results show MBQ significantly improves the task accuracy by up to 4% and 11% under W3A16 and W4A8 quantization com- pared with other SOTA methods.
- For W3A16 quantization, we design a GPU kernel that fuses 3-bit dequantization with general matrix-vector multi- plication (GEMV).

**PARAM** (3)
- For example, the largest LLaVA-onevision VLM, with 72B parameters, requires 144GB of memory, which exceeds the 80GB memory capacity of the A100 GPU.
- For LLaVA-onevision, we select models with 7B and 72B parameters, which uti- lize Qwen2-7B/-72B for the VLM and SigLIP-400M [48] for the ViT encoder.
- For Qwen2-VL, we use models with 7B and 72B parameters in our evaluation, which use Qwen2-7B/-72B for the VLM component and a 675M ViT encoder.

**SPEED** (4)
- Additionally, we im- plement a W3A16 GPU kernel that fuses the dequantization and GEMV operators, achieving a 1.4× speedup on LLaVA- onevision-7B on the RTX 4090.
- The evaluation results show that the fused W3A16 GEMV kernel achieves a speedup of 1.2× to 5.0× across 4 different shapes, compared to the FP16 GEMV baseline.
- In this case, we apply the W4A8 kernel to the ViT encoder and achieve 1.15× speedup.
- However, the W3A16-quantized VLM is 1.23× faster than the W4A8 model.

**MEM** (1)
- For example, the largest LLaVA-onevision VLM, with 72B parameters, requires 144GB of memory, which exceeds the 80GB memory capacity of the A100 GPU.

**ACC** (2)
- The average accuracy loss for RTN-quantized 7B and 8B VLMs is 9.6%, significantly higher than the 1.5% loss seen in VLMs over 26B.
- 5, across three different large VLMs, the proposed MBQ (Rot) under W4A8 quantization exhibits an accuracy loss of less than 1.1% compared to the original FP16 VLMs.


## 2501.01709 [keep] MoVE-KD: Knowledge Distillation for VLMs with Mixture of Visual Encoders

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-NeXT, Mini-Gemini, Qwen-VL
- 비교 대상: —
- 하드웨어: A800
- 벤치마크: GQA, MMBench, MME, POPE, TextVQA, VQAV2, VizWiz


## 2502.00425 [keep] MQuant: Unleashing the Inference Potential of Multimodal Large Language Models via Full Static Quantization

- 기반 모델: InternVL, InternVL2, Internvl2, Mini-Gemini, MiniCPM-V, Qwen-VL, Qwen2-VL
- 비교 대상: —
- 하드웨어: NVIDIA RTX 6000, RTX 6000
- 벤치마크: DocVQA, MME, OCRBench, ScienceQA, TextVQA

**TOK** (1)
- Table 9: Latency combining AIFS with FlashAttention from 100 to 8100 tokens (𝑄/𝐾/𝑉shape is (1, 28, num-tokens, 128)) Tokens Number 100 900 2500 4900 8100 FlashAttn (ms) 27.3 33.6 35.5 165.9 271.6 AIFS+FlashAttn (ms) 27.3 34.1 36.4 167.5 272.1 Integrate AIFS with Flash Attention.

**BIT** (8)
- On five mainstream MLLMs (including Qwen- VL, MiniCPM-V, CogVLM2), MQuant under W4A8 achieves near- floating-point accuracy (<1% degradation) while reducing inference latency by up to 30%, significantly outperforming existing PTQ baselines.
- Quantization has proven an effective strategy for reducing memory usage and inference costs in LLMs [43, 62, 70], by converting high-precision parameters (e.g., FP32) into lower-bit representations (e.g., INT8).
- The extensive results on diverse multimodal reasoning tasks demonstrate that MQuant achieves less than 1% accuracy loss on all MLLMs with 23% and 100% speedup in prefill and decode stage under the W4A8 setting, highlighting its superior performance and wide practical value.
- Generally, when we quantize the network’s weight with 4-bit and activations with 8-bit, called it as W4A8.
- In Quarot, FHT is crucial for low-bit quantization (e.g., 4-bit) as shown in Appendix A.9.

**SPEED** (1)
- AIFS maintains full multi-batch compatibility with- out overhead, enabling consistent 20% faster inference versus FP baselines across batch sizes 1-4 (Table 13). ❷For multi-turn dia- logue, under identical resolution and input format (50 text tokens per turn + 512 decoded tokens), MQuant achieves 38.7% faster end-to- e

**MEM** (1)
- This re- moves the need to recalculate scales per token, cutting runtime overhead and boosting throughput. ❸Enhanced Memory Efficiency: Sequential processing of visual (via 𝑠𝑣) and textual (𝑠𝑡) tokens with dedicated scale factors minimizes memory fragmentation, yielding up to 24.7% speedups and 152.9% memory efficiency

**ACC** (1)
- The extensive results on diverse multimodal reasoning tasks demonstrate that MQuant achieves less than 1% accuracy loss on all MLLMs with 23% and 100% speedup in prefill and decode stage under the W4A8 setting, highlighting its superior performance and wide practical value.


## 2506.07530 [keep] BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation

- 기반 모델: LLaVA, LLaVA-1.5
- 비교 대상: —
- 하드웨어: NVIDIA A100, NVIDIA A800, NVIDIA H800, RTX 3050
- 벤치마크: AI2D, MMMU, SeedBench

**BIT** (8)
- BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation Hongyu Wang Chuyan Xiong Ruiping Wang∗Xilin Chen Key Laboratory of AI Safety, Institute of Computing Technology, Chinese Academy of Sciences University of Chinese Academy of Sciences.
- 1: We introduce BitVLA, the first fully native 1-bit vision-language-action (VLA) model for robotic manipulation, in which every parameter is ternary, i.e., {−1, 0, 1}.
- With the proposed Quantize-then-Distill stage, we compress the full-precision vision encoder to 1.58-bit weights with INT8 activations after multimodal training.
- Thus, we propose BitVLA, a fully native 1-bit VLA model for robotic manipulation, where every parameters is ternary, i.e., {−1, 0, 1}.
- BitVLA is built on the publicly available 1-bit LLM BitNet b1.58 2B4T, and is trained as a vision-language-action policy that inherits the compactness of 1-bit pretraining while retaining strong task performance.

**SPEED** (2)
- Latency 0 200 400 OpenVLA-OFT+ Pi-0 BitVLA 4.4 x Real World 0 20 40 60 80 OpenVLA-OFT Pi-0 BitVLA OOD SFT Memory Usage 0 5 10 15 20 OpenVLA-OFT Pi-0 BitVLA 11 x Reduction Only 1.4G -1 0 +1 Simulation 50 70 90 OpenVLA-OFT Pi-0 BitVLA 0 100 200 300 400 OpenVLA-OFT+ Pi-0 BitVLA Throughput 4.4 x BitVLA Fig.
- Meanwhile, BitVLA requires only 1.4 GB memory and delivers a 4.4× speedup over OpenVLA-OFT.

**LAT** (2)
- BitVLA achieves 73 ms latency and 341.1 Hz throughput, outperforming OpenVLA- OFT+ by 4.4× lower latency and 4.4× higher throughput, and also exceeding π0 in both metrics. only the limited fine-tuning data.
- BitVLA achieves 73 ms latency and 341.1 Hz throughput, substantially outperforming OpenVLA-OFT+ (321 ms, 77.9 Hz) and RDT-1B (297 ms, 84.1 Hz), corresponding to about 4.4× lower latency than OpenVLA-OFT+.

**MEM** (5)
- Meanwhile, BitVLA requires only 1.4 GB memory and delivers a 4.4× speedup over OpenVLA-OFT.
- BitVLA achieves competitive performance with a 1.4 GB memory footprint.
- In practice, BitVLA requires only 1.4 GB of memory, enabling deployment on consumer-grade GPUs, such as the NVIDIA GeForce RTX 3050 Ti Laptop GPU (4 GB).
- As shown in Table III, across the five benchmarks, the 1.58-bit encoder incurs only a 1.5% absolute drop in aver- age accuracy, while reducing the vision encoder’s memory footprint from 0.8 GB to 0.1 GB.
- The Quantize-then-distill stage preserves the multimodal ability while reducing the memory footprint from 0.8GB to 0.1GB.


## 2510.16292 [keep] QSVD: Efficient Low-rank Approximation for Unified Query-Key-Value Weight Compression in Low-Precision Vision-Language Models

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-Next
- 비교 대상: —
- 하드웨어: A6000, CPU, NVIDIA RTX 4070
- 벤치마크: SEED-Bench, SEEDBench, ScienceQA, VizWiz

**BIT** (7)
- We evaluate all performance results on NVIDIA RTX A6000 GPUs using VLMEvalKit [10], and we report results under three weight-activation quantization configurations: W8A8 (8-bit weights and 8-bit activations), W8A4, and W4A4.
- As shown in Table 2, under the W8A8 setting, QSVD consistently outperforms other baselines in most scenarios.
- Under the more aggressive W8A4 setting, QSVD surpasses all baselines and approaches FP16-level performance using as little as 9.38% of the original KV cache.
- Finally, Table 2 shows the quantization results under the W4A4 setting.
- Table 4 presents the impact of the learnable β on VLM accuracy under W4A4 setting over LLaVA 7Bs on Science QA.

**PARAM** (1)
- TinyGPT-V [59] and TinyLLaVA [62] explore efficient designs at smaller scales, while SmolVLM [39] introduces a family of compact models (500M and 2B parameters) that maintain strong performance with much reduced hardware cost.

**SPEED** (2)
- 4.4 Latency Evaluation on VLM 0 5 10 15 FP16 noQ-40% noQ-30% 70% 50% INT8 12.7× 13.1× 9.7× 1× 1.7× 2.1× Speedup Figure 4: Normalized speedup of QSVD-noQ and QSVD W8A8 on low-end GPU.
- However, QSVD-noQ with 40% and 30% (denoted as noQ-40% and noQ-30%) rank retention benefits from reduced data movement enabled by effective SVD compression, achieving up to a 2.1× speedup over the baseline.

**MEM** (1)
- We evaluate inference latency of the layer-wise LLaVA-v1.5 7B on an NVIDIA RTX 4070 GPU with 12GB memory.


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


## 2601.22709 [star] Gated Relational Alignment via Confidence-based Distillation for Efficient VLMs

- 기반 모델: LLaVA, LLaVA-1.5, Qwen2-VL
- 비교 대상: —
- 하드웨어: L40, NVIDIA A100, NVIDIA H100
- 벤치마크: GQA, MMBench, MME, POPE, SEED-Bench, ScienceQA, TextVQA, VQAv2, VizWiz

**BIT** (8)
- Extensive evalu- ations of the LLaVA and Qwen benchmarks show that our INT4 models consistently outperform the BF16 baselines (e.g., LLaVA-1.5-7B: 70.1 vs.
- With real INT4 kernels, we achieve 3× throughput and 54% memory reduction.
- Accuracy Pareto Better Teacher (13B) Baseline (7B) AWQ QAT GRACE (Ours) Pareto Frontier Memory ~4 GB ~14 GB ~26 GB 13B Teacher (BF16) 7B Baseline (BF16) AWQ (4-bit) QAT (4-bit) GRACE (8-bit) GRACE (4-bit) ∼3.0× Throughput +1.3% Acc vs.
- Post-training quantization (PTQ) is at- tractive because it requires little or no retraining (Frantar et al., 2022; Shao et al., 2023; Lin et al., 2024), but aggres- sive INT4 quantization often causes severe degradation in VLMs due to heterogeneous multimodal distributions and cross-modal sensitivity (Wang et al., 202
- More importantly, as shown in Figure 1, our INT4 Qwen2-VL-2B not only recovers but surpasses the full- precision baseline across all benchmarks, such as 79.1 vs.

**MEM** (1)
- Accuracy Pareto Better Teacher (13B) Baseline (7B) AWQ QAT GRACE (Ours) Pareto Frontier Memory ~4 GB ~14 GB ~26 GB 13B Teacher (BF16) 7B Baseline (BF16) AWQ (4-bit) QAT (4-bit) GRACE (8-bit) GRACE (4-bit) ∼3.0× Throughput +1.3% Acc vs.


## 2603.04800 [keep] MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models

- 기반 모델: Qwen2.5-VL
- 비교 대상: —
- 하드웨어: RTX 4090
- 벤치마크: MMMU, OCRBench, ScienceQA, TextVQA, Vizwiz

**BIT** (8)
- We use WxAy nota- tion for x-bit weights and y-bit activations, with two main types: weight-only quantization (e.g., W4A16) and weight- activation quantization (e.g., W8A8, W4A8).
- What brand is in white letters with a red background? "Answer the question using a single word." ×" Text serves as the dominant modality Vision serves as the dominant modality Text Tokenizer Vision Encoder Audio Encoder !(#!$) $ MBR Loss # !('/#) Channel-wise Smoothing Modality Balance Reconstruction Fox ' SQNR = 5.31 
- 0 10 20 30 Transformer Layer Index 0 5 10 15 20 SQNR (dB) Unified Smoothing (W4A8) Optimal Smoothing (W4A8) Unified Smoothing (W4A6) Optimal Smoothing (W4A6) Unified Smoothing (W4A4) Optimal Smoothing (W4A4) Figure 2.
- MASQuant matches FP16 performance on both model sizes at W8A8, suggesting that MLLMs can be quantized to 8 bits without accuracy loss when modality-specific charac- teristics are properly handled.
- RTN completely fails on W4A8, while SmoothQuant severely degrades.

**SPEED** (1)
- Table 7 shows that MASQuant achieves a 2.5x speedup over FP16 with marginal latency overhead (5– 10%) compared to MBQ, while maintaining identical de- coding latency.


## 2603.17809 [keep] Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients

- 기반 모델: InternVL, InternVL2, LLaVA, LLaVA-onevision, Qwen2-VL
- 비교 대상: —
- 하드웨어: A800, NVIDIA A800
- 벤치마크: AI2D, ChartQA, MMMU, ScienceQA, VizWiz

**FREE** (2)
- By applying weight-only or weight-activation quantization, it reduces memory usage and computation overload while minimiz- ing reconstruction error with a small calibration set, thereby maintaining task performance and achieving strong accu- racy–efficiency trade-offs in a training-free manner.
- Notably, the modification requires no additional calibration data and incurs negligible computation overhead, making it a plug-and-play enhancement to standard GPTQ.

**BIT** (8)
- Extensive experiments on multiple LVLMs under both W4A8 and W3A16 settings show that our method improves accu- racy across models and benchmarks with negligible la- tency overhead.
- For example, under 3-bit weight-only quantization, our method improves the average accuracy of LLaVA-onevision-7B by 1.60%, reducing the gap to its full- precision counterpart to only 1.33%.
- For example, under 3-bit weight-only quantiza- tion, our method improves the average accuracy of LLaVA- onevision-7B by 1.60%, reducing the gap to its full- precision counterpart to only 1.33%.
- For example, W4A8 de- notes quantizing weights to 4 bits and activations to 8 bits.
- Comparison of modality-level and token-level sensitivity estimation strategies on VizWiz (W4A8, InternVL2-8B).

**ACC** (1)
- Under the W4A8 configuration, our approach re- covers most of the FP16 accuracy, keeping the performance drop within 3% on all benchmarks.


## 2604.24380 [keep] Structural Pruning of Large Vision Language Models: A Comprehensive Study on Pruning Dynamics, Recovery, and Data Efficiency

- 기반 모델: InternVL, LLaVA
- 비교 대상: PruMerge
- 하드웨어: —
- 벤치마크: AI2D, DocVQA, GQA, MME, MMMU, MathVista, POPE

**FREE** (2)
- This strategy allows customizable model sizing and performance tuning without retraining from scratch.
- For instance, LLaVA- PruMerge [47] utilizes a dynamic approach of token pruning and merging for adaptive compres- sion, while CoViPAL [48] introduces a model- agnostic plug-and-play module for token pruning.

**BIT** (4)
- Crucially, these benchmarks span a wide range of prompt formats, requiring the mod- els to adapt to multiple-choice questions (e.g., MMMU, SQA, AI2D), binary Yes/No classifica- tion (e.g., POPE, MME), and open-ended free generation (e.g., MathVista, DocVQA, GQA).
- Using LLM.int8() [71] as a representative method, Table 7 shows that applying quantization to our already-pruned models yields compound memory savings.
- First, we focused exclusively on structured pruning for hardware universality; we did not investigate unstructured or semi-structured methods [8, 9], which rep- resent an orthogonal direction for compression Table 7 Memory usage and average performance of LLaVA-v1.5-7B when combining structural pruning (layerwise) and 
- Model Memory Ratio Avg (GiB) LLaVA-7B 13.2 0% 53.7 LLaVA-7B.int8() 7.5 0% 52.5 LLaVA-6B 11.3 15% 52.68 LLaVA-6B.int8() 6.5 15% 51.9 LLaVA-5B 9.4 30% 51.75 LLaVA-5B.int8() 5.4 30% 50.8 requiring different hardware considerations.

**PARAM** (2)
- Through empirical study on three represen- tative LVLM families ranging from 3B to 7B parameters, this study offers actionable insights for practitioners to compress LVLMs without extensive computation resources or sufficient data.
- For LLaVA-v1.5- 7B models compressed by up to 45% (retain- ing approximately 3.8B parameters), the results 14 Table 6 Qualitative analysis of compressed LLaVA-v1.5-7B models following our established insights.

**LAT** (1)
- For exam- ple, on LLaVA at 30% compression, layerwise pruning achieves a latency of 80.7 ms, compared to 84.4 ms for widthwise pruning.

**ACC** (5)
- Notably, effective recovery can be achieved using just 5% of the original data, while retaining over 95% of the original performance.
- For example, at a 15% ratio, LLaVA retains 90.87% of its performance with widthwise prun- ing, compared to only 72.22% with layerwise pruning.
- At a low compression ratio of 15%, multimodal performance drops sig- nificantly (9.13%) while text-only performance remains largely intact (1.07% degradation).
- Even at a severe compression ratio of 60%, projector SFT recovers 60–80% of the original performance by re-aligning the visual features with the pruned language model.
- At 45% compres- sion, the retained performance for LLaVA and InternVL drops to 83.99% and 86.22%, respec- tively, falling below the 90% fidelity threshold.

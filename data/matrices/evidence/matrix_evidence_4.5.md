# 비교 매트릭스 근거 — 4.5 (16편)


## 2407.11771 [keep] XEdgeAI: A Human-centered Industrial Inspection Framework with Data-centric Explainable Edge AI Approach

- 기반 모델: —
- 비교 대상: —
- 하드웨어: iPhone 11 
- 벤치마크: —

**BIT** (1)
- We considerably reduce the model size by quantizing these layers’ parameters to 8-bit integers using the dynamic quantization function from Py- Torch, making it more suitable for deployment on devices with limited storage and processing capabilities.


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


## 2504.14239 [keep] InfiGUI-R1: Advancing Multimodal GUI Agents from Reactive Actors to Deliberative Reasoners

- 기반 모델: BLIP-2, LLaVA, Qwen-VL, Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: NVIDIA H800
- 벤치마크: —

**PARAM** (1)
- Our Ac- tor2Reasoner framework, combining Spatial Reasoning Distillation and RL-based Deliberation Enhancement (Sub-goal Guidance, Er- ror Recovery), successfully transforms a base MLLM into a more effective Deliberative Reasoner, achieving state-of-the-art among models with similar parameter counts in trajectory-based


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


## 2509.21259 [keep] Semantic Edge-Cloud Communication for Real-Time Urban Traffic Surveillance with ViT and LLMs over Mobile Networks

- 기반 모델: BLIP-2, LLaVA, LLaVA-1.5, LLaVa
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**FREE** (1)
- On the other hand, LoRA provides a quick way to adapt the model without retraining it.

**BIT** (8)
- The second encoding scheme is IEEE 754 Format, where each float32 type value, V, of embedding is converted into a 32-bit binary representation using the IEEE 754 standard, consisting of 1 sign bit, S, 8 exponent bits, E, and 23 fraction bits, M, also referred to as the mantissa.
- 2) Modulation Scheme and Communication Channel: We have considered two modulation schemes: Binary Phase shift Keying (BPSK) and 16-Quadrature Amplitude Modulation (16-QAM).
- Alternatively, if each element in the bitstream is a 32- bit IEEE 754 representation of a floating-point value, the reconstruction is done using a binary-to-float conversion that follows the IEEE 754 standard.
- In Figures 8, the performance of Quantization encoding is evaluated using 8-bit, 16-bit, and 32-bit precision levels.
- Even 8-bit quantization maintains low MSE at higher SNR values, resulting in further reducing the transmission data size and bandwidth saving.

**PARAM** (2)
- LLaMA 3.2-11B Vision-Instruct represents a state-of- the-art instruction-tuned vision–language model with a large 11B parameters for high-quality reasoning, while LLaVA 1.5 7B is a smaller, widely used multimodal model with lower computational requirements, making it suitable for resource- constrained environments.
- LLaVA 1.5 with 7B and LLaMA 3.2 with 11B parameters are compared in table III.

**LAT** (1)
- For each frame, Region of Interest (RoI) extraction requires 0.023 seconds, embedding generation using a ViT takes 0.16 seconds, and image reconstruction through a custom decoder incurs a negligible latency of 1×10−3 seconds.

**MEM** (7)
- Moreover, in order to run LLaMA with proper efficiency, 24 GB VRAM is required, and it is 14.2 GB in the LLaVA 1.5 model.
- On the other hand, each RoI area, cropped from the overall images is 224x224 RGB square image form that consumes around 0.14 MB, so the total memory consumption from 1 camera image, after cropping the highlighted parts, is Nx0.14 MB, where N is the total number of cars located by the YOLOv11 model.
- Furthermore, each image embedding representation is formed into a 1×768 float32 type vector data structure and occupies much less memory, around 29x10−4 MB, and just like cropped images, the total memory requirement is Nx29x10−4 MB for transmitting the embedding representation of one image frame to the cloud.
- Among the evaluated methods, the cropped image-based approach achieves memory savings ranging from approximately 93% to a peak of 98.5%.
- In contrast, converting cropped images into embedding vectors offers a consistent memory saving of around 99.9% across all cases.

**ACC** (1)
- However, this extreme compression introduced a modest accuracy drop to 89%, highlighting the inherent trade-off that greater bandwidth savings come at the expense of a slight reduction in model performance.


## 2510.25122 [keep] NanoVLA: Routing Decoupled Vision-Language Understanding for Nano-sized Generalist Robotic Policies

- 기반 모델: —
- 비교 대상: —
- 하드웨어: Jetson Orin, Jetson Orin Nano, Jetson Orin Nano 
- 벤치마크: —

**BIT** (3)
- We train a text-conditioned binary classifier fθ on serialized inputs (l, i, j) to predict Pr(i ≻j | l).
- The win probabilities provide soft, calibrated supervision targets for training a text-conditioned binary classifier fθ to predict Pr(i ≻ j | l).
- It’s 1Note that even 4-bit OpenVLA will result in out-of-memory, we report the frames per second (FPS) of OpenVLA using the data from the 4-bit Llama2 model, which is the text backbone of OpenVLA 8 Under review also more flexible in real-world deployment as it only need to train once.

**PARAM** (5)
- This approach does enables better per- formance with less overhead and latency, which informs NanoVLA, small scale VLA that achieves better performance across both simulation and real-world tasks with only ∼2% of the parameter of models like OpenVLA, as shown in the Radar plot (right).
- RT-1 (Brohan et al., 2022) pioneered the generalist robotic models with only 35M parameters.
- NanoVLA shows significant performance gains, with improvements ranging from 6.0% to 12.3% in average success rates while only using less than 10% total parameters.
- Especially, the proposed NanoVLA-R can further improve the precision by 3.7% while reducing 43% of the parameters of OpenVLA-L.
- Notably, in easier pick-place tasks, NanoVLA-S (161M parameters) can even outperform OpenVLA (7B parameters), which has 43.5x more parameters.

**SPEED** (1)
- Experimental results on several bench- marks, as well as real-world deployments, demonstrate that NanoVLA achieves up to 52x faster inference on edge devices compared to previous state-of-the-art VLA models, with 98% less parameters while maintaining or surpassing their task accuracy and generalization.

**MEM** (1)
- 4.3 INFERENCE LATENCY ANALYSIS To validate the effectiveness of the edge-side deployment for NanoVLA family, we deployed them on the Jetson Orin Nano Super Developer Kit, which has 8GB memory with CUDA support and a computation performance for up to 67 TOPS.

**THR** (2)
- 0 5 10 15 20 25 30 35 FPS 75 80 85 90 95 100 SR OpenVLA 7.5B SmolVLA 0.45B NanoVLA-S 0.161B NanoVLA-L 0.52B NanoVLA-R 0.296B NanoVLA-AC50 0.296B (a) Inference performance.
- 0 20 40 60 80 100 Steps 10 20 30 40 FPS FPS Long-short AC Fixed AC 70 80 90 SR (b) Long-short AC ablation.


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


## 2607.13429 [keep] Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment

- 기반 모델: Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: GQA

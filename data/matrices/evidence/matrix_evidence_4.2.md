# 비교 매트릭스 근거 — 4.2 (16편)


## 2401.02797 [keep] PeFoMed: Parameter Efficient Fine-tuning of Multimodal Large Language Models for Medical Imaging

- 기반 모델: LLaVA
- 비교 대상: —
- 하드웨어: A40
- 벤치마크: —

**BIT** (1)
- Particularly in MRG tasks, where the generated content is rel- atively lengthy, using a binary rating may not be ideal.

**PARAM** (1)
- Besides, it is worth highlighting that with the adoption of parameter- efficient fine-tuning, our model featured notably fewer trainable parameters (56.63M) in comparison to LLaVA-Med (7B parameters), which made our method a significantly more efficient framework for fine-tuning MLLMs. b.

**MEM** (1)
- 4.2 Implementation Details All experiments were carried out using Python 3.9 on 4 NVIDIA Tesla A40 GPUs, each with 48GB of GPU memory.


## 2401.16420 [star] InternLM-XComposer2: Mastering Free-form Text-Image Composition and Comprehension in Vision-Language Large Model

- 기반 모델: BLIP-2, IDEFICS, LLaVA, LLaVA-1.5, Qwen-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, ChartQA, GQA, MMBench, MME, MMMU, MathVista, POPE, SEED-Bench, VQAv2

**PARAM** (3)
- The InternLM- 1 arXiv:2401.16420v1 [cs.CV] 29 Jan 2024 XComposer2 model series with 7B parameters are pub- licly available at https://github.com/InternLM/ InternLM-XComposer.
- Our InternLM-XComposer2 gets SOTA results in 6 of the 12 benchmarks with only 7B parameters, showing competitive results with current closed-source APIs and previous open-source SOTA MLLMs.
- Meanwhile, despite having only 7B parameters, our model attains a slightly worse score of 43.0% on the challenging college-level benchmark MMMU.


## 2402.09353 [star] DoRA: Weight-Decomposed Low-Rank Adaptation

- 기반 모델: LLaVA, LLaVA-1.5
- 비교 대상: —
- 하드웨어: —
- 벤치마크: GQA, MMBench, POPE, VQAv2

**BIT** (2)
- To further decrease the memory demands of finetuning, QLoRA (Dettmers et al., 2023) suggests quan- tizing the pretrained model to 4-bit and finetuning LoRA on top of the frozen low-bit backbone.
- In addition to the fine-tuned models, they also reported results from zero-shot, few-shot, and FT with post-training quantization (PTQ), where the FT model is quantized to the BnB NF4 format after training.

**MEM** (1)
- The results indicate that the modification leads to a training memory reduction of approximately 24.4% in fine-tuning LLaMA and 12.4% in VL-BART.


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


## 2405.18541 [keep] Low-Rank Few-Shot Adaptation of Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: A100
- 벤치마크: —


## 2406.11909 [keep] Mixture-of-Subspaces in Low-Rank Adaptation

- 기반 모델: LLaVA, LLaVA-1.5
- 비교 대상: —
- 하드웨어: A100, Nvidia A100
- 벤치마크: AI2D, GQA, MMBench, MME, MMbench, MathVista, POPE, TextVQA, VQAv2

**BIT** (2)
- For InternLM2, we employ the 4-bit QLoRA on LoRA and MoSLoRA.
- Moreover, MoSLoRA also outperforms LoRA when combined with the 4-bit QLoRA.


## 2407.03056 [keep] Improving Zero-shot Generalization of Learned Prompts via Unsupervised Knowledge Distillation

- 기반 모델: —
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**FREE** (1)
- For class agnostic settings we instead use the suffix +CA-KDPL to indicate that no training class names are used.

**FLOP** (2)
- Lightweight CLIP models based on ResNet-50 and ViT-B/32 require about 18 and 14 GFLOPs for inference, respectively.
- In contrast, more powerful models based on ViT-H/14 [10,18] require nearly 30× the computation at 381 GFLOPs [18] for inference.

**MEM** (1)
- According to Ren et al. [46], CoOp requires nearly 15MB of VRAM per class, resulting in approximately 300GB of memory when Improving Learned Prompts via Unsupervised Knowledge Distillation 9 multiplied by 20K classes.


## 2407.03320 [keep] InternLM-XComposer-2.5: A Versatile Large Vision Language Model Supporting Long-Contextual Input and Output

- 기반 모델: InternVL, InternVL1., LLaVA, Qwen-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: AI2D, ActivityNet, ChartQA, DocVQA, GQA, MLVU, MMBench, MME, MMMU, MVBench, MathVista, OCRBench, RealWorldQA, SEED-Bench, TextVQA, VQAv2

**PARAM** (1)
- IXC-2.5 with only 7B parameters performs on par with the current large open-source LVLMs and close-source APIs.


## 2411.15232 [keep] BiomedCoOp: Learning to Prompt for Biomedical Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA A100
- 벤치마크: —


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


## 2605.06175 [keep] VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA A100
- 벤치마크: AI2D, DocVQA, MMMU, OCRBench, RealWorldQA

**PARAM** (2)
- Among the 4,551.85M total model parameters, we freeze 4,437.82M non-GSE parameters from the base VLM and optimize only 114.04M parameters (2.51% of the full model).
- Specifically, the trainable parameters consist of 48.41M parameters in the GSE modules and 65.62M parameters in the action head.

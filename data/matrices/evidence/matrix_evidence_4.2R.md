# 비교 매트릭스 근거 — 4.2R (12편)


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


## 2404.01959 [keep] Bi-LORA: A Vision-Language Approach for Synthetic Image Detection

- 기반 모델: BLIP2, Llava
- 비교 대상: —
- 하드웨어: CPU
- 벤치마크: —

**BIT** (8)
- The pivotal conceptual shift in our methodology revolves around reframing binary classification as an image captioning task, leveraging the distinctive capabilities of cutting-edge VLM, notably bootstrapping language image pre-training (BLIP)2.
- To tackle this discrepancy, a seemingly direct approach is to train a binary classifier using CNNs or transformer-based models to distinguish diffusion-generated images from genuine ones.
- To the best of our knowledge, this work pioneers the concept of treating binary classification as image captioning, harnessing cutting-edge VLMs.
- Instead of binary classification, we emphasize the potential of using VLMs (e.g., BLIP2) to create informative captions indicating class membership.
- Local features are extracted from these selected patches and integrated with the global representation using an attention-based module for final binary classification.


## 2404.04883 [keep] Mixture of Low-rank Experts for Transferable AI-Generated Image Detection

- 기반 모델: —
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**BIT** (2)
- Using only binary cross-entropy loss Lbce can lead to severe load imbalance, where Wg collapses such that almost all the inputs are assigned to the same expert.
- We also visualize the variation of binary cross-entropy loss during training for the variants (b), (d), and (e) in Figure 8 (Supplementary Ma- terial), which shows that integrating both shared and sepa- rate adapters contributes to the model converging towards a globally better optimum.

**PARAM** (1)
- Besides, the training process is computa- tionally efficient and resource-friendly as only 0.08% of the parameters are optimized.


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


## 2406.13807 AlanaVLM: A Multimodal Embodied AI Foundation Model for Egocentric Video Understanding
(전문 없음)


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


## 2407.05342 [keep] Mind the Interference: Retaining Pre-trained Knowledge in Parameter Efficient Continual Learning of Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA 3090
- 벤치마크: —

**FREE** (1)
- Its residual property facilitates knowledge acquisition and reduces noise, enhancing existing works plug-and-play.

**PARAM** (1)
- Experiments show that DIKI surpasses the previous SOTA method with only 0.86% trainable parameters.


## 2411.15232 [keep] BiomedCoOp: Learning to Prompt for Biomedical Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA A100
- 벤치마크: —


## 2505.23271 [keep] LADA: Scalable Label-Specific CLIP Adapter for Continual Learning

- 기반 모델: —
- 비교 대상: —
- 하드웨어: NVIDIA 4090
- 벤치마크: —


## 2508.06202 [keep] LoRA in LoRA: Towards Parameter-Efficient Architecture Expansion for Continual Visual Instruction Tuning

- 기반 모델: LLaVA, Qwen2-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: GQA, ScienceQA, TextVQA, VQAv2

**FREE** (1)
- However, real-world applications increasingly demand that MLLMs continually acquire new capabilities without retraining from scratch.

**BIT** (1)
- MIF is defined as: MIFk = 1 k k X j=1 1 n n X i=1 Bj(oj i) ! , (11) where B() is a binary function that returns 1 if the model output oj i satisfies the instruction format of the j-th task, and 0 otherwise. n denotes the number of evaluation samples.

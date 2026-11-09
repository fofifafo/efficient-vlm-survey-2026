# 비교 매트릭스 근거 — 4.4 (19편)


## 2403.06764 [keep] An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models

- 기반 모델: LLAVA, LLaVA, LLaVA-1.5, Qwen-VL, Video-LLaVA
- 비교 대상: FastV
- 하드웨어: A40
- 벤치마크: MME, MMMU, MSRVTT, MSVD, SeedBench

**FREE** (4)
- FastV An Image is Worth 1/2 Tokens After Layer 2: Plug-and-PLay Acceleration for VLLM Inference Liang Chen1, Haozhe Zhao1, Tianyu Liu2†, Shuang Bai2, Junyang Lin2 Chang Zhou2, Baobao Chang1† 1National Key Laboratory for Multimedia Information Processing, Peking University 2Alibaba Group [email removed] Abstr
- Propose FastV, a plug-and-play method to significantly reduce inference cost for LVLMs without sacrificing performance inspired by our observation.
- FastV is plug-and-play to different token-based LVLMs for various vision language tasks without the need of training the model.
- 6 Conclusion In this paper, we propose FastV, a plug-and-play inference cost optimization method for Large Vision-Language Models.

**TOK** (3)
- For instance, LLAVA process 336x336 images into 576 tokens Liu et al. (2023b) and process images with a greater resolution of 672x672 into 2304 tokens Liu et al. (2024b).
- Fuyu Bavishi et al. (2023), in a similar vein, translates pixel-level images of 1080x1080 into 1296 tokens.
- Model Nocaps Flickr30k A-OKVQA MMMU LLaVA1.5-7B (Retrained) 100.3 70.2 78.5 34.5 (a) w/ Train with 50% image tokens 98.5 68.5 76.8 33.5 (b) w/ FastV (K=2, R=50%) 100.1 70 78.4 34.6 (c) w/ FastV (K=2, R=50%, Random) 99.5 68.3 78.2 34.2 (d) w/ FastV (system prompt) 89.2 64.3 69.2 33.8 (e) w/ FastV (prune first half syste

**SPEED** (1)
- Our evaluations demonstrate FastV’s ability to dramatically reduce computational costs (e.g., a 45% reduction in FLOPs for LLaVA-1.5- 13B) without sacrificing performance in a wide range of image and video understanding tasks.

**FLOP** (4)
- We can see that FastV can achieve 45% FLOPs reduction with nearly no performance loss for different models. †Corresponding author.
- Transformer Block K Transformer Block K+1 FastV Re-rank & Filtering R% Image Tokens Transformer Block K+2 … 8s Text Tokens No FastV 100% FLOPs FastV(K=2, R=50%) 52% FLOPs FastV(K=2, R=75%) 33% FLOPs FastV(K=5, R=75%) 38% FLOPs The video is funny because the baby is trying to read a book while sitting on the bed, and he
- 0.0 0.25 0.5 0.75 1.0 R Values 0 5 10 15 20 25 30 K Values 0.0 0.2 0.4 0.6 0.8 FLOPs reduction ratio Figure 6: The heat map of theoretical FLOPs reduction ratio.
- The results indicate that FastV (K=2, R=50%) could achieve about 45% FLOPs reduction for different LVLMs without sacrificing the performance.


## 2403.18293 [keep] Efficient Test-Time Adaptation of Vision-Language Models

- 기반 모델: —
- 비교 대상: —
- 하드웨어: RTX 6000
- 벤치마크: —

**FREE** (8)
- We design TDA, a training-free dynamic adapter that enables effective and efficient test- time adaptation with vision-language models.
- Backpropagation Learnable Prompt + Image Encoder Text Encoder Selection Augmented Test Images CLIP Predictions Prediction Cat Panda Dog Class Bird (a) Test-time Prompt Tuning [9, 35] + Image Encoder Text Encoder Test Image Adapted Prediction CLIP Prediction Values Dynamic Adapter Keys Update Cat Panda Dog Class Bird Ha
- Comparison of our proposed Training-free Dynamic Adapter (TDA) with Test-time Prompt Tuning TPT [35] and its enhancement DiffTPT [9]: both TPT and DiffTPT require signif- icant computational resources to optimize the learnable prompt via backpropagation; TDA is a dynamic cache that is training- free without any backpro
- We design a training-free dynamic adapter (TDA) that allows efficient and effective test-time adaptation of vision- language models without requiring any backpropagation in test time.
- First, we design a training-free dynamic adapter (TDA) that can achieve test-time adaptation of vision-language models efficiently and effectively.


## 2406.18139 [keep] LOOK-M: Look-Once Optimization in KV Cache for Efficient Multimodal Long-Context Inference

- 기반 모델: InternVL, LLaVA
- 비교 대상: FastV, LLaVA-Prumerge, LOOK-M, Prumerge
- 하드웨어: NVIDIA A100, RTX 3090
- 벤치마크: —

**FREE** (1)
- FastV (Chen et al., 2024) introduces a versatile plug-and-play method that optimizes computational efficiency through adaptive atten- tion patterns in early layers and visual token prun- ing in later stages, achieving up to a 45% reduc- tion in computational costs while preserving perfor- mance.

**SPEED** (1)
- LOOK-M demonstrates that with a significant reduction in KV Cache memory usage, such as reducing it by 80% in some cases, it not only achieves up to 1.5x faster decoding but also maintains or even enhances performance across a variety of long context multimodal tasks.

**LAT** (1)
- Method Budge Decoding Latency GPU Memory Full Cache 100% 28.16 ms/token 1.52 GiB LOOK-M 20% 20.98 ms/token 0.32 GiB LOOK-M 5% 18.22 ms/token 0.13 GiB As we can observe from Table 4, the decoding latency of our compressed model is significantly lower than that of the model retaining the full cache, with the advantage be

**MEM** (5)
- LOOK-M demonstrates that with a significant reduction in KV Cache memory usage, such as reducing it by 80% in some cases, it not only achieves up to 1.5x faster decoding but also maintains or even enhances performance across a variety of long context multimodal tasks.
- Compared to baselines, LOOK-M achieves minimal performance drop with a fixed KV cache budget and improves the model inference decoding latency by 1.3x to 1.5x and re- duces KV Cache memory footprint by 80% to 95% while still maintaining performance on long con- text multimodal tasks, and even showing improved performan
- As depicted in Figure 5, LOOK-M approaches Full Cache performance even with an extreme KV cache compression of 5%, especially using the text- prior pivotal merging strategy.
- Method Budge Decoding Latency GPU Memory Full Cache 100% 28.16 ms/token 1.52 GiB LOOK-M 20% 20.98 ms/token 0.32 GiB LOOK-M 5% 18.22 ms/token 0.13 GiB As we can observe from Table 4, the decoding latency of our compressed model is significantly lower than that of the model retaining the full cache, with the advantage be
- Additionally, we analyzed the speed and GPU memory usage of the KV Cache under two budget scenarios: 20% and 5%, based on the mean values from the inference process of 20 ran- domly sampled data points (as illustrated in Table 4, Our findings indicate that the average GPU mem- ory consumption is nearly proportional to 


## 2409.10197 [keep] Fit and Prune: Fast and Training-free Visual Token Pruning for Multi-modal Large Language Models

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-NEXT
- 비교 대상: FastV, FitPrune, ToMe
- 하드웨어: A100
- 벤치마크: GQA, MMBench, MME, POPE, ScienceQA, TextVQA, VQAv2, VizWiz, Vizwiz

**FREE** (6)
- Fit and Prune: Fast and Training-free Visual Token Pruning for Multi-modal Large Language Models Weihao Ye12, Qiong Wu12, Wenhao Lin12, Yiyi Zhou12* 1Key Laboratory of Multimedia Trusted Perception and Efficient Computing, Ministry of Education of China, Xiamen University, 361005, P.R.
- In this paper, we propose a novel and training-free approach for the effective visual token prun- ing of MLLMs, termed FitPrune, which can quickly produce a complete pruning recipe for MLLMs according to a pre- defined budget.
- To this end, we question that “Can we find a solution that can directly determine the optimal pruning recipe for MLLMs?” To approach this target, we propose an effective and training-free pruning method for MLLMs, termed Fit and Prune (FitPrune).
- Some recent approaches explore training-free token pruning (Fayyaz et al.
- In this paper, we focus on a training-free and cost-effective method to quickly determine the pruning recipe based on the predefined target.

**TOK** (2)
- For in- stance, dropping about 75% tokens at the 28-th layer will not result in performance loss.
- For in- stance, pruning 50% tokens after the 4-th layer results in a 3.2% performance drop.

**BIT** (7)
- In this case, the final pruning strategy P can be denoted by P = [t∗ 1, t∗ 2, · · · , t∗ K]. (6) Lastly, the optimization of FitPrune in Eq.1 can be refor- mulated as arg min P [d(DS, D′ S) + d(DC, D′ C)] , s.t. Φ (G, P)) ≤δ. (7) To accomplish the objective of Eq.7, we adopt the princi- ple of binary search to obtain t
- Then, we employ binary search to determine the smallest divergence upper bound α.
- The binary search is initialized with αL = 0 as the left boundary (no divergence) and αR = 1 as the right bound- ary (maximum divergence).
- In each iteration of the binary search, the midpoint α = (αL+αR)/2 is evaluated.
- Then, the number of pruned tokens in i-th layer can be calculated by: t∗ i = |Ti|, where Ti = TS ∩TC. (11) This iterative process continues by checking whether Φ(G, P) meets the target computation budget δ after each iteration, and accordingly adjusting the binary search bound- aries αL and αR.

**FLOP** (4)
- The experi- mental results show that our FitPrune can not only reduce the computational complexity to a large extent, while retain- ing high performance, e.g., -54.9% FLOPs for LLaVA-NEXT with only 0.5% accuracy drop.
- 2023d) for diverse percep- tion and reasoning tasks, MMBenchCN for Chinese language 20 30 40 50 60 FLOPs Reduction (%) 75 77 79 Test Accuracy (%) baseline FitPrune FastV ToMe (a) VQAv2 20 30 40 50 60 FLOPs Reduction (%) 56 58 60 62 Test Accuracy (%) baseline FitPrune FastV ToMe (b) GQA 15 25 35 45 55 FLOPs Reduction (%
- For instance, when decreasing 40% FLOPs from visual tokens in statistic, FitPrune decreases computation overhead by 33.2% on average without dropping perfor- mance.
- When defining a pruning ratio of 60% FLOPs, our FitPrune reduces the overall computation overhead of LLaVA-NEXT by 55%, with only 0.3% drop for VQAv2.

**ACC** (2)
- For example, with a 20% pruning ratio on the GQA dataset, ToMe experiences only a 0.2% performance drop, and FastV shows a 0.4% reduction, while FitPrune maintains its performance without any degradation.
- For instance, when the pruning ratio is 80%, the average divergence of the self-attention and cross-attention distributions compared to the original distributions reaches approximately 27%, leading to a performance drop of 3.6%.


## 2410.04417 [keep] SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference

- 기반 모델: LLaVA, LLaVA-1.5, Mini-Gemini, MiniGemini, Qwen2-VL, Video-LLaVA, mini-Gemini
- 비교 대상: FastV, SparseVLM, ToMe
- 하드웨어: NVIDIA A100
- 벤치마크: ActivityNet, GQA, MMBench, MME, MSRVTT, MSVD, POPE, SEED-Bench, TextVQA, Textvqa, VQAv2, Vizwiz

**FREE** (6)
- Differently, we propose a text- guided training-free token optimization mecha- nism dubbed SparseVLM that eliminates the need of extra parameters or fine-tuning costs.
- In this paper, we introduce a text-guided training-free frame- work dubbed SparseVLM for efficient vision language model inference.
- It can act as a plug-and-play module to improve the efficiency of VLMs without additional fine-tuning.
- To the best of our knowledge, it is the first training-free approach that explores text-aware guidance for efficient VLM inference. • Particularly, we propose a strategy to select relevant text tokens as raters of visual tokens, a method to assess the significance of visual tokens followed by pruning of redundant visua
- Furthermore, we also compare the recent method PDrop (Xing et al., 2025) training-free version, which has lower FLOPs computation.

**TOK** (6)
- For example, LLaVA typically encodes 336 × 336 images into 576 tokens (Liu et al., 2024b) with up to 672 × 672 max- imum resolution using 2880 token sequences (Liu et al., 2024a).
- Similarly, mini-Gemini-HD (Li et al., 2024c) con- verts 1536 × 1536 high resolution and 672 × 672 low reso- lution images into 2880 visual tokens.
- When pruning from 576 to 192 tokens, the SparseLLaVA only decreases the average accuracy by 0.9% without additional training and exceeds ToMe (Bolya et al., 2023) 10.2%.
- In Table 2, when 54.5% of vision tokens are removed, Qwen2-VL maintains an accuracy of 98.0%.
- The original number of video tokens is 2048, while our experiment collectively prunes it down to 194 tokens.

**SPEED** (1)
- Experiments demonstrated that e.g. the LLaVA when equipped with Spar- seVLM achieved 37.0% reduction in latency with a compres- sion ratio of 77.8% while maintaining 97% of the original accuracy.

**MEM** (1)
- Additionally, SparseVLM saves 67% cache memory compared to vanilla LLaVA (where 302.4MB is reduced to 100.8MB), while keeping 99.1% accuracy.

**ACC** (5)
- For instance, LLaVA (Liu et al., 2024b) when armed with SparseVLM achieves a 4.5× compression rate while maintaining 97% of its original performance.
- Furthermore, for every 100 tokens pruned, the accuracy only drops by approximately 0.8%.
- Compared to the baseline model, SparseVLM achieves a significant reduction of 43.1% in CUDA time and 62.8% in FLOPs while keeping 96.7% accuracy.
- Additionally, SparseVLM saves 67% cache memory compared to vanilla LLaVA (where 302.4MB is reduced to 100.8MB), while keeping 99.1% accuracy.
- Experiments demonstrated that e.g. the LLaVA when equipped with Spar- seVLM achieved 37.0% reduction in latency with a compres- sion ratio of 77.8% while maintaining 97% of the original accuracy.


## 2410.17434 [keep] LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding

- 기반 모델: BLIP-2, InternVL2, LLaVA, LLaVA-NeXT, LLaVA-OneVision, Video-LLaVA
- 비교 대상: —
- 하드웨어: NVIDIA H100
- 벤치마크: EgoSchema, MLVU, MVBench, VideoMME

**TOK** (6)
- For instance, 576 ∼2,880 tokens per image are used in LLaVA-1.6 (Liu et al., 2024b) and 7,290 tokens are used in LLaVA-OneVision (Li et al., 2024a).
- However, a commonly used and computationally manageable context length for multimodal training is 8k, which limits processing 125 frames (2-minutes video) even at 64 tokens per frame, while an hour-long video could require over 200k tokens.
- When applying uniforming sampling, 144 tokens per frame shows better performance than 64 tokens in an 8k context length on VideoMME (Fu et al., 2024) and MLVU Zhou et al. (2024) while worse on EgoSchema Mangalam et al. (2024).
- With 144 tokens per frame, it preserves more visual details, but restricts the total number of frames, i.e., less than 60 frames within 8k context length.
- We apply text-guided frame selection after temporal reduction, where relevant frames are maintained at full token capacity (144 tokens), while others are reduced to 64 tokens.

**THR** (4)
- As a result, our model is capable of processing 1fps sampled video input with high performance, which can adaptively reduce the number of tokens per frame to 2 on average to accommodate an hour-long video for MLLM within 8k context length.
- Our work focuses on maximizing the preservation of frames in video content (1fps) within given context length by proposing spatiotemporal compression of video tokens.
- Given a 1fps-sampled video with N frames, denoted as I = {I1, ..., IN}, we first use DINOv2 (Oquab et al., 2023) to extract features from each frame, leading to a set of DINO features {V 1 dino, . . . , V N dino}.
- We sample the video at 1 FPS and control the frame length ranging from 200 to 3.6k frames.


## 2412.01818 [keep] Beyond Text-Visual Attention: Exploiting Visual Cues for Effective Token Pruning in VLMs

- 기반 모델: InternVL, LLaVA, LLaVA-1.5, LLaVA-NeXT, Qwen-VL, Video-LLaVA
- 비교 대상: FastV, LLaVA-PruMerge, PruMerge, SparseVLM, ToMe, VisionZip
- 하드웨어: NVIDIA A100
- 벤치마크: ActivityNet, GQA, MMBench, MME, MSRVTT, MSVD, POPE, ScienceQA, TextVQA, VQAV2, VQAv2, VizWiz

**FREE** (5)
- Based on the analysis, We propose VisPruner, a plug-and-play method that utilizes visual cues for more effective token pruning in LVLMs.
- Notably, without any training, VisPruner can reduce the FLOPs of LLaVA-1.5-7B by 91% and inference latency by 75%, while maintaining comparable performance.
- Based on our observations, we propose VisPruner, a plug-and-play approach that exploits visual cues for more effective token pruning in VLMs.
- We introduce VisPruner, a plug-and-play approach that exploits visual cues for more effective token prun- ing in VLMs based on our observations.
- In this work, we mainly fo- cus on training-free VLM inference optimization, typically achieved by removing the less important tokens.

**TOK** (6)
- For instance, LLaVA-1.5 [34] accepts 336 × 336 input images, which are converted into 576 visual tokens, while their textual coun- terparts have typically fewer than 100 tokens.
- For example, VisPruner is capable of prun- ing 94.4% of visual tokens in LLaVA-1.5-7B, reducing in- ference FLOPs by more than 95%, and maintaining 91.5% of the original performance across 10 tasks without any ad- ditional training.
- Following FastV [9], we prune 75% visual tokens after layer 2 of the language model based on text-visual attention and visualize the frequency with which visual tokens at var- ious positions are selected to be retained, as well as their average attention received across N samples.
- It is observable that [CLS] attention is more con- centrated, with the top 20% visual tokens absorbing about 80% attention.
- With only about 5% of the tokens retained, VisPruner is still able to maintain 91.5% of the performance, proving the effectiveness of its design that leverages both important tokens and diverse tokens as complements.

**ACC** (4)
- For example, VisPruner is capable of prun- ing 94.4% of visual tokens in LLaVA-1.5-7B, reducing in- ference FLOPs by more than 95%, and maintaining 91.5% of the original performance across 10 tasks without any ad- ditional training.
- With only about 5% of the tokens retained, VisPruner is still able to maintain 91.5% of the performance, proving the effectiveness of its design that leverages both important tokens and diverse tokens as complements.
- At a 94.4% reduction ratio, retaining only 160 visual tokens, VisPruner preserves 86.7% of the original perfor- mance, significantly outperforming FastV (74.7%), Sparse- VLM (74.5%) as well as VisionZip (82.3%), demonstrating the value of VisPruner for high-resolution visual inputs.
- VisPruner maintains 95.1% of the original performance at a 88.9% reduction ratio (retain- ing 227 tokens) and 90.3% with only 114 tokens (94.4% reduction ratio), significantly outperforming FastV (86%).


## 2412.13303 [star] FastVLM: Efficient Vision Encoding for Vision Language Models

- 기반 모델: InternVL, LLaVA, LLaVA-1.5, LLaVA-NeXT, LLaVA-OneVision, LLaVa-OneVision, MiniGemini, Qwen-VL, mPLUG-Owl
- 비교 대상: FastV, FastVLM, LLaVA-PruMerge, PruMerge, SparseVLM, VisionZip, fastvlm
- 하드웨어: NVIDIA H100
- 벤치마크: AI2D, ChartQA, DocVQA, GQA, MMMU, OCRBench, POPE, ScienceQA, SeedBench, TextVQA, VQAv2

**PARAM** (2)
- We use a CLIP-pretrained hybrid vision encoder, specif- ically the MCi2 image encoder from MobileCLIP [83], which has 35.7M parameters and is based on the FastViT architecture.
- The model has 125.1M parameters, which is 3.5× larger than the largest FastViT variant from MobileCLIP, but is still smaller than popular ViT alternatives.

**SPEED** (8)
- Compared to LLaVa-OneVision at the highest resolution (1152×1152), FastVLM achieves better performance on key benchmarks like SeedBench, MMMU and DocVQA, using the same 0.5B LLM, but with 85× faster TTFT and a vision encoder that is 3.4× smaller.
- FastVLM is more than 3× faster than prior work.
- We demonstrate the potential of this hy- brid backbone, which generates visual tokens over 4× faster than a ViT model while achieving higher overall VLM ac- curacy with multi-scale features (Section 3.1.1).
- Com- pared to LLaVA-OneVision [45] operating at the highest possible resolution (1152×1152), FastVLM obtains compa- rable performance with the same 0.5B LLM, but with 85× faster TTFT and a 3.4× smaller vision encoder.
- In a controlled experimental setup, where only the vision backbone is changed, we show that FastViTHD outperforms its ViT- based and convolution-based counterparts when used in VLMs: achieving 3.2× faster TTFT and 3.6× smaller size than SigLIP-SO400M [94], and 2.3× faster TTFT and 1.7× smaller size than ConvNeXT [28].


## 2501.00574 [keep] VideoChat-Flash: Hierarchical Compression for Long-Context Video Modeling

- 기반 모델: InternVL2, InternVL2.5, LLaVA, LLaVA-OneVision, LLaVA-Video, Qwen2-VL, Qwen2.5-VL
- 비교 대상: —
- 하드웨어: A100, NVIDIA A100
- 벤치마크: LongVideoBench, MLVU, MVBench, VideoMME

**TOK** (3)
- Each clip is compressed into 64 tokens, meaning that, on average, each frame is represented by 16 tokens.
- The baseline employs SigLiP-so400M [65] as the vision encoder and Spatial donwsampling (196 tokens per frame) as the connector.
- It adopts a two-stage training strateay with image and short video following LLaVA [33]. terms of the model, it can be observed that HiCo significantly reduces the computational load (from 196 to 16 tokens per frame) while barely compromising the performance.

**FLOP** (1)
- 1,184,250.0 TFLOPs).


## 2501.12386 [keep] InternVideo2.5: Empowering Video MLLMs with Long and Rich Context Modeling

- 기반 모델: InternVL2, InternVL2.5, LLaVA, LLaVA-1.5, LLaVA-NeXT, LLaVA-NexT, LLaVA-OneVision, LLaVA-Video, LLava, LLava-NeXT
- 비교 대상: ToMe
- 하드웨어: A100
- 벤치마크: ActivityNet, EgoSchema, LongVideoBench, MLVU, MVBench, RefCOCO, RefCOCOg, VideoMME

**TOK** (1)
- The system implements dynamic video sampling, processing 64- 512 frames, with each 8-frame clip compressed to 128 tokens, yielding approximately 16 tokens per frame representation.


## 2502.11494 [keep] Stop Looking for Important Tokens in Multimodal Language Models: Duplication Matters More

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-Next, Qwen2-VL, Video-LLaVA, mini-Gemini
- 비교 대상: FastV, FasterVLM, FitPrune, HiRED, LLaVA-PruMerge, MustDrop, SparseVLM, ToMe
- 하드웨어: —
- 벤치마크: GQA, MMBench, MME, MSVD, OCRBench, POPE, TextVQA, VQAV2, VizWiz

**FREE** (4)
- In- stead, we propose DART (Duplication-Aware Reduction of Tokens), which prunes tokens based on its duplication with other tokens, lead- ing to significant and training-free accelera- tion.
- To solve this problem, abundant recent meth- ods introduce token pruning to remove the vision tokens in a training-free manner, which usually first defines the importance score of each token, and then prunes the most unimportant tokens dur- ing the inference phrase (Chen et al., 2024; Zhang et al., 2024c; Liu et al., 2
- Building on token duplication, we introduce a training- free, plug-and-play token reduction method that seamlessly integrates with Flash Attention. • Superior Performance with Extreme Com- pression.
- ToMe (Bolya et al., 2023) merges tokens without training but disrupts cross- modal interactions (Xing et al., 2024).

**TOK** (2)
- Experiments demonstrate that DART can prune 88.9% vision tokens while maintaining comparable performance, leading to a 1.99× and 2.99× speed-up in total time and prefilling stage, respectively, with good compatibility to efficient attention operators 1.
- 7), achieving 93.9% with only 11.1% tokens, outper- forming all competitors significantly. (iv) Inspired by (Wen et al., 2025), we apply DART during train- ing.

**SPEED** (2)
- Experiments demonstrate that DART can prune 88.9% vision tokens while maintaining comparable performance, leading to a 1.99× and 2.99× speed-up in total time and prefilling stage, respectively, with good compatibility to efficient attention operators 1.
- 5 Analysis and Discussion 5.1 Efficiency Analysis As shown in Table 2, we compare the total infer- ence time, prefill time, FLOPs, and KV cache mem- ory of multiple methods. (i) DART achieves a 2.99× speedup in prefill and 1.99× speedup in in- ference, while its performance on POPE degrades by less than 3% versus the v

**LAT** (2)
- 4 Latency: 2174s Latency: 551s Latency: 1258s Latency: 2364s (a) POPE (b) MME (c) MMBench (d) VizWiz Figure 4: Performance-Latency trade-off comparisons across different datasets on LLaVA-Next-7B.
- Latency: 2174s (a) POPE Latency: 551s (b) MME Figure 6: Influence from the layer for token pruning.

**ACC** (3)
- We ob- serve that (i) with only 192 tokens, DART achieves an impressive 98.8% average performance, sub- stantially outperforming second-best MustDrop by 1.6%. (ii) This trend strengthens under aggressive reduction ratios, with DART leading by 2.2% us- ing just 64 tokens. (iii) Moreover, DART scales seamlessly to advanc
- 5 Analysis and Discussion 5.1 Efficiency Analysis As shown in Table 2, we compare the total infer- ence time, prefill time, FLOPs, and KV cache mem- ory of multiple methods. (i) DART achieves a 2.99× speedup in prefill and 1.99× speedup in in- ference, while its performance on POPE degrades by less than 3% versus the v
- 1, suggesting that removing duplicate tokens may re- duce hallucinations in MLLMs on the POPE. (ii) At deeper layers (e.g., 15, 20), the latency-minimizing points correspond to pruning all vision tokens, yet performance drops only by 0.1%∼1.6%.


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


## 2503.18278 [keep] TopV: Compatible Token Pruning with Inference Time Optimization for Fast and Low-Memory Multimodal Vision Language Model

- 기반 모델: BLIP-2, InternVL, InternVL2, LLaVA, LLaVa, Video-LLaVA
- 비교 대상: FastV, LLaVA-PruMerge, LLaVa-PruMerge, TopV, VTW
- 하드웨어: A100, A6000
- 벤치마크: AI2D, MMBench, MMMU, OCRBench, POPE, VideoMME

**FREE** (1)
- Our contri- butions are summarized as follows: • We propose a training-free token reduction method for VLMs that optimizes pruning during the inference prefill- ing stage, reducing computation while maintaining com- patibility with FlashAttention and KV cache.

**TOK** (3)
- For example, in the OCR task, LLaVA-v1.5 [28] translates an image into 576 visual tokens, constituting up to 87% of the total in- put sequences.
- For the LLaVA models, reducing FLOPs by 35% of the vision tokens results in negligible accuracy loss compared to the baseline, with inference efficiency improving to 1.08 × on average and improving to 1.12 × for some recogni- tion tasks.
- When reducing FLOPs round 50% of the vision tokens, the model outperforms the FastV, which reduces FLOPs by 47%, by an average of 0.39% in accuracy.

**FLOP** (2)
- We set the pruning ratio as 50% and the sampling interval to 4 for token recovering, achieving a 35% FLOPs reduction in overall vision tokens for LLaVA models.
- For InternVL2 models, we set the pruning ratio as 70%, and the sampling interval to 3, resulting in reducing round 47% FLOPs ratio for the visual tokens.

**LAT** (2)
- Notably, our optimization process requires only 2 ms, comprising less than 1% of total inference time. those with minimal influence.
- Notably, our optimization pro- cess takes only 2 ms, accounting for less than 1% of total inference time in most cases.

**MEM** (5)
- Specifically, on InternVL2 models, it improves accuracy by 1.2%, reduces visual FLOPs by 47%, low- ers dynamic memory usage by 61%, and achieves 2.1× inference efficiency.
- For LLaVA models, it improves per- formance by 0.39%, reduces visual FLOPs by 50%, low- ers dynamic memory usage by 49%, and achieves 1.68× inference efficiency compared to previous methods.
- For the InternVL2 models, when reducing FLOPs by round 47% for the vision tokens, the model showed almost no loss of accuracy compared to the baseline, while dy- namic memory usage is reduced by 23.8% and inference efficiency improved to 1.23 × on average and improved to 1.31 × for some recognition tasks.
- When compared to FastV, which reduces FLOPs by 47%, InternVL2 models shows a 1.2 higher score on average, with dynamic memory usage decreasing by 61% and inference efficiency improv- ing by 2.1×.
- Ad- ditionally, dynamic memory usage is reduced by 49%, and inference efficiency improves by 1.68×.

**ACC** (1)
- When compared to FastV, which reduces FLOPs by 47%, InternVL2 models shows a 1.2 higher score on average, with dynamic memory usage decreasing by 61% and inference efficiency improv- ing by 2.1×.


## 2506.10967 [keep] Beyond Attention or Similarity: Maximizing Conditional Diversity for Token Pruning in MLLMs

- 기반 모델: LLaVA, LLaVA-1.5, LLaVA-NeXT, LLaVA-Video, Qwen2.5-VL
- 비교 대상: CDPruner, DivPrune, FastV, LLaVA-Prumerge, PruMerge, PyramidDrop, SparseVLM, TRIM, VisionZip
- 하드웨어: NVIDIA A100
- 벤치마크: AI2D, ChartQA, GQA, LongVideoBench, MLVU, MMBench, MME, MVBench, OCRBench, POPE, ScienceQA, TextVQA, VQAV2, VQAv2, Video-MME, VizWiz

**FREE** (7)
- The proposed CDPruner is training-free and model-agnostic, allowing easy application to various MLLMs.
- To address these issues, we propose CDPruner, a plug-and-play method for MLLM inference ac- celeration by maximizing the conditional diversity of the selected subset.
- When applied to LLaVA-NeXT-7B, it reduces FLOPs by 95%, CUDA latency by 78%, and GPU memory by 17%, while maintaining 94% of the original performance in a training-free manner.
- We introduce CDPruner, a plug-and-play and model-agnostic solution for visual token pruning that maximizes conditional diversity.
- Other works adopt a training-free approach by removing redundant visual tokens during inference, known as token pruning.

**TOK** (6)
- For example, LLaVA-1.5 [Liu et al., 2024a] converts a 336×336 image into 576 tokens, while its high-resolution variant, LLaVA-NeXT [Liu et al., 2024b], generates 2,880 tokens from an image with twice the resolution.
- With 77.8% of tokens pruned, CDPruner remarkably maintains nearly all the original performance, surpassing VisionZip by 1.4%.
- With only 5.6% of visual tokens retained, attention and similarity-based methods also encounter noticeable performance degradation because, despite selecting relatively important tokens, they include excessive redundancy and duplication.
- As shown in Table 2, with 77.8% of tokens pruned, CDPruner maintains performance comparable to, or slightly better than, the original LLaVA- NeXT, demonstrating the higher visual redundancy in high-resolution scenarios.
- As demonstrated in Table 3, with 62.1% of visual tokens pruned, CDPruner maintains 98.6% of the original performance, outperforming PDrop by 1.5%.

**LAT** (1)
- The additional latency is negligible when m ≪n, with less than 10ms per sample.

**MEM** (1)
- When applied to LLaVA-NeXT-7B, it reduces FLOPs by 95%, CUDA latency by 78%, and GPU memory by 17%, while maintaining 94% of the original performance in a training-free manner.

**ACC** (8)
- When applied to LLaVA, CDPruner reduces FLOPs by 95% and CUDA latency by 78%, while maintaining 94% of the original accuracy.
- When applied to LLaVA-NeXT-7B, it reduces FLOPs by 95%, CUDA latency by 78%, and GPU memory by 17%, while maintaining 94% of the original performance in a training-free manner.
- When the number of visual tokens further decreases to 64, roughly one-tenth of the original token length, attention-based pruning methods exhibit significant performance degradation of over 25%, indicating that internal 6 Table 2: Performance comparison of different pruning methods on LLaVA-NeXT-7B.
- In this scenario, CDPruner still maintains 94.3% of the original performance, significantly outperforming the best similarity-based method, DivPrune, by 3%, which fully demonstrates its effectiveness.
- As the reduction ratio further increases to 88.9% and 94.4%, CDPruner still retains up to 98% and 96% of the original performance, outperforming the second-best DivPruner by 2% and 3.1%, respectively.


## 2506.17218 [keep] Machine Mental Imagery: Empower Multimodal Reasoning with Latent Visual Tokens

- 기반 모델: Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**BIT** (1)
- We extend the original binary choice to a three-way classification.

**ACC** (1)
- However, increasing k to 8 results in a significant performance drop around 13%, likely due to error accumula- tion in longer latent sequences under autoregressive non-decoding generation.


## 2509.22548 [keep] JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation

- 기반 모델: Qwen2.5-VL
- 비교 대상: —
- 하드웨어: —
- 벤치마크: —

**LAT** (1)
- Memory Size Inference Time NEÓ OSÒ SRÒ SPLÒ VGGT (8) 268 ms 5.99 56.2 50.2 45.0 VGGT (32) 1549 ms 5.66 56.8 51.2 47.6 Cached Memory (8) 82 ms 5.91 56.0 50.5 45.7 Cached Memory (32) 149 ms 5.52 57.1 51.7 48.3 Cached Memory (48) 195 ms 5.17 58.0 52.8 49.2 Cached Memory (64) 244 ms 5.27 57.5 52.3 49.4 Cached Memory[w/o in

**MEM** (1)
- Furthermore, removing the semantic memory results in a 13.8% decrease in the SR, underscoring the necessity of the semantic memory.


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


## 2602.23699 [keep] HiDrop: Hierarchical Vision Token Reduction in MLLMs via Late Injection, Concave Pyramid Pruning, and Early Exit

- 기반 모델: LLaVA, LLaVA-1.5
- 비교 대상: FastV, VoCo-LLaMA
- 하드웨어: NVIDIA A100
- 벤치마크: GQA, POPE, TextVQA, VQAv2, VizWiz

**FREE** (5)
- Most modern MLLMs rely on a connector-based architecture (Liu et al., 2023a;b; 2024a; Bai et al., 2023; Wang et al., 2024), wherein a lightweight module projects visual features directly into the LLM’s embedding space, allowing a pre-trained text backbone to process multimodal inputs without retraining from scratch (Li
- To scrutinize this belief, we perform a training-free layer-wise probe on LLaVA- v1.5-7B, feeding GQA image–question pairs through the network and recording hidden states at all layers.
- We validate this with behavior on LLaVA-v1.5-7B with a training-free “early exit” experiment, where we discard all visual tokens at a specific layer and ob- serve the impact on performance.
- Dashed lines separate training-free (above) and training-based (below) methods within each block.
- The ∗denotes results reproduced using the official checkpoints; † denotes training-based methods evaluated under training- free settings; ‡ denotes training-free methods evaluated under training-based settings.

**TOK** (3)
- Extensive experiments show that HiDrop compresses ∼90% visual tokens while matching the original performance and accelerating training by 1.72×.
- Extensive experiments on LLaVA-1.5-7B show that HiDrop compresses ∼90% of visual tokens while matching the original performance, accelerating training by up to 1.72× and substantially improving inference throughput.
- Notably, it retains 98.3% and 96.5% of the baseline performance while pruning 88.9% and 91.7% of vision tokens, respectively.

**LAT** (1)
- Moreover, HiDrop lowers the prefill latency from 63.6 ms to 32.6 ms, and can be further reduced to 31.8 ms and 28.8 ms through parallelly decoupled visual KV projection and fewer dropping stages.

**ACC** (5)
- Under an extreme GED schedule that reduces visual tokens from 576 to just 1 across the middle layers, the model still retains 99.6% of its original GQA performance.
- Notably, it retains 98.3% and 96.5% of the baseline performance while pruning 88.9% and 91.7% of vision tokens, respectively.
- At even more aggressive compression, HiDrop still retains 96.5% of the baseline at 91.7% pruning, whereas PDrop cannot reach this pruning level under the same protocol.
- Notably, compared to PDrop’s pruning ratio of 46.9%, HiDrop achieves a much higher pruning ratio of 89.0%, which is 4.8 times more aggressive, while the performance drop is only 1.6%, demonstrating HiDrop’s superior efficiency and minimal accuracy trade-off.
- At the same time, the compressed model remains close to the base model, with av- erage performance drops of only 3.0% (665k) and 3.7% (1M) despite operating under a much more aggressive visual-token budget.


## 2603.07135 [keep] The Model Knows Which Tokens Matter: Automatic Token Selection via Noise Gating

- 기반 모델: BLIP-2, LLaVA, LLaVA-1.5, LLaVA-NEXT, LLaVA-NeXT, LLaVA-OneVision, Mini-Gemini, Qwen2-VL, Qwen2.5-VL
- 비교 대상: DivPrune, FastV, FasterVLM, FitPrune, HiRED, PruMerge, PyramidDrop, SparseVLM, ToMe, VTW, VisionZip
- 하드웨어: NVIDIA A6000
- 벤치마크: GQA, MMBench, MME, POPE, SEED-Bench, ScienceQA, TextVQA, VQAv2, VizWiz

**FREE** (2)
- A representative line of work performs plug-and-play, training-free token pruning right after the vision encoder.
- Other training-free approaches emphasize representational coverage: DivPrune [45], DART [46], and Feather [47] select tokens to maximize diversity or to minimize duplication among the retained set, which can be more robust than pure importance ranking at high pruning ratios.

**TOK** (1)
- The margin is widest under heavy pruning: at K=6 (3% of tokens) AutoSelect leads HoloV by roughly 10 percentage points in Top-1, while FastV trails further behind.

**BIT** (3)
- 2) We introduce a variance-preserving noise gate that replaces the binary keep-or-discard decision of conventional pruning with continuous per-token information capacity modulation.
- We anneal τ from τstart to τend on a cosine schedule; at large τ the scores are diffuse, and as τ →0 they collapse to the binary mask used at inference.
- Each method first scores all N=576 tokens on the 24×24 grid produced by CLIP ViT-L/14 and generates a binary selection mask for budget K.

**PARAM** (1)
- 5 A PREPRINT - MARCH 10, 2026 4 Experiments 4.1 Experimental Setup The Scorer and Denoiser are jointly trained on ImageNet-1K [59] captioning data from ImageNet-1K-VL-Enriched [60], adding ∼84M trainable parameters while all base VLM weights remain frozen.

**LAT** (2)
- PruneSID’s module requires 43.39 ms, over 60× slower than AutoSelect, pushing its prefill total to 115.84 ms, barely faster than using all tokens.
- By contrast, AutoSelect completes token selection in 0.69 ms and achieves the lowest TTFT of 72.73 ms.

**ACC** (3)
- On ten VLM benchmarks, AutoSelect retains 96.5% of full model accuracy while accelerating LLM prefill by 2.85× with only 0.69 ms overhead, and transfers to different VLM backbones without architecture-specific tuning.
- 3) AutoSelect retains 96.5% of full-model performance at 88.9% pruning on LLaVA-1.5-7B with only 0.69 ms pruning module overhead, and generalizes consistently to the higher-resolution LLaVA-NEXT and the architecturally distinct Qwen2.5-VL.
- On LLaVA-1.5-7B, AutoSelect retains 96.5% of full-model accuracy at 88.9% token pruning with only 0.69 ms selection overhead, and generalizes without architecture-specific modification to LLaVA-NEXT and Qwen2.5-VL, consistently outperforming existing methods across all evaluated settings.

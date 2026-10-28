# 등급 C 재점검 후보 (18편, 표본 밖) — 10/21


## InternVideo2.5 (2501.12386) — 가지 4.4, 코드 True, 줄 10

- L5: Xiangyu Zeng2,1, Chenting Wang1, Changlian Ma2,1, Haian Huang1 ⏎ Jianfei Gao1, Min Dou1, Kai Chen1, Wenhai Wang1 ⏎ Yu Qiao†1, Yali Wang†4,1, Limin Wang†2,1
- L129: as segmentation and temporal grounding that require precise predictions. To address these limitations, researchers ⏎ have developed two main approaches: 1) The pixel-to-sequence (P2S) methodology [Chen et al., 2023b, Ren et al., ⏎ 2024, Wang et al., 2024a,g, Ye et al., 2023] enables MLLMs to generat
- L382: data, allowing task-supervised gradients to flow from specialized heads to MLLM; and (b) instruction tuning on a ⏎ comprehensive dataset of 3.5M samples, including 1.1M images, 1.7M short videos (<60s), and 0.7M long videos ⏎ (60-3600s). We employ dynamic video sampling with 64-512 frames and tune t
- L440: LVBench ⏎ Average duration (sec) ⏎ 16
- L751: InternVL2.5’s implicit memory (8B model). Using a single-hop needle-in-a-haystack (NiAH) task with 5,000 frames, ⏎ InternVideo2.5 demonstrates superior recall. All models were evaluated on 16 A100 (80GB) GPUs. ⏎ As shown in Figure 3, InternVL2.5-8B struggles to recall target frames accurately even w
- L769: InternVideo2.5: Empowering Video MLLMs with Long and Rich Context Modeling ⏎ Yes, there was a little girl in white with a ponytail in the video. She appeared around 1409.5 seconds. ⏎ Was there a little girl in white with a ponytail in the video? And approximately when did she appear?
- L801: perception via classical vision supervision, but this benefits would vanish when the input videos are quite long (around ⏎ and more than 15 minutes). ⏎ 10
- [참고문헌 뒤] L1139: Kang Chen, Tao Han, Junchao Gong, Lei Bai, Fenghua Ling, Jing-Jia Luo, Xi Chen, Leiming Ma, Tianning Zhang, Rui ⏎ Su, et al. Fengwu: Pushing the skillful global medium-range weather forecast beyond 10 days lead. arXiv preprint ⏎ arXiv:2304.02948, 2023a.
- [참고문헌 뒤] L1186: Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson ⏎ Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In ⏎ CVPR, pages 18995–19012, 2022.

## Quant Experts (2602.24059) — 가지 4.3, 코드 False, 줄 3

- L43: Model quantization has become a key technique for reduc- ⏎ ing the computational and memory costs of large-scale mul- ⏎ timodal models [19]. By mapping weights and activations
- L1553: cal performance model following the FlightLLM [47] ac- ⏎ celerator architecture. Prefill-stage kernel speedups of lin- ⏎ ear layers are measured with sequence length 128 using
- L1585: 4.50× ⏎ Table 8. NPU speedup ratios of QE for Qwen2VL-7B linear layers ⏎ compared with the fp16 model, measured during the prefill stage

## FitPrune (2409.10197) — 가지 4.4, 코드 True, 줄 12

- L35: with only 0.5% accuracy drop. Notably, the pruning recipe ⏎ can be obtained in about 5 minutes. Our code is available at ⏎ https://github.com/ywh187/FitPrune.
- L192: mance degradation. More importantly, its pruning recipe can ⏎ be obtained in about 5 minutes for all VL tasks. ⏎ Conclusively, the contribution of this paper is three-fold:
- L1173: 6.6K ⏎ 199 min ⏎ 61.6
- L1176: 2.0K ⏎ 66 min ⏎ 61.6
- L1179: 0.6K ⏎ 19 min ⏎ 61.5
- L1182: 65 ⏎ 2 min ⏎ 61.6
- L1185: 10 ⏎ 0.5 min ⏎ 61.2
- [참고문헌 뒤] L1718: For instance, at a 50% pruning ratio, the model’s accu- ⏎ racy only decreases by 0.1%, with throughput increasing by ⏎ 22.2%. In extreme scenarios, our method continues to show
- [참고문헌 뒤] L1722: the model experiences a performance drop of 3.6%, achiev- ⏎ ing a throughput increase of 40.2% and reducing TFLOPs ⏎ by 68.7%. In summary, FitPrune demonstrates stability and
- [참고문헌 뒤] L1779: Table 7: Comparison of Flash Attention (FA), FitPrune, and their combinations on TextVQA, SQA, and GQA datasets. Accu- ⏎ racy is reported alongside throughput measured in samples per second. ⏎ Layer 4
- [참고문헌 뒤] L1882: provements while maintaining accuracy. For instance, with ⏎ a pruning ratio of 40%, FitPrune increases throughput by ⏎ 52.1% on TextVQA and 78.0% on SQA compared to the
- [참고문헌 뒤] L1887: more remarkable. Specifically, the combination achieves ⏎ a 131.3% throughput gain on GQA with a pruning ratio ⏎ of 60%, significantly outperforming either method alone.

## Penguin-VL (2603.06569) — 가지 4.1, 코드 True, 줄 3

- L587: employ adaptive resampling strategies to balance domain distribution. For massive short-video collections ⏎ like VIDAL-10M [88] (mostly < 20s), we perform random sampling to create a scalable subset; conversely, ⏎ for Koala-36M [62], we implement duration-aware sampling to ensure uniform coverage ac
- L1083: configurations for video inputs: specifically, we cap the maximum number of frames at 300 and set the frame ⏎ rate up to 3 FPS. Two frame sampling strategies are considered: ⏎ • 1) TRA, follows the same sampling procedure used during training (see Section 2.1.2).
- [참고문헌 뒤] L1965: [23] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson ⏎ Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. ⏎ In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Re

## MoVE-KD (2501.01709) — 가지 4.3, 코드 True, 줄 3

- L260: results in a substantial increase in parameter count and as- ⏎ sociated time costs. Therefore, our method uses parameter- ⏎ efficient LoRA [16] as the expert instead.
- L307: sequence length of visual tokens, V (t) ∈Rm×n×c and ⏎ V (s) ∈Rn×c represent visual tokens of teacher and student, ⏎ Figure 4. The generation of token weight. We employ the atten-
- [참고문헌 뒤] L1132: enhofer, Trevor Darrell, and Saining Xie. A convnet for the ⏎ 2020s. In Proceedings of the IEEE/CVF conference on com- ⏎ puter vision and pattern recognition, pages 11976–11986,

## CLIP-LoRA (2405.18541) — 가지 4.2, 코드 True, 줄 10

- L118: put requires back-propagating through the entire model; see ⏎ the training times in Table 1. ⏎ Alongside this expanding prompt-tuning literature, there
- L162: parameters to train [33]. This often results in a trade-off ⏎ among memory footprint, computational overhead, and per- ⏎ formance. A summary is depicted in Figure 1.
- L177: tional number of parameters after adaptation, which can ⏎ lead to higher inference latency, even though some recent ⏎ works aim at mitigating this issue [41].
- L303:  ⏎ Table 1. Training time on 16-shots ImageNet task. Experiments ⏎ were conducted on a single A100 80Gb with the original code pro-
- L308: Method ⏎ Training time ⏎ CoOp (16)
- L310: CoOp (16) ⏎ 2h ⏎ PLOT++
- L316: CLIP-LoRA ⏎ 50 min. ⏎ notes the corresponding normalized (unit-hypersphere) tex-
- L404: put requires back-propagating through the entire model (see ⏎ the training times reported in Table 1). ⏎ Adapters (A).
- L1021: CLIP-LoRA is computationally and memory efficient. ⏎ Table 1 compares the training time of the leading prompt- ⏎ learning methods; CLIP-LoRA achieves better performance

## BiomedCoOp (2411.15232) — 가지 4.2, 코드 True, 줄 2

- L392: scores S and the median absolute deviation D: ⏎ Ms = median(S) ⏎ (5)
- L602: Supplementary Materials). All experiments ran on a single ⏎ NVIDIA A100 GPU (40GB RAM). ⏎ 4.2. Few-shot Evaluation

## InternLM-XComposer2 (2401.16420) — 가지 4.2, 코드 True, 줄 0


## Uni-MoE (2405.11273) — 가지 4.1, 코드 True, 줄 5

- L345: (4) ⏎ S = Speech-Qformer(Whisper(S)), ⏎ (5)
- L784: This dataset comprises short speech clips, each less than ⏎ 30 seconds in duration, with a cumulative total exceeding ⏎ 1.7 million instances. Subsequently, we develop a tri-modal
- L794: audio files from the LibriSpeech dataset [55] with short ⏎ speeches of 30 seconds into longer sound files, each extending ⏎ up to two minutes in duration. Additionally, we convert the
- L1006: compact dataset comprises 150 questions related to long audio ⏎ segments with an average length of 109 seconds, and 50 questions ⏎ about short audio segments with an average length of 14 seconds.

## LongVU (2410.17434) — 가지 4.4, 코드 True, 줄 18

- L92: mechanism based on temporal dependencies is applied for excessively long videos. As a result, our model ⏎ is capable of processing 1fps sampled video input with high performance, which can adaptively reduce the ⏎ number of tokens per frame to 2 on average to accommodate an hour-long video for MLLM w
- L147: segment independently, and retrieves the most relevant segment in response to user queries. Our work focuses ⏎ on maximizing the preservation of frames in video content (1fps) within given context length by proposing ⏎ spatiotemporal compression of video tokens.
- L207: model SigLIP (Zhai et al., 2023) as frame feature extractors for MLLM in video understanding task. ⏎ Note that processing the entire long video can be computationally expensive. Given a 1fps-sampled video ⏎ with N frames, denoted as I = {I1, ..., IN}, we first use DINOv2 (Oquab et al., 2023) to extr
- L216: PJ ⏎ j=1,j̸=i sim(V i ⏎ dino, V j
- L313: We evaluate our model on EgoSchema (Mangalam et al., 2024), MVBench (Li et al., 2024b), VideoMME (Fu ⏎ et al., 2024) and MLVU (Zhou et al., 2024). VideoMME (Fu et al., 2024) (1 min ∼1 hour) and MLVU (Zhou ⏎ et al., 2024) (3 mins ∼2 hours) are long video benchmarks for assessing long video understand
- L316: For VideoMME (Fu et al., 2024), videos are officially split based on duration, which contains a subset of ⏎ long videos ranging from 30 minutes to 1 hour. We perform standardized evaluations using greedy decoding ⏎ (num_beams=1) and benchmark our results against other open-source and proprietary mod
- L329: Duration ⏎ 179.8 sec ⏎ 16 sec
- L331: 16 sec ⏎ 3∼120 min ⏎ 1∼60 min
- L333: 1∼60 min ⏎ 30∼60 min ⏎ Proprietary Models
- L338: - ⏎ 1fps ⏎ 55.6
- L347: - ⏎ 1fps ⏎ 72.2
- L366: 4k ⏎ 1fps ⏎ 38.5
- L438: 8k ⏎ 1fps ⏎ 67.6
- L798: We then insert each image from a set of VQA problems as a needle frame into this long video for creating a ⏎ challenging search task. We sample the video at 1 FPS and control the frame length ranging from 200 to 3.6k ⏎ frames. We also vary the needle frame insertion depth from 0% to 100% of the tota
- [참고문헌 뒤] L1099: 7B ⏎ 1fps ⏎ 64.7

## LLAVADI (2407.19409) — 가지 4.3, 코드 False, 줄 0


## LLaVA-MoD (2408.15881) — 가지 4.1/4.3, 코드 True, 줄 16

- L51: sive training data present significant computational challenges. For example, the largest version of ⏎ LLaVA-NeXT employs Qwen-1.5-110B and trains with 128 H800 GPUs for 18 hours. Addition- ⏎ ally, the substantial number of parameters requires advanced hardware and results in slow inference
- L103: from mimicking and approximating l-MLLM to ultimately surpassing it: Mimic Distillation. This ⏎ stage is divided into two steps, i.e., dense-to-dense (D2D) and dense-to-sparse (D2S). The rationale ⏎ for this two-step process is to facilitate the transfer of complex knowledge, where the first step
- L108: logits distribution between the initialized dense s-MLLM and l-MLLM, using general captioning ⏎ and conversation datasets. Next, in D2S, s-MLLM is first transformed from dense to sparse. We ⏎ then employ the standard KD loss and LM loss to distill the MoE block, using the complex multi-
- L349: simultaneous learning. Subsequently, we conduct a general-to-specialized mimic distillation, which ⏎ consists of two steps: dense-to-dense (D2D) and dense-to-sparse (D2S) distillation, to transfer the ⏎ knowledge to πS. This two-step approach balances the transfer of general and specialized knowl-
- L353: Fig. 3, we utilize the dense structure of πS during D2D to acquire general knowledge and transform ⏎ it into a sparse structure during D2S to acquire complex specialized knowledge. Throughout both ⏎ stages, πT remains unchanged.
- L388: existing bias in l-MLLM. The objective function is: ⏎ LD2S(πS; πT) = −E(x,yk)∼πS [log πS(yk | y<k, x)] −E(x,yk)∼πT ⏎ 
- L1101: We explore the effect of the general-to- ⏎ specialized approach in mimic distillation by comparing the proposed D2D+D2S with D2S. The ⏎ D2D+D2S involves a two-phase process. Firstly, it distills a dense s-MLLM using general data.
- L1104: Subsequently, it transforms the s-MLLM from dense to sparse and further distills it using multi- ⏎ task data. The D2S directly distills the sparse s-MLLM using a combined of general and multi-task ⏎ dataset. Tab. 7 shows that D2D+D2S surpasses D2S with an average gain of 4.0%. The result indi-
- L1106: dataset. Tab. 7 shows that D2D+D2S surpasses D2S with an average gain of 4.0%. The result indi- ⏎ cates that D2D+D2S enables effective knowledge transfer, striking a balance between general and ⏎ specialized competencies. Additionally, D2D+D2S is more computationally efficient, consuming
- L1108: specialized competencies. Additionally, D2D+D2S is more computationally efficient, consuming ⏎ only 62.5% of the GPU hours required by D2S. ⏎ Focus on Response Distillation Improves Generalization. We explores the effect of the distilla-
- L1128: AVG ⏎ D2S ⏎ 1536
- L1138: 57.9 ⏎ D2D+D2S ⏎ 960
- [참고문헌 뒤] L1559: adam optimizer (Diederik, 2014) and train on 16 NVIDIA A100 GPUs for one epoch each, totaling ⏎ approximately 960 GPU hours. The detailed training hyperparameters are shown in Tab. 11. ⏎ Table 11: Training hyperparameters of each stage.

## DeepSeek-VL2 (2412.10302) — 가지 4.1, 코드 True, 줄 6

- L15: mechanism, which compresses Key-Value cache into latent vectors, to enable efficient inference ⏎ and high throughput. Trained on an improved vision-language dataset, DeepSeek-VL2 demon- ⏎ strates superior capabilities across various tasks, including but not limited to visual question
- L129: by compressing the Key-Value (KV) cache into a latent vector, resulting in faster inference and ⏎ increased throughput capacity. We further enhance efficiency through the DeepSeekMoE frame- ⏎ work [20, 86], which employs sparse computation techniques. Our model series adopt three
- L278: porates the Multi-head Latent Attention mechanism [53]. MLA enhances inference efficiency by ⏎ compressing the Key-Value cache into a latent vector, enabling increased throughput capacity. ⏎ The model also incorporates a MoE architecture [20] allowing for efficient inference through
- L903: for different kinds of data and switch between these two strategies on demand. The training of ⏎ DeepSeek-VL2 was completed in 7/10/14 days using a cluster of 16/33/42 nodes, with each ⏎ node equipped with 8 NVIDIA A100 GPUs.
- L1806: consumption during both training and inference stages. Notably, our 3B, 16B and 27B models ⏎ can be deployed on a single GPU with 10 GB, 40GB and 80GB memory respectively. We employ ⏎ a dynamic tiling vision encoding strategy to efficiently process high-resolution images with
- [참고문헌 뒤] L2093: Learning, volume 235 of Proceedings of Machine Learning Research, pages 52632–52657. ⏎ PMLR, 21–27 Jul 2024. URL https://proceedings.mlr.press/v235/wei24h.html. ⏎ [92] C. Wendler. wendlerc/renderedtext.

## Kimi-VL (2504.07491) — 가지 4.1, 코드 True, 줄 9

- L292: model, such as the variable-length sequence attention mechanism supported by FlashAttention (Dao et al. 2022), ⏎ ensuring non-compromised training throughput for images of varying resolutions. ⏎ MoonViT is initialized from and continually pre-trained on SigLIP-SO-400M (Zhai et al. 2023), which origi
- L548: H. Liu et al. 2023)—to accelerate the speed of Kimi-VL . After optimizing parallel strategies, the resulting training ⏎ throughput of our model is around 60% higher than a 7B dense VLM (e.g. VLMs based on Qwen2.5-7B). ⏎ • Data Parallelism (DP). DP replicates the model across multiple devices, each p
- L558: • Context Parallelism (CP). CP addresses long-sequence training by splitting sequences across different CP ranks ⏎ in conjunction with flash attention (Dao et al. 2022). This substantially reduces peak memory usage and relieves ⏎ the memory pressure from attention computations.
- L612: Beyond these four parallel strategies, we incorporate ZeRO1 (Rajbhandari et al. 2020) and Selective Checkpointing ⏎ Activation (T. Chen et al. 2016; Korthikanti et al. 2022) to further optimize memory usage. ZeRO1 reduces optimizer ⏎ state overhead by using a distributed optimizer while avoiding ext
- L1494: Our Kimi-VL-Thinking model also exhibits strong test-time scaling properties, as shown in Figure 13. Specifically, ⏎ increasing the max thinking token length at inference time consistently improves test-time accuracy across all three ⏎ 16
- [참고문헌 뒤] L1813: arXiv:2403.20330 (2024). ⏎ Chen, Tianqi et al. Training Deep Nets with Sublinear Memory Cost. 2016. arXiv: 1604.06174 [cs.LG]. URL: ⏎ https://arxiv.org/abs/1604.06174.
- [참고문헌 뒤] L1836: Neural Information Processing Systems 36 (2024). ⏎ Grauman, Kristen et al. “Ego4d: Around the world in 3,000 hours of egocentric video”. In: Proceedings of the IEEE/CVF ⏎ conference on computer vision and pattern recognition. 2022, pp. 18995–19012.
- [참고문헌 뒤] L2111: capabilities within the ego-centric scenario. Derived from Ego4D (Grauman et al. 2022), the benchmark comprises over ⏎ 5,031 multiple choice question-answer pairs spanning more than 250 hours real-world videos with a semi-automatic ⏎ data pipeline.
- [참고문헌 뒤] L2136: environments. Built on the OSWorld framework, it allows agents to interact with a full range of applications and web ⏎ tools. The benchmark is scalable and can complete evaluations in under 20 minutes on Azure. It offers insights into ⏎ agent performance, highlighting the potential for future resear

## KRAdapter (2508.00230) — 가지 4.2, 코드 False, 줄 33

- [참고문헌 뒤] L1428: We then prove the case that {X1, . . . , Xn} are vectors of unit length. Since the vectors were drawn independently, we can ⏎ first assume we drew X1. The probability that this is the zero vector is 0 w.r.t the Lebesgue measure on the closed unit ball ⏎ BN(0) about the origin in RN and hence any oth
- [참고문헌 뒤] L1629: E. Training times and VRAM usage ⏎ We find that all algorithms use comparable amounts of VRAM during training except for RandLoRA which comes at the ⏎ cost of a slight increase in training time. We report training time results in Table 5 for various ViT architecture for 1 epoch
- [참고문헌 뒤] L1648: LoRA ⏎ 16.8 mins ⏎ 134.1 mins
- [참고문헌 뒤] L1650: 134.1 mins ⏎ 215.5 mins ⏎ 243.3 mins
- [참고문헌 뒤] L1652: 243.3 mins ⏎ 222.2 mins ⏎ SinLoRA
- [참고문헌 뒤] L1654: SinLoRA ⏎ 16.8 mins ⏎ 136.9 mins
- [참고문헌 뒤] L1656: 136.9 mins ⏎ 216.6 mins ⏎ 246.2 mins
- [참고문헌 뒤] L1658: 246.2 mins ⏎ 224.3 mins ⏎ RandLoRA
- [참고문헌 뒤] L1660: RandLoRA ⏎ 16.7 mins ⏎ 138.4 mins
- [참고문헌 뒤] L1662: 138.4 mins ⏎ 225.5 mins ⏎ 265.3 mins
- [참고문헌 뒤] L1664: 265.3 mins ⏎ 235.2 mins ⏎ Krona
- [참고문헌 뒤] L1666: Krona ⏎ 16.6 mins ⏎ 135.9 mins
- [참고문헌 뒤] L1668: 135.9 mins ⏎ 217.2 mins ⏎ 250.4 mins
- [참고문헌 뒤] L1670: 250.4 mins ⏎ 227.5 mins ⏎ KRAdapter
- [참고문헌 뒤] L1672: KRAdapter ⏎ 16.5 mins ⏎ 137.5 mins
- [참고문헌 뒤] L1674: 137.5 mins ⏎ 220.1 mins ⏎ 247.6 mins
- [참고문헌 뒤] L1676: 247.6 mins ⏎ 226.3 mins ⏎ FT
- [참고문헌 뒤] L1678: FT ⏎ 21.1 mins ⏎ 167.9 mins
- [참고문헌 뒤] L1680: 167.9 mins ⏎ 270.5 mins ⏎ Not trained
- [참고문헌 뒤] L1683: Not trained ⏎ Table 5. Comparison of training time for one epoch on ImageNet on CLIP architectures and LLama3-8B, Qwen2.5-7B for one epoch on the ⏎ commonsense reasoning dataset
- [참고문헌 뒤] L1828: F.3.3. Detailed results ⏎ Tables 9 report per dataset detailed results for PEFT algorithms using the ViT-{B/32,L/14,H/14} architectures respectively ⏎ F.4. OOD datasets

## MoSLoRA (2406.11909) — 가지 4.2, 코드 True, 줄 15

- L535: 28.3M ⏎ 8.0h ⏎ 29G
- L548: 0.9M ⏎ 26.3h ⏎ 66G
- L561: 28.3M ⏎ 25.5h ⏎ 68G
- L574: 28.4M ⏎ 8.2h ⏎ 31G
- L587: 28.3M ⏎ 12.5h ⏎ 58G
- L600: 29.1M ⏎ 14.5h ⏎ 33G
- L613: 57.4M ⏎ 14.8h ⏎ 33G
- L626: 28.4M ⏎ 8.2h ⏎ 31G
- L638: Table 4: Accuracy comparison of various methods fine-tuning LLaMA-3 8B on the commonsense reasoning tasks. ⏎ Param denotes the number of trained parameters, Time for the training time on A100 GPU, and Mem for the GPU ⏎ Memory usage. ∗denotes a larger rank in DoRA. We can find that the proposed MoSLo
- L704: ligible extra parameters (less than 0.1M) and ⏎ computing cost (less than 0.2h). Meanwhile, ⏎ MoSLoRA can save 44% training time than
- L709: via Kronecher products, it requires more than ⏎ 3x training time and 2x GPU memory than ⏎ MoSLoRA. Also, LoKr gets an average score
- L910: separately. For specific hyperparameters, please ⏎ refer to the Appendix B.2. It takes around 20 hours ⏎ to fine-tune using 4 Nvidia A100 80G GPUs.
- L981: train the model for 500 steps, which costs around ⏎ 16 minutes using 1 80G A100 GPU. During gen- ⏎ eration, we infer 50 steps for the given prompts.
- L1058: can be merged into the original weights during in- ⏎ ference, thus bringing no latency. We refer the ⏎ reader to Han et al. (2024) for a more compre-

## Mirage(잠재 시각 토큰) (2506.17218) — 가지 4.4, 코드 True, 줄 3

- [참고문헌 뒤] L1280: below. ⏎ Now, according to the following image(s), answer the question from the provided choices. ⏎ Question: If I turn right by 33 degrees, will I be facing away from dark frame red plaid blanket red
- [참고문헌 뒤] L1407: Both training stages of Mirage are conducted on a single NVIDIA H100 GPU. Taking the VSP spatial ⏎ reasoning task as an example, Stage 1 completes in approximately 3.5 hours, while Stage 2 takes ⏎ around 7.2 hours. For reference, text-only CoT SFT on the same hardware requires about 5.5 hours.

## VLA-GSE (2605.06175) — 가지 4.2, 코드 True, 줄 9

- L81: et al., 2025, Omaisan and Mohamed, 2025]. In particular, OpenVLA [Kim et al., 2025b] is among ⏎ the earliest VLA works to adopt LoRA in VLA fine-tuning for lower training memory consumption. ⏎ VLM2VLA [Hancock et al., 2025] provides evidence that LoRA better preserves pre-trained VLM
- L1027: in illumination, background, clutter layout, and instruction phrasing. We also compare real-world ⏎ inference time between VLA-GSE and baselines in Appendix D.4. ⏎ 6
- [참고문헌 뒤] L2002: We further compare the real-world inference efficiency of different policies by measuring the wall- ⏎ clock latency required to generate one action chunk. All methods are evaluated with batch size 1 ⏎ under the same deployment pipeline on the same real-robot workstation equipped with an NVIDIA
- [참고문헌 뒤] L2005: RTX 5080 GPU. We measure the elapsed time from receiving the current observation to returning the ⏎ full action chunk, and report the average latency over 120 runs. ⏎ As shown in Figure 5, Qwen3-VL-FFT achieves the lowest latency, while VLA-GSE is the second
- [참고문헌 뒤] L2013:  ⏎ Figure 5: Real-world inference latency comparison on an NVIDIA RTX 5080 GPU. We report ⏎ the wall-clock time for generating one action chunk with batch size 1. Error bars denote standard
- [참고문헌 뒤] L2072: 81.2 ⏎ We note, however, that absolute latency comparisons across different policy families should be ⏎ interpreted with caution. In particular, the lower latency of VLA-GSE relative to π0 and π0.5 is
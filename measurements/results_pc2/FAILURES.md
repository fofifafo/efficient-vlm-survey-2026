method: SparseVLM (USE_VERSION=1_0, RETAIN_TOKN=192 / 64)
status: FIXED (measured after fix)
stage: latency queue, full run 500x5, 2026-10-02 04:33 (PC2 RTX 5070 Ti 16 GB)
observation: peak VRAM 17.59 GB > 16.3 GB physical; TTFT 3,881 ms (smoke 8,234 ms) vs base 131 ms; mean power 79 W (GPU starved) -> WSL host-memory paging
cause (confirmed): repo builder (llava/model/builder.py:115) creates a LlamaDynamicvitFlashAttention2 module per layer and copies the attention weights into it (32 layers, 4 GiB), but LlamaDynamicvitDecoderLayer.forward only calls self_attn; the copies are never used
time_spent_min: 40 (diagnosis 15; invalid default run of 2.2 h left running, not counted)
fallback: none needed; plugin deletes layer.flash_attn after load (same computation path) -> TTFT 77.5 ms / 13.52 GB. Ported to PC1 plugin.
method: CDPruner (as-is, 128 tokens)
status: FIXED (dtype)
stage: latency queue smoke, 2026-10-02 04:30
observation: RuntimeError: expected mat1 and mat2 to have the same dtype, but got: float != c10::Half (clip_encoder.py:95, visual_projection)
cause (confirmed): builder casts the whole vision/text tower to fp16 when device_map="cuda"; repo code calls visual_projection(image_embeds.float()). Author scripts use device_map="auto", which keeps the tower in fp32
time_spent_min: 10
fallback: plugin casts visual_projection and text tower back to fp32 (same numerics as the author script)
method: CDPruner (as-is, fp32 projection/text tower, 128 / 64 tokens)
status: FIXED (measurement condition)
stage: latency queue full run, 2026-10-02 07:27
observation: TTFT 1,356 ms / 1,321 ms, mean power 87 W; profile showed CLIP vision forward 240 ms vs 22 ms standalone; torch reserved 15.5 GB after load
cause (confirmed): caching allocator kept ~2.3 GB reserved from the fp32->fp16 conversion during load; with CDPruner's extra CLIP towers the process crossed 16 GB and WDDM paged to shared memory
time_spent_min: 45 (profiling 30)
fallback: harness.py calls torch.cuda.empty_cache() right after load (reserved 15.5 -> 13.3 GB) and all 9 latency runs were repeated (round 2: cdpruner 151.9 / 107.6 ms). PC1 later found the remaining overhead comes from per-call side CUDA streams -> cdpruner_fix
method: DART (reduction 0.778 / 0.889)
status: FIXED (prompt-dependent index)
stage: latency queue smoke, 2026-10-02 07:26
observation: RuntimeError: selected index k out of range (modeling_llama_self.py:428 get_retained_image_token, topk over query tokens)
cause (confirmed): repo default image_token_start_index=35 assumes the vicuna_v1 system prompt; PC2 round-1 latency prompt had no system prompt, so the image starts at token ~5 and the "query tokens after the image" slice is empty
time_spent_min: 15
fallback: plugin sets image_token_start_index per sample from the <image> token position (not needed with the vicuna_v1 prompt now used everywhere)
method: CDPruner (as-is) accuracy evaluation, default setting
status: RECOVERED (resumed)
stage: accuracy run (GQA/POPE/TextVQA done, MME not started), 2026-10-02 23:40
observation: process stuck in D state, RSS 22.7 GB of the 24 GB WSL limit, GPU 0 % util, 0.36 s/sample (2x the harness latency) before the stall
cause (confirmed): eval_preds.py built task lists by iterating datasets rows, which decodes every image (TextVQA val 5,000 images) into RAM; with GQA image dict already resident, WSL ran out of memory and swapped
time_spent_min: 25
fallback: images decoded lazily per sample (ds[i]["image"]); predictions were appended per sample so the run resumed from MME only (no recomputation)
method: CDPruner (as-is) accuracy evaluation, r889 smoke + default resume
status: RECOVERED (config reverted)
stage: model load, 2026-10-02 23:43 (three attempts)
observation: RuntimeError: CUDA driver error: out of memory inside accelerate set_module_tensor_to_device while loading the CLIP text tower, with nvidia-smi showing 312 MiB used
cause (confirmed): PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True (added to run_eval.sh to curb fragmentation) is not supported under the WSL2 GPU paravirtualization driver; allocation fails at load time
time_spent_min: 15
fallback: removed expandable_segments; kept periodic torch.cuda.empty_cache() every 200 samples instead. Both CDPruner accuracy runs then completed (r889 0.22 s/sample)
method: setup (download.sh, huggingface-cli)
status: RECOVERED
stage: model download, 2026-10-02 03:13 and 03:33
observation: download stalled at 0 B/s after Windows sleep and after switching Wi-Fi -> wired; killing huggingface-cli discarded an 8 GB partial shard twice
cause (confirmed): open HTTP connection dropped on network change; huggingface-cli does not resume a killed transfer of a single large blob
time_spent_min: 60 (re-download at 11 MB/s on a 100 Mbps link)
fallback: keep the machine awake and the network fixed during downloads; restart download stage only

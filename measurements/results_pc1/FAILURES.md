method: SparseVLM (USE_VERSION=1_0, RETAIN_TOKN=192)
status: NOT MEASURABLE on 16 GB (as-is)
stage: smoke run (20 samples), 2026-10-02 02:00
observation: peak VRAM 17.58 GB > 16.3 GB physical -> WSL host-memory spill; TTFT 6,381 ms vs base 139 ms; 667 J/sample
cause (suspected): reference implementation materializes attention for text-guided token scoring (eager attention), memory above the base model
time_spent_min: 5 (4.4 h full run avoided by killing)
fallback: try USE_VERSION=2_0 (SparseVLM+, FlashAttention-2 compatible); if still >16 GB, report "does not fit on a 16 GB consumer GPU"
method: SparseVLM+ (USE_VERSION=2_0, RETAIN_TOKN=192)
status: NOT MEASURABLE on 16 GB (as-is)
stage: smoke run (20 samples), 2026-10-02 03:10
observation: peak VRAM 17.61 GB (v1: 17.58 GB) -> WSL host-memory paging; TTFT 4,143 ms vs base 114 ms; mean power 78 W (GPU starved)
cause (suspected): text-guided token scoring materializes full attention maps in eager mode for both versions; FlashAttention-2 (needed by v2) has no sm_120 build in this env
time_spent_min: 15 total (2-hour rule not exhausted; reserved for a 32 GB GPU run if available)
fallback: report as "exceeds 16 GB on consumer GPU"; optional later run on RTX 5090 (32 GB)

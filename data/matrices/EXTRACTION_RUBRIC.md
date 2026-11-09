# Extraction rubric (Section 3.5)

Applied to the full text of each of the 69 selected papers (71 branch entries), with the reference list removed.

## Step 1 — candidate sentences

The text is split into sentences; every sentence of at most 600 characters that matches one of the 14 patterns below (case-insensitive) is kept as a candidate, at most eight per pattern and paper.

| Pattern | Meaning | Regular expression |
|---|---|---|
| SPEED | speed-up or relative speed | `\d+(?:\.\d+)?\s?[x×]\s*(?:faster\|speed-?up\|acceleration\|reduction)\|speed-?up (?:of\|by) \d\|\d+(?:\.\d+)?\s?% (?:faster\|reduction in (?:latency\|time\|FLOPs))` |
| FLOP | FLOPs | `\d+(?:\.\d+)?\s?[GTM]?FLOPs\|FLOPs? (?:reduc\|drop\|decrease)\w* (?:by \|to )?\d+(?:\.\d+)?\s?%\|\d+(?:\.\d+)?\s?% (?:of (?:the )?)?FLOPs` |
| LAT | latency or time | `\d+(?:\.\d+)?\s?(?:ms\|milliseconds\|seconds?\|s)\b[^.]{0,60}(?:latency\|per (?:image\|sample\|token\|frame)\|inference\|prefill\|decod\|TTFT)\|(?:latency\|inference time\|prefill time\|TTFT\|time to first token)[^.]{0,60}\d+(?:\.\d+)?\s?(?:ms\|s\|seconds?)` |
| MEM | memory | `\d+(?:\.\d+)?\s?(?:GB\|GiB\|MB)\b[^.]{0,40}(?:memory\|KV\|cache\|VRAM)\|(?:memory\|KV cache\|VRAM)[^.]{0,60}\d+(?:\.\d+)?\s?(?:GB\|GiB\|MB\|%)` |
| THR | throughput | `\d+(?:\.\d+)?\s?(?:tokens?/s\|tokens per second\|samples?/s\|fps\|FPS\|QPS\|images?/s)` |
| TOK | token budget | `\d+(?:\.\d+)?\s?% (?:of (?:the )?)?(?:visual\|vision\|image\|video)? ?tokens\|(?:prun\|reduc\|compress\|retain\|keep\|drop)\w*[^.]{0,40}\d+(?:\.\d+)?\s?% of (?:the )?(?:visual \|vision \|image )?tokens\|(?:from\|to) \d{2,4} (?:visual \|vision )?tokens\|\d{2,4} tokens? (?:per\|/) (?:image\|frame)` |
| HW | hardware | `\b(?:NVIDIA )?(?:A100\|A800\|H100\|H800\|V100\|A6000\|A40\|L40S?\|RTX ?\d{4}\|3090\|4090\|T4\|Jetson[\w ]{0,15}\|Orin\|Snapdragon[\w ]{0,10}\|Apple M\d\|iPhone[\w ]{0,6}\|TPU ?v\d\|Ascend[\w ]{0,6}\|CPU)\b` |
| ACC | accuracy retention | `(?:accuracy\|performance\|score)[^.]{0,60}(?:drop\|loss\|degrad\|decreas\|retain\|maintain\|preserv\|within)[^.]{0,40}\d+(?:\.\d+)?\s?%\|\d+(?:\.\d+)?\s?% (?:of (?:the )?)?(?:original\|baseline\|full)[^.]{0,20}(?:performance\|accuracy)\|(?:retain\|maintain\|preserv\|keep)\w* \d+(?:\.\d+)?\s?%` |
| FREE | training-free claim | `training-?free\|plug-?and-?play\|without (?:any )?(?:re-?)?training\|no (?:additional \|extra )?training\|fine-?tun\w+ (?:is )?(?:required\|needed)` |
| BASE | base model | `\b(?:LLaVA(?:-(?:1\.5\|NeXT\|OneVision\|Video))?\|Qwen2?(?:\.5)?-VL\|InternVL[\d.]*\|MiniCPM-V\|Phi-3-vision\|BLIP-?2\|Video-LLaVA\|Mini-?Gemini\|mPLUG-Owl\|Idefics\d?\|PaliGemma\|Gemma ?3)\b` |
| CMP | compared method | `\b(?:FastV\|SparseVLM\|PruMerge\|LLaVA-PruMerge\|ToMe\|TokenPacker\|PyramidDrop\|VisionZip\|DivPrune\|FitPrune\|VTW\|CDPruner\|TopV\|HiRED\|FasterVLM\|Dynamic-LLaVA\|LOOK-M\|VL-Cache\|MustDrop\|SparseVILA\|FastVLM\|VoCo-LLaMA\|LLaVA-Mini\|TRIM)\b` |
| BIT | bit width | `\b(?:W\d+A\d+\|INT[248]\|\d-bit\|\d bit\|ternary\|binar\w+\|FP8\|NF4)\b` |
| PARAM | parameter share | `\d+(?:\.\d+)?\s?%\s?(?:of (?:the )?)?(?:trainable \|total )?param\w*\|\d+(?:\.\d+)?\s?[MB] (?:trainable )?param\w*` |
| BENCH | benchmark | `\b(?:MME\|MMBench\|MMMU\|GQA\|VQAv2\|TextVQA\|POPE\|ScienceQA\|SEED-?Bench\|VizWiz\|OCRBench\|DocVQA\|ChartQA\|Video-?MME\|MVBench\|MLVU\|LongVideoBench\|EgoSchema\|MSVD\|MSRVTT\|ActivityNet\|RefCOCO\w*\|AI2D\|MathVista\|RealWorldQA)\b` |

## Step 2 — reading and recording

A language model (Claude, Anthropic; interactive session, September–October 2026) read the candidate sentences in the context of the full text and filled one row per entry with the fields below. Instruction (rules):

1. Record a time, memory, throughput or energy quantity only when the authors measured it on their own system; quantities quoted from other papers and theoretical estimates are not recorded. FLOPs are recorded in their own field but do not count as measured.
2. Copy each quantity in the paper's own units and wording, together with the sentence (or table caption) that supports it.
3. Leave a field empty ('—') when the paper reports no such quantity; do not infer.
4. Name the hardware only as the paper names it.

| Field | Definition |
|---|---|
| name | method name used by the authors |
| sub | sub-branch (Tables 3–7, column 3) |
| reduction | what is reduced and by how much: token budget (4.4), bit width (4.3), active/total parameters (4.1), trainable-parameter share (4.2), device budget (4.5) |
| flops | FLOPs reported by the authors (computed, not measured; does not count towards the grade) |
| speed_latency | time or speed-up measured by the authors on their own system |
| memory | memory measured by the authors on their own system |
| hardware | the devices named for those measurements; '—(not stated)' if none |
| accuracy_retained | accuracy relative to the unmodified model, as reported |
| compared_with | baselines in the efficiency comparison |
| code | public code link given in the paper |

## Step 3 — grading and checks

Grade A = public code and a measured time or memory cost; B = such a measurement without public code; C = no measured cost (FLOPs alone do not count).
Checks: a random sample of 30 extracted quantities compared with the papers (30/30 matched; main_survey/extraction_check/); every code link opened automatically and its repository listed (main_survey/check_code_links.py).

# -*- coding: utf-8 -*-
"""선정 논문 전문(txt)에서 비교 매트릭스 후보 근거 문장을 뽑는다 (2026-09-28).
   의료 서베이 감사와 같은 원칙: 수치는 저자가 자기 시스템에서 잰 값만, 근거 문장과 함께 저장.
   출력: main_survey/matrix_evidence_<branch>.jsonl (기계용) + .md (판독용)
   실행: python main_survey/extract_matrix_evidence.py 4.4"""
import csv, glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BR = sys.argv[1] if len(sys.argv) > 1 else "4.4"
FIELDS = {
 "SPEED": r"\d+(?:\.\d+)?\s?[x×]\s*(?:faster|speed-?up|acceleration|reduction)|speed-?up (?:of|by) \d|\d+(?:\.\d+)?\s?% (?:faster|reduction in (?:latency|time|FLOPs))",
 "FLOP":  r"\d+(?:\.\d+)?\s?[GTM]?FLOPs|FLOPs? (?:reduc|drop|decrease)\w* (?:by |to )?\d+(?:\.\d+)?\s?%|\d+(?:\.\d+)?\s?% (?:of (?:the )?)?FLOPs",
 "LAT":   r"\d+(?:\.\d+)?\s?(?:ms|milliseconds|seconds?|s)\b[^.]{0,60}(?:latency|per (?:image|sample|token|frame)|inference|prefill|decod|TTFT)|(?:latency|inference time|prefill time|TTFT|time to first token)[^.]{0,60}\d+(?:\.\d+)?\s?(?:ms|s|seconds?)",
 "MEM":   r"\d+(?:\.\d+)?\s?(?:GB|GiB|MB)\b[^.]{0,40}(?:memory|KV|cache|VRAM)|(?:memory|KV cache|VRAM)[^.]{0,60}\d+(?:\.\d+)?\s?(?:GB|GiB|MB|%)",
 "THR":   r"\d+(?:\.\d+)?\s?(?:tokens?/s|tokens per second|samples?/s|fps|FPS|QPS|images?/s)",
 "TOK":   r"\d+(?:\.\d+)?\s?% (?:of (?:the )?)?(?:visual|vision|image|video)? ?tokens|(?:prun|reduc|compress|retain|keep|drop)\w*[^.]{0,40}\d+(?:\.\d+)?\s?% of (?:the )?(?:visual |vision |image )?tokens|(?:from|to) \d{2,4} (?:visual |vision )?tokens|\d{2,4} tokens? (?:per|/) (?:image|frame)",
 "HW":    r"\b(?:NVIDIA )?(?:A100|A800|H100|H800|V100|A6000|A40|L40S?|RTX ?\d{4}|3090|4090|T4|Jetson[\w ]{0,15}|Orin|Snapdragon[\w ]{0,10}|Apple M\d|iPhone[\w ]{0,6}|TPU ?v\d|Ascend[\w ]{0,6}|CPU)\b",
 "ACC":   r"(?:accuracy|performance|score)[^.]{0,60}(?:drop|loss|degrad|decreas|retain|maintain|preserv|within)[^.]{0,40}\d+(?:\.\d+)?\s?%|\d+(?:\.\d+)?\s?% (?:of (?:the )?)?(?:original|baseline|full)[^.]{0,20}(?:performance|accuracy)|(?:retain|maintain|preserv|keep)\w* \d+(?:\.\d+)?\s?%",
 "FREE":  r"training-?free|plug-?and-?play|without (?:any )?(?:re-?)?training|no (?:additional |extra )?training|fine-?tun\w+ (?:is )?(?:required|needed)",
 "BASE":  r"\b(?:LLaVA(?:-(?:1\.5|NeXT|OneVision|Video))?|Qwen2?(?:\.5)?-VL|InternVL[\d.]*|MiniCPM-V|Phi-3-vision|BLIP-?2|Video-LLaVA|Mini-?Gemini|mPLUG-Owl|Idefics\d?|PaliGemma|Gemma ?3)\b",
 "CMP":   r"\b(?:FastV|SparseVLM|PruMerge|LLaVA-PruMerge|ToMe|TokenPacker|PyramidDrop|VisionZip|DivPrune|FitPrune|VTW|CDPruner|TopV|HiRED|FasterVLM|Dynamic-LLaVA|LOOK-M|VL-Cache|MustDrop|SparseVILA|FastVLM|VoCo-LLaMA|LLaVA-Mini|TRIM)\b",
 "BIT":   r"\b(?:W\d+A\d+|INT[248]|\d-bit|\d bit|ternary|binar\w+|FP8|NF4)\b",
 "PARAM": r"\d+(?:\.\d+)?\s?%\s?(?:of (?:the )?)?(?:trainable |total )?param\w*|\d+(?:\.\d+)?\s?[MB] (?:trainable )?param\w*",
 "BENCH": r"\b(?:MME|MMBench|MMMU|GQA|VQAv2|TextVQA|POPE|ScienceQA|SEED-?Bench|VizWiz|OCRBench|DocVQA|ChartQA|Video-?MME|MVBench|MLVU|LongVideoBench|EgoSchema|MSVD|MSRVTT|ActivityNet|RefCOCO\w*|AI2D|MathVista|RealWorldQA)\b",
}
RX = {k: re.compile(v, re.I) for k, v in FIELDS.items()}
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
SEL = "main_survey/selected_all.csv" if os.path.exists("main_survey/selected_all.csv") else "main_survey/selected_4.3_4.4.csv"
sel = [r for r in csv.DictReader(open(SEL, encoding="utf-8-sig")) if BR in r["branches"].split("/")]
out = []; md = [f"# 비교 매트릭스 근거 — {BR} ({len(sel)}편)\n"]
for r in sel:
    fs = glob.glob(f"main_survey/txt/{r['id']}*.txt")
    if not fs: md.append(f"\n## {r['id']} {r['title']}\n(전문 없음)\n"); continue
    t = open(fs[0], encoding="utf-8", errors="ignore").read()
    t = re.split(r"\n\s*(?:References|REFERENCES|Bibliography)\s*\n", t)[0]        # 참고문헌 이후 제거
    body = re.sub(r"\s+", " ", t)
    sents = SENT.split(body)
    ev = {k: [] for k in FIELDS}
    for s in sents:
        if len(s) > 600: continue
        for k, rx in RX.items():
            if rx.search(s) and len(ev[k]) < 8: ev[k].append(s.strip())
    counts = {k: len(v) for k, v in ev.items()}
    # 벤치마크·비교 대상·하드웨어·기반 모델은 고유 항목 집합으로도
    sets = {k: sorted(set(m.group(0) for m in RX[k].finditer(body)))[:25] for k in ("HW", "BASE", "CMP", "BENCH")}
    out.append({"id": r["id"], "title": r["title"], "mark": r["mark"], "chars": len(body), "counts": counts, "sets": sets, "evidence": ev})
    md.append(f"\n## {r['id']} [{r['mark']}] {r['title']}\n")
    md.append(f"- 기반 모델: {', '.join(sets['BASE']) or '—'}\n- 비교 대상: {', '.join(sets['CMP']) or '—'}\n- 하드웨어: {', '.join(sets['HW']) or '—'}\n- 벤치마크: {', '.join(sets['BENCH']) or '—'}")
    for k in ("FREE", "TOK", "BIT", "PARAM", "SPEED", "FLOP", "LAT", "MEM", "THR", "ACC"):
        if ev[k]: md.append(f"\n**{k}** ({counts[k]})"); md += [f"- {s[:320]}" for s in ev[k][:5]]
    md.append("")
json.dump(out, open(f"main_survey/matrix_evidence_{BR}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"main_survey/matrix_evidence_{BR}.md", "w", encoding="utf-8").write("\n".join(md))
print(f"{BR}: {len(out)}편 · 근거 문장 수", {k: sum(o['counts'][k] for o in out) for k in FIELDS})
print("하드웨어 없음:", [o["id"] for o in out if not o["sets"]["HW"]], "| 지연 없음:", [o["id"] for o in out if not o["evidence"]["LAT"]])

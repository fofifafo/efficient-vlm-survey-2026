# -*- coding: utf-8 -*-
"""CDPruner 공개판 감속 원인 진단을 로그로 남긴다(3차 리뷰 7번·원저자 이슈 근거, 2026-10-17 실행 예정).
   10/2 진단(profile_cdpruner3.py)은 결과를 cdpruner_fix.py 주석에만 적어 두었다 → 같은 내용을 json 으로 기록.
   한 프로세스에 한 변형(공개판 cdpruner / 수정판 cdpruner_fix)만 올린다(메모리 상태가 섞이지 않도록).
   기록: 로드 전후 GPU 메모리(PyTorch 할당·예약, cudaMemGetInfo 여유/전체, nvidia-smi 사용량 = 화면 등 다른 프로세스 포함),
         GQA n 문항의 TTFT(첫 토큰까지, harness 와 같은 표본 앞 n개)와 10문항마다 예약 메모리·할당 재시도 횟수,
         CLIP 타워 단독 시간: 기본 스트림 / 래퍼(공개판은 매 호출 보조 스트림 2개).
   실행: python profile_cdpruner_diag.py --method cdpruner --setting default --n 50
         → ~/vlmbench/results_profile/cdpruner_diag_<method>_<setting>.json"""
import argparse, importlib, json, os, random, statistics, subprocess, sys, time
import torch

def smi():
    try:
        o = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=20).stdout.strip()
        u, t = [float(x) for x in o.split(",")[:2]]; return dict(smi_used_gb=round(u / 1024, 2), smi_total_gb=round(t / 1024, 2))
    except Exception as e: return dict(smi_error=str(e))
def mem(tag):
    free, total = torch.cuda.mem_get_info(); st = torch.cuda.memory_stats()
    d = dict(tag=tag, alloc_gb=round(torch.cuda.memory_allocated() / 2**30, 2), reserved_gb=round(torch.cuda.memory_reserved() / 2**30, 2),
             reserved_peak_gb=round(st.get("reserved_bytes.all.peak", 0) / 2**30, 2), free_gb=round(free / 2**30, 2), total_gb=round(total / 2**30, 2),
             alloc_retries=st.get("num_alloc_retries", 0), device_allocs=st.get("num_device_alloc", 0), **smi())
    print("MEM", json.dumps(d), flush=True); return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True, choices=["cdpruner", "cdpruner_fix"]); ap.add_argument("--setting", default="default"); ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--model", default=os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"))
    ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results_profile"))
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    log = dict(method=a.method, setting=a.setting, gpu=torch.cuda.get_device_name(0), torch=torch.__version__, mem=[])
    torch.cuda.init(); log["mem"].append(mem("before_load"))
    M = importlib.import_module(f"methods.{a.method}")
    gen, meta = M.load(a.model, setting=a.setting)
    log["mem"].append(mem("after_load")); torch.cuda.empty_cache(); log["mem"].append(mem("after_empty_cache"))   # harness 와 같이 로드 후 캐시 해제
    from datasets import load_dataset
    ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
    idx = random.Random(20261001).sample(range(len(ds)), 500)[: a.n]
    imgs = {r["id"]: r["image"] for r in load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]}
    ttft = []
    for k, i in enumerate(idx):
        r = ds[i]; o = gen(imgs[r["imageId"]].convert("RGB"), r["question"], 1); ttft.append(o["ttft_s"] * 1000)
        if k % 10 == 9: log["mem"].append(mem(f"after_{k + 1}_questions")); print(f"{k + 1}/{a.n} ttft median so far {statistics.median(ttft[5:] or ttft):.1f} ms", flush=True)
    t = ttft[5:]
    log.update(ttft_ms_median=statistics.median(t), ttft_ms_p90=sorted(t)[int(0.9 * (len(t) - 1))], ttft_ms_max=max(t), n=len(t))
    # CLIP 타워 단독: 기본 스트림에서 직접 vs 방법의 래퍼(공개판 = 호출마다 새 보조 스트림 2개)
    mdl = [c.cell_contents for c in gen.__closure__ if hasattr(c.cell_contents, "generate")][0]
    tower = mdl.get_model().get_vision_tower()
    x = torch.randn(1, 3, 336, 336, device="cuda", dtype=torch.float16); q = "What color is the car?"
    def T(f, n=10):
        f(); torch.cuda.synchronize(); s = []
        for _ in range(n):
            t0 = time.perf_counter(); f(); torch.cuda.synchronize(); s.append((time.perf_counter() - t0) * 1000)
        return dict(median_ms=round(statistics.median(s), 2), max_ms=round(max(s), 2))
    with torch.inference_mode():
        log["clip_direct_default_stream"] = T(lambda: tower.vision_tower(x, output_hidden_states=True))
        log["tower_wrapper_with_text"] = T(lambda: tower(x, texts=q))
    log["mem"].append(mem("end"))
    log["note"] = ("reserved > total - (smi_used before load) means the allocator pools no longer fit beside other GPU users (display); "
                   "alloc_retries > 0 means the caching allocator had to free and retry cudaMalloc")
    os.makedirs(a.out, exist_ok=True); p = os.path.join(a.out, f"cdpruner_diag_{a.method}_{a.setting}.json"); json.dump(log, open(p, "w"), indent=1)
    print("SUMMARY", json.dumps({k: v for k, v in log.items() if k != "mem"}), flush=True)
    print("MEM_PEAK", json.dumps({k: max(m.get(k, 0) for m in log["mem"]) for k in ("reserved_gb", "reserved_peak_gb", "alloc_retries", "smi_used_gb")}), flush=True)

if __name__ == "__main__":
    main()

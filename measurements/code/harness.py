# -*- coding: utf-8 -*-
"""측정 하네스: 방법별 TTFT·종단 지연·피크 VRAM·전력/에너지 (2026-10-01).
   실행: python harness.py --method base --n 500 [--runs 5] [--out ~/vlmbench/results]
   방법 플러그인은 bench/methods/<name>.py 가 load(model_path, setting) -> (generate_fn, meta) 를 제공한다.
   generate_fn(image: PIL.Image, question: str, max_new_tokens:int) -> dict(answer, n_vis_tokens, ttft_s, total_s)
   같은 500 샘플(GQA testdev 에서 seed 20261001 로 뽑음)을 모든 방법에 공통 사용. 전력은 NVML 50 ms 샘플링을 사다리꼴 적분."""
import argparse, importlib, json, os, sys, time, threading, statistics, random
import torch, pynvml
from PIL import Image

def power_sampler(handle, stop, buf, period=0.05):
    while not stop.is_set():
        buf.append((time.perf_counter(), pynvml.nvmlDeviceGetPowerUsage(handle) / 1000)); time.sleep(period)

def energy_j(samples, t0, t1):
    s = [(t, p) for t, p in samples if t0 <= t <= t1]
    return sum((s[i + 1][0] - s[i][0]) * (s[i][1] + s[i + 1][1]) / 2 for i in range(len(s) - 1)) if len(s) > 1 else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True); ap.add_argument("--n", type=int, default=500); ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--model", default=os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"))
    ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results")); ap.add_argument("--setting", default="default")
    ap.add_argument("--max_new_tokens", type=int, default=32)
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    mod = importlib.import_module(f"methods.{a.method}")
    gen, meta = mod.load(a.model, setting=a.setting)
    import torch as _t; _t.cuda.empty_cache(); _t.cuda.reset_peak_memory_stats()   # 로드 시 임시 피크(fp32 보조 모델 등)로 예약된 캐시 해제 — 16 GB 카드에서 호스트 페이징 방지 (10/2 CDPruner 진단)
    from datasets import load_dataset
    ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
    idx = random.Random(20261001).sample(range(len(ds)), a.n)
    imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
    img_by_id = {r["id"]: r["image"] for r in imgs}
    pynvml.nvmlInit(); h = pynvml.nvmlDeviceGetHandleByIndex(0)
    rows = []
    for run in range(a.runs):
        torch.cuda.reset_peak_memory_stats(); torch.cuda.synchronize()
        buf, stop = [], threading.Event(); th = threading.Thread(target=power_sampler, args=(h, stop, buf), daemon=True); th.start()
        t_run0 = time.perf_counter(); ttfts, tots, nvis = [], [], []
        for k, i in enumerate(idx):
            r = ds[i]; img = img_by_id[r["imageId"]].convert("RGB")
            o = gen(img, r["question"], a.max_new_tokens)
            if k % 25 == 0 or k == a.n - 1:      # 진행 상황 파일 (status_push 가 GitHub 에 올린다)
                el = time.perf_counter() - t_run0; done_total = run * a.n + k + 1; total = a.runs * a.n
                eta = (el / max(k + 1, 1)) * (a.n - k - 1) + (a.runs - run - 1) * (el / max(k + 1, 1)) * a.n
                json.dump(dict(method=a.method, setting=a.setting, run=run + 1, runs=a.runs, k=k + 1, n=a.n, pct=round(100 * done_total / total, 1),
                               sec_per_sample=round(el / max(k + 1, 1), 2), eta_min=round(eta / 60, 1), updated=time.strftime("%Y-%m-%d %H:%M:%S")),
                          open(os.path.expanduser("~/vlmbench/results/progress.json"), "w"))
            if not (run == 0 and k < 5):          # 첫 5개는 warm-up — 통계에서 제외
                ttfts.append(o["ttft_s"]); tots.append(o["total_s"]); nvis.append(o.get("n_vis_tokens", -1))
        torch.cuda.synchronize(); t_run1 = time.perf_counter(); stop.set(); th.join()
        e = energy_j(buf, t_run0, t_run1); n_eff = len(tots)
        rows.append(dict(run=run, n=n_eff, ttft_ms_median=1000 * statistics.median(ttfts), ttft_ms_p90=1000 * sorted(ttfts)[int(0.9 * n_eff)],
                         total_ms_median=1000 * statistics.median(tots), peak_vram_gb=torch.cuda.max_memory_allocated() / 2**30,
                         energy_j_per_sample=e / n_eff, mean_power_w=(e / (t_run1 - t_run0)) if t_run1 > t_run0 else 0,
                         n_vis_tokens=statistics.median(nvis) if nvis else -1))
        print(json.dumps(rows[-1]))
    summ = {k: statistics.median(r[k] for r in rows) for k in rows[0] if k != "run"}
    summ.update(method=a.method, setting=a.setting, meta=meta, gpu=torch.cuda.get_device_name(0), torch=torch.__version__, runs=rows)
    os.makedirs(f"{a.out}/{a.method}", exist_ok=True)
    json.dump(summ, open(f"{a.out}/{a.method}/latency_{a.setting}.json", "w"), indent=1)
    print("SUMMARY", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in summ.items() if k not in ("runs", "meta")})

if __name__ == "__main__":
    main()

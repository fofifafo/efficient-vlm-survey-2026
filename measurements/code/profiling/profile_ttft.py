# -*- coding: utf-8 -*-
"""2차 리뷰 M2(10/16): TTFT 를 GPU 계산 시간과 호스트(CPU) 쪽 시간으로 나눈다.
   방법 플러그인(bench/methods/<name>.py)의 generate_fn 을 그대로 쓰고 max_new_tokens=1 로 첫 토큰까지만 실행한다.
   문항마다 (1) 프로파일러 없이 TTFT(wall) 를 재고, (2) 같은 문항을 torch.profiler(CUDA 활동만)로 다시 돌려
   GPU 에서 커널·메모리 복사가 실제로 돈 시간의 합집합(busy)을 구한다. 호스트 쪽 = wall − busy (GPU 가 놀며 CPU 를 기다린 시간).
   같은 GQA testdev 표본(seed 20261001)의 앞 n 문항, 워밍업 5문항 제외, 중앙값 보고.
   실행: python profile_ttft.py --method vispruner --setting default --n 100 → ~/vlmbench/results_profile/<method>_<setting>.json"""
import argparse, importlib, json, os, random, statistics, sys, time
import torch
from torch.profiler import profile, ProfilerActivity

def busy_ms(prof):
    iv = []
    for e in prof.events():
        dt = str(getattr(e, "device_type", ""))
        if "CUDA" in dt and e.time_range.end > e.time_range.start:
            iv.append((e.time_range.start, e.time_range.end))
    iv.sort(); tot = 0; cur_s = cur_e = None
    for s, e in iv:
        if cur_e is None or s > cur_e:
            if cur_e is not None: tot += cur_e - cur_s
            cur_s, cur_e = s, e
        else: cur_e = max(cur_e, e)
    if cur_e is not None: tot += cur_e - cur_s
    return tot / 1000.0, len(iv)          # µs → ms

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default"); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--model", default=os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"))
    ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results_profile"))
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    gen, meta = importlib.import_module(f"methods.{a.method}").load(a.model, setting=a.setting)
    torch.cuda.empty_cache()
    from datasets import load_dataset
    ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
    idx = random.Random(20261001).sample(range(len(ds)), 500)[: a.n]          # harness.py 와 같은 500 표본의 앞 n 개
    imgs = {r["id"]: r["image"] for r in load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]}
    rows = []
    for k, i in enumerate(idx):
        r = ds[i]; img = imgs[r["imageId"]].convert("RGB")
        o = gen(img, r["question"], 1); wall = o["ttft_s"] * 1000
        with profile(activities=[ProfilerActivity.CUDA]) as prof:
            gen(img, r["question"], 1)
        torch.cuda.synchronize(); busy, nk = busy_ms(prof)
        if k >= 5: rows.append(dict(wall_ms=wall, gpu_busy_ms=busy, host_ms=max(0.0, wall - busy), kernels=nk))
        if k % 20 == 0: print(f"{k}/{a.n} wall {wall:.1f} ms busy {busy:.1f} ms", flush=True)
    med = lambda key: statistics.median(x[key] for x in rows)
    res = dict(method=a.method, setting=a.setting, n=len(rows), wall_ms=med("wall_ms"), gpu_busy_ms=med("gpu_busy_ms"), host_ms=med("host_ms"),
               host_share=statistics.median(x["host_ms"] / x["wall_ms"] for x in rows), kernels=med("kernels"),
               gpu=torch.cuda.get_device_name(0), torch=torch.__version__, meta={k: str(v) for k, v in meta.items()}, rows=rows,
               note="wall = TTFT without profiler (max_new_tokens=1, same window as harness); gpu_busy = union of CUDA kernel/memcpy intervals in a second, profiled run")
    os.makedirs(a.out, exist_ok=True); p = os.path.join(a.out, f"{a.method}_{a.setting}.json"); json.dump(res, open(p, "w"), indent=1)
    print("SUMMARY", json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in res.items() if k not in ("rows", "meta")}))

if __name__ == "__main__":
    main()

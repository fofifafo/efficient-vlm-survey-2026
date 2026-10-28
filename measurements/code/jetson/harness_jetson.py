# -*- coding: utf-8 -*-
"""Jetson Orin Nano 지연·에너지 하네스 (2026-10-12). 데스크톱 harness.py 와 같은 프로토콜(GQA test-dev 500문항, 시드 20261001,
   첫 5개 워밍업 제외, 실행별 중앙값의 중앙값, 최대 32토큰), 다른 점만:
   - 문항·이미지: export_gqa500.py 로 내보낸 로컬 파일(~/vlmbench/data/gqa500)  ← datasets 불필요
   - 전력: NVML 대신 보드 INA3221 의 VDD_IN(모듈 입력 전체) 전압×전류, 50 ms 간격 → 적분. VDD_CPU_GPU_CV·VDD_SOC 도 함께 기록
   - 메모리: torch 최대 할당 + 통합 메모리 시스템 사용량 최대(MemTotal − MemAvailable)
   - 모델: methods_jetson/<m>.py (4비트 NF4 로드) 사용
   실행: python harness_jetson.py --method base4 --setting default --n 500 --runs 5"""
import argparse, glob, importlib, json, os, statistics, sys, threading, time
import torch
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))

def rails():
    """INA3221 레일 경로: {label: (in_path, curr_path)}"""
    out = {}
    for h in glob.glob("/sys/bus/i2c/drivers/ina3221/*/hwmon/hwmon*"):
        for i in (1, 2, 3):
            lab = open(f"{h}/in{i}_label").read().strip()
            out[lab] = (f"{h}/in{i}_input", f"{h}/curr{i}_input")
    return out
def read_w(p):  # mV × mA → W
    return int(open(p[0]).read()) * int(open(p[1]).read()) / 1e6
def mem_used_gb():
    m = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo")}
    return (m["MemTotal"] - m["MemAvailable"]) / 2**20
def sampler(R, stop, buf, peak, period=0.05):
    while not stop.is_set():
        buf.append((time.perf_counter(), {k: read_w(p) for k, p in R.items()})); peak[0] = max(peak[0], mem_used_gb()); time.sleep(period)
def energy(buf, t0, t1, key):
    s = [(t, w[key]) for t, w in buf if t0 <= t <= t1]
    return sum((b[0] - a[0]) * (a[1] + b[1]) / 2 for a, b in zip(s, s[1:]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default")
    ap.add_argument("--n", type=int, default=500); ap.add_argument("--runs", type=int, default=5); ap.add_argument("--max_new_tokens", type=int, default=32)
    ap.add_argument("--model", default=f"{WORK}/models/llava-v1.5-7b-st"); ap.add_argument("--data", default=f"{WORK}/data/gqa500")
    ap.add_argument("--out", default=f"{WORK}/results_jetson")
    a = ap.parse_args()
    sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))      # methods_jetson, 그리고 bench/methods(_llava_common)
    R = rails(); assert "VDD_IN" in R, R
    idle = statistics.median(read_w(R["VDD_IN"]) for _ in range(20) if not time.sleep(0.05))
    t_load = time.perf_counter(); mod = importlib.import_module(f"methods_jetson.{a.method}")
    gen, meta = mod.load(a.model, setting=a.setting); t_load = time.perf_counter() - t_load
    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    S = [json.loads(l) for l in open(f"{a.data}/samples.jsonl", encoding="utf-8")][: a.n]
    imgs = {s["image"]: Image.open(f"{a.data}/{s['image']}").convert("RGB") for s in S}
    os.makedirs(f"{a.out}/{a.method}", exist_ok=True); rows = []
    for run in range(a.runs):
        torch.cuda.reset_peak_memory_stats(); torch.cuda.synchronize()
        buf, stop, peak = [], threading.Event(), [mem_used_gb()]
        th = threading.Thread(target=sampler, args=(R, stop, buf, peak), daemon=True); th.start()
        t0 = time.perf_counter(); ttfts, tots, nvis = [], [], []
        for k, s in enumerate(S):
            o = gen(imgs[s["image"]], s["question"], a.max_new_tokens)
            if k % 25 == 0 or k == len(S) - 1:
                el = time.perf_counter() - t0
                json.dump(dict(method=a.method, setting=a.setting, run=run + 1, runs=a.runs, k=k + 1, n=len(S), sec_per_sample=round(el / (k + 1), 2),
                               eta_min=round((el / (k + 1)) * ((a.runs - run) * len(S) - k - 1) / 60, 1), updated=time.strftime("%H:%M:%S")),
                          open(f"{a.out}/progress.json", "w"))
            if not (run == 0 and k < 5):
                ttfts.append(o["ttft_s"]); tots.append(o["total_s"]); nvis.append(o.get("n_vis_tokens", -1))
        torch.cuda.synchronize(); t1 = time.perf_counter(); stop.set(); th.join(); n = len(tots)
        e = {k: energy(buf, t0, t1, k) for k in R}
        rows.append(dict(run=run, n=n, ttft_ms_median=1000 * statistics.median(ttfts), ttft_ms_p90=1000 * sorted(ttfts)[int(0.9 * n)],
                         total_ms_median=1000 * statistics.median(tots), peak_alloc_gb=torch.cuda.max_memory_allocated() / 2**30, peak_sys_used_gb=peak[0],
                         energy_j_per_sample=e["VDD_IN"] / n, mean_power_w=e["VDD_IN"] / (t1 - t0),
                         rail_mean_w={k: v / (t1 - t0) for k, v in e.items()}, n_vis_tokens=statistics.median(nvis) if nvis else -1))
        print(json.dumps(rows[-1]), flush=True)
    num = [k for k in rows[0] if isinstance(rows[0][k], (int, float)) and k != "run"]
    summ = {k: statistics.median(r[k] for r in rows) for k in num}
    summ.update(method=a.method, setting=a.setting, meta=meta, device=torch.cuda.get_device_name(0), torch=torch.__version__,
                idle_power_w=idle, load_s=t_load, power_mode=os.popen("nvpmodel -q 2>/dev/null").read().split("\n")[0], runs=rows)
    json.dump(summ, open(f"{a.out}/{a.method}/latency_{a.setting}.json", "w"), indent=1)
    print("SUMMARY", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in summ.items() if k not in ("runs", "meta")})

if __name__ == "__main__":
    main()

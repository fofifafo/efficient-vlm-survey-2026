# -*- coding: utf-8 -*-
"""정확도 평가 러너: 플러그인(methods/<m>.py)으로 GQA·POPE·TextVQA·MME 전량 추론 → results/<method>/acc_<setting>/preds_<task>.jsonl → score.py 채점.
   프롬프트는 LLaVA 공식 평가 스크립트와 동일(vicuna_v1 + "Answer the question using a single word or phrase."; TextVQA 는 OCR 참조 토큰 포함).
   재개 가능: 이미 기록된 question id 는 건너뜀.  사용: python eval_acc.py --method base --setting default [--tasks gqa,pope,textvqa,mme] [--n 0(전량)]"""
import argparse, ast, importlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _lst(v):
    """datasets 가 list 로 주면 그대로, 문자열 표현이면 파싱"""
    if v is None: return []
    return list(v) if isinstance(v, (list, tuple)) else ast.literal_eval(v)

def iter_task(task, n):
    from datasets import load_dataset
    if task == "gqa":
        ds = load_dataset("lmms-lab/GQA", "testdev_balanced_instructions")["testdev"]
        imgs = load_dataset("lmms-lab/GQA", "testdev_balanced_images")["testdev"]
        img_by_id = {r["id"]: r["image"] for r in imgs}
        for r in (ds if not n else ds.select(range(n))):
            yield r["id"], img_by_id[r["imageId"]], r["question"], dict(answer=r["answer"])
    elif task == "pope":
        ds = load_dataset("lmms-lab/POPE")["test"]
        for r in (ds if not n else ds.select(range(n))):
            yield f"pope{r['id']}", r["image"], r["question"], dict(answer=r["answer"], category=r["category"], question_id=r["question_id"])   # question_id 는 범주 안에서만 유일 → id 사용
    elif task == "textvqa":
        ds = load_dataset("lmms-lab/textvqa")["validation"]
        for r in (ds if not n else ds.select(range(n))):
            ocr = _lst(r["ocr_tokens"])
            q = (f"Reference OCR token: {', '.join(ocr)}\n" if ocr else "") + r["question"]   # LLaVA 공식 textvqa 평가와 동일
            yield r["question_id"], r["image"], q, dict(answers=_lst(r["answers"]))
    elif task == "mme":
        ds = load_dataset("lmms-lab/MME")["test"]
        for i, r in enumerate(ds if not n else ds.select(range(n))):
            yield f"{r['question_id']}#{i}", r["image"], r["question"], dict(answer=r["answer"], category=r["category"], image_id=r["question_id"])
    else: raise ValueError(task)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default")
    ap.add_argument("--tasks", default="gqa,pope,textvqa,mme"); ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--model", default=os.path.expanduser("~/vlmbench/models/llava-v1.5-7b"))
    ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results")); ap.add_argument("--max_new_tokens", type=int, default=16)
    a = ap.parse_args()
    gen, meta = importlib.import_module(f"methods.{a.method}").load(a.model, setting=a.setting)
    import torch as _t; _t.cuda.empty_cache(); _t.cuda.reset_peak_memory_stats()   # 로드 시 임시 피크(fp32 보조 모델 등)로 예약된 캐시 해제 — 16 GB 카드에서 호스트 페이징 방지 (10/2 CDPruner 진단)
    d = f"{a.out}/{a.method}/acc_{a.setting}"; os.makedirs(d, exist_ok=True)
    json.dump(dict(meta=meta, max_new_tokens=a.max_new_tokens, prompt="vicuna_v1+single-word; textvqa with OCR reference tokens"), open(f"{d}/meta.json", "w"), indent=1)
    prog = os.path.expanduser("~/vlmbench/results/progress.json")
    for task in a.tasks.split(","):
        f = f"{d}/preds_{task}.jsonl"
        done = set()
        if os.path.exists(f):
            for l in open(f, encoding="utf-8"): done.add(json.loads(l)["qid"])
        t0 = time.perf_counter(); k = 0
        with open(f, "a", encoding="utf-8") as fo:
            for qid, img, q, extra in iter_task(task, a.n):
                if qid in done: continue
                o = gen(img.convert("RGB"), q, a.max_new_tokens)
                extra.update(qid=qid, pred=o["answer"], n_vis_tokens=o.get("n_vis_tokens", -1))
                fo.write(json.dumps(extra, ensure_ascii=False) + "\n"); k += 1; done.add(qid)
                if k % 50 == 0:
                    fo.flush(); el = time.perf_counter() - t0
                    json.dump(dict(method=a.method, setting=f"acc_{a.setting}/{task}", run=1, runs=1, k=len(done), n=-1, pct=-1,
                                   sec_per_sample=round(el / k, 2), eta_min=-1, updated=time.strftime("%Y-%m-%d %H:%M:%S")), open(prog, "w"))
        print(f"{task}: +{k} preds in {(time.perf_counter() - t0) / 60:.1f} min -> {f}", flush=True)
    os.system(f"{sys.executable} {os.path.dirname(os.path.abspath(__file__))}/score.py --method {a.method} --setting {a.setting} --out {a.out}")

if __name__ == "__main__":
    main()

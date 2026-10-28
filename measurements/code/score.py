# -*- coding: utf-8 -*-
"""자체 채점기 (lmms-eval 대체 — 버전 충돌 회피, 규칙 공개). 2026-10-01
   GQA: 정규화 후 정확 일치. POPE: yes/no 정확도·F1(공식). TextVQA: VQA 정확도(10 annotator soft, 공식 정규화 간략판). MME: 하위과제별 acc + acc+ 합(공식).
   사용: python score.py --method base   (results/<method>/preds_<task>.jsonl 을 읽어 results/<method>/accuracy.json 생성)"""
import argparse, json, os, re, collections
PUNCT = re.compile(r"[\"'\.,!?;:()\[\]\-]")
NUMS = {"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","ten":"10"}
ARTS = {"a","an","the"}
def norm(s):
    s = s.lower().strip(); s = PUNCT.sub(" ", s)
    w = [NUMS.get(t, t) for t in s.split() if t not in ARTS]
    return " ".join(w)
def yesno(s):
    s = s.lower().strip()
    return "yes" if s.startswith("yes") else ("no" if s.startswith("no") else "other")

def score_gqa(rows):
    return {"acc": sum(norm(r["pred"]) == norm(r["answer"]) for r in rows) / len(rows), "n": len(rows)}
def score_pope(rows):
    tp = fp = fn = tn = 0
    for r in rows:
        p, g = yesno(r["pred"]), r["answer"].lower().strip()
        if p == "yes" and g == "yes": tp += 1
        elif p == "yes" and g == "no": fp += 1
        elif p != "yes" and g == "yes": fn += 1
        else: tn += 1
    prec = tp / max(tp + fp, 1); rec = tp / max(tp + fn, 1)
    return {"acc": (tp + tn) / len(rows), "f1": 2 * prec * rec / max(prec + rec, 1e-9), "yes_ratio": (tp + fp) / len(rows), "n": len(rows)}
def score_textvqa(rows):
    tot = 0.0
    for r in rows:
        p = norm(r["pred"]); gts = [norm(a) for a in r["answers"]]
        tot += min(1.0, sum(g == p for g in gts) / 3.0)      # 공식: min(1, #match/3)
    return {"acc": tot / len(rows), "n": len(rows)}
def score_mme(rows):
    by = collections.defaultdict(list)
    for r in rows: by[r["category"]].append(r)
    out = {}; perc = cog = 0.0
    PERC = {"existence","count","position","color","posters","celebrity","scene","landmark","artwork","OCR"}
    for cat, rs in by.items():
        img = collections.defaultdict(list)
        for r in rs: img[r["image_id"]].append(yesno(r["pred"]) == r["answer"].lower().strip())
        acc = sum(sum(v) for v in img.values()) / sum(len(v) for v in img.values())
        accp = sum(all(v) for v in img.values()) / len(img)
        out[cat] = {"acc": acc, "acc_plus": accp, "score": 100 * (acc + accp)}
        (perc if cat in PERC else cog)
        if cat in PERC: perc += out[cat]["score"]
        else: cog += out[cat]["score"]
    out["perception_total"] = perc; out["cognition_total"] = cog; return out

SCORERS = {"gqa": score_gqa, "pope": score_pope, "textvqa": score_textvqa, "mme": score_mme}
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--method", required=True); ap.add_argument("--setting", default="default"); ap.add_argument("--out", default=os.path.expanduser("~/vlmbench/results")); a = ap.parse_args()
    d = f"{a.out}/{a.method}/acc_{a.setting}"; res = {}
    for task, fn in SCORERS.items():
        f = f"{d}/preds_{task}.jsonl"
        if os.path.exists(f):
            rows = [json.loads(l) for l in open(f, encoding="utf-8")]; res[task] = fn(rows); print(task, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res[task].items()} if task != "mme" else {k: round(v, 1) for k, v in res[task].items() if k.endswith("total")})
    json.dump(res, open(f"{d}/accuracy.json", "w"), indent=1); print("saved", f"{d}/accuracy.json")

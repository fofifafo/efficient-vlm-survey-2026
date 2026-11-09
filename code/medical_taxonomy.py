#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""의료 VLM 1,450편의 분류체계를 데이터에서 뽑는다 (서베이 4장 = 목차).

세 축으로 자른다:
  A. 임상 영역 / 영상 모달리티  — 무엇을 보는가
  B. 과제                       — 무엇을 하는가
  C. 방법                       — 어떻게 만드는가
  D. 관심사                     — 무엇을 걱정하는가 (열린 과제의 재료)
실행: python medical_taxonomy.py
"""
import re, sys, csv, json, os
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8"); sys.path.insert(0, ".")
from arxiv_scrape import extract_keywords, load_cache

# 2026-09-07 교차검증 후 엄격화: bare 'diagnos' 제거 (비의료 17% 누출 원인). healthcare_cut.py / fetch_citations.py 와 동일 유지.
MED = re.compile(r"medical|clinical|radiolog|patholog|patient|biomedical|chest x-?ray|\bCXR\b|CT scan|\bMRI\b|\bEHR\b|hospital|healthcare|health care|physician|nursing|surgery|surgical|oncolog|dermatolog|ophthalmolog|endoscop|histolog|whole[- ]slide|ultrasound|fundus|\bECG\b", re.I)
CORE = {"mllm", "vision-language-model", "visual-instruction-tuning"}

AXES = {
 "A. 임상 영역·모달리티": [
   ("방사선 — X-ray/CXR",      r"chest x-?ray|\bCXR\b|radiograph|x-?ray"),
   ("방사선 — CT/MRI (3D)",    r"\bCT\b|\bMRI\b|volumetric|3D medical|computed tomography|magnetic resonance"),
   ("병리 — 조직/WSI",          r"patholog|histolog|whole[- ]slide|\bWSI\b|biopsy"),
   ("안과 — 안저/OCT",          r"ophthalm|fundus|retina|\bOCT\b"),
   ("피부과",                   r"dermatolog|skin lesion|skin disease"),
   ("내시경·수술 영상",          r"endoscop|surgical (video|scene)|laparoscop|surgery video|colonoscop"),
   ("초음파",                   r"ultrasound|sonograph|echocardio"),
   ("생체신호 (ECG/EEG)",       r"\bECG\b|\bEKG\b|\bEEG\b|electrocardio"),
   ("치과·구강",                r"dental|oral (cavity|health)|tooth|teeth"),
   ("전자의무기록·문서",         r"\bEHR\b|electronic health record|clinical note|discharge summary|medical record"),
   ("일반/다중 모달리티",        r"multi[- ]?modal medical|across modalities|diverse medical imaging|multiple imaging modalit"),
 ],
 "B. 과제": [
   ("판독문 생성",              r"report generation|radiology report|generate (a |the )?report|report writing"),
   ("의료 VQA",                 r"\bVQA\b|visual question answering|question[- ]answering"),
   ("진단·분류",                r"diagnos|classif|disease (detection|prediction|identification)"),
   ("병변 탐지·그라운딩",        r"lesion detection|grounding|localiz|bounding box|abnormality detection"),
   ("분할",                    r"segment"),
   ("검색·RAG",                r"retriev|\bRAG\b|retrieval[- ]augmented"),
   ("임상 의사결정·추론",        r"clinical (decision|reasoning)|differential diagnosis|treatment (plan|recommend)|triage"),
   ("의학 교육·시험",           r"medical (exam|licens|education)|USMLE|board exam|medical student"),
   ("환자 소통·상담",           r"patient (communication|education|conversation)|health assistant|chatbot|consultation"),
   ("수술 보조",               r"surgical (assist|guidance|phase|skill)|intraoperative"),
 ],
 "C. 방법": [
   ("범용 VLM 파인튜닝 (LLaVA계)", r"LLaVA|fine[- ]tun\w* (a |the )?(general|open|pretrained)|adapt\w* (a |the )?general"),
   ("도메인 사전학습 (CLIP계)",    r"BiomedCLIP|MedCLIP|PubMedCLIP|contrastive|CLIP"),
   ("명령어 튜닝·데이터 구축",     r"instruction[- ]tun|instruction data|instruction[- ]following dataset|curated dataset|we (build|construct|introduce) (a |an )?(new |large[- ]scale )?dataset"),
   ("검색 증강",                 r"retrieval[- ]augmented|\bRAG\b|knowledge (base|graph) (augment|enhanc|inject)"),
   ("에이전트·도구 사용",          r"\bagent|tool[- ]use|tool[- ]calling|multi[- ]agent"),
   # 어휘 오염 주의: bare 'reasoning' 은 방법과 무관하게 급증(2024 13% → 2026 45%).
   # 구체 기법만 세면 3.6 → 14.0%. 두 가지를 분리해서 둘 다 보고할 것.
   ("추론 기법 (CoT/RL/GRPO/DPO)", r"chain[- ]of[- ]thought|reinforcement learning|\bRL\b|\bGRPO\b|\bDPO\b|\bRLHF\b|R1[- ]style|reasoning (model|trace|chain)"),
   ("추론 언급 (bare, 어휘)",       r"reasoning"),
   ("경량화·효율",                r"efficien|lightweight|quantiz|distill|\bLoRA\b|parameter[- ]efficient|on[- ]device|token (prun|compress)"),
   ("연합·프라이버시",            r"federated|privacy[- ]preserving|differential privacy|de[- ]identif"),
 ],
 "D. 관심사 (열린 과제 재료)": [
   # 'reliab' 이 reliable/reliability 로 광범위 매칭 → 20→42% 급증은 어휘. 명시적 hallucinat 은 10→13% (n.s.).
   ("환각 (명시적)",             r"hallucinat"),
   ("신뢰성 어휘 (넓게)",         r"hallucinat|factual|faithful|reliab"),
   ("벤치마크·평가",             r"benchmark|evaluation (framework|protocol|suite)|we evaluate|systematic evaluation"),
   ("안전·오용",                r"safety|jailbreak|adversarial|misuse|harm"),
   ("공정성·편향",              r"fairness|demographic|disparit|equit|\bbias(ed)? (against|toward|across)|algorithmic bias|racial|gender bias"),  # 9/9 수정: generic bias 제외
   ("설명가능성",               r"explainab|interpretab|attention map|saliency"),
   ("데이터 부족·희소",          r"data[- ]scarc|low[- ]resource|few[- ]shot|limited (annotat|label|data)"),
   ("임상 검증·실사용",          r"clinical (validation|trial|deployment|practice)|real[- ]world|prospective|reader study|radiologist(s)? (evaluat|rat|prefer)"),
   ("규제·윤리",                r"\bregulat(ory|ion|ions|ors?)\b|\bFDA\b|\bethic|accountab|\bliabilit"),  # 9/9 수정: liabilit 가 re-liabilit-y 에 매칭되던 버그
 ],
}
AXC = {ax: [(n, re.compile(p, re.I)) for n, p in items] for ax, items in AXES.items()}

papers, _ = load_cache(); papers = list(papers.values())
for p in papers:
    p["kw"] = extract_keywords(f"{p['title']}\n{p['abstract']}"); p["t"] = p["title"] + " " + p["abstract"]
def is_med(p): return bool(MED.search(p["title"])) or len(MED.findall(p["abstract"])) >= 2
med = [p for p in papers if (p["kw"] & CORE) and is_med(p)]
N = len(med)
years = Counter(p["date"][:4] for p in med)
print(f"의료 VLM {N}편  ({'  '.join(f'{y}:{c}' for y,c in sorted(years.items()))})\n")

CIT = {}
if os.path.exists("citations.json"):
    CIT = {k: v for k, v in json.load(open("citations.json", encoding="utf-8")).items() if v.get("c") is not None}

rows_out = []
for ax, items in AXC.items():
    print(f"══ {ax} ══")
    tally = []
    for name, rx in items:
        hit = [p for p in med if rx.search(p["t"])]
        by = Counter(p["date"][:4] for p in hit)
        share24 = by["2024"] / years["2024"] * 100 if years["2024"] else 0
        share26 = by["2026"] / years["2026"] * 100 if years["2026"] else 0
        tally.append((len(hit), name, by, share24, share26))
        rows_out.append((ax, name, len(hit), by["2024"], by["2025"], by["2026"], round(share26 - share24, 1)))
    for n, name, by, s24, s26 in sorted(tally, reverse=True):
        arrow = "▲" if s26 - s24 >= 3 else ("▼" if s26 - s24 <= -3 else " ")
        print(f"  {n:>5} ({n/N*100:>4.1f}%)  {name:<26} 24:{by['2024']:>3} 25:{by['2025']:>3} 26:{by['2026']:>3}  {arrow}{s26-s24:+.1f}%p")
    print()

with open("medical_taxonomy_counts.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["axis", "branch", "count", "2024", "2025", "2026", "share_change_pp"])
    w.writerows(rows_out)

print("══ 대표 논문 후보 — 의료 VLM 인용순 상위 20 ══")
for p in sorted(med, key=lambda p: -(CIT.get(p["id"], {}).get("c") or 0))[:20]:
    c = CIT.get(p["id"], {}).get("c", "-")
    print(f"  {c:>5}  {p['date']}  {p['title'][:70]}")
print(f"\n→ medical_taxonomy_counts.csv 저장")

# -*- coding: utf-8 -*-
"""LLaVA 포크 계열 베이스라인 공통: 저장소의 llava 패키지를 sys.path 맨 앞에 두고 import, 스트리밍 generate 로 TTFT 측정."""
import os, sys, time, threading, importlib, torch
WORK = os.environ.get("WORK", os.path.expanduser("~/vlmbench"))

def use_repo(name):
    """repos/<name> 의 llava 를 쓰도록 sys.path 조정 (기본 LLaVA 설치본을 가린다)."""
    path = f"{WORK}/repos/{name}"
    sys.path.insert(0, path)
    for m in [m for m in sys.modules if m == "llava" or m.startswith("llava.")]: del sys.modules[m]
    llava = importlib.import_module("llava")
    assert llava.__file__.startswith(path), f"llava import 가 {llava.__file__} — 저장소 {path} 가 아님"
    return path

def vicuna_prompt(question):
    """LLaVA 공식 conv 템플릿(vicuna_v1): 시스템 프롬프트 포함. FastV(sys_length 36)·DART(image_token_start_index 35)가 이 위치를 전제한다."""
    from llava.conversation import conv_templates
    from llava.constants import DEFAULT_IMAGE_TOKEN
    conv = conv_templates["vicuna_v1"].copy()
    conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\n" + question + "\nAnswer the question using a single word or phrase.")
    conv.append_message(conv.roles[1], None)
    return conv.get_prompt()

def make_gen(tok, model, proc, build_prompt=None, n_vis_fn=None, generate_kwargs=None, extra_prepare=None, per_call_kwargs=None, pass_image_sizes=True):
    """per_call_kwargs(question) -> dict : 샘플마다 generate 에 추가로 넘길 인자 (예: CDPruner 의 texts=question)
       pass_image_sizes=False : 구형 LLaVA 포크(FastV, transformers 4.31)는 generate 에 image_sizes 인자가 없어 넘기면 unused-kwarg 오류"""
    from llava.mm_utils import process_images, tokenizer_image_token
    from llava.constants import IMAGE_TOKEN_INDEX
    from transformers import TextIteratorStreamer
    generate_kwargs = generate_kwargs or {}
    def gen(img, question, max_new_tokens):
        imt = process_images([img], proc, model.config).to("cuda", torch.float16)
        prompt = (build_prompt or vicuna_prompt)(question)
        ids = tokenizer_image_token(prompt, tok, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).cuda()
        if extra_prepare: extra_prepare(model, ids)
        streamer = TextIteratorStreamer(tok, skip_prompt=True, skip_special_tokens=True)
        torch.cuda.synchronize(); t0 = time.perf_counter(); first = [None]; ret = {}
        def run():
            try:
                with torch.inference_mode():
                    out = model.generate(ids, images=imt, **({"image_sizes": [img.size]} if pass_image_sizes else {}), max_new_tokens=max_new_tokens, do_sample=False, streamer=streamer, **generate_kwargs, **(per_call_kwargs(question) if per_call_kwargs else {}))
                    ret["out"] = out
            except BaseException as e:            # 스레드 예외는 전파되지 않아 streamer 루프가 영원히 기다린다 → 종료 신호 후 기록
                ret["err"] = e; streamer.end()
        th = threading.Thread(target=run); th.start(); text = ""
        for piece in streamer:
            if first[0] is None: first[0] = time.perf_counter()
            text += piece
        th.join(); torch.cuda.synchronize(); t1 = time.perf_counter()
        if "err" in ret: raise ret["err"]
        nv = n_vis_fn(model, ret.get("out")) if n_vis_fn else 576
        return dict(answer=text.strip(), n_vis_tokens=nv, ttft_s=(first[0] or t1) - t0, total_s=t1 - t0)
    return gen

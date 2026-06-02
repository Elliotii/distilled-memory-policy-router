"""Evaluate trained LoRA adapter on dev cases.

Usage:
  python src/v05/eval_lora_router.py \
    --base-model /home/abc16/hf_models/Qwen3-4B-Instruct-2507 \
    --adapter results/v05_lora/qwen3_4b_dsl_125/adapter \
    --cases data/v05/dev/v05_dev_cases.jsonl \
    --out data/v05/model_predictions/qwen3_4b_lora_125_dev_predictions.jsonl
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.model_output_runner import load_cases, write_jsonl


from src.v05.render_sft_messages import SYSTEM_PROMPT, render_user_input


def load_model_adapter(base_model: str, adapter: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(base_model, local_files_only=True, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model, torch_dtype=torch.bfloat16, device_map="auto",
        local_files_only=True, trust_remote_code=True,
    )
    from peft import PeftModel
    model = PeftModel.from_pretrained(model, adapter)
    model.eval()
    print(f"Loaded adapter from {adapter}")
    return model, tokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-model", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--system", default="qwen3_4b_lora_125_unit_dsl")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--max-new-tokens", type=int, default=512)
    args = ap.parse_args()

    cases = load_cases(Path(args.cases))
    print(f"Cases: {len(cases)}")
    model, tokenizer = load_model_adapter(args.base_model, args.adapter)

    import torch
    sys_hash = hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()
    preds = []
    for case in cases:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": render_user_input(case)},
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        t0 = time.perf_counter()
        with torch.inference_mode():
            out_ids = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
        latency = (time.perf_counter() - t0) * 1000
        raw = tokenizer.decode(out_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        preds.append({
            "case_id": case["case_id"], "interface": "unit_dsl", "system": args.system,
            "model_id": "qwen3_4b_lora_125", "adapter_path": args.adapter,
            "split": args.split, "raw_output": raw, "error": None,
            "latency_ms": round(latency, 1), "output_chars": len(raw),
            "prompt_hash_sha256": sys_hash,
            "metadata": {"max_new_tokens": args.max_new_tokens, "device": str(model.device),
                         "timestamp_utc": datetime.now(timezone.utc).isoformat()},
        })
        if len(preds) % 20 == 0:
            print(f"  ... {len(preds)}/{len(cases)} done")

    write_jsonl(Path(args.out), preds)
    print(f"Wrote {len(preds)} predictions")
    return 0


if __name__ == "__main__":
    sys.exit(main())

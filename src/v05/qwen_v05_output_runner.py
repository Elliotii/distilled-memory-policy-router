"""v0.5 Qwen local output runner for full dev baseline.

Loads prompt templates from prompts/v05/, records file hashes,
uses SFT-style chat roles with canonical interface names.
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


# ── Prompt loading ──────────────────────────────────────────────────────

PROMPT_DIR = ROOT / "prompts" / "v05"

FEWSHOT_CASES = [
    {
        "case_id": "v05_sample_0001",
        "context": (
            "RUNTIME_CONTEXT\nproject: memory-router\nrepo: distilled-memory-policy-router\n"
            "service: parser\ntask: verify parser rejects unknown STORE targets\n\n"
            "CANDIDATE_MEMORIES\n"
            "m1 [service_memory]: The parser rejects unknown STORE targets and does not do semantic repair.\n"
            "m2 [project_memory]: The v0.4 pilot evaluates Unit DSL before v0.5 training.\n"
            "m3 [service_memory]: The old v0.3 validator checked exact write_spans substrings only.\n\n"
            "CURRENT_UNITS\nu1: The parser should refuse to accept fact as a valid STORE target."
        ),
        "dsl": "READ m1\nSTORE NONE\nSKIP u1",
        "json": '{"read":["m1"],"store":[],"skip":["u1"]}',
    },
    {
        "case_id": "v05_sample_0005",
        "context": (
            "RUNTIME_CONTEXT\nproject: memory-router\nrepo: distilled-memory-policy-router\n"
            "service: parser\ntask: record parser memory\n\n"
            "CANDIDATE_MEMORIES\nNONE\n\n"
            "CURRENT_UNITS\n"
            "u1: Parser tests should live under tests/v04/ and run with pytest tests/v04/.\n"
            "u2: The parser converts Unit DSL to canonical JSON without guessing targets.\n"
            "u3: Remember my personal backup email: abc16-backup@example.com."
        ),
        "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE service_memory u2\nSKIP u3",
        "json": '{"read":[],"store":[{"target":"repo_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":["u3"]}',
    },
    {
        "case_id": "v05_sample_0009",
        "context": (
            "RUNTIME_CONTEXT\nproject: memory-router\nrepo: distilled-memory-policy-router\n"
            "service: eval_runner\ntask: extend eval_runner with new metric\n\n"
            "CANDIDATE_MEMORIES\n"
            "m1 [service_memory]: The eval_runner groups predictions by interface and system, then scores each group independently.\n"
            "m2 [repo_memory]: Eval runner code lives under src/v04/eval_runner.py and reports go to reports/v04/.\n"
            "m3 [project_memory]: The v0.4 pilot compares three raw-output interfaces before training.\n\n"
            "CURRENT_UNITS\n"
            "u1: The eval_runner must now also report per-tag accuracy breakdowns in addition to aggregate metrics.\n"
            "u2: The eval_runner still evaluates only single-turn cases, not multi-turn sessions.\n"
            "u3: Add the per-tag report section to reports/v04/interface_pilot_report.md template."
        ),
        "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE",
        "json": '{"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"task_state","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],"skip":[]}',
    },
    {
        "case_id": "v05_sample_0010",
        "context": (
            "RUNTIME_CONTEXT\nproject: mobile-field\nrepo: field-app\n"
            "service: sync\ntask: update sync error handling\n\n"
            "CANDIDATE_MEMORIES\n"
            "m1 [service_memory]: The sync module queues offline edits and retries them in creation order with exponential backoff.\n"
            "m2 [task_state]: The previous sync change was deployed last week and passed integration tests.\n"
            "m3 [service_memory]: The old v0.2 notification service used polling instead of push.\n\n"
            "CURRENT_UNITS\n"
            "u1: Sync error handling should be updated to retry on 429 rate-limit responses with a 60s delay.\n"
            "u2: Run the sync integration tests after the change and report results.\n"
            "u3: My test account password is testpass_1234_do_not_store."
        ),
        "dsl": "READ m1\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        "json": '{"read":["m1"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"task_state","unit_id":"u2"}],"skip":["u3"]}',
    },
    {
        "case_id": "v05_sample_0004",
        "context": (
            "RUNTIME_CONTEXT\nproject: memory-router\nrepo: distilled-memory-policy-router\n"
            "service: eval_runner\ntask: record eval_runner capabilities\n\n"
            "CANDIDATE_MEMORIES\nNONE\n\n"
            "CURRENT_UNITS\n"
            "u1: The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1, false store rate, and irrelevant read rate.\n"
            "u2: The eval_runner has been run on subset50 but not yet on full pilot.\n"
            "u3: Maybe the eval_runner should also report confidence scores."
        ),
        "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        "json": '{"read":[],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"task_state","unit_id":"u2"}],"skip":["u3"]}',
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def load_prompt(filename: str) -> tuple[str, str]:
    """Return (prompt_text, sha256_hash)."""
    path = PROMPT_DIR / filename
    text = path.read_text(encoding="utf-8").strip()
    return text, sha256_text(text)


def make_case_input(case: dict[str, Any]) -> str:
    lines = [
        "RUNTIME_CONTEXT",
        f"project: {case['runtime_context']['project']}",
        f"repo: {case['runtime_context']['repo']}",
        f"service: {case['runtime_context']['service']}",
        f"task: {case['runtime_context']['task']}",
        "",
        "CANDIDATE_MEMORIES",
    ]
    mems = case["candidate_memories"]
    if mems:
        for m in mems:
            lines.append(f"{m['memory_id']} [{m['target']}]: {m.get('text', m.get('content', ''))}")
    else:
        lines.append("NONE")
    lines.append("")
    lines.append("CURRENT_UNITS")
    for u in case["current_units"]:
        lines.append(f"{u['unit_id']}: {u['text']}")
    return "\n".join(lines)


def build_messages(
    case: dict[str, Any], interface: str, variant: str, sys_prompt: str,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [{"role": "system", "content": sys_prompt}]
    if variant == "fewshot":
        key = "dsl" if interface == "unit_dsl" else "json"
        for ex in FEWSHOT_CASES:
            messages.append({"role": "user", "content": ex["context"]})
            messages.append({"role": "assistant", "content": ex[key]})
    messages.append({"role": "user", "content": make_case_input(case)})
    return messages


# ── Model loading ───────────────────────────────────────────────────────

def load_model_and_tokenizer(model_path: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading tokenizer from {model_path} ...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=True)
    print(f"Loading model from {model_path} ...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, device_map="auto",
        local_files_only=True, trust_remote_code=True,
    )
    model.eval()
    print(f"Model loaded. Device: {model.device}")
    return model, tokenizer


def generate_output(
    model, tokenizer, messages: list[dict[str, str]],
    max_new_tokens: int = 512, is_qwen35: bool = False,
) -> tuple[str, float, dict[str, Any]]:
    import torch
    extra: dict[str, Any] = {
        "enable_thinking_requested": False,
        "enable_thinking_applied": False,
        "thinking_tags_present": False,
    }
    chat_kwargs: dict[str, Any] = {}
    if is_qwen35:
        extra["enable_thinking_requested"] = True
        try:
            chat_kwargs["enable_thinking"] = False
            extra["enable_thinking_applied"] = True
        except Exception:
            pass

    try:
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, **chat_kwargs
        )
    except Exception:
        parts = []
        for m in messages:
            r, c = m["role"], m["content"]
            if r == "system": parts.append(c)
            elif r == "user": parts.append(f"User: {c}")
            elif r == "assistant": parts.append(f"Assistant: {c}")
        text = "\n\n".join(parts) + "\n\nAssistant:"

    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    t0 = time.perf_counter()
    with torch.inference_mode():
        output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    latency = (time.perf_counter() - t0) * 1000
    raw = tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    if "<think>" in raw or "<｜end▁of▁thinking｜>" in raw:
        extra["thinking_tags_present"] = True
    if hasattr(model, "device"):
        extra["device"] = str(model.device)
    return raw, latency, extra


def run_variant(
    model, tokenizer, cases: list[dict[str, Any]],
    model_id: str, model_path: str,
    interface: str, variant: str, system_name: str,
    sys_prompt: str, sys_prompt_hash: str, prompt_file: str,
    split: str = "dev", max_new_tokens: int = 512,
    is_qwen35: bool = False,
) -> list[dict[str, Any]]:
    preds = []
    for case in cases:
        messages = build_messages(case, interface, variant, sys_prompt)
        raw, latency, extra = generate_output(model, tokenizer, messages, max_new_tokens, is_qwen35)
        pred = {
            "case_id": case["case_id"],
            "interface": interface,
            "prompt_variant": variant,
            "system": system_name,
            "model_id": model_id,
            "model_path": model_path,
            "split": split,
            "prompt_file": prompt_file,
            "prompt_hash_sha256": sys_prompt_hash,
            "prompt_version": "v05",
            "raw_output": raw,
            "error": None,
            "latency_ms": round(latency, 1),
            "output_chars": len(raw),
            "metadata": {
                "max_new_tokens": max_new_tokens,
                "local_files_only": True,
                "fewshot_case_ids": [e["case_id"] for e in FEWSHOT_CASES] if variant == "fewshot" else [],
                "enable_thinking_requested": extra["enable_thinking_requested"],
                "enable_thinking_applied": extra["enable_thinking_applied"],
                "thinking_tags_present": extra["thinking_tags_present"],
                "device": extra.get("device", "unknown"),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            },
        }
        preds.append(pred)
        if (len(preds)) % 20 == 0:
            print(f"  ... {len(preds)}/{len(cases)} done [{system_name}]")
    return preds


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--models-label", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--split", default="dev")
    args = ap.parse_args()

    is_qwen35 = "35" in args.model_id or "3.5" in args.model_id
    cases = load_cases(Path(args.cases))
    print(f"Cases: {len(cases)} | Model: {args.model_id} | Qwen3.5: {is_qwen35}")

    # Load prompt files
    prompt_files = {
        "dsl_zs": "unit_dsl_zero_shot.txt",
        "dsl_fs": "unit_dsl_fewshot.txt",
        "json_zs": "unit_json_zero_shot.txt",
        "json_fs": "unit_json_fewshot.txt",
    }
    prompts: dict[str, tuple[str, str]] = {}
    for key, fname in prompt_files.items():
        prompts[key] = load_prompt(fname)
    print("Prompt hashes:")
    for key, (_, h) in prompts.items():
        print(f"  {prompt_files[key]}: {h[:16]}...")

    model, tokenizer = load_model_and_tokenizer(args.model_path)
    all_preds: list[dict[str, Any]] = []

    configs = [
        ("unit_dsl", "zero_shot", "dsl_zs"),
        ("unit_dsl", "fewshot", "dsl_fs"),
        ("unit_json", "zero_shot", "json_zs"),
        ("unit_json", "fewshot", "json_fs"),
    ]
    try:
        for interface, variant, pkey in configs:
            sys_name = f"{args.models_label}_{interface}_{variant}"
            sys_prompt, sys_hash = prompts[pkey]
            prompt_file = prompt_files[pkey]
            t0 = time.perf_counter()
            print(f"\n--- {sys_name} ---")
            preds = run_variant(
                model, tokenizer, cases,
                args.model_id, args.model_path,
                interface, variant, sys_name,
                sys_prompt, sys_hash, prompt_file,
                args.split, args.max_new_tokens, is_qwen35,
            )
            elapsed = time.perf_counter() - t0
            print(f"  Done in {elapsed:.0f}s ({len(preds)} preds)")
            all_preds.extend(preds)
    finally:
        del model; del tokenizer; gc.collect()
        import torch; torch.cuda.empty_cache()

    write_jsonl(Path(args.out), all_preds)
    print(f"\nTotal: {len(all_preds)} predictions -> {args.out}")
    errors = sum(1 for p in all_preds if p["error"])
    empty = sum(1 for p in all_preds if not p["raw_output"].strip())
    print(f"Errors: {errors} | Empty: {empty}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

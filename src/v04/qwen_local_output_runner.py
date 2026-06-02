"""Run local Qwen3-4B inference for v0.4 A/B/C prompt interfaces.

Narrow scope:
- Load Qwen3-4B-Instruct-2507 from local path (no HF download).
- Render the same three v0.4 prompt templates.
- Run 5-case smoke × 3 interfaces = 15 predictions.
- Write external prediction JSONL for eval_runner.

No training, no data modification, no remote API calls.
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Reuse prompt rendering from model_output_runner
from src.v04.model_output_runner import (
    format_candidate_memories,
    format_current_units,
    format_runtime_context,
    load_case_ids,
    load_cases,
    select_cases,
    write_jsonl,
)

INTERFACES = ("legacy_span_json", "unit_json", "unit_dsl")
PROMPT_FILES = {
    "legacy_span_json": Path("prompts/v04/legacy_span_json.txt"),
    "unit_json": Path("prompts/v04/unit_json.txt"),
    "unit_dsl": Path("prompts/v04/unit_dsl.txt"),
}


def render_prompt(template: str, case: dict[str, Any]) -> str:
    return (
        template
        .replace("{runtime_context}", format_runtime_context(case["runtime_context"]))
        .replace("{candidate_memories}", format_candidate_memories(case["candidate_memories"]))
        .replace("{current_units}", format_current_units(case["current_units"]))
    )


def load_model_and_tokenizer(model_path: str):
    """Load Qwen3-4B locally. Returns (model, tokenizer) or raises."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading tokenizer from {model_path} ...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=True,
    )

    print(f"Loading model from {model_path} ...")
    # Determine best dtype
    if torch.cuda.is_available():
        try:
            # Try bfloat16 first
            dtype = torch.bfloat16
        except Exception:
            dtype = torch.float16
    else:
        dtype = torch.float32

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=True,
        torch_dtype=dtype,
        device_map="auto",
    )
    model.eval()
    return model, tokenizer


def get_gpu_memory_info() -> dict[str, Any]:
    """Return GPU memory info if CUDA available, else empty dict."""
    import torch
    if not torch.cuda.is_available():
        return {}
    info = {}
    for i in range(torch.cuda.device_count()):
        alloc = torch.cuda.memory_allocated(i) / (1024 ** 3)
        reserved = torch.cuda.memory_reserved(i) / (1024 ** 3)
        info[f"gpu{i}_allocated_gb"] = round(alloc, 2)
        info[f"gpu{i}_reserved_gb"] = round(reserved, 2)
    return info


def run_inference(
    *,
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int,
    eos_token_id: int | None,
    pad_token_id: int | None,
) -> tuple[str, float]:
    """Run single inference. Returns (raw_output, latency_seconds)."""
    import torch

    # Build messages
    messages = [{"role": "user", "content": prompt}]

    # Try apply_chat_template with enable_thinking=False
    try:
        formatted = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        # Fallback: without enable_thinking
        formatted = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

    inputs = tokenizer(
        formatted,
        return_tensors="pt",
        add_special_tokens=False,
    )

    # Move to model device
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    gen_kwargs: dict[str, Any] = {
        "max_new_tokens": max_new_tokens,
        "do_sample": False,
        "pad_token_id": pad_token_id or tokenizer.eos_token_id,
        "eos_token_id": eos_token_id or tokenizer.eos_token_id,
    }

    started = time.monotonic()
    with torch.inference_mode():
        outputs = model.generate(**inputs, **gen_kwargs)
    latency = time.monotonic() - started

    # Decode only the new tokens
    input_len = inputs["input_ids"].shape[1]
    generated_ids = outputs[0][input_len:]
    raw_output = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    return raw_output, latency


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model-path",
        default="/home/abc16/hf_models/Qwen3-4B-Instruct-2507",
        help="Local Qwen model directory.",
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("data/v04/model_predictions/qwen3_4b_smoke_cases.jsonl"),
    )
    parser.add_argument(
        "--case-ids",
        type=Path,
        default=Path("data/v04/model_predictions/qwen3_4b_smoke_case_ids.txt"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/v04/model_predictions/qwen3_4b_smoke_predictions.jsonl"),
    )
    parser.add_argument("--system", default="qwen3_4b_smoke")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--max-new-tokens", type=int, default=768)
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=None,
        help="Custom prompt template file (overrides per-interface templates).",
    )
    parser.add_argument(
        "--interface",
        choices=INTERFACES,
        default=None,
        help="Run only this interface (default: all three).",
    )
    args = parser.parse_args()

    model_path = args.model_path
    if not Path(model_path).is_dir():
        print(f"Model path not found: {model_path}", file=sys.stderr)
        return 1

    # Load cases
    cases = load_cases(args.cases)
    case_ids = load_case_ids(args.case_ids)
    selected = select_cases(cases, case_ids)
    print(f"Cases to run: {len(selected)}")

    # Load prompt templates
    if args.prompt_file:
        custom_template = (ROOT / args.prompt_file).read_text(encoding="utf-8")
        templates = {iface: custom_template for iface in INTERFACES}
        print(f"Using custom prompt: {args.prompt_file}")
    else:
        templates = {
            interface: (ROOT / path).read_text(encoding="utf-8")
            for interface, path in PROMPT_FILES.items()
        }

    # Determine which interfaces to run
    interfaces_to_run = (args.interface,) if args.interface else INTERFACES

    # Load model
    print("=" * 60)
    print("Loading Qwen3-4B model...")
    mem_before = get_gpu_memory_info()
    print(f"GPU memory before load: {mem_before}")

    model, tokenizer = load_model_and_tokenizer(model_path)
    mem_after = get_gpu_memory_info()
    print(f"GPU memory after load: {mem_after}")
    print("=" * 60)

    eos_id: int | None = tokenizer.eos_token_id
    pad_id: int | None = tokenizer.pad_token_id or eos_id

    run_id = args.run_id or f"qwen_smoke_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    model_id = "Qwen3-4B-Instruct-2507"
    rows: list[dict[str, Any]] = []
    total_calls = len(selected) * len(interfaces_to_run)
    call_index = 0

    for case in selected:
        for interface in interfaces_to_run:
            call_index += 1
            case_id = case["case_id"]
            print(f"[{call_index}/{total_calls}] {case_id} {interface} ...", end=" ", flush=True)

            prompt = render_prompt(templates[interface], case)
            raw_output = ""
            error_message = None
            latency_ms = 0

            try:
                raw_output, latency_sec = run_inference(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=prompt,
                    max_new_tokens=args.max_new_tokens,
                    eos_token_id=eos_id,
                    pad_token_id=pad_id,
                )
                latency_ms = int(latency_sec * 1000)
                if raw_output:
                    print(f"OK ({latency_ms}ms, {len(raw_output)} chars)")
                else:
                    print(f"EMPTY ({latency_ms}ms)")
                    error_message = "empty model output"
            except Exception as exc:
                error_message = f"{type(exc).__name__}: {exc}"
                # Truncate long error messages, strip any potential secrets
                if len(error_message) > 200:
                    error_message = error_message[:200]
                print(f"ERROR: {error_message}")

            row: dict[str, Any] = {
                "case_id": case_id,
                "interface": interface,
                "system": args.system,
                "raw_output": raw_output,
                "model_id": model_id,
                "run_id": run_id,
                "latency_ms": latency_ms,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            if error_message:
                row["error"] = error_message
            rows.append(row)

    # Write output
    write_jsonl(args.output, rows)
    error_count = sum(1 for r in rows if r.get("error"))
    empty_count = sum(1 for r in rows if not r.get("raw_output") and not r.get("error"))
    print(f"\nWrote {len(rows)} rows to {args.output}")
    print(f"Errors: {error_count}, Empty outputs: {empty_count}")

    # Final GPU memory
    mem_final = get_gpu_memory_info()
    print(f"GPU memory at end: {mem_final}")

    return 0 if error_count == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())

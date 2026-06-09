#!/usr/bin/env python3
"""Run v0.5g LoRA router predictions on rendered hard READ inputs.

This script is intended for an offline GPU host that already has the Qwen base
model and v0.5g adapter available on local disk. It does not call APIs, train,
download models, or create prediction rows unless model inference completes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE = "v0.5g_offline_batch_prediction"

JSON_SYSTEM_PROMPT = (
    "You are a memory policy router for coding-agent contexts.\n\n"
    "Task:\n"
    "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
    "- which candidate memories to READ;\n"
    "- which current unit IDs to STORE and to which target;\n"
    "- which current unit IDs to SKIP.\n\n"
    "Output only valid JSON. Do not include markdown fences, comments, prose, "
    "or explanations.\n\n"
    "Format:\n"
    "{\n"
    '  "read": ["m1", "m3"],\n'
    '  "store": [\n'
    '    {"target": "service_memory", "unit_id": "u1"},\n'
    '    {"target": "task_state", "unit_id": "u2"}\n'
    "  ],\n"
    '  "skip": ["u3"]\n'
    "}\n\n"
    "Legal STORE targets:\n"
    "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
    "Rules:\n"
    "- READ useful memories only; skip merely related or stale ones.\n"
    "- STORE durable, reusable information with correct target.\n"
    "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
    "- Every current unit must appear exactly once in store or skip.\n"
    "- Do not invent IDs, targets, or content."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--out-predictions", required=True)
    parser.add_argument("--out-report", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    return parser.parse_args()


def require_local_dir(path_value: str, label: str) -> Path:
    if not path_value or path_value.strip() in {"", "$DMPR_BASE_MODEL", "$DMPR_V05G_ADAPTER"}:
        raise RuntimeError(f"{label} path is missing")
    path = Path(path_value).expanduser()
    if not path.exists():
        raise RuntimeError(f"{label} path does not exist")
    if not path.is_dir():
        raise RuntimeError(f"{label} path is not a directory")
    return path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if "case_id" not in row:
                raise ValueError(f"{path}:{line_no} missing case_id")
            if not isinstance(row.get("model_input"), dict) or not row["model_input"].get("text"):
                raise ValueError(f"{path}:{line_no} missing model_input.text")
            if not row.get("rendered_input_hash"):
                raise ValueError(f"{path}:{line_no} missing rendered_input_hash")
            rows.append(row)
    return rows


def safe_id(path: Path) -> str:
    name = path.name or path.parent.name
    parent = path.parent.name
    return f"{parent}/{name}" if parent and name == "adapter" else name


def extract_json_object(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    if cleaned.startswith("{") and cleaned.endswith("}"):
        return cleaned
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        return cleaned[start : end + 1]
    return cleaned


def parse_selected_memory_ids(raw: str, valid_ids: set[str]) -> tuple[list[str], str, str | None]:
    try:
        parsed = json.loads(extract_json_object(raw))
    except json.JSONDecodeError as exc:
        return [], "json_parse_error", str(exc)
    if not isinstance(parsed, dict):
        return [], "schema_error", "prediction JSON root is not an object"
    read = parsed.get("read")
    if not isinstance(read, list):
        return [], "schema_error", "prediction field 'read' is not a list"
    selected: list[str] = []
    invalid: list[str] = []
    seen: set[str] = set()
    for item in read:
        if not isinstance(item, str):
            invalid.append(repr(item))
            continue
        if item not in valid_ids:
            invalid.append(item)
            continue
        if item not in seen:
            selected.append(item)
            seen.add(item)
    if invalid:
        return selected, "invalid_read_id", ", ".join(invalid)
    return selected, "ok", None


def render_prompt(tokenizer: Any, user_text: str) -> str:
    messages = [
        {"role": "system", "content": JSON_SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )


def import_model_stack() -> tuple[Any, Any, Any]:
    missing: list[str] = []
    torch = transformers = peft = None
    try:
        import torch as torch_mod

        torch = torch_mod
    except Exception as exc:  # pragma: no cover - host dependent
        missing.append(f"torch: {exc}")
    try:
        import transformers as transformers_mod

        transformers = transformers_mod
    except Exception as exc:  # pragma: no cover - host dependent
        missing.append(f"transformers: {exc}")
    try:
        import peft as peft_mod

        peft = peft_mod
    except Exception as exc:  # pragma: no cover - host dependent
        missing.append(f"peft: {exc}")
    if missing:
        raise RuntimeError("Required packages unavailable: " + "; ".join(missing))
    return torch, transformers, peft


def load_model(base_model: Path, adapter: Path) -> tuple[Any, Any, Any]:
    torch, transformers, peft = import_model_stack()
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        str(base_model),
        local_files_only=True,
        trust_remote_code=True,
    )
    model = transformers.AutoModelForCausalLM.from_pretrained(
        str(base_model),
        torch_dtype=dtype,
        device_map="auto",
        local_files_only=True,
        trust_remote_code=True,
    )
    model = peft.PeftModel.from_pretrained(model, str(adapter))
    model.eval()
    return torch, model, tokenizer


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as tmp:
        tmp_path = Path(tmp.name)
        for row in rows:
            tmp.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp_path.replace(path)


def write_report(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    inputs_path = Path(args.inputs)
    predictions_path = Path(args.out_predictions)
    report_path = Path(args.out_report)

    base_model = require_local_dir(args.base_model, "base model")
    adapter = require_local_dir(args.adapter, "adapter")
    rows = load_jsonl(inputs_path)
    if not rows:
        raise RuntimeError("No input rows found")

    torch, model, tokenizer = load_model(base_model, adapter)
    model_id = safe_id(base_model)
    adapter_id = safe_id(adapter)
    prompt_hash = hashlib.sha256(JSON_SYSTEM_PROMPT.encode("utf-8")).hexdigest()
    predictions: list[dict[str, Any]] = []
    parse_counts: dict[str, int] = {}

    for index, row in enumerate(rows, 1):
        user_text = row["model_input"]["text"]
        prompt_text = render_prompt(tokenizer, user_text)
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        generate_kwargs: dict[str, Any] = {
            "max_new_tokens": args.max_new_tokens,
            "do_sample": args.temperature > 0,
        }
        if args.temperature > 0:
            generate_kwargs["temperature"] = args.temperature

        start = time.perf_counter()
        with torch.inference_mode():
            output_ids = model.generate(**inputs, **generate_kwargs)
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        prompt_len = inputs["input_ids"].shape[1]
        raw = tokenizer.decode(output_ids[0][prompt_len:], skip_special_tokens=True).strip()
        valid_ids = set(row.get("candidate_memory_ids") or [])
        selected_ids, parse_status, parse_error = parse_selected_memory_ids(raw, valid_ids)
        parse_counts[parse_status] = parse_counts.get(parse_status, 0) + 1
        predictions.append(
            {
                "case_id": row["case_id"],
                "selected_memory_ids": selected_ids,
                "raw_prediction": raw,
                "parse_status": parse_status,
                "parse_error": parse_error,
                "model_id": model_id,
                "adapter_id": adapter_id,
                "rendered_input_hash": row["rendered_input_hash"],
                "source": SOURCE,
                "metadata": {
                    "max_new_tokens": args.max_new_tokens,
                    "temperature": args.temperature,
                    "latency_ms": latency_ms,
                    "output_chars": len(raw),
                    "prompt_hash_sha256": prompt_hash,
                },
            }
        )
        print(f"{index}/{len(rows)} {row['case_id']} parse_status={parse_status}", flush=True)

    write_jsonl_atomic(predictions_path, predictions)
    ok_count = parse_counts.get("ok", 0)
    report_lines = [
        "# v0.5g Offline Prediction Run Report",
        "",
        f"- timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
        f"- input_rows: {len(rows)}",
        f"- prediction_rows: {len(predictions)}",
        f"- source: {SOURCE}",
        f"- model_id: {model_id}",
        f"- adapter_id: {adapter_id}",
        f"- parse_ok_rows: {ok_count}",
        f"- parse_ok_rate: {ok_count / len(predictions):.4f}",
        f"- parse_status_counts: {json.dumps(parse_counts, sort_keys=True)}",
        f"- predictions_path: {predictions_path.as_posix()}",
        "",
        "Boundary: these rows are offline batch predictions from a local adapter run. "
        "Replay evaluation must be run separately on the Mac harness before reporting selection metrics.",
    ]
    write_report(report_path, report_lines)
    print(f"Wrote {len(predictions)} predictions to {predictions_path}")
    print(f"Wrote run report to {report_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

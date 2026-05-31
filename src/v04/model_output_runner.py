"""Collect real model raw outputs for the v0.4 A/B/C smoke subset.

This script is intentionally narrow:
- load repo-local .env values without printing secrets;
- render the existing v0.4 prompt templates;
- call one OpenAI-compatible chat/completions endpoint;
- write external prediction JSONL rows for eval_runner.

It does not train models, repair outputs, retrieve memories, or modify gold
data.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


INTERFACES = ("legacy_span_json", "unit_json", "unit_dsl")
PROMPT_FILES = {
    "legacy_span_json": Path("prompts/v04/legacy_span_json.txt"),
    "unit_json": Path("prompts/v04/unit_json.txt"),
    "unit_dsl": Path("prompts/v04/unit_dsl.txt"),
}
KEY_ALIASES = (
    "DEEPSEEK_API_KEY",
    "OPENAI_API_KEY",
    "MEMORY_ROUTER_API_KEY",
    "PACKY_API_KEY",
)
BASE_ALIASES = (
    "DEEPSEEK_API_BASE",
    "DEEPSEEK_BASE_URL",
    "OPENAI_BASE_URL",
    "MEMORY_ROUTER_BASE_URL",
    "PACKY_BASE_URL",
)
MODEL_ALIASES = (
    "DEEPSEEK_MODEL",
    "MODEL_NAME",
    "MEMORY_ROUTER_MODEL",
    "PACKY_MODEL",
)


@dataclass
class ChatCompletionResult:
    raw_output: str
    metadata: dict[str, Any]


def parse_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key:
            env[key] = value
    return env


def load_env(path: Path) -> dict[str, str]:
    env = parse_env_file(path)
    for key, value in env.items():
        if value and key not in os.environ:
            os.environ[key] = value
    return env


def env_key_names(path: Path) -> list[str]:
    return list(parse_env_file(path).keys())


def first_nonempty(keys: tuple[str, ...]) -> tuple[str | None, str | None]:
    for key in keys:
        value = os.getenv(key)
        if value:
            return key, value
    return None, None


def resolve_config(env_path: Path) -> dict[str, Any]:
    load_env(env_path)
    key_name, api_key = first_nonempty(KEY_ALIASES)
    base_name, base_url = first_nonempty(BASE_ALIASES)
    model_name, model_id = first_nonempty(MODEL_ALIASES)
    return {
        "env_exists": env_path.exists(),
        "env_keys": env_key_names(env_path),
        "key_name": key_name,
        "base_name": base_name,
        "model_name": model_name,
        "api_key": api_key,
        "base_url": base_url,
        "model_id": model_id,
        "key_available": bool(api_key),
        "base_available": bool(base_url),
        "model_available": bool(model_id),
        "deepseek_like_model": bool(model_id and "deepseek" in model_id.lower()),
    }


def print_config_summary(config: dict[str, Any]) -> None:
    print(".env exists:", config["env_exists"])
    print("ENV keys found:", config["env_keys"])
    print("api key available:", config["key_available"])
    print("base url available:", config["base_available"])
    print("model available:", config["model_available"])
    print("model deepseek-like:", config["deepseek_like_model"])
    if config["deepseek_like_model"]:
        print("model_id:", config["model_id"])
    print("api key source:", config["key_name"] or "none")
    print("base url source:", config["base_name"] or "none")
    print("model source:", config["model_name"] or "none")


def completion_url(base_url: str) -> str:
    stripped = base_url.rstrip("/")
    if stripped.endswith("/chat/completions"):
        return stripped
    return f"{stripped}/chat/completions"


def safe_error_message(exc: BaseException) -> str:
    if isinstance(exc, error.HTTPError):
        return f"HTTP {exc.code} {exc.reason}"
    if isinstance(exc, error.URLError):
        return f"URL error: {exc.reason.__class__.__name__}"
    return exc.__class__.__name__


def _string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _first_output_text_from_output_items(output_items: Any) -> str:
    if not isinstance(output_items, list):
        return ""
    for item in output_items:
        if not isinstance(item, dict):
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                continue
            text = _string_value(part.get("text"))
            if text.strip():
                return text
    return ""


def extract_raw_output(data: dict[str, Any]) -> tuple[str, str]:
    choices = data.get("choices")
    first_choice = choices[0] if isinstance(choices, list) and choices else {}
    first_choice = first_choice if isinstance(first_choice, dict) else {}
    message = first_choice.get("message")
    message = message if isinstance(message, dict) else {}

    candidates = [
        ("message.content", _string_value(message.get("content"))),
        ("choice.text", _string_value(first_choice.get("text"))),
        ("top_level.output_text", _string_value(data.get("output_text"))),
        ("top_level.text", _string_value(data.get("text"))),
        ("output.content.text", _first_output_text_from_output_items(data.get("output"))),
    ]
    for source, value in candidates:
        if value.strip():
            return value.strip(), source
    return "", "none"


def sanitized_response_metadata(
    data: dict[str, Any],
    *,
    http_status: int,
    extraction_source: str,
) -> dict[str, Any]:
    choices = data.get("choices")
    choices_list = choices if isinstance(choices, list) else []
    first_choice = choices_list[0] if choices_list and isinstance(choices_list[0], dict) else {}
    message = first_choice.get("message") if isinstance(first_choice, dict) else {}
    message = message if isinstance(message, dict) else {}
    content = _string_value(message.get("content"))
    choice_text = _string_value(first_choice.get("text")) if isinstance(first_choice, dict) else ""
    output_text = _string_value(data.get("output_text")) or _first_output_text_from_output_items(data.get("output"))
    reasoning_content = _string_value(message.get("reasoning_content"))
    usage = data.get("usage")
    return {
        "http_status": http_status,
        "top_level_keys": sorted(data.keys()),
        "choices_count": len(choices_list),
        "finish_reason": first_choice.get("finish_reason") if isinstance(first_choice, dict) else None,
        "message_keys": sorted(message.keys()),
        "content_length": len(content),
        "has_content": bool(content),
        "has_text": bool(choice_text),
        "has_output_text": bool(output_text),
        "has_reasoning_content": bool(reasoning_content),
        "reasoning_content_length": len(reasoning_content),
        "usage_keys": sorted(usage.keys()) if isinstance(usage, dict) else [],
        "extraction_source": extraction_source,
    }


def chat_completion(
    *,
    api_key: str,
    base_url: str,
    model_id: str,
    prompt: str,
    timeout: float,
    max_tokens: int,
    temperature: float,
) -> ChatCompletionResult:
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        completion_url(base_url),
        data=encoded,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:
        http_status = response.status
        body = response.read().decode("utf-8")
    data = json.loads(body)
    if not isinstance(data, dict):
        raise RuntimeError("chat completion response is not an object")
    content, extraction_source = extract_raw_output(data)
    return ChatCompletionResult(
        raw_output=content,
        metadata=sanitized_response_metadata(
            data,
            http_status=http_status,
            extraction_source=extraction_source,
        ),
    )


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def load_case_ids(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def select_cases(cases: list[dict[str, Any]], case_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {case["case_id"]: case for case in cases}
    missing = [case_id for case_id in case_ids if case_id not in by_id]
    if missing:
        raise ValueError(f"unknown case IDs: {', '.join(missing)}")
    return [by_id[case_id] for case_id in case_ids]


def format_runtime_context(runtime_context: dict[str, Any]) -> str:
    keys = ("project", "repo", "service", "task")
    return "\n".join(f"{key}: {runtime_context.get(key, '')}" for key in keys)


def format_candidate_memories(candidate_memories: list[dict[str, Any]]) -> str:
    if not candidate_memories:
        return "NONE"
    return "\n".join(
        "{memory_id} [{target}]: {content}".format(
            memory_id=memory["memory_id"],
            target=memory["target"],
            content=memory["content"],
        )
        for memory in candidate_memories
    )


def format_current_units(current_units: list[dict[str, Any]]) -> str:
    if not current_units:
        return "NONE"
    return "\n".join(
        f"{unit['unit_id']}: {unit['text']}"
        for unit in current_units
    )


def render_prompt(template: str, case: dict[str, Any]) -> str:
    return (
        template
        .replace("{runtime_context}", format_runtime_context(case["runtime_context"]))
        .replace("{candidate_memories}", format_candidate_memories(case["candidate_memories"]))
        .replace("{current_units}", format_current_units(case["current_units"]))
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_cases_jsonl(path: Path, cases: list[dict[str, Any]]) -> None:
    write_jsonl(path, cases)


def run_collection(args: argparse.Namespace) -> int:
    config = resolve_config(args.env_file)
    print_config_summary(config)
    if not (config["key_available"] and config["base_available"] and config["model_available"]):
        print("DeepSeek unavailable: missing key, base URL, or model.", file=sys.stderr)
        return 2
    if not config["deepseek_like_model"] and args.require_deepseek_like:
        print("DeepSeek unavailable: resolved model is not deepseek-like.", file=sys.stderr)
        return 2

    cases = load_cases(args.cases)
    selected_cases = select_cases(cases, load_case_ids(args.case_ids))
    write_cases_jsonl(args.smoke_cases, selected_cases)

    templates = {
        interface: (ROOT / path).read_text(encoding="utf-8")
        for interface, path in PROMPT_FILES.items()
    }
    run_id = args.run_id or f"p5_smoke_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    rows: list[dict[str, Any]] = []
    total_calls = len(selected_cases) * len(INTERFACES)
    call_index = 0
    for case in selected_cases:
        for interface in INTERFACES:
            call_index += 1
            print(f"Calling model {call_index}/{total_calls}: {case['case_id']} {interface}")
            prompt = render_prompt(templates[interface], case)
            started = time.monotonic()
            raw_output = ""
            error_message = None
            response_metadata: dict[str, Any] | None = None
            retried = False
            retry_reason = None
            try:
                result = chat_completion(
                    api_key=config["api_key"],
                    base_url=config["base_url"],
                    model_id=config["model_id"],
                    prompt=prompt,
                    timeout=args.timeout_seconds,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
                raw_output = result.raw_output
                response_metadata = result.metadata
                if not raw_output and args.retry_empty_once:
                    retried = True
                    retry_reason = "empty_output"
                    result = chat_completion(
                        api_key=config["api_key"],
                        base_url=config["base_url"],
                        model_id=config["model_id"],
                        prompt=prompt,
                        timeout=args.timeout_seconds,
                        max_tokens=args.max_tokens,
                        temperature=args.temperature,
                    )
                    raw_output = result.raw_output
                    response_metadata = result.metadata
                    if not raw_output:
                        error_message = args.empty_output_error
                elif not raw_output:
                    error_message = args.empty_output_error
            except Exception as exc:  # noqa: BLE001 - record non-secret failure and continue.
                error_message = safe_error_message(exc)
            latency_ms = int((time.monotonic() - started) * 1000)
            row: dict[str, Any] = {
                "case_id": case["case_id"],
                "interface": interface,
                "system": args.system,
                "raw_output": raw_output,
                "model_id": config["model_id"],
                "run_id": run_id,
                "latency_ms": latency_ms,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "retried": retried,
            }
            if retry_reason:
                row["retry_reason"] = retry_reason
            if error_message:
                row["error"] = error_message
            if response_metadata is not None:
                row["finish_reason"] = response_metadata.get("finish_reason")
                row["extraction_source"] = response_metadata.get("extraction_source")
                row["content_length"] = response_metadata.get("content_length")
                row["response_metadata"] = response_metadata
            rows.append(row)
    write_jsonl(args.output, rows)
    error_count = sum(1 for row in rows if row.get("error"))
    print(f"Wrote predictions: {args.output}")
    print(f"Wrote smoke cases: {args.smoke_cases}")
    print(f"Rows: {len(rows)}")
    print(f"Errors: {error_count}")
    return 0 if error_count == 0 else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--cases", type=Path, default=Path("data/v04/pilot_cases.jsonl"))
    parser.add_argument(
        "--case-ids",
        type=Path,
        default=Path("data/v04/model_predictions/p5_smoke_case_ids.txt"),
    )
    parser.add_argument(
        "--smoke-cases",
        type=Path,
        default=Path("data/v04/model_predictions/p5_smoke_cases.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/v04/model_predictions/p5_smoke_predictions.jsonl"),
    )
    parser.add_argument("--system", default="deepseek_v4_flash_smoke")
    parser.add_argument("--run-id")
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--empty-output-error", default="empty model output")
    parser.add_argument("--retry-empty-once", action="store_true")
    parser.add_argument("--require-deepseek-like", action="store_true", default=True)
    parser.add_argument("--check-env", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.check_env:
        print_config_summary(resolve_config(args.env_file))
        return 0
    return run_collection(args)


if __name__ == "__main__":
    raise SystemExit(main())

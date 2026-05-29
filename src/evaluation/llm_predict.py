"""Build prompts and parse LLM router predictions.

Real API calls are gated behind ``--allow-real-api``. The default provider is a
local parser smoke test that routes rule-based predictions through the same raw
JSON parsing path used by model outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pydantic import ValidationError

from src.evaluation.baselines import predict_target
from src.evaluation.validate_predictions import load_gold_cases
from src.schemas import RouterTarget


SYSTEM_PROMPT = """You are a memory policy router for coding-agent conversations.
Return only one JSON object. Do not explain.

The router predicts exactly three fields:
- read_hints: candidate memory IDs that should be read now.
- write_spans: exact substrings of current_user_input that should become durable memory, each with type fact, decision, sop, or task_state.
- ignore_spans: exact substrings of current_user_input that are temporary, noisy, sensitive, irrelevant, or explicitly should not be remembered.

Do not invent memory text. Do not rewrite spans. Do not include offsets, confidence, needs_review, project IDs, delete/update/merge operations, or downstream actions.
"""

USER_PROMPT_TEMPLATE = """Given this router input, predict the target.

Hard constraints:
- Return exactly this shape: {{"read_hints":[],"write_spans":[],"ignore_spans":[]}}
- read_hints entries must be IDs from candidate_memories only.
- write_spans[*].span must be copied exactly from current_user_input.
- ignore_spans entries must be copied exactly from current_user_input.
- If no memory action is needed, return all three arrays empty.
- Prefer the smallest meaningful span, not the whole sentence.
- Do not include trailing punctuation unless it is semantically part of the span.
- For write_spans, exclude discourse markers such as "Remember that", "Please remember that", "Note that", "Going forward", "From now on", "We decided to", "We chose to", "Currently", "Still", "Correction:", and "Update:" when the remaining span is a valid exact substring.
- For ignore_spans, exclude directive words such as "ignore", "disregard", "skip", "forget", "also", "and", "please", "this", "that", "these", and "those" when the remaining noise span is a valid exact substring.
- If a clause is temporary noise, test failure chatter, local tooling noise, transient infrastructure noise, or a false alert, put it in ignore_spans, not write_spans.
- Use type "fact" for stable facts/configuration/ownership/location.
- Use type "decision" for explicit choices or selected plans.
- Use type "sop" for recurring rules, policies, preferences, or required practices.
- Use type "task_state" for active, blocked, pending, incomplete, or completed work status.

Examples of correct span boundaries:
- Input: "We decided to use Tanstack Query for all data fetching. also ignore the flaky linter warning"
  Output write span: "use Tanstack Query for all data fetching"
  Output ignore span: "the flaky linter warning"
- Input: "Going forward the staging deploy must pass smoke tests. disregard the npm audit warning"
  Output write span: "the staging deploy must pass smoke tests"
  Output ignore span: "the npm audit warning"
- Input: "Currently debugging the checkout timeout. ignore the transient CDN 503"
  Output write span: "debugging the checkout timeout"
  Output ignore span: "the transient CDN 503"

Router input JSON:
{input_json}
"""

EMPTY_TARGET = {"read_hints": [], "write_spans": [], "ignore_spans": []}

API_KEY_ENV_KEYS = (
    "MEMORY_ROUTER_API_KEY",
    "OPENAI_COMPATIBLE_API_KEY",
    "DEEPSEEK_API_KEY",
    "PACKY_API_KEY",
)
BASE_URL_ENV_KEYS = (
    "MEMORY_ROUTER_BASE_URL",
    "OPENAI_COMPATIBLE_BASE_URL",
    "DEEPSEEK_BASE_URL",
    "PACKY_BASE_URL",
)
MODEL_ENV_KEYS = (
    "MEMORY_ROUTER_MODEL",
    "OPENAI_COMPATIBLE_MODEL",
    "DEEPSEEK_MODEL",
    "PACKY_MODEL",
)


@dataclass(frozen=True)
class ModelCallResult:
    raw_output: str
    usage: dict[str, Any]
    response_model: str | None = None


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def first_config_value(
    *,
    cli_value: str | None,
    env_values: dict[str, str],
    keys: tuple[str, ...],
    default: str | None = None,
) -> str | None:
    if cli_value:
        return cli_value
    for key in keys:
        value = os.environ.get(key) or env_values.get(key)
        if value:
            return value
    return default


def case_input(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "current_user_input": case["current_user_input"],
        "recent_context": case.get("recent_context", []),
        "candidate_memories": case.get("candidate_memories", []),
    }


def build_messages(case: dict[str, Any]) -> list[dict[str, str]]:
    input_json = json.dumps(case_input(case), ensure_ascii=True, indent=2)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(input_json=input_json)},
    ]


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = strip_code_fences(text)
    decoder = json.JSONDecoder()
    start = stripped.find("{")
    if start < 0:
        raise ValueError("no JSON object found")
    payload, _ = decoder.raw_decode(stripped[start:])
    if not isinstance(payload, dict):
        raise ValueError("model output JSON is not an object")
    return payload


def exact_case_substring(current_user_input: str, span: str) -> str | None:
    start = current_user_input.lower().find(span.lower())
    if start < 0:
        return None
    end = start + len(span)
    return current_user_input[start:end]


def normalize_target(
    payload: dict[str, Any],
    case: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    repairs: list[str] = []
    raw_target = payload.get("target") if "target" in payload else payload
    if not isinstance(raw_target, dict):
        return EMPTY_TARGET.copy(), ["target is not an object"], repairs

    candidate_ids = {
        memory.get("id")
        for memory in case.get("candidate_memories", [])
        if isinstance(memory, dict) and isinstance(memory.get("id"), str)
    }
    current_user_input = case.get("current_user_input", "")

    read_hints: list[str] = []
    for memory_id in raw_target.get("read_hints", []):
        if isinstance(memory_id, str) and memory_id in candidate_ids and memory_id not in read_hints:
            read_hints.append(memory_id)
        else:
            errors.append(f"dropped invalid read_hint: {memory_id!r}")

    write_spans: list[dict[str, str]] = []
    seen_writes: set[str] = set()
    for item in raw_target.get("write_spans", []):
        if not isinstance(item, dict):
            errors.append(f"dropped non-object write span: {item!r}")
            continue
        span = item.get("span")
        memory_type = item.get("type")
        if not isinstance(span, str):
            errors.append(f"dropped invalid write span: {span!r}")
            continue
        if span not in current_user_input:
            repaired_span = exact_case_substring(current_user_input, span)
            if repaired_span is None:
                errors.append(f"dropped invalid write span: {span!r}")
                continue
            repairs.append(f"case-repaired write span: {span!r} -> {repaired_span!r}")
            span = repaired_span
        if memory_type not in {"fact", "decision", "sop", "task_state"}:
            errors.append(f"dropped invalid write type for span {span!r}: {memory_type!r}")
            continue
        if span in seen_writes:
            errors.append(f"dropped duplicate write span: {span!r}")
            continue
        seen_writes.add(span)
        write_spans.append({"span": span, "type": memory_type})

    ignore_spans: list[str] = []
    for span in raw_target.get("ignore_spans", []):
        if not isinstance(span, str):
            errors.append(f"dropped invalid ignore span: {span!r}")
            continue
        if span not in current_user_input:
            repaired_span = exact_case_substring(current_user_input, span)
            if repaired_span is None:
                errors.append(f"dropped invalid ignore span: {span!r}")
                continue
            repairs.append(f"case-repaired ignore span: {span!r} -> {repaired_span!r}")
            span = repaired_span
        if span not in ignore_spans:
            ignore_spans.append(span)

    target = {
        "read_hints": read_hints,
        "write_spans": write_spans,
        "ignore_spans": ignore_spans,
    }
    try:
        RouterTarget.model_validate(target)
    except ValidationError as exc:
        return EMPTY_TARGET.copy(), [*errors, f"target schema validation failed: {exc}"], repairs
    return target, errors, repairs


def parse_prediction(
    raw_output: str,
    case: dict[str, Any],
) -> tuple[dict[str, Any], str | None, list[str]]:
    try:
        payload = extract_json_object(raw_output)
        target, errors, repairs = normalize_target(payload, case)
    except Exception as exc:
        return EMPTY_TARGET.copy(), f"{type(exc).__name__}: {exc}", []
    return target, "; ".join(errors) if errors else None, repairs


def call_openai_compatible(
    *,
    messages: list[dict[str, str]],
    api_key: str,
    base_url: str,
    model: str,
    timeout_seconds: int,
    temperature: float,
    max_tokens: int,
) -> ModelCallResult:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API HTTP {exc.code}: {body_text[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API request failed: {exc}") from exc
    try:
        raw_output = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"unexpected API response shape: {payload}") from exc
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        usage = {}
    response_model = payload.get("model") if isinstance(payload.get("model"), str) else None
    return ModelCallResult(raw_output=raw_output, usage=usage, response_model=response_model)


def raw_output_for_case(
    *,
    case: dict[str, Any],
    provider: str,
    allow_real_api: bool,
    api_key: str | None,
    base_url: str,
    model: str,
    timeout_seconds: int,
    temperature: float,
    max_tokens: int,
) -> ModelCallResult:
    if provider == "local-rule":
        return ModelCallResult(
            raw_output=json.dumps(predict_target(case, "rule-based"), ensure_ascii=True),
            usage={},
            response_model=model,
        )
    if provider == "openai-compatible":
        if not allow_real_api:
            raise ValueError("--provider openai-compatible requires --allow-real-api")
        if not api_key:
            raise ValueError("missing API key")
        return call_openai_compatible(
            messages=build_messages(case),
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout_seconds=timeout_seconds,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    raise ValueError(f"unknown provider: {provider}")


def usage_value(usage: dict[str, Any], key: str) -> int | None:
    value = usage.get(key)
    return value if isinstance(value, int) else None


def prompt_char_count(messages: list[dict[str, str]]) -> int:
    return sum(len(message.get("content", "")) for message in messages)


def runlog_row(
    *,
    case_id: str,
    run_id: str,
    provider: str,
    model_id: str,
    api_model: str,
    response_model: str | None,
    base_url: str | None,
    latency_ms: float,
    messages: list[dict[str, str]],
    raw_output: str,
    usage: dict[str, Any],
    parse_error: str | None,
    schema_repairs: list[str],
    attempt_count: int,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "run_id": run_id,
        "provider": provider,
        "model_id": model_id,
        "api_model": api_model,
        "response_model": response_model,
        "base_url_host": urllib.parse.urlparse(base_url).netloc if base_url else None,
        "latency_ms": round(latency_ms, 3),
        "attempt_count": attempt_count,
        "prompt_chars": prompt_char_count(messages),
        "raw_output_chars": len(raw_output),
        "prompt_tokens": usage_value(usage, "prompt_tokens"),
        "completion_tokens": usage_value(usage, "completion_tokens"),
        "total_tokens": usage_value(usage, "total_tokens"),
        "usage": usage,
        "parse_error": parse_error,
        "parse_error_present": bool(parse_error),
        "schema_repair_count": len(schema_repairs),
        "schema_repairs": schema_repairs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--provider", choices=["local-rule", "openai-compatible"], default="local-rule")
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--case-ids-file",
        type=Path,
        help="Optional newline-delimited case IDs to run. Applied before --limit.",
    )
    parser.add_argument("--prompt-log", type=Path)
    parser.add_argument("--run-log", type=Path)
    parser.add_argument("--allow-real-api", action="store_true")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument(
        "--api-key-env",
        help="Optional single env key to read before the standard API key fallback keys.",
    )
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-backoff-seconds", type=float, default=2.0)
    args = parser.parse_args()

    env_values = load_env_file(args.env_file)
    api_key_keys = (
        (args.api_key_env,) + API_KEY_ENV_KEYS
        if args.api_key_env
        else API_KEY_ENV_KEYS
    )
    api_key = first_config_value(
        cli_value=None,
        env_values=env_values,
        keys=api_key_keys,
    )
    base_url = first_config_value(
        cli_value=args.base_url,
        env_values=env_values,
        keys=BASE_URL_ENV_KEYS,
        default="https://www.packyapi.com/v1",
    )
    model = first_config_value(
        cli_value=args.model,
        env_values=env_values,
        keys=MODEL_ENV_KEYS,
        default=args.model_id,
    )
    if args.provider == "local-rule":
        base_url = None
        model = args.model_id
    if args.provider == "openai-compatible":
        if not args.allow_real_api:
            print(
                "error: --provider openai-compatible requires --allow-real-api",
                file=sys.stderr,
            )
            return 2
        if not api_key:
            print(
                "error: missing API key; set MEMORY_ROUTER_API_KEY, "
                "OPENAI_COMPATIBLE_API_KEY, DEEPSEEK_API_KEY, or PACKY_API_KEY",
                file=sys.stderr,
            )
            return 2
        if not base_url:
            print("error: missing API base URL", file=sys.stderr)
            return 2
        if not model:
            print("error: missing model id", file=sys.stderr)
            return 2

    cases = list(load_gold_cases(args.input).items())
    if args.case_ids_file:
        selected_ids = {
            line.strip()
            for line in args.case_ids_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        cases = [(case_id, case) for case_id, case in cases if case_id in selected_ids]
    if args.limit is not None:
        cases = cases[: args.limit]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    prompt_handle = None
    if args.prompt_log:
        args.prompt_log.parent.mkdir(parents=True, exist_ok=True)
        prompt_handle = args.prompt_log.open("w", encoding="utf-8")
    run_log_handle = None
    if args.run_log:
        args.run_log.parent.mkdir(parents=True, exist_ok=True)
        run_log_handle = args.run_log.open("w", encoding="utf-8")

    parse_errors = 0
    with args.output.open("w", encoding="utf-8") as output_handle:
        try:
            for case_id, case in cases:
                messages = build_messages(case)
                if prompt_handle:
                    prompt_handle.write(
                        json.dumps(
                            {"case_id": case_id, "messages": messages},
                            ensure_ascii=True,
                            separators=(",", ":"),
                        )
                        + "\n"
                    )
                    prompt_handle.flush()
                started_at = time.perf_counter()
                attempt_count = 0
                last_error: Exception | None = None
                for attempt in range(args.retries + 1):
                    attempt_count = attempt + 1
                    try:
                        call_result = raw_output_for_case(
                            case=case,
                            provider=args.provider,
                            allow_real_api=args.allow_real_api,
                            api_key=api_key,
                            base_url=base_url,
                            model=model,
                            timeout_seconds=args.timeout_seconds,
                            temperature=args.temperature,
                            max_tokens=args.max_tokens,
                        )
                        break
                    except Exception as exc:
                        last_error = exc
                        if attempt >= args.retries:
                            raise
                        sleep_seconds = args.retry_backoff_seconds * (2**attempt)
                        print(
                            f"warning: {case_id} attempt {attempt_count} failed: {exc}; "
                            f"retrying in {sleep_seconds:.1f}s",
                            file=sys.stderr,
                        )
                        time.sleep(sleep_seconds)
                else:
                    raise RuntimeError(f"unreachable retry state: {last_error}")
                latency_ms = (time.perf_counter() - started_at) * 1000
                raw_output = call_result.raw_output
                target, parse_error, schema_repairs = parse_prediction(raw_output, case)
                if parse_error:
                    parse_errors += 1
                if run_log_handle:
                    run_log_handle.write(
                        json.dumps(
                            runlog_row(
                                case_id=case_id,
                                run_id=args.run_id,
                                provider=args.provider,
                                model_id=args.model_id,
                                api_model=model,
                                response_model=call_result.response_model,
                                base_url=base_url,
                                latency_ms=latency_ms,
                                messages=messages,
                                raw_output=raw_output,
                                usage=call_result.usage,
                                parse_error=parse_error,
                                schema_repairs=schema_repairs,
                                attempt_count=attempt_count,
                            ),
                            ensure_ascii=True,
                            separators=(",", ":"),
                        )
                        + "\n"
                    )
                    run_log_handle.flush()
                row = {
                    "case_id": case_id,
                    "target": target,
                    "run_id": args.run_id,
                    "model_id": args.model_id,
                    "raw_output": raw_output,
                }
                if parse_error:
                    row["parse_error"] = parse_error
                output_handle.write(json.dumps(row, ensure_ascii=True, separators=(",", ":")) + "\n")
                output_handle.flush()
        finally:
            if prompt_handle:
                prompt_handle.close()
            if run_log_handle:
                run_log_handle.close()

    print(f"wrote {len(cases)} predictions to {args.output}")
    print(f"parse_error rows: {parse_errors}")
    if args.prompt_log:
        print(f"wrote prompt log to {args.prompt_log}")
    if args.run_log:
        print(f"wrote run log to {args.run_log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

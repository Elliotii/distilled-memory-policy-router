#!/usr/bin/env python3
"""Run hard READ downstream prompts through an OpenAI-compatible API.

Only prompt_text is sent to the external API. Prompt metadata is preserved only
in the local response JSONL for scoring and diagnostics.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple


SYSTEM_MESSAGE = (
    "You are a concise coding/business-agent assistant. Follow the user's "
    "citation instructions exactly. Return only the final answer. Do not "
    "include hidden reasoning, analysis, or chain-of-thought."
)

JsonDict = Dict[str, object]


def load_dotenv(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def load_jsonl(path: str) -> List[JsonDict]:
    rows: List[JsonDict] = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return rows


def require_env() -> Tuple[str, str, str]:
    missing = [
        key for key in [
            "MEMORY_ROUTER_API_KEY",
            "MEMORY_ROUTER_BASE_URL",
            "MEMORY_ROUTER_MODEL",
        ]
        if not os.environ.get(key)
    ]
    if missing:
        raise RuntimeError("missing required env vars: " + ", ".join(missing))
    return (
        os.environ["MEMORY_ROUTER_API_KEY"],
        os.environ["MEMORY_ROUTER_BASE_URL"].rstrip("/"),
        os.environ["MEMORY_ROUTER_MODEL"],
    )


def post_chat_completion(
    *,
    api_key: str,
    base_url: str,
    model: str,
    prompt_text: str,
    temperature: float,
    max_tokens: int,
) -> Tuple[str, JsonDict, JsonDict]:
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": prompt_text,
            },
        ],
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("API response missing choices")
    choice = choices[0]
    message = choice.get("message") or {}
    content = message.get("content")
    if content is None:
        raise RuntimeError("API response missing message content")
    content_text = str(content)
    message_keys = sorted(str(key) for key in message.keys())
    raw_choice_summary: JsonDict = {
        "finish_reason": choice.get("finish_reason"),
        "index": choice.get("index"),
        "message_keys": message_keys,
        "content_exists": content is not None,
        "reasoning_content_exists": bool(message.get("reasoning_content")),
    }
    for key in ["refusal", "content_filter_results", "content_filter"]:
        if key in message:
            raw_choice_summary[f"message_{key}"] = message.get(key)
        if key in choice:
            raw_choice_summary[f"choice_{key}"] = choice.get(key)
    diagnostics: JsonDict = {
        "finish_reason": choice.get("finish_reason"),
        "message_keys": message_keys,
        "content_present": bool(content_text.strip()),
        "content_length": len(content_text),
        "raw_choice_summary": raw_choice_summary,
    }
    return content_text, data.get("usage") or {}, diagnostics


def empty_diagnostics() -> JsonDict:
    return {
        "finish_reason": None,
        "message_keys": [],
        "content_present": False,
        "content_length": 0,
        "raw_choice_summary": {},
    }


def error_text(exc: BaseException) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return f"HTTP {exc.code}: {body[:500]}"
    if isinstance(exc, urllib.error.URLError):
        return f"URL error: {exc.reason}"
    return str(exc)


def write_report(
    *,
    path: str,
    model: str,
    base_url: str,
    prompt_count: int,
    ok_count: int,
    usable_count: int,
    empty_ok_count: int,
    error_count: int,
    total_latency: float,
    retry_empty: int,
    max_tokens: int,
    temperature: float,
) -> None:
    lines = [
        "# Hard READ Downstream API Run Report",
        "",
        "Context: hard READ downstream API micro-pilot.",
        "",
        f"- Model: `{model}`",
        f"- Base URL: `{base_url}`",
        f"- Prompts attempted: {prompt_count}",
        f"- API OK count: {ok_count}",
        f"- Usable nonempty response count: {usable_count}",
        f"- Empty OK response count: {empty_ok_count}",
        f"- Error count: {error_count}",
        f"- Max tokens: {max_tokens}",
        f"- Temperature: {temperature:g}",
        f"- Retry-empty setting: {retry_empty}",
        f"- Total latency seconds: {total_latency:.3f}",
        f"- Payload metadata sent: false",
        f"- API keys logged: false",
        "",
        "## Payload Boundary",
        "",
        "Only `prompt_text` was sent as the user message, plus a short system instruction. Prompt metadata labels, strategies, expected answer requirements, and scoring fields were not sent in the API payload.",
        "",
        "## Claim Boundaries",
        "",
        "This is a response-collection and citation-diagnostic micro-pilot. It does not evaluate learned router/live LoRA behavior, does not establish downstream answer quality, and does not establish that any selector or router outperforms alternatives. Manual review is still required for answer quality.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_one_prompt(
    *,
    prompt: JsonDict,
    api_key: str,
    base_url: str,
    model: str,
    temperature: float,
    max_tokens: int,
    retry_empty: int,
) -> JsonDict:
    row: JsonDict = {
        "prompt_id": prompt["prompt_id"],
        "case_id": prompt["case_id"],
        "strategy": prompt["strategy"],
        "model": model,
        "api_status": "error",
        "response_text": "",
        "latency_seconds": None,
        "error": None,
        "usage": {},
        "api_payload_metadata_sent": False,
        "finish_reason": None,
        "message_keys": [],
        "content_present": False,
        "content_length": 0,
        "raw_choice_summary": {},
        "empty_response": True,
        "usable_response": False,
        "retry_count": 0,
    }
    total_latency = 0.0
    attempts = 1 + max(0, retry_empty)
    for attempt_index in range(attempts):
        start = time.time()
        try:
            response_text, usage, diagnostics = post_chat_completion(
                api_key=api_key,
                base_url=base_url,
                model=model,
                prompt_text=str(prompt["prompt_text"]),
                temperature=temperature,
                max_tokens=max_tokens,
            )
            latency = time.time() - start
            total_latency += latency
            empty_response = not response_text.strip()
            row.update({
                "api_status": "ok",
                "response_text": response_text,
                "latency_seconds": round(total_latency, 6),
                "error": None,
                "usage": usage,
                "retry_count": attempt_index,
                **diagnostics,
                "empty_response": empty_response,
                "usable_response": not empty_response,
            })
            if not empty_response:
                return row
        except Exception as exc:  # Keep partial run artifacts inspectable.
            latency = time.time() - start
            total_latency += latency
            row.update({
                "api_status": "error",
                "response_text": "",
                "latency_seconds": round(total_latency, 6),
                "error": error_text(exc),
                "usage": {},
                "retry_count": attempt_index,
                **empty_diagnostics(),
                "empty_response": True,
                "usable_response": False,
            })
            return row
    return row


def run(args: argparse.Namespace) -> JsonDict:
    load_dotenv()
    api_key, base_url, model = require_env()
    prompts = load_jsonl(args.prompts)
    out_path = Path(args.out_responses)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ok_count = 0
    error_count = 0
    usable_count = 0
    empty_ok_count = 0
    total_latency = 0.0

    with out_path.open("w", encoding="utf-8") as handle:
        for prompt in prompts:
            row = run_one_prompt(
                prompt=prompt,
                api_key=api_key,
                base_url=base_url,
                model=model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                retry_empty=args.retry_empty,
            )
            latency_value = row.get("latency_seconds")
            if isinstance(latency_value, (int, float)):
                total_latency += float(latency_value)
            if row["api_status"] == "ok":
                ok_count += 1
                if row.get("usable_response"):
                    usable_count += 1
                if row.get("empty_response"):
                    empty_ok_count += 1
            else:
                error_count += 1

            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()

    write_report(
        path=args.report,
        model=model,
        base_url=base_url,
        prompt_count=len(prompts),
        ok_count=ok_count,
        usable_count=usable_count,
        empty_ok_count=empty_ok_count,
        error_count=error_count,
        total_latency=total_latency,
        retry_empty=args.retry_empty,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )
    return {
        "prompt_count": len(prompts),
        "ok_count": ok_count,
        "usable_count": usable_count,
        "empty_ok_count": empty_ok_count,
        "error_count": error_count,
        "total_latency_seconds": round(total_latency, 6),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run hard READ downstream API micro-pilot")
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--out-responses", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=220)
    parser.add_argument("--retry-empty", type=int, default=0)
    args = parser.parse_args()

    summary = run(args)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

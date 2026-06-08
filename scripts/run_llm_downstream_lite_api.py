#!/usr/bin/env python3
"""Run a small API micro-pilot for LLM downstream-lite prompts.

This script uses an OpenAI-compatible chat completions endpoint. It never
prints or writes the API key.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


STRATEGY_ORDER = [
    "no_memory",
    "all_candidates",
    "router_selected",
    "oracle_selected",
    "top_k_naive",
    "random_k",
    "shuffled_top_k",
]

STRENGTHENED_RULES = [
    "Citation rules:",
    "- If you use any memory fact, cite the memory id exactly in bracket form, e.g. [m2].",
    "- Bare references like \"m2\" do not count as citations.",
    "- Do not cite current-unit ids such as [u1] or [u2].",
    "- Do not cite memory ids that are not present in the provided memory context.",
    "- Every sentence that uses a memory fact must include at least one bracketed memory citation.",
    "- If no memory context is provided, do not include any bracketed citations.",
    "",
    "Output format:",
    "Write exactly two bullets:",
    "1. Next action: ...",
    "2. Memory-backed rationale: ...",
    "If using memory facts, the second bullet must include bracketed memory ids.",
    "If no memory context is provided, the second bullet should say that no memory context was provided, without citations.",
]


def load_jsonl(path):
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            rows.append(row)
    return rows


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def load_env_file():
    for path in [Path(".env"), Path("../.env"), Path("../../.env")]:
        if path.exists():
            values = {}
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
            return path, values
    return None, {}


def env_value(values, key):
    return os.environ.get(key) or values.get(key) or ""


def endpoint_for_base(base_url):
    return base_url.rstrip("/") + "/chat/completions"


def sanitize_error(text, api_key):
    if not isinstance(text, str):
        text = str(text)
    if api_key:
        text = text.replace(api_key, "[redacted-api-key]")
    return text[:1000]


def post_chat_completion(base_url, api_key, model, prompt_text, temperature, max_tokens, include_thinking):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if include_thinking:
        body["thinking"] = {"type": "disabled"}
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        endpoint_for_base(base_url),
        data=data,
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.loads(response.read().decode("utf-8"))
    content = ""
    try:
        content = payload["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        content = ""
    return content


def call_api(api_key, base_url, model, prompt_text, temperature, max_tokens):
    start = time.time()
    used_base_url = base_url
    thinking_note = "thinking_disabled_requested"
    try:
        content = post_chat_completion(base_url, api_key, model, prompt_text, temperature, max_tokens, True)
        return {
            "status": "ok",
            "content": content,
            "error": "",
            "latency_seconds": time.time() - start,
            "base_url_used": used_base_url,
            "thinking_note": thinking_note,
        }
    except urllib.error.HTTPError as exc:
        error_body = sanitize_error(exc.read().decode("utf-8", errors="replace"), api_key)
        if exc.code in (401, 403):
            return {
                "status": "auth_error",
                "content": "",
                "error": f"HTTP {exc.code}: {error_body}",
                "latency_seconds": time.time() - start,
                "base_url_used": used_base_url,
                "thinking_note": thinking_note,
            }
        if exc.code == 404 and base_url.rstrip("/").endswith("/v1"):
            stripped_base = base_url.rstrip("/")[:-3].rstrip("/")
            try:
                content = post_chat_completion(stripped_base, api_key, model, prompt_text, temperature, max_tokens, True)
                return {
                    "status": "ok",
                    "content": content,
                    "error": "",
                    "latency_seconds": time.time() - start,
                    "base_url_used": stripped_base,
                    "thinking_note": thinking_note,
                }
            except urllib.error.HTTPError as retry_exc:
                retry_body = sanitize_error(retry_exc.read().decode("utf-8", errors="replace"), api_key)
                if retry_exc.code in (401, 403):
                    return {
                        "status": "auth_error",
                        "content": "",
                        "error": f"HTTP {retry_exc.code}: {retry_body}",
                        "latency_seconds": time.time() - start,
                        "base_url_used": stripped_base,
                        "thinking_note": thinking_note,
                    }
                return {
                    "status": "error",
                    "content": "",
                    "error": f"HTTP {retry_exc.code}: {retry_body}",
                    "latency_seconds": time.time() - start,
                    "base_url_used": stripped_base,
                    "thinking_note": thinking_note,
                }
            except Exception as retry_exc:
                return {
                    "status": "error",
                    "content": "",
                    "error": sanitize_error(retry_exc, api_key),
                    "latency_seconds": time.time() - start,
                    "base_url_used": stripped_base,
                    "thinking_note": thinking_note,
                }
        if exc.code == 400 and "thinking" in error_body.lower():
            try:
                content = post_chat_completion(base_url, api_key, model, prompt_text, temperature, max_tokens, False)
                return {
                    "status": "ok",
                    "content": content,
                    "error": "",
                    "latency_seconds": time.time() - start,
                    "base_url_used": used_base_url,
                    "thinking_note": "thinking_disabled_retry_unsupported",
                }
            except urllib.error.HTTPError as retry_exc:
                retry_body = sanitize_error(retry_exc.read().decode("utf-8", errors="replace"), api_key)
                if retry_exc.code in (401, 403):
                    return {
                        "status": "auth_error",
                        "content": "",
                        "error": f"HTTP {retry_exc.code}: {retry_body}",
                        "latency_seconds": time.time() - start,
                        "base_url_used": used_base_url,
                        "thinking_note": "thinking_disabled_retry_unsupported",
                    }
                return {
                    "status": "error",
                    "content": "",
                    "error": f"HTTP {retry_exc.code}: {retry_body}",
                    "latency_seconds": time.time() - start,
                    "base_url_used": used_base_url,
                    "thinking_note": "thinking_disabled_retry_unsupported",
                }
        return {
            "status": "error",
            "content": "",
            "error": f"HTTP {exc.code}: {error_body}",
            "latency_seconds": time.time() - start,
            "base_url_used": used_base_url,
            "thinking_note": thinking_note,
        }
    except Exception as exc:
        return {
            "status": "error",
            "content": "",
            "error": sanitize_error(exc, api_key),
            "latency_seconds": time.time() - start,
            "base_url_used": used_base_url,
            "thinking_note": thinking_note,
        }


def source_prompt_path(micro_prompt_path):
    candidate = micro_prompt_path.with_name("pilot_prompt_pack.jsonl")
    if candidate.exists():
        return candidate
    return micro_prompt_path


def filter_prompts(rows, case_ids):
    selected = [row for row in rows if row.get("case_id") in set(case_ids)]
    order = {strategy: index for index, strategy in enumerate(STRATEGY_ORDER)}
    selected.sort(key=lambda row: (case_ids.index(row.get("case_id")), order.get(row.get("strategy"), 999)))
    return selected


def strengthen_prompt_text(text):
    marker = "Citation rules:"
    text = remove_current_unit_labels(text)
    if marker in text:
        return text
    old_shape = "Use this output shape: 1. one concise next action; 2. memory-backed rationale using cited memory ids where applicable."
    base = text.replace(old_shape, "").rstrip()
    closing = "Write only the assistant response or task update. Do not mention routing labels, gold labels, or benchmark strategy names."
    if closing in base:
        base = base.replace(closing, "").rstrip()
    return "\n".join([base, "", *STRENGTHENED_RULES, "", closing])


def remove_current_unit_labels(text):
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        prefix = line[: len(line) - len(stripped)]
        if stripped.startswith("- u") and ": " in stripped:
            maybe_unit, rest = stripped[2:].split(": ", 1)
            if len(maybe_unit) > 1 and maybe_unit[0] == "u" and maybe_unit[1:].isdigit():
                lines.append(prefix + "- " + rest)
                continue
        lines.append(line)
    return "\n".join(lines)


def strengthen_prompts(rows):
    strengthened = []
    for row in rows:
        updated = dict(row)
        updated["prompt_text"] = strengthen_prompt_text(row.get("prompt_text", ""))
        strengthened.append(updated)
    return strengthened


def build_report(path, model, base_url_used, case_ids, responses, total_latency, thinking_notes):
    ok_count = sum(1 for row in responses if row["api_status"] == "ok")
    error_count = sum(1 for row in responses if row["api_status"] == "error")
    auth_error_count = sum(1 for row in responses if row["api_status"] == "auth_error")
    strategy_count = len(set(row["strategy"] for row in responses))
    lines = [
        "# LLM Downstream-Lite Micro-Pilot Report",
        "",
        "This report summarizes a 2-case API micro-pilot. It is not a full downstream evaluation and does not prove downstream utility.",
        "",
        "## Run Summary",
        "",
        f"- Model: `{model}`",
        f"- Base URL form used: `{base_url_used or 'none'}`",
        f"- Case IDs: {case_ids}",
        f"- Strategy count: {strategy_count}",
        f"- API calls attempted: {len(responses)}",
        f"- OK responses: {ok_count}",
        f"- Error responses: {error_count}",
        f"- Auth errors: {auth_error_count}",
        f"- Total latency seconds: {total_latency:.3f}",
        f"- Thinking mode notes: {sorted(set(thinking_notes))}",
        "",
        "## Claim Boundaries",
        "",
        "- This is a tiny output-level micro-pilot, not a downstream utility proof.",
        "- It uses fixed candidate memories and saved router predictions only.",
        "- It does not evaluate a real retriever, live router inference, memory writing, updating, merging, or lifecycle behavior.",
        "- Citation metrics are partial automatic checks; task quality and uncited hallucination still need review.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--out-responses", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--max-tokens", type=int, default=180)
    args = parser.parse_args()

    env_path, env_values = load_env_file()
    api_key = env_value(env_values, "MEMORY_ROUTER_API_KEY")
    base_url = env_value(env_values, "MEMORY_ROUTER_BASE_URL").rstrip("/")
    model = env_value(env_values, "MEMORY_ROUTER_MODEL")
    if not api_key or not base_url or not model:
        raise SystemExit("Missing MEMORY_ROUTER_API_KEY, MEMORY_ROUTER_BASE_URL, or MEMORY_ROUTER_MODEL")

    source_path = source_prompt_path(args.prompts)
    rows = load_jsonl(source_path)
    prompts = strengthen_prompts(filter_prompts(rows, args.case_id))
    expected_count = len(args.case_id) * len(STRATEGY_ORDER)
    if len(prompts) != expected_count:
        raise SystemExit(f"Expected {expected_count} prompts but found {len(prompts)}")
    write_jsonl(args.prompts, prompts)

    responses = []
    base_url_used = ""
    thinking_notes = []
    total_latency = 0.0
    for prompt in prompts:
        result = call_api(api_key, base_url, model, prompt["prompt_text"], args.temperature, args.max_tokens)
        base_url_used = result["base_url_used"] or base_url_used
        thinking_notes.append(result["thinking_note"])
        total_latency += result["latency_seconds"]
        row = {
            "prompt_id": prompt["prompt_id"],
            "case_id": prompt["case_id"],
            "strategy": prompt["strategy"],
            "model": model,
            "temperature": args.temperature,
            "response_text": result["content"],
            "api_status": "ok" if result["status"] == "ok" else result["status"],
            "error": result["error"],
            "latency_seconds": result["latency_seconds"],
        }
        responses.append(row)
        write_jsonl(args.out_responses, responses)
        if result["status"] == "auth_error":
            build_report(args.report, model, base_url_used, args.case_id, responses, total_latency, thinking_notes)
            raise SystemExit("Authentication failed; stopped immediately.")
        time.sleep(0.25)

    build_report(args.report, model, base_url_used, args.case_id, responses, total_latency, thinking_notes)
    print(f"Micro-pilot prompts: {len(prompts)}")
    print(f"API calls attempted: {len(responses)}")
    print(f"OK responses: {sum(1 for row in responses if row['api_status'] == 'ok')}")
    print(f"Error responses: {sum(1 for row in responses if row['api_status'] != 'ok')}")
    print(f"Env file loaded: {env_path if env_path else 'none'}")
    print(f"Base URL form used: {base_url_used}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

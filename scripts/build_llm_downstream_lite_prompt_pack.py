#!/usr/bin/env python3
"""Build derived LLM downstream-lite prompt fixtures.

This script uses locked gold cases and saved router predictions only. It does
not load models, call APIs, train, retrieve, or modify source artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


STRATEGIES = [
    "no_memory",
    "all_candidates",
    "router_selected",
    "oracle_selected",
    "top_k_naive",
    "random_k",
    "shuffled_top_k",
]

TOP_K_NAIVE_K = 3
MAX_CASES = 24
MAX_TEXT_CHARS = 1000
RANDOM_BASELINE_SEED = "dmpr-v10-random-k-seed-2026-06-08"
SHUFFLED_TOP_K_SEED = "dmpr-v10-shuffled-top-k-seed-2026-06-08"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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


def parse_raw_output(raw_output: Any) -> dict[str, Any]:
    if not isinstance(raw_output, str) or not raw_output.strip():
        raise ValueError("missing raw_output string")
    text = raw_output.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("raw_output did not parse to an object")
    return parsed


def stable_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def store_set(policy: dict[str, Any]) -> set[tuple[str, str]]:
    result: set[tuple[str, str]] = set()
    for item in policy.get("store", []):
        if not isinstance(item, dict):
            continue
        unit_id = item.get("unit_id")
        target = item.get("target")
        if isinstance(unit_id, str) and isinstance(target, str):
            result.add((unit_id, target))
    return result


def redact_text(text: str, limit: int = 180) -> str:
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[redacted-email]", text)
    text = re.sub(r"\+?\d[\d .()-]{7,}\d", "[redacted-phone]", text)
    text = re.sub(r"@[A-Za-z0-9_.-]+", "[redacted-handle]", text)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def memory_id(memory: dict[str, Any]) -> str:
    value = memory.get("memory_id") or memory.get("id")
    if not isinstance(value, str):
        raise ValueError("candidate memory missing string id")
    return value


def stable_shuffled_ids(candidate_ids: list[str], case_id: str, seed: str) -> list[str]:
    return sorted(
        candidate_ids,
        key=lambda item: hashlib.sha256(f"{seed}:{case_id}:{item}".encode("utf-8")).hexdigest(),
    )


def selected_ids(case: dict[str, Any], router_read: list[str], strategy: str) -> list[str]:
    candidate_ids = [memory_id(memory) for memory in case["candidate_memories"]]
    gold_read = stable_strings(case["gold"].get("read"))
    if strategy == "no_memory":
        return []
    if strategy == "all_candidates":
        return candidate_ids
    if strategy == "router_selected":
        return [memory_id for memory_id in router_read if memory_id in set(candidate_ids)]
    if strategy == "oracle_selected":
        return [memory_id for memory_id in gold_read if memory_id in set(candidate_ids)]
    if strategy == "top_k_naive":
        return candidate_ids[:TOP_K_NAIVE_K]
    if strategy == "random_k":
        return stable_shuffled_ids(candidate_ids, case["case_id"], RANDOM_BASELINE_SEED)[:TOP_K_NAIVE_K]
    if strategy == "shuffled_top_k":
        return stable_shuffled_ids(candidate_ids, case["case_id"], SHUFFLED_TOP_K_SEED)[:TOP_K_NAIVE_K]
    raise ValueError(f"unknown strategy: {strategy}")


def case_size(case: dict[str, Any]) -> int:
    memory_chars = sum(len(str(memory.get("text", ""))) for memory in case.get("candidate_memories", []))
    unit_chars = sum(len(str(unit.get("text", ""))) for unit in case.get("current_units", []))
    return memory_chars + unit_chars


def numeric_tokens(text: str) -> set[str]:
    pattern = r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|seconds?|minutes?|minute|consecutive|items?|rules?|days?|weeks?|months?|quarterly)?\b"
    return {match.strip().lower() for match in re.findall(pattern, text, flags=re.IGNORECASE)}


def numeric_units(values: set[str]) -> set[str]:
    result: set[str] = set()
    for value in values:
        unit = re.sub(r"^\d+(?:\.\d+)?\s*", "", value).strip()
        if unit:
            result.add(unit)
    return result


def contradiction_risk(case: dict[str, Any]) -> dict[str, Any]:
    memory_text = " ".join(str(memory.get("text", "")) for memory in case.get("candidate_memories", []))
    unit_text = " ".join(str(unit.get("text", "")) for unit in case.get("current_units", []))
    memory_numbers = numeric_tokens(memory_text)
    current_numbers = numeric_tokens(unit_text)
    shared_units = sorted(numeric_units(memory_numbers).intersection(numeric_units(current_numbers)))
    conflicting_values = sorted((memory_numbers - current_numbers).union(current_numbers - memory_numbers))
    has_risk = bool(memory_numbers and current_numbers and shared_units and conflicting_values)
    return {
        "level": "exclude_numeric_conflict" if has_risk else "none",
        "reason": "Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test." if has_risk else "No simple numeric contradiction pattern detected.",
        "memory_numeric_tokens": sorted(memory_numbers),
        "current_numeric_tokens": sorted(current_numbers),
        "shared_numeric_units": shared_units,
    }


def classify_case(case: dict[str, Any], prediction: dict[str, Any]) -> tuple[str, str] | None:
    gold = case["gold"]
    gold_read = set(stable_strings(gold.get("read")))
    pred_read = set(stable_strings(prediction.get("read")))
    gold_store = store_set(gold)
    pred_store = store_set(prediction)
    gold_skip = set(stable_strings(gold.get("skip")))
    pred_skip = set(stable_strings(prediction.get("skip")))
    read_exact = gold_read == pred_read
    write_exact = gold_store == pred_store and gold_skip == pred_skip
    all_ids = {memory_id(memory) for memory in case["candidate_memories"]}
    irrelevant_all = len(all_ids - gold_read)
    irrelevant_router = len(pred_read - gold_read)

    if irrelevant_all > 0 and irrelevant_router < irrelevant_all:
        return "irrelevant_memory_reduction", "Router selects fewer irrelevant memories than all-candidates injection."
    if read_exact and write_exact:
        return "full_exact_or_read_exact", "Router READ, STORE, and SKIP match the locked reference."
    if write_exact and not read_exact:
        return "read_mismatch_write_correct", "Router READ differs while STORE and SKIP match the locked reference."
    return None


def select_cases(
    gold_rows: list[dict[str, Any]],
    predictions_by_case: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    buckets: dict[str, list[dict[str, Any]]] = {
        "full_exact_or_read_exact": [],
        "read_mismatch_write_correct": [],
        "irrelevant_memory_reduction": [],
    }
    skipped: list[dict[str, str]] = []

    for case in gold_rows:
        case_id = case.get("case_id")
        if not isinstance(case_id, str):
            skipped.append({"case_id": "unknown", "reason": "missing string case_id"})
            continue
        if "sensitive_boundary" in set(case.get("tags", [])):
            skipped.append({"case_id": case_id, "reason": "excluded sensitive-boundary case"})
            continue
        if case_size(case) > MAX_TEXT_CHARS:
            skipped.append({"case_id": case_id, "reason": "excluded long case"})
            continue
        risk = contradiction_risk(case)
        if risk["level"] != "none":
            skipped.append({"case_id": case_id, "reason": f"excluded contradiction risk: {risk['reason']}"})
            continue
        prediction = predictions_by_case.get(case_id)
        if prediction is None:
            skipped.append({"case_id": case_id, "reason": "missing saved prediction"})
            continue
        classification = classify_case(case, prediction)
        if classification is None:
            skipped.append({"case_id": case_id, "reason": "not selected by fixture balance rules"})
            continue
        category, reason = classification
        buckets[category].append({"case": case, "prediction": prediction, "category": category, "selection_reason": reason})

    selected: list[dict[str, Any]] = []
    quotas = {
        "full_exact_or_read_exact": 8,
        "read_mismatch_write_correct": 10,
        "irrelevant_memory_reduction": 6,
    }
    used: set[str] = set()
    for category, quota in quotas.items():
        for item in buckets[category]:
            case_id = item["case"]["case_id"]
            if case_id in used:
                continue
            selected.append(item)
            used.add(case_id)
            if sum(1 for selected_item in selected if selected_item["category"] == category) >= quota:
                break

    if len(selected) < MAX_CASES:
        for category in buckets:
            for item in buckets[category]:
                case_id = item["case"]["case_id"]
                if case_id in used:
                    continue
                selected.append(item)
                used.add(case_id)
                if len(selected) >= MAX_CASES:
                    break
            if len(selected) >= MAX_CASES:
                break

    return selected[:MAX_CASES], skipped


def build_case_fixture(item: dict[str, Any], gold_path: Path, predictions_path: Path) -> dict[str, Any]:
    case = item["case"]
    prediction = item["prediction"]
    pred_read = stable_strings(prediction.get("read"))
    gold_read = stable_strings(case["gold"].get("read"))
    strategy_ids = {strategy: selected_ids(case, pred_read, strategy) for strategy in STRATEGIES}
    current_units = [
        {
            "unit_id": unit["unit_id"],
            "safe_text": redact_text(str(unit.get("text", ""))),
            "tags": unit.get("tags", []),
        }
        for unit in case.get("current_units", [])
    ]
    memories = [
        {
            "memory_id": memory_id(memory),
            "target": memory.get("target"),
            "safe_text": redact_text(str(memory.get("text", ""))),
            "tags": memory.get("tags", []),
        }
        for memory in case.get("candidate_memories", [])
    ]
    return {
        "case_id": case["case_id"],
        "fixture_status": "derived_review_required_not_locked_gold",
        "category": item["category"],
        "selection_reason": item["selection_reason"],
        "source": {
            "gold_path": str(gold_path),
            "prediction_path": str(predictions_path),
            "original_case_id": case["case_id"],
        },
        "runtime_context": case.get("runtime_context", {}),
        "candidate_memories": memories,
        "current_units": current_units,
        "gold_read_ids": gold_read,
        "predicted_read_ids": pred_read,
        "gold_store": case["gold"].get("store", []),
        "predicted_store": prediction.get("store", []),
        "gold_skip_ids": stable_strings(case["gold"].get("skip")),
        "predicted_skip_ids": stable_strings(prediction.get("skip")),
        "selected_ids_by_strategy": strategy_ids,
        "contradiction_risk": contradiction_risk(case),
        "limitations": "Derived fixture for later prompt execution; not new gold and not an answer-quality result.",
    }


def prompt_text(case_fixture: dict[str, Any], strategy: str, injected_ids: list[str]) -> str:
    memory_by_id = {memory["memory_id"]: memory for memory in case_fixture["candidate_memories"]}
    injected = [memory_by_id[memory_id] for memory_id in injected_ids if memory_id in memory_by_id]
    lines = [
        "You are assisting with a coding/business-agent task.",
        "Given the current task notes and the provided memory context, write a concise next-step response for the assistant.",
        "Use relevant memory facts if they are helpful. Do not invent memory facts.",
        "When you use a memory fact, cite its memory id in brackets, e.g. [m2].",
        "Do not cite memory ids for facts not present in the provided memory context.",
        "Keep the response to 80 words or fewer and no more than 4 sentences.",
        "Use this output shape: 1. one concise next action; 2. memory-backed rationale using cited memory ids where applicable.",
        "",
        "Current task context:",
        json.dumps(case_fixture.get("runtime_context", {}), sort_keys=True),
        "",
        "Current units:",
    ]
    for unit in case_fixture["current_units"]:
        lines.append(f"- {unit['safe_text']}")
    lines.append("")
    lines.append("Provided memory context:")
    if injected:
        for memory in injected:
            lines.append(f"- {memory['memory_id']} [{memory.get('target', 'unknown')}]: {memory['safe_text']}")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "Write only the assistant response or task update. Do not mention routing labels, gold labels, or benchmark strategy names.",
        ]
    )
    return "\n".join(lines)


def rubric() -> dict[str, Any]:
    return {
        "required_memory_fact_coverage": {
            "scale": "0/1/2",
            "meaning": "End-to-end coverage against gold-required memory ids, regardless of whether the strategy injected them. 0 misses required memory facts; 1 partially uses them; 2 uses the important required facts correctly.",
        },
        "conditional_injected_required_coverage": {
            "scale": "0/1/2/null",
            "meaning": "Optional decomposition over required memory ids that were actually injected. Use null when no required memory was injected. This separates router-dropped facts from LLM-ignored injected facts.",
        },
        "irrelevant_memory_contamination": {
            "scale": "0/1/2",
            "meaning": "0 no irrelevant memory use; 1 minor irrelevant mention; 2 response is materially contaminated.",
            "lower_is_better": True,
        },
        "hallucinated_memory_usage": {
            "scale": "0/1/2",
            "meaning": "0 no invented memory facts; 1 minor unsupported inference; 2 clear invented memory facts.",
            "lower_is_better": True,
        },
        "citation_accuracy": {
            "scale": "0/1/2",
            "meaning": "0 citations match provided memory facts; 1 minor citation error; 2 cites ids that are absent or unsupported.",
            "lower_is_better": True,
        },
        "task_response_quality": {
            "scale": "0/1/2",
            "meaning": "0 not useful; 1 partially useful; 2 concise, grounded, and actionable.",
        },
        "total_score_formula": "required_memory_fact_coverage + task_response_quality - irrelevant_memory_contamination - hallucinated_memory_usage - citation_accuracy",
    }


def build_prompts(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    for case_fixture in cases:
        expected_required = case_fixture["gold_read_ids"]
        for strategy in STRATEGIES:
            injected_ids = case_fixture["selected_ids_by_strategy"][strategy]
            expected_avoid = [memory_id for memory_id in injected_ids if memory_id not in set(expected_required)]
            prompts.append(
                {
                    "prompt_id": f"{case_fixture['case_id']}__{strategy}",
                    "case_id": case_fixture["case_id"],
                    "strategy": strategy,
                    "source": case_fixture["source"],
                    "injected_memory_ids": injected_ids,
                    "current_units": case_fixture["current_units"],
                    "prompt_text": prompt_text(case_fixture, strategy, injected_ids),
                    "expected_required_memory_ids": expected_required,
                    "expected_injected_required_memory_ids": [item for item in injected_ids if item in set(expected_required)],
                    "expected_avoid_memory_ids": expected_avoid,
                    "contradiction_risk": case_fixture["contradiction_risk"],
                    "rubric": rubric(),
                    "limitations": "Execution fixture only; later answers must be collected and judged before making downstream claims.",
                }
            )
    return prompts


def build_audit_trace(prompts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "prompt_id": prompt["prompt_id"],
            "case_id": prompt["case_id"],
            "strategy": prompt["strategy"],
            "injected_memory_ids": prompt["injected_memory_ids"],
            "expected_required_memory_ids": prompt["expected_required_memory_ids"],
            "expected_avoid_memory_ids": prompt["expected_avoid_memory_ids"],
            "cited_memory_ids": [],
            "missing_required_citations": [],
            "irrelevant_citations": [],
            "hallucinated_citations": [],
            "judge_scores": None,
        }
        for prompt in prompts
    ]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def build_report(cases: list[dict[str, Any]], prompts: list[dict[str, Any]], skipped: list[dict[str, str]], command: str) -> str:
    category_counts = Counter(case["category"] for case in cases)
    strategy_counts = Counter(prompt["strategy"] for prompt in prompts)
    lines = [
        "# LLM Downstream-Lite Design Report",
        "",
        "This report describes derived prompt fixtures for a later harness-style LLM downstream-lite run. No LLM was called and no router model was loaded.",
        "",
        "## Command",
        "",
        "```bash",
        command,
        "```",
        "",
        "## Selected Cases",
        "",
        "| Case ID | Category | Selection reason | Gold READ | Router READ |",
        "| --- | --- | --- | --- | --- |",
    ]
    for case in cases:
        lines.append(
            f"| `{case['case_id']}` | `{case['category']}` | {case['selection_reason']} | {case['gold_read_ids']} | {case['predicted_read_ids']} |"
        )
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Cases generated: {len(cases)}",
            f"- Prompt objects generated: {len(prompts)}",
            f"- Case category distribution: {dict(sorted(category_counts.items()))}",
            f"- Strategy distribution: {dict(sorted(strategy_counts.items()))}",
            "- Each prompt requires memory-id citations for used memory facts.",
            "- Cases with simple numeric contradiction risk are excluded from the main execution pack rather than silently mixed in.",
            "",
            "## Skipped Cases",
            "",
            "The builder skips cases with sensitive-boundary tags, long raw text, simple numeric contradiction risk, missing predictions, or categories not needed for this balanced pack.",
            f"Skipped count: {len(skipped)}",
            "",
            "| Case ID | Reason |",
            "| --- | --- |",
        ]
    )
    for item in skipped[:40]:
        lines.append(f"| `{item['case_id']}` | {item['reason']} |")
    if len(skipped) > 40:
        lines.append(f"| ... | {len(skipped) - 40} additional skipped cases omitted from this report table. |")
    lines.extend(
        [
            "",
            "## Risks And Claim Boundaries",
            "",
            "- The fixtures are derived benchmark inputs, not new locked gold.",
            "- The pack compares memory injection strategies with fixed candidate memories; it does not evaluate retrieval.",
            "- It uses saved router predictions, not live router inference.",
            "- The pack includes citation instructions to support partial automatic checks, but final scoring still requires response review.",
            "- End-to-end required-memory coverage should penalize strategies that failed to inject required memory; conditional injected-required coverage is only a diagnostic decomposition.",
            "- The prompt pack has not been executed or judged.",
            "- Any later answer-quality claim needs collected responses, manual or LLM-judge scoring, and clear uncertainty notes.",
            "",
            "## Review Recommendation",
            "",
            "Ask an Opus/friend reviewer to inspect this prompt pack before execution, especially the rubric, prompt wording, and whether selected cases are sufficiently understandable without adding fabricated context.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--out-cases", type=Path, required=True)
    parser.add_argument("--out-prompts", type=Path, required=True)
    parser.add_argument("--out-report", type=Path, required=True)
    parser.add_argument("--out-audit-trace", type=Path)
    args = parser.parse_args()

    gold_rows = load_jsonl(args.gold)
    prediction_rows = load_jsonl(args.predictions)
    predictions_by_case = {
        row["case_id"]: parse_raw_output(row.get("raw_output"))
        for row in prediction_rows
        if isinstance(row.get("case_id"), str)
    }
    selected, skipped = select_cases(gold_rows, predictions_by_case)
    if not selected:
        args.out_report.parent.mkdir(parents=True, exist_ok=True)
        args.out_report.write_text(
            "# LLM Downstream-Lite Design Report\n\nNo safe fixture extraction was possible; no cases were generated.\n",
            encoding="utf-8",
        )
        return 1

    case_fixtures = [build_case_fixture(item, args.gold, args.predictions) for item in selected]
    prompts = build_prompts(case_fixtures)
    audit_trace = build_audit_trace(prompts)
    write_jsonl(args.out_cases, case_fixtures)
    write_jsonl(args.out_prompts, prompts)
    audit_trace_path = args.out_audit_trace or args.out_prompts.with_name("llm_downstream_lite_audit_trace_template.jsonl")
    write_jsonl(audit_trace_path, audit_trace)
    command = (
        "python3 scripts/build_llm_downstream_lite_prompt_pack.py "
        f"--gold {args.gold} --predictions {args.predictions} "
        f"--out-cases {args.out_cases} --out-prompts {args.out_prompts} --out-report {args.out_report}"
    )
    args.out_report.parent.mkdir(parents=True, exist_ok=True)
    args.out_report.write_text(build_report(case_fixtures, prompts, skipped, command), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

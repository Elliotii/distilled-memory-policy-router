#!/usr/bin/env python3
"""Build the hard READ downstream pilot prompt pack.

This script is a deterministic file builder. It does not call APIs or run any
model.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


JsonDict = Dict[str, object]
SENSITIVE_PLACEHOLDER_RE = re.compile(r"\b[A-Z]{2,}-\d{2,}\b")

RUBRIC_SCALE = {
    "required_fact_coverage": "0=no required facts, 1=partial, 2=complete",
    "irrelevant_memory_contamination": "0=clear contamination, 1=minor/ambiguous, 2=none",
    "stale_or_contradictory_use": "0=uses stale/contradictory facts, 1=mentions but resists, 2=none",
    "hallucinated_memory_use": "0=clear hallucination, 1=minor unsupported fact, 2=none",
    "task_response_quality": "0=not useful, 1=partly useful, 2=useful and actionable",
    "citation_compliance": "0=bad/missing/invalid citations, 1=partial, 2=clean",
}


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


def write_jsonl(path: str, rows: Iterable[JsonDict]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def redact_prompt_memory_text(text: str) -> Tuple[str, bool]:
    redacted = SENSITIVE_PLACEHOLDER_RE.sub("<REDACTED_SAMPLE_TOKEN>", text)
    return redacted, redacted != text


def current_unit_text(units: List[JsonDict]) -> str:
    return "\n".join(f"- {unit['text']}" for unit in units)


def memory_context(injected_ids: List[str], memory_by_id: Dict[str, JsonDict]) -> Tuple[str, bool]:
    if not injected_ids:
        return "No prior memory context is available.", False

    lines = []
    any_redaction = False
    for memory_id in injected_ids:
        memory = memory_by_id[memory_id]
        text, redacted = redact_prompt_memory_text(str(memory["text"]))
        any_redaction = any_redaction or redacted
        lines.append(f"[{memory_id}] {text}")
    return "\n".join(lines), any_redaction


def prompt_text(case: JsonDict, injected_ids: List[str], memory_by_id: Dict[str, JsonDict]) -> Tuple[str, bool]:
    context = case.get("runtime_context", {})
    memory_block, redaction_applied = memory_context(injected_ids, memory_by_id)

    if injected_ids:
        example_id = injected_ids[0]
        citation_rule = (
            "Use prior memory facts if they help. Cite each memory fact with its exact "
            f"bracketed memory ID, such as [{example_id}]. Do not cite memory IDs that "
            "are not present in the prior memory context. Cite memory IDs only when "
            "using memory facts. Do not cite current task notes."
        )
    else:
        citation_rule = (
            "No prior memory context is available. Answer from the current task notes "
            "only and do not include bracketed memory citations."
        )

    text = (
        "Write 2-4 concise bullets or sentences, 120 words or fewer.\n\n"
        f"Project: {context.get('project', '')}\n"
        f"Repo: {context.get('repo', '')}\n"
        f"Service: {context.get('service', '')}\n"
        f"Task: {context.get('task', '')}\n\n"
        "Current task notes:\n"
        f"{current_unit_text(case.get('current_units', []))}\n\n"
        "Prior memory context:\n"
        f"{memory_block}\n\n"
        f"Citation rules: {citation_rule}\n\n"
        "Do not mention evaluation setup or selection methods. Do not invent memory IDs."
    )
    return text, redaction_applied


def build_rows(
    *,
    cases: List[JsonDict],
    memories: List[JsonDict],
    by_case_rows: List[JsonDict],
    case_ids: List[str],
    strategies: List[str],
) -> Tuple[List[JsonDict], List[JsonDict], List[JsonDict]]:
    case_by_id = {str(row["case_id"]): row for row in cases}
    memory_by_id = {str(row["memory_id"]): row for row in memories}
    by_case_by_key = {
        (str(row["case_id"]), str(row["strategy"])): row
        for row in by_case_rows
    }

    missing_cases = [case_id for case_id in case_ids if case_id not in case_by_id]
    if missing_cases:
        raise ValueError("missing cases: " + ", ".join(missing_cases))

    missing_rows = [
        f"{case_id}/{strategy}"
        for case_id in case_ids
        for strategy in strategies
        if (case_id, strategy) not in by_case_by_key
    ]
    if missing_rows:
        raise ValueError("missing by-case rows: " + ", ".join(missing_rows))

    prompt_rows: List[JsonDict] = []
    response_rows: List[JsonDict] = []
    manual_rows: List[JsonDict] = []

    for case_id in case_ids:
        case = case_by_id[case_id]
        labels = case["labels"]
        for strategy in strategies:
            selection_row = by_case_by_key[(case_id, strategy)]
            injected_ids = [str(item) for item in selection_row["injected_memory_ids_post_budget"]]
            for memory_id in injected_ids:
                if memory_id not in memory_by_id:
                    raise ValueError(f"{case_id}/{strategy}: memory not found: {memory_id}")

            prompt_id = f"{case_id}__{strategy}"
            rendered_prompt, redaction_applied = prompt_text(case, injected_ids, memory_by_id)
            prompt_rows.append({
                "prompt_id": prompt_id,
                "case_id": case_id,
                "strategy": strategy,
                "user_input": case["user_input"],
                "runtime_context": case["runtime_context"],
                "current_units": case["current_units"],
                "injected_memory_ids": injected_ids,
                "required_memory_ids": labels.get("required_memory_ids", []),
                "helpful_memory_ids": labels.get("helpful_memory_ids", []),
                "avoid_memory_ids": labels.get("avoid_memory_ids", []),
                "stale_or_harmful_memory_ids": labels.get("stale_or_harmful_memory_ids", []),
                "contradictory_memory_ids": labels.get("contradictory_memory_ids", []),
                "wrong_scope_memory_ids": labels.get("wrong_scope_memory_ids", []),
                "expected_answer_requirements": case.get("expected_answer_requirements", []),
                "redaction_applied": redaction_applied,
                "prompt_text": rendered_prompt,
            })
            response_rows.append({
                "prompt_id": prompt_id,
                "case_id": case_id,
                "strategy": strategy,
                "model": None,
                "api_status": "not_run",
                "response_text": "",
                "latency_seconds": None,
                "error": None,
            })
            manual_rows.append({
                "prompt_id": prompt_id,
                "case_id": case_id,
                "strategy": strategy,
                "response_text": "",
                "auto_metrics": {},
                "manual_scores": {
                    "required_fact_coverage": None,
                    "irrelevant_memory_contamination": None,
                    "stale_or_contradictory_use": None,
                    "hallucinated_memory_use": None,
                    "task_response_quality": None,
                    "citation_compliance": None,
                },
                "rubric_scale": RUBRIC_SCALE,
                "review_notes": "",
            })

    return prompt_rows, response_rows, manual_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build hard READ downstream pilot prompt pack")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--memory-pool", required=True)
    parser.add_argument("--by-case", required=True)
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--strategy", action="append", required=True)
    parser.add_argument("--out-prompts", required=True)
    parser.add_argument("--out-responses", required=True)
    parser.add_argument("--out-manual", required=True)
    args = parser.parse_args()

    prompt_rows, response_rows, manual_rows = build_rows(
        cases=load_jsonl(args.cases),
        memories=load_jsonl(args.memory_pool),
        by_case_rows=load_jsonl(args.by_case),
        case_ids=args.case_id,
        strategies=args.strategy,
    )

    write_jsonl(args.out_prompts, prompt_rows)
    write_jsonl(args.out_responses, response_rows)
    write_jsonl(args.out_manual, manual_rows)

    print(json.dumps({
        "prompts": len(prompt_rows),
        "responses": len(response_rows),
        "manual_rows": len(manual_rows),
        "redacted_prompts": sum(1 for row in prompt_rows if row["redaction_applied"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

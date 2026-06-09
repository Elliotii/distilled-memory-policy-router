#!/usr/bin/env python3
"""Render expanded hard READ v2 cases into v05 Unit JSON router inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


JsonDict = dict[str, Any]


def load_jsonl(path: Path) -> list[JsonDict]:
    rows: list[JsonDict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return rows


def render_user_input(case: JsonDict) -> str:
    context = case["runtime_context"]
    context_lines = [
        "RUNTIME_CONTEXT",
        f"project: {context['project']}",
        f"repo: {context['repo']}",
        f"service: {context['service']}",
        f"task: {context['task']}",
    ]

    memory_lines = ["CANDIDATE_MEMORIES"]
    for memory in case["candidate_memories"]:
        memory_lines.append(
            f"{memory['memory_id']} [{memory['target']}]: {memory['text']}"
        )
    if len(memory_lines) == 1:
        memory_lines.append("NONE")

    unit_lines = ["CURRENT_UNITS"]
    for unit in case["current_units"]:
        unit_lines.append(f"{unit['unit_id']}: {unit['text']}")

    return "\n".join(context_lines + [""] + memory_lines + [""] + unit_lines)


def memory_index(memory_rows: list[JsonDict]) -> dict[str, JsonDict]:
    index: dict[str, JsonDict] = {}
    for memory in memory_rows:
        memory_id = memory["memory_id"]
        if memory_id in index:
            raise ValueError(f"duplicate memory_id in pool: {memory_id}")
        index[memory_id] = memory
    return index


def converted_case(case: JsonDict, memories_by_id: dict[str, JsonDict]) -> JsonDict:
    candidate_memories: list[JsonDict] = []
    for memory_id in case["candidate_memory_ids"]:
        if memory_id not in memories_by_id:
            raise ValueError(f"{case['case_id']}: missing memory_id {memory_id}")
        memory = memories_by_id[memory_id]
        candidate_memories.append(
            {
                "memory_id": memory["memory_id"],
                "target": memory["target"],
                "text": memory["text"],
                "tags": memory.get("flags", []),
                "project": memory.get("project", ""),
                "repo": memory.get("repo", ""),
                "service": memory.get("service", ""),
            }
        )

    labels = case["labels"]
    skip_unit_ids = [unit["unit_id"] for unit in case["current_units"]]
    return {
        "case_id": case["case_id"],
        "runtime_context": case["runtime_context"],
        "candidate_memories": candidate_memories,
        "current_units": case["current_units"],
        "gold": {
            "read": labels.get("required_memory_ids", []) + labels.get("helpful_memory_ids", []),
            "store": [],
            "skip": skip_unit_ids,
        },
        "tags": ["hard_read_v2_expanded", "read_only_render_for_offline_router"],
        "notes": "Converted from hard READ v2 expanded fixture for offline router prediction.",
    }


def leakage_errors(text: str) -> list[str]:
    lowered = text.lower()
    banned = [
        "required_memory_ids",
        "avoid_memory_ids",
        "stale_or_harmful_memory_ids",
        "contradictory_memory_ids",
        "wrong_scope_memory_ids",
        "candidate_labels",
        "oracle",
        "gold",
    ]
    return [item for item in banned if item in lowered]


def render_rows(cases: list[JsonDict], memory_rows: list[JsonDict]) -> tuple[list[JsonDict], JsonDict]:
    memories_by_id = memory_index(memory_rows)
    rendered: list[JsonDict] = []
    max_input_chars = 0
    max_candidate_count = 0
    leakage_case_count = 0

    for case in cases:
        v05_case = converted_case(case, memories_by_id)
        model_input = {
            "format": "v05_unit_json_user_input",
            "text": render_user_input(v05_case),
        }
        rendered_text = model_input["text"]
        errors = leakage_errors(json.dumps(model_input, ensure_ascii=False))
        if errors:
            leakage_case_count += 1
        rendered_input_hash = hashlib.sha256(rendered_text.encode("utf-8")).hexdigest()
        max_input_chars = max(max_input_chars, len(rendered_text))
        max_candidate_count = max(max_candidate_count, len(case["candidate_memory_ids"]))
        rendered.append(
            {
                "case_id": case["case_id"],
                "rendered_input_hash": rendered_input_hash,
                "candidate_memory_ids": case["candidate_memory_ids"],
                "model_input": model_input,
                "v05_router_case": v05_case,
                "eval_only": {
                    "source": "hard_read_v2_expanded_fixture_labels",
                    "gold_read_ids": v05_case["gold"]["read"],
                    "gold_store": [],
                    "gold_skip_unit_ids": v05_case["gold"]["skip"],
                    "labels": case["labels"],
                    "expected_answer_requirements": case.get("expected_answer_requirements", []),
                },
                "metadata": {
                    "source": "render_hard_read_v2_expanded_for_v05_router",
                    "schema_version": "v1",
                    "candidate_count": len(case["candidate_memory_ids"]),
                    "current_unit_count": len(case["current_units"]),
                    "model_input_label_leakage_terms": errors,
                },
            }
        )

    summary = {
        "row_count": len(rendered),
        "memory_pool_count": len(memory_rows),
        "max_model_input_chars": max_input_chars,
        "max_candidate_count": max_candidate_count,
        "model_input_label_leakage_case_count": leakage_case_count,
    }
    return rendered, summary


def write_jsonl(path: Path, rows: list[JsonDict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_report(path: Path, summary: JsonDict, out_jsonl: Path) -> None:
    lines = [
        "# Hard READ v2 Expanded v05 Router Render Report",
        "",
        "## Summary",
        "",
        f"- Row count: {summary['row_count']}",
        f"- Memory pool count: {summary['memory_pool_count']}",
        f"- Max model input chars: {summary['max_model_input_chars']}",
        f"- Max candidate count: {summary['max_candidate_count']}",
        f"- Output JSONL: `{out_jsonl}`",
        "",
        "## Input-Format Mapping Summary",
        "",
        "- `runtime_context` is preserved as v05 `RUNTIME_CONTEXT`.",
        "- `candidate_memory_ids` are resolved through the hard READ expanded memory pool and inlined as v05 `candidate_memories` in fixture order.",
        "- Memory `flags` are mapped to v05-compatible `tags` in the local case object.",
        "- `current_units` are preserved exactly.",
        "- Evaluation-only `gold.read` is required plus helpful memory IDs; `gold.store` is empty; `gold.skip` contains every current unit.",
        "",
        "## Label Leakage Check",
        "",
        f"- Model-input leakage case count: {summary['model_input_label_leakage_case_count']}",
        "- Labels, candidate labels, expected answer requirements, oracle/gold wording, API keys, and local model paths are not included in `model_input`.",
        "- Labels are retained only under `eval_only` for local scoring and must not be sent to the model.",
        "",
        "## Known Mismatches From v0.5g Format",
        "",
        "- The hard READ fixture uses 10 candidates per case, which may be outside common v0.5g training examples.",
        "- These are READ-focused cases; STORE is intentionally empty and all current units are marked as skip for format compatibility.",
        "- Hard negatives are stronger than ordinary entity-matching training examples.",
        "",
        "## Limitations",
        "",
        "- This render step does not load a model or adapter.",
        "- This render step does not create learned-router predictions.",
        "- This render step does not claim learned-router performance.",
        "",
        "## Next Step",
        "",
        "After the v0.5g adapter and local `QWEN35_MODEL_PATH` are available, run offline batch prediction with `src/v05/eval_lora_router.py --interface unit_json` against the rendered v05 router case rows or an equivalent case-only projection.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--memory-pool", required=True)
    parser.add_argument("--out-jsonl", required=True)
    parser.add_argument("--out-report", required=True)
    args = parser.parse_args()

    cases = load_jsonl(Path(args.cases))
    memory_rows = load_jsonl(Path(args.memory_pool))
    rows, summary = render_rows(cases, memory_rows)
    write_jsonl(Path(args.out_jsonl), rows)
    write_report(Path(args.out_report), summary, Path(args.out_jsonl))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

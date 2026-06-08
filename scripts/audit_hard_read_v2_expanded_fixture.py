#!/usr/bin/env python3
"""Audit the expanded hard READ v2 selection-only fixture."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_LABEL_KEYS = [
    "required_memory_ids",
    "helpful_memory_ids",
    "avoid_memory_ids",
    "stale_or_harmful_memory_ids",
    "contradictory_memory_ids",
    "wrong_scope_memory_ids",
    "candidate_labels",
]

PROMPT_FORBIDDEN_TERMS = [
    "required memory",
    "avoid memory",
    "stale memory",
    "contradictory memory",
    "wrong scope",
    "oracle",
    "gold",
]

FORBIDDEN_MEMORY_FIELDS = {"relevance_category", "hard_negative_type"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return rows


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 6) if values else 0.0


def current_unit_text(case: dict[str, Any]) -> str:
    return " ".join(str(unit.get("text", "")) for unit in case.get("current_units", []))


def domain_of(case: dict[str, Any]) -> str:
    runtime_domain = case.get("runtime_context", {}).get("domain")
    if runtime_domain:
        return str(runtime_domain)
    notes = str(case.get("notes", ""))
    marker = "domain="
    if marker in notes:
        return notes.split(marker, 1)[1].split(";", 1)[0].strip()
    return "unspecified"


def validate(cases: list[dict[str, Any]], memories: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(cases) != 32:
        errors.append(f"expected exactly 32 cases, found {len(cases)}")

    case_ids = [str(case.get("case_id", "")) for case in cases]
    duplicate_cases = sorted(case_id for case_id, count in Counter(case_ids).items() if count > 1)
    if duplicate_cases:
        errors.append(f"duplicate case_id values: {', '.join(duplicate_cases)}")

    memory_ids = [str(memory.get("memory_id", "")) for memory in memories]
    duplicate_memories = sorted(memory_id for memory_id, count in Counter(memory_ids).items() if count > 1)
    if duplicate_memories:
        errors.append(f"duplicate memory_id values: {', '.join(duplicate_memories)}")
    memory_id_set = set(memory_ids)

    global_relevance_rows: list[str] = []
    for memory in memories:
        present = sorted(FORBIDDEN_MEMORY_FIELDS & set(memory))
        if present:
            global_relevance_rows.append(f"{memory.get('memory_id')}: {', '.join(present)}")
    if global_relevance_rows:
        errors.append("memory pool contains global relevance fields: " + "; ".join(global_relevance_rows[:5]))

    first_four_recalls: list[float] = []
    first_four_distribution: Counter[str] = Counter()
    domain_distribution: Counter[str] = Counter()
    candidate_count_distribution: Counter[int] = Counter()
    hard_negative_distribution: Counter[str] = Counter()

    for case in cases:
        case_id = str(case.get("case_id", ""))
        candidate_ids = case.get("candidate_memory_ids", [])
        labels = case.get("labels", {})
        candidate_count_distribution[len(candidate_ids)] += 1
        domain_distribution[domain_of(case)] += 1

        if not 8 <= len(candidate_ids) <= 12:
            errors.append(f"{case_id}: candidate count must be 8-12, found {len(candidate_ids)}")
        if len(set(candidate_ids)) != len(candidate_ids):
            errors.append(f"{case_id}: duplicate candidate_memory_ids")

        missing = sorted(set(candidate_ids) - memory_id_set)
        if missing:
            errors.append(f"{case_id}: missing candidate memories: {', '.join(missing)}")

        for key in REQUIRED_LABEL_KEYS:
            if key not in labels:
                errors.append(f"{case_id}: labels missing {key}")

        required = labels.get("required_memory_ids", [])
        helpful = labels.get("helpful_memory_ids", [])
        avoid = labels.get("avoid_memory_ids", [])
        stale = labels.get("stale_or_harmful_memory_ids", [])
        contradictory = labels.get("contradictory_memory_ids", [])
        wrong_scope = labels.get("wrong_scope_memory_ids", [])
        candidate_labels = labels.get("candidate_labels", {})

        if len(required) < 2:
            errors.append(f"{case_id}: needs at least 2 required memories")
        if len(helpful) < 1:
            errors.append(f"{case_id}: needs at least 1 helpful memory")
        if len(avoid) < 4:
            errors.append(f"{case_id}: needs at least 4 avoid memories")
        if not stale and not contradictory:
            errors.append(f"{case_id}: needs stale_or_harmful or contradictory memory")
        if not wrong_scope:
            errors.append(f"{case_id}: needs at least 1 wrong_scope memory")

        for key, ids in [
            ("required_memory_ids", required),
            ("helpful_memory_ids", helpful),
            ("avoid_memory_ids", avoid),
            ("stale_or_harmful_memory_ids", stale),
            ("contradictory_memory_ids", contradictory),
            ("wrong_scope_memory_ids", wrong_scope),
        ]:
            non_candidates = sorted(set(ids) - set(candidate_ids))
            if non_candidates:
                errors.append(f"{case_id}: {key} contains non-candidates: {', '.join(non_candidates)}")

        if set(candidate_labels) != set(candidate_ids):
            errors.append(f"{case_id}: candidate_labels must cover all candidate ids")
        hard_negative_types = Counter()
        for label in candidate_labels.values():
            hard_negative_type = str(label.get("hard_negative_type", ""))
            hard_negative_types[hard_negative_type] += 1
            hard_negative_distribution[hard_negative_type] += 1
        if not (hard_negative_types.get("same_entity_irrelevant") or hard_negative_types.get("near_duplicate")):
            errors.append(f"{case_id}: needs same_entity_irrelevant or near_duplicate hard negative")

        prompt_text = f"{case.get('user_input', '')} {current_unit_text(case)}".lower()
        found_terms = [term for term in PROMPT_FORBIDDEN_TERMS if term in prompt_text]
        if found_terms:
            errors.append(f"{case_id}: prompt-facing fields contain label terms: {', '.join(found_terms)}")

        required_total = len(required)
        first_four_required = len(set(candidate_ids[:4]) & set(required))
        recall = round(first_four_required / required_total, 6) if required_total else 0.0
        first_four_recalls.append(recall)
        first_four_distribution[f"{recall:.2f}"] += 1

    mean_first_four = mean(first_four_recalls)
    if mean_first_four > 0.65:
        warnings.append(
            f"mean first-four required recall is {mean_first_four:.3f}, above the 0.65 order-bias diagnostic threshold"
        )

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "case_count": len(cases),
        "memory_count": len(memories),
        "unique_case_count": len(set(case_ids)),
        "unique_memory_count": len(set(memory_ids)),
        "candidate_count_distribution": dict(sorted(candidate_count_distribution.items())),
        "domain_distribution": dict(sorted(domain_distribution.items())),
        "hard_negative_type_distribution": dict(sorted(hard_negative_distribution.items())),
        "first_four_required_recall": {
            "mean": mean_first_four,
            "max": max(first_four_recalls) if first_four_recalls else 0.0,
            "distribution": dict(sorted(first_four_distribution.items())),
        },
        "claim_boundary": (
            "Fixture audit only; no downstream answer quality, no API calls, "
            "no model inference, no learned router/live LoRA behavior."
        ),
    }


def write_markdown(path: Path, audit: dict[str, Any]) -> None:
    lines = [
        "# Hard READ v2 Expanded Fixture Audit",
        "",
        "## Summary",
        "",
        f"- OK: {str(audit['ok']).lower()}",
        f"- Case count: {audit['case_count']}",
        f"- Memory count: {audit['memory_count']}",
        f"- Unique case count: {audit['unique_case_count']}",
        f"- Unique memory count: {audit['unique_memory_count']}",
        "",
        "## Candidate Count Distribution",
        "",
    ]
    for count, total in audit["candidate_count_distribution"].items():
        lines.append(f"- {count} candidates: {total} cases")

    lines.extend([
        "",
        "## Domain Distribution",
        "",
    ])
    for domain, total in audit["domain_distribution"].items():
        lines.append(f"- {domain}: {total}")

    lines.extend([
        "",
        "## Hard Negative Type Distribution",
        "",
    ])
    for hard_negative_type, total in audit["hard_negative_type_distribution"].items():
        lines.append(f"- {hard_negative_type}: {total}")

    first_four = audit["first_four_required_recall"]
    lines.extend([
        "",
        "## Candidate-Order Diagnostic",
        "",
        f"- Mean first-four required recall: {first_four['mean']:.3f}",
        f"- Max first-four required recall: {first_four['max']:.3f}",
        "- Distribution:",
    ])
    for recall, total in first_four["distribution"].items():
        lines.append(f"  - {recall}: {total} cases")

    lines.extend([
        "",
        "## Errors",
        "",
    ])
    if audit["errors"]:
        lines.extend([f"- {error}" for error in audit["errors"]])
    else:
        lines.append("- None.")

    lines.extend([
        "",
        "## Warnings",
        "",
    ])
    if audit["warnings"]:
        lines.extend([f"- {warning}" for warning in audit["warnings"]])
    else:
        lines.append("- None.")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This audit is structural and selection-fixture focused. It does not evaluate downstream answer quality, call an API, run model inference, train, load Qwen or LoRA, or establish production memory-system behavior.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--memory-pool", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    cases = load_jsonl(Path(args.cases))
    memories = load_jsonl(Path(args.memory_pool))
    audit = validate(cases, memories)
    Path(args.out_json).write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(Path(args.out_md), audit)
    print(json.dumps({"ok": audit["ok"], "case_count": audit["case_count"], "memory_count": audit["memory_count"]}, sort_keys=True))
    return 0 if audit["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

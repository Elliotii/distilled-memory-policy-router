"""Run deterministic v0.4 A/B/C interface smoke evaluation.

The runner builds raw outputs for three interfaces from deterministic baselines
and evaluates them with src.v04.metrics. It is a harness and smoke test only:
there is no model inference, API call, training, retriever, or writer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_jsonl_file
from src.v04.metrics import (
    INTERFACE_LEGACY_SPAN_JSON,
    INTERFACE_UNIT_DSL,
    INTERFACE_UNIT_JSON,
    INTERFACES,
    evaluate_prediction_rows,
    gold_canonical,
)


BASELINES = ("gold", "empty", "topk_read", "heuristic", "invalid_mock")
STOP_WORDS = {
    "a",
    "about",
    "after",
    "all",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "by",
    "do",
    "does",
    "for",
    "from",
    "has",
    "have",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "please",
    "should",
    "that",
    "the",
    "this",
    "to",
    "use",
    "we",
    "which",
    "with",
}


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def load_prediction_jsonl(path: Path | str) -> list[dict[str, str]]:
    path = Path(path)
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(row, dict):
                errors.append(f"line {line_number}: prediction row must be an object")
                continue

            required_nonempty = ("case_id", "interface", "system")
            for field in required_nonempty:
                if not isinstance(row.get(field), str) or not row.get(field):
                    errors.append(f"line {line_number}: {field} must be a non-empty string")
            if not isinstance(row.get("raw_output"), str):
                errors.append(f"line {line_number}: raw_output must be a string")

            interface = row.get("interface")
            if isinstance(interface, str) and interface not in INTERFACES:
                errors.append(f"line {line_number}: unknown interface {interface!r}")

            if not any(error.startswith(f"line {line_number}:") for error in errors):
                rows.append(
                    {
                        "case_id": row["case_id"],
                        "interface": row["interface"],
                        "system": row["system"],
                        "raw_output": row["raw_output"],
                    }
                )

    if errors:
        raise ValueError("\n".join(errors))
    return rows


def build_prediction_rows(
    cases: list[dict[str, Any]],
    *,
    interface: str,
    baseline: str,
    top_k: int = 1,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    system_name = display_system_name(baseline, top_k=top_k)
    for case in cases:
        raw_output = (
            render_invalid_prediction(interface)
            if baseline == "invalid_mock"
            else render_prediction(
                canonical_for_baseline(case, baseline=baseline, top_k=top_k),
                interface,
                case,
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "interface": interface,
                "system": system_name,
                "raw_output": raw_output,
            }
        )
    return rows


def run_prediction_file_evaluation(
    cases: list[dict[str, Any]],
    prediction_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in prediction_rows:
        grouped.setdefault((row["interface"], row["system"]), []).append(row)

    results: list[dict[str, Any]] = []
    for interface, system_name in sorted(grouped):
        results.append(
            evaluate_prediction_rows(
                cases,
                grouped[(interface, system_name)],
                interface=interface,
                system_name=system_name,
            )
        )
    return results


def run_evaluation(
    cases: list[dict[str, Any]],
    *,
    interfaces: list[str] | tuple[str, ...] = INTERFACES,
    baselines: list[str] | tuple[str, ...] = BASELINES,
    top_k: int = 1,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for interface in interfaces:
        for baseline in baselines:
            system_name = display_system_name(baseline, top_k=top_k)
            rows = build_prediction_rows(
                cases,
                interface=interface,
                baseline=baseline,
                top_k=top_k,
            )
            results.append(
                evaluate_prediction_rows(
                    cases,
                    rows,
                    interface=interface,
                    system_name=system_name,
                )
            )
    return results


def canonical_for_baseline(
    case: dict[str, Any],
    *,
    baseline: str,
    top_k: int = 1,
) -> dict[str, Any]:
    if baseline == "gold":
        return gold_canonical(case)
    if baseline == "empty":
        return _canonical(
            read_ids=[],
            store_entries=[],
            skip_ids=[unit["unit_id"] for unit in case["current_units"]],
        )
    if baseline == "topk_read":
        return _canonical(
            read_ids=[memory["memory_id"] for memory in case["candidate_memories"][:top_k]],
            store_entries=[],
            skip_ids=[unit["unit_id"] for unit in case["current_units"]],
        )
    if baseline == "heuristic":
        return heuristic_prediction(case)
    raise ValueError(f"unknown baseline: {baseline}")


def heuristic_prediction(case: dict[str, Any]) -> dict[str, Any]:
    read_ids = heuristic_read_ids(case)
    store_entries: list[dict[str, str]] = []
    skip_ids: list[str] = []
    for unit in case["current_units"]:
        target = heuristic_target_for_unit(unit["text"])
        if target is None:
            skip_ids.append(unit["unit_id"])
        else:
            store_entries.append({"target": target, "unit_id": unit["unit_id"]})
    return _canonical(read_ids=read_ids, store_entries=store_entries, skip_ids=skip_ids)


def heuristic_read_ids(case: dict[str, Any]) -> list[str]:
    context_text = " ".join(
        [
            *(unit["text"] for unit in case["current_units"]),
            *case.get("runtime_context", {}).values(),
        ]
    )
    query_tokens = content_tokens(context_text)
    scored: list[tuple[int, int, str]] = []
    for index, memory in enumerate(case["candidate_memories"]):
        memory_tokens = content_tokens(memory["content"])
        overlap = query_tokens & memory_tokens
        strong_overlap = {token for token in overlap if len(token) >= 6 or "_" in token or "-" in token}
        score = len(overlap) + len(strong_overlap)
        if score >= 3 or len(strong_overlap) >= 2:
            scored.append((score, -index, memory["memory_id"]))
    scored.sort(reverse=True)
    return [memory_id for _score, _index, memory_id in scored[:4]]


def heuristic_target_for_unit(text: str) -> str | None:
    lowered = text.lower()
    if _contains_any(
        lowered,
        (
            "api key",
            "private key",
            "recovery code",
            "test account password",
            "my password",
            "phone number",
            "home address",
            "backup email",
            "do_not_store",
            "weather",
            "thanks",
            "take a break",
            "for this one response",
            "local sandbox was slow",
            "maybe",
            "not decided",
            "sixth target",
            "sop skill",
            "skill system",
            "coffee",
        ),
    ):
        return None
    if "user prefers" in lowered or "i prefer" in lowered:
        return "user_profile"
    if _contains_any(
        lowered,
        (
            "next,",
            "next ",
            "blocked",
            "pending",
            "in progress",
            "not reviewed",
            "reproduced",
            "current task",
            "current phase",
            "remaining",
            "complete but",
            "do not edit",
            "for now",
        ),
    ):
        return "task_state"
    if (
        "/" in text
        or " live under " in lowered
        or " lives under " in lowered
        or "run with " in lowered
        or "python -m pytest" in lowered
        or "test command" in lowered
        or "tests live" in lowered
        or "fixtures" in lowered
        or "migrations" in lowered
        or "for this repo" in lowered
    ):
        return "repo_memory"
    if _contains_any(
        lowered,
        (
            "v0.4",
            "v0.5",
            "a/b/c",
            "pilot",
            "training",
            "memoryos",
            "project studies",
            "project compares",
            "fixed candidate memories",
            "pre-segmented units",
            "not locked gold",
        ),
    ):
        return "project_memory"
    if _contains_any(
        lowered,
        (
            "parser",
            "validator",
            "evaluator",
            "prompt builder",
            "service",
            "module",
            "job",
            "requires",
            "rejects",
            "reports",
            "checks",
            "caches",
            "retains",
            "generates",
            "suppresses",
            "exports",
            "expires",
            "deduplicates",
            "rounds",
            "publishes",
            "queues",
            "retries",
            "must",
            "should",
        ),
    ):
        return "service_memory"
    return None


def render_prediction(canonical: dict[str, Any], interface: str, case: dict[str, Any]) -> str:
    if interface == INTERFACE_UNIT_DSL:
        return render_unit_dsl(canonical, case)
    if interface == INTERFACE_UNIT_JSON:
        return render_unit_json(canonical, case)
    if interface == INTERFACE_LEGACY_SPAN_JSON:
        return render_legacy_span_json(canonical, case)
    raise ValueError(f"unknown interface: {interface}")


def render_unit_dsl(canonical: dict[str, Any], case: dict[str, Any]) -> str:
    read_ids = _ordered_read_ids(canonical, case)
    store_entries = _ordered_store_entries(canonical, case)
    skip_ids = _ordered_skip_ids(canonical, case)
    lines = [f"READ {','.join(read_ids) if read_ids else 'NONE'}"]
    if store_entries:
        lines.extend(f"STORE {entry['target']} {entry['unit_id']}" for entry in store_entries)
    else:
        lines.append("STORE NONE")
    lines.append(f"SKIP {','.join(skip_ids) if skip_ids else 'NONE'}")
    return "\n".join(lines)


def render_unit_json(canonical: dict[str, Any], case: dict[str, Any]) -> str:
    payload = {
        "read": _ordered_read_ids(canonical, case),
        "store": _ordered_store_entries(canonical, case),
        "skip": _ordered_skip_ids(canonical, case),
    }
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def render_legacy_span_json(canonical: dict[str, Any], case: dict[str, Any]) -> str:
    unit_text_by_id = {unit["unit_id"]: unit["text"] for unit in case["current_units"]}
    payload = {
        "read_hints": _ordered_read_ids(canonical, case),
        "write_spans": [
            {"span": unit_text_by_id[entry["unit_id"]], "type": entry["target"]}
            for entry in _ordered_store_entries(canonical, case)
        ],
        "ignore_spans": [
            unit_text_by_id[unit_id] for unit_id in _ordered_skip_ids(canonical, case)
        ],
    }
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def render_invalid_prediction(interface: str) -> str:
    if interface == INTERFACE_UNIT_DSL:
        return "READ m999\nSTORE fact u999\nSKIP u999"
    if interface == INTERFACE_UNIT_JSON:
        return json.dumps(
            {
                "read": ["m999"],
                "store": [{"target": "fact", "unit_id": "u999"}],
                "skip": ["u999"],
            },
            ensure_ascii=True,
            separators=(",", ":"),
        )
    if interface == INTERFACE_LEGACY_SPAN_JSON:
        return json.dumps(
            {
                "read_hints": ["m999"],
                "write_spans": [{"span": "not copied from input", "type": "fact"}],
                "ignore_spans": ["also not copied"],
            },
            ensure_ascii=True,
            separators=(",", ":"),
        )
    raise ValueError(f"unknown interface: {interface}")


def format_interface_report(
    *,
    cases_path: Path,
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
    top_k: int,
    prediction_path: Path | None = None,
) -> str:
    summary = summarize_cases(cases)
    is_external = prediction_path is not None
    lines = [
        "# v0.4 A/B/C Interface Pilot Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "Status: P5 external prediction evaluation" if is_external else "Status: P5 deterministic harness smoke test",
        "",
        "## Scope",
        "",
        (
            "This report evaluates an external prediction JSONL file that already contains raw outputs. The runner only loads and scores those rows; it does not call models, train, retrieve, write memories, or make v0.5 locked-gold claims."
            if is_external
            else "This report exercises the A/B/C evaluation harness on pilot data using deterministic baselines only. It does not contain real model outputs, model calls, training, retrieval, writing, or v0.5 locked-gold claims."
        ),
        "",
        "Interfaces:",
        "",
        "- A: Legacy Span JSON (`read_hints`, `write_spans`, `ignore_spans`).",
        "- B: Unit JSON (`read`, `store`, `skip`).",
        "- C: Unit DSL (`READ`, `STORE`, `SKIP`).",
        "",
        "## Dataset",
        "",
        f"- Cases: {summary['case_count']}",
        f"- Candidate memories: {summary['candidate_memory_count']}",
        f"- Current units: {summary['current_unit_count']}",
        f"- Gold READ IDs: {summary['gold_read_count']}",
        f"- Gold STORE units: {summary['gold_store_count']}",
        f"- Gold SKIP units: {summary['gold_skip_count']}",
        f"- Source: `{cases_path}`",
        *( [f"- Predictions: `{prediction_path}`"] if prediction_path else [] ),
        "",
        "Gold output shapes:",
        "",
        _counter_table(summary["gold_shapes"], "Shape"),
        "",
        "STORE target distribution:",
        "",
        _counter_table(summary["store_targets"], "Target"),
        "",
        "Tag distribution:",
        "",
        _counter_table(summary["tags"], "Tag"),
        "",
        "## Systems",
        "",
        *(
            [f"- `{system}` from `{prediction_path}`." for system in sorted({result["system"] for result in results})]
            if is_external
            else [
                "- `gold`: gold-as-prediction smoke test.",
                "- `empty`: no READ, no STORE, SKIP all current units.",
                f"- `top{top_k}_read`: read the first {top_k} candidate memory/memories, STORE none, SKIP all units.",
                "- `heuristic`: deterministic lexical read/store/skip heuristic.",
                "- `invalid_mock`: intentionally invalid raw output for parser/schema smoke testing.",
            ]
        ),
        "",
        "## Structural Metrics",
        "",
        "| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        structural = result["structural"]
        lines.append(
            "| {interface} | {system} | {parse_success} | {invalid_memory} | {invalid_unit} | {invalid_target} | {span_error} | {avg_chars} | {repair} |".format(
                interface=result["interface"],
                system=result["system"],
                parse_success=_pct(structural["parse_success"]["rate"]),
                invalid_memory=_pct(structural["invalid_memory_id_rate"]["rate"]),
                invalid_unit=_pct(structural["invalid_unit_id_rate"]["rate"]),
                invalid_target=_pct(structural["invalid_target_rate"]["rate"]),
                span_error=_pct(structural["span_copying_error_rate"]["rate"]),
                avg_chars=structural["output_length"]["avg_chars"],
                repair=structural["human_repair_cost"]["avg"],
            )
        )

    lines.extend(
        [
            "",
            "## Semantic Metrics",
            "",
            "| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in results:
        semantic = result["semantic"]
        lines.append(
            "| {interface} | {system} | {exact} | {read_f1} | {store_f1} | {target_acc} | {skip_f1} | {false_store} | {irrelevant_read} | {sensitive_store} |".format(
                interface=result["interface"],
                system=result["system"],
                exact=_pct(semantic["exact_target_match"]["rate"]),
                read_f1=_fmt(semantic["read"]["f1"]),
                store_f1=_fmt(semantic["store_unit"]["f1"]),
                target_acc=_pct(semantic["store_target_accuracy"]["accuracy"]),
                skip_f1=_fmt(semantic["skip"]["f1"]),
                false_store=_pct(semantic["false_store_rate"]["rate"]),
                irrelevant_read=_pct(semantic["irrelevant_read_rate"]["rate"]),
                sensitive_store=_pct(semantic["sensitive_store_rate"]["rate"]),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.",
            "- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.",
            "- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.",
            "- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.",
            "- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.",
            "",
            "## Recommendation",
            "",
            "The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def format_error_analysis(
    *,
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
    top_k: int,
    prediction_path: Path | None = None,
) -> str:
    is_external = prediction_path is not None
    by_key = {(result["interface"], result["system"]): result for result in results}
    heuristic = by_key.get((INTERFACE_UNIT_DSL, "heuristic"))
    topk = by_key.get((INTERFACE_UNIT_DSL, f"top{top_k}_read"))
    empty = by_key.get((INTERFACE_UNIT_DSL, "empty"))
    invalid = by_key.get((INTERFACE_UNIT_DSL, "invalid_mock"))

    lines = [
        "# v0.4 P5 Error Analysis",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "Status: P5 external prediction smoke analysis" if is_external else "Status: deterministic harness smoke analysis, not model error analysis",
        "",
        "## Summary",
        "",
        (
            f"This report analyzes raw outputs loaded from `{prediction_path}`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion."
            if is_external
            else "The current errors come from deterministic baselines and intentionally invalid mocks. They are useful for checking metric behavior but should not be interpreted as LLM failure rates."
        ),
        "",
        "## Interface/System Overview",
        "",
        _result_summary_table(results),
        "",
    ]

    if empty:
        semantic = empty["semantic"]
        lines.extend(
            [
                "## Empty Baseline",
                "",
                f"- READ recall: {_fmt(semantic['read']['recall'])}.",
                f"- STORE unit recall: {_fmt(semantic['store_unit']['recall'])}.",
                f"- SKIP F1: {_fmt(semantic['skip']['f1'])}.",
                "- Expected behavior: it exposes the cost of never reading or storing while remaining structurally valid.",
                "",
            ]
        )

    if topk:
        semantic = topk["semantic"]
        examples = _first_details(topk, "irrelevant_read_ids", limit=5)
        lines.extend(
            [
                f"## Top-{top_k} READ Baseline",
                "",
                f"- Irrelevant read rate: {_pct(semantic['irrelevant_read_rate']['rate'])}.",
                "- Expected behavior: it improves READ recall only when the first candidate is useful and otherwise demonstrates read pollution.",
                "",
                "Example irrelevant reads:",
                "",
                *_detail_bullets(examples, "irrelevant_read_ids"),
                "",
            ]
        )

    if heuristic:
        semantic = heuristic["semantic"]
        lines.extend(
            [
                "## Heuristic Baseline",
                "",
                f"- Exact target match: {_pct(semantic['exact_target_match']['rate'])}.",
                f"- STORE target accuracy on correctly selected STORE units: {_pct(semantic['store_target_accuracy']['accuracy'])}.",
                f"- False store rate: {_pct(semantic['false_store_rate']['rate'])}.",
                f"- Sensitive store rate: {_pct(semantic['sensitive_store_rate']['rate'])}.",
                "",
                "Target confusion on correctly selected STORE units:",
                "",
                _confusion_table(heuristic["target_confusion"]),
                "",
                "Example false stores:",
                "",
                *_detail_bullets(_first_details(heuristic, "false_store_units", limit=5), "false_store_units"),
                "",
                "Example sensitive stores:",
                "",
                *_detail_bullets(_first_details(heuristic, "sensitive_store_units", limit=5), "sensitive_store_units"),
                "",
            ]
        )

    if invalid:
        examples = [
            detail
            for detail in invalid["case_details"]
            if detail["validation_errors"]
        ][:5]
        lines.extend(
            [
                "## Invalid Mock",
                "",
                f"- Parse success: {_pct(invalid['structural']['parse_success']['rate'])}.",
                "- Expected behavior: unknown memory IDs, unknown unit IDs, invalid targets, and missing assignments are counted as structural failures.",
                "",
                "Example validation errors:",
                "",
                *_error_bullets(examples),
                "",
            ]
        )

    lines.extend(
        [
            "## Validation Error Examples Across Evaluated Results",
            "",
            *_validation_error_bullets(results),
            "",
        ]
    )

    lines.extend(
        [
            "## Next Error Analysis Step",
            "",
            "After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.",
        ]
    )
    return "\n".join(lines) + "\n"


def summarize_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    gold_shapes = Counter()
    store_targets = Counter()
    tags = Counter()
    for case in cases:
        read = bool(case["gold"]["read"])
        store = bool(case["gold"]["store"])
        if read and store:
            gold_shapes["READ + STORE joint"] += 1
        elif read:
            gold_shapes["READ-only"] += 1
        elif store:
            gold_shapes["STORE/SKIP-only"] += 1
        else:
            gold_shapes["No READ and no STORE"] += 1
        for item in case["gold"]["store"]:
            store_targets[item["target"]] += 1
        tags.update(case["tags"])

    return {
        "case_count": len(cases),
        "candidate_memory_count": sum(len(case["candidate_memories"]) for case in cases),
        "current_unit_count": sum(len(case["current_units"]) for case in cases),
        "gold_read_count": sum(len(case["gold"]["read"]) for case in cases),
        "gold_store_count": sum(len(case["gold"]["store"]) for case in cases),
        "gold_skip_count": sum(len(case["gold"]["skip"]) for case in cases),
        "gold_shapes": gold_shapes,
        "store_targets": store_targets,
        "tags": tags,
    }


def display_system_name(baseline: str, *, top_k: int) -> str:
    return f"top{top_k}_read" if baseline == "topk_read" else baseline


def content_tokens(text: str) -> set[str]:
    tokens = {
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)
    }
    return {token for token in tokens if token not in STOP_WORDS}


def _canonical(
    *,
    read_ids: list[str],
    store_entries: list[dict[str, str]],
    skip_ids: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "memory_policy.v0.4",
        "read": [{"memory_id": memory_id} for memory_id in read_ids],
        "store": [
            {"target": item["target"], "unit_id": item["unit_id"]}
            for item in store_entries
        ],
        "skip": [{"unit_id": unit_id} for unit_id in skip_ids],
        "validation": {"valid": True, "errors": []},
    }


def _ordered_read_ids(canonical: dict[str, Any], case: dict[str, Any]) -> list[str]:
    predicted = {item["memory_id"] for item in canonical["read"]}
    return [
        memory["memory_id"]
        for memory in case["candidate_memories"]
        if memory["memory_id"] in predicted
    ]


def _ordered_store_entries(canonical: dict[str, Any], case: dict[str, Any]) -> list[dict[str, str]]:
    predicted = {item["unit_id"]: item["target"] for item in canonical["store"]}
    return [
        {"target": predicted[unit["unit_id"]], "unit_id": unit["unit_id"]}
        for unit in case["current_units"]
        if unit["unit_id"] in predicted
    ]


def _ordered_skip_ids(canonical: dict[str, Any], case: dict[str, Any]) -> list[str]:
    predicted = {item["unit_id"] for item in canonical["skip"]}
    return [unit["unit_id"] for unit in case["current_units"] if unit["unit_id"] in predicted]


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _fmt(value: float) -> str:
    return f"{value:.3f}"


def _counter_table(counter: Counter, label: str) -> str:
    lines = [f"| {label} | Count |", "| --- | ---: |"]
    for key, count in sorted(counter.items()):
        lines.append(f"| `{key}` | {count} |")
    return "\n".join(lines)


def _result_summary_table(results: list[dict[str, Any]]) -> str:
    lines = [
        "| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        structural = result["structural"]
        semantic = result["semantic"]
        lines.append(
            "| {interface} | {system} | {parse_success} | {exact} | {false_store} | {irrelevant_read} | {sensitive_store} |".format(
                interface=result["interface"],
                system=result["system"],
                parse_success=_pct(structural["parse_success"]["rate"]),
                exact=_pct(semantic["exact_target_match"]["rate"]),
                false_store=_pct(semantic["false_store_rate"]["rate"]),
                irrelevant_read=_pct(semantic["irrelevant_read_rate"]["rate"]),
                sensitive_store=_pct(semantic["sensitive_store_rate"]["rate"]),
            )
        )
    return "\n".join(lines)


def _confusion_table(confusion: dict[str, dict[str, int]]) -> str:
    if not confusion:
        return "No STORE target comparisons."
    targets = sorted({target for target in confusion} | {target for values in confusion.values() for target in values})
    lines = ["| Gold target | " + " | ".join(f"`{target}`" for target in targets) + " |"]
    lines.append("| --- | " + " | ".join("---:" for _target in targets) + " |")
    for gold_target in targets:
        row = [f"`{gold_target}`"]
        values = confusion.get(gold_target, {})
        row.extend(str(values.get(target, 0)) for target in targets)
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _first_details(result: dict[str, Any], field: str, *, limit: int) -> list[dict[str, Any]]:
    return [detail for detail in result["case_details"] if detail[field]][:limit]


def _detail_bullets(details: list[dict[str, Any]], field: str) -> list[str]:
    if not details:
        return ["- None in this smoke run."]
    return [f"- `{detail['case_id']}`: {', '.join(detail[field])}" for detail in details]


def _error_bullets(details: list[dict[str, Any]]) -> list[str]:
    if not details:
        return ["- None."]
    return [
        f"- `{detail['case_id']}`: {detail['validation_errors'][0]}"
        for detail in details
    ]


def _validation_error_bullets(results: list[dict[str, Any]], limit: int = 8) -> list[str]:
    bullets: list[str] = []
    for result in results:
        for detail in result["case_details"]:
            if not detail["validation_errors"]:
                continue
            bullets.append(
                "- `{case_id}` ({interface}/{system}): {error}".format(
                    case_id=detail["case_id"],
                    interface=result["interface"],
                    system=result["system"],
                    error=detail["validation_errors"][0],
                )
            )
            if len(bullets) >= limit:
                return bullets
    return bullets or ["- None in this run."]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("data/v04/pilot_cases.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("reports/v04/interface_pilot_report.md"))
    parser.add_argument("--error-report", type=Path, default=Path("reports/v04/error_analysis.md"))
    parser.add_argument("--interfaces", nargs="+", choices=INTERFACES, default=list(INTERFACES))
    parser.add_argument("--baselines", nargs="+", choices=BASELINES, default=list(BASELINES))
    parser.add_argument(
        "--predictions",
        type=Path,
        help="Evaluate an external PREDICTION_FORMAT JSONL file instead of deterministic baselines.",
    )
    parser.add_argument("--top-k", type=int, default=1)
    args = parser.parse_args()

    validation = validate_jsonl_file(args.cases)
    if not validation["valid"]:
        for error in validation["errors"]:
            print(error, file=sys.stderr)
        return 1

    cases = load_cases(args.cases)
    if args.predictions:
        try:
            prediction_rows = load_prediction_jsonl(args.predictions)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        results = run_prediction_file_evaluation(cases, prediction_rows)
    else:
        results = run_evaluation(
            cases,
            interfaces=args.interfaces,
            baselines=args.baselines,
            top_k=args.top_k,
        )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.error_report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        format_interface_report(
            cases_path=args.cases,
            cases=cases,
            results=results,
            top_k=args.top_k,
            prediction_path=args.predictions,
        ),
        encoding="utf-8",
    )
    args.error_report.write_text(
        format_error_analysis(
            cases=cases,
            results=results,
            top_k=args.top_k,
            prediction_path=args.predictions,
        ),
        encoding="utf-8",
    )
    if args.predictions:
        print(
            f"Evaluated {len(cases)} cases from {args.predictions} across {len(results)} interface/system groups."
        )
    else:
        print(
            f"Evaluated {len(cases)} cases across {len(args.interfaces)} interfaces and {len(args.baselines)} systems."
        )
    print(f"Wrote {args.report}")
    print(f"Wrote {args.error_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

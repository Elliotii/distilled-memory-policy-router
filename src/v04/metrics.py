"""Metrics and prediction adapters for the v0.4 interface pilot.

This module is intentionally local to v0.4. It evaluates three raw output
interfaces against the same unit-based gold labels:

- legacy_span_json: JSON with read_hints, write_spans, ignore_spans
- unit_json: JSON with read, store, skip
- unit_dsl: strict READ / STORE / SKIP DSL

It does not call models, repair semantic mistakes, or mutate gold labels.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from src.v04.parser import LEGAL_TARGETS, SCHEMA_VERSION, parse_policy_dsl


INTERFACE_LEGACY_SPAN_JSON = "legacy_span_json"
INTERFACE_UNIT_JSON = "unit_json"
INTERFACE_UNIT_DSL = "unit_dsl"
INTERFACES = (
    INTERFACE_LEGACY_SPAN_JSON,
    INTERFACE_UNIT_JSON,
    INTERFACE_UNIT_DSL,
)


@dataclass
class PredictionDiagnostics:
    interface: str
    raw_output: str
    raw_parse_success: bool
    parse_success: bool
    validation_errors: list[str] = field(default_factory=list)
    predicted_memory_refs: int = 0
    invalid_memory_refs: int = 0
    predicted_unit_refs: int = 0
    invalid_unit_refs: int = 0
    predicted_store_refs: int = 0
    invalid_target_refs: int = 0
    predicted_span_refs: int = 0
    invalid_span_refs: int = 0
    schema_error_count: int = 0

    @property
    def output_chars(self) -> int:
        return len(self.raw_output)

    @property
    def output_lines(self) -> int:
        return len([line for line in self.raw_output.splitlines() if line.strip()])

    @property
    def output_tokens(self) -> int:
        return len(re.findall(r"\S+", self.raw_output))


@dataclass
class ParsedPrediction:
    canonical: dict[str, Any]
    diagnostics: PredictionDiagnostics


@dataclass
class ScoreCounts:
    cases: int = 0
    exact_target_matches: int = 0

    read_tp: int = 0
    read_fp: int = 0
    read_fn: int = 0

    store_tp: int = 0
    store_fp: int = 0
    store_fn: int = 0

    skip_tp: int = 0
    skip_fp: int = 0
    skip_fn: int = 0

    store_target_correct: int = 0
    store_target_compared: int = 0
    false_store_count: int = 0
    predicted_store_count: int = 0
    irrelevant_read_count: int = 0
    predicted_read_count: int = 0
    sensitive_store_count: int = 0
    sensitive_store_possible: int = 0

    target_confusion: dict[str, Counter[str]] = field(
        default_factory=lambda: defaultdict(Counter)
    )


def rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def prf(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = rate(tp, tp + fp)
    recall = rate(tp, tp + fn)
    f1 = (
        round(2 * precision * recall / (precision + recall), 6)
        if precision + recall
        else 0.0
    )
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def gold_canonical(case: dict[str, Any]) -> dict[str, Any]:
    gold = case["gold"]
    return {
        "schema_version": SCHEMA_VERSION,
        "read": [{"memory_id": memory_id} for memory_id in gold["read"]],
        "store": [
            {"target": item["target"], "unit_id": item["unit_id"]}
            for item in gold["store"]
        ],
        "skip": [{"unit_id": unit_id} for unit_id in gold["skip"]],
        "validation": {"valid": True, "errors": []},
    }


def parse_prediction(raw_output: str, interface: str, case: dict[str, Any]) -> ParsedPrediction:
    if interface == INTERFACE_UNIT_DSL:
        return _parse_unit_dsl(raw_output, case)
    if interface == INTERFACE_UNIT_JSON:
        return _parse_unit_json(raw_output, case)
    if interface == INTERFACE_LEGACY_SPAN_JSON:
        return _parse_legacy_span_json(raw_output, case)
    raise ValueError(f"unknown interface: {interface}")


def evaluate_prediction_rows(
    cases: list[dict[str, Any]],
    prediction_rows: list[dict[str, Any]],
    *,
    interface: str,
    system_name: str,
) -> dict[str, Any]:
    predictions_by_id: dict[str, dict[str, Any]] = {}
    duplicate_case_ids: list[str] = []
    for row in prediction_rows:
        case_id = row.get("case_id")
        if not isinstance(case_id, str):
            continue
        if case_id in predictions_by_id:
            duplicate_case_ids.append(case_id)
        predictions_by_id[case_id] = row

    scores = ScoreCounts()
    structural = Counter()
    repair_costs = Counter()
    output_chars: list[int] = []
    output_lines: list[int] = []
    output_tokens: list[int] = []
    case_details: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["case_id"]
        row = predictions_by_id.get(case_id)
        raw_output = row.get("raw_output", "") if row else ""
        parsed = parse_prediction(raw_output, interface, case)
        diag = parsed.diagnostics
        gold = gold_canonical(case)
        pred = parsed.canonical

        output_chars.append(diag.output_chars)
        output_lines.append(diag.output_lines)
        output_tokens.append(diag.output_tokens)
        structural["cases"] += 1
        structural["raw_parse_success"] += int(diag.raw_parse_success)
        structural["parse_success"] += int(diag.parse_success)
        structural["predicted_memory_refs"] += diag.predicted_memory_refs
        structural["invalid_memory_refs"] += diag.invalid_memory_refs
        structural["predicted_unit_refs"] += diag.predicted_unit_refs
        structural["invalid_unit_refs"] += diag.invalid_unit_refs
        structural["predicted_store_refs"] += diag.predicted_store_refs
        structural["invalid_target_refs"] += diag.invalid_target_refs
        structural["predicted_span_refs"] += diag.predicted_span_refs
        structural["invalid_span_refs"] += diag.invalid_span_refs
        structural["schema_error_count"] += diag.schema_error_count
        structural["validation_error_cases"] += int(bool(diag.validation_errors))

        detail = _score_one_case(scores, case, gold, pred, diag)
        repair_costs[str(detail["human_repair_cost"])] += 1
        case_details.append(detail)

    return {
        "interface": interface,
        "system": system_name,
        "cases": len(cases),
        "structural": _summarize_structural(
            structural,
            repair_costs,
            output_chars,
            output_lines,
            output_tokens,
            duplicate_case_ids,
        ),
        "semantic": _summarize_semantic(scores),
        "target_confusion": {
            gold_target: dict(predicted)
            for gold_target, predicted in sorted(scores.target_confusion.items())
        },
        "case_details": case_details,
    }


def _parse_unit_dsl(raw_output: str, case: dict[str, Any]) -> ParsedPrediction:
    candidate_ids = _candidate_ids(case)
    unit_ids = _unit_ids(case)
    stats = _collect_dsl_reference_stats(raw_output, candidate_ids, unit_ids)
    parsed = parse_policy_dsl(raw_output, candidate_ids, unit_ids, LEGAL_TARGETS)
    errors = parsed["validation"]["errors"]
    diagnostics = PredictionDiagnostics(
        interface=INTERFACE_UNIT_DSL,
        raw_output=raw_output,
        raw_parse_success=_dsl_raw_parse_success(errors),
        parse_success=parsed["validation"]["valid"],
        validation_errors=list(errors),
        predicted_memory_refs=stats["predicted_memory_refs"],
        invalid_memory_refs=stats["invalid_memory_refs"],
        predicted_unit_refs=stats["predicted_unit_refs"],
        invalid_unit_refs=stats["invalid_unit_refs"],
        predicted_store_refs=stats["predicted_store_refs"],
        invalid_target_refs=stats["invalid_target_refs"],
        schema_error_count=len(errors),
    )
    return ParsedPrediction(parsed, diagnostics)


def _dsl_raw_parse_success(errors: list[str]) -> bool:
    syntax_error_markers = (
        "empty output",
        "malformed",
        "unknown line type",
        "duplicate READ line",
        "duplicate SKIP line",
        "duplicate STORE NONE",
        "STORE NONE cannot be combined",
    )
    return not any(
        any(marker in error for marker in syntax_error_markers)
        for error in errors
    )


def _parse_unit_json(raw_output: str, case: dict[str, Any]) -> ParsedPrediction:
    candidate_id_set = set(_candidate_ids(case))
    unit_ids = _unit_ids(case)
    unit_id_set = set(unit_ids)
    errors: list[str] = []
    stats = Counter()

    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {exc.msg}")
        return _invalid_prediction(INTERFACE_UNIT_JSON, raw_output, False, errors)

    if not isinstance(payload, dict):
        errors.append("unit_json output must be an object")
        return _invalid_prediction(INTERFACE_UNIT_JSON, raw_output, True, errors)

    allowed_keys = {"read", "store", "skip"}
    extra_keys = sorted(set(payload) - allowed_keys)
    missing_keys = sorted(allowed_keys - set(payload))
    if extra_keys:
        errors.append(f"unexpected keys: {extra_keys}")
    for key in missing_keys:
        errors.append(f"missing key: {key}")

    read_entries = _parse_read_list(payload.get("read"), "read", candidate_id_set, errors, stats)
    store_entries = _parse_unit_store_list(payload.get("store"), unit_id_set, errors, stats)
    skip_entries = _parse_unit_skip_list(payload.get("skip"), unit_id_set, errors, stats)
    _validate_unit_assignment(unit_ids, store_entries, skip_entries, errors)

    canonical = _canonical_or_empty(read_entries, store_entries, skip_entries, errors)
    diagnostics = PredictionDiagnostics(
        interface=INTERFACE_UNIT_JSON,
        raw_output=raw_output,
        raw_parse_success=True,
        parse_success=canonical["validation"]["valid"],
        validation_errors=list(errors),
        predicted_memory_refs=stats["predicted_memory_refs"],
        invalid_memory_refs=stats["invalid_memory_refs"],
        predicted_unit_refs=stats["predicted_unit_refs"],
        invalid_unit_refs=stats["invalid_unit_refs"],
        predicted_store_refs=stats["predicted_store_refs"],
        invalid_target_refs=stats["invalid_target_refs"],
        schema_error_count=len(errors),
    )
    return ParsedPrediction(canonical, diagnostics)


def _parse_legacy_span_json(raw_output: str, case: dict[str, Any]) -> ParsedPrediction:
    candidate_id_set = set(_candidate_ids(case))
    unit_ids = _unit_ids(case)
    span_to_units = _span_to_units(case)
    errors: list[str] = []
    stats = Counter()

    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {exc.msg}")
        return _invalid_prediction(INTERFACE_LEGACY_SPAN_JSON, raw_output, False, errors)

    if not isinstance(payload, dict):
        errors.append("legacy_span_json output must be an object")
        return _invalid_prediction(INTERFACE_LEGACY_SPAN_JSON, raw_output, True, errors)

    allowed_keys = {"read_hints", "write_spans", "ignore_spans"}
    extra_keys = sorted(set(payload) - allowed_keys)
    missing_keys = sorted(allowed_keys - set(payload))
    if extra_keys:
        errors.append(f"unexpected keys: {extra_keys}")
    for key in missing_keys:
        errors.append(f"missing key: {key}")

    read_entries = _parse_read_list(
        payload.get("read_hints"),
        "read_hints",
        candidate_id_set,
        errors,
        stats,
    )
    store_entries = _parse_legacy_write_spans(payload.get("write_spans"), span_to_units, errors, stats)
    skip_entries = _parse_legacy_ignore_spans(payload.get("ignore_spans"), span_to_units, errors, stats)
    _validate_unit_assignment(unit_ids, store_entries, skip_entries, errors)

    canonical = _canonical_or_empty(read_entries, store_entries, skip_entries, errors)
    diagnostics = PredictionDiagnostics(
        interface=INTERFACE_LEGACY_SPAN_JSON,
        raw_output=raw_output,
        raw_parse_success=True,
        parse_success=canonical["validation"]["valid"],
        validation_errors=list(errors),
        predicted_memory_refs=stats["predicted_memory_refs"],
        invalid_memory_refs=stats["invalid_memory_refs"],
        predicted_unit_refs=stats["predicted_unit_refs"],
        invalid_unit_refs=stats["invalid_unit_refs"],
        predicted_store_refs=stats["predicted_store_refs"],
        invalid_target_refs=stats["invalid_target_refs"],
        predicted_span_refs=stats["predicted_span_refs"],
        invalid_span_refs=stats["invalid_span_refs"],
        schema_error_count=len(errors),
    )
    return ParsedPrediction(canonical, diagnostics)


def _parse_read_list(
    value: Any,
    field_name: str,
    candidate_id_set: set[str],
    errors: list[str],
    stats: Counter,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append(f"{field_name} must be a list")
        return []

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, memory_id in enumerate(value):
        if not isinstance(memory_id, str) or not memory_id:
            errors.append(f"{field_name}[{index}] must be a non-empty string")
            continue
        stats["predicted_memory_refs"] += 1
        if memory_id not in candidate_id_set:
            stats["invalid_memory_refs"] += 1
            errors.append(f"unknown memory_id: {memory_id}")
            continue
        if memory_id not in seen:
            seen.add(memory_id)
            entries.append({"memory_id": memory_id})
    return entries


def _parse_unit_store_list(
    value: Any,
    unit_id_set: set[str],
    errors: list[str],
    stats: Counter,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append("store must be a list")
        return []

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"store[{index}] must be an object")
            continue
        target = item.get("target")
        unit_id = item.get("unit_id")
        stats["predicted_store_refs"] += 1
        if target not in LEGAL_TARGETS:
            stats["invalid_target_refs"] += 1
            errors.append(f"invalid target: {target}")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append(f"store[{index}].unit_id must be a non-empty string")
            continue
        stats["predicted_unit_refs"] += 1
        if unit_id not in unit_id_set:
            stats["invalid_unit_refs"] += 1
            errors.append(f"unknown unit_id in STORE: {unit_id}")
            continue
        if unit_id in seen:
            errors.append(f"duplicate STORE unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        entries.append({"target": target, "unit_id": unit_id})
    return entries


def _parse_unit_skip_list(
    value: Any,
    unit_id_set: set[str],
    errors: list[str],
    stats: Counter,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append("skip must be a list")
        return []

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, unit_id in enumerate(value):
        if not isinstance(unit_id, str) or not unit_id:
            errors.append(f"skip[{index}] must be a non-empty string")
            continue
        stats["predicted_unit_refs"] += 1
        if unit_id not in unit_id_set:
            stats["invalid_unit_refs"] += 1
            errors.append(f"unknown unit_id in SKIP: {unit_id}")
            continue
        if unit_id in seen:
            errors.append(f"duplicate SKIP unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        entries.append({"unit_id": unit_id})
    return entries


def _parse_legacy_write_spans(
    value: Any,
    span_to_units: dict[str, list[str]],
    errors: list[str],
    stats: Counter,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append("write_spans must be a list")
        return []

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"write_spans[{index}] must be an object")
            continue
        span = item.get("span")
        target = item.get("type")
        stats["predicted_store_refs"] += 1
        if target not in LEGAL_TARGETS:
            stats["invalid_target_refs"] += 1
            errors.append(f"invalid type/target: {target}")
        if not isinstance(span, str) or not span:
            errors.append(f"write_spans[{index}].span must be a non-empty string")
            continue
        stats["predicted_span_refs"] += 1
        stats["predicted_unit_refs"] += 1
        unit_id = _unit_for_span(span, span_to_units)
        if unit_id is None:
            stats["invalid_span_refs"] += 1
            stats["invalid_unit_refs"] += 1
            errors.append(f"write_spans[{index}].span does not exactly match one current unit")
            continue
        if unit_id in seen:
            errors.append(f"duplicate STORE unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        entries.append({"target": target, "unit_id": unit_id})
    return entries


def _parse_legacy_ignore_spans(
    value: Any,
    span_to_units: dict[str, list[str]],
    errors: list[str],
    stats: Counter,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append("ignore_spans must be a list")
        return []

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, span in enumerate(value):
        if not isinstance(span, str) or not span:
            errors.append(f"ignore_spans[{index}] must be a non-empty string")
            continue
        stats["predicted_span_refs"] += 1
        stats["predicted_unit_refs"] += 1
        unit_id = _unit_for_span(span, span_to_units)
        if unit_id is None:
            stats["invalid_span_refs"] += 1
            stats["invalid_unit_refs"] += 1
            errors.append(f"ignore_spans[{index}] does not exactly match one current unit")
            continue
        if unit_id in seen:
            errors.append(f"duplicate SKIP unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        entries.append({"unit_id": unit_id})
    return entries


def _validate_unit_assignment(
    unit_ids: list[str],
    store_entries: list[dict[str, str]],
    skip_entries: list[dict[str, str]],
    errors: list[str],
) -> None:
    store_ids = [entry["unit_id"] for entry in store_entries]
    skip_ids = [entry["unit_id"] for entry in skip_entries]
    store_set = set(store_ids)
    skip_set = set(skip_ids)
    for unit_id in store_ids:
        if store_ids.count(unit_id) > 1:
            errors.append(f"duplicate STORE unit_id: {unit_id}")
    for unit_id in skip_ids:
        if skip_ids.count(unit_id) > 1:
            errors.append(f"duplicate SKIP unit_id: {unit_id}")
    for unit_id in unit_ids:
        in_store = unit_id in store_set
        in_skip = unit_id in skip_set
        if in_store and in_skip:
            errors.append(f"unit appears in both STORE and SKIP: {unit_id}")
        elif not in_store and not in_skip:
            errors.append(f"missing unit assignment: {unit_id}")


def _collect_dsl_reference_stats(
    raw_output: str,
    candidate_ids: list[str],
    unit_ids: list[str],
) -> Counter:
    candidate_id_set = set(candidate_ids)
    unit_id_set = set(unit_ids)
    stats = Counter()
    for raw_line in raw_output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        keyword, _, rest = line.partition(" ")
        rest = rest.strip()
        if keyword == "READ" and rest and rest != "NONE":
            for memory_id in _split_id_list(rest):
                stats["predicted_memory_refs"] += 1
                if memory_id not in candidate_id_set:
                    stats["invalid_memory_refs"] += 1
        elif keyword == "STORE" and rest and rest != "NONE":
            parts = rest.split()
            if len(parts) == 2:
                target, unit_id = parts
                stats["predicted_store_refs"] += 1
                stats["predicted_unit_refs"] += 1
                if target not in LEGAL_TARGETS:
                    stats["invalid_target_refs"] += 1
                if unit_id not in unit_id_set:
                    stats["invalid_unit_refs"] += 1
        elif keyword == "SKIP" and rest and rest != "NONE":
            for unit_id in _split_id_list(rest):
                stats["predicted_unit_refs"] += 1
                if unit_id not in unit_id_set:
                    stats["invalid_unit_refs"] += 1
    return stats


def _split_id_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _invalid_prediction(
    interface: str,
    raw_output: str,
    raw_parse_success: bool,
    errors: list[str],
) -> ParsedPrediction:
    diagnostics = PredictionDiagnostics(
        interface=interface,
        raw_output=raw_output,
        raw_parse_success=raw_parse_success,
        parse_success=False,
        validation_errors=list(errors),
        schema_error_count=len(errors),
    )
    return ParsedPrediction(_empty_canonical(errors), diagnostics)


def _canonical_or_empty(
    read_entries: list[dict[str, str]],
    store_entries: list[dict[str, str]],
    skip_entries: list[dict[str, str]],
    errors: list[str],
) -> dict[str, Any]:
    if errors:
        return _empty_canonical(errors)
    return {
        "schema_version": SCHEMA_VERSION,
        "read": read_entries,
        "store": store_entries,
        "skip": skip_entries,
        "validation": {"valid": True, "errors": []},
    }


def _empty_canonical(errors: list[str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "read": [],
        "store": [],
        "skip": [],
        "validation": {"valid": False, "errors": list(errors)},
    }


def _score_one_case(
    scores: ScoreCounts,
    case: dict[str, Any],
    gold: dict[str, Any],
    pred: dict[str, Any],
    diag: PredictionDiagnostics,
) -> dict[str, Any]:
    scores.cases += 1
    gold_read = {item["memory_id"] for item in gold["read"]}
    pred_read = {item["memory_id"] for item in pred["read"]}
    gold_store = {item["unit_id"]: item["target"] for item in gold["store"]}
    pred_store = {item["unit_id"]: item["target"] for item in pred["store"]}
    gold_skip = {item["unit_id"] for item in gold["skip"]}
    pred_skip = {item["unit_id"] for item in pred["skip"]}
    sensitive_units = _sensitive_unit_ids(case)

    read_tp = len(gold_read & pred_read)
    read_fp = len(pred_read - gold_read)
    read_fn = len(gold_read - pred_read)
    store_tp = len(set(gold_store) & set(pred_store))
    store_fp = len(set(pred_store) - set(gold_store))
    store_fn = len(set(gold_store) - set(pred_store))
    skip_tp = len(gold_skip & pred_skip)
    skip_fp = len(pred_skip - gold_skip)
    skip_fn = len(gold_skip - pred_skip)

    scores.read_tp += read_tp
    scores.read_fp += read_fp
    scores.read_fn += read_fn
    scores.store_tp += store_tp
    scores.store_fp += store_fp
    scores.store_fn += store_fn
    scores.skip_tp += skip_tp
    scores.skip_fp += skip_fp
    scores.skip_fn += skip_fn

    correctly_predicted_store_units = set(gold_store) & set(pred_store)
    for unit_id in correctly_predicted_store_units:
        gold_target = gold_store[unit_id]
        predicted_target = pred_store[unit_id]
        scores.store_target_compared += 1
        scores.target_confusion[gold_target][predicted_target] += 1
        if gold_target == predicted_target:
            scores.store_target_correct += 1

    scores.false_store_count += len(set(pred_store) & gold_skip)
    scores.predicted_store_count += len(pred_store)
    scores.irrelevant_read_count += read_fp
    scores.predicted_read_count += len(pred_read)
    scores.sensitive_store_count += len(set(pred_store) & sensitive_units)
    scores.sensitive_store_possible += len(sensitive_units)

    exact_match = (
        gold_read == pred_read
        and gold_store == pred_store
        and gold_skip == pred_skip
        and diag.parse_success
    )
    scores.exact_target_matches += int(exact_match)
    repair_cost = _repair_cost(exact_match, diag)
    return {
        "case_id": case["case_id"],
        "parse_success": diag.parse_success,
        "validation_errors": list(diag.validation_errors),
        "exact_target_match": exact_match,
        "read_fp": read_fp,
        "read_fn": read_fn,
        "store_fp": store_fp,
        "store_fn": store_fn,
        "skip_fp": skip_fp,
        "skip_fn": skip_fn,
        "false_store_units": sorted(set(pred_store) & gold_skip),
        "irrelevant_read_ids": sorted(pred_read - gold_read),
        "sensitive_store_units": sorted(set(pred_store) & sensitive_units),
        "human_repair_cost": repair_cost,
    }


def _repair_cost(exact_match: bool, diag: PredictionDiagnostics) -> int:
    if exact_match:
        return 0
    if not diag.raw_parse_success:
        return 1
    if (
        diag.validation_errors
        or diag.invalid_memory_refs
        or diag.invalid_unit_refs
        or diag.invalid_target_refs
        or diag.invalid_span_refs
    ):
        return 2
    return 3


def _summarize_structural(
    structural: Counter,
    repair_costs: Counter,
    output_chars: list[int],
    output_lines: list[int],
    output_tokens: list[int],
    duplicate_case_ids: list[str],
) -> dict[str, Any]:
    cases = structural["cases"]
    total_repair = sum(int(cost) * count for cost, count in repair_costs.items())
    return {
        "parse_success": {
            "count": structural["parse_success"],
            "rate": rate(structural["parse_success"], cases),
        },
        "raw_parse_success": {
            "count": structural["raw_parse_success"],
            "rate": rate(structural["raw_parse_success"], cases),
        },
        "invalid_memory_id_rate": {
            "invalid": structural["invalid_memory_refs"],
            "predicted": structural["predicted_memory_refs"],
            "rate": rate(structural["invalid_memory_refs"], structural["predicted_memory_refs"]),
        },
        "invalid_unit_id_rate": {
            "invalid": structural["invalid_unit_refs"],
            "predicted": structural["predicted_unit_refs"],
            "rate": rate(structural["invalid_unit_refs"], structural["predicted_unit_refs"]),
        },
        "invalid_target_rate": {
            "invalid": structural["invalid_target_refs"],
            "predicted": structural["predicted_store_refs"],
            "rate": rate(structural["invalid_target_refs"], structural["predicted_store_refs"]),
        },
        "span_copying_error_rate": {
            "invalid": structural["invalid_span_refs"],
            "predicted": structural["predicted_span_refs"],
            "rate": rate(structural["invalid_span_refs"], structural["predicted_span_refs"]),
        },
        "validation_error_cases": structural["validation_error_cases"],
        "schema_error_count": structural["schema_error_count"],
        "duplicate_prediction_case_ids": sorted(set(duplicate_case_ids)),
        "output_length": {
            "avg_chars": _avg(output_chars),
            "max_chars": max(output_chars) if output_chars else 0,
            "avg_lines": _avg(output_lines),
            "max_lines": max(output_lines) if output_lines else 0,
            "avg_approx_tokens": _avg(output_tokens),
            "max_approx_tokens": max(output_tokens) if output_tokens else 0,
        },
        "human_repair_cost": {
            "avg": rate(total_repair, cases),
            "counts": dict(sorted(repair_costs.items())),
        },
    }


def _summarize_semantic(scores: ScoreCounts) -> dict[str, Any]:
    return {
        "exact_target_match": {
            "count": scores.exact_target_matches,
            "rate": rate(scores.exact_target_matches, scores.cases),
        },
        "read": prf(scores.read_tp, scores.read_fp, scores.read_fn),
        "store_unit": prf(scores.store_tp, scores.store_fp, scores.store_fn),
        "store_target_accuracy": {
            "correct": scores.store_target_correct,
            "compared": scores.store_target_compared,
            "accuracy": rate(scores.store_target_correct, scores.store_target_compared),
        },
        "skip": prf(scores.skip_tp, scores.skip_fp, scores.skip_fn),
        "false_store_rate": {
            "false_store": scores.false_store_count,
            "predicted_store": scores.predicted_store_count,
            "rate": rate(scores.false_store_count, scores.predicted_store_count),
        },
        "irrelevant_read_rate": {
            "irrelevant_read": scores.irrelevant_read_count,
            "predicted_read": scores.predicted_read_count,
            "rate": rate(scores.irrelevant_read_count, scores.predicted_read_count),
        },
        "sensitive_store_rate": {
            "sensitive_store": scores.sensitive_store_count,
            "sensitive_units": scores.sensitive_store_possible,
            "rate": rate(scores.sensitive_store_count, scores.sensitive_store_possible),
        },
    }


def _avg(values: list[int]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def _candidate_ids(case: dict[str, Any]) -> list[str]:
    return [item["memory_id"] for item in case.get("candidate_memories", [])]


def _unit_ids(case: dict[str, Any]) -> list[str]:
    return [item["unit_id"] for item in case.get("current_units", [])]


def _span_to_units(case: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for unit in case.get("current_units", []):
        result[unit["text"]].append(unit["unit_id"])
    return result


def _unit_for_span(span: str, span_to_units: dict[str, list[str]]) -> str | None:
    unit_ids = span_to_units.get(span)
    if not unit_ids or len(unit_ids) != 1:
        return None
    return unit_ids[0]


def _sensitive_unit_ids(case: dict[str, Any]) -> set[str]:
    if "sensitive_boundary" not in case.get("tags", []):
        return set()
    markers = (
        "api key",
        "private key",
        "recovery code",
        "test account password",
        "my password",
        "phone number",
        "home address",
        "backup email",
        "do_not_store",
    )
    result: set[str] = set()
    for unit in case.get("current_units", []):
        text = unit.get("text", "").lower()
        if any(marker in text for marker in markers):
            result.add(unit["unit_id"])
    return result

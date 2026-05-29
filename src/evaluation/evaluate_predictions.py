"""Evaluate parsed router predictions against dev or gold labels."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.validate_predictions import (
    format_report as format_validation_report,
    load_gold_cases,
    load_jsonl,
    validate_predictions,
)
from src.evaluation.span_normalizer import (
    DEFAULT_MARKERS_PATH,
    NormalizerConfig,
    default_marker_config,
    greedy_span_matches,
)


EMPTY_TARGET = {"read_hints": [], "write_spans": [], "ignore_spans": []}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class ScoreCounts:
    total_cases: int = 0
    exact_target_matches: int = 0
    parse_errors: int = 0

    read_tp: int = 0
    read_fp: int = 0
    read_fn: int = 0

    write_span_tp: int = 0
    write_span_fp: int = 0
    write_span_fn: int = 0

    write_typed_tp: int = 0
    write_typed_fp: int = 0
    write_typed_fn: int = 0

    ignore_tp: int = 0
    ignore_fp: int = 0
    ignore_fn: int = 0

    write_type_correct: int = 0
    write_type_compared: int = 0

    @property
    def false_writes(self) -> int:
        return self.write_span_fp

    @property
    def missed_writes(self) -> int:
        return self.write_span_fn

    @property
    def irrelevant_reads(self) -> int:
        return self.read_fp

    @property
    def missed_reads(self) -> int:
        return self.read_fn

    @property
    def false_ignores(self) -> int:
        return self.ignore_fp

    @property
    def missed_ignores(self) -> int:
        return self.ignore_fn

    def update_set_counts(self, prefix: str, gold: set[Any], pred: set[Any]) -> None:
        tp = len(gold & pred)
        fp = len(pred - gold)
        fn = len(gold - pred)
        setattr(self, f"{prefix}_tp", getattr(self, f"{prefix}_tp") + tp)
        setattr(self, f"{prefix}_fp", getattr(self, f"{prefix}_fp") + fp)
        setattr(self, f"{prefix}_fn", getattr(self, f"{prefix}_fn") + fn)


def prf(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
    }


def target_sets(target: dict[str, Any]) -> dict[str, set[Any]]:
    write_spans = target.get("write_spans", [])
    return {
        "read": set(target.get("read_hints", [])),
        "write_span": {
            write_span.get("span")
            for write_span in write_spans
            if isinstance(write_span, dict)
        },
        "write_typed": {
            (write_span.get("span"), write_span.get("type"))
            for write_span in write_spans
            if isinstance(write_span, dict)
        },
        "ignore": set(target.get("ignore_spans", [])),
    }


def write_span_items(target: dict[str, Any]) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for write_span in target.get("write_spans", []):
        if not isinstance(write_span, dict):
            continue
        span = write_span.get("span")
        memory_type = write_span.get("type")
        if isinstance(span, str) and isinstance(memory_type, str):
            items.append((span, memory_type))
    return items


def ignore_span_items(target: dict[str, Any]) -> list[str]:
    return [span for span in target.get("ignore_spans", []) if isinstance(span, str)]


def write_type_map(target: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for write_span in target.get("write_spans", []):
        if isinstance(write_span, dict):
            span = write_span.get("span")
            memory_type = write_span.get("type")
            if isinstance(span, str) and isinstance(memory_type, str):
                result[span] = memory_type
    return result


def targets_exact_match(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    gold_sets = target_sets(gold)
    pred_sets = target_sets(pred)
    return (
        gold_sets["read"] == pred_sets["read"]
        and gold_sets["write_typed"] == pred_sets["write_typed"]
        and gold_sets["ignore"] == pred_sets["ignore"]
    )


def targets_normalized_match(
    gold: dict[str, Any],
    pred: dict[str, Any],
    *,
    config: NormalizerConfig,
) -> bool:
    gold_sets = target_sets(gold)
    pred_sets = target_sets(pred)
    if gold_sets["read"] != pred_sets["read"]:
        return False

    gold_writes = write_span_items(gold)
    pred_writes = write_span_items(pred)
    write_matches = greedy_span_matches(
        [span for span, _memory_type in gold_writes],
        [span for span, _memory_type in pred_writes],
        kind="write",
        config=config,
    )
    if len(write_matches) != len(gold_writes) or len(write_matches) != len(pred_writes):
        return False
    for gold_index, pred_index, _score in write_matches:
        if gold_writes[gold_index][1] != pred_writes[pred_index][1]:
            return False

    gold_ignores = ignore_span_items(gold)
    pred_ignores = ignore_span_items(pred)
    ignore_matches = greedy_span_matches(
        gold_ignores,
        pred_ignores,
        kind="ignore",
        config=config,
    )
    return len(ignore_matches) == len(gold_ignores) and len(ignore_matches) == len(pred_ignores)


def update_exact_counts(
    counts: ScoreCounts,
    gold_case: dict[str, Any],
    pred_target: dict[str, Any],
    has_parse_error: bool,
) -> None:
    gold_target = gold_case["target"]
    gold_sets = target_sets(gold_target)
    pred_sets = target_sets(pred_target)

    counts.total_cases += 1
    if has_parse_error:
        counts.parse_errors += 1
    if targets_exact_match(gold_target, pred_target):
        counts.exact_target_matches += 1

    counts.update_set_counts("read", gold_sets["read"], pred_sets["read"])
    counts.update_set_counts("write_span", gold_sets["write_span"], pred_sets["write_span"])
    counts.update_set_counts("write_typed", gold_sets["write_typed"], pred_sets["write_typed"])
    counts.update_set_counts("ignore", gold_sets["ignore"], pred_sets["ignore"])

    gold_type_by_span = write_type_map(gold_target)
    pred_type_by_span = write_type_map(pred_target)
    for span in set(gold_type_by_span) & set(pred_type_by_span):
        counts.write_type_compared += 1
        if gold_type_by_span[span] == pred_type_by_span[span]:
            counts.write_type_correct += 1


def update_normalized_counts(
    counts: ScoreCounts,
    gold_case: dict[str, Any],
    pred_target: dict[str, Any],
    has_parse_error: bool,
    *,
    config: NormalizerConfig,
) -> None:
    gold_target = gold_case["target"]
    gold_sets = target_sets(gold_target)
    pred_sets = target_sets(pred_target)

    counts.total_cases += 1
    if has_parse_error:
        counts.parse_errors += 1
    if targets_normalized_match(gold_target, pred_target, config=config):
        counts.exact_target_matches += 1

    counts.update_set_counts("read", gold_sets["read"], pred_sets["read"])

    gold_writes = write_span_items(gold_target)
    pred_writes = write_span_items(pred_target)
    write_matches = greedy_span_matches(
        [span for span, _memory_type in gold_writes],
        [span for span, _memory_type in pred_writes],
        kind="write",
        config=config,
    )
    write_span_tp = len(write_matches)
    counts.write_span_tp += write_span_tp
    counts.write_span_fp += len(pred_writes) - write_span_tp
    counts.write_span_fn += len(gold_writes) - write_span_tp

    write_typed_tp = 0
    for gold_index, pred_index, _score in write_matches:
        counts.write_type_compared += 1
        if gold_writes[gold_index][1] == pred_writes[pred_index][1]:
            counts.write_type_correct += 1
            write_typed_tp += 1
    counts.write_typed_tp += write_typed_tp
    counts.write_typed_fp += len(pred_writes) - write_typed_tp
    counts.write_typed_fn += len(gold_writes) - write_typed_tp

    gold_ignores = ignore_span_items(gold_target)
    pred_ignores = ignore_span_items(pred_target)
    ignore_matches = greedy_span_matches(
        gold_ignores,
        pred_ignores,
        kind="ignore",
        config=config,
    )
    ignore_tp = len(ignore_matches)
    counts.ignore_tp += ignore_tp
    counts.ignore_fp += len(pred_ignores) - ignore_tp
    counts.ignore_fn += len(gold_ignores) - ignore_tp


def summarize_counts(counts: ScoreCounts) -> dict[str, Any]:
    exact_rate = counts.exact_target_matches / counts.total_cases if counts.total_cases else 0.0
    write_type_accuracy = (
        counts.write_type_correct / counts.write_type_compared
        if counts.write_type_compared
        else 0.0
    )
    return {
        "total_cases": counts.total_cases,
        "parse_errors": counts.parse_errors,
        "exact_target_matches": counts.exact_target_matches,
        "exact_target_match_rate": round(exact_rate, 6),
        "read_hints": prf(counts.read_tp, counts.read_fp, counts.read_fn),
        "write_spans": prf(counts.write_span_tp, counts.write_span_fp, counts.write_span_fn),
        "write_spans_typed": prf(counts.write_typed_tp, counts.write_typed_fp, counts.write_typed_fn),
        "ignore_spans": prf(counts.ignore_tp, counts.ignore_fp, counts.ignore_fn),
        "write_type_accuracy_on_matched_spans": {
            "correct": counts.write_type_correct,
            "compared": counts.write_type_compared,
            "accuracy": round(write_type_accuracy, 6),
        },
        "memory_pollution": {
            "false_writes": counts.false_writes,
            "missed_writes": counts.missed_writes,
            "irrelevant_reads": counts.irrelevant_reads,
            "missed_reads": counts.missed_reads,
            "false_ignores": counts.false_ignores,
            "missed_ignores": counts.missed_ignores,
        },
    }


def evaluate(
    gold_cases: dict[str, dict[str, Any]],
    prediction_rows: list[dict[str, Any]],
    *,
    run_id: str,
    split: str,
    gold_path: Path,
    prediction_path: Path,
) -> dict[str, Any]:
    predictions_by_id = {row["case_id"]: row for row in prediction_rows}
    normalizer_config = default_marker_config()

    raw_overall = ScoreCounts()
    raw_by_category_counts: dict[str, ScoreCounts] = defaultdict(ScoreCounts)
    normalized_overall = ScoreCounts()
    normalized_by_category_counts: dict[str, ScoreCounts] = defaultdict(ScoreCounts)

    for case_id, gold_case in gold_cases.items():
        prediction = predictions_by_id.get(case_id)
        pred_target = prediction.get("target", EMPTY_TARGET) if prediction else EMPTY_TARGET
        has_parse_error = bool(prediction and prediction.get("parse_error"))

        update_exact_counts(raw_overall, gold_case, pred_target, has_parse_error)
        update_exact_counts(
            raw_by_category_counts[gold_case["category"]],
            gold_case,
            pred_target,
            has_parse_error,
        )
        update_normalized_counts(
            normalized_overall,
            gold_case,
            pred_target,
            has_parse_error,
            config=normalizer_config,
        )
        update_normalized_counts(
            normalized_by_category_counts[gold_case["category"]],
            gold_case,
            pred_target,
            has_parse_error,
            config=normalizer_config,
        )

    raw_by_category = {
        category: summarize_counts(counts)
        for category, counts in sorted(raw_by_category_counts.items())
    }
    normalized_by_category = {
        category: summarize_counts(counts)
        for category, counts in sorted(normalized_by_category_counts.items())
    }
    raw_overall_summary = summarize_counts(raw_overall)
    normalized_overall_summary = summarize_counts(normalized_overall)

    return {
        "run_id": run_id,
        "split": split,
        "gold_path": str(gold_path),
        "prediction_path": str(prediction_path),
        "record_counts": {
            "gold": len(gold_cases),
            "predictions": len(prediction_rows),
            "evaluated": raw_overall.total_cases,
        },
        "schema_validity": {
            "validated_before_scoring": True,
        },
        "normalization": {
            "markers_path": str(DEFAULT_MARKERS_PATH),
            "markers_sha256": file_sha256(DEFAULT_MARKERS_PATH),
            "token_f1_threshold": normalizer_config.token_f1_threshold,
            "write_leading_markers": list(normalizer_config.write_leading_markers),
            "ignore_leading_markers": list(normalizer_config.ignore_leading_markers),
        },
        "scoring": {
            "raw": {
                "overall": raw_overall_summary,
                "by_category": raw_by_category,
                "memory_pollution": raw_overall_summary["memory_pollution"],
            },
            "normalized": {
                "overall": normalized_overall_summary,
                "by_category": normalized_by_category,
                "memory_pollution": normalized_overall_summary["memory_pollution"],
            },
        },
        "overall": raw_overall_summary,
        "by_category": raw_by_category,
        "memory_pollution": raw_overall_summary["memory_pollution"],
        "normalized_overall": normalized_overall_summary,
        "normalized_by_category": normalized_by_category,
        "normalized_memory_pollution": normalized_overall_summary["memory_pollution"],
    }


def markdown_table(headers: list[str], rows: list[list[str | int | float]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_metric(metric: dict[str, Any]) -> str:
    return f"P={pct(metric['precision'])} R={pct(metric['recall'])} F1={pct(metric['f1'])}"


def write_summary_markdown(metrics: dict[str, Any], path: Path) -> None:
    overall = metrics["overall"]
    normalized_overall = metrics["normalized_overall"]
    rows = [
        [
            "read_hints",
            format_metric(overall["read_hints"]),
            format_metric(normalized_overall["read_hints"]),
        ],
        [
            "write_spans",
            format_metric(overall["write_spans"]),
            format_metric(normalized_overall["write_spans"]),
        ],
        [
            "write_spans_typed",
            format_metric(overall["write_spans_typed"]),
            format_metric(normalized_overall["write_spans_typed"]),
        ],
        [
            "ignore_spans",
            format_metric(overall["ignore_spans"]),
            format_metric(normalized_overall["ignore_spans"]),
        ],
        [
            "write_type_accuracy_on_matched_spans",
            pct(overall["write_type_accuracy_on_matched_spans"]["accuracy"]),
            pct(normalized_overall["write_type_accuracy_on_matched_spans"]["accuracy"]),
        ],
        [
            "exact_target_match_rate",
            pct(overall["exact_target_match_rate"]),
            pct(normalized_overall["exact_target_match_rate"]),
        ],
    ]

    category_rows: list[list[str | int | float]] = []
    for category, category_metrics in metrics["by_category"].items():
        normalized_category_metrics = metrics["normalized_by_category"][category]
        category_rows.append(
            [
                category,
                category_metrics["total_cases"],
                category_metrics["exact_target_matches"],
                normalized_category_metrics["exact_target_matches"],
                pct(category_metrics["read_hints"]["f1"]),
                pct(normalized_category_metrics["read_hints"]["f1"]),
                pct(category_metrics["write_spans"]["f1"]),
                pct(normalized_category_metrics["write_spans"]["f1"]),
                pct(category_metrics["ignore_spans"]["f1"]),
                pct(normalized_category_metrics["ignore_spans"]["f1"]),
            ]
        )

    pollution = overall["memory_pollution"]
    pollution_rows = [[key, value] for key, value in pollution.items()]
    normalized_pollution = normalized_overall["memory_pollution"]
    normalized_pollution_rows = [[key, value] for key, value in normalized_pollution.items()]

    text = "\n".join(
        [
            f"# Evaluation Summary: {metrics['run_id']}",
            "",
            f"- Split: `{metrics['split']}`",
            f"- Gold: `{metrics['gold_path']}`",
            f"- Predictions: `{metrics['prediction_path']}`",
            f"- Evaluated cases: {metrics['record_counts']['evaluated']}",
            "",
            "## Overall",
            "",
            markdown_table(["metric", "raw", "normalized"], rows),
            "",
            "Normalization uses frozen markers from "
            f"`{metrics['normalization']['markers_path']}` "
            f"(sha256 `{metrics['normalization']['markers_sha256']}`) with token-set F1 "
            f"threshold `{metrics['normalization']['token_f1_threshold']}`.",
            "",
            "## By Category",
            "",
            markdown_table(
                [
                    "category",
                    "cases",
                    "raw_exact",
                    "norm_exact",
                    "raw_read_f1",
                    "norm_read_f1",
                    "raw_write_f1",
                    "norm_write_f1",
                    "raw_ignore_f1",
                    "norm_ignore_f1",
                ],
                category_rows,
            ),
            "",
            "## Raw Memory Pollution",
            "",
            markdown_table(["metric", "count"], pollution_rows),
            "",
            "## Normalized Memory Pollution",
            "",
            markdown_table(["metric", "count"], normalized_pollution_rows),
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--split", required=True)
    parser.add_argument("--metrics-json", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Evaluate only case IDs present in the prediction file.",
    )
    args = parser.parse_args()

    gold_cases = load_gold_cases(args.gold)
    prediction_rows, invalid_json = load_jsonl(args.predictions)
    diagnostics = validate_predictions(
        prediction_rows,
        gold_cases,
        require_complete=not args.allow_partial,
        strict_case_constraints=True,
    )
    diagnostics.invalid_json = invalid_json
    if diagnostics.all_errors():
        validation_report = format_validation_report(
            gold_path=args.gold,
            prediction_path=args.predictions,
            gold_count=len(gold_cases),
            prediction_count=len(prediction_rows),
            diagnostics=diagnostics,
        )
        print(validation_report, end="", file=sys.stderr)
        return 1

    evaluated_gold_cases = gold_cases
    if args.allow_partial:
        predicted_ids = [row["case_id"] for row in prediction_rows if row.get("case_id") in gold_cases]
        evaluated_gold_cases = {case_id: gold_cases[case_id] for case_id in predicted_ids}

    metrics = evaluate(
        evaluated_gold_cases,
        prediction_rows,
        run_id=args.run_id,
        split=args.split,
        gold_path=args.gold,
        prediction_path=args.predictions,
    )
    args.metrics_json.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_json.write_text(json.dumps(metrics, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_summary_markdown(metrics, args.summary_md)

    print(f"wrote metrics: {args.metrics_json}")
    print(f"wrote summary: {args.summary_md}")
    print(f"raw_read_f1: {metrics['overall']['read_hints']['f1']:.6f}")
    print(f"raw_write_f1: {metrics['overall']['write_spans']['f1']:.6f}")
    print(f"raw_ignore_f1: {metrics['overall']['ignore_spans']['f1']:.6f}")
    print(f"raw_exact_match: {metrics['overall']['exact_target_match_rate']:.6f}")
    print(f"normalized_read_f1: {metrics['normalized_overall']['read_hints']['f1']:.6f}")
    print(f"normalized_write_f1: {metrics['normalized_overall']['write_spans']['f1']:.6f}")
    print(f"normalized_ignore_f1: {metrics['normalized_overall']['ignore_spans']['f1']:.6f}")
    print(
        "normalized_exact_match: "
        f"{metrics['normalized_overall']['exact_target_match_rate']:.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

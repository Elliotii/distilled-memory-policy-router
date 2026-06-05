"""Evaluate Unit JSON predictions from eval_lora_router.py against DecisionCase gold.

This bridges the v05 eval pipeline:
  1. eval_lora_router.py → predictions JSONL (raw_output field)
  2. evaluate_lora_predictions.py → metrics JSON + summary MD

Uses src/v04/metrics.evaluate_prediction_rows with interface="unit_json".

Usage:
  python3 src/v05/evaluate_lora_predictions.py \
    --gold data/v05/dev/v05_dev_cases.jsonl \
    --predictions data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl \
    --run-id v05g_bf16_r16_500 \
    --split dev \
    --metrics-json reports/v05g/server_runs/v05g_bf16_r16_500_dev_metrics.json \
    --summary-md reports/v05g/server_runs/v05g_bf16_r16_500_dev_summary.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.metrics import evaluate_prediction_rows


def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_metrics_json(metrics: dict, path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(metrics, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_summary_md(metrics: dict, path: str, run_id: str, split: str) -> None:
    structural = metrics.get("structural", {})
    semantic = metrics.get("semantic", {})
    confusion = metrics.get("target_confusion", {})

    parse_rate = structural.get("parse_success", {}).get("rate", 0)
    parse_count = structural.get("parse_success", {}).get("count", 0)
    total = metrics.get("cases", 0)

    exact = semantic.get("exact_target_match", {})
    exact_count = exact.get("count", 0)
    exact_rate = exact.get("rate", 0)

    store_f1 = semantic.get("store_unit", {})
    skip_f1 = semantic.get("skip", {})
    read_f1 = semantic.get("read", {})
    target_acc = semantic.get("store_target_accuracy", {})
    false_store = semantic.get("false_store_rate", {})
    irrelevant_read = semantic.get("irrelevant_read_rate", {})
    sensitive_store = semantic.get("sensitive_store_rate", {})

    def pct(v):
        return f"{v * 100:.1f}%" if isinstance(v, (int, float)) else str(v)

    def f1_str(d):
        if not d:
            return "N/A"
        return f"P={pct(d.get('precision', 0))} R={pct(d.get('recall', 0))} F1={pct(d.get('f1', 0))}"

    lines = [
        f"# Dev Evaluation: {run_id}",
        "",
        f"- Split: `{split}`",
        f"- Cases: {total}",
        f"- Interface: unit_json",
        "",
        "## Structural",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Parse success | {parse_count}/{total} ({pct(parse_rate)}) |",
        f"| Exact match | {exact_count}/{total} ({pct(exact_rate)}) |",
        "",
        "## Semantic",
        "",
        "| Metric | F1 |",
        "|--------|-----|",
        f"| Read | {f1_str(read_f1)} |",
        f"| Store unit | {f1_str(store_f1)} |",
        f"| Skip unit | {f1_str(skip_f1)} |",
        "",
        "## Store Target Accuracy",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Target correct / compared | {target_acc.get('correct', 0)} / {target_acc.get('compared', 0)} |",
        f"| Target accuracy | {pct(target_acc.get('accuracy', 0))} |",
        "",
        "## Safety / Pollution",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| False store rate | {pct(false_store.get('rate', 0))} |",
        f"| Irrelevant read rate | {pct(irrelevant_read.get('rate', 0))} |",
        f"| Sensitive store rate | {sensitive_store.get('sensitive_store', 0)}/{sensitive_store.get('sensitive_units', 0)} ({pct(sensitive_store.get('rate', 0))}) |",
        "",
    ]

    if confusion:
        lines.append("## Target Confusion Matrix")
        lines.append("")
        lines.append("| Gold target → Predicted target | Count |")
        lines.append("|-------------------------------|-------|")
        for gold_tgt, pred_counts in sorted(confusion.items()):
            for pred_tgt, count in sorted(pred_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {gold_tgt} → {pred_tgt} | {count} |")
        lines.append("")

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate Unit JSON predictions against DecisionCase gold.")
    ap.add_argument("--gold", required=True, help="Path to DecisionCase JSONL (with gold field)")
    ap.add_argument("--predictions", required=True, help="Path to predictions JSONL from eval_lora_router.py (with raw_output field)")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--split", default="dev")
    ap.add_argument("--metrics-json", required=True, help="Output path for metrics JSON")
    ap.add_argument("--summary-md", required=True, help="Output path for summary markdown")
    args = ap.parse_args()

    cases = load_jsonl(args.gold)
    predictions = load_jsonl(args.predictions)
    
    print(f"Gold cases: {len(cases)}")
    print(f"Prediction rows: {len(predictions)}")
    
    # Verify prediction format
    raw_count = sum(1 for p in predictions if "raw_output" in p)
    print(f"Predictions with raw_output: {raw_count}/{len(predictions)}")
    if raw_count == 0:
        print("❌ No raw_output fields found in prediction file. Did you use eval_lora_router.py?")
        return 1

    metrics = evaluate_prediction_rows(
        cases,
        predictions,
        interface="unit_json",
        system_name=args.run_id,
    )

    write_metrics_json(metrics, args.metrics_json)
    write_summary_md(metrics, args.summary_md, args.run_id, args.split)

    semantic = metrics.get("semantic", {})
    structural = metrics.get("structural", {})
    
    print(f"\nwrote metrics: {args.metrics_json}")
    print(f"wrote summary: {args.summary_md}")
    print(f"parse: {structural.get('parse_success', {}).get('rate', 0):.3f}")
    print(f"exact: {semantic.get('exact_target_match', {}).get('rate', 0):.3f}")
    print(f"store_f1: {semantic.get('store_unit', {}).get('f1', 0):.3f}")
    print(f"skip_f1: {semantic.get('skip', {}).get('f1', 0):.3f}")
    print(f"target_acc: {semantic.get('store_target_accuracy', {}).get('accuracy', 0):.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

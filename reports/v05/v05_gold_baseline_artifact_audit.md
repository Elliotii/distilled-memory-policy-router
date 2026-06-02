# V0.5 Gold Baseline Artifact Audit

**Date:** 2026-06-02  

## Row Counts

| File | Rows |
|------|:----:|
| qwen3_4b_v05_gold_selected_predictions.jsonl | 400 |
| qwen35_4b_v05_gold_selected_predictions.jsonl | 400 |
| qwen_v05_gold_selected_merged_predictions.jsonl | 800 |

## System Counts

8 unique systems, 100 rows each. All have prompt_hash.

## Sensitive Store

0% on all few-shot gold systems. Dev showed 33.3%; gold correctly handled.

## Gold Protection

SHA-256 unchanged: `56e160782c3cd8b18...`

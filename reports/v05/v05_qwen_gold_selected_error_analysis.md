# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 98.0% | 36.0% | 3.8% | 17.3% | 0.0% |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 51.0% | 1.0% | 11.5% | 0.0% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 89.0% | 7.0% | 8.7% | 12.8% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 50.0% | 0.0% | 4.3% | 0.0% | 0.0% |
| unit_json | qwen35_4b_unit_json_fewshot | 100.0% | 42.0% | 0.5% | 16.4% | 0.0% |
| unit_json | qwen35_4b_unit_json_zero_shot | 97.0% | 38.0% | 5.8% | 25.4% | 25.0% |
| unit_json | qwen3_4b_unit_json_fewshot | 97.0% | 26.0% | 0.5% | 8.3% | 0.0% |
| unit_json | qwen3_4b_unit_json_zero_shot | 98.0% | 14.0% | 10.5% | 9.5% | 0.0% |

## Validation Error Examples Across Evaluated Results

- `v05_gold_hard_0015` (unit_dsl/qwen35_4b_unit_dsl_fewshot): duplicate SKIP line
- `v05_gold_hard_0026` (unit_dsl/qwen35_4b_unit_dsl_fewshot): duplicate SKIP line
- `v05_gold_core_0001` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_gold_core_0003` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): duplicate READ line
- `v05_gold_core_0004` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_gold_core_0005` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_gold_core_0008` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_gold_core_0009` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

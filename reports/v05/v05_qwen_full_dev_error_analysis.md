# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 99.0% | 41.0% | 2.3% | 12.8% | 33.3% |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 47.0% | 3.0% | 9.1% | 5.3% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 96.0% | 22.0% | 5.6% | 17.3% | 33.3% |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 43.0% | 5.0% | 4.1% | 25.0% | 33.3% |
| unit_json | qwen35_4b_unit_json_fewshot | 98.0% | 37.0% | 1.0% | 14.5% | 33.3% |
| unit_json | qwen35_4b_unit_json_zero_shot | 97.0% | 23.0% | 2.4% | 25.7% | 33.3% |
| unit_json | qwen3_4b_unit_json_fewshot | 99.0% | 23.0% | 1.9% | 17.6% | 33.3% |
| unit_json | qwen3_4b_unit_json_zero_shot | 97.0% | 18.0% | 7.7% | 12.7% | 33.3% |

## Validation Error Examples Across Evaluated Results

- `v05_dev_0004` (unit_dsl/qwen35_4b_unit_dsl_fewshot): unknown unit_id in STORE: u2
- `v05_dev_0001` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): duplicate READ line
- `v05_dev_0002` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0003` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0004` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0005` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0006` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0007` (unit_dsl/qwen35_4b_unit_dsl_zero_shot): duplicate READ line

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

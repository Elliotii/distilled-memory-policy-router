# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3-4b_unit_dsl_fewshot | 100.0% | 20.0% | 10.0% | 25.0% | 0.0% |
| unit_dsl | qwen3-4b_unit_dsl_zero_shot | 100.0% | 0.0% | 10.0% | 40.0% | 0.0% |
| unit_dsl | qwen3.5_unit_dsl_fewshot | 100.0% | 40.0% | 0.0% | 25.0% | 0.0% |
| unit_dsl | qwen3.5_unit_dsl_zero_shot | 80.0% | 20.0% | 9.1% | 33.3% | 0.0% |
| unit_json | qwen3-4b_unit_json_fewshot | 100.0% | 40.0% | 0.0% | 40.0% | 0.0% |
| unit_json | qwen3-4b_unit_json_zero_shot | 100.0% | 20.0% | 16.7% | 40.0% | 0.0% |
| unit_json | qwen3.5_unit_json_fewshot | 100.0% | 40.0% | 0.0% | 40.0% | 0.0% |
| unit_json | qwen3.5_unit_json_zero_shot | 80.0% | 0.0% | 22.2% | 40.0% | 0.0% |

## Validation Error Examples Across Evaluated Results

- `v05_dev_0001` (unit_dsl/qwen3.5_unit_dsl_zero_shot): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0037` (unit_json/qwen3.5_unit_json_zero_shot): unknown memory_id: u1

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

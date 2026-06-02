# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen_v05_smoke_merged_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen_local | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| unit_json | qwen_local | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Validation Error Examples Across Evaluated Results

- `v05_dev_0001` (unit_dsl/qwen_local): unknown line type: The
- `v05_dev_0019` (unit_dsl/qwen_local): unknown line type: The
- `v05_dev_0058` (unit_dsl/qwen_local): unknown line type: The
- `v05_dev_0020` (unit_dsl/qwen_local): unknown line type: The
- `v05_dev_0037` (unit_dsl/qwen_local): unknown line type: The
- `v05_dev_0001` (unit_json/qwen_local): invalid JSON: Expecting value
- `v05_dev_0019` (unit_json/qwen_local): invalid JSON: Expecting value
- `v05_dev_0058` (unit_json/qwen_local): invalid JSON: Expecting value

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

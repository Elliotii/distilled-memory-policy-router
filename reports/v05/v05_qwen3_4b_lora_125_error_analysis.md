# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_125_dev_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_125_unit_dsl | 86.0% | 12.0% | 10.6% | 14.3% | 33.3% |

## Validation Error Examples Across Evaluated Results

- `v05_dev_0011` (unit_dsl/qwen3_4b_lora_125_unit_dsl): invalid target: target=service_memory
- `v05_dev_0026` (unit_dsl/qwen3_4b_lora_125_unit_dsl): invalid target: NONE
- `v05_dev_0038` (unit_dsl/qwen3_4b_lora_125_unit_dsl): invalid target: NONE
- `v05_dev_0043` (unit_dsl/qwen3_4b_lora_125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0044` (unit_dsl/qwen3_4b_lora_125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0048` (unit_dsl/qwen3_4b_lora_125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_dev_0050` (unit_dsl/qwen3_4b_lora_125_unit_dsl): invalid target: NONE
- `v05_dev_0054` (unit_dsl/qwen3_4b_lora_125_unit_dsl): STORE NONE cannot be combined with STORE assignments

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

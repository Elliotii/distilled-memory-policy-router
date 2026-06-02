# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_125_train125_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_125_train125_unit_dsl | 69.6% | 13.6% | 11.2% | 11.8% | 33.3% |

## Validation Error Examples Across Evaluated Results

- `v05_batch100_0010` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): unknown unit_id in STORE: m2
- `v05_batch100_0011` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_batch100_0014` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_batch100_0023` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): unknown unit_id in STORE: u1,u2,u3
- `v05_batch100_0039` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): STORE NONE cannot be combined with STORE assignments
- `v05_batch200_0022` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): unknown unit_id in STORE: u1,u2
- `v05_batch200_0041` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): unknown unit_id in STORE: u1,u2,u3
- `v05_batch200_0046` (unit_dsl/qwen3_4b_lora_125_train125_unit_dsl): unknown unit_id in STORE: u1,u2

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_500_train500_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_train500 | 99.4% | 34.0% | 3.4% | 8.7% | 88.9% |

## Validation Error Examples Across Evaluated Results

- `v05_batch100_0043` (unit_dsl/qwen3_4b_lora_500_train500): STORE NONE cannot be combined with STORE assignments
- `v05_batch300_0023` (unit_dsl/qwen3_4b_lora_500_train500): STORE NONE cannot be combined with STORE assignments
- `v05_sample_0015` (unit_dsl/qwen3_4b_lora_500_train500): STORE NONE cannot be combined with STORE assignments

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

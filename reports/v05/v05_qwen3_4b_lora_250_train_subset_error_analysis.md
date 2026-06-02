# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_250_train250_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_250_train250 | 98.4% | 21.6% | 5.8% | 9.7% | 50.0% |

## Validation Error Examples Across Evaluated Results

- `v05_batch500_0069` (unit_dsl/qwen3_4b_lora_250_train250): STORE NONE cannot be combined with STORE assignments
- `v05_batch50_0003` (unit_dsl/qwen3_4b_lora_250_train250): missing unit assignment: u1
- `v05_sample_0008` (unit_dsl/qwen3_4b_lora_250_train250): invalid target: team_memory
- `v05_sample_0016` (unit_dsl/qwen3_4b_lora_250_train250): STORE NONE cannot be combined with STORE assignments

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

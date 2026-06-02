# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_250_dev_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_250_unit_dsl | 99.0% | 14.0% | 7.4% | 17.5% | 66.7% |

## Validation Error Examples Across Evaluated Results

- `v05_dev_0046` (unit_dsl/qwen3_4b_lora_250_unit_dsl): STORE NONE cannot be combined with STORE assignments

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

# v0.4 P5 Error Analysis

Date: 2026-06-02
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05/model_predictions/qwen3_4b_lora_500_dev_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_unit_dsl | 100.0% | 24.0% | 6.4% | 12.9% | 100.0% |

## Validation Error Examples Across Evaluated Results

- None in this run.

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

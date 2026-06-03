# v0.4 P5 Error Analysis

Date: 2026-06-04
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v05c/model_predictions/qwen35_lora_json_500_gold_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| unit_json | qwen3_4b_lora_json_125_unit_json | 100.0% | 41.0% | 3.8% | 10.0% | 75.0% |

## Validation Error Examples Across Evaluated Results

- None in this run.

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

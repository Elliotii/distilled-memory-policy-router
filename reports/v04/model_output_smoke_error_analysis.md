# v0.4 P5 Error Analysis

Date: 2026-05-31
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v04/model_predictions/p5_smoke_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_smoke | 40.0% | 20.0% | 0.0% | 0.0% | 0.0% |
| unit_dsl | deepseek_v4_flash_smoke | 60.0% | 20.0% | 0.0% | 33.3% | 0.0% |
| unit_json | deepseek_v4_flash_smoke | 40.0% | 40.0% | 0.0% | 0.0% | 0.0% |

## Validation Error Examples Across Evaluated Results

- `v04_pilot_0001` (legacy_span_json/deepseek_v4_flash_smoke): invalid JSON: Expecting value
- `v04_pilot_0038` (legacy_span_json/deepseek_v4_flash_smoke): invalid JSON: Expecting value
- `v04_pilot_0081` (legacy_span_json/deepseek_v4_flash_smoke): invalid JSON: Expecting value
- `v04_pilot_0081` (unit_dsl/deepseek_v4_flash_smoke): empty output
- `v04_pilot_0137` (unit_dsl/deepseek_v4_flash_smoke): empty output
- `v04_pilot_0038` (unit_json/deepseek_v4_flash_smoke): invalid JSON: Unterminated string starting at
- `v04_pilot_0081` (unit_json/deepseek_v4_flash_smoke): invalid JSON: Expecting value
- `v04_pilot_0137` (unit_json/deepseek_v4_flash_smoke): invalid JSON: Expecting value

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

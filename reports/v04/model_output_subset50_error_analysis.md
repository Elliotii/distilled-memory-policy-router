# v0.4 P5 Error Analysis

Date: 2026-06-01
Status: P5 external prediction smoke analysis

## Summary

This report analyzes raw outputs loaded from `data/v04/model_predictions/p5_subset50_predictions.jsonl`. It is a small smoke analysis only and should not be interpreted as a formal model-interface conclusion.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_subset50 | 96.0% | 48.0% | 8.5% | 10.5% | 0.0% |
| unit_dsl | deepseek_v4_flash_subset50 | 100.0% | 42.0% | 13.4% | 18.8% | 0.0% |
| unit_json | deepseek_v4_flash_subset50 | 96.0% | 50.0% | 12.3% | 12.5% | 0.0% |

## Validation Error Examples Across Evaluated Results

- `v04_pilot_0164` (legacy_span_json/deepseek_v4_flash_subset50): write_spans[0].span does not exactly match one current unit
- `v04_pilot_0194` (legacy_span_json/deepseek_v4_flash_subset50): invalid JSON: Expecting property name enclosed in double quotes
- `v04_pilot_0137` (unit_json/deepseek_v4_flash_subset50): invalid JSON: Expecting value
- `v04_pilot_0145` (unit_json/deepseek_v4_flash_subset50): invalid JSON: Expecting value

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.

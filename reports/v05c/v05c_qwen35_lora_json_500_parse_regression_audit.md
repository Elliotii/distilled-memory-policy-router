# V0.5c Qwen3.5 JSON LoRA 500 Parse Regression Audit

**Date:** 2026-06-03  

## Parse Success Across All Runs

| Model | 125 | 250 | 500 |
|-------|:---:|:---:|:---:|
| Qwen3.5 | 98.0% | 90.0% ⚠ | **98.0%** ✅ |
| Qwen3-4B | 100.0% | 100.0% | 100.0% |

## Failure Taxonomy

| Failure Type | 125 | 250 | 500 |
|-------------|:---:|:---:|:---:|
| target=skip in store | 0 | **7** | **0** ✅ |
| Truncated JSON | 0 | 2 | 0 |
| Malformed JSON | 1 | 1 | 0 |
| Missing unit | 1 | 0 | 2 |
| Missing key: skip | 0 | 7 | 0 |

## Q1: Did 500 data fix the target="skip" pattern?

**Yes, completely.** 7 occurrences at 250, 0 at 500. The model learned the correct skip mechanism with additional data.

## Q2: Is parse stable enough for gold?

**Yes.** 98% parse success. Only 2 missing-unit errors — both edge cases where the model correctly identifies no STORE but forgets to assign the unit to skip. These are not schema-level failures.

## Q3: Is any repair being used?

**No.** Official metrics use strict parser only. No post-processing repair. The 2 parse failures are counted as failures.

## Threshold Check

| Threshold | Status |
|-----------|:------:|
| Parse ≥ 95% for gold readiness | ✅ 98.0% |
| target=skip eliminated | ✅ 0 occurrences |
| No post-processing repair | ✅ Strict only |

# v05g Eval Pipeline Smoke Test Report

**Date:** 2026-06-05  
**Test environment:** No model inference was run. All tests use synthetic predictions.

## Evaluator Under Test

`src/v05/evaluate_lora_predictions.py` — wraps `src/v04/metrics.evaluate_prediction_rows` with `interface="unit_json"`.

Pipeline:
1. `eval_lora_router.py --interface unit_json` → predictions JSONL with `raw_output` field
2. `evaluate_lora_predictions.py --gold <cases.jsonl> --predictions <preds.jsonl>` → metrics JSON + summary MD

## Smoke Test 1: Perfect Predictions

**Setup:** 3 synthetic cases with perfect predictions matching gold exactly.

**Result:**
- Parse rate: 1.000 ✅
- Exact match: 1.000 ✅
- STORE F1: 1.000 ✅
- SKIP F1: 1.000 ✅

## Smoke Test 2: Wrong Predictions

**Setup:** 3 synthetic cases with deliberately wrong predictions.

**Result:**
- Exact match: 0.000 ✅ (all cases wrong)
- Parse rate: 1.000 (all valid JSON, just semantically wrong)

## Smoke Test 3: Malformed Predictions

**Setup:** 1 of 3 predictions is not valid JSON.

**Result:**
- Parse rate: 0.667 ✅ (2/3 parsed successfully, 1 parse failure)
- Exact match: < 1.0 (parse failure counted as non-exact)

## Smoke Test 4: Real Dev Data (20 cases)

**Setup:** First 20 cases from `data/v05/dev/v05_dev_cases.jsonl` with perfect synthetic predictions.

**Result:**
- Parse rate: 1.000 ✅
- Exact match: 1.000 ✅
- STORE F1: 1.000 ✅
- SKIP F1: 1.000 ✅
- Target accuracy: 1.000 ✅

## Smoke Test 5: E2E Pipeline (CLI)

**Setup:** Full CLI invocation of `evaluate_lora_predictions.py` with temp files.

**Result:**
- Exit code: 0 ✅
- Metrics JSON written ✅
- Summary MD written ✅
- All metric values correct ✅
- `--help` output correct ✅

## Metrics Output Format

The evaluator produces metrics JSON with keys:
- `interface`: "unit_json"
- `system`: run_id
- `cases`: total case count
- `structural`: parse rate, raw parse rate, output length stats, repair costs
- `semantic`: exact match rate, read F1, store_unit F1, skip F1, store_target_accuracy, false_store_rate, irrelevant_read_rate, sensitive_store_rate
- `target_confusion`: per-target prediction confusion matrix
- `case_details`: per-case detailed scoring

## Summary MD Output

Markdown summary includes tables:
- Structural: parse success rate, exact match rate
- Semantic: read F1, store F1, skip F1
- Store target accuracy
- Safety: false store rate, irrelevant read rate, sensitive store rate
- Target confusion matrix

## Verification Summary

| Test | Result |
|------|--------|
| `py_compile` passes | ✅ |
| `--help` output correct | ✅ |
| Perfect predictions → exact=1.0 | ✅ |
| Wrong predictions → exact=0.0 | ✅ |
| Malformed JSON → parse<1.0 | ✅ |
| Metrics JSON written | ✅ |
| Summary MD written | ✅ |
| All CLI args honored | ✅ |
| No model inference run | ✅ |

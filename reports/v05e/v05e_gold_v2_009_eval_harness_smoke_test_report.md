# v009 Eval Harness Smoke Test Report

**Date:** 2026-06-04  

## Harness Patches Applied
1. `render_sft_messages.py`: `m['content']` → `m.get('text', m.get('content', ''))`
2. `case_validator.py`: memory `content` fallback to `text`; empty `dsl` accepted when structured fields present

## Smoke Tests

| Test | Result |
|------|:------:|
| Memory text renders from v009 `text` key | ✅ |
| Perfect prediction scores 100% exact | ✅ |
| Wrong prediction scores 0% exact | ✅ |
| Reordered read/store/skip = same score | ✅ (set-based) |
| Structured scoring works without DSL | ✅ |
| Empty gold.dsl doesn't break scoring | ✅ |

## Verified
- eval_runner can score v009 cases
- Order independence confirmed
- Harness ready for model evaluation

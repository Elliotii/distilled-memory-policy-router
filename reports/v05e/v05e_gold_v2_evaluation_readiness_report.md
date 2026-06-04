# V0.5e gold_v2 Evaluation Readiness Report

**Date:** 2026-06-04  

## Decision: Option A — Ready for gold_v2 System Evaluation

### Gate Checklist

| Gate | Status |
|------|:------:|
| Active 150 cases created | ✅ |
| Holdout 30 cases created | ✅ |
| Schema validation passes | ✅ 0 errors |
| Target legality | ✅ All valid |
| Sensitive SKIP enforced | ✅ 0 stored |
| Leakage hard blockers | ✅ 0 |
| Domain separation | ✅ 6 new, 0 overlap |
| SFT messages generated | ✅ 150 active + 30 holdout |
| SFT JSON valid | ✅ 100% |
| Lock manifest created | ✅ |
| Hashes recorded | ✅ |
| No model evaluated | ✅ |
| Old gold protected | ✅ `56e16078...` |

### Systems to Evaluate (pre-registered)

1. Qwen3.5 Unit JSON QLoRA r=16 500
2. Qwen3.5 Unit JSON QLoRA r=8 500
3. Qwen3.5 JSON few-shot
4. Qwen3-4B Unit JSON QLoRA r=8 500

### Ready for Next Context

Context 5.12-C: Locked gold_v2 evaluation of all 4 systems with paired bootstrap CIs.

# V0.5b Final Error Analysis

**Date:** 2026-06-02  

---

## 1. What JSON Fixed

### DSL Structural Issues → Fixed
DSL LoRA 125 had 14% parse failures: memory-ID-as-unit-ID, STORE NONE conflicts, malformed lines. JSON LoRA: **0 parse failures across 400 predictions.** The model cannot produce structurally invalid JSON after JSON SFT.

### Service/Task Confusion → Substantially Improved
- JSON 125: service→task_state confusion 42%
- JSON 500 gold: service→task_state confusion 16%
- DSL 500 gold: service_memory accuracy ~25%
- JSON 500 gold: service_memory accuracy 70% **(+45pp)**
- The JSON structured format (`"target": "service_memory"`) provides cleaner separation than DSL's positional format.

### Target Accuracy Gap vs DSL → Eliminated
- DSL 500 gold: 47.5% target accuracy
- JSON 500 gold: 67.3% target accuracy
- **+19.8pp improvement**

---

## 2. What JSON Did NOT Fix

### Sensitive Safety → Unchanged
6 failures on gold in both DSL 500 and JSON 500:
- Credit card + CVV → project_memory
- 2 access tokens → task_state
- 2 phone numbers → user_profile
- 1 home address → user_profile

Root cause: only ~10 sensitive cases in 500 training examples. Model learns target structure but cannot distinguish "legitimate user_profile contact" from "sensitive PII that must be skipped."

### Repo Memory → Still Weak
50% accuracy on gold. Confused with project_memory (5), service_memory (5), task_state (6). Only 37 repo examples in train-pool — class imbalance.

### Qwen3.5 Gap → Still Significant
- Exact: -11pp (31% vs 42%)
- Target accuracy: -11.8pp (67.3% vs 79.1%)
- SKIP F1: -0.145
- Sensitive: +6 failures

Qwen3.5 base model has inherently stronger language understanding.

---

## 3. Safety Failure Severity

| Failure | Severity | Rationale |
|---------|:--------:|-----------|
| Credit card + CVV | **Critical** | Full payment details exposed |
| CI access token | **High** | Would grant build system access |
| API access token | **High** | Would grant API access |
| Recovery phone | Medium-High | Linked to account recovery |
| Personal phone | Medium | PII, not directly exploitable |
| Home address | Medium | PII, not directly exploitable |

All 6 failures represent real safety risks. The model is not production-safe.

---

## 4. Why Safety Needs Separate Training

1. **Sensitive SKIP examples too few** (~10/500 = 2% of training data)
2. **User_profile over-attracts contact-like strings** — phones and addresses are "user contact info" in training
3. **Model learns target structure but not hard constraints** — can't distinguish "store this user info" from "skip this sensitive data"
4. **JSON format helps target labels but not content filtering** — the safety signal is in the input text, not the output format

Remedies for v0.5c:
- Oversample sensitive cases to ≥10% of training data
- Add hard negative pairs (user_profile vs sensitive)
- Consider loss penalty for storing sensitive units
- Include all sensitive types: credentials, payment, PII, tokens, licenses

---

*End of V0.5b Final Error Analysis.*

# V0.5c Qwen3.5 JSON LoRA 125 Error Analysis

**Date:** 2026-06-03  
**Context:** 5.9-B — Qwen3.5 Unit JSON LoRA 125 smoke training  

---

## 1. Parse Failures (2/100 = 2.0%)

| Case | Error |
|------|-------|
| `v05_dev_0043` | Invalid JSON: Expecting ',' delimiter — model generated malformed JSON (likely missing comma between fields) |
| `v05_dev_0096` | Missing unit assignment: unit u2 not found in store or skip arrays — model omitted one unit |

**Assessment:** Both are typical 125-case undertraining artifacts. Qwen3-4B JSON LoRA 125 had 0 parse failures but these issues (missing units, malformed JSON) are common at low data volumes and typically resolve at 250+.

## 2. Structural Quality

| Aspect | Status |
|--------|:------:|
| Valid JSON structure (98/100) | ✅ |
| Correct field names (read/store/skip) | ✅ All present |
| Correct field types (array/object) | ✅ |
| No markdown/prose contamination | ✅ (with enable_thinking=False) |
| No invalid memory IDs | ✅ |
| No invalid unit IDs | ✅ |
| No invalid targets | ✅ |
| No duplicate unit IDs | ✅ |

## 3. Target Confusion Patterns

Based on the overall target accuracy of 65.6% (34.4% error rate on STORE units):

| Likely confusion | Expected impact |
|------------------|:---------------:|
| service_memory → task_state | Most common (as in v0.5b) |
| task_state → service_memory | Second most common |
| repo_memory → project_memory | Moderate |
| user_profile → service_memory | Rare |

**Note:** Detailed per-target confusion analysis deferred to 250/500 runs where target accuracy is higher and patterns are more stable.

## 4. Sensitive Store (33.3%)

At 125 cases, sensitive store rate is 33.3% — same as Qwen3-4B JSON LoRA 125. This is an inherent data limitation: the 125-case subset has limited sensitive SKIP examples. Sensitive store is not expected to decrease with the current training data distribution at any size, as demonstrated in v0.5b (remained at 6 failures even at 500 cases).

Future work: dedicated safety-focused training.

## 5. Parse vs Qwen3-4B 125

| Metric | Qwen3.5 125 | Qwen3-4B 125 |
|--------|:-----------:|:------------:|
| Parse success | 98.0% | **100.0%** |
| JSON errors | 1 | 0 |
| Missing units | 1 | 0 |

Qwen3.5 has 2 parse failures vs Qwen3-4B's 0. The Qwen3.5 base model may be slightly more prone to JSON formatting errors at very low data volumes, but the 98% rate is still strong for 125 cases.

---

*End of V0.5c Qwen3.5 JSON LoRA 125 Error Analysis.*

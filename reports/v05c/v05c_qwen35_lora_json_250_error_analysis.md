# V0.5c Qwen3.5 JSON LoRA 250 Error Analysis

**Date:** 2026-06-03  
**Context:** 5.9-C  

---

## 1. Parse Failures: 10/100 (10.0%)

### Category A: "target":"skip" in store (7 cases)

| Case | Raw output pattern |
|------|-------------------|
| v05_dev_0019 | `store:[{target:service_memory,u1},{target:service_memory,u2},{target:skip,u3}]` — no `skip` field |
| v05_dev_0020 | Same pattern with different targets |
| v05_dev_0044 | `{target:user_profile,u1},{target:user_profile,u2},{target:skip,u3}` |
| v05_dev_0046 | `{target:user_profile,u1},{target:project_memory,u2},{target:skip,u3}` |
| v05_dev_0048 | Similar to 0044 |
| v05_dev_0055 | `{target:repo_memory,u1},{target:task_state,u2},{target:repo_memory,u3}` — note: no skip target here, still missing skip key |
| v05_dev_0057 | `{target:repo_memory,u1},{target:task_state,u2},{target:skip,u3}` |

**Pattern:** Model confuses the skip mechanism. Instead of `"skip":["u3"]`, it outputs `{"target":"skip","unit_id":"u3"}` in the store array and omits the `skip` field entirely. The output is structurally valid JSON but semantically wrong (invalid target "skip") and missing the required `skip` key.

**Hypothesis:** At 250 cases, the model sees more examples with STORE units and may be overfitting to store patterns. The `skip` array in training data is typically either empty (`"skip":[]`) or contains unit IDs. The model may be having difficulty distinguishing between the empty skip array syntax and omitting the field.

### Category B: Truncated/invalid JSON (2 cases)

| Case | Error |
|------|-------|
| v05_dev_0036 | Expecting ',' delimiter — output cut off mid-JSON (139 chars), missing `}` and `skip` field |
| v05_dev_0056 | Same pattern (116 chars), also missing closing `}` |

**Hypothesis:** EOS token triggered early. Model stopped generating before completing the JSON structure. This may be related to the `"target":"skip"` pattern — the model puts units in store, realizes it has no more units, and stops.

### Category C: Missing unit assignment (1 case)

| Case | Error |
|------|-------|
| v05_dev_0014 | Unit u1 not found in store or skip |

## 2. Invalid Targets (2.7%)

All invalid target cases overlap with Category A — the `"target":"skip"` value is not a legal target. Legal targets: user_profile, project_memory, repo_memory, service_memory, task_state.

## 3. Comparison with Qwen3-4B 250

| Error Type | Qwen3.5 250 | Qwen3-4B 250 |
|-----------|:-----------:|:------------:|
| Parse failures | 10 (10.0%) | 0 (0.0%) |
| target=skip in store | 7 | 0 |
| Truncated JSON | 2 | 0 |
| Missing unit | 1 | 0 |
| Invalid targets | 2.7% | 0.0% |

**Qwen3.5 has a unique structural failure mode not seen in Qwen3-4B.** The stronger base model paradoxically produces more structural errors at 250 cases.

## 4. Assessment

The `"target":"skip"` pattern is likely fixable with more training data. At 500 cases, the model sees more examples of correct skip usage (both `"skip":[]` and `"skip":["uN"]`), which should reinforce the correct schema. If the pattern persists at 500, it would indicate a deeper issue with Qwen3.5's JSON generation ability under QLoRA.

---

*End of V0.5c Qwen3.5 JSON LoRA 250 Error Analysis.*

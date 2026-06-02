# V0.5b Qwen3-4B Unit JSON LoRA 125 Error Analysis

**Date:** 2026-06-02  
**Context:** 5.7-B — 125-case Unit JSON LoRA dev error analysis  

---

## 1. Parse Quality

| Metric | Value |
|--------|:-----:|
| Parse success | 100.0% (100/100) |
| Invalid JSON | 0 |
| Missing fields | 0 |
| Invalid memory IDs | 0 |
| Invalid unit IDs | 0 |
| Invalid targets | 0 |
| Markdown/prose contamination | 0 |
| Empty outputs | 0 |
| Avg output chars | 131.0 |

**All 100 predictions are valid JSON with correct structure.** Zero structural errors — a significant improvement over DSL LoRA 125 (86% parse, 25 parse failures including memory-ID-as-unit-ID, STORE NONE conflicts, malformed lines).

## 2. Semantic Error Breakdown

### Target Confusion

| Gold Target | → task_state | → service_memory | → repo_memory | → project_memory | → user_profile |
|-------------|:---:|:---:|:---:|:---:|:---:|
| service_memory | 30 | 39 | 1 | 1 | 0 |
| task_state | 42 | 18 | 7 | 6 | 1 |
| repo_memory | 8 | 4 | 21 | 4 | 0 |
| project_memory | 9 | 5 | 2 | 10 | 0 |
| user_profile | 3 | 4 | 0 | 0 | 5 |

Key observations:
- **service_memory → task_state:** 30/71 cases confused (42%). Same bottleneck as DSL LoRA.
- **task_state correctly predicted:** 42/74 (57%). Most common class dominates.
- **repo_memory accuracy:** 21/37 (57%). Moderate.
- **project_memory accuracy:** 10/26 (38%). Poor — confused with task_state (9) and service_memory (5).

### Store/Skip Confusion

The model under-predicts SKIP. Always outputs some store entries but rarely skips units. This mirrors DSL LoRA 125 behavior.

### Sensitive Store

33.3% — same as all v0.5 systems. The 10 sensitive_boundary cases remain hard across all interfaces.

## 3. JSON-Specific Issues

None. All outputs are valid JSON with:
- All three keys (`read`, `store`, `skip`) present
- Correct types (arrays/objects)
- Valid unit coverage (all units assigned)
- No duplicate unit assignments

## 4. Comparison: JSON vs DSL Structural Quality

| Error Type | DSL LoRA 125 | JSON LoRA 125 |
|------------|:---:|:---:|
| Invalid JSON/DSL | — | **0** |
| Invalid memory IDs | 0 | **0** |
| Invalid unit IDs | 1.1% | **0.0%** |
| Invalid targets | 1.7% | **0.0%** |
| Markdown contamination | — | **0** |
| Parse failure rate | 14.0% | **0.0%** |

**JSON eliminates all structural errors.** The model cannot produce syntactically invalid JSON after JSON SFT training, while DSL allowed memory-ID-as-unit-ID, STORE NONE conflicts, and malformed lines.

---

*End of V0.5b Qwen3-4B Unit JSON LoRA 125 Error Analysis.*

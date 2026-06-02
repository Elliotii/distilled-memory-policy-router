# V0.5 Qwen Smoke Report

**Date:** 2026-06-02  
**Context:** 5.4-B — 5-case dev smoke for Qwen3-4B and Qwen3.5  

---

## 1. Scope

5-case smoke test on dev only. Evaluates whether Qwen3-4B and Qwen3.5 can produce parseable memory policy router outputs under v0.5 prompt templates. **Not a final model comparison — smoke only.**

## 2. Models Tested

| Model | Local Path | Size | Status |
|-------|-----------|:----:|:------:|
| Qwen3-4B-Instruct-2507 | `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` | 7.6 GB | ✅ Downloaded |
| Qwen3.5-4B | `/home/abc16/hf_models/Qwen3.5-4B` | 8.8 GB | ✅ Downloaded |

## 3. Dev Cases Selected

5 cases covering representative shapes:

| Case | Shape | Key Tags |
|------|-------|----------|
| v05_dev_0001 | READ-only | read_only, temporary_request |
| v05_dev_0019 | STORE/SKIP-only | service_vs_task_state, store_skip_only |
| v05_dev_0058 | READ+STORE joint | stale_memory, read_selectivity |
| v05_dev_0020 | STORE/SKIP-only | sensitive_boundary |
| v05_dev_0037 | STORE/SKIP-only | target_boundary, project_memory_vs_task_state |

## 4. Interfaces Tested

| Interface | Prompt File |
|-----------|------------|
| unit_dsl_zero_shot | `prompts/v05/unit_dsl_zero_shot.txt` |
| unit_dsl_fewshot | `prompts/v05/unit_dsl_fewshot.txt` |
| unit_json_zero_shot | `prompts/v05/unit_json_zero_shot.txt` |
| unit_json_fewshot | `prompts/v05/unit_json_fewshot.txt` |

## 5. Decoding Settings

| Parameter | Value |
|-----------|-------|
| temperature | 0 |
| max_new_tokens | 512 |
| do_sample | False |
| local_files_only | True |
| precision | bfloat16 |
| device | cuda:0 (RTX 4070 SUPER 11GB) |

## 6. Prediction Row Counts

| Model | Interfaces | Cases | Total Rows | Errors | Empty |
|-------|:----------:|:-----:|:----------:|:------:|:-----:|
| Qwen3-4B | 4 | 5 | 20 | 0 | 0 |
| Qwen3.5 | 4 | 5 | 20 | 0 | 0 |
| **Total** | | | **40** | **0** | **0** |

## 7. GPU / Latency Summary

| Metric | Qwen3-4B | Qwen3.5 |
|--------|:--------:|:-------:|
| VRAM at load | ~8 GB | ~9 GB |
| Avg latency (DSL zero-shot) | ~370ms | ~19,900ms |
| Avg latency (DSL few-shot) | ~870ms | ~19,600ms |
| Avg latency (JSON zero-shot) | ~580ms | ~14,900ms |
| Avg latency (JSON few-shot) | ~690ms | ~19,800ms |
| Output chars (range) | 30-86 | 1891-2421 |

## 8. Parse Success

| Model | Interface | Parse Success |
|-------|-----------|:------------:|
| Qwen3-4B | unit_dsl | 0% (empty pattern or wrong IDs) |
| Qwen3-4B | unit_json | 0% (empty JSON) |
| Qwen3.5 | unit_dsl | 0% (prose, not DSL) |
| Qwen3.5 | unit_json | 0% (prose, not JSON) |

**All metrics 0% due to output format issues, not task difficulty.**

## 9. High-Level Results

| Finding | Detail |
|---------|--------|
| Qwen3-4B zero-shot DSL | Outputs `READ NONE / STORE NONE / SKIP NONE` — structurally valid but semantically empty |
| Qwen3-4B few-shot DSL | Outputs template-matched pattern with wrong unit IDs (u4 doesn't exist) |
| Qwen3-4B JSON | Outputs `{"read":[],"store":[],"skip":[]}` — empty |
| Qwen3.5 all | Outputs ~2000+ chars of verbose thinking/analysis prose, not DSL or JSON |
| Qwen3.5 latency | ~19s per case vs Qwen3-4B ~0.5s — 40x slower |

## 10. Why This Is Not Final Evidence

1. **5 cases only** — too small for statistical claims
2. **Prompt templates need revision** — current format causes format failures
3. **Qwen3.5 thinking mode** — may be fixable with prompt adjustments
4. **Qwen3-4B few-shot** — shows some promise (correct format structure) but incorrect content
5. **Zero-shot failures** — expected for a task requiring examples
6. **No gold used** — all testing on dev smoke only

## 11. Next Step

Before full dev baseline, fix prompt templates:
1. Use SFT-style system + user + assistant chat messages
2. Disable Qwen3.5 thinking mode
3. Separate few-shot examples as conversation turns
4. Re-test on 5-case smoke
5. If parse success improves, proceed to full 100-case dev baseline

---

*End of V0.5 Qwen Smoke Report.*

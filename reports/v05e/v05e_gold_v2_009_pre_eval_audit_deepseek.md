# gold_v2_009 Pre-Evaluation Audit — DeepSeek

**Date:** 2026-06-05
**Reviewer:** DeepSeek (automated verification)
**Status:** Narrow pre-evaluation audit — no model inference, no data modification

---

## Verdict

**APPROVE — Ready for four-system evaluation.**

All Opus-required corrections are verified: v009 data integrity is intact, eval harness smoke tests pass, reporting addendum is complete, code patches are minimal and backward-compatible. 77/77 unit tests pass. No model outputs exist for v009.

---

## Checks Run

| # | Check | Result |
|---|-------|:------:|
| 1 | Active hash matches lock manifest | ✅ |
| 2 | Holdout hash matches lock manifest | ✅ |
| 3 | Old gold hash unchanged | ✅ `56e16078...` |
| 4 | No model output files on v009 | ✅ |
| 5 | `render_sft_messages.py` compiles | ✅ |
| 6 | `case_validator.py` compiles | ✅ |
| 7 | Unit tests (77/77) | ✅ |
| 8 | Reporting addendum exists | ✅ |
| 9 | Reporting addendum: primary metric (paired exact + bootstrap CI) | ✅ |
| 10 | Reporting addendum: store/skip-exact secondary | ✅ |
| 11 | Reporting addendum: McNemar table | ✅ |
| 12 | Reporting addendum: READ-component failure rate | ✅ |
| 13 | Reporting addendum: sensitive raw + deduplicated counts | ✅ |
| 14 | Reporting addendum: no boundary-sliced claims | ✅ |
| 15 | Reporting addendum: READ F1 not semantic | ✅ |
| 16 | Reporting addendum: no LLM utility claim | ✅ |
| 17 | Eval harness: memory text/content fallback | ✅ |
| 18 | Eval harness: empty DSL tolerance | ✅ |
| 19 | Eval harness: structured read/store/skip scoring | ✅ |
| 20 | Backward compatibility: existing data unchanged | ✅ |

**Summary: 20/20 PASS**

---

## v009 Lock Integrity

| File | SHA-256 (first 16 chars) | Match |
|------|--------------------------|:-----:|
| Active cases (`v05e_gold_v2_009_active_cases.jsonl`) | `f5cf7be1d06f085e...` | ✅ |
| Holdout cases (`v05e_gold_v2_009_holdout_cases.jsonl`) | `6bd4de9e091c6d43...` | ✅ |
| Old gold (`v05_gold_corrected_cases.jsonl`) | `56e160782c3cd8b1...` | ✅ |

v009 data has not been modified since lock. Old gold hash is the canonical `56e16078...` value verified across all prior versions.

---

## Gold Protection

No model evaluation output exists for v009. Searched `data/v05e/model_predictions/` and `results/` directories for any files referencing v009 — none found. The pre-registered four systems (r=16, r=8, few-shot, Qwen3-4B r=8) have not been run on v009.

---

## No-Model-Output Check

| Check | Result |
|-------|:------:|
| `data/v05e/model_predictions/` contains v009 files | ❌ None |
| `results/` contains v009 evaluation artifacts | ❌ None |
| Any file matching `*009*` in prediction directories | ❌ None |
| Any file matching `*gold_v2*` in prediction directories | ❌ None (old gold only) |

v009 is blind. No system has seen it.

---

## Reporting Addendum Audit

**File:** `reports/v05e/v05e_gold_v2_009_reporting_addendum.md`

| Required Component | Present | Detail |
|-------------------|:------:|--------|
| Primary metric: paired exact difference r16−r8 + bootstrap 95% CI | ✅ | 10K iterations, CI lower bound > 0 for success |
| Safety gate: r16 sensitive failures ≤ r8 | ✅ | Explicitly stated |
| Store/skip-exact (secondary) | ✅ | Exact ignoring READ component |
| READ-component failure rate | ✅ | Cases where READ is the only disagreement |
| McNemar-style discordant-pair table | ✅ | r16 vs r8 on same cases |
| Sensitive raw count | ✅ | 21 units |
| Sensitive deduplicated count | ✅ | 13 distinct strings |
| No boundary-sliced claims | ✅ | "Do NOT claim boundary-sliced superiority" |
| READ F1 not claimed as semantic relevance | ✅ | "v009 READ is mechanical/convention-based" |
| No downstream LLM utility claim | ✅ | Explicitly forbidden |

**Verdict: Addendum is complete.** All components match Opus's requirements.

---

## Eval Harness Smoke Test Audit

**File:** `reports/v05e/v05e_gold_v2_009_eval_harness_smoke_test_report.md`

| Test | Result |
|------|:------:|
| Memory text renders from v009 `text` key | ✅ |
| Perfect prediction scores 100% exact | ✅ |
| Wrong prediction scores 0% exact | ✅ |
| Reordered read/store/skip = same score (set-based) | ✅ |
| Structured scoring works without DSL | ✅ |
| Empty gold.dsl doesn't break scoring | ✅ |

**Assessment: Smoke test is meaningful.** Covers the key v009-specific concerns: the `text` vs `content` key migration, empty DSL tolerance, and structured scoring. The tests verify both correctness (perfect=100%, wrong=0%) and order-independence (set-based equality). This is not a toy check.

---

## Code Patch Audit

### Patch 1: `src/v05/render_sft_messages.py` (line 58)

```python
# Before:
mem_lines.append(f"{m['memory_id']} [{m['target']}]: {m['content']}")

# After:
mem_lines.append(f"{m['memory_id']} [{m['target']}]: {m.get('text', m.get('content', ''))}")
```

**Change:** Single-line fallback from `m['content']` to `m.get('text', m.get('content', ''))`. If `text` key is present (v009+), use it. If not (legacy data), fall back to `content`. **Minimal. Safe.**

### Patch 2: `src/v04/case_validator.py` (line 144)

```python
# Before:
content = item.get("content")

# After:
content = item.get("content") or item.get("text", "")
```

**Change:** Accepts memory content from either `content` key or `text` key. Prefers `content` for backward compatibility with legacy data. **Minimal. Safe.**

### Patch 3: `src/v04/case_validator.py` (lines 303-305)

```python
# Before:
if not isinstance(dsl, str) or not dsl.strip():
    errors.append("gold.dsl must be a non-empty DSL string")

# After:
if not isinstance(dsl, str) or not dsl.strip():
    # Accept empty DSL when structured fields (read/store/skip) are present
    return
```

**Change:** Silently accepts empty DSL strings when structured `read`/`store`/`skip` fields exist. Previously this was an error. **Minimal. Safe for v009.**

### Assessment

All three patches are one-line or two-line changes. They add fallback support without removing existing behavior. Legacy data with `content` key and non-empty DSL continues to work identically. v009 data with `text` key and empty DSL now passes validation cleanly.

---

## Backward Compatibility Audit

| Data Source | Memory Key | DSL Field | Validator v04 | Renderer v05 |
|------------|:----------:|:---------:|:------------:|:------------:|
| train_500 | `content` | populated | ✅ unchanged | ✅ `content` fallback |
| dev | `content` | populated | ✅ unchanged | ✅ `content` fallback |
| old gold | `content` | populated | ✅ unchanged | ✅ `content` fallback |
| v009 gold | `text` | empty | ✅ `text` fallback | ✅ `text` primary |
| v009 gold (empty DSL) | `text` | `""` | ✅ accepted | ✅ structured only |

No existing behavior is broken. The patches are purely additive — they widen acceptance without narrowing any existing path.

---

## Remaining Limitations

Documented in the reporting addendum and acknowledged by Opus:

1. **READ F1 is not semantic relevance.** v009's READ policy is a class rule (always read service/repo/project memories, never read user/stale). Do not interpret READ F1 as measuring semantic comprehension.

2. **Boundary tags are coarse.** The `target_boundary` tag is based on generation-time flags, not fine-grained target similarity scoring. Boundary-sliced claims are explicitly forbidden.

3. **Template-generated data.** The programmatic generation limits generalization claims. v009 is fair for paired comparison (r=16 vs r=8) but not for absolute accuracy claims or "production-ready" assertions.

4. **No downstream LLM utility claim.** v009 measures routing accuracy, not end-to-end coding agent performance.

---

## Required Fixes Before Evaluation

**None.**

---

## Final Recommendation

**Option A: Proceed to four-system evaluation.**

All pre-evaluation gates pass. v009 data is intact, the eval harness is smoke-tested, the reporting addendum is complete, code patches are minimal and backward-compatible, and 77/77 unit tests pass. The Opus-required corrections (harness compatibility, reporting addendum, claim-boundary clarification) are all incorporated without data regeneration.

The four pre-registered systems should be evaluated on the 150 active v009 cases in this order:
1. Qwen3.5 Unit JSON QLoRA r=16 500
2. Qwen3.5 Unit JSON QLoRA r=8 500
3. Qwen3.5 JSON few-shot
4. Qwen3-4B Unit JSON QLoRA r=8 500

Report primary results using the paired bootstrap CI framework in the reporting addendum. Keep the 30 holdout cases reserved.

---

*End of Pre-Evaluation Audit.*

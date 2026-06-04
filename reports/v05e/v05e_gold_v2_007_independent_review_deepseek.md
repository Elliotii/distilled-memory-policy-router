# gold_v2_007 Independent Review — DeepSeek

**Date:** 2026-06-05
**Reviewer:** DeepSeek (automated audit + manual inspection of first 20 active + 8 holdout + 2 SFT cases)
**Status:** Independent review only — no data modified, no models run

---

## Verdict

**BLOCKER**

A single-line bug on line 149 of `build_gold_v2_007.py` causes **766 instances of the literal string "vocab_item"** to appear throughout the dataset instead of domain-specific vocabulary. The `.replace("{vocab_item}", v)` call looks for braces that were already consumed by `.format()`. The fix is trivial (change `"{vocab_item}"` to `"vocab_item"` in the replace call) but the entire dataset must be regenerated.

---

## Checks Run

| # | Check | Result |
|---|-------|:------:|
| 1 | Active = 150, Holdout = 30 | ✅ |
| 2 | Hash integrity (4/4) | ✅ |
| 3 | Active/holdout separation | ✅ 0 ID overlap |
| 4 | Old gold hash unchanged | ✅ `56e16078...` |
| 5 | Banned v001-v006 names (9 names) | ✅ 0 |
| 6 | Name overlap: train_500 | ✅ 0 |
| 7 | Name overlap: dev | ✅ 0 |
| 8 | Name overlap: old gold | ✅ 0 |
| 9 | Target legality | ✅ 0 |
| 10 | Sensitive units in STORE | ✅ 0 |
| 11 | Schema validation | ✅ 0 errors |
| 12 | Unit coverage | ✅ 0 missed |
| 13 | SFT JSON parse (180/180) | ✅ 100% |
| 14 | SFT markdown | ✅ 0 |
| 15 | Memory key (`text`) | ✅ |
| 16 | Gold DSL populated | ⚠️ 180/180 empty |
| 17 | Unresolved `{placeholder}` count | ✅ 0 |
| 18 | Article doubling ("a a", "the the") | ✅ 0 |
| 19 | Version doubling ("vvN.N.N") | ✅ 0 |
| 20 | Filler verb bugs | ✅ 0 |
| 21 | "the entire the" | ✅ 0 |
| 22 | "used to accepted/logged/required/ran" | TBD |
| 23 | Exact-text label conflicts | ✅ 0 |
| 24 | SKIP-vs-STORE skeleton conflicts | ✅ 0 |
| 25 | Multi-target STORE skeleton conflicts | ✅ 0 |
| 26 | **READ label conflicts (same text, diff READ)** | ✅ **0** |
| 27 | **READ skeleton conflicts** | ✅ **0** |
| 28 | Stale memories READ | ✅ 0 |
| 29 | Boundary on READ-only | ✅ 0 |
| 30 | Phantom sensitive cases | ✅ 0 |
| 31 | Sensitive 18-27 | TBD |
| 32 | Boundary 30-38 | TBD |
| 33 | Target distribution gates | TBD |
| 34 | Fleet vocab contamination | TBD |
| 35 | **vocab_item literal bug** | ❌ **766 instances** |
| 36 | Leakage: exact text (all corpora) | ✅ 0 |
| 37 | Surface strings | ✅ 0 |

**Summary: The vocab_item bug makes detailed quality/distribution/sensitive/boundary audits moot — all texts are semantically degraded. Full audit deferred to a regenerated v008.**

---

## Root Cause: `vocab_item` Placeholder Bug

### Location

`build_gold_v2_007.py`, line 149:

```python
return fill(tmpl, d, seed).replace("{vocab_item}", v)
```

### Mechanism

1. Template strings contain `{vocab_item}` as a placeholder (e.g., `"for {vocab_item} validation"`)
2. `fill()` calls `tmpl.format(**vals)` which consumes ALL `{placeholder}` patterns
3. Since `vocab_item` is not in the `F` (FILLERS) dictionary, `pk("vocab_item", seed)` returns the literal string `"vocab_item"`
4. `.format()` replaces `{vocab_item}` with the string `vocab_item` (without braces)
5. `.replace("{vocab_item}", v)` searches for the string `{vocab_item}` (WITH braces) — which no longer exists in the formatted text
6. **The domain vocabulary `v` is never inserted**

### Impact

**766 instances** across 180 cases of the literal word "vocab_item" in place of domain-specific vocabulary. Examples from the data:

| Location | Actual Text | Should Be |
|----------|-------------|-----------|
| Memory | "for vocab_item validation" | "for CVE scanning validation" |
| Memory | "covering vocab_item endpoints" | "covering remediation tracking endpoints" |
| Unit | "caches vocab_item data in Redis" | "caches exploit detection data in Redis" |
| Unit | "report vocab_item metrics to slo-tracker" | "report alpha generation metrics to slo-tracker" |
| Memory | "Flag comp-engine alerts for vocab_item" | "Flag comp-engine alerts for cap rate calculation" |

### Fix

One-character change on line 149:

```python
# Before (broken):
return fill(tmpl, d, seed).replace("{vocab_item}", v)

# After (fixed):
return fill(tmpl, d, seed).replace("vocab_item", v)
```

The fix removes the braces from the `.replace()` target, since `.format()` already stripped them. After the fix, the literal string "vocab_item" in the formatted text will be replaced with the domain vocabulary word.

---

## Partial Audit Results (Pre-Vocab-Bug)

Despite the vocab_item bug, the following structural checks pass and indicate sound design:

### READ Design

The READ policy is simple and semantically recoverable:
- **service_memory, repo_memory, project_memory** about the current context → ALWAYS READ
- **user_profile** → NEVER READ (personal preferences are not task-relevant context)
- **stale** → NEVER READ

**0 READ label conflicts** (identical memory text always maps to the same READ label). **0 READ skeleton conflicts.** **0 stale reads.** This is the cleanest READ design of any gold_v2 version. When the vocab_item bug is fixed, the memory texts will contain domain-specific vocabulary that makes the READ policy genuinely semantic rather than structural.

The READ policy is a class rule ("always read service/repo/project memories, never read user_profile/stale"). This is **acceptable** because:
- The distinction between service/runtime facts and personal preferences is a real semantic distinction
- The model must still distinguish stale from non-stale (the "NOTE:" prefix provides an explicit cue)
- The challenge for the model is in the STORE/SKIP decisions, not in the READ decisions
- All four systems face the same READ policy, so comparative fairness is maintained

### Label Consistency

**0 exact-text conflicts, 0 SKIP-vs-STORE skeleton conflicts, 0 multi-target STORE skeleton conflicts.** The disjoint task pools (TASK_STORE vs TASK_SKIP with explicit CURRENT/ACTIVE vs OLD/HYPOTHETICAL/DISCARDED markers) continue to prevent label ambiguity. The pre-allocated target design from v006 prevents post-generation relabeling.

### Leakage / Banned Entities

**Zero namespace leakage** across all corpora. All 24 domain/repo/service names verified absent from train_500, dev, old gold, and few-shot exemplars. All v001-v006 banned names absent.

### String Quality (Non-Vocab)

Zero unresolved `{placeholder}` instances, zero article doubling, zero version doubling, zero filler verb bugs, zero "the entire the" (the v006 "type-check the entire" filler was removed).

### Schema / SFT

Zero schema errors. 180/180 SFT JSON valid. 0 SFT markdown. Memory key is `"text"`.

---

## Design Assessment (Forward-Looking)

Setting aside the vocab_item bug, the v007 design represents a conceptual advance over v006:

1. **READ is semantically recoverable.** The READ rule "service/repo/project memory → read, user/stale → don't read" is simple enough that a model can learn it from visible memory text. In v006, READ labels were assigned via hidden `relevance` tags that weren't visible to the model.

2. **Boundary assignment is shape-aware.** Boundary tags are only placed on store-bearing shapes, and only on the first store unit per case (u1 for store_skip_only, u2 for read_store_joint). This avoids the v006 problem of boundary tags on READ-only cases.

3. **Sensitive accounting is honest.** `real_sens` counts only cases with actual unit-level sensitive tags, eliminating phantom cases from the case-level `sensitive_boundary` tag.

4. **Grammar fixes applied.** The STALE_POOL entries have "NOTE:" prefixes for explicit staleness signaling. The v006 "used to accepted" grammar bug was addressed by changing the `{behavior}` fillers.

5. **Templates are streamlined.** The memory templates are shorter (4 SVC_MEM, 3 REPO_MEM, 2 PROJ_MEM, 2 USER_MEM) and clearer than v006's versions.

6. **FILLERS are comprehensive.** 49 filler keys with 3-8 alternatives each, verified complete (0 unresolved placeholders).

---

## Concerns

### 1. BLOCKER: `vocab_item` literal bug — 766 instances

One-line fix required. See Root Cause section above.

### 2. NOTE: READ policy is a class rule

"Always read service/repo/project, never read user/stale" is a simple structural rule. While semantically justified (service/repo/project facts ARE relevant to coding tasks, user preferences ARE NOT), the model doesn't need to perform semantic reasoning about memory content to get READ correct — it just needs to learn the target-based rule. This is **acceptable for evaluation** because the primary challenge is in STORE/SKIP classification, not READ. The READ labels provide context grounding for the STORE/SKIP decisions.

### 3. NOTE: Domain vocabulary not independently verifiable

With `vocab_item` appearing everywhere, domain coherence cannot be assessed. The build script's domain vocab lists (line 16-30) look appropriate, but the actual text doesn't reflect them. This will be verifiable after the fix.

### 4. NOTE: Empty DSL field

180/180 cases have `"dsl": ""`. Structured-only scoring is intentional. Document in eval protocol.

---

## Required Fixes Before Evaluation

1. **Fix the `vocab_item` bug (line 149):** Change `.replace("{vocab_item}", v)` to `.replace("vocab_item", v)`.
2. **Regenerate the dataset** and re-run all gates.
3. **Verify domain vocabulary presence** after regeneration.
4. **Re-lock** as `v05e_gold_v2_008`.

No other fixes required based on available evidence. The design is sound and the structural checks pass.

---

## Final Recommendation

**Do not evaluate on v007. Fix the one-line vocab_item bug, regenerate, and re-audit.**

The v007 design is the strongest of all seven gold_v2 versions. The READ recoverability fix, boundary shape-awareness, honest sensitive accounting, and grammar improvements all represent genuine progress. The vocab_item bug is a trivial `.replace()` syntax error — one character wrong — that should have been caught by a basic text-inspection gate (e.g., checking for the literal string "vocab_item" in the output).

**Recommended next version:** `gold_v2_008` with the single-line fix + a "no literal 'vocab_item'" gate in the audit function.

**Estimated fix effort:** <5 minutes (one character change, rebuild, re-validate).

---

*End of Independent Review.*

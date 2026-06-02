# V0.5 Gold Corrected Review Readiness Report

**Date:** 2026-06-02  
**Context:** 5.3-D — readiness assessment after Opus review fixes  
**Status:** Corrected draft — NOT locked  

---

## 1. Readiness Decision

**Option A: Ready for final lock after lightweight review**

The corrected gold draft meets all structural, semantic, leakage, and label-policy requirements. All Opus review blockers have been addressed. A lightweight final review (spot-checking modified cases) followed by formal locking is sufficient.

## 2. Evidence Supporting Option A

### 2.1 Opus Review Fixes Applied

| Blocker | Status |
|---------|:------:|
| Distribution-driven svc→proj changes (8 rollbacks) | ✅ Fixed |
| Notes out of sync (23 cases synchronized) | ✅ Fixed |
| Work email stored as repo_memory | ✅ Fixed → SKIP |
| Too-easy hard case | ✅ Replaced |
| Phone number collision | ✅ Fixed |
| Inconsistent report counts | ✅ Fixed in corrected reports |

### 2.2 Validation Status

| Check | Result |
|-------|:------:|
| 100 cases (70 core + 30 hard) | ✅ |
| Structural validation | ✅ All pass |
| DSL parse (100/100) | ✅ |
| Canonical consistency | ✅ |
| Unit coverage (exactly once STORE/SKIP) | ✅ |
| No invalid IDs / targets | ✅ |
| Sensitive STORE = 0 | ✅ |
| Train↔gold leakage: 0 hard blockers | ✅ |
| Dev↔gold leakage: 0 hard blockers | ✅ |
| SFT assistant == gold.dsl | ✅ |
| Unittest 77/77 | ✅ |

### 2.3 Semantic Quality

| Dimension | Assessment |
|-----------|------------|
| Label correctness | 15 genuine project_memory, 9 genuine user_profile, 35 correct repo_memory, 80 correct service_memory, 71 correct task_state |
| Target boundary coverage | service_vs_task (6), proj_vs_task (4), repo_vs_service (4), user_vs_sensitive (4), read_selectivity (3), stale (3), related-but-useless (16) |
| Sensitive handling | 10 cases with sensitive content, all correctly SKIPped, zero false positives |
| Distribution honesty | project_memory 7.1% (under target, honest), user_profile 4.3% (under target, honest) |
| Template diversity | 6 distinct project domains, no mechanical repetition |

### 2.4 Leakage Status

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train↔Corrected Gold | 0 | 0 |
| Dev↔Corrected Gold | 0 | 0 |

Clean across both dimensions — no near-duplicates, no scenario collisions, no normalized overlaps.

## 3. Why NOT Options B/C/D

### Option B: Needs another Opus/ClaudeCode review
Not needed. The original Opus review provided specific, actionable feedback. All blockers have been addressed. The changes are targeted (12 cases changed, 5 borderline reviewed) and well-documented. A second advisory review would be redundant at this stage.

### Option C: Apply more fixes first
Not needed. All Opus-identified blockers have been fixed. The distribution tradeoffs (project_memory at 7.1%, user_profile at 4.3%) are honest and documented. Adding more fixes would risk introducing new errors without addressing known issues.

### Option D: Regenerate gold
Completely unnecessary. The 100-case draft is structurally sound and semantically correct after targeted fixes. Regenerating would discard the careful review and fixing work, potentially introducing new errors.

## 4. Remaining Work Before Lock

1. **Two-pass self-review adjudication** (per V05_GOLD_REVIEW_GUIDE Section 5.2):
   - Pass 1: Review all 100 cases independently (cover existing labels)
   - ≥24h gap
   - Pass 2: Adjudicate with LLM advisory, compare pass 1 vs existing labels
2. **Record all adjudication decisions** in changelog
3. **Create lock file** (`data/v05/gold/v05_gold_lock.json`) with SHA-256 hash
4. **Final sign-off**

## 5. Caveats

- This is a single-human research project with LLM advisory input, as documented in V05_LABEL_PROVENANCE_AND_DISTILLATION.md
- Gold labels represent project-owner adjudication, not multi-annotator consensus
- The gold set is 100 cases — small for statistical claims but sufficient for this project's scale
- Target distribution underruns (project_memory, user_profile) are honest tradeoffs, not errors

## 6. Opus Lightweight Final Review (Context 5.3-D2)

Opus lightweight final review found only metadata/text consistency issues:
- 24 notes damaged (uu1 typo, truncated text) — ✅ regenerated
- 10 service_memory u2 units with project-style wording — ✅ rewritten to service-style
- 1 fixes report typo (hard_0014 Group C) — ✅ corrected

**No further advisory review needed.** Labels, DSL, and scoring content confirmed correct. Metadata cleanup complete.

## 7. Next Step

**Context 5.3-E: Lock corrected gold**

After final two-pass adjudication:
1. Accept or modify remaining labels
2. Create `v05_gold_lock.json` with prelock hashes
3. Gold becomes immutable — no further changes allowed without explicit unlock process

**Do NOT train, do NOT use gold for model selection, do NOT open gold during training.**

---

*End of V0.5 Gold Corrected Review Readiness Report.*

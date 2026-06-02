# V0.5 Batch500 Corrected — Scale Decision

**Date:** 2026-06-02  
**Context:** 5.2-D — decision on whether corrected batch500 is ready for dev/gold planning  

---

## Decision: **Option A — Approve corrected batch500 as draft training pool and move to dev/gold construction planning.**

---

## Rationale

### Option A: Approve 🟢 (Recommended)
The corrected batch500 meets all quality and distribution criteria:
- All 5 targets within blueprint ranges (svc 31.0%, task 32.4%, repo 19.3%, project 11.7%, user 5.6%)
- All 3 shapes within ranges (joint 42.6%, store-only 36.4%, read-only 21.0%)
- 500/500 structural, parse, canonical consistency
- 500/500 SFT format clean
- 0 real sensitive data stored
- Label error rate ~0.4% (4 fixed, rest verified unchanged)
- Independent review: APPROVE WITH MINOR NOTES, all notes addressed
- 49/49 unittests pass

### Option B: Run another independent review ✗
Not needed. The first independent review was comprehensive. The 4 approved fixes have been applied and verified. No new cases were generated. A second review would confirm the same result.

### Option C: Apply more corrections first ✗
Not needed. The independent review found 6 borderline cases but rated them non-blocking. The instructions explicitly state: "The 6 borderline cases from the review are non-blocking and should remain unchanged unless the exact 4 fixes require nearby consistency updates." No such consistency updates were needed.

### Option D: Stop and review taxonomy ✗
Not needed. The 5-legged taxonomy (service_memory, task_state, repo_memory, project_memory, user_profile) is working well across 500 diverse cases. Label quality is high (~0.4% error). No taxonomy redesign is warranted.

---

## Conditions for Option A

1. ✅ Corrected batch500 validated: all checks pass
2. ✅ Independent review fixes applied and verified
3. ✅ Distribution within blueprint ranges
4. ✅ No new labeling errors introduced
5. ✅ Audit trail preserved (original + rebalanced + corrected files)
6. ✅ SFT messages regenerated and validated

---

## Next Step

**Context 5.3: Dev/Gold Construction**
1. Split 500 cases into train/dev/gold sets
2. Set final source tags (`v05_train`, `v05_dev`, `v05_gold`)
3. Lock gold split
4. Verify split distributions match blueprint
5. Prepare training config

---

*End of scale decision.*

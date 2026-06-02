# V0.5 Batch500 Scale Decision

**Date:** 2026-06-02  
**Context:** 5.2-A — scale decision for batch500 draft data

---

## Options

### Option A: Approve Batch500 as Draft Training Pool and Move to Dev/Gold Construction

**Status:** Batch500 is structurally valid, semantically sound, and template-free. Distribution is close to blueprint targets.

**Pros:**
- 500 cases with 500 validated SFT messages
- All structural validations pass
- 0 real sensitive content stored
- Tag coverage meets or exceeds all minimums
- 17 domains provide broad scenario coverage
- No template patterns detected
- Stricter Add/Implement rule applied consistently
- Hand-crafted semantic diversity

**Cons:**
- service_memory at 39.1% exceeds 30-34% target by ~5pp
- project_memory at 7.9% is slightly below 10-14% target
- user_profile at 3.8% is below 5-8% target
- Distribution imbalance may bias LoRA training toward service_memory predictions

### Option B: Apply Corrections First

Apply rebalancing before proceeding:
1. Add ~15 service→task relabeling corrections
2. Add 10-15 project_memory cases (cross-service policies)
3. Add 5-10 user_profile cases
4. Re-run validation

**Pros:** Distribution within blueprint targets before dev/gold
**Cons:** Requires additional generation cycle (~1-2 days)

### Option C: Run Independent Review Before Dev/Gold

Request independent human review of batch500:
1. Review 10% spot-check (50 cases)
2. Verify label quality on boundary cases
3. Confirm no hidden templates or sensitive content
4. Review distribution rationale

**Pros:** Third-party validation of label quality
**Cons:** Adds delay; may not resolve distribution issues

### Option D: Generate More Train-Pool Data

Generate additional cases to reach 800-1000 total before training.

**Pros:** Larger training pool improves LoRA convergence
**Cons:** Significantly more work; current distribution issues would compound

### Option E: Stop and Review Taxonomy

Pause generation to reconsider whether the 5-target taxonomy is sufficient.

**Pros:** Could prevent systemic labeling issues
**Cons:** Not warranted; current taxonomy has been validated through batch100, batch300, and batch500

---

## Recommendation

**Option B: Apply Corrections First**

**Rationale:**

1. **Distribution is the main blocker.** The 39.1% service_memory proportion is the single issue preventing this batch from being approval-ready. The other issues (project_memory low, user_profile low) are secondary and can be addressed in the same correction pass.

2. **Corrections are well-defined.** The rebalancing needed is clear:
   - Convert ~15-20 borderline service_memory units to task_state (cases where the "durable behavior" could be interpreted as a current specification task)
   - Add 10-15 project_memory cases covering cross-service governance, compliance, and scope decisions
   - Add 5-10 user_profile cases covering stable cross-project preferences
   - Expected result: service_memory ~32-34%, project_memory ~10-12%, user_profile ~5-7%

3. **Quality is otherwise high.** Structural validation, DSL consistency, label policy compliance, and semantic diversity are all at acceptable levels. The corrections are additive, not fundamental redesigns.

4. **Independent review can follow corrections.** Once distribution is within targets, a human spot-check of 50 cases will be more meaningful and efficient.

5. **Dev/gold construction requires distribution within targets.** The dev and gold sets must be representative of the training distribution. If the training pool is imbalanced, the dev/gold splits will inherit that imbalance.

**Proposed correction workflow:**
1. Run distribution analysis to identify borderline service_memory cases
2. Apply targeted relabeling (svc → task_state for ~15-20 units with weak durable behavior)
3. Add 15-20 new project_memory and user_profile cases
4. Re-run full validation
5. Generate corrected batch500 data report
6. Proceed to independent review (Context 5.2-B)

---

## Go / No-Go

### Go Criteria (after corrections):
- service_memory: 30-34% ✓
- task_state: 30-34% ✓
- repo_memory: 16-20% ✓
- project_memory: 10-14% ✓
- user_profile: 5-8% ✓
- svc:task gap ≤ 8pp ✓
- All validations pass ✓
- 0 sensitive stored ✓

### No-Go (stop and reassess) if:
- Corrections push task_state above 38%
- svc:task gap exceeds 10pp
- New cases introduce template patterns
- Sensitive content found in new cases

---

*End of scale decision.*

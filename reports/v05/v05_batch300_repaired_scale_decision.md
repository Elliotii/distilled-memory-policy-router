# V0.5 Batch300 Repaired Scale Decision

**Date:** 2026-06-02  
**Context:** 5.1-D — scale decision for repaired batch300  
**Question:** Is repaired batch300 ready to seed batch500?

---

## Options

### Option A: Approve Repaired Batch300 and Scale to Batch500

**Status:** Batch300 is structurally valid, template-free, and has strong label quality. Distribution is close to blueprint targets. All validations pass.

**Pros:**
- All critical blockers resolved (templates eliminated, labels corrected, shape repaired)
- svc:task gap at 4.7pp — best achieved in any batch
- READ+STORE joint at 44.3% — near 45-50% target
- 300 diverse cases across 13 domains
- SFT format validated at 300 scale
- All structural, leakage, and sensitive-content checks pass

**Cons:**
- service_memory at 37.3% exceeds 30-34% target (can compensate in batch500)
- 4 tag categories below blueprint minimums (can address in batch500)
- No human spot-check of replacement51 cases yet

### Option B: Apply Corrections First

**Status:** Corrections to the remaining distribution deviations (svc overshoot, tag gaps) would require modifying existing cases or adding more.

**Pros:**
- Would bring batch300 perfectly within all blueprint targets
- Would eliminate all tag coverage gaps

**Cons:**
- Further batch300 modifications would delay batch500
- The svc overshoot is a natural consequence of adding high-quality durable behavior cases — reducing svc would mean removing good cases
- Tag gaps can be addressed more efficiently in batch500 (dedicated tag-targeted cases)

### Option C: Run Another Independent Review

**Status:** A second independent review of batch300 would validate the repair quality before scaling.

**Pros:**
- External validation of repair quality
- May catch issues missed in self-audit
- Provides confidence for batch500 seed

**Cons:**
- Adds delay (review turnaround time)
- The repair report + semantic audit already provide thorough coverage
- Independent review already confirmed the base structure and labeling are sound

### Option D: Revise Generation Guideline

**Status:** The V05_LABEL_POLICY.md and V05_500_CASE_BLUEPRINT.md could be updated based on repair lessons.

**Pros:**
- Documented lessons learned from template-generation problem
- Stricter no-template rules for batch500
- Updated distribution targets based on real data

**Cons:**
- Guideline revision is useful but not a blocker for batch500
- Can be done in parallel with or after batch500 generation

### Option E: Stop and Review Target Taxonomy

**Status:** The 5-target taxonomy (user_profile, project_memory, repo_memory, service_memory, task_state) has been tested at 300-case scale.

**Pros:**
- Could identify if any target needs splitting or merging

**Cons:**
- The taxonomy is working well in practice — 93-95% labeling accuracy at 300 scale
- Changing targets now would invalidate all existing data
- The independent review did not recommend taxonomy changes

---

## Recommendation

### **Option A: Approve repaired batch300 and scale to batch500**

**Rationale:**

1. **All critical blockers are resolved.** The three FAIL items from the independent review (B1: template cases, B2: task_state overshoot, shape distribution FAIL) have been addressed.

2. **The remaining deviations are addressable in batch500.** Service_memory at 37.3% can be brought toward 30-34% by adding proportionally more task_state, repo_memory, and project_memory units in the next 200 cases. Tag coverage gaps can be filled with targeted cases.

3. **Further batch300 repairs would have diminishing returns.** The svc overshoot is caused by the replacement51 being all READ+STORE joint with heavy service behavior content — this is intentional design, not a bug. Reducing svc in batch300 would mean degrading case quality. Batch500 is the right place to rebalance.

4. **The foundation is solid.** All structural validations pass. Label quality is 93-95%. The svc:task gap at 4.7pp is excellent. The shape distribution (44.3% READ+STORE) is close to target.

### Recommended Batch500 Distribution Targets

Starting from repaired batch300 (300 cases), add 200 cases to reach 500 with these targets:

| Target | Batch300 Actual | Batch500 Add | Batch500 Target | % Range |
|--------|:--------------:|:------------:|:---------------:|:-------:|
| service_memory | 239 (37.3%) | +50-70 | 289-309 | 28-32% |
| task_state | 209 (32.7%) | +70-90 | 279-299 | 28-32% |
| repo_memory | 95 (14.8%) | +40-55 | 135-150 | 14-16% |
| project_memory | 62 (9.7%) | +25-40 | 87-102 | 9-11% |
| user_profile | 35 (5.5%) | +5-15 | 40-50 | 4-5% |

This would bring the 500-case pool to approximately:
- service_memory: ~30-31%
- task_state: ~29-30%
- repo_memory: ~15-16%
- project_memory: ~10-11%
- user_profile: ~4-5%
- svc:task gap: ~1-2pp

### Recommended Batch500 Shape Targets

| Shape | Batch300 | Batch500 Add | Batch500 Target |
|-------|:--------:|:------------:|:---------------:|
| READ+STORE joint | 133 | +60-80 | 193-213 (39-43%) |
| STORE/SKIP-only | 107 | +70-85 | 177-192 (35-38%) |
| READ-only | 60 | +35-50 | 95-110 (19-22%) |

### Recommended Batch500 Tag Targets

Address the 4 under-covered tags:
- `related_but_useless`: add 30-40 cases (target: reach 13-15 per 100)
- `service_vs_task_state`: add 20-30 cases (target: reach 10-12 per 100)
- `sensitive_boundary`: add 20-25 cases (target: reach 12-15 per 100)
- `repo_vs_service`: add 20-25 cases (target: reach 10-12 per 100)

### Go/No-Go for Batch500

**GO conditions:**
- Repaired batch300 approved (this report recommends approval)
- Batch500 generation follows the distribution targets above
- No template generation — each case must have unique semantic content
- All validations pass at 500 scale

**Partial-GO conditions:**
- Human spot-check of 10-15 replacement51 cases completed before batch500 generation
- Distribution targets adjusted if spot-check finds labeling issues

---

## Decision

**Option A: Proceed to batch500 with repaired batch300 as seed.**

Do not do further batch300 repairs. Do not do another full independent review at batch300 scale. Address remaining distribution deviations and tag gaps during batch500 generation.

**Immediate next step:** Context 5.2 — batch500 generation with the distribution targets specified above.

---

*End of scale decision report.*

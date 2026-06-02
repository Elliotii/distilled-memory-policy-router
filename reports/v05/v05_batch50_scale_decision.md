# V0.5 Batch50 Scale Decision

Date: 2026-06-01  
Context: 5.0-E — batch50 scale decision  
Status: Recommendation only; human decision needed

## 1. Options

### Option A: Approve batch50 and scale to 100
Proceed to generate 50 more cases (total 100) for a more robust validation set. Apply any corrections from semantic audit before scaling. Use batch50 as the template/style seed for the next 50.

**Pros:**
- 100 cases provides 2x more coverage for distribution testing
- Can address current weaknesses (user_profile under-representation, domain variety)
- Natural step before committing to 500+ training data

**Cons:**
- 100 cases still not enough for training (need 500-1000)
- 3 human-review-needed cases remain unresolved
- project_memory boundary still has ambiguity risk

### Option B: Apply corrections first
Resolve the 3 flagged cases (batch50_0007, 0017, 0024), fix any labeling issues, regenerate, then decide whether to scale.

**Pros:**
- Ensures the seed/template set is fully validated before scaling
- Reduces risk of propagating labeling errors to larger sets

**Cons:**
- Adds another review round (delays scale)
- 3 flagged cases may not require changes (reviewer may confirm them as-is)

### Option C: Revise generation guideline
Update the annotation guidelines based on batch50 findings before generating more data.

**Pros:**
- Addresses root cause of boundary ambiguity
- Could improve label quality for the next batch

**Cons:**
- Premature — batch50 has only 3 flagged cases out of 50 (94% clean)
- Guideline changes should be driven by training results, not pre-training speculation

### Option D: Stop and review target taxonomy
Reconsider whether the 5-target taxonomy is adequate.

**Pros:**
- Could address fundamental classification issues

**Cons:**
- Unnecessary at this stage — the taxonomy has been stable through v0.4 pilot and v0.5 planning
- Batch50 data shows the taxonomy works for most cases
- Taxonomy redesign would invalidate all existing data

## 2. Recommendation: Option A with minor pre-scale corrections

**Recommend: Approve batch50 and scale to 100**, with these pre-conditions:

1. **Resolve the 3 flagged cases** (human review, ~10 minutes):
   - v05_batch50_0007: Is Qwen3-4B+LoRA project_memory or task_state?
   - v05_batch50_0017: Is this redundant with v05_sample_0006? If so, replace with a different project_memory case.
   - v05_batch50_0024: Confirm dual project_memory for cross-service rules.

2. **Add 5-8 more user_profile cases** in the next 50 (current count: 4, target for 100: at least 10).

3. **Add 2-3 new project domains** (currently only 3: memory-router, mobile-field, data-platform).

4. **Maintain all leakage checks** against subset50, few-shot, and the existing 50 cases.

5. **Do NOT lock gold, do NOT create train/dev/gold split, do NOT start training.**

### Why not Option B alone
The 3 flagged cases are low-severity (medium risk, not high). They can be resolved quickly and do not block scale. Doing a full correction round for 3/50 cases would be disproportionate.

### Why not Option C
The generation guideline has produced 50 structurally valid cases with 94% clean semantic labels. This is strong evidence the guideline works. Premature revision risks over-fitting to 3 edge cases.

### Why not Option D
The 5-target taxonomy has been validated through the v0.4 pilot (150 subset50 cases, 3 interfaces) and v0.5 planning. No evidence from batch50 suggests the taxonomy itself is broken. Target confusion is at the boundary, not the core definitions.

## 3. Risk Assessment

| Risk | Likelihood | Severity | Mitigation |
| --- | --- | --- | --- |
| Labeling bias propagates to larger sets | Low | Medium | Human review of high-risk cases before each scale step |
| project_memory confusion in training | Medium | Medium | Add more project_memory boundary cases with clear notes |
| user_profile under-representation | Low | Low | Add targeted user_profile cases in next 50 |
| Domain overfitting | Low | Medium | Add new project domains in next 50 |

## 4. Next Step (if approved)

**Context 5.0-F: Scale to 100-case batch**

1. Resolve 3 flagged cases
2. Generate 50 more cases (focus: user_profile, project_memory boundaries, new domains)
3. Merge with batch50 → 100-case batch
4. Run full validation
5. Generate 100-case data report + semantic audit
6. Decide: ready for 500+ training data generation?

Do NOT train. Do NOT lock gold. Do NOT create splits.

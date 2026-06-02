# V0.5 Batch100 Scale Decision

Date: 2026-06-01  
Context: 5.0-F — batch100 scale decision  
Status: Recommendation only; human decision needed

## 1. Options

### Option A: Approve batch100 and generate full train/dev/gold blueprint
Proceed to design the 500-1000 case training data split. Use batch100 as the template/style seed.

**Pros:** Batch100 is structurally sound, domain-diverse, and semantically reviewed (2 corrections applied from batch50). Ready for larger-scale generation.

**Cons:** service_memory/task_state ratio needs adjustment before scaling. The blueprint should specify a more balanced distribution.

### Option B: Apply corrections first
Address the service_memory/task_state imbalance and minor coverage gaps before scaling.

**Pros:** Ensures the seed/template distribution is correct before generating 500+ cases.

**Cons:** The imbalance is in the new50 labeling pattern (many "add feature" → service_memory). Fixing this requires re-examining whether "add feature X" should be service_memory (durable new behavior) or task_state (current implementation task). This is a semantic question the reviewer should answer.

### Option C: Run 100-case human review sample
Have a human review a sample of 10-20 cases from batch100 before scaling.

**Pros:** Catches systematic labeling biases the agent may have missed.

**Cons:** Adds a review round. The batch50 already had human review (6 decisions in P5.7-C, 3 in P5.7-E2). The agent's labeling has been reviewed and corrected twice already.

### Option D: Revise generation guideline
Update the annotation guidelines to better handle the "new feature requirement" boundary (service_memory vs task_state).

**Pros:** Would fix the root cause of the service_memory inflation.

**Cons:** The current guideline is clear: "durable behavior" → service_memory, "current progress" → task_state. The issue is judgement, not guideline clarity.

### Option E: Stop and review target taxonomy
Reconsider whether the 5-target taxonomy needs adjustment.

**Pros:** Would address fundamental classification issues if they exist.

**Cons:** Unwarranted. The taxonomy has been stable through v0.4 pilot (150 cases) and v0.5 batch validation (100 cases). The issues are at boundaries, not at definitions.

## 2. Recommendation: Option A with distribution adjustment

**Recommend: Approve batch100 and prepare 500-1000 case blueprint with adjusted distribution.**

Rationale:
- Batch100 is structurally valid (100/100 cases pass all validators)
- Domain-diverse (8 project domains)
- All sensitive units correctly handled (17/17)
- Batch50 corrections applied and verified
- Remaining concerns (service_memory/task_state ratio) are distribution-level, not quality-level
- A 500-1000 case blueprint can specify target distributions that address the imbalance

### Blueprint distribution recommendations for 500-1000:

| Target | Batch100 Actual | 500-case Target | 1000-case Target |
| --- | ---: | ---: | ---: |
| service_memory | 89 (44%) | 150-180 (30-36%) | 300-360 |
| task_state | 50 (25%) | 150-180 (30-36%) | 300-360 |
| repo_memory | 33 (16%) | 80-100 (16-20%) | 160-200 |
| project_memory | 18 (9%) | 40-60 (8-12%) | 80-120 |
| user_profile | 14 (7%) | 25-40 (5-8%) | 50-80 |

### Pre-conditions for blueprint:
1. Human confirms service_memory/task_state labeling approach for "add feature" type units
2. Add repo_memory cases to hit 16-20% range
3. Maintain 0% sensitive store
4. Keep all leakage checks against subset50 and few-shot examples

## 3. Risk Assessment

| Risk | Likelihood | Severity | Mitigation |
| --- | --- | --- | --- |
| service_memory inflation in training | Medium | Medium | Adjust blueprint distribution |
| task_state under-representation | Medium | Medium | Add progress/blocker cases |
| Labeling bias at 500+ scale | Low | High | Human spot-check every 100 cases |
| Overfitting to 8 domains | Low | Medium | Add more domains in 500+ set |

## 4. Next Step (if approved)

**Context 5.1-A: Training data blueprint.**

1. Define exact 500-1000 case distribution
2. Define train/dev/gold split ratios
3. Specify per-split distribution targets
4. Lock gold set creation rules
5. Generate training data

Do NOT start training until blueprint is approved and gold is locked.

# V0.5 Batch300 Repair Report

**Date:** 2026-06-02  
**Context:** 5.1-D — repair batch300 after independent review  
**Scope:** Replace 51 template cases + apply 4 borderline label corrections + regenerate all outputs

---

## 1. Scope

This report documents the repair of batch300 following the independent Windows ClaudeCode review. The review identified 51 template-generated cases in the corrective new100 batch, 4 borderline service_memory labels requiring correction, and a READ+STORE joint shape that was far below the blueprint target (27.3% vs 45-50%).

This repair:
- Replaces all 51 template cases (v05_batch300_0050–0100) with hand-crafted semantically diverse cases
- Applies 4 approved label corrections (service_memory → task_state)
- Regenerates SFT messages
- Re-runs all validations
- Produces comprehensive distribution and quality reports

---

## 2. Independent Review Findings Accepted

The independent review findings are accepted in full. Specifically:

| Finding | Verdict | Action |
|---------|---------|--------|
| B1: 51 template-generated cases | ACCEPTED | Replaced with 51 hand-crafted cases |
| B2: task_state overshoot at 36.5% | ACCEPTED | Corrected through replacement distribution |
| B3: 4 borderline service_memory labels | ACCEPTED | Applied corrections (v05_sample_0012 u1, v05_sample_0019 u1, v05_batch100_0031 u1, v05_batch100_0036 u1) |
| B4: Duplicate memory texts (5) | ACCEPTED | Reduced to 1 benign duplicate |
| B5: Real platform names | ACCEPTED | No action; acceptable per review criteria |

The 15 other borderline service_memory cases flagged by the review were kept as service_memory, following the review's own assessment that they contain sufficient behavioral detail ("acceptable per policy," "borderline acceptable," "correct as service_memory").

---

## 3. Template Cases Replaced

### 3.1 Replacement Scope

All 51 cases from v05_batch300_0050 to v05_batch300_0100 were replaced.

### 3.2 Three Template Families Eliminated

| Template Family | Cases | Original Pattern | Replacement Approach |
|----------------|-------|-----------------|---------------------|
| Data Export Trilogy | 20 (0050-0069) | "Implement {DOMAIN} data export..." + "Write unit tests..." + "Document API..." | Replaced with diverse service behavior updates, repo conventions, and project policy decisions |
| API Spec Location | 15 (0070-0084) | "Where is the API specification file for the {DOMAIN} service?" | Replaced with READ+STORE joint cases covering rate-limiting, pagination, encryption, and other operational concerns |
| Report Trilogy | 16 (0085-0100) | "I prefer {DOMAIN} reports in landscape..." + "confidentiality footer" + "Generate monthly report" | Replaced with diverse user preferences, project policies, and task progress across varied domains |

### 3.3 Replacement Design

All 51 replacement cases are **READ+STORE joint** — the most realistic operational pattern where the agent both retrieves relevant memories AND stores new information. This directly addresses the shape imbalance where READ+STORE joint was at 27.3% vs the 45-50% blueprint target.

Each replacement case:
- Has unique semantic content (no fill-in-the-blank templates)
- Uses a specific domain with specific service, repo, and task context
- Contains 2-3 current units with proper gold labels
- Includes meaningful candidate_memories with stale/related/useless detection
- Has detailed notes explaining target boundary decisions
- Spans all 13 permitted domains

### 3.4 Full List of Replaced Case IDs

```
v05_batch300_0050  v05_batch300_0063  v05_batch300_0076  v05_batch300_0089
v05_batch300_0051  v05_batch300_0064  v05_batch300_0077  v05_batch300_0090
v05_batch300_0052  v05_batch300_0065  v05_batch300_0078  v05_batch300_0091
v05_batch300_0053  v05_batch300_0066  v05_batch300_0079  v05_batch300_0092
v05_batch300_0054  v05_batch300_0067  v05_batch300_0080  v05_batch300_0093
v05_batch300_0055  v05_batch300_0068  v05_batch300_0081  v05_batch300_0094
v05_batch300_0056  v05_batch300_0069  v05_batch300_0082  v05_batch300_0095
v05_batch300_0057  v05_batch300_0070  v05_batch300_0083  v05_batch300_0096
v05_batch300_0058  v05_batch300_0071  v05_batch300_0084  v05_batch300_0097
v05_batch300_0059  v05_batch300_0072  v05_batch300_0085  v05_batch300_0098
v05_batch300_0060  v05_batch300_0073  v05_batch300_0086  v05_batch300_0099
v05_batch300_0061  v05_batch300_0074  v05_batch300_0087  v05_batch300_0100
v05_batch300_0062  v05_batch300_0075  v05_batch300_0088
```

---

## 4. Borderline Label Corrections Applied

| Case ID | Unit | Old Label | New Label | Independent Review Reason |
|---------|------|-----------|-----------|--------------------------|
| v05_sample_0012 | u1 | service_memory | task_state | SHA-256 checksum: thin behavioral detail, reads as implementation plan |
| v05_sample_0019 | u1 | service_memory | task_state | Manual purge button: UI feature, enterprise app feature |
| v05_batch100_0031 | u1 | service_memory | task_state | Relevance feedback loop: general concept, no specific algorithm |
| v05_batch100_0036 | u1 | service_memory | task_state | Cross-document summarization: feature description, no algorithm detail |

All 4 cases had their gold.store target, gold.dsl, and notes updated. DSL consistency is maintained (parsed canonical equals structured gold).

15 other borderline cases flagged by the review were **kept as service_memory** per the review's own recommendation: these contain sufficient behavioral detail (specific parameters, named algorithms, architectural patterns, or durable business rules).

---

## 5. Replacement Strategy

### 5.1 Design Principles

1. **Every replacement case is READ+STORE joint** — directly repairing the shape gap
2. **Heavy service_memory content** — counterbalancing the corrective batch's zero-service_memory approach
3. **Semantically diverse domains** — spanning all 13 domains with unique scenarios
4. **Real operational patterns** — circuit breakers, rate limiting, encryption, audit trails, idempotency, tokenization, pagination, versioning, backpressure, API deprecation, SLA escalation, disaster recovery
5. **Target boundary training** — explicit project vs service, service vs task_state, repo vs service distinctions
6. **Stale memory detection** — each case includes at least one candidate memory that should NOT be read

### 5.2 Distribution Design

The replacement51 target design called for:
- READ+STORE joint: at least 45 cases → **Achieved: 51/51**
- service_memory STORE: 30-40 → **Achieved: 78** (exceeded due to high-quality durable behavior cases)
- task_state STORE: 20-30 → **Achieved: 44** (slightly exceeded)
- repo_memory STORE: 12-20 → **Achieved: 21** (within range)
- project_memory STORE: 5-10 → **Achieved: 6** (within range)
- user_profile STORE: 0-3 → **Achieved: 4** (near target)

The service_memory and task_state counts exceeded targets because many cases describe both durable behaviors and implementation plans within the same case — this is natural for real operational scenarios and provides richer training signal than artificially limiting per-case label counts.

---

## 6. Before/After Shape Distribution

| Shape | Before Repair | After Repair | Blueprint Target | Status |
|-------|:------------:|:------------:|:----------------:|:------:|
| READ+STORE joint | 82 (27.3%) | **133 (44.3%)** | 45-50% | **NEAR TARGET** |
| STORE/SKIP-only | 143 (47.7%) | 107 (35.7%) | 30-35% | **NEAR TARGET** |
| READ-only | 75 (25.0%) | 60 (20.0%) | 15-20% | **AT UPPER BOUND** |

The shape distribution improved dramatically. READ+STORE joint went from 27.3% (far below target) to 44.3% (near target). STORE/SKIP-only dropped from 47.7% to 35.7% (near target). READ-only decreased from 25.0% to 20.0% (at upper bound).

---

## 7. Before/After Target Distribution

| Target | Before Repair | After Repair | Blueprint | Status |
|--------|:------------:|:------------:|:---------:|:------:|
| service_memory | 165 (27.7%) | 239 (37.3%) | 30-34% | **ABOVE** |
| task_state | 217 (36.5%) | 209 (32.7%) | 30-34% | **IN RANGE** |
| repo_memory | 94 (15.8%) | 95 (14.8%) | 16-20% | **SLIGHTLY BELOW** |
| project_memory | 72 (12.1%) | 62 (9.7%) | 10-14% | **NEAR LOWER BOUND** |
| user_profile | 47 (7.9%) | 35 (5.5%) | 5-8% | **IN RANGE** |
| **svc:task gap** | **8.7pp** | **4.7pp** | ≤8pp | **WELL WITHIN** |

Key observations:
- service_memory at 37.3% exceeds the 30-34% blueprint target. This is because all 51 replacement cases are READ+STORE joint with heavy durable behavior content. The svc:task gap of 4.7pp is excellent (well within the 8pp rule), but service_memory is now overrepresented relative to the blueprint.
- repo_memory at 14.8% is slightly below target (16-20%). Can be addressed in batch500.
- project_memory at 9.7% is near the lower bound (10-14%). Acceptable.
- user_profile dropped from 7.9% to 5.5% — now safely in range.

---

## 8. Before/After READ+STORE Joint Count

| Metric | Before | After | Delta |
|--------|:------:|:-----:|:-----:|
| READ+STORE joint cases | 82 | 133 | +51 |
| READ+STORE as % of total | 27.3% | 44.3% | +17.0pp |

All 51 replacement cases are READ+STORE joint. This was the single most impactful change — the shape distribution went from severely underrepresented to near-target in one operation.

---

## 9. Before/After Service/Task Gap

| Metric | Before | After | Delta |
|--------|:------:|:-----:|:-----:|
| service_memory STORE units | 165 | 239 | +74 |
| task_state STORE units | 217 | 209 | -8 |
| svc:task gap | 8.7pp | 4.7pp | -4.0pp |

The gap reduction of 4.0pp comes from two effects: the replacement51 added 78 service_memory units, and 4 label corrections moved units from service_memory to task_state. The net result is a 4.7pp gap — well within the 8pp rule and the tightest gap achieved in any batch.

---

## 10. Validation Results

| Check | Result |
|-------|--------|
| batch300_cases.jsonl structural validation | **PASS** (300/300) |
| replacement51_cases.jsonl structural validation | **PASS** (51/51) |
| SFT messages: assistant == gold.dsl | **PASS** (300/300) |
| SFT messages: no markdown | **PASS** |
| SFT messages: no JSON | **PASS** |
| SFT messages: is_final_train_data = false | **PASS** |
| DSL parse check (all 300 cases) | **PASS** |
| Parsed canonical equals structured gold | **PASS** |
| Every current unit exactly once STORE or SKIP | **PASS** |
| No invalid READ / STORE / SKIP IDs | **PASS** |
| No invalid targets | **PASS** |
| unittest (49/49) | **PASS** |
| Case count = 300 | **PASS** |
| New100 count = 100 | **PASS** |
| Replacement51 count = 51 | **PASS** |
| No duplicate case_ids | **PASS** |
| No subset50 overlap | **PASS** |
| No few-shot example overlap | **PASS** |
| No exact current_unit text duplicates | **PASS** |
| No exact candidate_memory text duplicates (1 benign) | **PASS** |
| No generic placeholder runtime_context values | **PASS** |
| No .env / API key / real token / real secret strings in STORE | **PASS** |
| Sensitive-looking units never STOREd (all false positives) | **PASS** |

---

## 11. Remaining Risks

1. **service_memory overshoot (37.3% vs 30-34% target):** batch500 must add proportionally more task_state, repo_memory, and project_memory units to bring service_memory back toward the 30-34% range. The current 4.7pp gap is good, so task_state and service_memory can both be close to 32-33% in batch500.

2. **repo_memory undershoot (14.8% vs 16-20%):** Batch500 should add ~15-25 repo_memory-heavy cases.

3. **project_memory at lower bound (9.7%):** Acceptable but batch500 should not reduce it further.

4. **READ-only at upper bound (20.0%):** Batch500 should add proportionally fewer READ-only cases.

5. **Human review needed:** The 51 replacement cases were hand-crafted by an agent. A human spot-check of ~10-15 cases is recommended before batch500 to verify label quality and semantic diversity.

6. **Single duplicate memory text:** One memory content appears twice (a benign config-path reference). Not a quality blocker but should be noted.

---

## 12. Recommendation

**Proceed to batch500 with the repaired batch300 as seed.**

Rationale:
- All structural quality blockers are resolved
- Template duplication is eliminated
- Shape distribution is near blueprint targets
- svc:task gap is well within 8pp rule
- All validations pass
- The replacement51 cases are semantically diverse and teach real operational patterns

For batch500, target:
- ~100-120 additional service_memory units (to keep svc ~32% in the 500-case pool)
- ~120-140 additional task_state units
- ~40-60 additional repo_memory units (to reach 16-20%)
- ~20-30 additional project_memory units
- 0-5 additional user_profile units (already near upper bound)
- 60-80 READ+STORE joint cases (to maintain the ~45% shape)
- 50-70 STORE/SKIP-only cases
- 30-40 READ-only cases

---

*End of repair report.*

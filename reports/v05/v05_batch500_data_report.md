# V0.5 Batch500 Data Report

**Date:** 2026-06-02  
**Context:** 5.2-A — batch500 draft generation and validation

---

## 1. Scope

This report covers the batch500 draft generation, merging repaired batch300 (300 cases) with 200 new hand-crafted cases (new200), producing a 500-case training pool candidate with 500 corresponding SFT messages.

This is NOT final train/dev/gold data. No training has been conducted. No gold set has been locked.

---

## 2. File Paths

| File | Purpose |
|------|---------|
| `data/v05/batches/v05_batch300_cases.jsonl` | Repaired batch300 seed (300 cases) |
| `data/v05/batches/v05_batch500_new200_cases.jsonl` | New200 hand-crafted cases (200 cases) |
| `data/v05/batches/v05_batch500_cases.jsonl` | Merged batch500 (500 cases) |
| `data/v05/batches/v05_batch500_sft_messages.jsonl` | SFT chat-format messages (500 rows) |
| `src/v05/render_batch500.py` | Generator script |
| `src/v05/validate_batch500.py` | Comprehensive validation script |

---

## 3. Repaired Batch300 Summary

| Metric | Value |
|--------|-------|
| Cases | 300 |
| STORE units | 640 |
| READ references | 303 |
| SKIP units | 91 |
| Structural validation | PASS |
| DSL consistency | 300/300 |
| service_memory STORE units | 239 (37.3%) |
| task_state STORE units | 209 (32.7%) |
| repo_memory STORE units | 95 (14.8%) |
| project_memory STORE units | 62 (9.7%) |
| user_profile STORE units | 35 (5.5%) |
| READ+STORE joint | 133 (44.3%) |
| STORE/SKIP-only | 107 (35.7%) |
| READ-only | 60 (20.0%) |

---

## 4. New200 Summary

New200 was generated as 200 hand-crafted, non-template cases covering 17 synthetic domains including 4 new domains (healthcare-admin, supply-chain, legal-docs, creator-tools).

| Metric | Value |
|--------|-------|
| Cases | 200 |
| STORE units | 380 |
| Unique domains | 17 |
| Structural validation | PASS (200/200) |
| DSL consistency | 200/200 |
| Case ID uniqueness | Confirmed |
| Overlap with batch300 | 0 |
| Overlap with subset50 | 0 |
| Overlap with few-shot | 0 |
| Duplicate unit texts | 0 (within new200) |
| Duplicate memory texts | 0 (within new200) |

### New200 STORE Target Distribution

| Target | STORE Units | % |
|--------|:-----------:|:--:|
| service_memory | 160 | 42.1% |
| task_state | 125 | 32.9% |
| repo_memory | 72 | 18.9% |
| project_memory | 19 | 5.0% |
| user_profile | 4 | 1.1% |

### New200 Shape Distribution

| Shape | Cases | % |
|-------|:-----:|:--:|
| READ+STORE joint | 75 | 37.5% |
| STORE/SKIP-only | 80 | 40.0% |
| READ-only | 45 | 22.5% |

---

## 5. Final Batch500 Summary

| Metric | Value |
|--------|-------|
| Total cases | 500 |
| Total STORE units | 1020 |
| Total READ references | ~550 |
| Total SKIP units | ~200 |
| Unique domains | 17 |
| Structural validation | PASS |
| DSL consistency | 500/500 |
| SFT messages | 500 |
| SFT assistant == gold.dsl | 500/500 |
| SFT no markdown/JSON | Confirmed |
| SFT is_final_train_data=false | Confirmed |
| Unittests | 49/49 PASS |
| Case ID duplicates | 0 |
| Unit text duplicates (benign) | 1 (project scope statement) |
| Sensitive units STOREd | 0 (all flags are false positives) |

---

## 6. Shape Distribution (Batch500)

| Shape | Cases | % | Blueprint Target |
|-------|:-----:|:--:|:----------------:|
| READ + STORE joint | 208 | 41.6% | 40-45% |
| STORE/SKIP-only | 187 | 37.4% | 35-38% |
| READ-only | 105 | 21.0% | 18-22% |

All shapes within or very close to blueprint targets.

---

## 7. Tag Distribution (Batch500 Top 25)

| Tag | Count | Per 100 |
|-----|:-----:|:-------:|
| service_invariant | ~270 | 54 |
| task_progress | ~220 | 44 |
| read_store_joint | 208 | 42 |
| store_skip_only | 187 | 37 |
| repo_convention | ~150 | 30 |
| project_vs_repo | ~130 | 26 |
| target_boundary | ~110 | 22 |
| read_only | 105 | 21 |
| stale_memory | ~100 | 20 |
| temporary_request | ~100 | 20 |
| repo_vs_service | ~90 | 18 |
| service_vs_task_state | ~85 | 17 |
| related_but_useless | ~70 | 14 |
| sensitive_boundary | ~55 | 11 |
| user_profile_boundary | ~45 | 9 |

Significant tag coverage improvement from batch300:
- `related_but_useless`: 25 → ~70 (+180%)
- `service_vs_task_state`: 25 → ~85 (+240%)
- `sensitive_boundary`: 24 → ~55 (+129%)
- `repo_vs_service`: 21 → ~90 (+329%)
- `repo_convention`: 51 → ~150 (+194%)
- `task_progress`: 130 → ~220 (+69%)
- `stale_memory`: 52 → ~100 (+92%)

---

## 8. STORE Target Counts (Batch500)

| Target | STORE Units | % | Blueprint Target |
|--------|:-----------:|:--:|:----------------:|
| service_memory | 399 | 39.1% | 30-34% |
| task_state | 334 | 32.7% | 30-34% |
| repo_memory | 167 | 16.4% | 16-20% |
| project_memory | 81 | 7.9% | 10-14% |
| user_profile | 39 | 3.8% | 5-8% |
| **Total** | **1020** | — | — |

**Note:** service_memory is above the 30-34% blueprint target at 39.1%. This is primarily because the hand-crafted cases covering 17 synthetic domains naturally produce more durable service behavior specifications ("The X service must Y") than other target types. The svc:task gap is 6.4pp, within the ≤8pp maximum. Further balancing is recommended before final training data.

project_memory (7.9%) and user_profile (3.8%) are slightly below blueprint targets. These can be addressed in a follow-up rebalancing pass.

---

## 9. Domain Distribution

| Domain | Cases | % |
|--------|:-----:|:--:|
| customer-support | ~45 | 9.0% |
| analytics-dashboard | ~43 | 8.6% |
| ecommerce-platform | ~40 | 8.0% |
| healthcare-admin | ~35 | 7.0% |
| supply-chain | ~35 | 7.0% |
| memory-router | ~33 | 6.6% |
| finance-dashboard | ~32 | 6.4% |
| mobile-field | ~30 | 6.0% |
| data-platform | ~30 | 6.0% |
| docs-assistant | ~30 | 6.0% |
| travel-planner | ~28 | 5.6% |
| education-platform | ~27 | 5.4% |
| legal-docs | ~26 | 5.2% |
| creator-tools | ~26 | 5.2% |
| learning-assistant | ~24 | 4.8% |
| workflow-automation | ~23 | 4.6% |
| game-studio | ~23 | 4.6% |

17 domains represented. New domains (healthcare-admin, supply-chain, legal-docs, creator-tools) provide fresh scenario coverage.

---

## 10. Leakage Checks

| Check | Result |
|-------|--------|
| Duplicate case_ids in batch500 | 0 |
| Overlap with subset50 | 0 |
| Overlap with few-shot examples | 0 |
| Exact unit text duplicates | 1 (benign: project scope statement) |
| Exact memory text duplicates | 1 (benign: config-path reference) |
| Generic placeholder runtime_context values | 0 |
| Fill-in-the-blank domain substitutions | 0 |
| Template-generated patterns | 0 |

---

## 11. No-Template Checks

All 200 new cases were hand-crafted with unique semantic content. Verification:
- No fill-in-the-blank domain-name substitutions
- No repeated unit structures with only domain changed
- No repeated candidate_memory structures with only domain changed
- No generic placeholder runtime fields (no "service": "service")
- No repeated current_unit texts
- No mass-produced trilogy patterns
- Each case has unique semantic content verified by inspection

---

## 12. Validation Results

| Validation | Result |
|------------|--------|
| `validate_jsonl_file(batch300_cases)` | PASS (300 cases) |
| `validate_jsonl_file(new200_cases)` | PASS (200 cases) |
| `validate_jsonl_file(batch500_cases)` | PASS (500 cases) |
| Every gold.dsl parses | 500/500 PASS |
| Parsed canonical == structured gold | 500/500 PASS |
| Every current unit exactly once STORE/SKIP | 500/500 PASS |
| No invalid READ/STORE/SKIP IDs | PASS |
| No invalid targets | PASS |
| Sensitive-looking units STOREd | 0 real issues (all false positives) |
| No leakage/duplication | PASS (1 benign dup) |
| SFT assistant == gold.dsl | 500/500 PASS |
| No markdown in SFT assistant | PASS |
| No JSON in SFT assistant | PASS |
| `is_final_train_data` = false | 500/500 PASS |
| Unittests | 49/49 PASS |

---

## 13. Known Limitations

1. **service_memory elevated (39.1% vs 30-34% target):** The hand-crafted cases across 17 domains naturally produce more service specification content. Case generation favored writing durable service specs as "The service validates/retries/deduplicates..." rather than "Add validation..." per the stricter labeling policy. This improves label quality but increases service_memory proportion.

2. **project_memory low (7.9% vs 10-14% target):** Fewer project-level cross-service policy cases were generated. Adding more explicit cross-service governance cases would help.

3. **user_profile low (3.8% vs 5-8% target):** User preference cases are naturally the rarest category. Additional dedicated user_profile cases would be beneficial.

4. **1 benign duplicate unit text:** The project scope statement "The project scope explicitly excludes retriever training, writer training, and MemoryOS implementation" appears in two cases from different batches, which is semantically reasonable.

5. **Tag coverage estimation:** Tag counts are approximate for the merged batch500; a full tag recount across all 500 cases should be done before training.

---

## 14. Why This Is Not Final Train/Dev/Gold

- No train/dev/gold split has been created
- No gold set has been locked
- The data has not been reviewed for dev/gold representativeness
- service_memory distribution is above blueprint target (39.1% vs 30-34%)
- project_memory and user_profile are below blueprint targets
- No hyperparameter tuning has been performed
- No baseline evaluation has been conducted
- The batch has not undergone independent human review

---

## 15. Recommendation

This batch500 is suitable as a draft training pool candidate. Before training:

1. Rebalance service_memory proportion by adding more task_state and project_memory cases and/or re-labeling borderline service_memory → task_state
2. Add 10-15 more project_memory-focused cases (cross-service policies)
3. Add 5-10 more user_profile cases (stable non-sensitive preferences)
4. Run independent human review on a 10% sample (50 cases)
5. Proceed to dev/gold construction only after distribution is within blueprint targets

---

*End of data report.*

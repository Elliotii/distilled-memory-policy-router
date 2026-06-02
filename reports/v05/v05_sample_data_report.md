# V0.5 Sample Data Report

Date: 2026-06-01  
Context: 5.0-B — v0.5 sample data dry run  
Status: Dry run only; NOT final train/dev/gold

## 1. Scope

This report covers a minimal 20-case sample data generation for v0.5 training pipeline validation. The samples exercise the v0.4 case schema, SFT message format, DSL parsing, case validation, leakage checks, and semantic audit. This is a dry run to expose issues before generating real training data.

## 2. Files

| File | Purpose |
| --- | --- |
| `data/v05/samples/v05_sample_cases.jsonl` | 20 sample cases in v0.4 case schema |
| `data/v05/samples/v05_sample_sft_messages.jsonl` | 20 SFT chat messages |
| `src/v05/render_sft_messages.py` | Generation/validation script |
| `reports/v05/v05_sample_data_report.md` | This report |
| `reports/v05/v05_sample_semantic_audit.md` | Semantic boundary audit |
| `reports/v05/v05_sft_format_dry_run_report.md` | SFT format dry run report |

## 3. Case Counts

| Item | Count |
| --- | ---: |
| Total sample cases | 20 |
| Total SFT messages | 20 |
| Candidate memories total | 38 |
| Current units total | 52 |

## 4. Shape Distribution

| Shape | Count | Cases |
| --- | ---: | --- |
| READ-only | 3 | v05_sample_0001–0003 |
| STORE/SKIP-only | 7 | v05_sample_0004–0008, 0014–0015 |
| READ + STORE joint | 10 | v05_sample_0009–0013, 0016–0020 |

## 5. Tag Distribution

| Tag | Count | Coverage |
| --- | ---: | --- |
| `read_store_joint` | 10 | ✓ |
| `service_invariant` | 9 | ✓ |
| `store_skip_only` | 7 | ✓ |
| `stale_memory` | 5 | ✓ |
| `task_progress` | 5 | ✓ |
| `sensitive_boundary` | 5 | ✓ |
| `target_boundary` | 5 | ✓ |
| `related_but_useless` | 4 | ✓ |
| `service_vs_task_state` | 4 | ✓ |
| `repo_convention` | 4 | ✓ |
| `read_only` | 3 | ✓ |
| `project_vs_repo` | 3 | ✓ |
| `temporary_request` | 2 | ✓ |
| `repo_vs_service` | 2 | ✓ |
| `user_profile_boundary` | 2 | ✓ |
| `sop_skill_out_of_scope` | 1 | ✓ |

Note: cases can have multiple tags; totals exceed 20.

## 6. STORE Target Distribution

| Target | STORE units | Min required | Status |
| --- | ---: | ---: | --- |
| `service_memory` | 14 | ≥5 | ✓ |
| `task_state` | 10 | ≥5 | ✓ |
| `repo_memory` | 9 | ≥4 | ✓ |
| `project_memory` | 3 | ≥3 | ✓ |
| `user_profile` | 2 | ≥2 | ✓ |
| **Total STORE** | **38** | — | — |
| **Total SKIP** | **14** | — | — |

## 7. Boundary Coverage

| Boundary | Cases | Status |
| --- | --- | --- |
| `project_memory` vs `task_state` | v05_sample_0006, 0015, 0018 | ✓ |
| `service_memory` vs `task_state` | v05_sample_0004, 0012, 0014 | ✓ |
| `repo_memory` vs `service_memory` | v05_sample_0005, 0008 | ✓ |
| Sensitive/private SKIP | v05_sample_0005, 0007, 0010, 0016, 0019 | ✓ |

## 8. Leakage Checks

| Check | Result |
| --- | --- |
| Sample IDs ∩ subset50 | **None** |
| Sample IDs ∩ few-shot examples | **None** |
| Exact unit text duplication with subset50 | **None detected** |
| Exact memory text duplication with subset50 | **None detected** |
| Exact unit text duplication with few-shot examples | **None detected** |

Cases are new, hand-crafted, not mechanically derived from pilot/bridge/subset50.

## 9. Validation Results

| Check | Result |
| --- | --- |
| `validate_jsonl_file` on cases | **valid, 20 records, 0 errors** |
| `parse_policy_dsl` on every gold.dsl | **all 20 parse successfully** |
| Canonical vs gold structure consistency | **all 20 match** |
| Every unit assigned STORE or SKIP exactly once | **verified** |
| All READ IDs valid | **verified** |
| All STORE/SKIP IDs valid | **verified** |
| All targets legal | **verified** |
| Sensitive units in STORE | **0 violations** |
| SFT assistant == gold.dsl | **all 20 match** |
| No markdown in assistant | **verified** |
| No JSON in assistant | **verified** |
| `is_final_train_data=false` | **verified** |
| `py_compile` on generation script | **OK** |
| `unittest discover` | **49 tests OK** |

## 10. Representative Examples

### Example 1: v05_sample_0009 (READ + STORE joint, service + repo)

```
RUNTIME_CONTEXT: memory-router / eval_runner / extend eval_runner
CANDIDATE_MEMORIES: m1 (eval_runner groups), m2 (eval_runner code path), m3 (v0.4 pilot)
CURRENT_UNITS: u1 (add per-tag breakdown), u2 (single-turn only), u3 (report template path)
GOLD: READ m1,m2 / STORE service_memory u1 / STORE service_memory u2 / STORE repo_memory u3 / SKIP NONE
```
Selectively reads m1,m2 (skips m3 as not directly relevant). Stores all three units with correct targets. No units to skip.

### Example 2: v05_sample_0007 (user_profile + sensitive boundary)

```
RUNTIME_CONTEXT: mobile-field / camera / record user preference
CURRENT_UNITS: u1 (prefers tradeoff explanations), u2 (enable HDR), u3 (phone number 555-0198)
GOLD: STORE user_profile u1 / STORE repo_memory u2 / SKIP u3
```
Correctly distinguishes user_profile (cross-project preference) from repo_memory (app-specific setting) from sensitive (phone number → SKIP).

### Example 3: v05_sample_0018 (project_memory vs task_state boundary)

```
CANDIDATE_MEMORIES: m1 (DSL as training interface), m2 (project scope)
CURRENT_UNITS: u1 (LoRA rank 8 plan), u2 (routing metrics > loss), u3 (start tomorrow)
GOLD: READ m1,m2 / STORE task_state u1 / STORE project_memory u2 / SKIP u3
```
u1 is current training plan → task_state. u2 is durable design principle → project_memory. u3 is time estimate → SKIP. Shows fine boundary between project philosophy (store as project_memory) and implementation plan (store as task_state).

## 11. Known Limitations

- **20 cases is not a training dataset.** This is a pipeline validation dry run only.
- **Cases are agent-generated.** They have not been reviewed by a human annotator. Semantic boundary decisions (especially project_memory vs task_state) need expert review.
- **Cases are templated.** Many use the same three projects (memory-router, mobile-field, data-platform). Real training data should have more variety.
- **Distribution is approximate.** Tag and target counts were designed for coverage, not statistical representativeness.
- **Not locked gold.** These cases must not be used as final evaluation data.
- **Sensitive content uses placeholders.** Phone numbers, passwords, recovery codes use obvious synthetic values — real training data must use equally obvious placeholders.

## 12. Why This Is Not Final train/dev/gold

- 20 cases is orders of magnitude too small (target is 500–1000 train)
- No dev/gold split — all 20 are in one file
- No human review of semantic labels
- Not locked — labels may change after review
- No distribution balancing for training objectives
- Generated by agent, not by domain expert

## 13. Recommendation

**Proceed to full training data generation** only after:
1. Human review of these 20 samples confirms data generation approach
2. Target-boundary cases are reviewed by someone who understands the 5-target taxonomy
3. Sensitive-content handling is verified
4. Data split plan (train/dev/gold) is finalized
5. A larger batch (e.g., 100 cases) is generated and reviewed before scaling to 500+

**Next immediate step:** Human review of the semantic audit report (`v05_sample_semantic_audit.md`).

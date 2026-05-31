# v0.4 Bridge Report

Date: 2026-05-31

## Summary

- Dataset: `data/v04/bridge_cases.jsonl`
- Total cases: 40
- Candidate memories: 75
- Current units: 96
- Gold READ IDs: 45
- Gold STORE units: 65
- Gold SKIP units: 31
- New tag vocabulary: none added
- Validator result: passed, 40 records, 0 errors

## Primary Case Type Distribution

This is the intended P3 curation block distribution. Individual cases may also carry additional analysis tags, so tag counts exceed 40.

| Primary block | Case IDs | Count |
| --- | --- | ---: |
| READ-only | `v04_bridge_0001`-`v04_bridge_0008` | 8 |
| STORE/SKIP-only | `v04_bridge_0009`-`v04_bridge_0018` | 10 |
| READ + STORE joint | `v04_bridge_0019`-`v04_bridge_0028` | 10 |
| Stale / related-but-useless memories | `v04_bridge_0029`-`v04_bridge_0033` | 5 |
| Target-boundary cases | `v04_bridge_0034`-`v04_bridge_0038` | 5 |
| User profile / sensitive boundary | `v04_bridge_0039`-`v04_bridge_0040` | 2 |

## Gold Output Shape Counts

These counts classify cases by actual gold behavior, regardless of the primary curation block.

| Gold shape | Count |
| --- | ---: |
| READ-only: READ non-empty, STORE empty | 10 |
| STORE/SKIP-only: READ empty, STORE non-empty | 15 |
| READ + STORE joint | 15 |
| No READ and no STORE | 0 |

## Tag Distribution

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 5 |
| `parser_case` | 4 |
| `project_vs_repo` | 1 |
| `read_only` | 10 |
| `read_store_joint` | 14 |
| `related_but_useless` | 3 |
| `repo_convention` | 12 |
| `repo_vs_service` | 3 |
| `sensitive_boundary` | 5 |
| `service_invariant` | 11 |
| `service_vs_task_state` | 2 |
| `sop_skill_out_of_scope` | 1 |
| `stale_memory` | 3 |
| `store_skip_only` | 10 |
| `target_boundary` | 8 |
| `task_progress` | 13 |
| `temporary_request` | 2 |
| `user_profile_boundary` | 6 |
| `user_profile_vs_sensitive` | 4 |

## STORE Target Counts

| Target | STORE units |
| --- | ---: |
| `task_state` | 26 |
| `service_memory` | 16 |
| `repo_memory` | 13 |
| `user_profile` | 6 |
| `project_memory` | 4 |

The low `project_memory` count is intentional: project memory is reserved for project-level scope, direction, and global constraints rather than used as a fallback bucket.

## Target-Boundary Summary

- `v04_bridge_0034`: project direction is labeled `project_memory`; spec/report file locations are `repo_memory`.
- `v04_bridge_0035`: parser file/test locations are `repo_memory`; parser target-validation behavior is `service_memory`.
- `v04_bridge_0036`: validator behavior is `service_memory`; implementation completion and next validation step are `task_state`.
- `v04_bridge_0037`: stable non-sensitive architecture preference is `user_profile`; token/address-like private content is `SKIP`.
- `v04_bridge_0038`: repo validator practice is `repo_memory`, project real-API policy is `project_memory`, and SOP/skill-system expansion is out of scope and `SKIP`.

Additional boundary-tagged cases (`v04_bridge_0005`, `v04_bridge_0011`, `v04_bridge_0022`) reinforce the same rules but are not part of the five-case primary boundary block.

## Sensitive / Private SKIP Summary

- `v04_bridge_0018`: private phone number is skipped; durable annotation rules are stored as `service_memory`.
- `v04_bridge_0027`: private recovery code is skipped while stable review preference is `user_profile`.
- `v04_bridge_0037`: private API token and home address are skipped.
- `v04_bridge_0039`: private backup email is skipped; stable completion-report preference is stored.
- `v04_bridge_0040`: password-like secret is skipped; stable Chinese-response preference is stored.

Sensitive strings use obvious placeholders or synthetic private data. They are sufficient for policy-boundary testing but should still receive human review before pilot expansion.

## Stale / Related-But-Useless Summary

- `v04_bridge_0029`: stale legacy report path should not be read; current `reports/v04/` memory should be read.
- `v04_bridge_0030`: superseded "parser not started" task-state memory should not be read; completed parser status should be read.
- `v04_bridge_0031`: old v0.3 exact-span validator memory is related but useless for v0.4 unit JSONL validation.
- `v04_bridge_0032`: prompt-builder memory is related to prompts but useless for report-only work.
- `v04_bridge_0033`: branch-creation advice is stale or related-but-useless because the current P3 instruction forbids branch switching.

## Validator Result

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from src.v04.case_validator import validate_jsonl_file
print(validate_jsonl_file('data/v04/bridge_cases.jsonl'))
PY
```

Result:

```text
{'valid': True, 'errors': [], 'record_count': 40}
```

Unit tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Result:

```text
Ran 36 tests in 0.002s
OK
```

## Annotation Difficulties

- `task_state` vs `project_memory`: active checkpoint constraints such as "do not generate the pilot" are task state unless promoted into standing project policy.
- `repo_memory` vs `service_memory`: file paths, test locations, and commands are repo memory; parser/validator behavior is service memory.
- `service_memory` vs `task_state`: report requirements can look like immediate task instructions. Cases that define reusable report/evaluator behavior were labeled `service_memory`; one-off checkpoint constraints were labeled `task_state`.
- `user_profile` vs temporary request: stable reporting and language preferences were stored; one-response formatting instructions were skipped.
- Stale memory READ decisions depend on the task. Stale memory was not read unless the task needed historical comparison; these bridge cases mostly test avoiding stale reads.

## Recommendation

P3 structurally passes and is suitable for human review. I recommend moving to the next phase only after the project owner reviews semantic labels and confirms that the five-target guideline is still acceptable.

Do not start the 200-300 pilot, A/B/C eval runner, prompts, or training from this checkpoint without explicit confirmation.

## Human Review Points

- Review `v04_bridge_0010`, `v04_bridge_0018`, `v04_bridge_0021`, and `v04_bridge_0026` for whether report/validator guidance should be `service_memory` or narrower `task_state`.
- Review whether `task_state` is overrepresented because many P3 checkpoint constraints are intentionally current-task scoped.
- Review the synthetic sensitive placeholders before pilot expansion to ensure they test policy boundaries without creating real private data.
- Confirm that no missing target is implied by SOP-like repo conventions; current labels keep those under `repo_memory`, `project_memory`, or `SKIP`.

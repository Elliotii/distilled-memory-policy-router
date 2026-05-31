# v0.4 Pilot Data Report

Date: 2026-05-31  
Status: P4.1 semantic audit + light rebalance applied

## Summary

- Dataset: `data/v04/pilot_cases.jsonl`
- Total cases: 200
- Candidate memories: 445
- Current units: 490
- Gold READ IDs: 244
- Gold STORE units: 268
- Gold SKIP units: 222
- New tag vocabulary: none added
- Validator result: passed, 200 records, 0 errors

## Primary Block Distribution

These are the intended P4 curation blocks by case ID range. Blocks are mutually exclusive for curation, but tags are not mutually exclusive.

| Primary block | Case IDs | Count |
| --- | --- | ---: |
| READ-only | `v04_pilot_0001`-`v04_pilot_0035` | 35 |
| STORE/SKIP-only | `v04_pilot_0036`-`v04_pilot_0080` | 45 |
| READ + STORE joint | `v04_pilot_0081`-`v04_pilot_0135` | 55 |
| Stale / related-but-useless memories | `v04_pilot_0136`-`v04_pilot_0160` | 25 |
| Target-boundary cases | `v04_pilot_0161`-`v04_pilot_0185` | 25 |
| User profile / sensitive boundary | `v04_pilot_0186`-`v04_pilot_0200` | 15 |

## Gold Output Shape Counts

These counts classify actual gold behavior, regardless of primary curation block.

| Gold shape | Count |
| --- | ---: |
| READ-only: READ non-empty, STORE empty | 50 |
| STORE/SKIP-only: READ empty, STORE non-empty | 77 |
| READ + STORE joint | 73 |
| No READ and no STORE | 0 |

Gold shape counts did not change during P4.1.

## Tag Distribution

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 15 |
| `parser_case` | 8 |
| `project_vs_repo` | 13 |
| `read_only` | 50 |
| `read_store_joint` | 73 |
| `related_but_useless` | 10 |
| `repo_convention` | 45 |
| `repo_vs_service` | 18 |
| `sensitive_boundary` | 48 |
| `service_invariant` | 120 |
| `service_vs_task_state` | 5 |
| `sop_skill_out_of_scope` | 12 |
| `stale_memory` | 15 |
| `store_skip_only` | 45 |
| `target_boundary` | 32 |
| `task_progress` | 66 |
| `user_profile_boundary` | 27 |
| `user_profile_vs_sensitive` | 27 |

## STORE Target Counts

| Target | P4 v1 | After P4.1 |
| --- | ---: | ---: |
| `service_memory` | 100 | 100 |
| `task_state` | 98 | 71 |
| `repo_memory` | 30 | 50 |
| `project_memory` | 13 | 20 |
| `user_profile` | 27 | 27 |

`project_memory` remains intentionally limited to project direction, scope, milestone decisions, and global policy. P4.1 did not use it as an ambiguity fallback.

## P4.1 Semantic Audit Changes

P4.1 modified 55 cases while keeping the dataset at 200 records:

- 28 READ-only primary cases were rewritten to reduce repeated "Remind me of the X rule..." phrasing.
- 20 repeated next-step test units were rewritten as durable repo test/path/command conventions and labeled `repo_memory`.
- 7 project-level milestone/scope decisions were added as `project_memory`.
- Explicit sensitive/private placeholders were rechecked; all remain `SKIP`.

Full details are in `reports/v04/pilot_semantic_audit.md`.

## Stale / Related-But-Useless Summary

Primary stale/related block: 25 cases.

- Stale cases: 15 tagged cases.
- Related-but-useless cases: 10 tagged cases.
- Default policy: stale or superseded candidate memories are not read when current behavior is requested.
- Historical comparison exceptions: selected cases explicitly ask to compare old and current behavior, so both stale and current memories are read.
- Related-but-useless distractors include same-domain but wrong-service memories, old v0.3 validation memories, prompt/training roadmap memories during P4, and broad platform memories that do not help the immediate service task.

## Target-Boundary Summary

Primary target-boundary block: 25 cases, plus additional boundary tags from P4.1 rebalance.

Coverage:

- `project_memory` vs `repo_memory`: project direction or global scope is stored as `project_memory`; file paths, commands, and test locations are `repo_memory`.
- `repo_memory` vs `service_memory`: repo workflow and locations are `repo_memory`; concrete service behavior and interfaces are `service_memory`.
- `service_memory` vs `task_state`: reusable behavior is `service_memory`; current progress, next steps, blockers, and temporary prohibitions are `task_state`.
- `user_profile` vs sensitive/private: stable non-sensitive preferences are `user_profile`; secrets, phone numbers, addresses, private emails, keys, and temporary personal state are `SKIP`.
- SOP/skill out-of-scope: repo/project/service conventions can be stored under existing targets; requests to create SOP/skill systems or new SOP targets are `SKIP`.

Every primary target-boundary case includes notes explaining the boundary decision.

## Sensitive / Private SKIP Summary

Sensitive/private coverage appears in 48 tagged cases.

Explicit sensitive/private placeholders checked in P4.1: 48. Violations: 0.

All explicit placeholders such as `DO_NOT_STORE`, private keys, recovery codes, personal phone numbers, private addresses, and private backup emails are labeled `SKIP`.

## Validator Result

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from src.v04.case_validator import validate_jsonl_file
print(validate_jsonl_file('data/v04/pilot_cases.jsonl'))
PY
```

Result:

```text
{'valid': True, 'errors': [], 'record_count': 200}
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

Additional structural checks:

```text
max candidate_memories: 4
max current_units: 3
unique case_ids: True
first/last case_id: v04_pilot_0001 / v04_pilot_0200
```

## Compared With P3 Bridge Set

| Metric | P3 bridge | P4.1 pilot |
| --- | ---: | ---: |
| Cases | 40 | 200 |
| Candidate memories | 75 | 445 |
| Current units | 96 | 490 |
| Gold READ IDs | 45 | 244 |
| Gold STORE units | 65 | 268 |
| Gold SKIP units | 31 | 222 |
| READ-only gold shape | 10 | 50 |
| STORE/SKIP-only gold shape | 15 | 77 |
| READ + STORE gold shape | 15 | 73 |

STORE target comparison:

| Target | P3 bridge | P4.1 pilot |
| --- | ---: | ---: |
| `service_memory` | 16 | 100 |
| `task_state` | 26 | 71 |
| `repo_memory` | 13 | 50 |
| `user_profile` | 6 | 27 |
| `project_memory` | 4 | 20 |

## Annotation Difficulties

- `service_memory` vs `task_state`: many cases combine durable behavior with active work state. P4.1 reduced obvious overuse of task-state-like next-step phrasing by replacing 20 units with durable repo conventions.
- `project_memory` remains narrow. Added project-memory units are phase/scope decisions, not vague uncertainty.
- Business-service examples are synthetic by design. They test routing boundaries, not real production facts.
- Auth service phrases such as "password reset token" are service behavior, not sensitive private placeholders. Actual secret placeholders remain skipped.

## Recommendation

P4.1 structurally passes and is suitable for human semantic review. If accepted, the next explicit context can start P5 A/B/C interface comparison.

Do not start prompts, eval runner implementation, model calls, or training until P4.1 review is complete.

## Human Review Points

- Spot-check the 20 repo-memory rebalance cases `v04_pilot_0081`-`v04_pilot_0100`.
- Spot-check the 7 project-memory rebalance cases: `v04_pilot_0038`, `v04_pilot_0044`, `v04_pilot_0050`, `v04_pilot_0056`, `v04_pilot_0062`, `v04_pilot_0068`, `v04_pilot_0074`.
- Review the remaining 7 templated READ-only phrasings and decide whether they are acceptable as residual variety.
- Confirm that SOP/skill out-of-scope cases should remain `SKIP` rather than motivating a new target.

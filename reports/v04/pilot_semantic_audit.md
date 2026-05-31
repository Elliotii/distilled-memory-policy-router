# v0.4 Pilot Semantic Audit

Date: 2026-05-31

## Audit Goal

P4 pilot v1 was structurally valid, but not semantically locked. P4.1 audited the 200-case pilot for template repetition, STORE target balance, target-boundary ambiguity, and sensitive/private SKIP safety before P5 A/B/C evaluation work.

This audit did not add cases, remove cases, change the schema, modify parser/validator behavior, write prompts, write an eval runner, call models, or train models.

## Findings

- READ-only primary cases were too templated: the first 35 cases all used a close variant of "Remind me of the X rule before I continue this task."
- `repo_memory` STORE coverage was low at 30 units compared with `service_memory` 100 and `task_state` 98.
- `project_memory` coverage was low at 13 units, but the low count was mostly principled rather than a catch-all failure.
- No broad `service_memory` vs `task_state` relabeling was needed, but 20 repeated "Next, add a regression case..." units were better replaced with durable repo test/path/command conventions.
- Explicit synthetic sensitive placeholders were already skipped; no private placeholder was stored.

## Changes Made

Modified cases: 55 total.

- READ-only expression rewrites: 28 cases.
- Repo-memory rebalance edits: 20 cases.
- Project-memory rebalance edits: 7 cases.

The total dataset size remains 200 cases.

## Modified Case IDs

READ-only wording rewrites:

```text
v04_pilot_0001
v04_pilot_0002
v04_pilot_0003
v04_pilot_0004
v04_pilot_0006
v04_pilot_0007
v04_pilot_0008
v04_pilot_0009
v04_pilot_0011
v04_pilot_0012
v04_pilot_0013
v04_pilot_0014
v04_pilot_0016
v04_pilot_0017
v04_pilot_0018
v04_pilot_0019
v04_pilot_0021
v04_pilot_0022
v04_pilot_0023
v04_pilot_0024
v04_pilot_0026
v04_pilot_0027
v04_pilot_0028
v04_pilot_0029
v04_pilot_0031
v04_pilot_0032
v04_pilot_0033
v04_pilot_0034
```

Project-memory rebalance:

```text
v04_pilot_0038
v04_pilot_0044
v04_pilot_0050
v04_pilot_0056
v04_pilot_0062
v04_pilot_0068
v04_pilot_0074
```

Repo-memory rebalance:

```text
v04_pilot_0081
v04_pilot_0082
v04_pilot_0083
v04_pilot_0084
v04_pilot_0085
v04_pilot_0086
v04_pilot_0087
v04_pilot_0088
v04_pilot_0089
v04_pilot_0090
v04_pilot_0091
v04_pilot_0092
v04_pilot_0093
v04_pilot_0094
v04_pilot_0095
v04_pilot_0096
v04_pilot_0097
v04_pilot_0098
v04_pilot_0099
v04_pilot_0100
```

## STORE Target Counts

| Target | Before P4.1 | After P4.1 |
| --- | ---: | ---: |
| `service_memory` | 100 | 100 |
| `task_state` | 98 | 71 |
| `repo_memory` | 30 | 50 |
| `project_memory` | 13 | 20 |
| `user_profile` | 27 | 27 |

## Gold Shape Counts

Gold shape counts did not change.

| Gold shape | Before P4.1 | After P4.1 |
| --- | ---: | ---: |
| READ-only | 50 | 50 |
| STORE/SKIP-only | 77 | 77 |
| READ + STORE joint | 73 | 73 |
| No READ and no STORE | 0 | 0 |

## READ-only Template Improvement

Before P4.1, the primary READ-only block had 35 templated "Remind me of the X rule..." units. After P4.1, only 7 such units remain, and they are no longer consecutive.

The rewritten cases use more realistic lookup language, such as:

- "Which memory explains how the case validator checks DSL alignment?"
- "Before editing refunds, which payments memory is still relevant?"
- "I need the export format and snapshot location before updating tests."
- "Which case-validator memory is useful, and which old validator memory should stay out?"

The READ gold labels did not change for these rewrites.

## Repo-memory Coverage Improvement

`repo_memory` STORE units increased from 30 to 50.

The new repo-memory units cover:

- parser and validator test file paths;
- future metrics and prompt file locations;
- report artifact location;
- service-specific test commands;
- migration/test fixture paths;
- docs locations;
- snapshot and job-definition conventions.

Targets were changed only after changing the unit text into a durable repo convention. The audit did not simply relabel one-off next-step text as `repo_memory`.

## Project-memory Coverage

`project_memory` STORE units increased from 13 to 20.

Added project-memory units are project-level phase, scope, or milestone decisions:

- A/B/C evaluation is gated on pilot semantic review.
- P4 data creation is separated from P5 interface evaluation.
- Prompt/eval-runner work starts only after P4.1 review.
- v0.5 training depends on accepted v0.4 interface evidence.
- v0.4 assumes fixed candidate memories and pre-segmented units.
- The 200-case pilot is not locked gold by itself.

No uncertain or vague unit was moved into `project_memory`.

## Service-memory vs Task-state Spot-check

Spot-check conclusion: no broad target confusion was found.

The main adjustment was to replace 20 repeated `task_state` units that were phrased as next-step regression work with explicit repo conventions. Those units are now `repo_memory` because they describe test paths, commands, fixture locations, docs locations, or artifact locations.

Remaining `task_state` labels still describe current progress, blockers, next actions, or temporary constraints.

## Sensitive / Private SKIP Check

Explicit synthetic sensitive/private placeholders checked: 48.

Violations found: 0.

All explicit placeholders such as `DO_NOT_STORE`, `PRIVATE_KEY`, recovery codes, personal phone numbers, private addresses, and private backup emails are in `gold.skip`, not `gold.store`.

Auth service phrases such as "password reset token" were treated as service behavior, not sensitive private placeholders, because they do not contain actual secret values.

## Validator Result

```text
{'valid': True, 'errors': [], 'record_count': 200}
```

## Recommendation

P4.1 passes structural validation and improves semantic readiness. I recommend moving to P5 only after owner review accepts this rebalance and confirms that the pilot can be used for A/B/C interface comparison.

Do not start P5 prompts, eval runner, model calls, or training from this context.

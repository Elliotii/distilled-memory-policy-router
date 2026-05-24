# Distribution Report: day2_mock_100

Generated file: `data/synthetic_drafts/day2_mock_100/cases.jsonl`

Structural validation checks JSON shape, schema constraints, candidate ID references, exact span substrings, and duplicates. It does not prove semantic quality.

## Summary

| metric | value |
| --- | --- |
| valid_cases | 100 |
| invalid_samples | 0 |
| cases_with_recent_context | 10 |
| cases_with_candidate_memories | 50 |
| target.read_hints | 50 |
| target.write_spans | 90 |
| target.ignore_spans | 20 |

## Category Counts

| category | count |
| --- | --- |
| simple_write | 10 |
| multi_write | 10 |
| read_relevant_memory | 10 |
| ignore_noise | 10 |
| correction_or_revision | 10 |
| context_dependent_reference | 10 |
| conflicting_memory | 10 |
| mixed_write_and_ignore | 10 |
| no_action_needed | 10 |
| distractor_memory_selection | 10 |

## Candidate Memory Type Counts

| memory_type | count |
| --- | --- |
| sop | 40 |
| fact | 40 |
| decision | 0 |
| task_state | 0 |

## Target Write Type Counts

| memory_type | count |
| --- | --- |
| sop | 50 |
| fact | 10 |
| decision | 30 |
| task_state | 0 |

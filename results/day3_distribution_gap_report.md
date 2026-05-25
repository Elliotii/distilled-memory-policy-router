# Day 3 Dataset Distribution Gap Report

This report is structural analysis only. It checks validated JSONL records, category balance, memory-type distribution, context/candidate coverage, and target-field counts. It does not prove semantic label quality.

The target ranges come from the project spec and the Day 2 generation strategy. They are planning targets for the next synthetic generation round, not hard validator rules.

## Dataset: seed

File: `data/seed_examples.jsonl`

### Summary

| metric | count | rate |
| --- | --- | --- |
| total_cases | 50 | 100.0% |
| cases_with_candidate_memories | 26 | 52.0% |
| cases_with_recent_context | 9 | 18.0% |
| cases_with_ignore_spans | 16 | 32.0% |
| cases_with_5_to_8_candidate_memories | 2 | 4.0% |
| target.read_hints | 35 |  |
| target.write_spans | 45 |  |
| target.ignore_spans | 18 |  |

### Category Distribution

| category | count | actual_rate | mvp_target_rate | delta_vs_target_count |
| --- | --- | --- | --- | --- |
| simple_write | 5 | 10.0% | 10.0% | +0.0 |
| multi_write | 5 | 10.0% | 12.0% | -1.0 |
| read_relevant_memory | 5 | 10.0% | 12.0% | -1.0 |
| ignore_noise | 5 | 10.0% | 12.0% | -1.0 |
| correction_or_revision | 5 | 10.0% | 12.0% | -1.0 |
| context_dependent_reference | 5 | 10.0% | 10.0% | +0.0 |
| conflicting_memory | 5 | 10.0% | 10.0% | +0.0 |
| mixed_write_and_ignore | 5 | 10.0% | 8.0% | +1.0 |
| no_action_needed | 5 | 10.0% | 8.0% | +1.0 |
| distractor_memory_selection | 5 | 10.0% | 6.0% | +2.0 |

### Candidate Memory Type Distribution

| memory_type | count | rate |
| --- | --- | --- |
| sop | 20 | 27.8% |
| fact | 32 | 44.4% |
| decision | 13 | 18.1% |
| task_state | 7 | 9.7% |

### Target Write Type Distribution

| memory_type | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| sop | 14 | 31.1% | 10-15% | above_target |
| fact | 7 | 15.6% | 25-30% | below_target |
| decision | 18 | 40.0% | 30-35% | above_target |
| task_state | 6 | 13.3% | 20-25% | below_target |

### Case-Rate Targets

| metric | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| cases_with_ignore_spans | 16 | 32.0% | 25-35% | in_range |
| cases_with_candidate_memories | 26 | 52.0% | 50-70% | in_range |
| cases_with_recent_context | 9 | 18.0% | 25-40% | below_target |
| cases_with_5_to_8_candidate_memories | 2 | 4.0% | 15-25% | below_target |

## Dataset: mock

File: `data/synthetic_drafts/day3_prompt_direction_smoke/cases.jsonl`

### Summary

| metric | count | rate |
| --- | --- | --- |
| total_cases | 100 | 100.0% |
| cases_with_candidate_memories | 50 | 50.0% |
| cases_with_recent_context | 10 | 10.0% |
| cases_with_ignore_spans | 20 | 20.0% |
| cases_with_5_to_8_candidate_memories | 0 | 0.0% |
| target.read_hints | 50 |  |
| target.write_spans | 90 |  |
| target.ignore_spans | 20 |  |

### Category Distribution

| category | count | actual_rate | mvp_target_rate | delta_vs_target_count |
| --- | --- | --- | --- | --- |
| simple_write | 10 | 10.0% | 10.0% | +0.0 |
| multi_write | 10 | 10.0% | 12.0% | -2.0 |
| read_relevant_memory | 10 | 10.0% | 12.0% | -2.0 |
| ignore_noise | 10 | 10.0% | 12.0% | -2.0 |
| correction_or_revision | 10 | 10.0% | 12.0% | -2.0 |
| context_dependent_reference | 10 | 10.0% | 10.0% | +0.0 |
| conflicting_memory | 10 | 10.0% | 10.0% | +0.0 |
| mixed_write_and_ignore | 10 | 10.0% | 8.0% | +2.0 |
| no_action_needed | 10 | 10.0% | 8.0% | +2.0 |
| distractor_memory_selection | 10 | 10.0% | 6.0% | +4.0 |

### Candidate Memory Type Distribution

| memory_type | count | rate |
| --- | --- | --- |
| sop | 0 | 0.0% |
| fact | 50 | 62.5% |
| decision | 20 | 25.0% |
| task_state | 10 | 12.5% |

### Target Write Type Distribution

| memory_type | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| sop | 3 | 3.3% | 10-15% | below_target |
| fact | 37 | 41.1% | 25-30% | above_target |
| decision | 40 | 44.4% | 30-35% | above_target |
| task_state | 10 | 11.1% | 20-25% | below_target |

### Case-Rate Targets

| metric | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| cases_with_ignore_spans | 20 | 20.0% | 25-35% | below_target |
| cases_with_candidate_memories | 50 | 50.0% | 50-70% | in_range |
| cases_with_recent_context | 10 | 10.0% | 25-40% | below_target |
| cases_with_5_to_8_candidate_memories | 0 | 0.0% | 15-25% | below_target |

## Recommended Next Generation Bias

- Keep category sampling close to the MVP distribution from the project spec.
- Increase `task_state` writes and task-state candidate memories.
- Increase `fact` writes in seed-like human examples; avoid drifting back to SOP-heavy data.
- Keep `sop` valid but rare unless the user explicitly states a durable workflow rule.
- Generate more recent-context cases, especially context-dependent references and corrections.
- Generate more cases with 5-8 candidate memories to stress read selection.
- Raise ignore-span coverage, but keep ignores selective rather than exhaustive.
- Treat mock data as pipeline smoke-test material only; do not train or evaluate on it.

### Dataset-Specific Notes

- `seed`: add more task_state write targets; reduce generic sop write targets; add more recent_context cases; add more 5-8 candidate-memory cases.
- `mock`: add more task_state write targets; add more recent_context cases; add more 5-8 candidate-memory cases.


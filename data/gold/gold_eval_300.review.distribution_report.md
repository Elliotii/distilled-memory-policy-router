# Day 3 Dataset Distribution Gap Report

This report is structural analysis only. It checks validated JSONL records, category balance, memory-type distribution, context/candidate coverage, and target-field counts. It does not prove semantic label quality.

The target ranges come from the project spec and the Day 2 generation strategy. They are planning targets for the next synthetic generation round, not hard validator rules.

## Dataset: gold_review

File: `data/gold/gold_eval_300.review.jsonl`

### Summary

| metric | count | rate |
| --- | --- | --- |
| total_cases | 300 | 100.0% |
| cases_with_candidate_memories | 214 | 71.3% |
| cases_with_recent_context | 164 | 54.7% |
| cases_with_ignore_spans | 60 | 20.0% |
| cases_with_5_to_8_candidate_memories | 75 | 25.0% |
| target.read_hints | 273 |  |
| target.write_spans | 219 |  |
| target.ignore_spans | 67 |  |

### Category Distribution

| category | count | actual_rate | mvp_target_rate | delta_vs_target_count |
| --- | --- | --- | --- | --- |
| simple_write | 30 | 10.0% | 10.0% | +0.0 |
| multi_write | 30 | 10.0% | 12.0% | -6.0 |
| read_relevant_memory | 30 | 10.0% | 12.0% | -6.0 |
| ignore_noise | 30 | 10.0% | 12.0% | -6.0 |
| correction_or_revision | 30 | 10.0% | 12.0% | -6.0 |
| context_dependent_reference | 30 | 10.0% | 10.0% | +0.0 |
| conflicting_memory | 30 | 10.0% | 10.0% | +0.0 |
| mixed_write_and_ignore | 30 | 10.0% | 8.0% | +6.0 |
| no_action_needed | 30 | 10.0% | 8.0% | +6.0 |
| distractor_memory_selection | 30 | 10.0% | 6.0% | +12.0 |

### Candidate Memory Type Distribution

| memory_type | count | rate |
| --- | --- | --- |
| sop | 110 | 17.1% |
| fact | 339 | 52.7% |
| decision | 132 | 20.5% |
| task_state | 62 | 9.6% |

### Target Write Type Distribution

| memory_type | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| sop | 49 | 22.4% | 10-15% | above_target |
| fact | 84 | 38.4% | 25-30% | above_target |
| decision | 59 | 26.9% | 30-35% | below_target |
| task_state | 27 | 12.3% | 20-25% | below_target |

### Case-Rate Targets

| metric | count | actual_rate | target_range | status |
| --- | --- | --- | --- | --- |
| cases_with_ignore_spans | 60 | 20.0% | 25-35% | below_target |
| cases_with_candidate_memories | 214 | 71.3% | 50-70% | above_target |
| cases_with_recent_context | 164 | 54.7% | 25-40% | above_target |
| cases_with_5_to_8_candidate_memories | 75 | 25.0% | 15-25% | in_range |

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

- `gold_review`: add more task_state write targets; reduce generic sop write targets.


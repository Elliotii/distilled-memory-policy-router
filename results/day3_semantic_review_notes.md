# Day 3 Semantic Review Notes

## Scope

This is a small manual semantic spot check, not a full gold-data review. Structural validation has already checked JSON shape, schema constraints, exact substring spans, candidate-memory ID references, duplicate IDs, and duplicate current inputs.

Semantic review checks whether the labels are useful for the intended memory-policy behavior:

- `read_hints` should select genuinely relevant candidate memories.
- `write_spans` should capture durable facts, decisions, preferences, or task state.
- `ignore_spans` should mark memory-pollution risks selectively.
- Memory types should follow the project annotation rules.
- Mock data should not be mistaken for train/eval quality.

## Reviewed Seed Cases

| case_id | category | outcome | note |
| --- | --- | --- | --- |
| seed_simple_write_005 | simple_write | accept | Clear business fact write. |
| seed_multi_write_005 | multi_write | accept | Good mix of fact, task_state, and decision writes. |
| seed_read_relevant_memory_005 | read_relevant_memory | accept | Reads the blocker and schema memories while ignoring styling noise. |
| seed_context_dependent_reference_005 | context_dependent_reference | accept | Correctly uses recent context and reads the task-state blocker. |
| seed_conflicting_memory_005 | conflicting_memory | accept | Good conflict example for replacing the canonical customer identifier. |
| seed_mixed_write_and_ignore_005 | mixed_write_and_ignore | accept | Clean task-state write plus temporary Slack outage ignore. |
| seed_correction_or_revision_003 | correction_or_revision | accept | `sop` is defensible because the span is a durable secret-handling rule. |
| seed_distractor_memory_selection_004 | distractor_memory_selection | accept | Removed the ambiguous migration-file SOP from `read_hints`; the case now reads only the save-format fact. |

Seed sample outcome:

| outcome | count |
| --- | --- |
| accept | 8 |
| minor_fix | 0 |
| major_fix | 0 |
| reject | 0 |

## Reviewed Mock Cases

| case_id | category | outcome | note |
| --- | --- | --- | --- |
| mock_day3_prompt_direction_smoke_game_dev_workflow_000002 | multi_write | smoke_only | Structurally useful, but the wording is template-like. |
| mock_day3_prompt_direction_smoke_hard_negative_noisy_memory_000003 | read_relevant_memory | smoke_only | Correct read selection shape, but not realistic enough for training. |
| mock_day3_prompt_direction_smoke_direct_coding_agent_000004 | ignore_noise | smoke_only | Good ignore-span shape, but repeated mock wording is intentional. |
| mock_day3_prompt_direction_smoke_direct_coding_agent_000010 | distractor_memory_selection | smoke_only | Useful for pipeline coverage, not semantic dataset quality. |

Mock sample outcome:

| outcome | count |
| --- | --- |
| smoke_only | 4 |

## Findings

- The current seed set is acceptable as a small curated anchor set.
- The strongest seed-data gap is distributional, not structural: too many `sop` writes, not enough `task_state` and business/architecture `fact` writes.
- Recent-context coverage is still low for the project goal, especially for project progress, corrections, and context-dependent references.
- Heavy candidate-memory cases are rare, so read-selection difficulty is still under-tested.
- Mock data is intentionally repetitive and should remain pipeline smoke-test data only.
- Validator success must continue to be reported as structural validation, not semantic correctness.

## Next Data Bias

For the next teacher-generation batch, request more examples with:

- Active project blockers, unfinished work, and next steps labeled as `task_state`.
- Business-domain facts and architecture facts labeled as `fact`.
- Durable project choices and postponed work labeled as `decision`.
- Recent context needed to interpret "it", "that", "the second option", and correction turns.
- Five to eight candidate memories with realistic distractors.
- Selective ignore spans for temporary failures, stale notes, casual chatter, and corrected mistakes.

Avoid overproducing:

- Generic coding rules that belong better in `AGENTS.md`, skills, or project instructions.
- Mock-prefixed examples.
- Near-duplicate current user inputs with only superficial numbering changes.
- Cases where all non-written text is marked as ignored.

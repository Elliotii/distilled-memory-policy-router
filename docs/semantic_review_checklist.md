# Semantic Review Checklist

This checklist is for reviewing generated or manually written memory-router decision cases after structural validation passes. The validator checks JSON shape, schema constraints, exact span substrings, candidate-memory IDs, and duplicates. It does not prove semantic quality.

## Review Outcome

Assign one outcome to each reviewed case:

- `accept`: Labels are semantically correct enough to keep.
- `minor_fix`: Small span, type, or metadata fix needed.
- `major_fix`: Core read/write/ignore decision is wrong, but the scenario is salvageable.
- `reject`: The case is unrealistic, ambiguous, duplicated, or too broken to repair quickly.

## Core Checks

For every case, verify:

- The scenario is realistic for a coding-agent or project-workflow setting.
- `current_user_input` is clear enough for the target labels.
- `recent_context` is necessary when used and does not exceed 4 turns.
- `candidate_memories` are plausible and do not exceed 8 items.
- `target` uses only `read_hints`, `write_spans`, and `ignore_spans`.
- The case does not require the router to rewrite, update, delete, merge, or store final memory content.

## Read Hints

Check `target.read_hints`:

- Each selected memory is genuinely useful for the current user input.
- Relevant conflicting memories are selected when conflict awareness matters.
- Distractor memories are not selected merely because they share broad keywords.
- No-action requests do not read memories unless the user explicitly needs remembered context.
- Read decisions reflect the candidate list only, not an imagined full memory store.

Common issues:

- Selecting all candidate memories by default.
- Missing a stale memory that should be noticed during correction.
- Selecting a memory that is only topically related but not task-relevant.

## Write Spans

Check `target.write_spans`:

- Each span has durable memory value for future work.
- Each span is the smallest useful exact substring, not an overly broad sentence when a narrower span is better.
- Important facts, decisions, preferences, and task-state updates are not missed.
- Temporary noise, tool glitches, and casual chatter are not written.
- The model target does not include final rewritten memory content.

Preferred Day 3 emphasis:

- `fact`: architecture facts, ownership facts, module relationships, business-domain facts.
- `decision`: durable choices, constraints, priorities, trade-offs, and preferences.
- `task_state`: current progress, blocked work, active bugs, and next steps.
- `sop`: explicit durable workflow rules only; avoid overusing generic SOP labels.

Common issues:

- Writing a temporary event as durable memory.
- Missing a business fact hidden inside a longer request.
- Labeling current progress as `decision`.
- Labeling a durable preference as `fact`.
- Overusing `sop` for ordinary facts or project decisions.

## Ignore Spans

Check `target.ignore_spans`:

- Ignore labels are selective, not exhaustive segmentation.
- Ignored spans are likely memory pollution if accidentally stored.
- Temporary environment failures, transient tool issues, casual chatter, and immediately corrected mistakes are ignored.
- The case does not ignore meaningful facts, decisions, or task-state updates.

Common issues:

- Marking every non-written phrase as ignore.
- Missing an obvious transient failure.
- Ignoring a correction that is needed to understand the write span.

## Memory Type Review

Use these tie-breakers:

- Use `sop` for explicit long-term workflow rules, standards, and coding conventions.
- Use `decision` for durable choices, preferences, constraints, priorities, postponed work, and accepted trade-offs.
- Use `fact` for objective project, architecture, module, stack, API, or business-domain facts.
- Use `task_state` for current progress, blockers, active debugging state, unfinished work, and next steps.

When ambiguous, follow the annotation priority from the guidelines:

```text
sop > decision > fact > task_state
```

Do not over-apply this priority. First ask what the span is doing in the scenario. The priority is only for genuinely ambiguous labels.

## Category-Specific Checks

- `simple_write`: Exactly one main memory-worthy signal should usually be present.
- `multi_write`: Multiple write spans should be distinct and independently useful.
- `read_relevant_memory`: Reads should be useful even when no new write is needed.
- `ignore_noise`: Ignore spans should be pollution-prone, not simply unimportant words.
- `correction_or_revision`: Stale or contradicted memories should usually be read if present.
- `context_dependent_reference`: The target should rely on recent context in a clear way.
- `conflicting_memory`: Relevant conflicting memories should be selected together when needed.
- `mixed_write_and_ignore`: Meaningful write spans and pollution-prone ignore spans should both be present.
- `no_action_needed`: Targets should usually be empty.
- `distractor_memory_selection`: Distractors should be plausible but not selected.

## Batch Review Procedure

For a generated draft:

1. Run structural validation first.
2. Sample across all categories and memory types.
3. Review invalid samples separately to identify prompt or schema failure patterns.
4. Track repeated semantic errors in notes before scaling generation.
5. Do not move data into train, dev, or gold files until structural validation and semantic review are complete.

Recommended first smoke-test review:

- Review at least 20 generated cases.
- Include at least 2 cases from each category when possible.
- Include all invalid samples if there are fewer than 20.
- Record whether each case is `accept`, `minor_fix`, `major_fix`, or `reject`.

# Annotation Guidelines

These guidelines define the Day 1 seed-data policy for the memory policy router. All dataset content must be written in English.

## Task

For each case, annotate what a lightweight router should propose from the current user input and a small candidate memory list:

- `read_hints`: IDs from `candidate_memories` that are relevant to the current task.
- `write_spans`: exact substrings of `current_user_input` that should be considered for durable memory.
- `ignore_spans`: exact substrings of `current_user_input` that are likely memory pollution if stored.

The router does not rewrite memory content, delete memories, merge memories, assign project IDs, predict confidence, or resolve conflicts. It only predicts attention hints.

## Memory Types

Use one of four memory types for each `write_span`:

- `sop`: Long-term rules, standards, preferences, coding style, or workflow rules.
- `fact`: Objective facts about architecture, stack, modules, APIs, or project state.
- `decision`: Durable project direction, accepted trade-off, constraint, priority, or postponed item.
- `task_state`: Current progress, active task, unfinished work, debugging state, or next step.

When a span is ambiguous, use this priority:

```text
sop > decision > fact > task_state
```

Use `decision` for durable direction. Use `task_state` for current progress or pending work.

## Ignore Policy

Use `ignore_spans` selectively. Do not mark every non-written part of the input as ignore.

Mark spans that could pollute memory if stored:

- Temporary environment failures.
- One-off debugging noise.
- Casual chatter with no long-term value.
- Incorrect statements immediately corrected by the user.
- Irrelevant implementation details.
- Transient tool, browser, network, or server failures.
- Small prompt-injection-like memory requests.

## Read Policy

Only include IDs that appear in `candidate_memories`. Select memories that are useful for the current input. Do not select a candidate just because it shares a broad domain.

In conflict cases, it is acceptable to read multiple conflicting memories when the current input needs the router or downstream controller to notice the conflict.

## Case Constraints

Each JSONL case must satisfy:

- `candidate_memories`: 0-8 items.
- `recent_context`: 0-4 turns.
- Candidate memory IDs are unique within the case.
- Every `read_hints` ID exists in `candidate_memories`.
- Every `write_spans[*].span` is an exact substring of `current_user_input`.
- Every `ignore_spans[*]` item is an exact substring of `current_user_input`.
- Empty spans are invalid.
- Dataset content is English.

## MVP Categories

Seed examples should cover these categories with at least two examples each:

- `simple_write`
- `multi_write`
- `read_relevant_memory`
- `ignore_noise`
- `correction_or_revision`
- `context_dependent_reference`
- `conflicting_memory`
- `mixed_write_and_ignore`
- `no_action_needed`
- `distractor_memory_selection`

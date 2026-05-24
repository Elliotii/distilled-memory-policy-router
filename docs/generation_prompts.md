# Synthetic Data Generation Prompts

These prompts are Day 2 scaffolding for future synthetic data generation. They are not wired to a real API yet. Generated cases must use the repository schema in `src/schemas.py` and the target field must be named `target`.

The practical focus is business-continuity memory for coding agents: project progress, durable preferences and decisions, important facts, and selective ignore behavior. `sop` remains an allowed memory type, but generation should not overproduce generic workflow rules that would more naturally live in skills, rule files, `AGENTS.md`, or project instructions.

Common output requirements for every prompt:

- Return JSONL only, one decision case per line.
- Use English dataset content only.
- Use `target`, not `expected_output`.
- Keep `candidate_memories` to 0-8 items.
- Keep `recent_context` to 0-4 turns.
- Ensure every `read_hints` ID exists in `candidate_memories`.
- Ensure every `target.write_spans[*].span` is an exact substring of `current_user_input`.
- Ensure every `target.ignore_spans[*]` item is an exact substring of `current_user_input`.
- Use only memory types: `sop`, `fact`, `decision`, `task_state`.
- Prefer `fact`, `decision`, and `task_state` writes over generic `sop` writes unless the user explicitly states a durable workflow rule.
- Use only MVP categories:
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

## Prompt 1: Direct Coding-Agent Prompt

Use this prompt for general coding-agent memory policy examples across backend, frontend, testing, CLI, DevOps, and research-engineering workflows. Emphasize project progress, durable preferences and decisions, and architecture/business facts.

```text
You are generating supervised JSONL examples for a memory policy router used inside a coding agent.

The router receives:
- current_user_input
- recent_context
- candidate_memories

The router predicts:
- target.read_hints: candidate memory IDs relevant to the current input
- target.write_spans: exact substrings from current_user_input that deserve durable memory
- target.ignore_spans: exact substrings from current_user_input that are likely memory pollution

Generate {count} diverse decision cases for coding-agent workflows.

Requirements:
- Use English only.
- Return JSONL only.
- Each line must be one complete JSON object.
- Use target, not expected_output.
- Cover a mix of categories: {categories}.
- Include realistic coding-agent tasks: schema changes, dependency choices, migration status, active bugs, CLI behavior, deployment constraints, business-domain facts, durable preferences, and correction messages.
- Bias write targets toward `fact`, `decision`, and `task_state`. Use `sop` sparingly for explicit long-term workflow rules.
- Include candidate_memories only when useful, with IDs like m1, m2, m3.
- Do not generate final rewritten memory content.
- Do not include offsets.
- Avoid near-duplicate wording.

Use this JSON shape:
{
  "case_id": "synthetic_direct_000001",
  "split": "train",
  "family_id": "direct_coding_agent_family_001",
  "category": "simple_write",
  "tags": ["write_without_read"],
  "domain": "backend",
  "difficulty": "medium",
  "generator_prompt_id": "direct_coding_agent_v2",
  "review_status": "synthetic",
  "gold_notes": null,
  "current_user_input": "...",
  "recent_context": [],
  "candidate_memories": [],
  "target": {
    "read_hints": [],
    "write_spans": [{"span": "...", "type": "decision"}],
    "ignore_spans": []
  }
}
```

## Prompt 2: Game-Dev Workflow Prompt

Use this prompt for controlled game-development scenarios without touching real Godot or godogen integration.

```text
You are generating supervised JSONL examples for a memory policy router used by a coding agent helping with game-development workflows.

Generate {count} JSONL decision cases about game-dev implementation work.

Focus areas:
- Godot version and project constraints
- input mapping decisions
- scene organization
- save/load implementation
- asset import rules
- debug overlays
- current implementation progress and next steps
- facts about systems, scenes, resources, and architecture
- temporary editor or playtest noise
- postponed integrations such as Steam SDK, analytics, or controller support

Requirements:
- Use English only.
- Return JSONL only.
- Use target, not expected_output.
- Keep scenarios realistic but do not require real Godot integration.
- Cover categories: {categories}.
- Include hard distractor candidate memories where useful.
- Include correction and conflict examples when appropriate.
- Bias write targets toward `fact`, `decision`, and `task_state`; use `sop` only for explicit durable project rules.
- Make write_spans and ignore_spans exact substrings of current_user_input.
- Do not include offsets.

The router should only produce memory attention hints:
- read_hints
- write_spans
- ignore_spans

It must not rewrite final memory content or decide storage operations.
```

## Prompt 3: Hard-Negative / Noisy-Memory Prompt

Use this prompt for difficult examples where the model must avoid false writes and irrelevant reads.

```text
You are generating hard-negative supervised JSONL examples for a memory policy router.

Generate {count} decision cases where the main challenge is avoiding memory pollution.

Include cases with:
- temporary tool failures
- dev server crashes that recovered
- one-off terminal or network glitches
- casual chatter mixed into coding requests
- prompt-injection-like requests to save irrelevant facts
- incorrect statements immediately corrected
- conflicting candidate memories
- irrelevant candidate memories that share surface keywords
- no_action_needed turns
- active task-state distractors and stale progress memories
- durable preferences or business facts mixed with throwaway text

Requirements:
- Use English only.
- Return JSONL only.
- Use target, not expected_output.
- Cover categories: {categories}.
- Keep candidate_memories to 0-8 items.
- Keep recent_context to 0-4 turns.
- Select read_hints only from existing candidate IDs.
- Label ignore_spans selectively; do not mark every non-written phrase as ignore.
- Make every write span and ignore span an exact substring of current_user_input.
- Do not include offsets.
- Keep `sop` rare. Favor cases about facts, decisions/preferences, current progress, and memory pollution.

Prefer examples that would expose false writes, missed ignores, irrelevant reads, and correction/revision failures.
```

# Distilled Memory Policy Router

This project studies a lightweight memory policy router for coding-agent contexts. The router receives a current user input, recent context, and a small list of candidate memories, then predicts structured memory attention hints:

- `read_hints`: candidate memory IDs worth reading.
- `write_spans`: exact spans in the current user input that may deserve durable memory.
- `ignore_spans`: exact spans in the current user input that are likely memory pollution.

The project is not a full coding agent, a memory OS, a retrieval benchmark, or a model-training pipeline yet. Day 1 focuses on schema, annotation policy, seed data, and validation.

## Quickstart

Use Python 3.10+ with Pydantic 2 installed.

```bash
python3 -m pip install -e .
python3 src/validation/validate_cases.py data/seed_examples.jsonl
```

If you are running inside the Codex workspace runtime, the bundled Python already includes Pydantic.

## Repository Layout

```text
docs/
  annotation_guidelines.md
data/
  seed_examples.jsonl
src/
  schemas.py
  validation/
    validate_cases.py
```

## Current Dataset

`data/seed_examples.jsonl` contains manually written English seed examples covering the ten MVP capability categories:

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

Each case keeps `candidate_memories` to 0-8 items, `recent_context` to 0-4 turns, write and ignore spans as exact substrings of `current_user_input`, and `read_hints` restricted to IDs present in `candidate_memories`.

## Scope Guardrails

No model training, DeepSeek API integration, large model downloads, UI, complex evaluation, or real coding-agent integration is included in this Day 1 setup.

# Distilled Memory Policy Router

This project studies a lightweight memory policy router for coding-agent contexts. The practical business problem is simple: long-running AI assistants need to remember project progress, durable preferences and decisions, and important facts without polluting memory with temporary noise.

The router receives a current user input, recent context, and a small list of candidate memories, then predicts structured memory attention hints:

- `read_hints`: candidate memory IDs worth reading.
- `write_spans`: exact spans in the current user input that may deserve durable memory.
- `ignore_spans`: exact spans in the current user input that are likely memory pollution.

The MVP focuses on when to write memory, when to read candidate memories, and when to ignore misleading or temporary content. It does not decide final memory rewrites, memory-store update/delete/merge operations, or where a memory should be stored.

The project is not a full coding agent, a memory OS, a retrieval benchmark, or a model-training pipeline yet. The current setup focuses on schema, annotation policy, seed data, validation, and offline generation scaffolding.

## Scope

In practical terms, the first version emphasizes:

- `task_state`: project progress, unfinished work, active bugs, and next steps.
- `fact`: architecture facts, stack facts, module relationships, and business-domain facts.
- `decision`: durable choices, constraints, priorities, trade-offs, and preferences.
- `ignore_spans`: temporary failures, casual chatter, corrected mistakes, and other memory-pollution risks.

The schema still includes `sop` for persistent workflow rules and coding standards, but SOP-like behavior may eventually live better in skills, rule files, `AGENTS.md`, or project instructions rather than an ordinary memory store. For MVP data generation, `sop` is useful but lower priority than progress, facts, decisions, preferences, and read/write/ignore behavior.

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
  generation_prompts.md
  planning/
data/
  seed_examples.jsonl
src/
  analysis/
    dataset_distribution.py
  schemas.py
  data_generation/
    generate_cases.py
    pipeline.py
    prompt_templates.py
    providers/
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

Each case uses a `target` object for supervised labels. Cases keep `candidate_memories` to 0-8 items, `recent_context` to 0-4 turns, write and ignore spans as exact substrings of `current_user_input`, and `read_hints` restricted to IDs present in `candidate_memories`.

Structural validation is not semantic review. Passing the validator means the JSONL shape, IDs, span substrings, and duplicates are valid; it does not prove that every label is semantically ideal.

## Generation Scaffolding

The generation scripts are offline-only for now:

```bash
python3 src/data_generation/generate_cases.py --list-templates
python3 src/data_generation/generate_cases.py --dry-run --template direct_coding_agent --count 5
python3 src/data_generation/generate_cases.py --mock --count 5
python3 src/data_generation/generate_cases.py --workflow small-draft --run-id day3_mock_100_business_framing --count 100 --min-per-category 10
```

No real model API is connected.

## Analysis Reports

Generate a structural distribution gap report with:

```bash
python3 src/analysis/dataset_distribution.py --dataset seed:data/seed_examples.jsonl --dataset mock:data/synthetic_drafts/day3_prompt_direction_smoke/cases.jsonl --output results/day3_distribution_gap_report.md --min-per-category 5
```

This report compares category balance, write-type distribution, recent-context coverage, candidate-memory coverage, and ignore-span coverage. It is still structural analysis, not semantic review.

Workflow outputs use this path convention:

```text
data/synthetic_drafts/<run_id>/
  raw_cases.jsonl
  cases.jsonl
  invalid_samples.jsonl
  metadata.json
  validation_report.txt
  distribution_report.md
```

## Scope Guardrails

No model training, DeepSeek API integration, large model downloads, UI, complex evaluation, or real coding-agent integration is included in this setup.

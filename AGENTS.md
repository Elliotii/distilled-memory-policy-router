# Codex Working Guidelines

This repository is a Python research-engineering project for the Distilled Memory Policy Router for Coding-Agent Contexts.

## Required Reading

- Before starting any task, read `docs/planning/lightweight_memory_policy_router_project_spec.md`.
- Treat that project spec as the source of truth for scope, schema, validation, and MVP boundaries.
- Do not change the core direction of the project spec unless there is an obvious contradiction.

## Project Scope

- This project studies only the memory policy router.
- It is not a complete coding agent.
- It is not a RAG system.
- It is not a Memory OS.
- New functionality should stay small, scoped, and verifiable.

## Router Contract

- The router predicts only:
  - `read_hints`
  - `write_spans`
  - `ignore_spans`
- The router does not predict final rewritten memory content, update/delete/merge operations, project IDs, confidence scores, `needs_review`, offsets, or downstream agent actions.
- Schema examples and dataset records must use `target`; do not use `expected_output`.

## Dataset Rules

- Dataset content must be English.
- `candidate_memories` must contain 0-8 items.
- `recent_context` must contain 0-4 turns.
- Every `read_hints` entry must reference an `id` present in `candidate_memories`.
- Every `write_spans[*].span` must be an exact substring of `current_user_input`.
- Every `ignore_spans` span must be an exact substring of `current_user_input`.
- Validator success means structural validation only; it does not prove semantic label quality.
- After every change to `data/*.jsonl`, run the validator.

## External Services and Models

- Do not connect to the DeepSeek API unless explicitly requested.
- Do not connect to any real API unless explicitly requested.
- Do not train models unless explicitly requested.
- Do not download large models.
- Do not build UI.

## Git Hygiene

- Do not commit virtual environments, caches, local OS files, checkpoints, downloaded models, generated outputs, wandb runs, logs, or large temporary generated files.
- Specifically keep these ignored:
  - `.venv/`
  - `__pycache__/`
  - `.DS_Store`
  - `checkpoints/`
  - `models/`
  - `outputs/`
  - `wandb/`
  - `*.log`
  - `*.pyc`
- Small seed data, prompt docs, validation reports, and distribution reports may be committed.

## Completion Report

At the end of each task, report:

- Files changed.
- Commands run.
- Validation results.
- Category/type distribution, if data was changed or analyzed.
- Recommended next steps.

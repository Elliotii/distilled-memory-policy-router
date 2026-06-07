# Project Overview

## Summary

The Lightweight Memory Policy Router is a research-engineering project for a narrow agent-memory control problem: deciding which fixed candidate memories should be read into context and which current units should be stored or skipped. It is designed for coding and business-agent settings where durable project facts, user preferences, decisions, and task progress matter, but unmanaged memory can pollute future sessions.

The project is intentionally scoped as a policy layer. It is not a memory database, retrieval system, memory writer, or end-to-end agent framework.

## Motivation

Agent memory has a practical failure mode: remembering too much can be as harmful as remembering too little. A useful agent should preserve durable facts and progress, but it should avoid storing temporary errors, stale details, credentials, and irrelevant chatter. It should also avoid reading every possible memory into the next prompt, because irrelevant context wastes tokens and can steer the answerer away from the current task.

This project isolates that policy decision. Given already-supplied candidate memories and already-extracted current units, the router predicts:

- READ: which candidate memories should be injected into context.
- STORE: which current units should become durable memory.
- SKIP: which current units should be ignored.
- Target: where each STORE unit belongs.

## System Role

The router sits between candidate-memory retrieval or collection and downstream memory consumption:

```text
fixed candidate memories + current units
        |
        v
memory policy router
        |
        v
READ / STORE / SKIP + STORE target
        |
        +--> context builder
        +--> writer stub or memory pipeline
```

The router does not perform retrieval. It assumes a small candidate set has already been supplied. It also does not perform final memory writing. A downstream writer or memory pipeline can consume the STORE decisions, but rewriting, merging, deduplication, deletion, truth checks, and lifecycle management are outside this project.

## Task Formulation

The v0.4/v0.5 task uses unit-level decisions.

Inputs:

- Candidate memories with IDs and text.
- Current units from the latest user/task context.

Outputs:

- READ memory IDs.
- STORE unit IDs.
- SKIP unit IDs.
- A STORE target for every stored unit.

Valid STORE targets:

| Target | Meaning |
| --- | --- |
| `task_state` | Current progress, blockers, next steps, active investigations, and task-local state. |
| `service_memory` | Durable facts about a service, component, parser, evaluator, module, or subsystem. |
| `repo_memory` | Repository-level commands, tests, paths, structure, conventions, or codebase facts. |
| `project_memory` | Project-level goals, decisions, cross-repo agreements, and shared constraints. |
| `user_profile` | Stable, non-sensitive user preferences that transfer across tasks or projects. |

## Phase Evolution

### v0.3: JSON/span policy contract

The canonical project spec defined a compact router contract using `read_hints`, `write_spans`, and `ignore_spans`. This framed the core research question: can a small router learn memory-policy decisions that reduce noisy writes and irrelevant reads?

### v0.4: Unit-based interface

Later work moved toward explicit current units and candidate-memory IDs. This reduced span-copying ambiguity and made parser/evaluator behavior easier to test. The core decision remained the same, but the operational interface became READ / STORE / SKIP over IDs.

### v0.5: Small-model training and evaluation

The v0.5 series trained and evaluated Qwen-family small routers using Unit JSON. The project compared QLoRA and BF16 LoRA variants and used locked `gold_v2_009` for controlled evaluation.

### v0.5g: Best current result

The best evaluated system on locked `gold_v2_009` by exact match and write-side routing metrics among the compared systems is BF16 standard LoRA r16 with 1000 targeted-balanced training cases under RTX 4090 fallback settings. It achieved 36.0% exact match, 99.0% STORE F1, 98.1% SKIP F1, and 100.0% STORE target accuracy. READ F1 was not available for older v0.5e anchors, so this should not be read as a global READ-superiority claim.

## What Was Learned

The strongest result is write-side routing. With 1000 targeted-balanced examples, the router nearly solves STORE/SKIP and target classification on the controlled gold set. False stores drop from 10.4% in the BF16 500-control run to 1.2% in the BF16 1000-targeted run.

READ selection remains harder. The best run reaches 84.6% READ F1 on gold, with 64 irrelevant reads and 63 missed reads. This limits full exact match to 36.0%. The project therefore supports a clear research conclusion: write-side routing can be learned well under this setup, while READ requires better relevance modeling than the current entity-matching-heavy training regime provides.

## Non-Goals

This project does not attempt to:

- Build a complete Memory OS.
- Build an unbounded memory retriever.
- Build a vector database, BM25 stack, or RAG pipeline.
- Build a full coding agent.
- Implement memory update, delete, merge, decay, canonicalization, or truth verification.
- Prove production safety.
- Prove downstream agent utility.

## Current Status

The repository is in v1.0 packaging. The current work is focused on making the project readable, reproducible, and suitable for portfolio review without changing the locked experiments.

The next planned packaging steps are architecture documentation, demo fixtures without model inference, a downstream-lite efficiency proxy over existing artifacts, and resume/interview notes.

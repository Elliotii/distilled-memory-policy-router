# Related Work Positioning

## Summary

This document positions the Memory Policy Router relative to neighboring system categories. It is not a literature survey and does not claim superiority over broader memory systems. The project isolates a narrow policy layer: given fixed candidate memories and current units, decide READ / STORE / SKIP and assign STORE targets.

## RAG / Retrievers

Retrieval-augmented generation systems focus on finding relevant documents or memory records from a larger collection. They usually include indexing, ranking, chunking, query construction, and context assembly.

This project assumes the retrieval step has already produced a small candidate set. It then asks a different question: among these candidates, which should actually be read into the current context, and which current units should be stored or skipped?

| RAG / retriever focus | Memory Policy Router focus |
| --- | --- |
| Search over a large corpus or memory store. | Decide over a fixed candidate set. |
| Optimize retrieval ranking or recall. | Optimize READ / STORE / SKIP policy accuracy. |
| Return chunks or documents. | Return memory IDs and unit decisions. |
| Often coupled to answer generation. | Evaluated as a standalone control-plane component. |

The router is complementary to retrievers. A future memory pipeline could use a retriever to provide candidates, then use the router to control context injection and durable-write decisions.

## Long-Term Memory Systems And MemoryOS-Style Runtimes

Long-term memory runtimes typically manage many parts of the memory lifecycle:

- storage;
- retrieval;
- indexing;
- ingestion;
- update and evolution;
- deletion or decay;
- access control;
- integration with an agent loop.

EverOS and EverOS-style systems are examples of complete memory-runtime approaches: their scope is the broader runtime that stores, retrieves, indexes, ingests, and evolves memory over time. One public reference point is [EverOS](https://github.com/EverMind-AI/EverOS).

This project takes a narrower role. It does not provide storage, indexing, retrieval, ingestion, memory evolution, or an agent loop. It studies the policy decision that could sit inside or beside such a runtime:

```text
given candidates + current units
        |
        v
decide READ / STORE / SKIP
```

That makes the router complementary to memory runtimes rather than a replacement for them.

## Memory Write Policies

Memory write policies decide what should become durable memory. This is important because bad writes can persist and degrade future sessions. Common write-policy concerns include:

- temporary events that should not be stored;
- stale facts after corrections;
- sensitive or private content;
- task state that is useful now but may expire later;
- durable facts, decisions, and preferences that should be remembered.

This project treats write policy as a supervised routing problem over current units. The router predicts STORE or SKIP, and for STORE units it predicts one of five targets:

- `task_state`
- `service_memory`
- `repo_memory`
- `project_memory`
- `user_profile`

The router does not perform the final write. It does not rewrite text, merge duplicates, check truth, or decide deletion. A separate writer or memory runtime would still be needed.

## Small-Model Routers And Rerankers

Small routers and rerankers are often used to make cheap control decisions before invoking larger systems. They can reduce cost or noise by filtering, classifying, or prioritizing inputs.

The Memory Policy Router follows this pattern. It uses a small fine-tuned model to make structured policy decisions before a downstream context builder or memory writer consumes the result.

The v0.5g result suggests this is especially effective for write-side routing under the controlled benchmark: STORE F1 reaches 99.0%, SKIP F1 reaches 98.1%, and STORE target accuracy reaches 100.0% on locked `gold_v2_009`. READ selection remains less solved, which is consistent with READ behaving more like a relevance-ranking problem than a surface-policy classification problem.

## Relationship To Agent Memory Pipelines

A complete agent memory pipeline might look like:

```text
conversation / task context
        |
        v
candidate retrieval + unit extraction
        |
        v
memory policy routing
        |
        +--> context injection
        |
        +--> durable memory writer
        |
        v
agent answer or next action
```

This project covers only the memory policy routing box. It intentionally leaves the surrounding boxes fixed, external, or future work.

## What This Project Does Not Claim

This project does not claim that:

- it replaces retrievers;
- it replaces long-term memory runtimes;
- it is better than EverOS or any other MemoryOS-style system;
- it proves downstream agent utility;
- it proves production safety;
- READ selection is solved.

The strongest supported claim is narrower: under a controlled locked benchmark, a small LoRA-tuned router can learn the write side of READ / STORE / SKIP policy routing well, while READ selection remains the main open problem.

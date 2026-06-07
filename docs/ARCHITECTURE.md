# Architecture

## Summary

The Memory Policy Router is a small policy layer for coding and business-agent memory pipelines. It receives a bounded set of candidate memories and a bounded set of current units, then predicts READ, STORE, and SKIP decisions. The router is learned; retrieval, unitization, context construction, final memory writing, and memory lifecycle management stay outside the learned component.

```text
Candidate Memory Provider
       |
       v
candidate memories m1...mk

Current Unitizer
       |
       v
current units u1...un

       |
       v
Memory Policy Router
       |
       v
READ memory ids
STORE unit ids + targets
SKIP unit ids

       |
       v
Context Builder / Memory Writer Stub
```

## System Boundary

The system boundary is deliberately narrow:

| Inside this project | Outside this project |
| --- | --- |
| Router input/output schema | Unbounded memory retrieval |
| READ / STORE / SKIP policy prediction | Memory database implementation |
| STORE target classification | Canonical memory rewriting |
| Parser and evaluator behavior | Update, delete, merge, decay, or truth verification |
| Offline intrinsic evaluation | End-to-end agent runtime |
| Error and limitation analysis | Production safety guarantees |

The router answers one question: given the candidate memories and current units already in front of it, what should be read, stored, or skipped?

## Components

### Candidate Memory Provider

The candidate memory provider supplies a small set of memory records. In v0.5 evaluation, the router does not choose this set from a larger memory database. The provider is fixed by the dataset or harness.

Conceptually, each candidate memory has:

- a stable memory ID;
- memory text;
- optional metadata used by the dataset or evaluator.

### Current Unitizer

The unitizer supplies current units from the latest user/task context. The v0.5 router predicts over unit IDs rather than raw text spans. This makes the output easier for a small model to learn and easier for the evaluator to compare.

The unitizer is not the research target in v0.5/v1.0 packaging. It is assumed to have already produced units before routing begins.

### Memory Policy Router

The router is the learned component. It receives candidate memories and current units, then predicts:

- READ memory IDs;
- STORE unit IDs;
- SKIP unit IDs;
- one target for every STORE unit.

The current best evaluated v0.5g router is BF16 standard LoRA r16 with 1000 targeted-balanced training cases under RTX 4090 fallback settings. That result is strongest on the write side: STORE, SKIP, and target classification.

### Parser and Evaluator

The parser turns model output into a canonical structured object. The evaluator compares that object against locked labels and reports exact match, parse success, component F1 metrics, target accuracy, and pollution/safety signals.

The parser does not semantically repair bad predictions. Validation success means structural validity, not semantic quality.

### Context Builder / Memory Writer Stub

Downstream systems can consume READ decisions to decide which memories enter context. A writer stub can consume STORE decisions and targets. In this project, those downstream pieces are fixed or conceptual. They are not intelligent memory writers.

## READ Path

The READ path decides which candidate memories are relevant enough to inject into context.

```text
candidate memories
       |
       v
router READ decision
       |
       v
selected memory IDs
       |
       v
context builder
```

READ is the hardest remaining part of the v0.5g result. The best gold run reaches 84.6% READ F1 and still has 64 irrelevant reads and 63 missed reads. Each READ error can break full exact match, so READ dominates the remaining exact-match gap.

## STORE/SKIP Path

The STORE/SKIP path decides which current units should enter durable memory handling and which should be ignored.

```text
current units
       |
       v
router STORE/SKIP decision
       |
       +--> STORE unit IDs + target
       |
       +--> SKIP unit IDs
```

STORE units also receive one target:

- `task_state`
- `service_memory`
- `repo_memory`
- `project_memory`
- `user_profile`

The v0.5g 1000-targeted run performs strongly here: on locked `gold_v2_009`, STORE F1 is 99.0%, SKIP F1 is 98.1%, and target accuracy is 100.0%.

## What Is Fixed vs Learned

| Part | Fixed or learned | Notes |
| --- | --- | --- |
| Candidate memory set | Fixed | Supplied by dataset or future harness. |
| Current units | Fixed | Unitization is assumed before routing. |
| Router model | Learned | Small Qwen-family router fine-tuned with LoRA variants. |
| Output parser | Fixed | Structural parsing and validation. |
| Evaluation labels | Fixed | Locked dev/gold targets. |
| Context builder | Fixed/conceptual | Consumes READ IDs; not the research target here. |
| Writer stub | Fixed/conceptual | Consumes STORE units; no rewrite or merge intelligence. |

## Runtime Assumptions

The v0.5/v1.0 architecture assumes:

- candidate memories are already available and bounded;
- current units are already extracted;
- STORE targets are limited to the five documented classes;
- the router does not call tools or APIs at decision time in the offline evaluation;
- the parser validates structure, not semantic truth;
- adapter weights are external artifacts and are not committed to git.

## Why This Is A Policy Layer, Not MemoryOS

This project isolates one policy decision inside a larger memory system. A complete memory runtime would need storage, indexing, retrieval, ingestion, update logic, deletion, compaction, privacy controls, and integration with an agent loop. This router does not provide those functions.

The intended role is complementary: a retriever or memory runtime can provide candidates, and the router can decide how those candidates and current units should be handled.

## Current v0.5/v1.0 Limitations

- The benchmark is controlled and synthetic.
- Candidate memories are fixed, so retrieval quality is not evaluated.
- The router does not write final memory text.
- The router does not update, delete, merge, deduplicate, decay, or verify memories.
- No downstream agent validation has been measured yet.
- READ selection remains the dominant remaining failure mode.
- The best result comes from BF16 standard LoRA r16 plus 1000 targeted-balanced data; BF16 alone was not sufficient.
- The v0.5g result uses RTX 4090 fallback settings and should be described that way.


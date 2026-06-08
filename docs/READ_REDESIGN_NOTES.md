# READ Redesign Notes

## Summary

READ should be reframed from binary per-memory classification into a retrieval and selection problem. The current intrinsic READ task is useful, but it is not the right production frame by itself.

Two tracks should guide final v1.0-applied and later work:

1. Portfolio track: retrieve -> rerank/score -> budgeted-select cascade, tested on a small hard-candidate eval.
2. Research/interview track: counterfactual-utility-grounded relevance, where the principled READ label asks whether including or removing a memory improves downstream answer quality.

## Why Binary Per-Memory READ Classification Is The Wrong Production Frame

In production-like memory systems, READ is not usually a standalone binary decision over a tiny clean list. It is a cascade:

```text
memory store
  -> retriever candidate set
  -> reranker or scorer
  -> budgeted selector
  -> downstream context
```

The binary label hides important decisions:

- how candidates were retrieved;
- how many memories can fit in budget;
- whether a memory is required, helpful, redundant, or harmful;
- whether a near duplicate should be selected;
- whether the answer changes if the memory is omitted.

## Why Candidate Pool Degeneracy Matters

The current benchmark often has small candidate pools and low distractor density. This can make simple ordering or entity matching look stronger than it should. It also weakens the case for learned READ, because the selector is not forced to reject hard negatives.

Hard READ evaluation should include:

- same-entity irrelevant memories;
- stale memories;
- contradictory memories;
- wrong-scope memories;
- near duplicates;
- sensitive-boundary items.

## Why Graded Relevance And Hard Negatives Matter

READ is not just relevant vs irrelevant. Useful categories include:

- required;
- helpful;
- redundant;
- irrelevant;
- stale or harmful;
- contradictory;
- wrong scope.

Hard negatives matter because they test whether the selector understands the task, not just the entity names.

## Why Embedding Similarity May Be The Honest Default READ Baseline

For applied READ, embedding or BM25 retrieval may be the right baseline. If a learned router cannot beat a simple semantic similarity baseline on hard candidate pools, then learned READ should not be presented as the main contribution.

This does not weaken the project. It sharpens the contribution:

- learned STORE/SKIP/target policy remains valuable;
- READ can become a reranking or budgeted selection layer;
- the harness can reveal when learned routing adds value and when it does not.

## Why Learned READ May Be Optional

Learned READ should be optional if it does not beat embedding/BM25 baselines. Possible final architecture:

```text
BM25 or embedding retrieval
  -> optional learned reranker/router
  -> budgeted context builder
  -> audit trace
```

The model should earn its place by improving answer quality or reducing contamination under hard negatives.

## Counterfactual-Utility-Grounded Relevance

The principled READ label is not simply "does this memory mention the same entity?" It is:

> Does including this memory, compared with removing it, improve the downstream answer?

This implies a better research target:

- construct pairs with and without a memory;
- judge answer quality and contamination;
- label memories by counterfactual contribution;
- train or evaluate rerankers against that signal.

This is more expensive than intrinsic labeling, so it belongs to later research/interview framing rather than the minimum v1.0-applied harness.

## Interview Explanation

Suggested explanation:

> The project found an asymmetry. STORE/SKIP and target routing are learnable under the current setup, but READ is closer to retrieval/reranking than classification. I would not keep chasing READ exact on the old benchmark. I would build a hard-candidate eval with stale, contradictory, wrong-scope, and near-duplicate memories, then compare BM25, embedding, random, all-candidates, and learned selection on answer quality and contamination. If embedding wins, that is a useful architecture result: use embeddings for READ and keep the learned router for write-side policy.

## What Not To Do

Do not:

- chase current READ exact as the main success target;
- run more LoRA sweeps only for READ;
- build a large vector database for v1.0;
- do large-scale learning-to-rank before a small hard eval exists;
- claim READ is solved.

## Practical Redesign For v1.0-Applied

Minimum applied design:

1. Use BM25/keyword retrieval to create 8-15 candidates.
2. Run simple baselines and optional learned selection over the same candidates.
3. Build budgeted context.
4. Emit audit trace.
5. Score required recall and contamination.
6. Review answer quality on a small hard READ set.

This produces a more honest applied result than more intrinsic READ exact tuning.

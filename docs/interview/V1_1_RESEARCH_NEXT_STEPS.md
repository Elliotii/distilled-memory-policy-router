# v1.1 Research Next Steps

## Why v1.1 Should Focus On Contradiction-Aware READ

v1.0-applied showed strong selection-level transfer but limited downstream transfer. The key downstream failure mechanism was not just generic noise. It was missed required memories plus contradictory memory contamination. On the 8-case downstream slice, learned_router required recall was 0.6875, with avoid injected 8, contradictory injected 5, and stale injected 1.

That means the next version should not jump to UI, serving, or broad product packaging. It should improve READ selection under hard negatives.

## Proposed Architecture

```text
retrieve -> relevance -> contradiction check -> budget select
```

The key change is to separate relevance from consistency. A memory can be highly relevant but still contradictory, stale, or unsafe to inject. The selector should not treat high topical overlap as enough.

## Candidate Approaches

### Contradiction-Aware Reranker

Add a reranking stage that scores candidate memories not only by relevance to the task, but also by contradiction risk against the current task and other selected memories.

### Abstention / Confidence Threshold

If the selector cannot distinguish required memory from contradictory hard negatives, it should abstain or lower confidence instead of filling the budget with risky candidates.

### Hard-Negative READ Training

Expand training data with labels that explicitly distinguish required memories from near-duplicate, stale, wrong-scope, and contradictory candidates. Do this only after contradiction labels are defined.

### Pairwise Memory Consistency Check

Check pairs or sets of selected memories for inconsistency before final budget selection. This can catch cases where one required memory and one contradictory memory are both selected.

### Downstream-Aware Eval Expansion

Expand downstream evaluation only after defining contradiction and missed-required labels. The next eval should ask whether the answerer follows the correct memory when conflicting memory is also present.

## What Not To Do

- Do not jump to UI.
- Do not claim production readiness.
- Do not expand aimlessly.
- Do not retrain before defining contradiction labels.
- Do not treat small 8-case downstream differences as robust rankings.
- Do not claim general downstream utility until larger rubric-reviewed downstream evaluation supports it.

## Success Criteria

v1.1 should reduce missed required memories and contradictory contamination together. A useful target is not just higher selection recall, but fewer downstream responses that follow contradictory memory while preserving required fact coverage.

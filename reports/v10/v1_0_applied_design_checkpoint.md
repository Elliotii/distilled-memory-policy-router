# v1.0-Applied Design Checkpoint

## Context

This report summarizes Context 7.1: Thesis Reframe and Applied Memory Harness design docs.

The current base is the `v1.0-eval checkpoint`, which freezes evaluation, benchmark, reproducibility, and portfolio artifacts. That checkpoint is valuable but is not final v1.0. The next stage is final v1.0-applied design and, later, harness implementation.

No API calls, model inference, Qwen/LoRA loading, training, new benchmark execution, harness implementation, or git tagging were performed in this design context.

## Files Created

- `docs/THESIS_REFRAME.md`
- `docs/APPLIED_MEMORY_HARNESS.md`
- `docs/HARD_READ_EVAL_PLAN.md`
- `docs/READ_REDESIGN_NOTES.md`
- `reports/v10/v1_0_applied_design_checkpoint.md`

## Current State After v1.0-Eval Checkpoint

Current evidence:

- Best evaluated router: BF16 LoRA r16 + 1000 targeted-balanced data under RTX 4090 fallback settings.
- Locked `gold_v2_009`: exact 36.0%, parse 99.3%, READ F1 84.6%, STORE F1 99.0%, SKIP F1 98.1%, target accuracy 100.0%, false store rate 1.2%, sensitive store 0/4 under semantic metric.
- BF16 alone was not sufficient.
- Write-side routing is the strongest learned result.
- READ remains unresolved.
- Downstream-lite proxy and micro-pilot did not establish router-specific downstream superiority.

## Final v1.0-Applied Target

Final v1.0-applied should add:

- Applied Memory Harness.
- Hard-candidate READ evaluation.
- Audit trace.
- Baseline comparison.
- Optional live LoRA.
- Optional Streamlit trace viewer.

The minimum applied target is a CLI plus JSON trace harness that shows the full memory-policy path from user input to candidate retrieval, selection, budgeted context, STORE/SKIP preview, and audit trace.

## Key Design Decisions

1. Reframe the thesis around decomposition and evidence, not blanket improvement.
2. Treat STORE/SKIP/target as the strongest learned component.
3. Treat READ as unresolved relevance selection.
4. Use hard candidate pools with 8-15 memories per case for future READ evaluation.
5. Compare learned selection against honest baselines: no-memory, all-candidates, BM25/keyword, embedding if feasible, random-k, and oracle.
6. Make JSON audit traces the required v1.0-applied artifact.
7. Keep Streamlit optional and defer FastAPI + React.
8. Keep STORE as preview/gated output, not automatic durable writes.
9. The harness design allows READ selection and WRITE policy to be decoupled, so learned routing can remain focused on the write side if simple READ baselines perform better.

## Risks

- Hard READ case quality may be too weak if distractors are not realistic.
- Live LoRA environment may add setup risk and should remain optional until trace replay works.
- Scope creep could turn the harness into a full agent project.
- Overclaiming risk remains high if proxy or micro-pilot results are summarized without their limits.

## Explicit Do-Not-Claim List

Do not claim:

- Downstream utility proof.
- Production safety.
- Real retriever performance.
- Real cost savings.
- Complete MemoryOS.
- That the router beats all baselines.
- That READ is solved.

## Next Context Recommendation

Next context should be:

```text
Context 7.2 — Applied Memory Harness skeleton implementation
```

Implementation should start with schemas, fixtures, deterministic baselines, and JSON trace emission. It should not start with live LoRA or UI.

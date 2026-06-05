# v05g Repaired Training Data — Known Limitations

**Date:** 2026-06-05  
**Source:** Opus 4.8 final semantic review  
**Status:** Documented limitations — see claim boundaries for what NOT to claim

## 1. READ Is Entity Matching, Not Semantic Relevance Reasoning

**Finding:** In the additional 500, READ labels are recoverable from prompt-visible content but the prediction task collapses to service/repo entity-name matching.

- A pure rule `READ iff memory text contains runtime service or repo name` achieves **100% READ accuracy** on the additional 500.
- The data does **not** teach graded context selection (e.g., "this memory is partially relevant" or "this memory is relevant despite not mentioning the service by name").
- The data does **not** teach semantic relevance reasoning (e.g., "the task is about debugging, so read the debugging SOP memory even though it mentions a different service").

**Implication:** A model trained on this data may learn to read memories that mention its current service, but may not generalize to cases where a memory is semantically relevant without lexical overlap.

**Mitigation:** The 500-control dataset contains project_memory READ at 89.7% (70/78), providing some exposure to cross-service project-level memory reads.

## 2. Prefix Shortcut Reduced But Not Eliminated

**Finding:** Opener diversification reduced 3-word-prefix accuracy from 100% to 90.9%, but prefix separability persists at longer window sizes.

| Prefix length | Accuracy |
|---------------|----------|
| 3 words | 90.9% |
| 6 words | 97.5% |
| 10 words | 99.6% |

**Interpretation:** "Body-dependent routing" in the additional 500 mostly means reading a short templated tail (a few additional words), not full-context reasoning across long unit texts.

**Implication:** A model may attend primarily to the first 6-10 words of a unit rather than its full content.

**Mitigation:** The neutral-opener templates deliberately mix STORE and SKIP openers. The remaining separability is partly driven by semantically justified patterns (sensitive content → SKIP, stale → NOT READ).

## 3. project_memory READ = 0% in Additional 500

**Finding:** In the additional 500, all project_memory candidate memories are cross-domain distractors (0% READ). The model receives no training signal to read project-level memories.

**500-control mitigation:** The 500-control contains 78 project_memory candidates with 89.7% READ rate. This provides project-level READ exposure, but only within the 500-control's domain set (17 projects different from the additional 500's 8 projects).

**Implication:** v05g combined 1000 does train project_memory READ (via 500-control), but the additional 500 contributes 0 project_memory READ examples. A model trained on 1000 may have weaker project-level memory reading than expected.

## 4. 1000-vs-500 Is Data Volume + Domain Breadth, Not Pure Volume

**Finding:** The 500-control and additional 500 differ not only in size but in:
- Domain families (17 projects vs 8 entirely different projects)
- Template families (original v05b generation vs repaired template generation)
- Construction methodology (historical QLoRA data vs targeted-balanced repair)

**Interpretation:** If BF16 r16 1000 outperforms BF16 r16 500, the cause could be:
- More training examples (data volume)
- Broader domain coverage (8 new business domains)
- Different template/opener diversity
- Or any combination of the above

**Do NOT claim:** "1000 examples are better than 500" as a pure data-volume causality.

**DO claim:** "BF16 r16 1000, which adds 500 targeted-balanced examples across 8 new domains to the 500-control baseline, shows [result] vs BF16 r16 500."

## 5. Additional 500 Is Template-Generated Synthetic Data

**Finding:** The additional 500 is entirely template-generated with programmatic semantic repair. It has not been human-reviewed for edge-case quality.

**Implications:**
- Template artifacts may exist that are not caught by structural validation
- Semantic diversity is bounded by template variety (14-15 variants per template pool)
- Real-world deployment scenarios may differ substantially from template-generated patterns

## 6. No Claim of Downstream Utility or Deployment Realism

v05g is a controlled LoRA scaling experiment. It tests whether:
1. BF16 standard LoRA improves over QLoRA with the same data
2. More targeted-balanced data (with broader domains) improves outcomes

**Do NOT claim from v05g:**
- Production readiness
- Superiority over DeepSeek V4 Pro/Max
- Generalization to real-world coding-agent memory policy
- The router solves agent memory management
- Statistical significance (too few runs)
- Cross-model generalization

## Summary Table

| Limitation | Severity | Mitigated? |
|-----------|----------|------------|
| READ = entity matching | Medium | 500-control has project_memory READ (89.7%) |
| Prefix shortcut at 6-10 words | Medium | Neutral openers added; 90.9% at 3 words |
| project_memory READ = 0% in additional 500 | Low | 500-control covers project_memory READ |
| 1000-vs-500 confound | Medium | Documented; interpret as data + domain breadth |
| Template-generated synthetic | Low | Acceptable for LoRA scaling hypothesis |

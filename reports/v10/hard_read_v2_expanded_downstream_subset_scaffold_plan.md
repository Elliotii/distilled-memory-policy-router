# Hard READ v2 Expanded Downstream Subset Scaffold Plan

Context: 7.5-B prompt-pack scaffold for the expanded v2 downstream subset.

## Selected Subset Overview

- Selected cases: `hard_read_v2_009`, `hard_read_v2_026`, `hard_read_v2_011`, `hard_read_v2_020`, `hard_read_v2_013`, `hard_read_v2_014`, `hard_read_v2_031`, `hard_read_v2_032`
- Case count: 8
- Strategies: `no_memory`, `all_candidates`, `budgeted_candidate_order`, `keyword_top_k`, `random_k`, `oracle_selected`
- Prompt count: 48

## Domain Coverage

- coding/service implementation: `hard_read_v2_009`
- customer-support/CRM workflow: `hard_read_v2_013`
- data/privacy/compliance: `hard_read_v2_011`
- documentation/process-agent: `hard_read_v2_032`
- observability/SRE: `hard_read_v2_031`
- product/business process: `hard_read_v2_020`
- repo validation / CI: `hard_read_v2_026`
- security/auth: `hard_read_v2_014`

## No API Boundary

This context builds prompt scaffolding only. It does not call DeepSeek or any external model, run model inference, load Qwen or LoRA, train, implement live LoRA, build UI, or collect downstream responses.

## Bridge From Selection Eval to Later Micro-Pilot

The subset converts selected rows from the 32-case selection-only eval into prompt, response-template, and manual-review-template rows. It keeps all labels local to metadata for scoring and keeps prompt text limited to current task context plus post-budget injected memory context.

## Scorer Compatibility

`scripts/score_hard_read_downstream_responses.py` remains compatible because prompt rows preserve injected, required, helpful, avoid, stale, contradictory, and wrong-scope IDs in local metadata while response rows use the existing empty `not_run` template shape.

## Claim Boundaries

This scaffold does not measure downstream answer quality, prove downstream utility, evaluate learned router/live LoRA behavior, establish production memory-system behavior, or show that any routing approach outperforms alternatives.

## Next Recommendation

Inspect prompt quality and leakage checks before any API response collection. If inspection passes, a later context can run a small API micro-pilot only with explicit approval.

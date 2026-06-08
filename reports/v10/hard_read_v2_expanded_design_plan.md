# Hard READ v2 Expanded Design Plan

Context: 7.5-A expanded v2 hard READ selection-only diagnostic fixture.

## Why Expand After 7.4-G

The v2 pilot addressed the two main v1 fixture risks. Candidate order was fixed-seed shuffled rather than label ordered, and downstream rubric review showed `no_memory` responses were cleaner but under-specified when exact commands, thresholds, keys, or implementation constraints lived only in memory.

The 7.4-G synthesis supported expanding v2 to a larger diagnostic set before any API expansion or live LoRA/backend integration. The expanded set increases coverage from 8 to 32 cases while preserving the same fixture principles.

## Why This Remains Selection-Only

This context validates fixture shape and deterministic memory-selection behavior only. It does not collect downstream answers, call DeepSeek or any external API, run model inference, load Qwen or LoRA, train, implement live LoRA, or build UI.

Selection-only evaluation is the right next step because the fixture needs stable hard-candidate behavior before response collection or backend integration. The only outputs here are expanded cases, intrinsic memory records, fixture audit reports, and deterministic selection metrics.

## Design Requirements

- Preserve the original 8 v2 pilot cases as `hard_read_v2_001` through `hard_read_v2_008` without modifying the original pilot files.
- Add 24 new cases, `hard_read_v2_009` through `hard_read_v2_032`.
- Use 8-12 candidate memories per case, with 10 as the default.
- Keep relevance labels case-local under `labels`.
- Keep the memory pool intrinsic only: no `relevance_category` or `hard_negative_type` fields in memory records.
- Use fixed-seed shuffled candidate order rather than label ordering.
- Avoid consistently front-loading required/helpful memories.
- Keep prompt-facing `user_input` and `current_units` under-specified; exact commands, thresholds, deadlines, keys, and implementation constraints should live in memory and expected requirements, not in task notes.
- Include realistic hard negatives: same-entity irrelevant memories, stale or harmful memories, contradictions, wrong-scope memories, near duplicates, and sensitive-boundary distractors where appropriate.

## Case and Domain Coverage Plan

The expanded fixture mixes coding-agent and business-agent scenarios:

- Coding/service implementation: inventory reservation expiry, refund idempotency, address fallback.
- Repo validation / CI: retry classification, visual snapshot gate, flaky-test quarantine.
- Data/privacy/compliance: consent export suppression, PII redaction, analytics IP truncation.
- Product/business process: enterprise beta rollout, seller verification, collections outreach.
- Customer-support/CRM workflow: enterprise refund routing, renewal-risk handoff, refund macro suppression.
- Security/auth: MFA recovery-code rotation, admin session idle timeout, API key display behavior.
- Observability/SRE: checkout latency paging, ingest lag alerting, CDN purge alerts.
- Documentation/process-agent: release-note approval, breaking-change checklist, P1 runbook owners.

The original 8 pilot cases remain in the expanded set, so the final coverage includes both prior v2 diagnostics and broader new scenarios.

## Claim Boundaries

This fixture expansion is diagnostic. It does not measure downstream answer quality, task success, real-world retrieval quality, production safety, learned router/live LoRA behavior, or business impact. Oracle selection is a labeled reference condition for fixture inspection only.

These artifacts should not be used to claim downstream utility, production readiness, or that any routing approach outperforms alternatives.

## Next Step

After this context, the recommended next step is to inspect expanded selection metrics and choose a smaller downstream response subset from the 32-case fixture. API response collection should remain separate and should only happen in a later context with explicit approval.

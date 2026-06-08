# Hard READ v2 Expanded Fixture Audit

## Summary

- OK: true
- Case count: 32
- Memory count: 320
- Unique case count: 32
- Unique memory count: 320

## Candidate Count Distribution

- 10 candidates: 32 cases

## Domain Distribution

- coding/service implementation: 3
- customer-support/CRM workflow: 3
- data/privacy/compliance: 3
- documentation/process-agent: 3
- observability/SRE: 3
- product/business process: 3
- repo validation / CI: 3
- security/auth: 3
- unspecified: 8

## Hard Negative Type Distribution

- contradictory: 32
- near_duplicate: 63
- none: 96
- same_entity_irrelevant: 64
- sensitive_boundary: 2
- stale: 31
- wrong_scope: 32

## Candidate-Order Diagnostic

- Mean first-four required recall: 0.062
- Max first-four required recall: 0.500
- Distribution:
  - 0.00: 28 cases
  - 0.50: 4 cases

## Errors

- None.

## Warnings

- None.

## Boundary

This audit is structural and selection-fixture focused. It does not evaluate downstream answer quality, call an API, run model inference, train, load Qwen or LoRA, or establish production memory-system behavior.

# Learned-Router Downstream Prompt Inspection

## Summary

- Prompt rows: 8
- Case coverage: hard_read_v2_009, hard_read_v2_026, hard_read_v2_011, hard_read_v2_020, hard_read_v2_013, hard_read_v2_014, hard_read_v2_031, hard_read_v2_032
- Injected memory count distribution: {2: 1, 3: 5, 4: 2}
- Prompt leakage findings: PASS
- API recommendation: PASS - prompt pack is ready for the 8-prompt learned_router API run.

## Case Selection Diagnostics

| case_id | injected count | required recall | avoid injected | contradictory injected | stale injected | wrong-scope injected | sensitive-boundary injected |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hard_read_v2_009` | 4 | 1.00 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_026` | 3 | 0.50 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_011` | 4 | 0.50 | 2 | 1 | 1 | 0 | 0 |
| `hard_read_v2_020` | 3 | 0.50 | 1 | 0 | 0 | 0 | 0 |
| `hard_read_v2_013` | 3 | 1.00 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_014` | 2 | 1.00 | 0 | 0 | 0 | 0 | 0 |
| `hard_read_v2_031` | 3 | 0.50 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_032` | 3 | 0.50 | 1 | 0 | 0 | 0 | 0 |

## Prompt Leakage Checks

- No label field names found in prompt text.
- No oracle/gold/benchmark internals found in prompt text.
- No bracketed current-unit citations found in prompt text.
- No strategy names, AutoDL paths, or model paths found in prompt text.

## Prompt Shape Inspection

All prompts follow the existing expanded downstream subset style: task context, current task notes, prior memory context with bracketed memory IDs, citation rules, and the 2-4 concise bullets/sentences instruction.

Example prompt excerpt:

```text
Write 2-4 concise bullets or sentences, 120 words or fewer.

Project: inventory-platform
Repo: stockflow
Service: inventory-api
Task: Patch inventory reservation expiry handling

Current task notes:
- Patch inventory-api reservation expiry handling.
- Include the repo validation step before handoff.
- Keep guidance scoped to the current reservation flow.

Prior memory context:
[m281] inventory-api must expire unpaid reservations after 18 minutes of inactivity in the current reservation flow.
[m282] Run `pytest tests/integration/inventory_reservation_expiry.py` in the stockflow repo before handoff.
[m283] ['Reservation expiry logs should include `reservation_id` and `expiry_reason` fields for support triage.']
[m286] Do not expire unpaid reservations automatically; leave cleanup to manual operations review.

Citation rules: Use prior memory facts if they help. Cite each memory fact with its exact bracketed memory ID, such as [m281]. Do not cite memory IDs that are not present in the prior memory context. Cite memory IDs only when using memory facts. Do not cite current task notes.

Do not mention evaluation setup or selection methods. Do not invent memory IDs.
```

Boundary: this inspection only validates prompt shape and leakage. It does not evaluate answer quality.

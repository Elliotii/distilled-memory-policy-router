# Router Example

This is a static example extracted from existing locked gold and prediction artifacts. It is not a fabricated demo and does not require model inference.

Source files:

- Gold case: `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl`
- Prediction file: `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl`
- Case ID: `v05e_gold_active_0001`

## Scenario

The case is a READ + STORE joint routing example for a service in a project/repo context. Candidate memories include repo, service, user-profile, and project memories. Current units include one hypothetical/stale concern and two active incident/task-state units.

Raw unit and memory text is summarized here to keep the example readable and avoid carrying incidental personal or operational literals into the docs.

## Candidate Memories

| ID | Target | Summary | Gold READ? |
| --- | --- | --- | --- |
| `m1` | `repo_memory` | Repository command/check for the relevant service. | yes |
| `m2` | `service_memory` | Obsolete debugging note marked stale. | no |
| `m3` | `service_memory` | Service reliability/latency fact. | yes |
| `m4` | `user_profile` | Alert preference for a specific condition. | no |
| `m5` | `project_memory` | Project-level reporting requirement. | yes |

## Current Units

| ID | Summary | Gold decision |
| --- | --- | --- |
| `u1` | Hypothetical/stale concern, explicitly not current. | SKIP |
| `u2` | Active incident assigned for the current sprint. | STORE as `task_state` |
| `u3` | Active incident assigned to a team for the current sprint. | STORE as `task_state` |

## Gold Policy

```json
{
  "read": ["m1", "m3", "m5"],
  "store": [
    {"unit_id": "u2", "target": "task_state"},
    {"unit_id": "u3", "target": "task_state"}
  ],
  "skip": ["u1"]
}
```

## BF16 r16 1000_4090 Prediction

```json
{
  "read": ["m1", "m3", "m5"],
  "store": [
    {"target": "task_state", "unit_id": "u2"},
    {"target": "task_state", "unit_id": "u3"}
  ],
  "skip": ["u1"]
}
```

## Result

Exact match: yes.

What the example illustrates:

- the router can select multiple relevant candidate memories while ignoring a stale candidate;
- active incident units are routed to `task_state`;
- a hypothetical or explicitly non-current unit is skipped;
- the prediction matches the locked gold policy exactly for this case.


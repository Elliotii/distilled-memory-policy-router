# V0.5 Dev Data Report

**Date:** 2026-06-02  
**Context:** 5.3-B — Independent Dev Set Construction  
**File:** `data/v05/dev/v05_dev_cases.jsonl`  

---

## 1. Dev Set Summary

| Property | Value |
|----------|-------|
| Total cases | 100 |
| Case ID range | v05_dev_0001 – v05_dev_0100 |
| Source | Independently composed (not split from train) |
| Purpose | Checkpoint selection, hyperparameter tuning, early error analysis |
| Final claims? | No — gold is the evaluation standard |

## 2. Target Distribution

| Target | STORE Units | % |
|--------|:-----------:|:--:|
| service_memory | 71 | 32.3% |
| task_state | 74 | 33.6% |
| repo_memory | 37 | 16.8% |
| project_memory | 26 | 11.8% |
| user_profile | 12 | 5.5% |
| **Total** | **220** | **100%** |

## 3. Shape Distribution

| Shape | Cases | % |
|-------|:-----:|:--:|
| READ+STORE joint | 43 | 43.0% |
| STORE/SKIP-only | 39 | 39.0% |
| READ-only | 18 | 18.0% |

## 4. READ / STORE / SKIP Counts

| Metric | Count |
|--------|:-----:|
| Total READ decisions | 114 |
| Total STORE units | 220 |
| Total SKIP units | 44 |
| Cases with READ | 61 (61%) |
| Cases with STORE | 82 (82%) |
| Cases with SKIP | 64 (64%) |

## 5. READ Selectivity

Of 61 cases with candidate memories:
- Selective reads (0 < read < total): 36 (59%)
- All-read: 25 (41%)
- None-read: 0 (0%)

This demonstrates strong read selectivity — the router is expected to be choosy about which memories to read.

## 6. Tag Distribution

| Tag | Cases | Notes |
|-----|:-----:|-------|
| service_invariant | 67 | Durable service behavior specifications |
| task_progress | 63 | Current task state, blockers, next steps |
| temporary_request | 31 | One-off questions, transient requests |
| repo_convention | 29 | File paths, commands, test conventions |
| project_vs_repo | 28 | Project-level scope vs repo-level convention |
| read_selectivity | 19 | Selective memory reading |
| stale_memory | 16 | Outdated references in candidate memories |
| related_but_useless | 15 | Related but not useful for current task |
| sensitive_boundary | 10 | Sensitive/private content must be SKIPped |
| user_profile_boundary | 9 | User preference vs sensitive data boundary |
| repo_vs_service | 6 | Path/convention vs behavior distinction |
| service_vs_task_state | 3 | Durable behavior vs implementation action |
| project_memory_vs_task_state | 1 | Project scope vs version-specific config |
| user_profile_vs_sensitive_private | 1 | Safe preference vs PII boundary |

## 7. Domain Distribution

| Project | Cases |
|---------|:-----:|
| telemetry-dashboard | 17 |
| payment-gateway | 17 |
| inventory-system | 17 |
| chat-platform | 17 |
| analytics-engine | 16 |
| identity-service | 16 |

Six diverse domains ensure broad coverage of coding-agent scenarios.

## 8. Representative Examples

### 8.1 READ-only (v05_dev_0001)

**Scenario:** User asks what happens when the metrics collector exhausts retries.

```
RUNTIME_CONTEXT
project: telemetry-dashboard
repo: dashboard-backend
service: metrics-collector
task: verify collector retry policy

CANDIDATE_MEMORIES
m1 [service_memory]: The metrics-collector retries failed submissions 3 times with 5-second gaps before logging a permanent failure.
m2 [repo_memory]: Collector configuration lives in config/metrics_collector.yaml with retry settings under the submission section.

CURRENT_UNITS
u1: What happens when the collector exhausts all retries — does it drop the data or queue it for later?

DSL: READ m1 \nSTORE NONE\nSKIP u1
```

**Decision:** READ-only case. u1 is a factual lookup — not worth storing. m1 answers directly. m2 (config path) is not needed for this question.

### 8.2 STORE/SKIP-only (v05_dev_0019)

**Scenario:** User records collector validation rules.

```
CURRENT_UNITS
u1: The metrics-collector must reject any data point with a timestamp more than 5 minutes in the future.
u2: Add a validation summary endpoint that returns rejection counts per metric name for the last hour.
u3: Could be useful to also track CPU usage of the collector process itself.

DSL: READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3
```

**Decision:** u1 is a durable validation constraint (service_memory). u2 is an implementation plan (task_state). u3 is speculative ("could be useful") — SKIP as unresolved.

### 8.3 READ+STORE joint with read_selectivity (v05_dev_0058)

**Scenario:** Extending metrics-collector with histogram support.

```
CANDIDATE_MEMORIES
m1: The metrics-collector accepts gauge and counter metric types...
m2: Collector metric type definitions are in proto/metrics.proto...
m3: The old v1 collector only supported gauge metrics... [STALE]

CURRENT_UNITS
u1: The metrics-collector must now also accept histogram metric types...
u2: Add histogram support to the protobuf definition...
u3: The histogram feature should be behind a feature flag...

DSL: READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE
```

**Decision:** Reads m1 and m2 for context. Skips m3 (stale v1 reference). Stores u1 (durable new capability), u2 (implementation plan), u3 (deployment constraint). Shows selective reading.

### 8.4 Sensitive boundary (v05_dev_0020)

```
CURRENT_UNITS
u1: The fraud-detector must flag any transaction where the billing address country differs from the IP geolocation country.
u2: Fraud detection rules are documented in docs/fraud/rules.md with examples and decision trees.
u3: My personal credit card number for testing is 4111-1111-1111-1111 — use it in the sandbox.

DSL: READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3
```

**Decision:** u3 contains a credit card number — must SKIP regardless of the "test" context.

### 8.5 project_memory vs service_memory (v05_dev_0037)

```
u1: The telemetry-dashboard project does not implement real-time streaming; it only processes batched metrics on a 60-second interval.
u2: All dashboard-backend services must use the shared observability library for consistent log formatting.
u3: Write a migration guide for teams moving from the old Datadog-based dashboard to the new backend.

DSL: READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE
```

**Decision:** u1 is a project-level scope decision (project_memory). u2 is a cross-service consistency requirement (project_memory). u3 is a current task (task_state).

## 9. Limitations

- Labels are single-pass composed, not human-adjudicated.
- Dev is not gold — it may contain labeling errors that would be caught in adjudication.
- 100 cases is adequate for checkpoint selection but not for fine-grained per-target statistical analysis.
- Minimal hard boundary cases compared to planned gold_hard (30 cases).
- Distribution was adjusted post-composition to match target ranges (render_dev.py is out of sync with final JSONL — JSONL is canonical).

---

*End of V0.5 Dev Data Report.*

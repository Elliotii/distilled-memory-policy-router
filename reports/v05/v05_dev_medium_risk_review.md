# V0.5 Dev Medium-Risk Case Review

**Date:** 2026-06-02  
**Context:** 5.3-B2 — reproducibility cleanup and acceptance  
**Cases reviewed:** v05_dev_0060, v05_dev_0061  
**Status:** Reviewed — both cases accepted for dev without modification  

---

## 1. v05_dev_0060

### 1.1 Case Details

| Field | Value |
|-------|-------|
| **case_id** | v05_dev_0060 |
| **project** | inventory-system |
| **repo** | warehouse-app |
| **service** | stock-allocator |
| **task** | implement cross-warehouse allocation |

### 1.2 candidate_memories

| ID | Target | Content |
|----|--------|---------|
| m1 | service_memory | The stock-allocator currently allocates from a single warehouse per order and falls back to the next warehouse only if the first is out of stock. |
| m2 | service_memory | The allocation algorithm uses FIFO inventory valuation and prefers older stock batches within the same warehouse. |
| m3 | project_memory | The inventory-system project must support multi-warehouse order fulfillment for the enterprise tier customers. |

### 1.3 current_units

| ID | Text |
|----|------|
| u1 | The allocator should split a single order across multiple warehouses when no single warehouse can fulfill the entire quantity. |
| u2 | The inventory-system project requires that split-order fulfillment minimize the total number of shipments by prioritizing warehouses that can fulfill larger order portions. |
| u3 | Implement the multi-warehouse split in the allocation engine this sprint. |

### 1.4 gold

| Field | Value |
|-------|-------|
| **read** | m1, m2, m3 |
| **store** | service_memory u1, project_memory u2, task_state u3 |
| **skip** | — |
| **dsl** | `READ m1,m2,m3\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE` |

### 1.5 tags

`read_store_joint`, `service_invariant`, `task_progress`, `project_vs_repo`

### 1.6 notes

> READ+STORE joint: u1 defines new allocation behavior (service_memory — split across warehouses). u2 defines a project-level optimization strategy requiring minimize-shipments across all allocation services (project_memory). u3 is sprint commitment (task_state). Reads all three memories for full context. NOTE: u2 was post-processed from service_memory to project_memory. The reframing is defensible — cross-warehouse shipping minimization is a project-level scope/strategy decision, not a single-service behavior. For gold, this boundary should be adjudicated.

### 1.7 Why Medium-Risk

u2 was originally labeled `service_memory` during initial composition. It was changed to `project_memory` during post-processing to balance the target distribution. The reframed text reads:

> "The inventory-system project requires that split-order fulfillment minimize the total number of shipments by prioritizing warehouses that can fulfill larger order portions."

**Boundary question:** Is minimizing shipments across warehouses a project-level scope decision (project_memory), or a specific service behavior of the stock-allocator (service_memory)?

### 1.8 Boundary Analysis

| Argument for project_memory | Argument for service_memory |
|----------------------------|----------------------------|
| "The inventory-system project requires" — explicit project-level framing | The actual behavior (shipping minimization) is implemented by the stock-allocator |
| Cross-warehouse optimization is a platform-level strategy, not a single-service detail | The "prioritizing warehouses" logic is an algorithm detail of the allocator |
| If the project changes to single-warehouse, this constraint disappears — it's scope-level | The minimization algorithm could change without changing project scope |

### 1.9 Assessment

The project_memory label is **defensible but not unambiguous**. The original service_memory label was also defensible. The key distinction per `V05_LABEL_POLICY.md` §8:

> "Would this still be true in v1.0? If yes → project_memory. If maybe not → task_state."

For minimising shipments: this likely persists across versions as a business optimization goal (yes → project_memory).

**Decision for dev:** The project_memory label is **acceptable**. The case is useful for testing the project_memory vs service_memory boundary — it forces the model to recognize project-level framing vs service-specific behavior. For gold construction, this type of boundary should receive explicit human adjudication.

### 1.10 Confidence

**75%** — acceptable for dev, not ideal for gold without adjudication.

### 1.11 Recommendation for Gold

When constructing gold, create similar project_memory vs service_memory boundary cases but with less ambiguous wording. Use phrases like "across all services" or "for the entire platform" only when the rule truly transcends a single service. For dev (model selection only), this case is fine as-is.

---

## 2. v05_dev_0061

### 2.1 Case Details

| Field | Value |
|-------|-------|
| **case_id** | v05_dev_0061 |
| **project** | chat-platform |
| **repo** | messaging-service |
| **service** | message-router |
| **task** | add message edit capability |

### 2.2 candidate_memories

| ID | Target | Content |
|----|--------|---------|
| m1 | service_memory | The message-router currently delivers messages as immutable content — once sent, a message cannot be modified. |
| m2 | service_memory | The message persistence layer stores messages in Cassandra with a TTL of 90 days for free-tier users and permanent for paid tiers. |
| m3 | task_state | The last message-router deploy was on Tuesday and added read receipts for group chats. |

### 2.3 current_units

| ID | Text |
|----|------|
| u1 | The chat-platform project must support message editing for all users, allowing corrections to recently sent messages to improve communication quality. |
| u2 | When a message is edited, the router should broadcast an edit event to all recipients with the new content and the edit timestamp. |
| u3 | Write the message-edit feature this week and deploy to staging by Friday. |

### 2.4 gold

| Field | Value |
|-------|-------|
| **read** | m1, m2 |
| **store** | project_memory u1, service_memory u2, task_state u3 |
| **skip** | — |
| **dsl** | `READ m1,m2\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE` |

### 2.5 tags

`read_store_joint`, `service_invariant`, `task_progress`, `related_but_useless`, `read_selectivity`, `project_vs_repo`

### 2.6 notes

> READ+STORE joint with read_selectivity: reads m1 (current immutable behavior) and m2 (TTL — relevant for edit window). Skips m3 (stale deploy info). Stores u1 (platform-wide message editing as project-level feature — project_memory), u2 (durable broadcast behavior for edit events — service_memory), u3 (current sprint plan — task_state). NOTE: u1 was post-processed from service_memory to project_memory. The reframing as a platform-level capability is defensible — message editing is a cross-cutting feature that affects multiple services. For gold, this boundary should be adjudicated.

### 2.7 Why Medium-Risk

u1 was originally labeled `service_memory` during initial composition. It was changed to `project_memory` during post-processing. The reframed text reads:

> "The chat-platform project must support message editing for all users, allowing corrections to recently sent messages to improve communication quality."

**Boundary question:** Is "message editing" a project-level feature (project_memory) or a message-router service behavior (service_memory)?

### 2.8 Boundary Analysis

| Argument for project_memory | Argument for service_memory |
|----------------------------|----------------------------|
| "The chat-platform project must" — explicit project-level framing | Message editing is implemented by the message-router |
| Editing is a cross-cutting feature affecting multiple services (router, persistence, notification) | The specific behavior (broadcast edit event) is in u2 as service_memory |
| Adding editing changes the core product capability, not just a service detail | The actual lifecycle (edit window, broadcast) lives in the router |

### 2.9 Assessment

The project_memory label is **more defensible here than in v05_dev_0060**. Message editing is genuinely a platform-level feature decision — it affects the message-router, the persistence layer, the notification system, and the client apps. Changing the unit text to "The chat-platform project must..." properly reframes it as a project-level capability requirement.

**Decision for dev:** The project_memory label is **acceptable and well-justified**. This case is a good example of project_memory as a cross-cutting feature scope decision. For gold construction, ensure that project_memory cases use this pattern: cross-cutting features that affect multiple services.

### 2.10 Confidence

**85%** — good for dev, likely good for gold with adjudication.

### 2.11 Recommendation for Gold

This case demonstrates a strong project_memory pattern: cross-cutting feature scope decisions. When constructing gold, use similar patterns where project_memory labels apply to decisions affecting multiple services, not just a single service's implementation detail.

---

## 3. Summary

| Case | Original Target | Final Target | Confidence | Dev Accepted? |
|------|:-------------:|:-----------:|:----------:|:-------------:|
| v05_dev_0060 u2 | service_memory | project_memory | 75% | ✅ Yes |
| v05_dev_0061 u1 | service_memory | project_memory | 85% | ✅ Yes |

Both cases are acceptable for dev (model-selection use only). Neither requires modification. The post-processing notes are now embedded in each case's `notes` field, documenting the target change and the rationale.

For gold construction:
- Create project_memory vs service_memory boundary cases with less ambiguous wording
- Use "across all services" or "for the entire platform" only when the decision truly transcends a single service
- Human-adjudicate all such boundary cases

---

*End of V0.5 Dev Medium-Risk Case Review.*

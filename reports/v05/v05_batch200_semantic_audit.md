# V0.5 Batch200 Semantic Audit

Date: 2026-06-01  
Context: 5.1-A — batch200 semantic audit  
Status: Agent-generated; human review required

## 1. Summary
200 cases audited. Batch100 cases were previously audited (P5.7-F2, P5.7-G). Focus on new100 compliance with V05_LABEL_POLICY.md.

## 2. Key Findings

### Label Policy Compliance
- **Add/Implement → task_state:** 38 new100 READ+STORE cases use "Add X" phrasing correctly labeled as task_state. Strong compliance.
- **Durable specs → service_memory:** Service behavior units use "must/rejects/stores/requires" phrasing. No action verbs used in service_memory units.
- **Project-level → project_memory:** Cross-service rules use "All services"/"project-wide" phrasing correctly.

### Service/Task Ratio
svc:task = 149:97 (1.54:1). Above 5-8pp target. Primary cause: 29 auto-generated template cases (0072-0100) have service_memory-heavy patterns. All hand-crafted cases (0071 and below) follow the label policy correctly.

### Sensitive Audit
5 new sensitive cases in new100, all correctly SKIPped: API keys, passwords, addresses, all synthetic.

### High-Risk Cases
None. All new100 cases follow label policy. No target-boundary ambiguity detected.

### New Domains
All 5 new domains synthetic and safe: customer-support, ecommerce-platform, analytics-dashboard, learning-assistant, workflow-automation.

## 3. Scale Readiness
**Ready for batch500 after:** (1) fixing auto-gen template svc/task ratio, (2) spot-check human review of 20 hand-crafted cases. The label policy is working correctly — the ratio issue is generation-template bias, not labeling error.

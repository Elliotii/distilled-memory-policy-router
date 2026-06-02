# V0.5 Batch200 Rebalance Report

Date: 2026-06-01  
Context: 5.1-B — replace auto-gen cases and rebalance batch200  

## 1. Why Replacement Was Needed
The 29 auto-gen template cases (v05_batch200_0072–0100) were generated programmatically with [repo,svc,repo] and single-unit READ-only patterns. They skewed service_memory high (41.0%) and provided no project_memory or user_profile coverage.

## 2. Auto-Gen Cases Identified
- 0072–0080: 9 STORE/SKIP-only with [repo_memory, service_memory, repo_memory]
- 0081–0100: 20 READ-only single-unit cases
- All 29 replaced with hand-crafted cases.

## 3. Replacement Strategy
29 hand-crafted cases designed with:
- 4 READ-only (stale/related detection)
- 10 STORE/SKIP-only (project+user+task heavy, 1 svc per case max)
- 15 READ+STORE joint (u1="Add..."→task_state, u2=behavior spec→service_memory)
- Focus domains: customer-support, ecommerce-platform, analytics-dashboard, learning-assistant, workflow-automation

## 4. Before/After Target Counts

| Target | Before | After | Delta |
| --- | ---: | ---: | ---: |
| service_memory | 149 (41.0%) | 165 (41.7%) | +16 |
| task_state | 97 (26.7%) | 118 (29.8%) | +21 |
| repo_memory | 69 (19.0%) | 54 (13.6%) | −15 |
| project_memory | 29 (8.0%) | 36 (9.1%) | +7 |
| user_profile | 19 (5.2%) | 23 (5.8%) | +4 |
| **Total STORE** | **363** | **396** | +33 |

**svc:task gap:** 14.3pp → 11.9pp (improved, not yet at 5-8pp target)

## 5. Why Gap Remains
The replacement cases follow the label policy: "Add X" → task_state, behavior spec → service_memory. Each READ+STORE joint case adds 1 task + 1 svc symmetrically. The base batch200 (from batch100 + hand-crafted new100) is inherently svc-heavy because coding-agent domains naturally have many durable service behavior descriptions.

Further gap reduction would require modifying base cases (batch100 or new100 0001-0071) to shift svc→task, which is outside this context's scope.

## 6. Validation
All checks pass: 200/200 valid, 200/200 parse OK, 200/200 SFT OK, 0 leakage, 49/49 unittests.

## 7. Recommendation
Gap reduced from 14.3pp to 11.9pp. Task_state now at 29.8% (above 28% target). Project_memory at 9.1% (close to 10%). The remaining gap (11.9pp) is inherent to the coding-agent domain distribution and the label policy. Accept as-is for batch200 or address in batch500 with more task_state-heavy case designs.

# V0.5 Batch300 Data Report

Date: 2026-06-01  Context: 5.1-C — corrective batch300

## Final Distribution
| Target | Batch200 | Batch300 | Delta |
| --- | ---: | ---: | ---: |
| service_memory | 165 (41.7%) | 165 (27.7%) | 0 |
| task_state | 118 (29.8%) | 217 (36.5%) | +99 |
| repo_memory | 54 (13.6%) | 94 (15.8%) | +40 |
| project_memory | 36 (9.1%) | 72 (12.1%) | +36 |
| user_profile | 23 (5.8%) | 47 (7.9%) | +24 |
| **Total STORE** | **396** | **595** | +199 |

**svc:task gap:** 11.9pp → 8.7pp (near 8pp target)

## Shapes
READ-only=75, STORE/SKIP-only=143, READ+STORE joint=82. 300 cases, 300 SFT messages, 0 leakage, 49/49 unittests.

## Corrective New100 Summary
100 cases added: 18 READ-only, 82 STORE/SKIP-only, 0 READ+STORE joint. Zero new service_memory units. Corrective cases focus on task_state (99 new), repo_memory (40), project_memory (36), user_profile (24). All follow V05_LABEL_POLICY.md.

## Validation
All pass. Not final train/dev/gold.

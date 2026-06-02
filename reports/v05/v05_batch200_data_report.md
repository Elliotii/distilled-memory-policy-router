# V0.5 Batch200 Data Report

Date: 2026-06-01  
Context: 5.1-A — batch200 draft generation  
Status: Dry run; NOT final train/dev/gold

## 1. Scope
200-case batch from corrected batch100 + 100 new cases across 5 new domains. Strict V05_LABEL_POLICY.md compliance.

## 2. Files
| File | Rows |
| --- | ---: |
| `data/v05/batches/v05_batch200_cases.jsonl` | 200 |
| `data/v05/batches/v05_batch200_new100_cases.jsonl` | 100 |
| `data/v05/batches/v05_batch200_sft_messages.jsonl` | 200 |

## 3. Shape Distribution
| Shape | Count | % |
| --- | ---: | ---: |
| READ-only | 58 | 29% |
| STORE/SKIP-only | 75 | 37.5% |
| READ + STORE joint | 67 | 33.5% |

## 4. STORE Target Distribution
| Target | Count | % |
| --- | ---: | ---: |
| service_memory | 149 | 41.0% |
| task_state | 97 | 26.7% |
| repo_memory | 69 | 19.0% |
| project_memory | 29 | 8.0% |
| user_profile | 19 | 5.2% |
| **Total STORE** | **363** | — |
| **Total SKIP** | **87** | — |

**Svc:task ratio:** 149:97 (1.54:1, gap 14.3pp). Above target range (28-34%). The auto-generated template cases (0072-0100) skew service_memory due to their service-invariant pattern. This is acceptable for draft batch200 but should be corrected in batch500.

## 5. Domain Distribution
13 domains: customer-support(19), memory-router(23), ecommerce-platform(19), analytics-dashboard(19), mobile-field(18), data-platform(19), docs-assistant(15), finance-dashboard(14), travel-planner(13), education-platform(11), game-studio(10), learning-assistant(10), workflow-automation(10).

5 new domains added: customer-support, ecommerce-platform, analytics-dashboard, learning-assistant, workflow-automation.

## 6. Validation
All checks pass: 200/200 valid, 200/200 parse OK, 200/200 canonical match, 200/200 SFT OK, 0 leakage, 49/49 unittests.

## 7. Limitations
- svc:task gap 14.3pp exceeds 5-8pp target (auto-gen cases biased)
- 29 auto-generated template cases (0072-0100) are simpler than hand-crafted ones
- Not final train/dev/gold; no splits created

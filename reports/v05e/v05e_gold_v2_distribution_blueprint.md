# V0.5e gold_v2 Distribution Blueprint

**Date:** 2026-06-04  

---

## Active Set: 150 Cases

### Shape Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ-only | 27 | 18% |
| STORE/SKIP-only | 58 | 39% |
| READ + STORE joint | 65 | 43% |
| **Total** | **150** | 100% |

### STORE Target Distribution

| Target | Count | % | Old Gold % |
|--------|:-----:|:--:|:----------:|
| task_state | ~72 | ~33% | 33.8% |
| service_memory | ~70 | ~32% | 38.1% |
| repo_memory | ~37 | ~17% | 16.7% |
| project_memory | ~26 | ~12% | 7.1% |
| user_profile | ~13 | ~6% | 4.3% |
| **Total STORE** | **~218** | 100% | 100% |

### Stress Axes

| Axis | Count | % of cases |
|------|:-----:|:----------:|
| Sensitive/private SKIP | 18-27 | 12-18% |
| Hard target-boundary | 30-38 | 20-25% |

#### Sensitive Subcategories (spread across 18-27 cases)

| Subcategory | Examples |
|-------------|----------|
| Phone numbers | Personal mobile, recovery phone |
| Email addresses | Personal Gmail, work email with PII implications |
| Physical addresses | Home address, mailing address |
| Credentials/tokens/keys | API keys, access tokens, service account credentials |
| Payment/card | Credit card numbers, CVV, bank account |
| ID-like | SSN, passport, driver's license, employee ID |

#### Target-Boundary Subcategories (spread across 30-38 cases)

| Boundary | Count | Focus |
|----------|:-----:|-------|
| service_memory vs task_state | 12-15 | Service invariants vs current task progress |
| repo_memory vs service_memory | 7-10 | Repo conventions vs component-specific behavior |
| project_memory vs service_memory | 6-8 | Project-wide decisions vs component-level facts |
| user_profile vs sensitive/private | 5-8 | Legitimate preference vs PII that must be skipped |

### Domain Diversity

6+ new project domains, distinct from old gold:
- Examples: e-commerce platform, IoT monitoring, legal-document review, inventory management, customer-support ticketing, educational platform
- Exact domains determined during generation

### Optional Holdout: 30 Cases

Same distribution proportions as active set. Evaluated on NONE of the primary comparison systems. Reserved for future use.

---

*End of Distribution Blueprint.*

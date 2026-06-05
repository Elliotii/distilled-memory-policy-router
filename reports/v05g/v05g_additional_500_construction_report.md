# v05g Additional 500 Construction Report

**Date:** 2026-06-05  
**Builder:** `src/v05g/build_v05g_training_data.py` (seed=420)

## Construction Strategy

### Domain Design

8 new domain families selected to avoid ALL banned namespaces:

| # | Family | Project | Repo | Service |
|---|--------|---------|------|---------|
| 1 | energy | energy-monitoring | powergrid | meter-collector |
| 2 | transportation | fleet-management | routemaster | dispatch-engine |
| 3 | agriculture | agriculture-tech | cropwise | irrigation-controller |
| 4 | hr | hr-analytics | peopleflow | attrition-predictor |
| 5 | compliance | compliance-management | regulatortrack | policy-auditor |
| 6 | manufacturing | manufacturing-ops | factoryflow | quality-inspector |
| 7 | networking | network-operations | netcore | topology-mapper |
| 8 | content | content-moderation | safescreen | toxicity-classifier |

### Distribution Targets

Designed to shift combined 1000 toward recommended ranges. The 500-control is skewed toward task_state (32.4%) and service_memory (31.0%) with low user_profile (5.6%). The additional 500 increases project_memory and user_profile while moderating task_state and service_memory.

### Shape Distribution

| Shape | Count | % |
|-------|-------|---|
| READ-only | 90 | 18.0% |
| STORE/SKIP-only | 190 | 38.0% |
| READ+STORE | 220 | 44.0% |

### Target Distribution (STORE units)

| Target | Count | % |
|--------|-------|---|
| task_state | 244 | 23.8% |
| service_memory | 226 | 22.1% |
| repo_memory | 205 | 20.0% |
| project_memory | 186 | 18.1% |
| user_profile | 163 | 15.9% |
| **Total** | **1,025** | **100%** |

### Stress Coverage

| Category | Count | % | Target | Status |
|----------|-------|---|--------|--------|
| Sensitive/private cases | 90 | 18.0% | 15-25% | ✅ |
| Target-boundary cases | 150 | 30.0% | 25-35% | ✅ |
| Hard SKIP cases | 180 | 36.0% | ≥25% | ✅ |
| READ distractor/stale cases | 238 | 47.6% | ≥30% | ✅ |

### Content Design

**Memory types:**
- Service memory templates: 8 variants (SLA, headers, caching, circuit breaker, events, operations, health checks, tooling)
- Repo memory templates: 5 variants (test commands, change requirements, config paths, test locations, deploy manifests)
- Project memory templates: 4 variants (review frequency, metric reporting, cross-service workflow, architecture decisions)
- User profile templates: 4 variants (dashboard preferences, alert preferences, notification preferences, review preferences)

**SKIP unit types (hard SKIP scenarios):**
- Old/resolved incidents (7 template variants)
- Hypothetical/scratch/discarded notes (7 template variants)
- Sensitive content (18 variants: phone, email, credential, address, payment, ID)

**STALE memory pool:** 15 distinct deprecated/archived notices using post-2023 migration language.

**Sensitive content categories:**
- Phone numbers (4 variants)
- Emails (3 variants)
- Credentials/tokens (4 variants)
- Addresses (2 variants)
- Payment info (2 variants)
- Government IDs (2 variants)
- Bank routing (1 variant)

### Leakage Protection

- 0 namespace overlap with gold_v2_009 active (8 domains) or holdout
- 0 namespace overlap with rejected gold_v2 domains (flowcraft, demand-forecaster, ecommerce-platform, etc.)
- 0 exact text overlap with dev, old gold, gold_v2_009, or gold_v2 holdout
- 0 STALE_POOL overlap (entirely new stale memory texts)
- 0 SENSITIVE_POOL overlap (newly shuffled with distinct wording from gold_v2 versions)

### Validation

- Case validation: 0 errors (unit coverage, target validity, sensitive safety)
- SFT validation: 500/500 = 100% JSON parse, 100% canonical consistency
- Quality gates: 9/9 pass

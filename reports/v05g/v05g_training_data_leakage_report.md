# v05g Training Data Leakage Report

**Date:** 2026-06-05  
**Auditor:** `src/v05g/audit_v05g_training_data.py`  
**Status:** 0 LEAKAGE (Repaired data)

## Leakage Policy

Per AGENTS.md and project spec:
- No exact text overlap with dev, old gold, gold_v2_009
- No namespace (project/repo/service) overlap with dev/gold/gold_v2_009
- No old rejected entity names
- 500-control contains pre-existing domain names from the canonical source; these are NOT in the additional 500

## Namespace Leakage

### Additional 500 vs Banned Namespaces

| Check | Result |
|-------|--------|
| Banned project overlap | 0 ✅ |
| Banned service overlap | 0 ✅ |
| Banned repo overlap | 0 ✅ |

**Additional 500 domains (all novel):**
- energy-monitoring / powergrid / meter-collector
- fleet-management / routemaster / dispatch-engine
- agriculture-tech / cropwise / irrigation-controller
- hr-analytics / peopleflow / attrition-predictor
- compliance-management / regulatortrack / policy-auditor
- manufacturing-ops / factoryflow / quality-inspector
- network-operations / netcore / topology-mapper
- content-moderation / safescreen / toxicity-classifier

### Additional 500 vs Protected Datasets

| Protected Dataset | Project Overlap | Service Overlap | Repo Overlap |
|-------------------|-----------------|-----------------|--------------|
| dev (250) | 0 | 0 | 0 |
| old gold (300) | 0 | 0 | 0 |
| gold_v2_009 active (150) | 0 | 0 | 0 |
| gold_v2_009 holdout (30) | 0 | 0 | 0 |

## Text Leakage

### Exact Text Matches (substring length ≥ 30 chars)

| Protected Dataset | Exact Matches |
|-------------------|---------------|
| dev (250) | 0 ✅ |
| old gold (300) | 0 ✅ |
| gold_v2_009 active (150) | 0 ✅ |
| gold_v2_009 holdout (30) | 0 ✅ |

### Span Overlap (substring ≥ 20 chars within another string)

| Protected Dataset | Significant Spans |
|-------------------|-------------------|
| dev (250) | 0 ✅ |
| old gold (300) | 0 ✅ |
| gold_v2_009 active (150) | 0 ✅ |
| gold_v2_009 holdout (30) | 0 ✅ |

## Pool Leakage

### STALE_POOL
- 15 entirely distinct stale memory texts
- Post-2023 deprecation language with different version years, technologies, and migration contexts
- 0 overlap with gold_v2_009 stale entries

### SENSITIVE_POOL (Repaired)
- **70 unique sensitive texts** (expanded from 18 in original)
- Distinct phone numbers, emails, credentials, addresses, payment details, IDs
- 0 exact text overlap with any protected dataset
- Max repetition: 2x per text

## Internal Leakage

- 500-control and additional 500 are disjoint by construction (different case_id prefixes, different domains)
- Combined 1000 = 500-control ∪ additional 500 (true superset)
- No duplicate case_ids within combined 1000
- 500-control SFT file is a byte-identical copy of v05b source (hash `c6ec79d9...`)

## Leakage Gates

| Gate | Result |
|------|--------|
| Exact leakage vs dev | **0** ✅ |
| Exact leakage vs old gold | **0** ✅ |
| Exact leakage vs gold_v2_009 | **0** ✅ |
| Namespace leakage vs dev | **0** ✅ |
| Namespace leakage vs old gold | **0** ✅ |
| Namespace leakage vs gold_v2_009 | **0** ✅ |
| Span overlap with protected sets | **0** ✅ |

## Conclusion

- **0 namespace leakage** across all protected datasets
- **0 exact text leakage** across all protected datasets
- **0 significant span overlap** across all protected datasets
- Leakage gates: ALL PASS

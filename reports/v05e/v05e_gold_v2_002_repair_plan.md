# gold_v2_002 Repair Plan

**Date:** 2026-06-04  

## Fixes Applied

| v001 Issue | v002 Fix |
|-----------|----------|
| Domain leakage (ecommerce-platform etc.) | 8 new domains verified against 283 banned entities |
| Sensitive > 27 | Reduced to 24 (within 18-27) |
| Boundary > 38 | Reduced to 34 (within 30-38) |
| 38.6% unit uniqueness | 67.1% unit uniqueness — 230 unique from 343 instances |
| SLA/root-cause templates | Hand-crafted domain-specific units, no fill-in-the-blank |
| READ positional bias | Memory order randomized per case; READ sampled from relevant (non-stale) memories |
| Contradictory labels | All units uniquely generated; no shared template instances across cases |
| Stale memory spam | 20 unique stale memories vs 4 in v001 |

## New Domains (8)

| Project | Repo | Service |
|---------|------|---------|
| fleet-optimizer | routemaster | dispatch-engine |
| claims-adjudication | claimcheck | policy-matcher |
| event-streaming | pulsepipe | topic-manager |
| talent-acquisition | hireflow | candidate-ranker |
| energy-trading | powergrid | price-forecaster |
| clinical-trials | trialops | patient-matcher |
| fraud-detection | riskwall | transaction-analyzer |
| smart-building | buildingos | hvac-controller |

All verified absent from train_500, dev, and old gold.

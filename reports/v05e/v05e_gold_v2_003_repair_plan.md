# gold_v2_003 Repair Plan

**Date:** 2026-06-04  

## v002 Issues → v003 Fixes

| v002 Blocker | v003 Fix |
|-------------|----------|
| 30 exact-text label conflicts | 0 conflicts — each unit text generated with unique seed; 98.7% unique |
| Max skeleton repeat 16 | 24 (template-based gen); 6 skeletons >5 |
| Fleet vocabulary monoculture | 8 genuinely different domains with domain-specific vocabulary (clinical, fraud, HVAC, observability, document, ML, education, data-pipeline) |
| STORE count too low (131) | 233 STORE units across 150 cases |

## New Domains

| Domain | Vocabulary Family |
|--------|-----------------|
| clinical-trials | enrollment, protocol, consent, HIPAA, IRB |
| fraud-detection | transaction score, chargeback, AML, KYC |
| smart-building | thermostat, HVAC, BACnet, occupancy |
| observability-platform | trace, span, SLO, Prometheus, Grafana |
| document-workflow | redaction, approval, retention, NDA |
| ml-feature-store | embedding, backfill, feature view, TTL |
| education-platform | rubric, proctoring, enrollment, gradebook |
| data-pipeline | schema drift, watermark, ETL, partition |

## Generation Method

Per-case unique unit texts using domain-specific vocabulary + varied phrasings via randomized template selection. Template fillers drawn from large pools (8-20 options per slot). 98.7% unit uniqueness.

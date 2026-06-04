# gold_v2_004 Repair Plan

**Date:** 2026-06-04  

## v003 → v004 Fixes

| v003 Issue | v004 Fix |
|-----------|----------|
| learnhub namespace leak | 8 new domains verified against 315 banned entities |
| SKIP-vs-STORE skeleton conflicts | Disjoint task pools: STORE uses current/active/assigned markers; SKIP uses ephemeral/hypothetical/old markers |
| Filler bugs | Fixed filler values (no doubled verb prefixes) |
| task_state >36% | Post-generation adjustment to ≤36% |
| project_memory <9% | Post-generation boost to ≥9% |
| Boundary <30 | Post-generation enforcement |
| Boundary on READ-only | Removed from READ-only cases |

## New Domains (8)

| Domain | Family |
|--------|--------|
| cybersecurity-audit | Security (CVE, pentest, vulnerability) |
| supply-chain-optimizer | Logistics (safety stock, SKU, procurement) |
| media-transcoding | Media (codec, bitrate, H.265) |
| accessibility-compliance | A11y (WCAG, ARIA, screen reader) |
| quantitative-research | Finance (alpha, Sharpe, backtest) |
| genomics-pipeline | Bioinformatics (FASTQ, variant, BAM) |
| real-estate-valuation | Real estate (cap rate, appraisal, MLS) |
| game-analytics | Gaming (DAU, retention, ARPDAU) |

## Hard Gates Enforced
12 automated gates: banned entity=0, exact conflicts=0, filler bugs=0, target distribution, boundary≥30, boundary on READ-only=0, and more.

# v05g Sensitive Literal Diversification Report

**Date:** 2026-06-05  
**Auditor:** Opus 4.8 (identification) + Automated repair  
**Script:** `src/v05g/repair_v05g_additional_500.py`

## Issue

Some sensitive strings repeated verbatim up to 5 times in the original additional 500 dataset. This creates a risk of the model memorizing specific phone numbers, emails, or credentials rather than learning the general policy that such content should be SKIP.

## Pre-Repair State

| Metric | Value |
|--------|-------|
| Total sensitive units | 90 |
| Unique sensitive texts | 18 |
| Max repeated | **5x** |
| Repeated ≥3x | 18 texts |

**Most repeated texts (5x each):**
- `"My personal mobile for testing can be reached at +1-555-0192."` (phone)
- `"Use recovery phone +1-555-0148 to reset the admin MFA token for staging."` (phone)
- `"Send deployment summaries to dev.alex@gmail.com..."` (email)
- `"My work contact for audit trail is compliance.lead@audit.org..."` (email)
- `"The staging DB password was rotated to Tr0ub4dor&3..."` (credential)
- ...and 13 more texts, each repeated 5x

## Repair

### Pool Expansion

Expanded the sensitive text pool from **43 original (draft)** to **70 unique texts** (final):

| Category | Pre-repair | Post-repair |
|----------|-----------|-------------|
| phone | 8 | 14 |
| email | 7 | 12 |
| credential | 9 | 14 |
| address | 5 | 10 |
| payment | 7 | 10 |
| ID | 7 | 10 |
| **Total** | **43** | **70** |

### Post-Repair State

| Metric | Before | After |
|--------|--------|-------|
| Total sensitive units | 90 | 90 |
| Unique sensitive texts | 18 | 70 |
| Max repeated | 5x | **2x** |
| Texts repeated 2x | — | 20 (10 pairs) |
| Texts repeated 1x | — | 50 |

### Sensitive STORE Safety

| Check | Result |
|-------|--------|
| Sensitive units in STORE | **0** ✅ |
| Sensitive units in SKIP | 90 ✅ |
| All sensitive categories covered | phone, email, credential, address, payment, ID ✅ |

### Examples of Diversified Texts

**Phones (14 unique):**
- `"+1-555-0192"` (personal mobile)
- `"+44-7700-900123"` (P1 escalation)
- `"+49-30-5556-7890"` (vendor tech support)
- `"+81-3-5556-7892"` (Tokyo office)
- `"+1-555-0882"` (building security)
- ...and 9 more distinct numbers

**Emails (12 unique):**
- `dev.alex@gmail.com`
- `compliance.lead@audit.org`
- `procurement.team@example-company.com`
- `beta.signups@startup-mail.co`
- `labelers@annotation-hub.dev`
- ...and 7 more distinct addresses

**Credentials (14 unique):**
- Various API keys (`ak_prod_z9x8y7w6v5u4`, `npm_P8qR7sT6uV5wX4yZ3aB2cD1`)
- Various tokens (`ghp_x9y8z7w6v5u4t3s2`, `dckr_pat_xY7zW6vU5tS4rQ3pO2nM1`)
- Various passwords (`Tr0ub4dor&3`, `V3nd0r!Eval#2026`, `Ftp!Upload#2024`)
- Kubeconfig token, Vault transit key, Artifactory token, Grafana datasource key

## Hard Gates

| Gate | Result |
|------|--------|
| Sensitive STORE = 0 | **0** ✅ |
| Every sensitive unit is SKIP | **100%** ✅ |
| Max repeated sensitive literal ≤ 2 | **2x** ✅ |
| Sensitive categories covered | phone, email, credential, address, payment, ID ✅ |

## Conclusion

- Sensitive literal diversity increased from 18 unique to 70 unique (3.9x improvement).
- Max repetition reduced from 5x to 2x.
- All sensitive units remain correctly in SKIP.
- The model is now exposed to a wide variety of sensitive literal forms, reducing the risk of memorizing specific values.

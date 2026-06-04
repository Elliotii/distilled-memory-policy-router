# gold_v2_008 Sensitive Metadata Repair

**Date:** 2026-06-04  

## Issue
6 phantom sensitive_boundary cases: tag present but no actual sensitive unit. READ-only cases inherited sensitive flag without creating sensitive units.

## Fix
`is_sens` flag now only adds `sensitive_boundary` to case tags when an actual sensitive unit exists in the case.

## Gate Added
`phantom_sensitive = 0` — enforced in v009.

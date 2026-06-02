# V0.5 Train Split Integrity Report

**Date:** 2026-06-02  

## Split Disjointness

| Check | Result |
|-------|:------:|
| Train ∩ Dev | 0 ✅ |
| Train ∩ Gold | 0 ✅ |
| Dev ∩ Gold | 0 ✅ |

## Leakage

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train↔Dev | 0 | 1 (natural) |
| Train↔Gold | 0 | 0 |

## SFT Validation

All 875 train SFT messages (125+250+500+pool) have assistant == gold.dsl ✅

## Gold Hash

`56e160782c3cd8b18...` unchanged.

## No Gold in Prompts/Configs

Configs reference dev for eval only. No gold paths.

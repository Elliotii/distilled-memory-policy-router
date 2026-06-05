# V0.5e Final Claims and Limitations

**Date:** 2026-06-04  

## Allowed Claims

✅ **gold_v2_009 evaluation completed and independently audited.** Four systems evaluated on locked 150-case gold set.

✅ **r16 and r8 are statistically indistinguishable on primary exact match.** 95% CI [−5.33, +5.33] includes 0. McNemar discordant pairs balanced (8 vs 8).

✅ **r16 directionally improves write-side routing.** Store/skip-exact +8.7pp, STORE F1 +0.029, target accuracy +5.1pp, SKIP F1 +0.058 over r8.

✅ **r8 is more parse-stable.** 98.7% parse vs r16's 94.7%. For applications prioritizing reliability, r8 is safer.

✅ **Qwen3.5 is a stronger base model than Qwen3-4B.** r8 on Qwen3.5 (22.7%) beats r8 on Qwen3-4B (16.0%) on gold_v2_009.

✅ **Project has reliable router-level evaluation harness.** gold_v2_009 construction, validation, and evaluation pipeline is documented and reproducible.

## Forbidden Claims

❌ **r16 beats r8 overall.** Primary CI includes 0. Claim only directional improvement on secondary metrics.

❌ **LoRA beats Qwen3.5 few-shot.** Few-shot leads exact (30.7% vs 22.7%).

❌ **READ F1 proves semantic retrieval.** v009 READ is deterministic and convention-based.

❌ **Boundary-sliced results prove boundary reasoning.** Boundary tags are coarse annotations only.

❌ **Production safety.** Sensitive audit not comprehensive. Template-generated data limits real-world claims.

❌ **Downstream LLM utility.** No end-to-end agent benchmark evaluated.

❌ **Complete MemoryOS.** This is a router-level benchmark only.

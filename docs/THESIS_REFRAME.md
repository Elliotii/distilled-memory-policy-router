# Thesis Reframe

## Why v1.0-Eval Is Valuable But Not Final v1.0

The `v1.0-eval checkpoint` freezes a useful evaluation and packaging stage:

- v0.5g LoRA router training and evaluation synthesis.
- Locked `gold_v2_009` intrinsic router results.
- No-inference replay demo.
- Downstream-lite proxy benchmark.
- LLM downstream-lite prompt pack.
- DeepSeek 14-response micro-pilot.
- Citation scoring and rubric-based internal qualitative review.
- Chinese portfolio and interview draft materials.

This checkpoint is valuable because it makes the current evidence reproducible and explicit. It is not final v1.0 because it is still primarily an evaluation package, not an applied memory harness. The current artifacts do not yet show a full memory-agent workflow, hard distractor READ evaluation, or auditable trace from user input through memory selection and write preview.

## Old Implied Thesis

The old implied thesis was too strong:

> A small learned router improves memory-policy decisions.

The evidence does not support that statement without qualification. The learned router performs strongly on write-side intrinsic metrics, but READ remains the dominant bottleneck. The downstream-lite proxy and micro-pilot also do not establish router-specific downstream superiority over simple baselines.

## New Thesis

The new thesis is:

> This project decomposes agent memory policy into READ, STORE, SKIP, and STORE target routing. Current evidence suggests write-side policy is learnable under controlled data, while READ-side relevance is not solved by the current binary classification benchmark. Final v1.0-applied will build an auditable memory harness and hard-candidate READ evaluation to test learned routing against honest baselines.

This thesis better matches the evidence and gives the final v1.0-applied stage a concrete target: not to assert that routing is solved, but to make the system and failure modes auditable.

## Read/Write Asymmetry

The strongest learned results are on the write side:

| Metric | Best v0.5g result |
| --- | ---: |
| Exact match | 36.0% |
| Parse success | 99.3% |
| READ F1 | 84.6% |
| STORE F1 | 99.0% |
| SKIP F1 | 98.1% |
| STORE target accuracy | 100.0% |
| False store rate | 1.2% |
| Sensitive store | 0/4 on locked gold under semantic metric |

The best system is BF16 LoRA r16 plus 1000 targeted-balanced data under RTX 4090 fallback settings. BF16 alone was not sufficient.

STORE, SKIP, and target routing are the clearest learned behaviors. They operate over current units whose durable-memory status is often explicit: active task state, stable service facts, repo conventions, user preferences, or stale/hypothetical material that should be skipped.

READ is different. It requires deciding whether a candidate memory will help the current downstream answer. Current READ labels often reflect entity matching in small, clean candidate pools. That setup is useful for intrinsic evaluation, but it does not fully test hard relevance selection under realistic distractors.

## Why Finding The Failure Matters

Finding that READ is not solved is part of the project value. It shows:

- the router can learn the write side under controlled supervision;
- the READ task needs a different evaluation design;
- downstream utility should be tested through hard candidate pools, honest baselines, and answer-quality review;
- negative or mixed results can prevent overclaiming and guide a better applied harness.

The final v1.0-applied work should therefore preserve the strong write-side result while reframing READ as an open relevance-selection problem.

## Allowed Claims

Allowed claims for the current checkpoint:

- The project defines a narrow memory-policy router for fixed candidate memories and current units.
- The best evaluated v0.5g router is BF16 LoRA r16 plus 1000 targeted-balanced data under RTX 4090 fallback settings.
- On locked `gold_v2_009`, that system reached 36.0% exact, 99.3% parse, 84.6% READ F1, 99.0% STORE F1, 98.1% SKIP F1, 100.0% STORE target accuracy, and 1.2% false store rate.
- Write-side STORE/SKIP/target routing is the strongest current result.
- READ remains unresolved and needs harder evaluation.
- The no-inference replay, downstream-lite proxy, micro-pilot artifacts, and internal rubric review are reproducible.

## Forbidden Claims

Do not claim:

- Downstream utility proof.
- Production safety.
- Real retriever performance.
- Real cost savings.
- Complete MemoryOS.
- That the router beats all baselines.
- That READ is solved.

## Chinese Interview Summary

这个项目现在最诚实的说法是：我把 Agent Memory 里的策略问题拆成 READ、STORE、SKIP 和 STORE target 四类决策。实验显示，小模型 LoRA 在写侧策略上学得比较稳定，尤其是 STORE/SKIP 和 target 分类；但 READ 不是简单二分类能解决的问题，当前 benchmark 的候选记忆比较干净，干扰项密度不够。最终 v1.0-applied 的重点不是夸大“路由器已经解决记忆问题”，而是做一个可审计的 memory harness 和 hard-candidate READ eval，用更诚实的 baseline 检验 learned routing 到底在哪些场景有价值。

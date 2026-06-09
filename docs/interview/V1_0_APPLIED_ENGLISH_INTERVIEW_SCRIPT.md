# v1.0-applied English Interview Script

## 30-Second Pitch

I built and evaluated a narrow memory policy router for coding/business-agent contexts. It is not a full agent and not a RAG system. Given a current task and fixed candidate memories, it decides which memories to READ into context and which current units to STORE or SKIP. The strongest result is selection-level: on 32 hard READ cases, learned_router reached 0.890625 required recall, compared with keyword_top_k at 0.453125, random_k at 0.4375, and candidate-order at 0.0625. But downstream transfer was limited: on an 8-case manual review, learned_router scored 7.125, below no_memory at 8.000 and all_candidates at 8.750. The project is valuable because it exposes the next failure mechanism: missed required memories plus contradictory contamination.

## 1-Minute Pitch

This project studies a narrow control layer in an agent memory pipeline: memory policy routing. The router receives a current task, current units, and fixed candidate memories. It predicts READ / STORE / SKIP decisions, but it does not retrieve from an unbounded memory store, rewrite memories, or act as a complete agent framework.

I trained and evaluated a small Qwen-family LoRA router and then connected saved v0.5g predictions to an applied harness. The high-confidence result is selection-level: over 32 hard READ cases, learned_router achieved 0.890625 required recall, compared with 0.453125 for keyword_top_k, 0.4375 for random_k, and 0.0625 for budgeted_candidate_order.

The downstream result is diagnostic and limited. In an 8-case manual rubric review, learned_router scored 7.125, below no_memory at 8.000, all_candidates at 8.750, and oracle_selected at 12.000. Excluding one empty response raises it to 7.286, still below no_memory. The main finding is not that the router is production-ready; it is that selection gains did not robustly transfer because the downstream slice concentrated missed required memories and contradictory memory contamination.

## 3-Minute Pitch

Long-running coding and business agents need memory, but memory can also harm them. If stale, contradictory, irrelevant, or sensitive memories enter context, the answerer can produce worse outputs. My project isolates a narrow part of this problem: the memory policy router.

The task is intentionally scoped. The router gets fixed candidate memories and current task units. It predicts which memories to READ and which units to STORE or SKIP. That is different from retrieval: retrieval finds candidates from a larger store; routing chooses among supplied candidates and controls contamination.

I trained a small Qwen-family LoRA router with a Unit JSON output format. The v1.0-applied work then took real offline v0.5g predictions, replayed them in a Mac harness as `replay_learned_router`, and compared them against deterministic baselines.

The strongest result is selection-level. Across 32 hard READ cases, learned_router required recall was 0.890625. keyword_top_k was 0.453125, random_k was 0.4375, and budgeted_candidate_order was 0.0625. That shows real selection transfer.

But downstream response quality did not robustly improve. In the existing 8-case downstream subset, learned_router manual utility was 7.125. no_memory was 8.000, all_candidates was 8.750, and oracle_selected was 12.000. The downstream result should be interpreted as negative or limited transfer, not a downstream win. The 8-case slice had learned_router required recall 0.6875, avoid injected 8, contradictory injected 5, and stale injected 1. The failure mechanism is two-dimensional: missed required memories and contradictory contamination.

The most useful conclusion is architectural. A strong downstream reader may tolerate extra non-contradictory noise better than it tolerates missing required facts or injected contradictions. That explains why all_candidates can outperform learned_router in downstream utility despite much higher avoid-memory injection. v1.1 should therefore focus on contradiction-aware READ, not UI or broad expansion.

## Technical Deep-Dive

The system has four layers:

1. Data and task contract: current units, candidate memories, runtime context, and READ / STORE / SKIP labels.
2. Model layer: v0.5g learned_router with Unit JSON output, trained as a small LoRA router.
3. Selection harness: replay saved learned_router predictions and compare selection recall/contamination against no_memory, all_candidates, keyword_top_k, random_k, and oracle_selected.
4. Downstream harness: keep the answerer fixed and vary only the injected memory context, then evaluate automatic citation behavior and manual rubric utility.

The key engineering choice was separating model prediction from replay and downstream response generation. AutoDL produced offline prediction JSONL. The Mac harness replayed those rows without loading Qwen or LoRA. The downstream harness then tested answer quality using fixed prompts and saved responses.

This separation made the result auditable. It also made the failure visible: the full 32-case selection result is strong, but the 8-case downstream slice is harder. The slice required recall is 0.6875 and includes five missed-required cases plus five contradictory-injection cases.

## Q&A

### What problem does this project solve?

It addresses memory policy control: deciding which candidate memories should enter context and which current facts should be stored or skipped. The goal is to reduce memory pollution and context waste in agent-like workflows.

### Why is memory routing not ordinary retrieval?

Retrieval finds candidate documents or memories from a larger store. Memory routing starts after candidate retrieval: it decides which supplied memories are useful, stale, contradictory, wrong-scope, or risky for the current task.

### What model did you train?

I trained a small Qwen-family LoRA router that outputs Unit JSON READ / STORE / SKIP decisions. In the v1.0-applied package, the learned_router downstream work uses saved v0.5g offline predictions, not live model loading.

### How was the harness designed?

There are two harness layers. The selection harness measures which memory IDs are selected and what contamination enters context. The downstream harness fixes the answerer and compares response quality under different memory-injection strategies.

### What is the most important result?

Selection-level transfer is strong: learned_router required recall is 0.890625 on 32 hard READ cases. But downstream transfer is limited: in an 8-case manual review, learned_router scored 7.125, below no_memory and all_candidates.

### Why did downstream not beat no_memory?

no_memory is generic and misses memory-only facts, but it cannot be misled by bad memories. learned_router missed required memories in the downstream slice and injected contradictions in several cases, which materially hurt responses.

### Is this result a failure?

It is not a downstream win, but it is a useful research result. It proves the selection layer can improve recall, and it identifies why selection gains fail to transfer: missed required evidence and contradictory contamination.

### What would you do next?

I would build contradiction-aware READ: retrieve -> relevance -> contradiction check -> budget select. That means adding contradiction labels, pairwise memory consistency checks, abstention thresholds, and downstream-aware evaluation before retraining or building UI.

## Claim Boundaries

- Do not say READ is solved.
- Do not say the system is production-ready.
- Do not say general downstream utility is proven.
- Do not say learned_router beats all baselines.
- Safe claim: learned_router shows strong selection-level transfer and measured but limited downstream behavior on a small diagnostic subset.

# Hard READ v2 Design Repair Plan

Context 7.4-C showed that the first hard READ downstream micro-pilot was useful as a diagnostic but too biased for expansion. `no_memory` scored surprisingly well because current task notes already exposed much of the answer shape. `budgeted_candidate_order` nearly matched the oracle condition because required memories were often front-loaded in a structured order. At the same time, `all_candidates` and `keyword_top_k` still showed the intended contamination risk from stale, contradictory, wrong-scope, and same-entity distractors.

## v2 Changes

- Create a new 8-case pilot fixture under `data/v10/hard_read_v2/` without overwriting v1 artifacts.
- Use 10 candidate memories per case, with at least two required, one helpful, and four avoid memories.
- Use fixed-seed shuffled candidate order instead of label-ordering, so first-k order is no longer a favorable proxy for oracle selection.
- Make current task notes under-specified: they name the task and service but omit exact command names, thresholds, deadlines, and implementation constraints.
- Keep labels local to the case file. The shared memory pool contains only intrinsic memory fields.

v2 is designed to reduce no_memory answerability by under-specifying task notes, but this is not verified by the selection-only eval; it must be checked in a later downstream response pilot.

## Unchanged

- The work remains selection-only and no-inference.
- Strategies remain deterministic baselines plus oracle: `no_memory`, `all_candidates`, `budgeted_candidate_order`, `keyword_top_k`, `random_k`, and `oracle_selected`.
- The oracle remains a labeled reference for fixture inspection only.
- The benchmark remains a pilot, not the final 30-40 case hard READ evaluation.

## Claim Boundary

v2 repairs fixture and prompt design before any larger evaluation. It does not measure downstream answer quality, task success, real retrieval behavior, production safety, or learned router behavior.

## Learned Router / Live LoRA Boundary

No learned selector, live LoRA, saved router replay, DeepSeek call, Qwen load, training run, or external API call is part of this context. The v2 output is a cleaner hard READ fixture plus deterministic selection-only metrics.

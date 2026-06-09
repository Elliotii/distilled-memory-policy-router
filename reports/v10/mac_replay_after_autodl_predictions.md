# Mac Replay After AutoDL Predictions

After import, real predictions should exist at:

```text
data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl
```

Replay command:

```bash
python3 apps/memory_harness/eval_hard_read.py \
  --cases data/v10/hard_read_v2_expanded/hard_read_v2_expanded_cases.jsonl \
  --memory-pool data/v10/hard_read_v2_expanded/hard_read_v2_expanded_memory_pool.jsonl \
  --strategies replay_learned_router \
  --replay-predictions data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl \
  --top-k 4 \
  --max-context-chars 1600 \
  --out-dir reports/v10/hard_read_v2_expanded_learned_router_selection_eval
```

Prediction validation:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path("data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl")
rows = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
assert len(rows) == 32, len(rows)
assert all(r.get("source") == "v0.5g_offline_batch_prediction" for r in rows)
for r in rows:
    assert "case_id" in r
    assert "selected_memory_ids" in r
    assert "parse_status" in r
    assert "rendered_input_hash" in r
print("OK real predictions", len(rows))
PY
```

Replay metrics validation:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path("reports/v10/hard_read_v2_expanded_learned_router_selection_eval/metrics.json")
data = json.loads(p.read_text())
assert "aggregates" in data
assert "replay_learned_router" in data["aggregates"]
print("OK learned-router eval metrics")
PY
```

Claim boundary:

- Replay eval is a real learned-router selection result only if predictions use `source = "v0.5g_offline_batch_prediction"`.
- The debug replay fixture is harness plumbing only, not learned-router performance.
- If learned-router results are poor on hard distractor pools, report that limitation directly and do not tune fixture labels to improve the outcome.

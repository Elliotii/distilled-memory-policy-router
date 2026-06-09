# v0.5g Offline Prediction Run Report

- timestamp_utc: 2026-06-09T05:44:00.409264+00:00
- input_rows: 32
- prediction_rows: 32
- source: v0.5g_offline_batch_prediction
- model_id: Qwen3.5-4B
- adapter_id: qwen35_json_r16_1000_4090/adapter
- parse_ok_rows: 32
- parse_ok_rate: 1.0000
- parse_status_counts: {"ok": 32}
- predictions_path: data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl

Boundary: these rows are offline batch predictions from a local adapter run. Replay evaluation must be run separately on the Mac harness before reporting selection metrics.

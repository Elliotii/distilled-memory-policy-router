# Hard READ Downstream Empty Response Diagnostic

Context: 7.4-B-R pre-repair diagnostic for the first 7.4-B API run.

## Summary

- Response file: `data/v10/hard_read_downstream/hard_read_downstream_responses_deepseek_v4_flash.jsonl`
- Total rows: 24
- API OK rows: 24
- API error rows: 0
- Empty `response_text` rows: 10
- Nonempty `response_text` rows: 14

## Empty Rows By Case

| Case | Empty rows |
| --- | ---: |
| `hard_read_pilot_001` | 2 |
| `hard_read_pilot_002` | 2 |
| `hard_read_pilot_003` | 2 |
| `hard_read_pilot_009` | 4 |

## Empty Rows By Strategy

| Strategy | Empty rows |
| --- | ---: |
| `all_candidates` | 3 |
| `budgeted_candidate_order` | 1 |
| `keyword_top_k` | 2 |
| `oracle_selected` | 2 |
| `random_k` | 2 |

## Empty Rows By Case And Strategy

| Case | Strategy | Empty rows |
| --- | --- | ---: |
| `hard_read_pilot_001` | `all_candidates` | 1 |
| `hard_read_pilot_001` | `random_k` | 1 |
| `hard_read_pilot_002` | `budgeted_candidate_order` | 1 |
| `hard_read_pilot_002` | `oracle_selected` | 1 |
| `hard_read_pilot_003` | `all_candidates` | 1 |
| `hard_read_pilot_003` | `keyword_top_k` | 1 |
| `hard_read_pilot_009` | `all_candidates` | 1 |
| `hard_read_pilot_009` | `keyword_top_k` | 1 |
| `hard_read_pilot_009` | `oracle_selected` | 1 |
| `hard_read_pilot_009` | `random_k` | 1 |

## Empty Row Details

The first-run response rows stored only local response text, status, usage, and basic API metadata. No raw response body, finish reason, message-key list, or refusal/content-filter fields were available in the original file.

### `hard_read_pilot_001__all_candidates`

- case_id: `hard_read_pilot_001`
- strategy: `all_candidates`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 346, "prompt_tokens": 346, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 566}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_001__random_k`

- case_id: `hard_read_pilot_001`
- strategy: `random_k`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 262, "prompt_tokens": 262, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 482}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_002__budgeted_candidate_order`

- case_id: `hard_read_pilot_002`
- strategy: `budgeted_candidate_order`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 252, "prompt_tokens": 252, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 472}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_002__oracle_selected`

- case_id: `hard_read_pilot_002`
- strategy: `oracle_selected`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 128, "prompt_cache_miss_tokens": 106, "prompt_tokens": 234, "prompt_tokens_details": {"cached_tokens": 128}, "total_tokens": 454}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_003__all_candidates`

- case_id: `hard_read_pilot_003`
- strategy: `all_candidates`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 333, "prompt_tokens": 333, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 553}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_003__keyword_top_k`

- case_id: `hard_read_pilot_003`
- strategy: `keyword_top_k`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 254, "prompt_tokens": 254, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 474}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_009__all_candidates`

- case_id: `hard_read_pilot_009`
- strategy: `all_candidates`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 332, "prompt_tokens": 332, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 552}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_009__keyword_top_k`

- case_id: `hard_read_pilot_009`
- strategy: `keyword_top_k`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 256, "prompt_tokens": 256, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 476}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_009__random_k`

- case_id: `hard_read_pilot_009`
- strategy: `random_k`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 249, "prompt_tokens": 249, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 469}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

### `hard_read_pilot_009__oracle_selected`

- case_id: `hard_read_pilot_009`
- strategy: `oracle_selected`
- api_status: `ok`
- error: `None`
- usage: `{"completion_tokens": 220, "completion_tokens_details": {"reasoning_tokens": 220}, "prompt_cache_hit_tokens": 128, "prompt_cache_miss_tokens": 104, "prompt_tokens": 232, "prompt_tokens_details": {"cached_tokens": 128}, "total_tokens": 452}`
- available response metadata keys: `api_payload_metadata_sent, latency_seconds, model`

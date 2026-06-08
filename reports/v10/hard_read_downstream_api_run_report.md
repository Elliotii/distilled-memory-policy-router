# Hard READ Downstream API Run Report

Context: 7.4-B-S hard READ downstream DeepSeek micro-pilot token-budget repair.

- Model: `deepseek-v4-flash`
- Base URL: `https://api.deepseek.com/v1`
- Prompt count: 24
- API OK count: 24
- Usable nonempty response count: 24
- Empty OK response count: 0
- Error count: 0
- Max tokens: 600
- Retry-empty setting: 2
- Total latency seconds: 151.215

## Payload Boundary

Only `prompt_text` was sent as the user message, plus a short system instruction. Prompt metadata labels, strategies, expected answer requirements, and scoring fields were not sent in the API payload.

## Claim Boundaries

This is a 24-response micro-pilot. It does not evaluate learned router/live LoRA behavior, does not prove downstream utility, and does not establish that any selector or router outperforms alternatives. Manual review is still required for answer quality.

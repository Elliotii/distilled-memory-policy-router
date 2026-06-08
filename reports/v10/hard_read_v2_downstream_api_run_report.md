# Hard READ Downstream API Run Report

Context: hard READ downstream API micro-pilot.

- Model: `deepseek-v4-flash`
- Base URL: `https://api.deepseek.com/v1`
- Prompts attempted: 30
- API OK count: 30
- Usable nonempty response count: 30
- Empty OK response count: 0
- Error count: 0
- Max tokens: 600
- Temperature: 0
- Retry-empty setting: 2
- Total latency seconds: 178.421
- Payload metadata sent: false
- API keys logged: false

## Payload Boundary

Only `prompt_text` was sent as the user message, plus a short system instruction. Prompt metadata labels, strategies, expected answer requirements, and scoring fields were not sent in the API payload.

## Claim Boundaries

This is a response-collection and citation-diagnostic micro-pilot. It does not evaluate learned router/live LoRA behavior, does not establish downstream answer quality, and does not establish that any selector or router outperforms alternatives. Manual review is still required for answer quality.

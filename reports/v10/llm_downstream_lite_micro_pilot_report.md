# LLM Downstream-Lite Micro-Pilot Report

This report summarizes a 2-case API micro-pilot. It is not a full downstream evaluation and does not prove downstream utility.

## Run Summary

- Model: `deepseek-v4-flash`
- Base URL form used: `https://api.deepseek.com/v1`
- Case IDs: ['v05e_gold_active_0002', 'v05e_gold_active_0006']
- Strategy count: 7
- API calls attempted: 14
- OK responses: 14
- Error responses: 0
- Auth errors: 0
- Total latency seconds: 34.807
- Thinking mode notes: ['thinking_disabled_requested']

## Claim Boundaries

- This is a tiny output-level micro-pilot, not a downstream utility proof.
- It uses fixed candidate memories and saved router predictions only.
- It does not evaluate a real retriever, live router inference, memory writing, updating, merging, or lifecycle behavior.
- Citation metrics are partial automatic checks; task quality and uncited hallucination still need review.

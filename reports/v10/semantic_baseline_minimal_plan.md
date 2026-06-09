# Semantic Baseline Minimal Plan

## Scope

This plan adds a non-blocking semantic retrieval baseline for hard READ comparison. It is secondary to the learned-router gap closure. It should not delay offline learned-router replay.

No network downloads, API calls, model inference, or large model loading are required by this plan.

## Baseline Priority

1. Local embedding baseline if a small embedding stack is already installed and available locally.
2. TF-IDF fallback using the Python standard library or lightweight local dependencies.
3. Keep `keyword_top_k` as the current deterministic lexical baseline if neither option is easy.

## Local Embedding Baseline

Use only if all of the following are true:

- embedding library is already installed;
- embedding model is already local;
- no network download is required;
- runtime is small enough for the 32-case fixture;
- outputs are deterministic or seeded.

Suggested strategy name:

```text
semantic_embedding_top_k
```

Input text:

- query: `user_input + runtime_context project/repo/service/task`;
- candidate: memory text plus optional target/repo/service fields.

Metrics:

- same hard READ selection metrics as other selectors;
- report model/library name and local path;
- report that it is a local semantic baseline, not real deployed retrieval.

## TF-IDF Fallback

If local embeddings are not easy, implement:

```text
tfidf_top_k
```

Recommended design:

- tokenize with the same conservative tokenization used by the keyword retriever or a simple word regex;
- build document frequencies over the candidate memories for each case or over the full fixture pool;
- compute cosine similarity over TF-IDF vectors;
- return top-k candidate IDs;
- deterministic tie-break by candidate order.

This is enough to test whether weighted lexical semantics improves over the existing keyword/BM25-lite stub.

## Non-Blocking Policy

The semantic baseline is useful but not required for the first learned-router gap closure run. If implementation risk is higher than expected, defer it and report:

```text
semantic baseline deferred; keyword_top_k remains the lexical baseline for this run
```

Do not block learned-router replay on semantic baseline work.

## Claim Boundary

Neither local embedding nor TF-IDF evaluates real retriever behavior. These are controlled baselines over a fixed candidate pool.


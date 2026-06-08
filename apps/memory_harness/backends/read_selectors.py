"""READ selector baselines for the Applied Memory Harness."""

from __future__ import annotations

import random
from typing import Dict, List

from apps.memory_harness.retrievers import retrieve_top_k
from apps.memory_harness.schemas import JsonDict


def _ordered_existing(ids: List[str], candidate_ids: List[str]) -> List[str]:
    allowed = set(candidate_ids)
    return [memory_id for memory_id in ids if memory_id in allowed]


def select_no_memory(scenario: JsonDict, candidates: List[JsonDict], **_: object) -> JsonDict:
    return {
        "selected_memory_ids": [],
        "backend": "no_memory",
        "diagnostics": {"reason": "explicit no-memory baseline"},
    }


def select_all_candidates(scenario: JsonDict, candidates: List[JsonDict], **_: object) -> JsonDict:
    return {
        "selected_memory_ids": [memory["memory_id"] for memory in candidates],
        "backend": "all_candidates",
        "diagnostics": {"candidate_count": len(candidates)},
    }


def select_budgeted_candidate_order(
    scenario: JsonDict,
    candidates: List[JsonDict],
    *,
    k: int,
    **_: object,
) -> JsonDict:
    return {
        "selected_memory_ids": [memory["memory_id"] for memory in candidates[: max(k, 0)]],
        "backend": "budgeted_candidate_order",
        "diagnostics": {
            "k": k,
            "note": "order-sensitive first-k candidate baseline, not a learned selector",
        },
    }


def select_keyword_top_k(
    scenario: JsonDict,
    candidates: List[JsonDict],
    *,
    query: str,
    k: int,
    **_: object,
) -> JsonDict:
    retrieved = retrieve_top_k(query, candidates, k)
    return {
        "selected_memory_ids": [item["memory_id"] for item in retrieved],
        "backend": "keyword_top_k",
        "diagnostics": {
            "k": k,
            "scores": [
                {
                    "memory_id": item["memory_id"],
                    "score": item["score"],
                    "matched_tokens": item["matched_tokens"],
                }
                for item in retrieved
            ],
            "note": "deterministic keyword/BM25-lite stub, not a retrieval claim",
        },
    }


def select_random_k(
    scenario: JsonDict,
    candidates: List[JsonDict],
    *,
    k: int,
    seed: int = 1729,
    **_: object,
) -> JsonDict:
    ids = [memory["memory_id"] for memory in candidates]
    rng = random.Random(f"{seed}:{scenario['scenario_id']}")
    shuffled = ids[:]
    rng.shuffle(shuffled)
    return {
        "selected_memory_ids": sorted(shuffled[: max(k, 0)]),
        "backend": "random_k",
        "diagnostics": {"k": k, "seed": seed},
    }


def select_oracle_selected(scenario: JsonDict, candidates: List[JsonDict], **_: object) -> JsonDict:
    labels = scenario.get("labels", {})
    candidate_ids = [memory["memory_id"] for memory in candidates]
    selected = _ordered_existing(
        labels.get("required_memory_ids", []) + labels.get("helpful_memory_ids", []),
        candidate_ids,
    )
    return {
        "selected_memory_ids": selected,
        "backend": "oracle_selected",
        "diagnostics": {"uses": "required_memory_ids + helpful_memory_ids"},
    }


def select_replay_router_selected(scenario: JsonDict, candidates: List[JsonDict], **_: object) -> JsonDict:
    candidate_ids = [memory["memory_id"] for memory in candidates]
    fixture_ids = scenario.get("fixture_router_read_ids", [])
    return {
        "selected_memory_ids": _ordered_existing(fixture_ids, candidate_ids),
        "backend": "replay_router_selected",
        "diagnostics": {
            "fixture_available": bool(fixture_ids),
            "source": "scenario.fixture_router_read_ids",
        },
    }


READ_SELECTORS = {
    "no_memory": select_no_memory,
    "all_candidates": select_all_candidates,
    "budgeted_candidate_order": select_budgeted_candidate_order,
    "keyword_top_k": select_keyword_top_k,
    "random_k": select_random_k,
    "oracle_selected": select_oracle_selected,
    "replay_router_selected": select_replay_router_selected,
}


def run_read_selector(
    name: str,
    scenario: JsonDict,
    candidates: List[JsonDict],
    *,
    query: str,
    k: int,
) -> JsonDict:
    if name not in READ_SELECTORS:
        raise ValueError(f"unknown read selector: {name}")
    return READ_SELECTORS[name](scenario, candidates, query=query, k=k)

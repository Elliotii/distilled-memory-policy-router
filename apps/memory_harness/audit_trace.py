"""Audit trace construction and writing."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from apps.memory_harness.schemas import JsonDict


def _count_selected(selected_ids: List[str], label_ids: List[str]) -> int:
    return len(set(selected_ids) & set(label_ids))


def _recall(selected_ids: List[str], required_ids: List[str]) -> float:
    if not required_ids:
        return 0.0
    return _count_selected(selected_ids, required_ids) / len(required_ids)


def build_evaluation(scenario: JsonDict, selected_memory_ids: List[str]) -> JsonDict:
    labels = scenario.get("labels", {})
    required_ids = labels.get("required_memory_ids", [])
    avoid_ids = labels.get("avoid_memory_ids", [])
    stale_ids = labels.get("stale_or_harmful_memory_ids", [])
    contradictory_ids = labels.get("contradictory_memory_ids", [])
    return {
        "required_memory_ids": required_ids,
        "helpful_memory_ids": labels.get("helpful_memory_ids", []),
        "avoid_memory_ids": avoid_ids,
        "stale_or_harmful_memory_ids": stale_ids,
        "contradictory_memory_ids": contradictory_ids,
        "wrong_scope_memory_ids": labels.get("wrong_scope_memory_ids", []),
        "required_selected_recall": round(_recall(selected_memory_ids, required_ids), 6),
        "avoid_selected_count": _count_selected(selected_memory_ids, avoid_ids),
        "stale_selected_count": _count_selected(selected_memory_ids, stale_ids),
        "contradiction_selected_count": _count_selected(selected_memory_ids, contradictory_ids),
    }


def build_trace(
    *,
    scenario: JsonDict,
    current_units: List[JsonDict],
    retrieval: JsonDict,
    read_selection: JsonDict,
    write_policy: JsonDict,
    context_builder: JsonDict,
    write_preview: JsonDict,
) -> JsonDict:
    selected_ids = context_builder.get("selected_memory_ids", [])
    return {
        "trace_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scenario_id": scenario["scenario_id"],
        "user_input": scenario["user_input"],
        "current_units": current_units,
        "retrieval": retrieval,
        "read_selection": {
            "read_selector_backend": read_selection["backend"],
            "selected_memory_ids": read_selection["selected_memory_ids"],
            "diagnostics": read_selection.get("diagnostics", {}),
        },
        "write_policy": {
            "write_policy_backend": write_policy["backend"],
            "store_units": write_policy.get("store_units", []),
            "skip_unit_ids": write_policy.get("skip_unit_ids", []),
            "diagnostics": write_policy.get("diagnostics", {}),
        },
        "context_builder": context_builder,
        "downstream_response": {
            "backend": "none",
            "response_text": "",
            "citations": [],
            "note": "No downstream LLM is run by this harness skeleton.",
        },
        "write_preview": write_preview,
        "evaluation": build_evaluation(scenario, selected_ids),
        "claim_boundary": (
            "Skeleton trace for deterministic fixture replay; not production "
            "readiness, live retrieval evidence, or answer-quality proof."
        ),
    }


def write_trace(path: str, trace: JsonDict) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n")

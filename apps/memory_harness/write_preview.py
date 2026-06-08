"""STORE/SKIP preview helpers.

STORE is preview-only in this skeleton. Flags are audit aids, not safety
guarantees.
"""

from __future__ import annotations

from typing import Dict, List

from apps.memory_harness.schemas import JsonDict


SENSITIVE_MARKERS = [
    "ssn",
    "password",
    "token",
    "api key",
    "apikey",
    "address",
    "credit card",
]

STALE_MARKERS = [
    "old",
    "resolved",
    "hypothetical",
    "not current",
    "no longer active",
]


def audit_flags(text: str) -> List[str]:
    lowered = text.lower()
    flags: List[str] = []
    if any(marker in lowered for marker in SENSITIVE_MARKERS):
        flags.append("sensitive_boundary")
    if any(marker in lowered for marker in STALE_MARKERS):
        flags.append("stale_or_hypothetical")
    return flags


def build_write_preview(
    current_units: List[JsonDict],
    store_units: List[JsonDict],
    skip_unit_ids: List[str],
) -> JsonDict:
    unit_by_id: Dict[str, JsonDict] = {unit["unit_id"]: unit for unit in current_units}
    store_previews = []
    for item in store_units:
        unit_id = item["unit_id"]
        unit = unit_by_id.get(unit_id, {"text": ""})
        text = unit.get("text", "")
        store_previews.append({
            "unit_id": unit_id,
            "target": item.get("target", ""),
            "text": text,
            "review_required": True,
            "action": "preview_store",
            "flags": sorted(set(unit.get("flags", []) + audit_flags(text))),
        })

    skip_previews = []
    for unit_id in skip_unit_ids:
        unit = unit_by_id.get(unit_id, {"text": ""})
        text = unit.get("text", "")
        skip_previews.append({
            "unit_id": unit_id,
            "text": text,
            "action": "skip",
            "flags": sorted(set(unit.get("flags", []) + audit_flags(text))),
        })

    return {
        "store_previews": store_previews,
        "skip_previews": skip_previews,
        "diagnostics": {
            "store_is_preview_only": True,
            "flag_note": "flags are audit aids, not safety guarantees",
        },
    }


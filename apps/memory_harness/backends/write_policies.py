"""WRITE policy baselines for the Applied Memory Harness."""

from __future__ import annotations

from typing import List

from apps.memory_harness.schemas import JsonDict


def disabled_write_policy(scenario: JsonDict, current_units: List[JsonDict]) -> JsonDict:
    return {
        "store_units": [],
        "skip_unit_ids": [],
        "backend": "disabled",
        "diagnostics": {"reason": "write policy disabled"},
    }


def fixture_write_policy(scenario: JsonDict, current_units: List[JsonDict]) -> JsonDict:
    unit_ids = {unit["unit_id"] for unit in current_units}
    store_units = [
        item
        for item in scenario.get("fixture_store_units", [])
        if item.get("unit_id") in unit_ids
    ]
    skip_unit_ids = [
        unit_id
        for unit_id in scenario.get("fixture_skip_unit_ids", [])
        if unit_id in unit_ids
    ]
    return {
        "store_units": store_units,
        "skip_unit_ids": skip_unit_ids,
        "backend": "fixture",
        "diagnostics": {"source": "scenario fixture write labels"},
    }


WRITE_POLICIES = {
    "disabled": disabled_write_policy,
    "fixture": fixture_write_policy,
}


def run_write_policy(name: str, scenario: JsonDict, current_units: List[JsonDict]) -> JsonDict:
    if name not in WRITE_POLICIES:
        raise ValueError(f"unknown write policy: {name}")
    return WRITE_POLICIES[name](scenario, current_units)


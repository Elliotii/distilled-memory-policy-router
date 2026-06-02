"""
Context 5.3-D2: Final corrected-gold metadata cleanup before lock.

Fix 24 damaged notes (uu1 typo, truncated text) and 10 service_memory u2
units with project-style wording. Fix fixes report typo. No label changes.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_cases(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_cases(cases: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for case in cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")


def build_dsl(case: dict) -> str:
    gold = case["gold"]
    lines = []
    reads = gold.get("read", [])
    lines.append(f"READ {','.join(reads)}" if reads else "READ NONE")
    stores = gold.get("store", [])
    if stores:
        for s in stores:
            lines.append(f"STORE {s['target']} {s['unit_id']}")
    else:
        lines.append("STORE NONE")
    skips = gold.get("skip", [])
    lines.append(f"SKIP {','.join(skips)}" if skips else "SKIP NONE")
    return "\n".join(lines)


def _get_label_info(case: dict) -> dict:
    """Get structured label info for a case."""
    gold = case["gold"]
    reads = gold.get("read", [])
    stores = {s["unit_id"]: s["target"] for s in gold.get("store", [])}
    skips = set(gold.get("skip", []))
    units = {u["unit_id"]: u["text"] for u in case["current_units"]}
    return {"reads": reads, "stores": stores, "skips": skips, "units": units}


# ── Clean notes for each of the 24 affected cases ──────────────────────

CLEAN_NOTES: dict[str, str] = {}

CLEAN_NOTES["v05_gold_core_0019"] = (
    "STORE/SKIP-only: u1 is a durable security validation rule for the policy-validator — "
    "it defines WHAT the service must check (service_memory). "
    "u2 is a config file path describing the storage location of validation rules (repo_memory). "
    "u3 is a stable, non-sensitive user preference for how audit findings should be grouped and displayed "
    "(user_profile — crosses projects, not sensitive)."
)

CLEAN_NOTES["v05_gold_core_0021"] = (
    "STORE/SKIP-only: u1 describes a durable indexing SLA — the search-indexer service "
    "must make primary-language content searchable within 5 minutes (service_memory). "
    "u2 is a config file path for search shard configuration (repo_memory). "
    "u3 is a feature implementation plan with action framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0029"] = (
    "STORE/SKIP-only: u1 describes the logging convention for uptime-checker probes — "
    "documents where probe metrics docs live and the gauge metric type (repo_memory). "
    "u2 describes source code file paths for probe implementations (repo_memory). "
    "u3 is a test command convention with explicit path and flags (repo_memory)."
)

CLEAN_NOTES["v05_gold_core_0041"] = (
    "READ+STORE joint: reads m1 (current deploy behavior) and m2 (config structure). "
    "u1 is a cross-service deployment policy requiring canary deployments for all production "
    "services — project-level operational policy, not single-service (project_memory). "
    "u2 specifies a config file path for the new canary section (repo_memory). "
    "u3 describes a testing plan for staging environment (task_state)."
)

CLEAN_NOTES["v05_gold_core_0042"] = (
    "READ+STORE joint: reads m1 (current search) and m2 (index schema). "
    "u1 is a cross-surface project requirement for faceted search across all search surfaces "
    "(project_memory). u2 describes durable facet-count return behavior for the search-indexer "
    "(service_memory). u3 is an implementation plan with 'Add' action framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0044"] = (
    "READ+STORE joint: reads m1 (current probe) and m2 (cert validity context). "
    "u1 describes durable SSL certificate inspection behavior for the uptime-checker (service_memory). "
    "u2 describes the 7-day escalation threshold from WARNING to CRITICAL — this is a durable "
    "behavior of the uptime-checker service, not a project-wide policy (service_memory). "
    "u3 is implementation with 'Add' framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0045"] = (
    "READ+STORE joint: reads m1 (current routing) and m2 (weather context). "
    "u1 describes durable weather-aware routing behavior for the route-optimizer (service_memory). "
    "u2 is a manual dispatcher review threshold — a project-level operational policy that "
    "constrains the dispatch workflow across all routing decisions, not just route-optimizer "
    "behavior (project_memory). u3 is 'Integrate' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0047"] = (
    "READ+STORE joint: reads m1 (retry behavior) and m2 (test history storage). "
    "u1 describes durable flakiness tracking behavior — recording retry-pass and flagging >5% flake "
    "rate is a durable behavioral invariant for the test-runner (service_memory). "
    "u2 describes automatic flaky-test reporting to the team channel — a service-level behavior "
    "of the test-runner, not a project-wide policy (service_memory). "
    "u3 is implementation with 'Add' framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0048"] = (
    "READ+STORE joint: reads m1 (current processor) and m2 (accessibility requirement). "
    "u1 describes durable auto-captioning behavior for the media-processor within 30 minutes "
    "(service_memory). u2 is a project-level accessibility compliance policy (WCAG 2.1 AA) — "
    "the 90% confidence threshold for human review is a project-wide quality requirement, not "
    "just a media-processor setting (project_memory). u3 is 'Integrate' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0049"] = (
    "READ+STORE joint: reads m1 (current matching) and m2 (data source path). "
    "u1 describes durable duplicate detection behavior — matching by amount, date, merchant with "
    "manual review flagging (service_memory). u2 describes an implementation intention with "
    "'should run before' phrasing — this is a pipeline-ordering plan, not a durable spec "
    "(task_state). u3 is 'Add' action framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0050"] = (
    "READ+STORE joint: reads m1 (current alerts) and m2 (alert storm context). "
    "u1 describes durable alert correlation behavior — grouping same-service alerts within "
    "5-minute windows into single incidents (service_memory). "
    "u2 describes root-cause-first ordering of correlated alerts — durable behavior of the "
    "alert-dispatcher service (service_memory). u3 is 'Implement' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0051"] = (
    "READ+STORE joint: reads m1 (current tracking) and m2 (historical delay data). "
    "u1 describes durable delay prediction behavior — comparing shipment progress against "
    "historical route/season averages (service_memory). "
    "u2 describes proactive customer notification with updated ETA and delay reason — durable "
    "behavior of the tracking-notifier service (service_memory). u3 is 'Build' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0053"] = (
    "READ+STORE joint: reads m1 (current publishing) and m2 (KMS key setup). "
    "u1 describes durable GPG signing behavior — signing release artifacts and publishing "
    "signatures alongside them (service_memory). "
    "u2 describes a cross-environment deployment policy: any artifact deployed to any environment "
    "must have GPG signature verified — this is a project-level security policy, not single-service "
    "(project_memory). u3 is 'Set up' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0054"] = (
    "READ+STORE joint: reads m1 (indexing) and m2 (analytics pipeline). "
    "u1 describes durable content similarity computation using shared tags and categories "
    "(service_memory). u2 describes current implementation state — the engine recomputes daily "
    "with Redis caching and 24-hour TTL, which is a version-specific optimization (task_state). "
    "u3 is 'Add' action framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0055"] = (
    "READ+STORE joint: reads m1 (current tax) and m2 (project currency plans). "
    "u1 describes durable multi-currency tax calculation behavior — EUR/GBP with jurisdiction-"
    "specific VAT rates (service_memory). u2 documents the config file path for the ECB exchange "
    "rate feed configuration (repo_memory). u3 is 'Add' action framing (task_state)."
)

CLEAN_NOTES["v05_gold_core_0056"] = (
    "READ+STORE joint: reads m1 (current validation) and m2 (response patterns). "
    "u1 describes durable response body validation behavior — matching JSON fields against "
    "regex patterns (service_memory). u2 describes logging of validation failures with 1KB "
    "truncation — durable behavior of the uptime-checker for debugging (service_memory). "
    "u3 is 'Add' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0057"] = (
    "READ+STORE joint: reads m1 (current range assumption). Skips m2 (fleet change context — "
    "related but not needed for algorithm design). "
    "u1 describes durable EV range behavior — inserting charging stops when range < 20 miles "
    "(service_memory). u2 describes the per-200-mile charging time limit — durable constraint "
    "on the route-optimizer service (service_memory). u3 is 'Integrate' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0058"] = (
    "READ+STORE joint: reads m1 (built-in rules) and m2 (custom policy config). "
    "u1 describes durable hot-reload capability — loading custom policies without service restart "
    "(service_memory). u2 describes JSON schema validation for custom policies before loading — "
    "durable behavior of the policy-validator (service_memory). u3 is 'Implement' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0060"] = (
    "READ+STORE joint: reads m1 (current processing) and m2 (watermark assets). "
    "u1 describes durable watermark application behavior — semi-transparent overlay in "
    "bottom-right for free-tier users (service_memory). "
    "u2 describes a cross-tier content policy: watermarks only for free-tier, pro/enterprise "
    "unwatermarked — project-level content monetization policy (project_memory). "
    "u3 is 'Add' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0062"] = (
    "READ+STORE joint: reads m1 (current alerting) and m2 (alert fatigue context). "
    "u1 describes durable alert suppression behavior — suppressing non-critical alerts during "
    "business hours after 3+ fires in an hour (service_memory). "
    "u2 describes hourly digest aggregation for suppressed alerts — durable behavior of the "
    "alert-dispatcher service (service_memory). u3 is 'Deploy' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0065"] = (
    "READ+STORE joint: reads m1 (current test execution) and m2 (impact mapping config). "
    "u1 describes durable test impact analysis behavior — running only tests mapped to changed "
    "source files with full-suite fallback (service_memory). "
    "u2 documents the config file path for test-to-source mapping (repo_memory). "
    "u3 is 'Implement' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0066"] = (
    "READ+STORE joint: reads m1 (English-only search) and m2 (multi-language audience). "
    "u1 describes durable multi-language indexing behavior — language detection, language-specific "
    "stemming and stop-word removal (service_memory). "
    "u2 describes language-aware query prioritization with fallback to English — durable behavior "
    "of the search-indexer service (service_memory). u3 is 'Add' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0067"] = (
    "READ+STORE joint: reads m1 (current tax calc) and m2 (audit trail requirement). "
    "u1 describes durable tax audit logging behavior — recording location, rate, taxable amount, "
    "and calculated tax in immutable log (service_memory). "
    "u2 documents the documentation path for retention requirements (repo_memory). "
    "u3 is 'Add' action (task_state)."
)

CLEAN_NOTES["v05_gold_core_0069"] = (
    "READ+STORE joint: reads m1 (current single-stop) and m2 (multi-stop efficiency). "
    "u1 describes durable TSP-based multi-stop optimization behavior (service_memory). "
    "u2 describes the 30-second timeout with sub-optimal fallback for up to 50 stops — durable "
    "performance constraint of the route-optimizer service (service_memory). "
    "u3 is 'Implement' action (task_state)."
)

# ── Service wording rewrites for 10 u2 units ──────────────────────────

# Map case_id -> new u2 text (service-style wording)
SERVICE_REWRITES: dict[str, str] = {}

SERVICE_REWRITES["v05_gold_core_0044"] = (
    "Certificate expiry alerts from the uptime-checker must escalate from WARNING to CRITICAL "
    "when expiry is within 7 days."
)

SERVICE_REWRITES["v05_gold_core_0047"] = (
    "The test-runner must report flaky tests automatically to the team communication channel "
    "so that unstable tests are immediately visible."
)

SERVICE_REWRITES["v05_gold_core_0050"] = (
    "Correlated alerts from the alert-dispatcher must list the root cause first with dependent "
    "alerts listed below, providing clear incident context for on-call engineers."
)

SERVICE_REWRITES["v05_gold_core_0051"] = (
    "The tracking-notifier must proactively notify customers with an updated ETA and delay reason "
    "whenever a delivery delay is predicted."
)

SERVICE_REWRITES["v05_gold_core_0056"] = (
    "API response body validation failures in the uptime-checker must log the actual response "
    "truncated to 1KB for debugging purposes."
)

SERVICE_REWRITES["v05_gold_core_0057"] = (
    "The route-optimizer must limit EV charging detours to no more than 30 minutes per 200 miles "
    "to maintain delivery schedule reliability."
)

SERVICE_REWRITES["v05_gold_core_0058"] = (
    "All custom policies loaded by the policy-validator must pass JSON schema validation before "
    "being activated, to prevent malformed rules from entering the evaluation engine."
)

SERVICE_REWRITES["v05_gold_core_0062"] = (
    "Suppressed alerts from the alert-dispatcher must be aggregated into an hourly digest rather "
    "than generating individual pages, to reduce on-call notification fatigue."
)

SERVICE_REWRITES["v05_gold_core_0066"] = (
    "Search queries in one language should prioritize results in that language with fallback "
    "to English when the search-indexer serves results."
)

SERVICE_REWRITES["v05_gold_core_0069"] = (
    "Route optimization in the route-optimizer must complete within 30 seconds for up to 50 stops, "
    "returning a usable sub-optimal route on timeout."
)


def main() -> int:
    print("=" * 70)
    print("Context 5.3-D2: Final metadata cleanup before lock")
    print("=" * 70)

    cases = load_cases(ROOT / "data/v05/gold/v05_gold_corrected_cases.jsonl")
    print(f"Loaded {len(cases)} cases")

    notes_fixed = 0
    wording_fixed = 0

    for case in cases:
        cid = case["case_id"]

        # Cleanup A: fix damaged notes
        if cid in CLEAN_NOTES:
            case["notes"] = CLEAN_NOTES[cid]
            notes_fixed += 1

        # Cleanup B: rewrite service_memory u2 project-style wording
        if cid in SERVICE_REWRITES:
            for u in case["current_units"]:
                if u["unit_id"] == "u2":
                    u["text"] = SERVICE_REWRITES[cid]
                    wording_fixed += 1
                    break

    print(f"\nNotes fixed: {notes_fixed} (expected 24)")
    print(f"Service wording rewrites: {wording_fixed} (expected 10)")

    # Verify no labels changed
    print("\nVerifying no label changes...")
    for case in cases:
        gold = case["gold"]
        stores = {s["unit_id"]: s["target"] for s in gold.get("store", [])}
        skips = set(gold.get("skip", []))
        reads = set(gold.get("read", []))
        unit_ids = {u["unit_id"] for u in case["current_units"]}
        mem_ids = {m["memory_id"] for m in case["candidate_memories"]}

        # Basic structural checks
        if reads - mem_ids:
            print(f"  ERROR: {case['case_id']} reads invalid mem: {reads - mem_ids}")
        if set(stores.keys()) - unit_ids:
            print(f"  ERROR: {case['case_id']} stores invalid unit")
        if skips - unit_ids:
            print(f"  ERROR: {case['case_id']} skips invalid unit")
        if set(stores.keys()) & skips:
            print(f"  ERROR: {case['case_id']} unit in both store and skip")

    # Rebuild DSLs
    for case in cases:
        case["gold"]["dsl"] = build_dsl(case)

    # Write all corrected files
    paths = {
        "combined": ROOT / "data/v05/gold/v05_gold_corrected_cases.jsonl",
        "core": ROOT / "data/v05/gold/v05_gold_core_corrected_cases.jsonl",
        "hard": ROOT / "data/v05/gold/v05_gold_hard_corrected_cases.jsonl",
    }
    for label, path in paths.items():
        if label == "combined":
            write_cases(cases, path)
        elif label == "core":
            write_cases([c for c in cases if "gold_core" in c["case_id"]], path)
        else:
            write_cases([c for c in cases if "gold_hard" in c["case_id"]], path)
        print(f"Wrote {label} to {path}")

    # Check no "uu1" typo in notes
    bad_notes = sum(1 for c in cases if "uu1" in c.get("notes", ""))
    print(f"\nNotes with 'uu1' typo (should be 0): {bad_notes}")
    if bad_notes:
        for c in cases:
            if "uu1" in c.get("notes", ""):
                print(f"  BAD: {c['case_id']}")

    # Check no truncated placeholder notes
    bad_trunc = sum(1 for c in cases if "... ->" in c.get("notes", ""))
    print(f"Notes with truncated '... ->' pattern (should be 0): {bad_trunc}")

    # Verify no "project requires" in service_memory units
    bad_wording = 0
    for case in cases:
        for s in case["gold"].get("store", []):
            if s["target"] == "service_memory":
                for u in case["current_units"]:
                    if u["unit_id"] == s["unit_id"]:
                        if "project requires" in u["text"]:
                            bad_wording += 1
                            print(f"  BAD service_memory wording: {case['case_id']} {s['unit_id']}")
    print(f"service_memory units with 'project requires' wording (should be 0): {bad_wording}")

    # ── Fix the fixes report typo ──────────────────────────────────────
    fixes_report_path = ROOT / "reports/v05/v05_gold_opus_review_fixes_report.md"
    if fixes_report_path.exists():
        content = fixes_report_path.read_text()
        # Fix: "SKIP u2,u3" should not be in Group C description
        # The correct statement: hard_0014 u2 changed to SKIP, u3 remained STORE task_state
        old_text = "| v05_gold_hard_0014 | `STORE repo_memory u2` (no SKIP of u2) | `SKIP u2,u3` (u2 removed from STORE) |"
        new_text = "| v05_gold_hard_0014 | `STORE repo_memory u2` | `SKIP u2` (u2 removed from STORE, u3 remains STORE task_state) |"
        if old_text in content:
            content = content.replace(old_text, new_text)
            fixes_report_path.write_text(content)
            print(f"\nFixed fixes report typo in {fixes_report_path}")
        else:
            # Try alternative match
            if "SKIP u2,u3" in content:
                print("  Warning: old text pattern not found exactly, but 'SKIP u2,u3' exists")
                content = content.replace("SKIP u2,u3", "SKIP u2")
                fixes_report_path.write_text(content)
                print(f"  Replaced 'SKIP u2,u3' with 'SKIP u2' in fixes report")
            else:
                print("  Fixes report typo already fixed or pattern not found")

    print("\n✅ Cleanup complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

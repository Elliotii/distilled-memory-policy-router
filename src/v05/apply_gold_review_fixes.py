"""
Apply Opus gold review fixes to v05 gold draft.

Context 5.3-D: Reads gold draft JSONL, applies required fixes (groups A-E),
validates everything, writes corrected gold files.

Does NOT lock gold, train, or run inference.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS
from src.v04.case_validator import validate_case

# ── File paths ──────────────────────────────────────────────────────────

DRAFT_PATH = ROOT / "data/v05/gold/v05_gold_draft_cases.jsonl"
CORRECTED_PATH = ROOT / "data/v05/gold/v05_gold_corrected_cases.jsonl"
CORE_CORRECTED_PATH = ROOT / "data/v05/gold/v05_gold_core_corrected_cases.jsonl"
HARD_CORRECTED_PATH = ROOT / "data/v05/gold/v05_gold_hard_corrected_cases.jsonl"

REPORTS_DIR = ROOT / "reports/v05"


def load_cases(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_cases(cases: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for case in cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")


def build_dsl(case: dict[str, Any]) -> str:
    """Rebuild gold.dsl from gold.read / gold.store / gold.skip."""
    gold = case["gold"]
    lines = []

    reads = gold.get("read", [])
    if reads:
        lines.append(f"READ {','.join(reads)}")
    else:
        lines.append("READ NONE")

    stores = gold.get("store", [])
    if stores:
        for s in stores:
            lines.append(f"STORE {s['target']} {s['unit_id']}")
    else:
        lines.append("STORE NONE")

    skips = gold.get("skip", [])
    if skips:
        lines.append(f"SKIP {','.join(skips)}")
    else:
        lines.append("SKIP NONE")

    return "\n".join(lines)


def update_dsl(case: dict[str, Any]) -> None:
    """Rebuild case['gold']['dsl'] from structured fields."""
    case["gold"]["dsl"] = build_dsl(case)


def validate_case_parsed(case: dict[str, Any]) -> list[str]:
    """Validate a single case: structural, DSL parse, canonical consistency."""
    errors = []

    result = validate_case(case)
    if not result["valid"]:
        errors.extend(f"structural: {e}" for e in result["errors"])

    gold = case["gold"]
    mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
    unit_ids = [u["unit_id"] for u in case["current_units"]]
    parsed = parse_policy_dsl(gold["dsl"], mem_ids, unit_ids, LEGAL_TARGETS)
    if not parsed["validation"]["valid"]:
        errors.extend(f"dsl parse: {e}" for e in parsed["validation"]["errors"])

    # Canonical consistency
    parsed_read = {item["memory_id"] for item in parsed["read"]}
    parsed_store = {item["unit_id"]: item["target"] for item in parsed["store"]}
    parsed_skip = {item["unit_id"] for item in parsed["skip"]}
    gold_read = set(gold.get("read", []))
    gold_store = {s["unit_id"]: s["target"] for s in gold.get("store", [])}
    gold_skip = set(gold.get("skip", []))

    if parsed_read != gold_read:
        errors.append(f"READ mismatch: parsed={sorted(parsed_read)} gold={sorted(gold_read)}")
    if parsed_store != gold_store:
        errors.append(f"STORE mismatch: parsed={sorted(parsed_store.items())} gold={sorted(gold_store.items())}")
    if parsed_skip != gold_skip:
        errors.append(f"SKIP mismatch: parsed={sorted(parsed_skip)} gold={sorted(gold_skip)}")

    return errors


def distribution_summary(cases: list[dict[str, Any]]) -> dict:
    """Compute target and shape distribution."""
    targets = Counter()
    shapes = {"READ+STORE joint": 0, "STORE/SKIP-only": 0, "READ-only": 0}
    case_ids = set()
    case_ids_read = set()
    case_ids_store = set()
    case_ids_skip = set()
    read_count = 0
    store_count = 0
    skip_count = 0

    for c in cases:
        case_ids.add(c["case_id"])
        gold = c["gold"]
        has_read = bool(gold.get("read"))
        has_store = bool(gold.get("store"))
        has_skip = bool(gold.get("skip"))

        if has_read:
            case_ids_read.add(c["case_id"])
            read_count += len(gold["read"])
        if has_store:
            case_ids_store.add(c["case_id"])
            store_count += len(gold["store"])
        if has_skip:
            case_ids_skip.add(c["case_id"])
            skip_count += len(gold["skip"])

        if has_read and has_store:
            shapes["READ+STORE joint"] += 1
        elif has_read:
            shapes["READ-only"] += 1
        elif has_store:
            shapes["STORE/SKIP-only"] += 1

        for s in gold.get("store", []):
            targets[s["target"]] += 1

    total_store = sum(targets.values())
    return {
        "total_cases": len(cases),
        "core_cases": sum(1 for c in cases if "gold_core" in c["case_id"]),
        "hard_cases": sum(1 for c in cases if "gold_hard" in c["case_id"]),
        "targets": dict(targets),
        "target_pcts": {k: round(v / total_store * 100, 1) for k, v in targets.items()} if total_store else {},
        "total_store_units": total_store,
        "shapes": shapes,
        "shape_pcts": {k: round(v / len(cases) * 100) for k, v in shapes.items()} if cases else {},
        "cases_with_read": len(case_ids_read),
        "cases_with_store": len(case_ids_store),
        "cases_with_skip": len(case_ids_skip),
        "read_decision_count": read_count,
        "store_unit_count": store_count,
        "skip_unit_count": skip_count,
    }


def sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ── Fixes ───────────────────────────────────────────────────────────────

def apply_fixes(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply all Opus review fixes. Returns fix log."""
    fix_log: dict[str, list[str]] = {
        "group_a_svc_proj_rollback": [],
        "group_b_false_user_profile": [],
        "group_c_work_email_skip": [],
        "group_d_phone_collision": [],
        "group_e_replace_easy_hard": [],
        "borderline_reviewed": [],
        "notes_synchronized": [],
    }

    case_map = {c["case_id"]: c for c in cases}

    # ── Fix group A: svc→proj rollback to service_memory ────────────────
    rollback_cases = {
        "v05_gold_core_0044": "u2",
        "v05_gold_core_0047": "u2",
        "v05_gold_core_0050": "u2",
        "v05_gold_core_0051": "u2",
        "v05_gold_core_0056": "u2",
        "v05_gold_core_0057": "u2",
        "v05_gold_core_0058": "u2",
        "v05_gold_core_0066": "u2",
    }

    for case_id, unit_id in rollback_cases.items():
        case = case_map[case_id]
        gold = case["gold"]
        old_dsl = gold["dsl"]

        # Update store target
        for s in gold["store"]:
            if s["unit_id"] == unit_id:
                s["target"] = "service_memory"
                break

        # Rebuild DSL
        update_dsl(case)

        # Update notes
        unit_text = ""
        for u in case["current_units"]:
            if u["unit_id"] == unit_id:
                unit_text = u["text"]
                break
        case["notes"] = _rewrite_svc_rollback_note(case, unit_id, unit_text)

        fix_log["group_a_svc_proj_rollback"].append(
            f"{case_id} {unit_id}: project_memory -> service_memory"
        )

    # ── Fix group B: false user_profile ──────────────────────────────────
    case = case_map["v05_gold_core_0021"]
    gold = case["gold"]
    for s in gold["store"]:
        if s["unit_id"] == "u1":
            s["target"] = "service_memory"
            break
    update_dsl(case)
    case["notes"] = (
        "STORE/SKIP-only: u1 is an indexing SLA expectation (service_memory — "
        "it describes a durable service requirement for search-indexer indexing "
        "latency, not a stable cross-project user preference). u2 is config path "
        "(repo_memory). u3 is a feature plan (task_state — 'Add a search relevance dashboard')."
    )
    fix_log["group_b_false_user_profile"].append(
        "v05_gold_core_0021 u1: user_profile -> service_memory"
    )

    # ── Fix group C: work email should SKIP ──────────────────────────────
    case = case_map["v05_gold_hard_0014"]
    gold = case["gold"]
    # Remove u2 from store
    gold["store"] = [s for s in gold["store"] if s["unit_id"] != "u2"]
    # Add u2 to skip
    if "u2" not in gold["skip"]:
        gold["skip"].append("u2")
        # Keep skip list sorted
        gold["skip"] = sorted(gold["skip"])
    update_dsl(case)
    case["notes"] = (
        "HARD user_profile_vs_sensitive: u1 is a safe sorting preference (user_profile). "
        "u2 is a work email address — email addresses (even work emails) are personal "
        "contact info and must be SKIPped per V05_LABEL_POLICY sensitive/private policy. "
        "u3 is current behavior (task_state)."
    )
    fix_log["group_c_work_email_skip"].append(
        "v05_gold_hard_0014 u2: repo_memory -> SKIP (email = sensitive)"
    )

    # ── Fix group D: phone number collision ──────────────────────────────
    case = case_map["v05_gold_hard_0015"]
    for u in case["current_units"]:
        if u["unit_id"] == "u3":
            old_text = u["text"]
            u["text"] = (
                "My recovery phone number for PagerDuty account recovery is +1-555-0147."
            )
            break
    case["notes"] = case["notes"].replace(
        "phone number — clear PII, must SKIP.",
        "phone number (synthetic +1-555-0147) — PII, must SKIP."
    )
    fix_log["group_d_phone_collision"].append(
        f"v05_gold_hard_0015 u3: phone +1-555-0198 -> +1-555-0147 (avoid train sensitive-boundary pattern collision)"
    )

    # ── Fix group E: replace too-easy hard case ──────────────────────────
    # Replace v05_gold_hard_0013 with a genuine repo-vs-service boundary case
    case = case_map["v05_gold_hard_0013"]

    # Keep the runtime context same (shipping-logistics / tracking-notifier)
    # but redo units and labels to create genuine ambiguity
    case["case_id"] = "v05_gold_hard_0013"
    case["tags"] = ["store_skip_only", "repo_vs_service", "target_boundary"]

    # New current units with genuine repo-vs-service ambiguity
    case["current_units"] = [
        {
            "unit_id": "u1",
            "text": (
                "The tracking-notifier must deduplicate carrier scan events by "
                "shipment_id and event_type within a 10-minute window, discarding "
                "any duplicate event that arrives after the first instance."
            ),
        },
        {
            "unit_id": "u2",
            "text": (
                "The deduplication window and event-type key configuration are "
                "in config/notification_dedup.yaml with the fields window_minutes, "
                "event_key_fields, and discard_policy."
            ),
        },
        {
            "unit_id": "u3",
            "text": (
                "The dedup logic implementation is in services/notifier/dedup.py "
                "and the unit tests covering duplicate detection scenarios live in "
                "tests/notifier/test_dedup.py."
            ),
        },
    ]

    case["gold"] = {
        "read": [],
        "store": [
            {"target": "service_memory", "unit_id": "u1"},
            {"target": "repo_memory", "unit_id": "u2"},
            {"target": "repo_memory", "unit_id": "u3"},
        ],
        "skip": [],
    }
    update_dsl(case)

    case["notes"] = (
        "HARD repo_vs_service (rewritten per Opus review): u1 describes WHAT the "
        "tracking-notifier DOES — deduplication behavior is a durable service invariant "
        "(service_memory). u2 names a configuration file path (repo_memory) BUT also "
        "describes the config schema fields (window_minutes, event_key_fields, "
        "discard_policy) which are service behavior details. The boundary is ambiguous: "
        "is mentioning config field names sufficient to make u2 service_memory? We judge "
        "no — the primary content is WHERE configuration lives, with incidental field "
        "names to identify the file. u3 is source code and test paths (repo_memory) BUT "
        "also references the dedup logic, making it slightly harder to classify. "
        "The genuine challenge is recognizing that config paths + field name hints still "
        "belong in repo_memory."
    )

    fix_log["group_e_replace_easy_hard"].append(
        "v05_gold_hard_0013: replaced with genuine repo-vs-service boundary case"
    )

    # ── Borderline review ──────────────────────────────────────────────
    borderline_cases = [
        "v05_gold_core_0045",
        "v05_gold_core_0048",
        "v05_gold_core_0062",
        "v05_gold_core_0069",
        "v05_gold_core_0049",
    ]

    for bid in borderline_cases:
        c = case_map[bid]
        fix_log["borderline_reviewed"].append(
            _borderline_review(c)
        )

    # ── Notes synchronization ───────────────────────────────────────────
    # For all 25 post-processing adjusted cases (from the adjustment log),
    # verify and fix notes to match final labels.
    pp_cases = set()
    # Read adjustment log to get the case list
    adj_log_path = REPORTS_DIR / "v05_gold_postprocessing_adjustment_log.md"
    # We hardcode the list from the Opus review
    pp_adjusted = [
        "v05_gold_core_0021", "v05_gold_core_0029", "v05_gold_core_0041",
        "v05_gold_core_0042", "v05_gold_core_0044", "v05_gold_core_0045",
        "v05_gold_core_0047", "v05_gold_core_0048", "v05_gold_core_0049",
        "v05_gold_core_0050", "v05_gold_core_0051", "v05_gold_core_0053",
        "v05_gold_core_0054", "v05_gold_core_0055", "v05_gold_core_0056",
        "v05_gold_core_0057", "v05_gold_core_0058", "v05_gold_core_0060",
        "v05_gold_core_0062", "v05_gold_core_0065", "v05_gold_core_0066",
        "v05_gold_core_0067",  # round 2 cases also
        "v05_gold_core_0019",  # round 3
    ]

    for pp_cid in pp_adjusted:
        c = case_map.get(pp_cid)
        if c:
            c["notes"] = _sync_notes(c)
            fix_log["notes_synchronized"].append(pp_cid)

    return fix_log


def _rewrite_svc_rollback_note(case: dict[str, Any], unit_id: str, unit_text: str) -> str:
    """Create a notes entry explaining the service_memory label after rollback."""
    # Build a simple summary of final labels
    stores = case["gold"]["store"]
    store_summary = ", ".join(
        f"u{s['unit_id']} = {s['target']}" for s in stores
    )
    skips = case["gold"]["skip"]
    skip_summary = f"SKIP: {','.join(skips)}" if skips else "no SKIPs"
    reads = case["gold"]["read"]
    read_summary = f"READ: {','.join(reads)}" if reads else "no READs"

    return (
        f"{read_summary}. Final labels: {store_summary}. {skip_summary}. "
        f"(u2 label: service_memory — describes single-service durable behavior, "
        f"not project-level scope/policy. The 'The {{project}} project requires...' "
        f"prefix is not sufficient to make this project_memory per V05_LABEL_POLICY.)"
    )


def _borderline_review(case: dict[str, Any]) -> str:
    """Review borderline case and return a decision string."""
    case_id = case["case_id"]
    gold = case["gold"]
    stores = gold.get("store", [])

    # Build unit text lookup
    unit_texts = {u["unit_id"]: u["text"] for u in case["current_units"]}

    lines = [f"\n### {case_id}"]
    for s in stores:
        uid = s["unit_id"]
        target = s["target"]
        text = unit_texts.get(uid, "?")
        lines.append(f"- **u{uid}**: `{target}` — \"{text[:120]}...\"")

    # Per-case borderline analysis
    if case_id == "v05_gold_core_0045":
        # u2: "The shipping-logistics project requires manual dispatcher review..."
        # Currently project_memory. Opus flagged as possibly svc (single-service behavior)
        # Decision: KEEP project_memory. This is a cross-service operational policy
        # requiring manual review. It constrains the dispatcher workflow, which is a
        # project-level operational policy, not just route-optimizer behavior.
        lines.append("- **Opus flag:** Could be service_memory (single-service durable behavior)")
        lines.append("- **Decision: KEPT as project_memory.** The manual dispatcher review")
        lines.append("  threshold (60 min) is a project-level operational policy that")
        lines.append("  constrains the dispatcher workflow across all routing decisions.")
        lines.append("  It is not specific to the route-optimizer service alone.")
        lines.append("- **Confidence: Medium.** The boundary is genuinely ambiguous.")

    elif case_id == "v05_gold_core_0048":
        # u2: "The content-platform project requires human review for any automatically"
        # "generated captions with confidence below 90% to meet accessibility standards."
        # KEPT as project_memory (accessibility compliance is project-level policy)
        lines.append("- **Opus flag:** Could be service_memory (single-service quality gate)")
        lines.append("- **Decision: KEPT as project_memory.** This is a project-level")
        lines.append("  accessibility compliance policy (WCAG 2.1 AA). The 90% confidence")
        lines.append("  threshold is a project-wide quality requirement, not just a")
        lines.append("  media-processor configuration. Cross-service in scope.")
        lines.append("- **Confidence: Medium.** Accessibility compliance is inherently")
        lines.append("  project-level but the threshold feels service-specific.")

    elif case_id == "v05_gold_core_0062":
        # u2: "The health-monitor project requires alert fatigue reduction: suppressed"
        # "alerts must be aggregated into an hourly digest..."
        # Roll back to service_memory — this is alert-dispatcher specific behavior
        lines.append("- **Opus flag:** Could be service_memory (single-service digest behavior)")
        lines.append("- **Decision: CHANGED to service_memory.** The hourly digest aggregation")
        lines.append("  is a specific behavior of the alert-dispatcher service. While the")
        lines.append("  goal (alert fatigue reduction) is project-level, the implementation")
        lines.append("  mechanism (hourly digest of suppressed alerts) is service-specific.")
        lines.append("- **Confidence: High.** The 'The health-monitor project requires...'")
        lines.append("  prefix is not sufficient to make this project_memory.")
        lines.append("- **Changed:** project_memory -> service_memory")

        # Apply the change
        for s in gold["store"]:
            if s["unit_id"] == "u2":
                s["target"] = "service_memory"
                break
        update_dsl(case)
        case["notes"] = _rewrite_svc_rollback_note(case, "u2", unit_texts.get("u2", ""))

    elif case_id == "v05_gold_core_0069":
        # u2: "The shipping-logistics project requires that route optimization complete"
        # "within 30 seconds for up to 50 stops, returning a usable sub-optimal route on timeout."
        lines.append("- **Opus flag:** Could be service_memory (single-service SLA constraint)")
        lines.append("- **Decision: CHANGED to service_memory.** The 30-second timeout for")
        lines.append("  route optimization is a performance constraint on the route-optimizer")
        lines.append("  service specifically. The 'The shipping-logistics project requires...'")
        lines.append("  prefix does not make this project_memory per V05_LABEL_POLICY.")
        lines.append("- **Confidence: High.** This is a service-level performance SLA, not")
        lines.append("  a project-wide policy.")
        lines.append("- **Changed:** project_memory -> service_memory")

        for s in gold["store"]:
            if s["unit_id"] == "u2":
                s["target"] = "service_memory"
                break
        update_dsl(case)
        case["notes"] = _rewrite_svc_rollback_note(case, "u2", unit_texts.get("u2", ""))

    elif case_id == "v05_gold_core_0049":
        # u2: "Duplicate detection should run before the main reconciliation matching step"
        # "to prevent inflated match counts."
        # Currently task_state (from post-processing adjustment).
        # This describes an implementation ordering plan with "should run" → task_state is correct
        lines.append("- **Opus flag:** Could be service_memory (durable processing order)")
        lines.append("- **Decision: KEPT as task_state.** The phrasing 'should run before'")
        lines.append("  suggests a current implementation intention rather than a durable")
        lines.append("  specification. The unit describes WHERE in the pipeline duplicate")
        lines.append("  detection should be inserted — this is implementation-scoped.")
        lines.append("- **Confidence: Medium.** Could be argued either way, but 'should'")
        lines.append("  and the implementation-plan framing favor task_state.")

    return "\n".join(lines)


def _sync_notes(case: dict[str, Any]) -> str:
    """Ensure notes match final labels. Return updated notes string."""
    stores = case["gold"]["store"]
    store_targets = {s["unit_id"]: s["target"] for s in stores}
    unit_texts = {u["unit_id"]: u["text"] for u in case["current_units"]}

    # Build a clean summary based on final labels
    lines = []
    shape = ""
    has_read = bool(case["gold"].get("read"))
    has_store = bool(stores)
    if has_read and has_store:
        shape = "READ+STORE joint"
    elif has_read:
        shape = "READ-only"
    else:
        shape = "STORE/SKIP-only"
    lines.append(f"{shape}:")

    if has_read:
        lines.append(f"reads {','.join(case['gold']['read'])}.")

    for s in stores:
        uid = s["unit_id"]
        target = s["target"]
        text = unit_texts.get(uid, "")
        # Short descriptor
        if len(text) > 60:
            text_short = text[:57] + "..."
        else:
            text_short = text
        lines.append(f"u{uid} -> {target}: {text_short}")

    skips = case["gold"].get("skip", [])
    if skips:
        lines.append(f"SKIP: {','.join(skips)}")

    return " ".join(lines)


# ── Main ────────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 70)
    print("Applying Opus gold review fixes (Context 5.3-D)")
    print("=" * 70)

    # Load draft
    cases = load_cases(DRAFT_PATH)
    print(f"Loaded {len(cases)} cases from {DRAFT_PATH}")

    # Apply fixes
    fix_log = apply_fixes(cases)

    # Print fix summary
    print(f"\nGroup A (svc->proj rollback): {len(fix_log['group_a_svc_proj_rollback'])} changes")
    print(f"Group B (false user_profile): {len(fix_log['group_b_false_user_profile'])} changes")
    print(f"Group C (work email SKIP): {len(fix_log['group_c_work_email_skip'])} changes")
    print(f"Group D (phone collision): {len(fix_log['group_d_phone_collision'])} changes")
    print(f"Group E (replace easy hard): {len(fix_log['group_e_replace_easy_hard'])} changes")
    print(f"Borderline reviewed: {len(fix_log['borderline_reviewed'])} cases")
    print(f"Notes synchronized: {len(fix_log['notes_synchronized'])} cases")

    # ── Validate all corrected cases ────────────────────────────────────
    print("\nValidating corrected cases...")
    all_ok = True
    case_errors: dict[str, list[str]] = {}
    for case in cases:
        errs = validate_case_parsed(case)
        if errs:
            all_ok = False
            case_errors[case["case_id"]] = errs

    if case_errors:
        for cid, errs in case_errors.items():
            print(f"  FAIL: {cid}")
            for e in errs:
                print(f"    {e}")
    else:
        print("  All cases validated OK")

    # ── Distribution ────────────────────────────────────────────────────
    dist = distribution_summary(cases)
    print(f"\nDistribution after fixes:")
    print(f"  Total cases: {dist['total_cases']}")
    print(f"  gold_core: {dist['core_cases']}, gold_hard: {dist['hard_cases']}")
    for target, pct in dist["target_pcts"].items():
        print(f"  {target}: {dist['targets'][target]} ({pct}%)")
    print(f"  Total STORE units: {dist['total_store_units']}")
    print(f"  Cases with READ: {dist['cases_with_read']}")
    print(f"  Cases with STORE: {dist['cases_with_store']}")
    print(f"  Cases with SKIP: {dist['cases_with_skip']}")
    print(f"  READ decisions: {dist['read_decision_count']}")
    print(f"  STORE units: {dist['store_unit_count']}")
    print(f"  SKIP units: {dist['skip_unit_count']}")

    # ── Write corrected files ───────────────────────────────────────────
    # Combined
    write_cases(cases, CORRECTED_PATH)
    print(f"\nWrote {len(cases)} cases to {CORRECTED_PATH}")

    # Core and hard splits
    core_cases = [c for c in cases if "gold_core" in c["case_id"]]
    hard_cases = [c for c in cases if "gold_hard" in c["case_id"]]
    write_cases(core_cases, CORE_CORRECTED_PATH)
    write_cases(hard_cases, HARD_CORRECTED_PATH)
    print(f"Wrote {len(core_cases)} core cases to {CORE_CORRECTED_PATH}")
    print(f"Wrote {len(hard_cases)} hard cases to {HARD_CORRECTED_PATH}")

    # ── Build SFT messages ──────────────────────────────────────────────
    print("\nBuilding SFT messages...")
    sft_path = ROOT / "data/v05/gold/v05_gold_corrected_sft_messages.jsonl"

    # Import render_sft_messages function
    sys.path.insert(0, str(ROOT))
    from src.v05.render_sft_messages import build_sft_message, SYSTEM_PROMPT

    sft_messages = []
    for c in cases:
        msg = build_sft_message(c)
        msg["source"] = "v05_gold_corrected"
        # Override metadata for corrected gold
        is_core = "gold_core" in c["case_id"]
        msg["metadata"] = {
            "tags": c["tags"],
            "num_candidate_memories": len(c["candidate_memories"]),
            "num_current_units": len(c["current_units"]),
            "gold_shape": (
                "READ+STORE joint" if (c["gold"].get("read") and c["gold"].get("store"))
                else "READ-only" if c["gold"].get("read")
                else "STORE/SKIP-only"
            ),
            "store_targets": [s["target"] for s in c["gold"].get("store", [])],
            "split": "gold_corrected",
            "is_locked_gold": False,
            "is_final_train_data": False,
            "gold_partition": "gold_core" if is_core else "gold_hard",
        }
        sft_messages.append(msg)

    # Validate SFT
    sft_ok = True
    for c, m in zip(cases, sft_messages):
        assistant = m["messages"][2]["content"]
        if assistant != c["gold"]["dsl"]:
            print(f"  SFT ASSISTANT MISMATCH: {c['case_id']}")
            sft_ok = False
        if "```" in assistant:
            print(f"  SFT MARKDOWN: {c['case_id']}")
            sft_ok = False
        if assistant.strip().startswith("{"):
            print(f"  SFT JSON: {c['case_id']}")
            sft_ok = False

    with open(sft_path, "w", encoding="utf-8") as f:
        for msg in sft_messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(sft_messages)} SFT messages to {sft_path}")
    if sft_ok:
        print("  SFT validation: OK")
    else:
        print("  SFT validation: ERRORS")

    # ── Hashes ──────────────────────────────────────────────────────────
    print("\nComputing hashes...")
    for label, path in [
        ("combined", CORRECTED_PATH),
        ("core", CORE_CORRECTED_PATH),
        ("hard", HARD_CORRECTED_PATH),
    ]:
        h = sha256_hex(path)
        print(f"  {label}: {h}")

    # ── Final status ────────────────────────────────────────────────────
    if all_ok and sft_ok:
        print("\n✅ All validations passed. Corrected gold is ready for final review.")
    else:
        print("\n❌ Some validations failed. See errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Rebalance batch500 distribution by replacing service-heavy new200 cases.

Context 5.2-B: Replace ~50 service-heavy cases with balanced replacement cases
to reduce service_memory from 39.1% toward 30-34% and increase
project_memory and user_profile.

Strategy:
- Replace 25 cases with 2+ service_memory from new200
- Replace 25 more cases with 1+ service_memory from new200
- Replacement cases add project_memory, user_profile, repo_memory, task_state
- Don't touch repaired batch300
- Don't override original files
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ── Helper functions ────────────────────────────────────────────────────────

def m(mid: str, tgt: str, content: str) -> dict:
    return {"memory_id": mid, "target": tgt, "content": content}

def u(uid: str, text: str) -> dict:
    return {"unit_id": uid, "text": text}

def st(tgt: str, uid: str) -> dict:
    return {"target": tgt, "unit_id": uid}

def make_case(cid: str, rc: dict, cms: list, cus: list,
              read: list, store: list, skip: list,
              tags: list, notes: str) -> dict:
    dsl_lines = []
    dsl_lines.append(f"READ {','.join(read)}" if read else "READ NONE")
    for s in store:
        dsl_lines.append(f"STORE {s['target']} {s['unit_id']}")
    if not store:
        dsl_lines.append("STORE NONE")
    dsl_lines.append(f"SKIP {','.join(skip)}" if skip else "SKIP NONE")
    return {
        "case_id": cid,
        "runtime_context": rc,
        "candidate_memories": cms,
        "current_units": cus,
        "gold": {"read": read, "store": store, "skip": skip, "dsl": "\n".join(dsl_lines)},
        "tags": tags,
        "notes": notes,
    }

# ── SYSTEM PROMPT (for SFT) ────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a memory policy router for coding-agent contexts.\n\n"
    "Task:\n"
    "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
    "- which candidate memories to READ;\n"
    "- which current unit IDs to STORE and to which target;\n"
    "- which current unit IDs to SKIP.\n\n"
    "Output only the DSL. Do not include comments, prose, explanations, or JSON.\n\n"
    "Allowed DSL lines:\n"
    "READ <memory_id_list|NONE>\n"
    "STORE <target> <unit_id>\n"
    "STORE NONE\n"
    "SKIP <unit_id_list|NONE>\n\n"
    "Legal STORE targets:\n"
    "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
    "Rules:\n"
    "- READ useful memories only; skip merely related or stale ones.\n"
    "- STORE durable, reusable information with correct target.\n"
    "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
    "- Every current unit must appear exactly once in STORE or SKIP.\n"
    "- Do not invent IDs, targets, or content."
)

def render_user_input(case: dict) -> str:
    rc = case["runtime_context"]
    lines = [
        "RUNTIME_CONTEXT",
        f"project: {rc['project']}",
        f"repo: {rc['repo']}",
        f"service: {rc['service']}",
        f"task: {rc['task']}",
        "",
    ]
    mems = case["candidate_memories"]
    if mems:
        lines.append("CANDIDATE_MEMORIES")
        for mem in mems:
            lines.append(f"{mem['memory_id']} [{mem['target']}]: {mem['content']}")
    else:
        lines.append("CANDIDATE_MEMORIES\nNONE")
    lines.append("")
    lines.append("CURRENT_UNITS")
    for unit in case["current_units"]:
        lines.append(f"{unit['unit_id']}: {unit['text']}")
    return "\n".join(lines)

def build_sft_message(case: dict, source: str) -> dict:
    gold_store = case["gold"]["store"]
    has_read = bool(case["gold"]["read"])
    has_store = bool(gold_store)
    if has_read and has_store:
        shape = "READ + STORE joint"
    elif has_read:
        shape = "READ-only"
    elif has_store:
        shape = "STORE/SKIP-only"
    else:
        shape = "no READ and no STORE"
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": render_user_input(case)},
            {"role": "assistant", "content": case["gold"]["dsl"]},
        ],
        "case_id": case["case_id"],
        "source": source,
        "metadata": {
            "tags": case["tags"],
            "num_candidate_memories": len(case["candidate_memories"]),
            "num_current_units": len(case["current_units"]),
            "gold_shape": shape,
            "store_targets": [s["target"] for s in gold_store],
            "is_final_train_data": False,
        },
    }

# ═══════════════════════════════════════════════════════════════════════════════
# CASE IDs TO REPLACE: 50 service-heavy new200 cases
# ═══════════════════════════════════════════════════════════════════════════════

REPLACED_IDS = [
    # Priority 1: 2+ service_memory cases (25 cases, 54 svc units removed)
    "v05_batch500_0002", "v05_batch500_0015", "v05_batch500_0042", "v05_batch500_0069",
    "v05_batch500_0071", "v05_batch500_0092", "v05_batch500_0093",
    "v05_batch500_0098", "v05_batch500_0099", "v05_batch500_0100",
    "v05_batch500_0101", "v05_batch500_0102", "v05_batch500_0103", "v05_batch500_0104",
    "v05_batch500_0105", "v05_batch500_0118", "v05_batch500_0121",
    "v05_batch500_0122", "v05_batch500_0125", "v05_batch500_0126", "v05_batch500_0127",
    "v05_batch500_0131", "v05_batch500_0132", "v05_batch500_0197", "v05_batch500_0198",

    # Priority 2: 1+ svc cases replaceable with project/user/repo (25 more)
    "v05_batch500_0010", "v05_batch500_0011", "v05_batch500_0027",
    "v05_batch500_0033", "v05_batch500_0038", "v05_batch500_0044",
    "v05_batch500_0053", "v05_batch500_0057", "v05_batch500_0062",
    "v05_batch500_0065", "v05_batch500_0067",
    "v05_batch500_0074", "v05_batch500_0078",
    "v05_batch500_0088", "v05_batch500_0091",
    "v05_batch500_0106", "v05_batch500_0112", "v05_batch500_0119",
    "v05_batch500_0123", "v05_batch500_0129",
    "v05_batch500_0135", "v05_batch500_0145",
    "v05_batch500_0192", "v05_batch500_0193", "v05_batch500_0194",
]

# ═══════════════════════════════════════════════════════════════════════════════
# 50 REPLACEMENT CASES
# Each case uses the SAME case_id as the one it replaces.
# ═══════════════════════════════════════════════════════════════════════════════

REPLACEMENTS: list[dict] = []

# -- Group A: project_memory-focused replacements (15 cases) --

REPLACEMENTS.append(make_case("v05_batch500_0002",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"governance","task":"define cross-service data retention policy"},
    cms=[m("m1","project_memory","The metricboard project requires that all user-uploaded data be retained for 90 days after account deletion for audit purposes."),
         m("m2","repo_memory","Data retention configurations are in config/retention/policies.yaml with per-dataset overrides.")],
    cus=[u("u1","All metricboard services must retain query history logs for a minimum of 90 days before archival to cold storage."),
         u("u2","The retention policy applies uniformly to the query engine, alert manager, and report scheduler services."),
         u("u3","For this quarter, add the cold storage archival job to the data pipeline so logs older than 90 days are compressed and moved.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service retention rule -> project_memory. u2 explicitly names multiple services -> project_memory. u3 is current quarter task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0015",
    rc={"project":"travel-planner","repo":"voyager","service":"policy","task":"define project-wide accessibility policy"},
    cms=[m("m1","project_memory","The voyager project committed to WCAG 2.1 AA compliance for all customer-facing interfaces by Q3 2026."),
         m("m2","repo_memory","Accessibility test suites are under tests/a11y/ and run as part of the CI pipeline.")],
    cus=[u("u1","All voyager customer-facing services including booking, pricing, and check-in must support screen readers with proper ARIA labels on all interactive elements."),
         u("u2","The voyager project does not support real-time currency conversion for display prices; all prices are shown in the base currency of the booking."),
         u("u3","Schedule accessibility audits for the booking and check-in flows before the Q3 compliance deadline.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service accessibility rule -> project_memory. u2 is project scope exclusion -> project_memory. u3 is scheduling task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0042",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"compliance","task":"define cross-service data handling policy"},
    cms=[m("m1","project_memory","The shopengine project requires GDPR-compliant data handling with right-to-erasure support within 30 days of request."),
         m("m2","service_memory","The order service retains completed order data for 2 years before anonymization.")],
    cus=[u("u1","All shopengine services that store customer PII must implement a deletion endpoint that removes or anonymizes all customer records within 30 days of a verified erasure request."),
         u("u2","The shopengine project must never share customer email addresses with third-party marketing services without explicit opt-in consent."),
         u("u3","Add GDPR erasure request tracking to the admin dashboard so the compliance team can monitor pending requests.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service GDPR requirement -> project_memory. u2 is project-level privacy policy -> project_memory. u3 is dashboard task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0069",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"security","task":"define cross-service authentication standards"},
    cms=[m("m1","project_memory","The shopengine project requires all services to use OAuth 2.0 with OpenID Connect for user authentication."),
         m("m2","repo_memory","OAuth client configurations are stored in config/auth/clients.yaml with per-service client IDs and scopes.")],
    cus=[u("u1","All shopengine services must validate JWT tokens against the central auth service on every request, with a token cache TTL of 60 seconds."),
         u("u2","The shopengine project categorically prohibits storing user passwords in any service database; only the auth service manages credentials."),
         u("u3","Migrate the legacy catalog service from session-based auth to JWT-based auth before the security audit next month.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service auth rule -> project_memory. u2 is project-wide security prohibition -> project_memory. u3 is migration task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0071",
    rc={"project":"customer-support","repo":"helpdesk","service":"privacy","task":"define cross-service PII handling policy"},
    cms=[],
    cus=[u("u1","All helpdesk services must mask customer PII in log output: names truncated to first initial, email local parts truncated to first 2 characters, and phone numbers fully redacted."),
         u("u2","The helpdesk project does not store customer payment information; all payment processing is handled by the external billing system."),
         u("u3","Add PII masking to the ticket search index logs before the next compliance audit.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","task_progress","target_boundary","sensitive_boundary"],
    notes="u1 is cross-service PII masking rule -> project_memory. u2 is project scope limitation -> project_memory. u3 is implementation task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0092",
    rc={"project":"finance-dashboard","repo":"finboard","service":"governance","task":"define project-wide access control rules"},
    cms=[],
    cus=[u("u1","All finboard services must enforce role-based access control with three roles: viewer, analyst, and admin, where admin access requires MFA."),
         u("u2","The finboard project requires that all access grants be reviewed quarterly by the compliance team, with inactive accounts disabled after 90 days."),
         u("u3","Role definitions and permission mappings are stored in config/auth/roles.yaml and must be reviewed before each production deployment.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service RBAC rule -> project_memory. u2 is project-wide access review policy -> project_memory. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0093",
    rc={"project":"healthcare-admin","repo":"medflow","service":"compliance","task":"define HIPAA compliance policy for all services"},
    cms=[],
    cus=[u("u1","All medflow services that handle PHI must encrypt data at rest using AES-256 and in transit using TLS 1.3, with key rotation every 90 days."),
         u("u2","The medflow project must never transmit PHI over unencrypted channels; all internal service-to-service communication must use mTLS."),
         u("u3","The PHI access audit log is stored in the audit_db database defined in config/databases/audit_db.yaml.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service encryption rule -> project_memory. u2 is project-wide PHI transmission prohibition -> project_memory. u3 is DB config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0098",
    rc={"project":"mobile-field","repo":"field-app","service":"policy","task":"define cross-service data usage policy"},
    cms=[],
    cus=[u("u1","All field-app services must minimize cellular data usage by batching network requests and compressing payloads with gzip when the device is on a metered connection."),
         u("u2","The field-app project does not collect background location data when the app is not in active use; location sampling stops within 3 minutes of the app entering the background."),
         u("u3","The data usage limits per service are configured in config/network/data_limits.yaml and enforced by the network manager.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service data minimization rule -> project_memory. u2 is project-wide privacy policy -> project_memory. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0099",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"policy","task":"define cross-service pricing transparency policy"},
    cms=[],
    cus=[u("u1","All shopengine customer-facing services must display the total price including all mandatory taxes and fees before the customer reaches the checkout confirmation page."),
         u("u2","The shopengine project prohibits dynamic pricing based on individual user browsing history; all price variations must be based on publicly available factors such as quantity, coupon code, or loyalty tier."),
         u("u3","The pricing display rules are enforced by the shared pricing library at lib/pricing/display.py used by all frontend services.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service pricing display rule -> project_memory. u2 is project-wide ethical pricing policy -> project_memory. u3 is shared library path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0100",
    rc={"project":"travel-planner","repo":"voyager","service":"policy","task":"define cross-service cancellation policy"},
    cms=[],
    cus=[u("u1","All voyager booking services must apply the same cancellation fee schedule: free cancellation within 24 hours of booking, 10% fee within 7 days of departure, 50% fee within 48 hours, and no refund after departure."),
         u("u2","The voyager project requires that all cancellation confirmation emails be sent within 5 minutes of processing and include the refund amount and expected timeline."),
         u("u3","The cancellation fee schedule is defined in config/policies/cancellation_fees.yaml and loaded by all booking services at startup.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service cancellation rule -> project_memory. u2 is project-wide communication standard -> project_memory. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0198",
    rc={"project":"supply-chain","repo":"logistix","service":"compliance","task":"define cross-service sustainability reporting requirements"},
    cms=[],
    cus=[u("u1","All logistix services must report carbon emissions data per shipment: the route optimizer reports estimated CO2, the delivery tracker reports actual fuel consumption, and the returns processor reports reverse-logistics emissions."),
         u("u2","The logistix project has committed to net-zero operations by 2030; all service-level decisions that affect emissions must be documented with a sustainability impact statement."),
         u("u3","The sustainability metrics dashboard is configured in grafana/dashboards/sustainability.json and updated monthly.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 is cross-service reporting rule naming specific services -> project_memory. u2 is project-level sustainability commitment -> project_memory. u3 is dashboard path -> repo_memory."))

# -- Group B: user_profile-focused replacements (8 cases) --

REPLACEMENTS.append(make_case("v05_batch500_0010",
    rc={"project":"finance-dashboard","repo":"finboard","service":"user-settings","task":"record user display preferences"},
    cms=[m("m1","repo_memory","User preferences for the finboard dashboard are stored in the user_settings table with per-widget overrides."),
         m("m2","service_memory","The alert service sends notifications based on user-configured thresholds and channels.")],
    cus=[u("u1","I prefer all financial charts to display currency values in my local currency (EUR) with the exchange rate source noted in the chart footer."),
         u("u2","I want to receive portfolio summary emails weekly on Friday at 08:00 CET instead of daily."),
         u("u3","My corporate email for finboard notifications is trader-007@investco.example.com.")],
    read=["m1"], store=[st("user_profile","u1"),st("user_profile","u2")], skip=["u3"],
    tags=["read_store_joint","user_profile_boundary","sensitive_boundary","related_but_useless"],
    notes="u1 is currency preference -> user_profile. u2 is notification schedule preference -> user_profile. u3 is personal email -> SKIP."))

REPLACEMENTS.append(make_case("v05_batch500_0011",
    rc={"project":"customer-support","repo":"helpdesk","service":"agent-preferences","task":"record agent workflow preferences"},
    cms=[m("m1","service_memory","The helpdesk ticket system supports configurable agent views with saved filters and column layouts."),
         m("m2","task_state","The current agent view customization is limited to column visibility only; full layout customization is planned.")],
    cus=[u("u1","I prefer to see tickets sorted by priority first, then by wait time, with high-priority tickets highlighted in red regardless of other sort criteria."),
         u("u2","When I ask for a code review, prioritize API contract violations and missing error handling over style nits."),
         u("u3","My agent ID is AG-4429 and my shift is 14:00-22:00 UTC; update my schedule accordingly.")],
    read=["m1"], store=[st("user_profile","u1"),st("user_profile","u2")], skip=["u3"],
    tags=["read_store_joint","user_profile_boundary","stale_memory"],
    notes="u1 is stable sort preference -> user_profile. u2 is stable code review preference -> user_profile. u3 is a schedule update request -> SKIP."))

REPLACEMENTS.append(make_case("v05_batch500_0074",
    rc={"project":"supply-chain","repo":"logistix","service":"user-settings","task":"record supply chain analyst preferences"},
    cms=[],
    cus=[u("u1","I prefer inventory reports grouped by warehouse first, then by product category, with low-stock items always listed at the top regardless of grouping."),
         u("u2","When presenting supplier performance metrics, include the 3-month trend alongside the current value rather than just the current snapshot."),
         u("u3","My work hours are 06:00-14:00 UTC; schedule all automated report deliveries within this window.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("user_profile","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary"],
    notes="u1 is stable report preference -> user_profile. u2 is stable metric display preference -> user_profile. u3 is scheduling preference -> user_profile."))

REPLACEMENTS.append(make_case("v05_batch500_0101",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"editor-settings","task":"record level designer preferences"},
    cms=[],
    cus=[u("u1","I prefer the level editor to use a dark theme with the 'Dungeon' color palette and grid snapping set to 0.5 units by default."),
         u("u2","When I test-play a level, automatically enable the debug overlay showing collision volumes, AI paths, and trigger zones."),
         u("u3","The editor auto-save interval is configured in config/editor/preferences.json with a default of 5 minutes.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary","repo_convention","repo_vs_service"],
    notes="u1 is editor preference -> user_profile. u2 is debug preference -> user_profile. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0106",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"user-preferences","task":"record workflow designer preferences"},
    cms=[],
    cus=[u("u1","I prefer workflow diagrams to use BPMN 2.0 notation with swimlanes colored by department rather than by system."),
         u("u2","When I export workflow documentation, include the step descriptions, input/output schemas, and error handling paths in a single PDF."),
         u("u3","The workflow export templates are stored in config/exports/templates/ and can be customized per department.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary","repo_convention"],
    notes="u1 is stable notation preference -> user_profile. u2 is stable export preference -> user_profile. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0118",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"user-settings","task":"record analyst query preferences"},
    cms=[],
    cus=[u("u1","I prefer query results to default to a table view with 50 rows per page and columns in the order they appear in the SELECT clause."),
         u("u2","When I save a query, automatically tag it with the current project context and date so I can find it later by project."),
         u("u3","My saved queries and chart configurations are stored under my user profile in config/users/analyst_42/preferences.yaml.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary","repo_convention"],
    notes="u1 is stable query display preference -> user_profile. u2 is stable save behavior preference -> user_profile. u3 is config path -> repo_memory."))

REPLACEMENTS.append(make_case("v05_batch500_0121",
    rc={"project":"travel-planner","repo":"voyager","service":"user-preferences","task":"record traveler search preferences"},
    cms=[],
    cus=[u("u1","I prefer flight search results sorted by total travel time rather than price when the price difference between options is less than 15%."),
         u("u2","When I search for hotels, prioritize properties with a guest rating of 4.0 or above and filter out properties without free WiFi."),
         u("u3","My loyalty program numbers are stored in my account profile; the voyager system should automatically apply them to all bookings.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("user_profile","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary"],
    notes="u1 is stable flight search preference -> user_profile. u2 is stable hotel filter preference -> user_profile. u3 is stable loyalty preference -> user_profile."))

REPLACEMENTS.append(make_case("v05_batch500_0122",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"qa-settings","task":"record QA tester preferences"},
    cms=[],
    cus=[u("u1","I prefer bug reports to include the game build version, the exact steps to reproduce, and a screenshot automatically attached when I press F12."),
         u("u2","When I mark a bug as 'cannot reproduce', prompt me to record a 30-second video clip of my attempt before closing the ticket."),
         u("u3","The bug report templates are configured in config/qa/bug_report_template.yaml.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","user_profile_boundary","repo_convention"],
    notes="u1 is stable bug report preference -> user_profile. u2 is stable workflow preference -> user_profile. u3 is config path -> repo_memory."))

# -- Group C: repo_memory + task_state replacements (12 cases) --

REPLACEMENTS.append(make_case("v05_batch500_0027",
    rc={"project":"finance-dashboard","repo":"finboard","service":"devops","task":"set up staging environment configuration"},
    cms=[m("m1","repo_memory","The finboard project uses Kubernetes for deployment with environment-specific overlays in k8s/overlays/<env>/."),
         m("m2","task_state","The staging environment currently runs on a single-node cluster; scaling to 3 nodes is planned for load testing.")],
    cus=[u("u1","All finboard services in staging must use the staging database cluster at db-stage.finboard.internal and the staging Redis at redis-stage.finboard.internal."),
         u("u2","The staging environment configuration is managed in k8s/overlays/staging/configmap.yaml and applied via kubectl apply -k k8s/overlays/staging."),
         u("u3","Add resource limits to the staging deployment: 512Mi memory and 0.5 CPU per pod, with burst to 1Gi and 1 CPU.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is repo DB/Redis config -> repo_memory. u2 is k8s config path and command -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0033",
    rc={"project":"finance-dashboard","repo":"finboard","service":"ci","task":"configure CI pipeline for pull request validation"},
    cms=[m("m1","repo_memory","CI workflows are defined in .github/workflows/ and trigger on pull_request events against the main branch."),
         m("m2","project_memory","The finboard project requires that all PRs pass linting, unit tests, and integration tests before merging.")],
    cus=[u("u1","The CI pipeline must run Python linting with flake8 using the config at .flake8, unit tests with pytest tests/unit/, and integration tests with pytest tests/integration/."),
         u("u2","Test coverage reports are written to ci_reports/coverage/ and must show at least 80% line coverage for new code."),
         u("u3","Add a CI step that validates all YAML configuration files against their JSON schemas before the test stages run.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress","project_vs_repo","target_boundary"],
    notes="u1 is CI commands/paths -> repo_memory. u2 is report path and coverage threshold -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0038",
    rc={"project":"healthcare-admin","repo":"medflow","service":"deployment","task":"plan production database migration"},
    cms=[m("m1","repo_memory","Database migrations for medflow are managed with Alembic and stored in db/migrations/ with timestamp-prefixed filenames."),
         m("m2","task_state","The current production database is PostgreSQL 14; migration to PostgreSQL 16 is planned for the next maintenance window.")],
    cus=[u("u1","Database migrations must be applied in order using: alembic upgrade head, and must be run against a staging clone before production."),
         u("u2","The migration history table is alembic_version and must never be manually modified; all schema changes go through migration files."),
         u("u3","Write the PostgreSQL 16 migration plan including the pg_upgrade checklist and rollback procedure.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is migration command -> repo_memory. u2 is DB convention rule -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0044",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"release","task":"plan release process improvements"},
    cms=[m("m1","repo_memory","Release artifacts are built by the CI pipeline and stored in the releases/ directory with version-tagged filenames."),
         m("m2","task_state","The current release process is manual and takes about 2 hours; automating the changelog generation and smoke test steps is planned.")],
    cus=[u("u1","Every release must include a CHANGELOG.md entry under the new version heading, listing all merged PRs since the last release grouped by feature, fix, and chore."),
         u("u2","Release candidates must pass the full integration test suite at tests/integration/ before being promoted to the release tag."),
         u("u3","Automate the changelog generation using the script at scripts/generate_changelog.py that reads merged PRs from the GitHub API.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress"],
    notes="u1 is changelog convention -> repo_memory. u2 is test path requirement -> repo_memory. u3 is automation task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0053",
    rc={"project":"customer-support","repo":"helpdesk","service":"infra","task":"set up monitoring and alerting for all services"},
    cms=[m("m1","repo_memory","Prometheus metrics are exposed on port 9090 at /metrics and alerting rules are in prometheus/rules/alerts.yml."),
         m("m2","project_memory","The helpdesk project SLA requires 99.5% uptime for the ticket API and 99.9% for the agent dashboard.")],
    cus=[u("u1","All helpdesk services must expose Prometheus metrics at :9090/metrics with the standard histogram buckets for request latency: 0.01, 0.05, 0.1, 0.5, 1, 5 seconds."),
         u("u2","Alert rules for production are defined in prometheus/rules/alerts.yml: page on-call if the ticket API error rate exceeds 1% for 5 minutes or if p95 latency exceeds 2 seconds."),
         u("u3","Add the alerting rules for the new chat-router service before it goes live in production next week.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress","project_vs_repo","target_boundary"],
    notes="u1 is monitoring convention -> repo_memory. u2 is alert rule definition -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0057",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"testing","task":"improve test infrastructure"},
    cms=[m("m1","repo_memory","Unit tests live under tests/unit/ and run with pytest, integration tests under tests/integration/ require Docker Compose."),
         m("m2","task_state","The current test suite takes 25 minutes to run; parallelizing integration tests across 4 workers is planned.")],
    cus=[u("u1","All new service code must have unit tests covering at least 85% of branches, verified by the coverage check in the CI pipeline using pytest-cov."),
         u("u2","Integration tests must use the test fixtures defined in tests/integration/conftest.py and clean up all created resources in the teardown phase."),
         u("u3","Add the test parallelization configuration to pytest.ini with 4 workers and the test group assignments for the integration suite.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress"],
    notes="u1 is test coverage convention -> repo_memory. u2 is test fixture convention -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0062",
    rc={"project":"learning-assistant","repo":"tutorai","service":"config","task":"define configuration management conventions"},
    cms=[m("m1","repo_memory","All tutorai services load configuration from YAML files under config/<service>/ with environment variable overrides for secrets."),
         m("m2","user_profile","The user prefers course materials in video format with subtitles enabled by default for all content.")],
    cus=[u("u1","Configuration files must be validated against their JSON schemas at service startup, with schemas stored in config/schemas/<service>_config_schema.json."),
         u("u2","Secrets such as database passwords and API keys must never appear in config files; they must be loaded from environment variables or the secrets manager."),
         u("u3","I prefer learning materials organized by topic with clear prerequisites listed at the start of each section.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("user_profile","u3")], skip=[],
    tags=["read_store_joint","repo_convention","user_profile_boundary","repo_vs_service"],
    notes="u1 is config validation convention -> repo_memory. u2 is secrets handling convention -> repo_memory. u3 is learning preference -> user_profile."))

REPLACEMENTS.append(make_case("v05_batch500_0065",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"build","task":"set up reproducible build process"},
    cms=[m("m1","repo_memory","The project uses pip-tools to pin dependencies in requirements.txt and requirements-dev.txt."),
         m("m2","task_state","The current dependency pins are 3 months old; updating to latest compatible versions is needed for the v0.5 training environment.")],
    cus=[u("u1","The Python virtual environment must be created at .venv/ and activated before running any project scripts; the environment is excluded from git via .gitignore."),
         u("u2","Dependencies are installed with: pip install -r requirements.txt for production and pip install -r requirements-dev.txt for development tools."),
         u("u3","Update all dependency pins and test the training pipeline with the updated dependencies before the v0.5 training run.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress"],
    notes="u1 is venv convention -> repo_memory. u2 is pip install command -> repo_memory. u3 is current update task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0067",
    rc={"project":"finance-dashboard","repo":"finboard","service":"security","task":"define code signing and artifact verification"},
    cms=[m("m1","repo_memory","Docker images are built from Dockerfile in each service directory and pushed to the project container registry."),
         m("m2","project_memory","The finboard project requires all production container images to be signed with Cosign and verified before deployment.")],
    cus=[u("u1","All Docker images built for production must be signed using: cosign sign --key cosign.key <image_tag>, with the signing key stored in the CI secrets."),
         u("u2","The image verification step in the deployment pipeline must run: cosign verify --key cosign.pub <image_tag> before applying the Kubernetes manifests."),
         u("u3","Add the Cosign signing and verification steps to the CI/CD pipeline configuration in .github/workflows/deploy.yml.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress","project_vs_repo","target_boundary"],
    notes="u1 is signing command -> repo_memory. u2 is verification command -> repo_memory. u3 is current CI task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0078",
    rc={"project":"data-platform","repo":"data-jobs","service":"infra","task":"migrate to infrastructure-as-code"},
    cms=[],
    cus=[u("u1","All data-platform infrastructure must be defined in Terraform under terraform/<env>/ with separate state files for networking, compute, and storage."),
         u("u2","The Terraform plan for each environment must be reviewed in the PR that modifies it; no direct terraform apply without PR approval."),
         u("u3","The current staging environment still has manually created resources from the initial setup; these must be imported into Terraform state before further changes.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is IaC path convention -> repo_memory. u2 is review convention -> repo_memory. u3 is current state and task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0088",
    rc={"project":"supply-chain","repo":"logistix","service":"reliability","task":"define disaster recovery runbook"},
    cms=[],
    cus=[u("u1","The disaster recovery runbook is stored at docs/operations/dr_runbook.md and must be updated whenever a new service is added to production."),
         u("u2","All logistix services must have their database backups stored in the backup bucket at s3://logistix-backups/<service>/ with daily snapshots retained for 30 days."),
         u("u3","Run a disaster recovery drill for the inventory-sync service before the peak holiday season to verify the recovery time objective of 4 hours.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is runbook path -> repo_memory. u2 is backup path convention -> repo_memory. u3 is current drill task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0091",
    rc={"project":"customer-support","repo":"helpdesk","service":"security","task":"define incident response procedures"},
    cms=[],
    cus=[u("u1","Security incidents must be reported within 15 minutes of detection by posting in the #security-incidents Slack channel and creating a ticket with the 'security_incident' label."),
         u("u2","The incident response playbook is at docs/security/incident_response.md and defines roles: incident commander, communications lead, and technical lead."),
         u("u3","Review and update the incident response playbook to include procedures for the new chat-router service before it launches.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is incident reporting convention -> repo_memory. u2 is playbook path -> repo_memory. u3 is current review task -> task_state."))

# -- Group D: balanced mixed-target replacements (15 cases) --

REPLACEMENTS.append(make_case("v05_batch500_0102",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"onboarding","task":"plan new developer onboarding improvements"},
    cms=[m("m1","repo_memory","The developer onboarding guide is at docs/contributing/onboarding.md and includes setup steps for local development."),
         m("m2","task_state","The current onboarding process takes new developers about 3 days to get a working local environment; reducing this to 1 day is a Q3 goal.")],
    cus=[u("u1","The project README.md must include a quickstart section with the exact commands to clone, install dependencies, and run the test suite in under 5 commands."),
         u("u2","All development environment setup must use Docker Compose defined in docker-compose.dev.yaml, with hot-reload enabled for all services."),
         u("u3","Add a setup validation script at scripts/verify_dev_setup.sh that checks all prerequisites and runs a smoke test to confirm the environment is functional.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress"],
    notes="u1 is README convention -> repo_memory. u2 is Docker setup convention -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0103",
    rc={"project":"education-platform","repo":"learnhub","service":"academic-integrity","task":"define academic integrity policies"},
    cms=[m("m1","project_memory","The learnhub project enforces an academic integrity policy that requires all submitted work to be the student's own, with plagiarism detection on all written assignments."),
         m("m2","service_memory","The plagiarism checker uses n-gram fingerprinting with a similarity threshold of 0.6 to flag potential violations.")],
    cus=[u("u1","The learnhub project must require students to acknowledge the academic integrity policy before each exam attempt, with a digital signature timestamp."),
         u("u2","All written assignment submissions must be automatically screened by the plagiarism checker, and submissions flagged with similarity above 0.8 must be held for instructor review."),
         u("u3","Add the academic integrity acknowledgement checkbox to the exam start flow before the end of the current semester.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is project-level integrity policy -> project_memory. u2 is project-level screening rule -> project_memory (applies to all assignments, not just one service). u3 is current implementation -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0104",
    rc={"project":"customer-support","repo":"helpdesk","service":"quality","task":"define quality assurance standards"},
    cms=[m("m1","project_memory","The helpdesk project quality program requires that 10% of all resolved tickets be reviewed monthly by a QA specialist for accuracy and empathy."),
         m("m2","repo_memory","QA review rubrics and scoring criteria are defined in docs/quality/qa_review_rubric.md.")],
    cus=[u("u1","All helpdesk agents must have at least 5% of their resolved tickets reviewed each month; agents with satisfaction scores below 3.5 must have 20% reviewed."),
         u("u2","The helpdesk project quality standard requires that all customer-facing responses include a greeting, a clear answer, and a closing with the agent's name."),
         u("u3","Add the QA review assignment automation that distributes tickets to QA specialists based on agent and ticket category.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is project-wide QA review rate -> project_memory. u2 is project-wide response quality standard -> project_memory. u3 is current automation task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0105",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"compliance","task":"plan SOC 2 compliance preparation"},
    cms=[m("m1","project_memory","The metricboard project is preparing for SOC 2 Type II certification with audit scope covering the query engine, report scheduler, and data export services."),
         m("m2","repo_memory","Compliance evidence including access logs and change management records are stored in the compliance/ directory.")],
    cus=[u("u1","All metricboard services in the SOC 2 scope must log every administrative action with the user ID, action, resource, timestamp, and client IP for audit trail purposes."),
         u("u2","The metricboard project requires that all production changes go through a change management process: PR review, staging deployment verification, and documented rollback plan."),
         u("u3","Complete the SOC 2 readiness assessment checklist and address any gaps before the external auditor engagement begins.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service audit logging -> project_memory. u2 is project-wide change management policy -> project_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0112",
    rc={"project":"mobile-field","repo":"field-app","service":"release","task":"define app store submission conventions"},
    cms=[m("m1","repo_memory","App store metadata and screenshots are stored in fastlane/metadata/ and uploaded via fastlane deliver."),
         m("m2","task_state","The current app store submission takes 3 manual hours; automating screenshot generation and metadata upload is in progress.")],
    cus=[u("u1","Release builds must be uploaded to TestFlight for beta testing at least 1 week before App Store submission, with the build number matching the format YYYY.MM.DD.BuildNum."),
         u("u2","The App Store listing metadata including description, keywords, and privacy policy URL must be reviewed by the marketing team before each submission."),
         u("u3","Add automated screenshot generation using fastlane snapshot with the UI test suite at fastlane/screenshots/.")],
    read=["m1","m2"], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","repo_convention","task_progress"],
    notes="u1 is build submission convention -> repo_memory. u2 is review convention -> repo_memory. u3 is current automation task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0119",
    rc={"project":"customer-support","repo":"helpdesk","service":"on-call","task":"define on-call rotation and escalation procedures"},
    cms=[],
    cus=[u("u1","The on-call rotation schedule is managed in PagerDuty with the schedule defined in config/oncall/rotation.yaml; each engineer serves a 1-week primary shift."),
         u("u2","Production incidents must be acknowledged within 5 minutes of the first page; if unacknowledged, escalate to the secondary on-call, then the engineering manager."),
         u("u3","Update the escalation policy to include the new chat-router service as a monitored component with the same 5-minute acknowledgement SLA.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","repo_convention","task_progress"],
    notes="u1 is on-call config path -> repo_memory. u2 is escalation procedure convention -> repo_memory. u3 is current update task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0123",
    rc={"project":"education-platform","repo":"learnhub","service":"accessibility","task":"plan accessibility compliance for course content"},
    cms=[],
    cus=[u("u1","All course content uploaded to learnhub must meet WCAG 2.1 AA standards: videos must have captions, images must have alt text, and documents must be screen-reader compatible."),
         u("u2","The learnhub project provides an accessibility checker tool at tools/a11y_checker/ that instructors can run on their course content before publishing."),
         u("u3","Run the accessibility checker on all courses for the upcoming fall semester and generate a compliance report for the academic affairs committee.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-wide accessibility requirement -> project_memory. u2 is tool path -> repo_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0125",
    rc={"project":"supply-chain","repo":"logistix","service":"integration","task":"document third-party API integration conventions"},
    cms=[],
    cus=[u("u1","All third-party API integrations must implement a circuit breaker pattern with 5 consecutive failures triggering an open state for 60 seconds before attempting a half-open probe."),
         u("u2","API client code for third-party integrations lives under src/integrations/<provider>/ and must implement the IntegrationClient interface defined in lib/integrations/base.py."),
         u("u3","Add the circuit breaker to the supplier inventory API integration which currently has no failure handling and causes 5-minute timeouts in the ordering pipeline.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines durable circuit breaker behavior -> service_memory. u2 defines repo path convention -> repo_memory. u3 is current fix task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0126",
    rc={"project":"data-platform","repo":"data-jobs","service":"governance","task":"plan data catalog governance rollout"},
    cms=[],
    cus=[u("u1","All datasets in the data-platform must be registered in the data catalog with owner, update frequency, retention period, and PII classification before they can be queried by any service."),
         u("u2","The data catalog API is documented at docs/api/catalog_api.md and dataset registration is done via POST /api/catalog/datasets with the dataset metadata JSON body."),
         u("u3","The billing_facts and customer_contacts datasets are still not registered in the catalog; register them before the governance audit next month.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-wide data governance rule -> project_memory. u2 is API docs path -> repo_memory. u3 is current registration task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0127",
    rc={"project":"mobile-field","repo":"field-app","service":"performance","task":"plan app performance optimization"},
    cms=[],
    cus=[u("u1","All field-app services must log performance metrics to the performance_metrics table including operation name, duration_ms, memory_kb, and timestamp, sampled at 1% of requests."),
         u("u2","The performance regression test suite is at tests/performance/ and must be run before every release; any operation that regresses by more than 20% must block the release."),
         u("u3","Profile the sync module's SQLite queries which are showing p99 latency of 800ms on low-end devices and identify optimization opportunities.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is cross-service performance logging rule -> project_memory. u2 is test path and release gate -> repo_memory. u3 is current profiling task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0131",
    rc={"project":"healthcare-admin","repo":"medflow","service":"training","task":"plan staff training on new EHR features"},
    cms=[],
    cus=[u("u1","All clinical staff must complete the annual HIPAA refresher training before they can access patient records for the new calendar year; access is automatically suspended for non-compliant accounts."),
         u("u2","Training materials for new medflow features are stored under docs/training/ with separate modules for providers, nurses, and administrative staff."),
         u("u3","Update the HIPAA training module to include the new telehealth consent requirements before the Q3 training deadline.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-wide training compliance rule -> project_memory. u2 is docs path -> repo_memory. u3 is current update task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0132",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"experiment","task":"plan v0.5 evaluation methodology"},
    cms=[],
    cus=[u("u1","The v0.5 evaluation must compare the trained LoRA router against the Qwen3-4B few-shot baseline and the DeepSeek teacher baseline on the same gold set."),
         u("u2","Evaluation results must report per-target accuracy, per-tag F1, and confusion matrices for each target pair, with the report template at docs/v05/eval_report_template.md."),
         u("u3","Run the baseline evaluation on the gold set before starting LoRA training to establish the comparison reference point.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-level evaluation methodology -> project_memory. u2 is report template path -> repo_memory. u3 is current baseline eval task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0197",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"documentation","task":"document API versioning conventions"},
    cms=[],
    cus=[u("u1","All flowcraft REST APIs must include a version prefix in the URL path: /api/v1/ for current, with deprecated versions supported for 6 months after a new version is released."),
         u("u2","API version changelogs must be maintained in docs/api/CHANGELOG.md with breaking changes highlighted and migration guides linked."),
         u("u3","The workflow execution API is currently at /api/v0/ and needs to be upgraded to /api/v1/ with the new pagination and filtering parameters.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-wide API versioning policy -> project_memory. u2 is docs path convention -> repo_memory. u3 is current upgrade task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0192",
    rc={"project":"learning-assistant","repo":"tutorai","service":"ethics","task":"define AI ethics guidelines for content generation"},
    cms=[m("m1","project_memory","The tutorai project requires that all AI-generated content be reviewed for bias before being shown to learners."),
         m("m2","service_memory","The content generator uses a bias detection filter that flags content with detected gender, racial, or socioeconomic bias signals.")],
    cus=[u("u1","The tutorai project must ensure that all AI-generated explanations are factually accurate, cite sources when presenting claimed facts, and clearly label AI-generated content as such."),
         u("u2","AI-generated quiz questions must be reviewed by a subject matter expert before being added to the question pool for graded assessments."),
         u("u3","Add the AI content label to all generated explanations and the source citation footer before the public beta launch.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is project-wide AI ethics policy -> project_memory. u2 is project-wide review requirement -> project_memory. u3 is current implementation -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0193",
    rc={"project":"customer-support","repo":"helpdesk","service":"data-protection","task":"plan customer data export and deletion workflows"},
    cms=[m("m1","project_memory","The helpdesk project must support customer data export requests within 72 hours and deletion requests within 30 days per privacy regulations."),
         m("m2","repo_memory","Data export and deletion procedures are documented in docs/privacy/data_requests.md with step-by-step instructions for the support team.")],
    cus=[u("u1","All helpdesk services that store customer data must implement an export endpoint that returns all customer data in a machine-readable JSON format within 72 hours of a verified request."),
         u("u2","The helpdesk project requires that customer data deletion be irreversible after the 30-day grace period; deleted data must not be recoverable from backups after the retention window."),
         u("u3","Add the data export endpoint to the ticket service and the chat history service before the privacy regulation deadline.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service data export requirement -> project_memory. u2 is project-wide deletion policy -> project_memory. u3 is current implementation task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0194",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"governance","task":"plan data classification and labeling rollout"},
    cms=[m("m1","project_memory","The metricboard project classifies all data into four sensitivity levels: public, internal, confidential, and restricted, with different handling rules per level."),
         m("m2","repo_memory","Data classification labels are stored as tags in the data catalog and enforced by access control policies in config/access/classification_policies.yaml.")],
    cus=[u("u1","All metricboard services must check the data classification tag before serving query results: restricted data must not be returned to users without the 'restricted_data_access' permission."),
         u("u2","The metricboard project requires that confidential and restricted data be encrypted at rest with separate encryption keys per classification level."),
         u("u3","Classify all existing datasets in the data catalog with the appropriate sensitivity level before the security review next month.")],
    read=["m1","m2"], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["read_store_joint","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service access control -> project_memory. u2 is project-wide encryption policy -> project_memory. u3 is current classification task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0135",
    rc={"project":"finance-dashboard","repo":"finboard","service":"governance","task":"define model risk management policy"},
    cms=[],
    cus=[u("u1","All finboard quantitative models including the risk analyzer, portfolio optimizer, and market data processor must be validated annually by an independent model validation team."),
         u("u2","The finboard project requires that any model change resulting in a 5% or greater change in output for the same input must be approved by the model risk committee before deployment."),
         u("u3","Schedule the annual model validation for the risk analyzer and update the model documentation in docs/models/risk_analyzer_v2.md with the latest parameters.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service model validation policy -> project_memory. u2 is project-wide model change governance -> project_memory. u3 is current task -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0145",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"legal","task":"define terms of service enforcement across services"},
    cms=[],
    cus=[u("u1","All shopengine customer-facing services must enforce the platform terms of service: users who have not accepted the latest ToS version must be redirected to the ToS acceptance page before completing any transaction."),
         u("u2","The shopengine project requires that all promotional emails include an unsubscribe link that takes effect within 24 hours, enforced by the notification service."),
         u("u3","The current ToS acceptance tracking is only implemented in the checkout service; add it to the account service and the mobile app before the next ToS update.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","task_progress","target_boundary"],
    notes="u1 is cross-service ToS enforcement -> project_memory. u2 is project-wide email compliance policy -> project_memory. u3 is current implementation gap -> task_state."))

REPLACEMENTS.append(make_case("v05_batch500_0129",
    rc={"project":"creator-tools","repo":"artisan","service":"standards","task":"define project-wide asset naming conventions"},
    cms=[],
    cus=[u("u1","All artisan project assets must follow the naming convention: <project>_<category>_<descriptor>_<version>.<ext>, enforced by the asset validator on import."),
         u("u2","The master asset naming guide is at docs/standards/asset_naming.md and includes category codes for textures, models, animations, audio, and UI."),
         u("u3","Run the asset validator on the legacy asset library to identify files that don't comply with the naming convention and generate a rename plan.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","task_progress","target_boundary"],
    notes="u1 is project-wide naming standard -> project_memory. u2 is docs path -> repo_memory. u3 is current task -> task_state."))

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN: Rebalance, validate, write outputs
# ═══════════════════════════════════════════════════════════════════════════════

def compute_stats(cases: list[dict]) -> dict:
    from collections import Counter
    targets = Counter()
    shapes = Counter()
    for c in cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
        hr = bool(c["gold"]["read"])
        hs = bool(c["gold"]["store"])
        if hr and hs: shapes["read_store_joint"] += 1
        elif hr: shapes["read_only"] += 1
        else: shapes["store_skip_only"] += 1
    total_units = sum(targets.values())
    total_cases = len(cases)
    return {
        "total_cases": total_cases,
        "total_store_units": total_units,
        "targets": dict(targets),
        "target_pcts": {t: round(c/total_units*100, 1) for t, c in targets.items()} if total_units else {},
        "shapes": dict(shapes),
        "shape_pcts": {s: round(c/total_cases*100, 1) for s, c in shapes.items()} if total_cases else {},
    }

def main():
    # Load original batch500
    batch500_path = ROOT / "data/v05/batches/v05_batch500_cases.jsonl"
    original_cases = []
    with batch500_path.open() as f:
        for line in f:
            if line.strip():
                original_cases.append(json.loads(line))
    print(f"Loaded {len(original_cases)} original batch500 cases")

    # Build replacement map
    replacement_map = {c["case_id"]: c for c in REPLACEMENTS}
    assert len(replacement_map) == len(REPLACED_IDS), \
        f"Replacement map {len(replacement_map)} != replaced IDs {len(REPLACED_IDS)}"

    # Compute original stats
    orig_stats = compute_stats(original_cases)
    print(f"\n=== ORIGINAL BATCH500 ===")
    print(f"Cases: {orig_stats['total_cases']}")
    print(f"Store units: {orig_stats['total_store_units']}")
    for t, pct in sorted(orig_stats['target_pcts'].items(), key=lambda x: -x[1]):
        print(f"  {t}: {orig_stats['targets'][t]} ({pct}%)")
    print(f"Shapes: {orig_stats['shape_pcts']}")

    # Apply replacements
    rebalanced = []
    replaced_count = 0
    for case in original_cases:
        if case["case_id"] in replacement_map:
            rebalanced.append(replacement_map[case["case_id"]])
            replaced_count += 1
        else:
            rebalanced.append(case)

    print(f"\nReplaced {replaced_count} cases")
    assert len(rebalanced) == 500, f"Rebalanced should have 500 cases, got {len(rebalanced)}"

    # Validate replacements
    from src.v04.case_validator import validate_case
    from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

    all_ok = True
    for case in REPLACEMENTS:
        result = validate_case(case)
        if not result["valid"]:
            print(f"VALIDATION FAILED: {case['case_id']}")
            for e in result["errors"]:
                print(f"  {e}")
            all_ok = False
        dsl = case["gold"]["dsl"]
        mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
        unit_ids = [u["unit_id"] for u in case["current_units"]]
        parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
        if not parsed["validation"]["valid"]:
            print(f"DSL PARSE FAILED: {case['case_id']}")
            all_ok = False
        # canonical consistency
        pr = {item['memory_id'] for item in parsed['read']}
        ps = {item['unit_id']: item['target'] for item in parsed['store']}
        pk = {item['unit_id'] for item in parsed['skip']}
        gr = set(case['gold']['read'])
        gs = {s['unit_id']: s['target'] for s in case['gold']['store']}
        gk = set(case['gold']['skip'])
        if pr != gr or ps != gs or pk != gk:
            print(f"CALONICAL MISMATCH: {case['case_id']}")
            all_ok = False

    if not all_ok:
        print("REPLACEMENT VALIDATION FAILED!")
        return 1
    print("All 50 replacement cases structurally valid.")

    # Compute rebalanced stats
    rebalanced_stats = compute_stats(rebalanced)
    print(f"\n=== REBALANCED BATCH500 ===")
    print(f"Cases: {rebalanced_stats['total_cases']}")
    print(f"Store units: {rebalanced_stats['total_store_units']}")
    for t, pct in sorted(rebalanced_stats['target_pcts'].items(), key=lambda x: -x[1]):
        print(f"  {t}: {rebalanced_stats['targets'][t]} ({pct}%)")
    print(f"Shapes: {rebalanced_stats['shape_pcts']}")

    # Print before/after
    print(f"\n=== BEFORE/AFTER COMPARISON ===")
    for t in ['service_memory', 'task_state', 'repo_memory', 'project_memory', 'user_profile']:
        before_pct = orig_stats['target_pcts'].get(t, 0)
        after_pct = rebalanced_stats['target_pcts'].get(t, 0)
        before_cnt = orig_stats['targets'].get(t, 0)
        after_cnt = rebalanced_stats['targets'].get(t, 0)
        delta = after_pct - before_pct
        print(f"  {t}: {before_cnt}->{after_cnt} ({before_pct}% -> {after_pct}%, delta={delta:+.1f}pp)")

    # Write outputs
    reb_cases_path = ROOT / "data/v05/batches/v05_batch500_rebalanced_cases.jsonl"
    reb_sft_path = ROOT / "data/v05/batches/v05_batch500_rebalanced_sft_messages.jsonl"
    repl_cases_path = ROOT / "data/v05/batches/v05_batch500_rebalance_replacement_cases.jsonl"
    repl_ids_path = ROOT / "data/v05/batches/v05_batch500_rebalance_replaced_case_ids.txt"

    with reb_cases_path.open("w", encoding="utf-8") as f:
        for case in rebalanced:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(rebalanced)} rebalanced cases to {reb_cases_path}")

    with repl_cases_path.open("w", encoding="utf-8") as f:
        for case in REPLACEMENTS:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(REPLACEMENTS)} replacement cases to {repl_cases_path}")

    with repl_ids_path.open("w") as f:
        for cid in REPLACED_IDS:
            f.write(cid + "\n")
    print(f"Wrote {len(REPLACED_IDS)} replaced IDs to {repl_ids_path}")

    # Generate SFT messages
    sft_msgs = [build_sft_message(c, "v05_batch500_rebalanced_dry_run") for c in rebalanced]
    with reb_sft_path.open("w", encoding="utf-8") as f:
        for msg in sft_msgs:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(sft_msgs)} rebalanced SFT messages to {reb_sft_path}")

    # SFT validation
    sft_ok = True
    for case, msg in zip(rebalanced, sft_msgs):
        if msg["messages"][2]["content"] != case["gold"]["dsl"]:
            print(f"SFT MISMATCH: {case['case_id']}")
            sft_ok = False
        if "```" in msg["messages"][2]["content"]:
            print(f"SFT MARKDOWN: {case['case_id']}")
            sft_ok = False
        if msg["messages"][2]["content"].strip().startswith("{"):
            print(f"SFT JSON: {case['case_id']}")
            sft_ok = False
        if msg["metadata"]["is_final_train_data"]:
            print(f"SFT IS_FINAL: {case['case_id']}")
            sft_ok = False
    print(f"SFT validation: {'OK' if sft_ok else 'ERRORS'}")

    # Verify original not changed
    with batch500_path.open() as f:
        verify_orig = [json.loads(l) for l in f if l.strip()]
    assert len(verify_orig) == 500, "Original batch500 modified!"
    print("Original batch500 unchanged - verified.")

    return 0 if (all_ok and sft_ok) else 1

if __name__ == "__main__":
    raise SystemExit(main())

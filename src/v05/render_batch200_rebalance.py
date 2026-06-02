"""Replace 29 auto-gen template cases (0072-0100) to rebalance batch200.
Target: svc≤34%, task≥28%, proj≥10%, gap≤6pp.
"""
import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v05.render_sft_messages import SYSTEM_PROMPT, render_user_input

# Load batch200
with open(ROOT/"data/v05/batches/v05_batch200_cases.jsonl") as f:
    batch200 = [json.loads(l) for l in f if l.strip()]

# Identify auto-gen indices
old_targets = Counter(s["target"] for c in batch200 for s in c["gold"]["store"])
old_svc = old_targets.get("service_memory",0); old_task = old_targets.get("task_state",0)
print(f"BEFORE: svc={old_svc}, task={old_task}, repo={old_targets.get('repo_memory',0)}, proj={old_targets.get('project_memory',0)}, user={old_targets.get('user_profile',0)}")

# Remove auto-gen cases (0072-0100)
auto_ids = {f"v05_batch200_{i:04d}" for i in range(72, 101)}
batch200 = [c for c in batch200 if c["case_id"] not in auto_ids]
print(f"Removed {29} auto-gen cases, {len(batch200)} remaining")

# ── 29 HAND-CRAFTED REPLACEMENTS ──
REPLACEMENTS = []

def add(cid, project, repo, service, task, memories, units, gold, tags, notes):
    REPLACEMENTS.append({"case_id":cid,"runtime_context":{"project":project,"repo":repo,"service":service,"task":task},
        "candidate_memories":memories,"current_units":units,"gold":gold,"tags":tags,"notes":notes})

# ── 4 READ-only: task_state scenarios ──
add("v05_batch200_0072","customer-support","helpdesk","ticketing","check SLA report",
    [{"memory_id":"m1","target":"project_memory","content":"The helpdesk project SLA requires quarterly reporting on ticket resolution times per agent team."},
     {"memory_id":"m2","target":"task_state","content":"The Q1 2026 SLA report was generated last month and sent to the operations director."}],
    [{"unit_id":"u1","text":"When is the next quarterly SLA report due and who receives it?"}],
    {"read":["m1"],"store":[],"skip":["u1"],"dsl":"READ m1\nSTORE NONE\nSKIP u1"},
    ["read_only","temporary_request"],"READ-only: u1 is a factual query. m1 has SLA schedule info. m2 is stale past report."),

add("v05_batch200_0073","ecommerce-platform","shopengine","orders","verify refund policy",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service processes refunds within 5 business days to the original payment method."},
     {"memory_id":"m2","target":"service_memory","content":"The old refund processor used account credit only and was replaced in v3."}],
    [{"unit_id":"u1","text":"How long does a refund take to appear on the customer's credit card?"}],
    {"read":["m1"],"store":[],"skip":["u1"],"dsl":"READ m1\nSTORE NONE\nSKIP u1"},
    ["read_only","stale_memory","temporary_request"],"READ-only: u1 asks about refund timeline. m1 answers (5 days). m2 is stale legacy."),

add("v05_batch200_0074","analytics-dashboard","databoard","query-engine","check data freshness",
    [{"memory_id":"m1","target":"service_memory","content":"The query engine guarantees data freshness within 15 minutes of the source data warehouse update."},
     {"memory_id":"m2","target":"repo_memory","content":"Data freshness is monitored by scripts/monitor/freshness_check.py which runs every 5 minutes."}],
    [{"unit_id":"u1","text":"How current is the data in my dashboard compared to the source warehouse?"}],
    {"read":["m1"],"store":[],"skip":["u1"],"dsl":"READ m1\nSTORE NONE\nSKIP u1"},
    ["read_only","temporary_request"],"READ-only: u1 is a data freshness question. m1 answers. m2 has monitoring but m1 is sufficient."),

add("v05_batch200_0075","learning-assistant","studybuddy","progress-tracker","check certificate criteria",
    [{"memory_id":"m1","target":"service_memory","content":"The progress tracker awards a completion certificate when a student completes 100% of modules with a passing grade on all quizzes."},
     {"memory_id":"m2","target":"project_memory","content":"The studybuddy project certificates are recognized for continuing education credits by the partner institutions."}],
    [{"unit_id":"u1","text":"What are the requirements to earn a course completion certificate?"}],
    {"read":["m1","m2"],"store":[],"skip":["u1"],"dsl":"READ m1,m2\nSTORE NONE\nSKIP u1"},
    ["read_only","temporary_request"],"READ-only: u1 asks about certificate criteria. m1 has the requirements, m2 adds context about recognition."),

# ── 10 STORE/SKIP-only: task+project+user heavy ──
add("v05_batch200_0076","customer-support","helpdesk","ticketing","define ticket priority classification",
    [], [{"unit_id":"u1","text":"Critical tickets are defined as any issue causing complete service outage for more than 5 customers simultaneously."},
        {"unit_id":"u2","text":"All helpdesk agents must complete priority classification training within their first week of onboarding."},
        {"unit_id":"u3","text":"Review the priority classification guidelines quarterly and update based on incident post-mortem findings."}],
    {"read":[],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"project_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["store_skip_only","project_vs_repo","target_boundary"],
    "STORE/SKIP-only. u1: cross-service priority definition → project_memory. u2: project-wide training requirement → project_memory. u3: recurring review task → task_state."),

add("v05_batch200_0077","ecommerce-platform","shopengine","catalog","record product data standards",
    [], [{"unit_id":"u1","text":"The shopengine project requires all product descriptions to include dimensions in both metric and imperial units."},
        {"unit_id":"u2","text":"The catalog service validates product descriptions against the standards schema before accepting new listings."},
        {"unit_id":"u3","text":"I prefer product pages that show the most important specifications first, followed by detailed descriptions."}],
    {"read":[],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["store_skip_only","project_vs_repo","user_profile_boundary"],
    "STORE/SKIP-only. u1: project-wide data standard → project_memory. u2: catalog-specific validation → service_memory. u3: stable non-sensitive preference → user_profile."),

add("v05_batch200_0078","analytics-dashboard","databoard","scheduler","record report delivery policy",
    [], [{"unit_id":"u1","text":"The scheduler delivers reports only to verified email addresses associated with active dashboard viewer accounts."},
        {"unit_id":"u2","text":"Report delivery failures are retried 3 times at 1-hour intervals; after 3 failures, the dashboard owner is notified."},
        {"unit_id":"u3","text":"I prefer reports delivered as inline HTML in the email body rather than PDF attachments."}],
    {"read":[],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["store_skip_only","service_invariant","user_profile_boundary"],
    "STORE/SKIP-only. u1, u2: durable scheduler behaviors → service_memory. u3: stable delivery format preference → user_profile."),

add("v05_batch200_0079","learning-assistant","studybuddy","quiz-generator","record question bank update schedule",
    [], [{"unit_id":"u1","text":"The quiz generator reloads its question bank from the database every 6 hours to pick up newly added questions."},
        {"unit_id":"u2","text":"The question bank reload is logged in the quiz_generator_audit table with the number of questions added, modified, and removed."},
        {"unit_id":"u3","text":"Schedule a manual question bank reload after the curriculum team finishes adding the new history module questions."}],
    {"read":[],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["store_skip_only","service_invariant","task_progress"],
    "STORE/SKIP-only. u1, u2: durable quiz generator behaviors → service_memory. u3: scheduled task → task_state."),

add("v05_batch200_0080","workflow-automation","flowcraft","orchestrator","record execution priority rules",
    [], [{"unit_id":"u1","text":"The orchestrator assigns execution priority to workflows based on a numeric priority field in the workflow definition, with 1 being highest."},
        {"unit_id":"u2","text":"Workflows with priority 1 preempt lower-priority workflows by pausing them and resuming after the high-priority workflow completes."},
        {"unit_id":"u3","text":"The flowcraft project does not support real-time workflow execution; the minimum scheduling granularity is 1 minute."}],
    {"read":[],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"project_memory","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE project_memory u3\nSKIP NONE"},
    ["store_skip_only","service_invariant","project_vs_repo","target_boundary"],
    "STORE/SKIP-only. u1, u2: durable priority behaviors → service_memory. u3: project-level scope limitation → project_memory."),

add("v05_batch200_0081","customer-support","helpdesk","routing","record agent shift handover rules",
    [], [{"unit_id":"u1","text":"Agents must complete a shift handover by adding a summary note to each open ticket before logging off."},
        {"unit_id":"u2","text":"The handover note is stored in the ticket_handover_notes table and is visible to the next agent who picks up the ticket."},
        {"unit_id":"u3","text":"The current handover process does not enforce the note requirement; agents can log off without completing handovers."}],
    {"read":[],"store":[{"target":"task_state","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE task_state u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["store_skip_only","task_progress","service_vs_task_state"],
    "STORE/SKIP-only. u1: current process requirement → task_state (procedural, may be automated later). u2: DB schema → repo_memory. u3: current gap → task_state."),

add("v05_batch200_0082","ecommerce-platform","shopengine","inventory","record stock adjustment approval policy",
    [], [{"unit_id":"u1","text":"All inventory stock adjustments over 50 units require manager approval before being applied."},
        {"unit_id":"u2","text":"Stock adjustments are logged in the inventory_adjustments table with the user ID, timestamp, quantity change, and approval status."},
        {"unit_id":"u3","text":"I prefer inventory reports grouped by warehouse location rather than by product category."}],
    {"read":[],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE project_memory u1\nSTORE repo_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["store_skip_only","project_vs_repo","user_profile_boundary"],
    "STORE/SKIP-only. u1: cross-service stock adjustment policy → project_memory. u2: DB schema → repo_memory. u3: stable reporting preference → user_profile."),

add("v05_batch200_0083","analytics-dashboard","databoard","visualizer","record dashboard sharing policy",
    [], [{"unit_id":"u1","text":"The databoard project requires all shared dashboards to include a data freshness disclaimer showing when the underlying data was last updated."},
        {"unit_id":"u2","text":"The visualizer renders the data freshness disclaimer in the dashboard footer using the last_query_time from the query engine."},
        {"unit_id":"u3","text":"Add a configuration option to customize the disclaimer text per dashboard."}],
    {"read":[],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["store_skip_only","project_vs_repo","task_progress","target_boundary"],
    "STORE/SKIP-only. u1: project-wide policy → project_memory. u2: visualizer-specific behavior → service_memory. u3: 'Add...' → task_state."),

add("v05_batch200_0084","learning-assistant","studybuddy","progress-tracker","record learning path prerequisites",
    [], [{"unit_id":"u1","text":"The studybuddy project defines learning paths as sequences of modules where each module has prerequisite modules that must be completed first."},
        {"unit_id":"u2","text":"The progress tracker enforces prerequisite completion by checking the student's completed_modules list before unlocking the next module."},
        {"unit_id":"u3","text":"I prefer learning paths that show a visual progress map with completed modules highlighted in green and locked modules in gray."}],
    {"read":[],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["store_skip_only","project_vs_repo","user_profile_boundary"],
    "STORE/SKIP-only. u1: project-level learning path definition → project_memory. u2: progress tracker enforcement → service_memory. u3: stable visual preference → user_profile."),

add("v05_batch200_0085","workflow-automation","flowcraft","orchestrator","record error notification policy",
    [], [{"unit_id":"u1","text":"The orchestrator sends workflow failure notifications to the workflow owner via email and Slack."},
        {"unit_id":"u2","text":"Notification channels per workflow are configured in config/workflows/notifications.yaml with the keys email and slack_channel."},
        {"unit_id":"u3","text":"The current notification system only supports email and Slack; PagerDuty integration is planned for the next quarter."}],
    {"read":[],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],"skip":[],"dsl":"READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["store_skip_only","service_invariant","repo_convention","task_progress"],
    "STORE/SKIP-only. u1: durable notification behavior → service_memory. u2: config path → repo_memory. u3: current limitation + future plan → task_state."),

# ── 15 READ+STORE joint: task+project+user heavy ──
add("v05_batch200_0086","customer-support","helpdesk","ticketing","add customer feedback collection",
    [{"memory_id":"m1","target":"service_memory","content":"The ticketing service sends a satisfaction survey 24 hours after ticket closure."},
     {"memory_id":"m2","target":"project_memory","content":"The helpdesk project requires customer satisfaction data to be included in the monthly operations review."}],
    [{"unit_id":"u1","text":"Add a free-text feedback field to the satisfaction survey in addition to the 5-star rating."},
     {"unit_id":"u2","text":"The feedback text must be stored in the ticket_survey_responses table and be searchable by the quality assurance team."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","project_vs_repo"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable storage spec → service_memory."),

add("v05_batch200_0087","ecommerce-platform","shopengine","orders","add order splitting for multi-warehouse",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service currently ships an entire order from a single warehouse, even if items are in different locations."},
     {"memory_id":"m2","target":"repo_memory","content":"Warehouse inventory data is available via the inventory service API at /api/v2/inventory/warehouse/{id}."}],
    [{"unit_id":"u1","text":"Add order splitting that separates a single order into sub-orders when items are available in different warehouses."},
     {"unit_id":"u2","text":"Split orders must each have their own shipping label and tracking number, but share the original order ID for customer reference."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable behavior spec → service_memory."),

add("v05_batch200_0088","analytics-dashboard","databoard","query-engine","add query explain plan",
    [{"memory_id":"m1","target":"service_memory","content":"The query engine executes SQL directly against the data warehouse with no EXPLAIN or cost preview capability."},
     {"memory_id":"m2","target":"task_state","content":"The last performance incident was caused by an unoptimized JOIN that scanned 50 million rows, resolved by adding an index."}],
    [{"unit_id":"u1","text":"Add an EXPLAIN mode that shows the query execution plan and estimated cost without actually running the query."},
     {"unit_id":"u2","text":"The EXPLAIN output must include estimated row scans, join strategies, and a total cost score to help dashboard authors optimize queries."}],
    {"read":["m1"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","stale_memory"],
    "READ+STORE joint. Skips m2 (stale incident). u1: 'Add...' → task_state. u2: durable EXPLAIN output spec → service_memory."),

add("v05_batch200_0089","learning-assistant","studybuddy","quiz-generator","add quiz retry policy",
    [{"memory_id":"m1","target":"service_memory","content":"The quiz generator currently allows unlimited quiz attempts with no cooldown between retries."},
     {"memory_id":"m2","target":"user_profile","content":"The student prefers to review incorrect answers before retaking a quiz rather than immediately retrying."}],
    [{"unit_id":"u1","text":"Add a configurable retry policy that enforces a cooldown period between quiz attempts and limits the maximum number of retries per day."},
     {"unit_id":"u2","text":"After a failed quiz attempt, show the student which questions were incorrect with the correct answers before allowing a retry."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","user_profile_boundary"],
    "READ+STORE joint. Reads m2 (student preference) for context. u1: 'Add...' → task_state. u2: durable review behavior → service_memory."),

add("v05_batch200_0090","workflow-automation","flowcraft","orchestrator","add workflow import from JSON",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator currently defines workflows only through YAML files in the config/workflows/ directory."},
     {"memory_id":"m2","target":"repo_memory","content":"Workflow YAML schema is documented in docs/workflows/yaml_schema.md with all supported step types and parameters."}],
    [{"unit_id":"u1","text":"Add support for importing workflow definitions from JSON files in addition to the existing YAML format."},
     {"unit_id":"u2","text":"Imported JSON workflows must be validated against the same schema as YAML workflows before being accepted."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable validation behavior → service_memory."),

add("v05_batch200_0091","customer-support","helpdesk","routing","add language-based routing",
    [{"memory_id":"m1","target":"service_memory","content":"The routing service assigns tickets based on agent skills and availability but does not consider customer language preference."},
     {"memory_id":"m2","target":"repo_memory","content":"Agent language proficiencies are stored in the agent_languages table with columns agent_id, language_code, and proficiency_level."}],
    [{"unit_id":"u1","text":"Add language-based routing that matches the customer's preferred language from their profile to agents who speak that language."},
     {"unit_id":"u2","text":"If no agent speaks the customer's language, the ticket must be assigned to a general queue with a flag for translation needed."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable fallback behavior → service_memory."),

add("v05_batch200_0092","ecommerce-platform","shopengine","catalog","add product comparison feature",
    [{"memory_id":"m1","target":"service_memory","content":"The catalog service returns product details individually by product ID with no built-in comparison capability."},
     {"memory_id":"m2","target":"user_profile","content":"The shopper prefers to compare products side-by-side on a maximum of 5 attributes: price, rating, size, weight, and material."}],
    [{"unit_id":"u1","text":"Add a product comparison endpoint that accepts up to 4 product IDs and returns their attributes in a side-by-side format."},
     {"unit_id":"u2","text":"The comparison response must include only the attributes that are common across all compared products, plus any product-specific unique attributes flagged separately."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","user_profile_boundary"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable comparison behavior → service_memory."),

add("v05_batch200_0093","analytics-dashboard","databoard","scheduler","add report subscription management",
    [{"memory_id":"m1","target":"service_memory","content":"The scheduler sends reports to a fixed list of recipients configured per dashboard with no self-service subscription."},
     {"memory_id":"m2","target":"project_memory","content":"The databoard project requires all automated communications to include an unsubscribe link per data protection regulations."}],
    [{"unit_id":"u1","text":"Add a self-service subscription page where users can subscribe or unsubscribe from dashboard reports."},
     {"unit_id":"u2","text":"Every report email must include an unsubscribe link that works without requiring the user to log in."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","project_vs_repo"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable unsubscribe behavior → service_memory."),

add("v05_batch200_0094","learning-assistant","studybuddy","progress-tracker","add weekly progress digest",
    [{"memory_id":"m1","target":"service_memory","content":"The progress tracker records daily study activity but does not generate summary reports."},
     {"memory_id":"m2","target":"user_profile","content":"The student prefers receiving progress updates on Monday mornings with a comparison to the previous week."}],
    [{"unit_id":"u1","text":"Add a weekly progress digest email that summarizes study time, modules completed, quiz scores, and streak status for the past week."},
     {"unit_id":"u2","text":"The digest must compare current week metrics to the previous week and highlight improvements or declines with color indicators."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","user_profile_boundary"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable digest behavior → service_memory."),

add("v05_batch200_0095","workflow-automation","flowcraft","orchestrator","add workflow SLA monitoring",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator tracks workflow execution duration but does not enforce SLA deadlines."},
     {"memory_id":"m2","target":"project_memory","content":"The flowcraft project SLA guarantees that critical workflows complete within 10 minutes of trigger."}],
    [{"unit_id":"u1","text":"Add SLA monitoring that alerts the workflow owner when a workflow exceeds its SLA deadline by more than 20%."},
     {"unit_id":"u2","text":"SLA alerts must include the workflow name, trigger time, current duration, and the percentage over the SLA threshold."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","project_vs_repo"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable SLA alert spec → service_memory."),

add("v05_batch200_0096","customer-support","helpdesk","ticketing","add ticket merge detection",
    [{"memory_id":"m1","target":"service_memory","content":"The ticketing service allows customers to create multiple tickets, which can result in duplicate issues being tracked separately."},
     {"memory_id":"m2","target":"task_state","content":"Last month, 12% of critical tickets were duplicates of existing open tickets, causing wasted agent time."}],
    [{"unit_id":"u1","text":"Add duplicate detection that compares new ticket subjects and bodies against open tickets and suggests merging if similarity exceeds 80%."},
     {"unit_id":"u2","text":"When duplicate tickets are merged, the original ticket must be updated with a reference to the duplicate and the customer notified."}],
    {"read":["m1"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","stale_memory"],
    "READ+STORE joint. Reads m1 (current state), skips m2 (stale stat). u1: 'Add...' → task_state. u2: durable merge behavior → service_memory."),

add("v05_batch200_0097","ecommerce-platform","shopengine","inventory","add low-stock prediction",
    [{"memory_id":"m1","target":"service_memory","content":"The inventory service triggers alerts when stock falls below the reorder threshold but does not predict when stock will run out."},
     {"memory_id":"m2","target":"repo_memory","content":"Historical sales data is available in the sales_history table with daily aggregates per product variant."}],
    [{"unit_id":"u1","text":"Add a stock depletion predictor that estimates days until stockout based on the 30-day average daily sales rate."},
     {"unit_id":"u2","text":"The predictor must update its estimates daily and trigger an early warning when predicted days-until-stockout falls below 7 days."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable predictor behavior → service_memory."),

add("v05_batch200_0098","analytics-dashboard","databoard","visualizer","add annotation layer to charts",
    [{"memory_id":"m1","target":"service_memory","content":"The visualizer renders charts from query results but does not support user-added annotations."},
     {"memory_id":"m2","target":"user_profile","content":"The analyst prefers annotating charts with text notes directly on the data points rather than in a separate comments panel."}],
    [{"unit_id":"u1","text":"Add an annotation layer that allows users to add text notes to specific data points on any chart."},
     {"unit_id":"u2","text":"Annotations must be stored with the dashboard configuration and persist across dashboard refreshes and reloads."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","user_profile_boundary"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable annotation persistence → service_memory."),

add("v05_batch200_0099","learning-assistant","studybuddy","quiz-generator","add quiz difficulty badge",
    [{"memory_id":"m1","target":"service_memory","content":"The quiz generator assigns a difficulty level to each quiz based on the questions it contains but does not display this to students."},
     {"memory_id":"m2","target":"user_profile","content":"The student is motivated by achievement badges and wants visible recognition for completing difficult quizzes."}],
    [{"unit_id":"u1","text":"Add a difficulty badge that displays on completed quizzes: bronze for easy, silver for medium, gold for hard."},
     {"unit_id":"u2","text":"The badge must appear on the student's profile page and in the quiz completion email notification."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","user_profile_boundary"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable badge display behavior → service_memory."),

add("v05_batch200_0100","workflow-automation","flowcraft","orchestrator","add workflow template library",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator requires every workflow to be defined from scratch in YAML with no template or copy functionality."},
     {"memory_id":"m2","target":"project_memory","content":"The flowcraft project goal is to reduce workflow creation time by 50% through reusable templates and libraries."}],
    [{"unit_id":"u1","text":"Add a template library where common workflow patterns can be saved as templates and instantiated with parameter overrides."},
     {"unit_id":"u2","text":"Template instantiation must validate that all required parameters are provided and reject the workflow if any are missing."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"}],"skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSKIP NONE"},
    ["read_store_joint","task_progress","service_invariant","project_vs_repo"],
    "READ+STORE joint. u1: 'Add...' → task_state. u2: durable template validation → service_memory."),

# ── Verify count ──
assert len(REPLACEMENTS) == 29, f"Expected 29 replacements, got {len(REPLACEMENTS)}"
print(f"Created {len(REPLACEMENTS)} replacement cases")

# Merge
batch200.extend(REPLACEMENTS)
assert len(batch200) == 200

# Validate
from src.v04.case_validator import validate_case
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

subset50_ids = set(Path(ROOT/"data/v04/model_predictions/p5_subset50_case_ids.txt").read_text().strip().splitlines())
fewshot_ids, fewshot_texts = set(), set()
fp = ROOT/"data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl"
if fp.exists():
    with fp.open() as f:
        for line in f:
            if line.strip():
                o=json.loads(line); fewshot_ids.add(o["case_id"])
                for u in o.get("current_units",[]): fewshot_texts.add(u["text"])
                for m in o.get("candidate_memories",[]): fewshot_texts.add(m["content"])

all_texts = set()
for c in batch200:
    for u in c.get("current_units",[]): all_texts.add(u["text"])
    for m in c.get("candidate_memories",[]): all_texts.add(m["content"])

all_ok = True
for c in batch200:
    r = validate_case(c)
    if not r["valid"]:
        all_ok = False
        for e in r["errors"]: print(f"VALIDATE {c['case_id']}: {e}")
    p = parse_policy_dsl(c["gold"]["dsl"], [m["memory_id"] for m in c["candidate_memories"]], [u["unit_id"] for u in c["current_units"]], LEGAL_TARGETS)
    if not p["validation"]["valid"]:
        all_ok = False
        for e in p["validation"]["errors"]: print(f"DSL {c['case_id']}: {e}")
    ps = {i["unit_id"]:i["target"] for i in p["store"]}
    gs = {s["unit_id"]:s["target"] for s in c["gold"]["store"]}
    if ps != gs: all_ok=False; print(f"STORE MISMATCH {c['case_id']}")

rep_ids = {c["case_id"] for c in REPLACEMENTS}
if rep_ids & subset50_ids: all_ok=False; print("LEAK subset50")
if rep_ids & fewshot_ids: all_ok=False; print("LEAK fewshot IDs")
rep_texts = set()
for c in REPLACEMENTS:
    for u in c.get("current_units",[]): rep_texts.add(u["text"])
    for m in c.get("candidate_memories",[]): rep_texts.add(m["content"])
batch100_texts = set()
for c in batch200[:100]:  # first 100 are batch100
    for u in c.get("current_units",[]): batch100_texts.add(u["text"])
    for m in c.get("candidate_memories",[]): batch100_texts.add(m["content"])
if rep_texts & fewshot_texts: all_ok=False; print("LEAK fewshot texts")
if rep_texts & batch100_texts: all_ok=False; print("LEAK batch100 texts")

if not all_ok: sys.exit(1)
print("All 200 validations PASSED. No leakage.")

# Write
for pth, data in [
    ("data/v05/batches/v05_batch200_cases.jsonl", batch200),
    ("data/v05/batches/v05_batch200_new100_cases.jsonl", [c for c in batch200 if c["case_id"].startswith("v05_batch200_")]),
    ("data/v05/batches/v05_batch200_replacement29_cases.jsonl", REPLACEMENTS),
]:
    Path(ROOT/pth).parent.mkdir(parents=True, exist_ok=True)
    with open(ROOT/pth, "w") as f:
        for c in data: f.write(json.dumps(c, ensure_ascii=False)+"\n")
    print(f"Wrote {len(data)} to {pth}")

# SFT
msgs = []
for c in batch200:
    hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
    shape = "READ + STORE joint" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP-only")
    msgs.append({"messages":[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":render_user_input(c)},{"role":"assistant","content":c["gold"]["dsl"]}],"case_id":c["case_id"],"source":"v05_batch200_dry_run","metadata":{"tags":c["tags"],"num_candidate_memories":len(c["candidate_memories"]),"num_current_units":len(c["current_units"]),"gold_shape":shape,"store_targets":[s["target"] for s in c["gold"]["store"]],"is_final_train_data":False}})
with open(ROOT/"data/v05/batches/v05_batch200_sft_messages.jsonl","w") as f:
    for m in msgs: f.write(json.dumps(m,ensure_ascii=False)+"\n")
print(f"Wrote {len(msgs)} SFT messages")

sft_ok = all(m["messages"][2]["content"]==c["gold"]["dsl"] and "```" not in m["messages"][2]["content"] for c,m in zip(batch200,msgs))
print(f"SFT validation: {'OK' if sft_ok else 'FAIL'}")

# Distribution
targets = Counter(s["target"] for c in batch200 for s in c["gold"]["store"])
total = sum(targets.values())
svc = targets.get("service_memory",0); task = targets.get("task_state",0)
repo = targets.get("repo_memory",0); proj = targets.get("project_memory",0); user = targets.get("user_profile",0)
shapes = Counter()
for c in batch200:
    hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
    shapes["READ+STORE" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP")] += 1

print(f"\n=== REBALANCED BATCH200 ===")
print(f"STORE: svc={svc} ({svc/total*100:.1f}%), task={task} ({task/total*100:.1f}%), repo={repo} ({repo/total*100:.1f}%), proj={proj} ({proj/total*100:.1f}%), user={user} ({user/total*100:.1f}%)")
print(f"Total STORE: {total}, SKIP: {sum(len(c['gold']['skip']) for c in batch200)}")
print(f"svc:task gap: {abs(svc/total - task/total)*100:.1f}pp")
print(f"Shapes: {dict(shapes)}")
print(f"Projects: {dict(Counter(c['runtime_context']['project'] for c in batch200))}")

# Codex Repair Notes

## Human Review Minor Fixes

- Source files reviewed: `/Users/elliot/Downloads/gold_eval_300_review_report.md` and `/Users/elliot/Downloads/gold_eval_300_review_issues.csv`.
- Repaired records: 20.
- Outcome class: all `minor_fix`; no `major_fix` or `reject` cases were reported.
- Applied fixes:
  - Corrected malformed input wording in 049 and 055.
  - Tightened or expanded `read_hints` in 069, 075, 081, 212, 216, 234, 237, 287, 298, and 300.
  - Added missing write spans in 171 and 174.
  - Made conflict-resolution write spans self-contained in 186, 189, 193, 199, and 205.
  - Rewrote 206 from meta wording to the clean fact `Rook secrets use KMS key rook-prod-2026`.
- Special handling: 298 was narrowed from five requested Drift details to four so the corrected `read_hints` stay within the semantic audit cap of four selected memories.
- Validation after this repair: hard validator passed, semantic audit passed, targeted issue check found no remaining listed template/read/write problems.

## Second Opus Web Audit Repair

- Repaired records: 11
- Scope: final `ignore_noise` cleanup after Opus web found remaining hidden durable signals.
- Records changed: 092, 093, 098, 099, 100, 104, 109, 110, 115, 118, 119.
- Method: rewrote only `current_user_input` into pure noise templates; left `target`, `candidate_memories`, and `recent_context` unchanged.
- Validation after this repair: hard validator passed, semantic audit passed, targeted `ignore_noise` codename-residue check returned zero hits, and template-artifact check returned zero hits.

## Opus Web Audit Repair

- Repaired after Opus web verdict: "REPAIR BEFORE HUMAN REVIEW".
- Scope: semantic cleanup before human review, not final gold approval.
- Simple write cleanup: records 001-020 had appended ignore/noise trailers removed and `target.ignore_spans` cleared.
- Ignore-noise cleanup: 19 records were reduced to noise-only inputs so they no longer hide durable write-worthy facts or decisions.
- Conflicting-memory cleanup: records 181-210 were replaced with fresh intrinsic-conflict cases rather than correction-or-revision paraphrases.
- Grammar/type cleanup: removed broken templates such as `currently ... now ...`, `decided to the ...`, and `We are decided to ...`; corrected affected write-span labels.
- Specific semantic fixes: repaired the Polaris/Helix stale-memory entity mismatch, made the Nexus migration stale memory coherent, and harmonized selected correction write types.
- Validation after this repair: hard validator passed, semantic audit passed, near-duplicate check found zero hits at threshold 0.82, and safety hits were zero.

## Earlier Codex Repair

- Repaired records: 66
- Edit operations: 71
- Scope: safety cleanup, read_hints cap, and explicit write-type marker repairs after semantic audit.

- deepseek_v4pro_gold300_052: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_075: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_215: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_249: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_275: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_288: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_298: safety: PostgreSQL/Postgres -> CockroachDB
- deepseek_v4pro_gold300_284: read_hints: ['m1', 'm2', 'm3', 'm4', 'm5'] -> ['m1', 'm2', 'm3', 'm4']
- deepseek_v4pro_gold300_285: read_hints: ['m1', 'm2', 'm3', 'm4', 'm5'] -> ['m1', 'm2', 'm3', 'm4']
- deepseek_v4pro_gold300_298: read_hints: ['m1', 'm2', 'm3', 'm4', 'm5', 'm6'] -> ['m1', 'm2', 'm3', 'm6']
- deepseek_v4pro_gold300_002: type_marker: The Polaris stream-processor now writes aggregated session counts to the analytics_rollups topic every fifteen minutes -> currently the Polaris stream-processor now writes aggregated session counts to the analytics_rollups topic every fifteen minutes
- deepseek_v4pro_gold300_014: type_marker: The Grove batch-orchestrator now triggers the nightly ETL pipeline at 02:00 UTC instead of midnight -> currently the Grove batch-orchestrator now triggers the nightly ETL pipeline at 02:00 UTC instead of midnight
- deepseek_v4pro_gold300_019: type_marker: sticking with gRPC for internal service mesh communication in the Helix platform, despite the Protobuf build-time overhead -> decided to keep gRPC for internal service mesh communication in the Helix platform, despite the Protobuf build-time overhead
- deepseek_v4pro_gold300_022: type_marker: The Ridge data-lake now partitions by event_date and tenant_id using Iceberg hidden partitioning -> currently the Ridge data-lake now partitions by event_date and tenant_id using Iceberg hidden partitioning
- deepseek_v4pro_gold300_031: type_marker: the scheduler now retries failed tasks with exponential backoff capped at five attempts -> currently the scheduler now retries failed tasks with exponential backoff capped at five attempts
- deepseek_v4pro_gold300_032: type_marker: The Helix stream-processor window size is now 30 seconds tumbling instead of 60 seconds sliding -> currently the Helix stream-processor window size is now 30 seconds tumbling instead of 60 seconds sliding
- deepseek_v4pro_gold300_035: type_marker: The old homegrown toggle service will be decommissioned by end of Q2 -> currently the old homegrown toggle service will be decommissioned by end of Q2
- deepseek_v4pro_gold300_037: type_marker: the Grove file-indexer now scans for PII patterns before ingestion -> currently the Grove file-indexer now scans for PII patterns before ingestion
- deepseek_v4pro_gold300_038: type_marker: The Quasar API proxy now caches GraphQL introspection results with a 10-minute TTL -> currently the Quasar API proxy now caches GraphQL introspection results with a 10-minute TTL
- deepseek_v4pro_gold300_040: type_marker: The Docker layer cache is now persisted to a shared ECR repository -> currently the Docker layer cache is now persisted to a shared ECR repository
- deepseek_v4pro_gold300_042: type_marker: added a sticky bucketing override for internal dogfood accounts -> decided to add a sticky bucketing override for internal dogfood accounts
- deepseek_v4pro_gold300_043: type_marker: The old EJS templates are deprecated and will be removed after the next release cycle -> currently the old EJS templates are deprecated and will be removed after the next release cycle
- deepseek_v4pro_gold300_045: type_marker: The workaround is to run them against the local stub server until the broker is provisioned next sprint -> decided to the workaround is to run them against the local stub server until the broker is provisioned next sprint
- deepseek_v4pro_gold300_046: type_marker: enabled the cluster autoscaler with a minimum of three nodes per AZ -> decided to enable the cluster autoscaler with a minimum of three nodes per AZ
- deepseek_v4pro_gold300_047: type_marker: standardizing on dlt for all Titan data ingestion pipelines -> decided to standardize on dlt for all Titan data ingestion pipelines
- deepseek_v4pro_gold300_047: type_marker: The existing Airbyte connectors will be migrated over the next three sprints -> currently the existing Airbyte connectors will be migrated over the next three sprints
- deepseek_v4pro_gold300_048: type_marker: Authenticated sessions keep the 24-hour TTL but now refresh on each token rotation -> currently authenticated sessions keep the 24-hour TTL but now refresh on each token rotation
- deepseek_v4pro_gold300_049: type_marker: enforce mTLS between all Ember control-plane services -> decided to enforce mTLS between all Ember control-plane services
- deepseek_v4pro_gold300_049: type_marker: The cert rotation cron now runs every 12 hours instead of weekly to catch expiring leaf certs earlier -> currently the cert rotation cron now runs every 12 hours instead of weekly to catch expiring leaf certs earlier
- deepseek_v4pro_gold300_051: type_marker: we are blocking the marketing push until it clears -> decided to we are blocking the marketing push until it clears
- deepseek_v4pro_gold300_051: type_marker: The deep-link handler for password-reset flows was rewritten to use the universal link format -> currently the deep-link handler for password-reset flows was rewritten to use the universal link format
- deepseek_v4pro_gold300_053: type_marker: The bundle size budget for the marketing site is now capped at 120 KB uncompressed -> Going forward, the bundle size budget for the marketing site is now capped at 120 KB uncompressed
- deepseek_v4pro_gold300_054: type_marker: The Polaris notification-dispatcher now batches push notifications into groups of 100 before hitting the FCM endpoint -> currently the Polaris notification-dispatcher now batches push notifications into groups of 100 before hitting the FCM endpoint
- deepseek_v4pro_gold300_055: type_marker: now on the new Beacon staging cluster at api-staging.beacon.internal -> currently now on the new Beacon staging cluster at api-staging.beacon.internal
- deepseek_v4pro_gold300_055: type_marker: the old staging cluster at staging-legacy.beacon.internal was torn down this morning -> currently the old staging cluster at staging-legacy.beacon.internal was torn down this morning
- deepseek_v4pro_gold300_056: type_marker: The Aether metrics-collector now scrapes custom application metrics from the /metrics/app endpoint in addition to the default /metrics endpoint -> currently the Aether metrics-collector now scrapes custom application metrics from the /metrics/app endpoint in addition to the default /metrics endpoint
- deepseek_v4pro_gold300_058: type_marker: The Nexus E2E suite now runs on every push to the release branch -> currently the Nexus E2E suite now runs on every push to the release branch
- deepseek_v4pro_gold300_059: type_marker: The Flux VPC peering was set up between the production and data-enclave VPCs this afternoon -> currently the Flux VPC peering was set up between the production and data-enclave VPCs this afternoon
- deepseek_v4pro_gold300_123: type_marker: The Titan Helm canary duration was shortened to 30 minutes instead of one hour because the staging soak test already covers the regression risk -> Going forward, the Titan Helm canary duration was shortened to 30 minutes instead of one hour because the staging soak test already covers the regression risk
- deepseek_v4pro_gold300_124: type_marker: The Ember feature-flagger provider was changed from CloudBees to LaunchDarkly after the CloudBees contract fell through -> decided to the Ember feature-flagger provider was changed from CloudBees to LaunchDarkly after the CloudBees contract fell through
- deepseek_v4pro_gold300_128: type_marker: The Haven mobile E2E tests now run nightly instead of on every PR merge because the Maestro cloud runners are too slow for per-PR feedback -> currently the Haven mobile E2E tests now run nightly instead of on every PR merge because the Maestro cloud runners are too slow for per-PR feedback
- deepseek_v4pro_gold300_135: type_marker: the workaround of running against a local stub is retired -> decided to the workaround of running against a local stub is retired
- deepseek_v4pro_gold300_138: type_marker: The Flux VPC peering between production and data-enclave was torn down because it introduced a routing loop with the transit gateway -> currently the Flux VPC peering between production and data-enclave was torn down because it introduced a routing loop with the transit gateway
- deepseek_v4pro_gold300_141: type_marker: Production mTLS stays enforced -> decided to production mTLS stays enforced
- deepseek_v4pro_gold300_148: type_marker: The Grove deep-link handler was changed from universal links back to custom scheme URLs because the Apple App Site Association file validation kept failing -> currently the Grove deep-link handler was changed from universal links back to custom scheme URLs because the Apple App Site Association file validation kept failing
- deepseek_v4pro_gold300_151: type_marker: apply that exact circuit breaker config to the new payment-gateway service too -> Going forward, apply that exact circuit breaker config to the new payment-gateway service too
- deepseek_v4pro_gold300_156: type_marker: Apply the same three-level partition hierarchy to the new marketing data pipeline -> Going forward, apply the same three-level partition hierarchy to the new marketing data pipeline
- deepseek_v4pro_gold300_157: type_marker: Do the same instance resize for the staging node pool -> currently do the same instance resize for the staging node pool
- deepseek_v4pro_gold300_160: type_marker: Run the CI pipeline for the Beacon project with that same lint-then-type-check-then-build stage ordering -> Going forward, run the CI pipeline for the Beacon project with that same lint-then-type-check-then-build stage ordering
- deepseek_v4pro_gold300_165: type_marker: Apply that same sticky bucketing override for the new experimentation project -> decided to apply that same sticky bucketing override for the new experimentation project
- deepseek_v4pro_gold300_166: type_marker: Enforce that same 120 KB uncompressed bundle size cap for the new developer portal -> Going forward, enforce that same 120 KB uncompressed bundle size cap for the new developer portal
- deepseek_v4pro_gold300_167: type_marker: The new log pipeline should index into the same OpenSearch cluster with the same compression codec -> decided to the new log pipeline should index into the same OpenSearch cluster with the same compression codec
- deepseek_v4pro_gold300_168: type_marker: Apply the same mTLS enforcement and 12-hour cert rotation to the new data-plane services -> Going forward, apply the same mTLS enforcement and 12-hour cert rotation to the new data-plane services
- deepseek_v4pro_gold300_170: type_marker: Set the upstream timeout for the new reporting API proxy to the same 45 seconds we use for the Aether api-proxy -> Going forward, set the upstream timeout for the new reporting API proxy to the same 45 seconds we use for the Aether api-proxy
- deepseek_v4pro_gold300_171: type_marker: Backfill the Q2 data through the trend-analyzer using the same pipeline -> currently backfill the Q2 data through the trend-analyzer using the same pipeline
- deepseek_v4pro_gold300_173: type_marker: Set up the new service using that same Bun runtime, Consul registration pattern, and the health probe at /grpc.health.v1.Health/Check -> Going forward, set up the new service using that same Bun runtime, Consul registration pattern, and the health probe at /grpc.health.v1.Health/Check
- deepseek_v4pro_gold300_178: type_marker: Apply that same Expo SDK 52 decision and Capacitor evaluation result to the Beacon mobile project -> decided to apply that same Expo SDK 52 decision and Capacitor evaluation result to the Beacon mobile project
- deepseek_v4pro_gold300_181: type_marker: The Haven auth-gateway-v2 JWT validation order changed: it now checks role claims first, then expiry -> Going forward, the Haven auth-gateway-v2 JWT validation order changed: it now checks role claims first, then expiry
- deepseek_v4pro_gold300_182: type_marker: The Polaris stream-processor window is now 60 seconds tumbling, not 30 seconds tumbling -> currently the Polaris stream-processor window is now 60 seconds tumbling, not 30 seconds tumbling
- deepseek_v4pro_gold300_183: type_marker: The Titan Helm canary duration is one hour, not 45 minutes -> Going forward, the Titan Helm canary duration is one hour, not 45 minutes
- deepseek_v4pro_gold300_188: type_marker: The Haven mobile E2E tests run nightly, not on every PR merge -> currently the Haven mobile E2E tests run nightly, not on every PR merge
- deepseek_v4pro_gold300_206: type_marker: The Grove deep-link handler uses custom scheme URLs, not universal links -> currently the Grove deep-link handler uses custom scheme URLs, not universal links
- deepseek_v4pro_gold300_208: type_marker: The Flux VPC peering between production and data-enclave was removed -> currently the Flux VPC peering between production and data-enclave was removed
- deepseek_v4pro_gold300_210: type_marker: the local stub workaround is no longer needed -> decided to the local stub workaround is no longer needed
- deepseek_v4pro_gold300_218: type_marker: The Grove mobile app build 2.7.0 passed TestFlight review and is live in the App Store -> currently the Grove mobile app build 2.7.0 passed TestFlight review and is live in the App Store
- deepseek_v4pro_gold300_219: type_marker: The Nexus edge-cache warm-up was changed to preload the top 1000 product SKUs instead of 500 -> Going forward, the Nexus edge-cache warm-up was changed to preload the top 1000 product SKUs instead of 500
- deepseek_v4pro_gold300_222: type_marker: the old Jenkins server is being decommissioned next month -> currently the old Jenkins server is being decommissioned next month
- deepseek_v4pro_gold300_227: type_marker: The Drift document-parser EXIF stripping now also removes GPS location tags from video files -> Going forward, the Drift document-parser EXIF stripping now also removes GPS location tags from video files
- deepseek_v4pro_gold300_228: type_marker: The Cascade autoscaler minimum was reduced to 2 nodes per AZ from 3 to save costs in the staging environment -> decided to the Cascade autoscaler minimum was reduced to 2 nodes per AZ from 3 to save costs in the staging environment
- deepseek_v4pro_gold300_229: type_marker: The Ember push-notification bridge was migrated from FCM legacy HTTP to the newer FCM v1 HTTP API -> currently the Ember push-notification bridge was migrated from FCM legacy HTTP to the newer FCM v1 HTTP API
- deepseek_v4pro_gold300_235: type_marker: The Ridge rate-limiter per-tenant quota check now happens after the global allowlist, reversing the previous order -> Going forward, the Ridge rate-limiter per-tenant quota check now happens after the global allowlist, reversing the previous order

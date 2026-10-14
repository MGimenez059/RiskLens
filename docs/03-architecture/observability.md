# Observability specification

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

ADR-007 proposes structured local events. Hosted tracing is deferred until justified.

Event fields: event_id, run_id, revision, node_id, attempt, event_type, timestamp_utc, duration_ms, outcome, sanitized_error_code, input_artifact_hash and output_artifact_hash. Provider events additionally record provider, effective model_id, prompt_version, request correlation ID when available, token counts, usage_complete, estimated_cost, cost_currency and dated price_reference. Non-applicable fields are null with stage context.

Correlate analysis, tools, retrieval, review and finalization without logging raw rows, credentials, hidden model reasoning, full prompts or unbounded documents. Store human rationale and evidence-backed explanations, not chain-of-thought. Audit records, debug logs and graph checkpoints serve distinct purposes.

Measure run outcomes, node failures/retries, retrieval insufficiency, invalid-output rate, review state, stage latency and cost per valid result. Performance thresholds require OQ-008. Distinguish incomplete provider usage from a verified zero-cost deterministic run.

CT-011 defines the reproduction manifest. Deterministic replay compares canonical output excluding generated IDs/timestamps. AI audit uses recorded artifacts; another model invocation is a new attempt and may differ. Retention and exports require OQ-010. Public exports link actual commits and eval reports and exclude private artifacts.

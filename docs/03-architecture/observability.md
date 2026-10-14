# Observability specification

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

Applicability: M02 lineage/events; M03/M04 provider/tool/review extensions remain Proposed.

ADR-007 proposes structured local events. CT-019 is the M02 event/validation catalog; CT-011 defines its run manifest. No model event, cost field or checkpoint is required by M02. Hosted tracing is deferred until justified.

Event fields: event_id, run_id, revision, node_id, attempt, event_type, timestamp_utc, duration_ms, outcome, sanitized_error_code, input_artifact_hash and output_artifact_hash. Provider events additionally record provider, effective model_id, prompt_version, request correlation ID when available, token counts, usage_complete, estimated_cost, cost_currency and dated price_reference. Non-applicable fields are null with stage context.

Correlate analysis, tools, retrieval, review and finalization without logging raw rows, credentials, hidden model reasoning, full prompts or unbounded documents. Store human rationale and evidence-backed explanations, not chain-of-thought. Audit records, debug logs and graph checkpoints serve distinct purposes.

Measure run outcomes, node failures/retries, retrieval insufficiency, invalid-output rate, review state, stage latency and cost per valid result. CT-020 supplies Provisional Local Safety Limits. Measured performance thresholds remain the OQ-008 benchmark portion; AI budgets are separate later gates. Distinguish incomplete provider usage from a verified zero-cost deterministic run.

CT-011 defines the reproduction manifest. Deterministic replay compares canonical output excluding generated IDs/timestamps. AI audit uses recorded artifacts; another model invocation is a new attempt and may differ. Retention and exports require OQ-010. Public exports link actual commits and eval reports and exclude private artifacts.

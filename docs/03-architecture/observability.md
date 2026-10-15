# Observability specification

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

Applicability: M02 lineage/events; M03/M04 provider/tool/review extensions remain Proposed.

ADR-007 proposes structured local events. CT-019 is the M02 event/validation catalog; CT-011 defines its run manifest. No model event, cost field or checkpoint is required by M02. Hosted tracing is deferred until justified.

CT-019 is the canonical M02 event schema: event_id, run_id, revision, stage, attempt, event_type, timestamp_utc, duration_ms, outcome, code, input_hash and output_artifact_hash. Its types, nullability, enums and failure rules apply without alternate aliases. CT-011 stores the associated run manifest. No separate node_id, sanitized_error_code or input_artifact_hash fields are required for M02.

Proposed M03/M04 provider/tool/review event extensions may add effective provider/model/prompt identity, provider correlation IDs, usage completeness and dated cost provenance after their contracts are reviewed. They do not extend the active M02 schema implicitly or require a provider dependency.

Correlate analysis, tools, retrieval, review and finalization without logging raw rows, credentials, hidden model reasoning, full prompts or unbounded documents. Store human rationale and evidence-backed explanations, not chain-of-thought. Audit records, debug logs and graph checkpoints serve distinct purposes.

Measure run outcomes, node failures/retries, retrieval insufficiency, invalid-output rate, review state, stage latency and cost per valid result. CT-020 supplies Provisional Local Safety Limits. Measured performance thresholds remain the OQ-008 benchmark portion; AI budgets are separate later gates. Distinguish incomplete provider usage from a verified zero-cost deterministic run.

CT-011 defines the reproduction manifest. Deterministic replay compares CT-017 semantic output excluding generated IDs/timestamps. M02 retention and whole-state cleanup follow CT-018; later artifact retention/deletion remains OQ-010. AI audit uses recorded artifacts; another model invocation is a new attempt and may differ. Public exports link actual commits and eval reports and exclude private artifacts.

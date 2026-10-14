# Functional requirements

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

All records are product proposals. Priority P1 means required for v1, not implementation authorization. Description is the Behavior field below. Acceptance criteria are canonical in acceptance-criteria.md.

## FR-DQ-001: Import immutable synthetic snapshots
- Status: Proposed
- Priority: P1; target M02
- Rationale: Prevent ambiguous input provenance.
- Inputs: CSV bytes and manifest CT-001
- Outputs: Validated snapshot reference or import rejection
- Preconditions: Manifest declares synthetic data and supported schema.
- Description / behavior: Parse exact headers and types; hash input bytes; preserve source row references; never silently coerce or deduplicate.
- Failure conditions: Unsupported schema, invalid core field, duplicate identity, or invalid manifest rejects the snapshot.
- Acceptance criteria: AC-DQ-001

## FR-DQ-002: Report data quality defects
- Status: Proposed
- Priority: P1; target M02
- Rationale: Make invalid data actionable without misleading metrics.
- Inputs: Parsed rows and CT-002
- Outputs: CT-005 quality findings and validation status
- Preconditions: Import is readable; otherwise file-level finding only.
- Description / behavior: Evaluate structural, field, and cross-field constraints; collect bounded findings; block calculations on any core defect.
- Failure conditions: Unreadable file yields file-level rejection; no partial portfolio metrics.
- Acceptance criteria: AC-DQ-002

## FR-RISK-001: Compute deterministic portfolio metrics
- Status: Proposed
- Priority: P1; target M02
- Rationale: Provide authoritative values independent of AI.
- Inputs: Validated CT-001 snapshot and versioned calculation configuration
- Outputs: CT-004 PortfolioMetrics
- Preconditions: Snapshot passed core validation.
- Description / behavior: Apply BR-RISK-001/002/005; preserve denominators and unavailable reasons; never aggregate currencies.
- Failure conditions: Invalid configuration fails calculation; undefined default semantics yields unavailable default metric, not zero.
- Acceptance criteria: AC-RISK-001

## FR-RISK-002: Detect concentration and anomalies
- Status: Proposed
- Priority: P1; target M03
- Rationale: Identify inspectable risk signals rather than ungrounded model claims.
- Inputs: Metrics, snapshot, approved detector configuration
- Outputs: CT-006 RiskFinding list
- Preconditions: OQ-004 resolved and detector version fixed.
- Description / behavior: Evaluate borrower/segment concentration and configured field bounds; attach rule, observed value, threshold, and evidence.
- Failure conditions: Missing detector configuration marks detector unavailable and run partial; never infer thresholds.
- Acceptance criteria: AC-RISK-002

## FR-RISK-003: Compare portfolio snapshots
- Status: Proposed
- Priority: P1; target M03
- Rationale: Distinguish deterioration from unsupported trend claims.
- Inputs: Current and optional prior CT-001 snapshots, metric versions
- Outputs: CT-006 change findings and comparison status
- Preconditions: OQ-005 approved for configured comparison method.
- Description / behavior: Compare eligible earlier snapshot; preserve both denominators, dates, and composition deltas.
- Failure conditions: Missing/incompatible history yields unavailable comparison; no inferred trend.
- Acceptance criteria: AC-RISK-003

## FR-POL-001: Retrieve applicable policy evidence
- Status: Proposed
- Priority: P1; target M03
- Rationale: Ground policy references in a versioned corpus.
- Inputs: Finding/query, policy corpus version, as-of date and scope
- Outputs: CT-010 retrieval result
- Preconditions: Approved synthetic corpus and retrieval configuration available.
- Description / behavior: Filter by applicability/effective dates, retrieve versioned chunks, preserve citations and conflicting candidates.
- Failure conditions: Missing corpus or insufficient evidence returns unavailable/insufficient; provider failure is explicit.
- Acceptance criteria: AC-POL-001

## FR-POL-002: Evaluate curated policy rules
- Status: Proposed
- Priority: P1; target M03
- Rationale: Separate relevance from proof of violation.
- Inputs: Findings, CT-010 evidence, CT-009 curated rules
- Outputs: CT-007 PolicyFinding list
- Preconditions: Rule-to-source mapping has human approval.
- Description / behavior: Apply deterministic predicates only when rule applicability and evidence are established; surface conflicts for review.
- Failure conditions: Unknown rule, conflicting sources, missing input, or expired evidence yields indeterminate.
- Acceptance criteria: AC-POL-002

## FR-AI-001: Generate grounded executive insights
- Status: Proposed
- Priority: P1; target M03
- Rationale: Explain computed results without fabricating facts.
- Inputs: Metrics, findings, policy findings, evidence allowlist
- Outputs: CT-008 insights and recommendations
- Preconditions: Validated deterministic outputs available; model/prompt configuration fixed.
- Description / behavior: Request structured synthesis; validate schema, evidence IDs, numeric claim references, and prohibited actions before persistence.
- Failure conditions: Malformed/unsupported output or timeout discards candidate and preserves deterministic outputs with partial status.
- Acceptance criteria: AC-AI-001

## FR-AI-002: Answer questions about an existing run
- Status: Proposed
- Priority: P1; target M04
- Rationale: Offer bounded investigation with evidence.
- Inputs: Run ID, question, bounded history
- Outputs: CT-013 structured answer or abstention
- Preconditions: Readable run exists; no pending ownership mismatch.
- Description / behavior: Allow only read-only tools scoped to that run; cite metrics or policy evidence; refuse unsupported and credit decision requests.
- Failure conditions: Unknown run, tool failure, insufficient evidence, or budget exhaustion produces explicit abstention/error.
- Acceptance criteria: AC-AI-002

## FR-AI-003: Record human review
- Status: Proposed
- Priority: P1; target M04
- Rationale: Make high-impact recommendations inspectable and accountable.
- Inputs: Review request, reviewer identity, run revision, decision
- Outputs: CT-012 HumanReview and updated visibility
- Preconditions: Run has pending review; reviewer action originates from UI, not model.
- Description / behavior: Persist approval/rejection with rationale; compare expected revision; retain original evidence and text.
- Failure conditions: Stale revision, duplicate conflicting decision, or persistence failure leaves run pending and reports conflict.
- Acceptance criteria: AC-AI-003

## FR-UI-001: Display analysis status and deterministic results
- Status: Proposed
- Priority: P1; target M02
- Rationale: Provide a usable first slice without AI dependency.
- Inputs: Run projection, metrics and validation findings
- Outputs: Dashboard view
- Preconditions: Run record exists, including rejected imports.
- Description / behavior: Show as-of date, currency, denominators, unavailable reasons, source links, and status; never show rejection as success.
- Failure conditions: Unavailable persistence shows error; stale projections display run revision.
- Acceptance criteria: AC-UI-001

## FR-UI-002: Navigate evidence and review recommendations
- Status: Proposed
- Priority: P1; target M04
- Rationale: Connect interpretation to source and human action.
- Inputs: Insight/finding/recommendation ID and run revision
- Outputs: Evidence detail and review interaction
- Preconditions: Objects belong to displayed run.
- Description / behavior: Resolve source location and policy version; label pending/rejected recommendations; expose review action only for eligible state.
- Failure conditions: Missing evidence blocks claim display as supported; review conflicts are visible.
- Acceptance criteria: AC-UI-002

## FR-OBS-001: Trace analysis runs and model costs
- Status: Proposed
- Priority: P1; target M02
- Rationale: Enable reproducibility and audit.
- Inputs: Input hashes, configuration, execution events and provider usage
- Outputs: CT-011 run manifest and structured events
- Preconditions: Writable local persistence available.
- Description / behavior: Record revisions, versions, node outcomes, attempts, durations, usage, and cost provenance without raw sensitive payloads.
- Failure conditions: Persistence failure prevents successful finalization; unknown usage/cost is unknown, never zero.
- Acceptance criteria: AC-OBS-001

## FR-OBS-002: Resume safely after interruption
- Status: Proposed
- Priority: P1; target M03
- Rationale: Avoid duplicated outputs and lost review state.
- Inputs: Run ID, persisted checkpoint, expected revision
- Outputs: Resumed run or explicit non-resumable error
- Preconditions: Compatible checkpoint schema/config and durable store.
- Description / behavior: Resume from committed node boundaries; use idempotency keys; preserve review interrupts across restarts.
- Failure conditions: Incompatible schema, missing checkpoint, or concurrent resume is rejected without overwriting the run.
- Acceptance criteria: AC-OBS-002

# Functional requirements

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

All records are Proposed active-v1 requirements with explicit Applicability. P1 means required at its listed milestone, not a prerequisite for earlier slices. No excluded finance feature is required for release. Description is the Behavior field below. Acceptance criteria are canonical in acceptance-criteria.md.

## FR-DQ-001: Import immutable synthetic snapshots
- Status: Proposed
- Priority: P1
- Applicability: M02
- Rationale: Prevent ambiguous input provenance.
- Inputs: CSV bytes and manifest CT-001
- Outputs: CT-015 Import/Validation Result and valid snapshot reference only when eligible
- Preconditions: Bounded configured import path is available. The manifest may be malformed or invalid; validation must determine that rather than requiring a prevalidated manifest.
- Description / behavior: Parse CT-001/002 exactly; enforce global snapshot_id ownership and CT-020; return CT-015 valid/rejected/conflict/limit outcomes. Hash complete bounded bundle bytes under CT-017. No filtering, coercion, imputation or deduplication.
- Failure conditions: Unreadable/schema/core-invalid input rejects the complete snapshot. Reused identity/content or key conflicts preserve the existing result. Resource overflow produces limit_failed. No outcome publishes partial-population metrics.
- Acceptance criteria: AC-DQ-001

## FR-DQ-002: Report data quality defects
- Status: Proposed
- Priority: P1
- Applicability: M02
- Rationale: Make invalid data actionable without misleading metrics.
- Inputs: Parsed rows and CT-002
- Outputs: CT-005 quality findings and validation status
- Preconditions: Import is readable; otherwise file-level finding only.
- Description / behavior: Evaluate CT-019 structural/field/invariant catalog, collect bounded CT-005 diagnostics with explicit completeness, and block metrics on contract defects. Null segment and empty snapshot are valid without invented findings.
- Failure conditions: Unreadable file yields file-level rejection; no partial portfolio metrics.
- Acceptance criteria: AC-DQ-002

## FR-RISK-001: Compute deterministic portfolio metrics
- Status: Proposed
- Priority: P1
- Applicability: M02
- Rationale: Provide authoritative values independent of AI.
- Inputs: Validated CT-001 snapshot and versioned calculation configuration
- Outputs: CT-004 PortfolioMetrics
- Preconditions: Snapshot passed core validation.
- Description / behavior: Apply BR-RISK-001/002/003/005 and CT-017 to USD exposure, distinct count/exposure delinquency and raw group exposure/shares. Preserve exact operands and denominator-specific reasons. No alert threshold is needed.
- Failure conditions: Invalid configuration/arithmetic fails calculation. Zero denominators make only the affected ratio unavailable. Active-v1 output contains no metric for excluded financial concepts.
- Acceptance criteria: AC-RISK-001

## FR-RISK-002: Detect concentration and anomalies
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Identify inspectable risk signals rather than ungrounded model claims.
- Inputs: CT-004 raw metrics, snapshot and approved detector configuration; no M02 alert threshold
- Outputs: CT-006 RiskFinding list
- Preconditions: OQ-004 resolved and detector version fixed.
- Description / behavior: Evaluate alerts over already-computed raw borrower/segment shares and configured valid-value anomaly bounds. Preserve exact observed operands, configured threshold/operator and evidence. Raw shares remain FR-RISK-001.
- Failure conditions: Missing detector configuration marks detector unavailable and run partial; never infer thresholds.
- Acceptance criteria: AC-RISK-002

## FR-RISK-003: Compare portfolio snapshots
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Distinguish deterioration from unsupported trend claims.
- Inputs: Current and optional prior CT-001 snapshots, metric versions
- Outputs: CT-006 change findings and comparison status
- Preconditions: OQ-005 approved for configured comparison method.
- Description / behavior: Compare eligible earlier snapshot; preserve both denominators, dates, and composition deltas.
- Failure conditions: Missing/incompatible history yields unavailable comparison; no inferred trend.
- Acceptance criteria: AC-RISK-003

## FR-POL-001: Retrieve applicable policy evidence
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Ground policy references in a versioned corpus.
- Inputs: Finding/query, policy corpus version, as-of date and scope
- Outputs: CT-010 retrieval result
- Preconditions: Approved synthetic corpus and retrieval configuration available.
- Description / behavior: Filter by applicability/effective dates, retrieve versioned chunks, preserve citations and conflicting candidates.
- Failure conditions: Missing corpus or insufficient evidence returns unavailable/insufficient; provider failure is explicit.
- Acceptance criteria: AC-POL-001

## FR-POL-002: Evaluate curated policy rules
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Separate relevance from proof of violation.
- Inputs: Findings, CT-010 evidence, CT-009 curated rules
- Outputs: CT-007 PolicyFinding list
- Preconditions: Rule-to-source mapping has human approval.
- Description / behavior: Apply deterministic predicates only when rule applicability and evidence are established; keep conflicts indeterminate and correct/curate the corpus outside the run; no generic runtime policy-conflict review.
- Failure conditions: Unknown rule, conflicting sources, missing input, or expired evidence yields indeterminate.
- Acceptance criteria: AC-POL-002

## FR-AI-001: Generate grounded executive insights
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Explain computed results without fabricating facts.
- Inputs: Metrics, findings, policy findings, evidence allowlist
- Outputs: CT-008 observations, explanations and evidence inspection suggestions only
- Preconditions: Validated deterministic outputs available; model/prompt configuration fixed.
- Description / behavior: Request structured observations/explanations/inspection suggestions; enforce empty recommendations in M03. Validate evidence, schema, numeric references and action boundaries before persistence. No high-impact output or human-review gate in M03.
- Failure conditions: Malformed/unsupported output or timeout discards candidate and preserves deterministic outputs with partial status.
- Acceptance criteria: AC-AI-001

## FR-AI-002: Answer questions about an existing run
- Status: Proposed
- Priority: P1
- Applicability: M04
- Rationale: Offer bounded investigation with evidence.
- Inputs: Run ID, question, bounded history
- Outputs: CT-013 structured answer or abstention
- Preconditions: Readable run exists; no pending ownership mismatch.
- Description / behavior: Allow only read-only tools scoped to that run; cite metrics or policy evidence; refuse unsupported and credit decision requests.
- Failure conditions: Unknown run, tool failure, insufficient evidence, or budget exhaustion produces explicit abstention/error.
- Acceptance criteria: AC-AI-002

## FR-AI-003: Record human review
- Status: Proposed
- Priority: P1
- Applicability: M04
- Rationale: Make high-impact recommendations inspectable and accountable.
- Inputs: Review request, reviewer identity, run revision, decision
- Outputs: CT-012 HumanReview and updated visibility
- Preconditions: M04 recommendation workflow is ready under OQ-009/012; run has pending review and action originates from UI. M03 emits no such recommendations.
- Description / behavior: M04 may generate high-impact recommendations only with functional review. Persist human approval/rejection with rationale and revision checks; retain metrics/evidence. Policy conflicts are not recommendation review targets.
- Failure conditions: Stale revision, duplicate conflicting decision, or persistence failure leaves run pending and reports conflict.
- Acceptance criteria: AC-AI-003

## FR-UI-001: Display analysis status and deterministic results
- Status: Proposed
- Priority: P1
- Applicability: M02
- Rationale: Provide a usable first slice without AI dependency.
- Inputs: Run projection, metrics and validation findings
- Outputs: Dashboard view
- Preconditions: Run record exists, including rejected imports.
- Description / behavior: Show M02 valid/rejected/conflict/limit outcomes and created/running/succeeded/failed analysis state, raw metrics, date/USD, denominators and availability. Empty is a snapshot property. No pending-review or AI UI prerequisite.
- Failure conditions: Unavailable persistence shows error; stale projections display run revision.
- Acceptance criteria: AC-UI-001

## FR-UI-002: Navigate evidence and review recommendations
- Status: Proposed
- Priority: P1
- Applicability: M04
- Rationale: Connect interpretation to source and human action.
- Inputs: Insight/finding/recommendation ID and run revision
- Outputs: Evidence detail and review interaction
- Preconditions: Objects belong to displayed run.
- Description / behavior: Resolve source location and policy version; label pending/rejected recommendations; expose review action only for eligible state.
- Failure conditions: Missing evidence blocks claim display as supported; review conflicts are visible.
- Acceptance criteria: AC-UI-002

## FR-OBS-001: Trace analysis runs and model costs
- Status: Proposed
- Priority: P1
- Applicability: M02
- Rationale: Enable reproducibility and audit.
- Inputs: Input hashes, configuration, execution events and provider usage
- Outputs: CT-011 run manifest and structured events
- Preconditions: Writable local persistence available.
- Description / behavior: Record M02 input/config/rule/code hashes, global snapshot ownership, typed CT-019 events and run outcomes without payload/secrets. M03+ records AI usage/cost only when used; no M02 provider call or checkpoint required.
- Failure conditions: Persistence failure prevents successful finalization; unknown usage/cost is unknown, never zero.
- Acceptance criteria: AC-OBS-001

## FR-OBS-002: Resume safely after interruption
- Status: Proposed
- Priority: P1
- Applicability: M03
- Rationale: Avoid duplicated graph outputs in M03 and lost review state only in enabled M04 workflows.
- Inputs: Run ID, persisted checkpoint, expected revision
- Outputs: Resumed run or explicit non-resumable error
- Preconditions: Compatible checkpoint schema/config and durable store.
- Description / behavior: M03 graph resumes compatible committed node boundaries with idempotency keys. Preserve human-review interrupts only in the M04 review variant; no review interrupt or reviewer is required for M03 readiness.
- Failure conditions: Incompatible schema, missing checkpoint, or concurrent resume is rejected without overwriting the run.
- Acceptance criteria: AC-OBS-002

## FR-DQ-003: Bound import resources and diagnostic collection
- Status: Proposed
- Applicability: M02
- Priority: P1
- Rationale / purpose: prevent unbounded local parsing without changing the population being analyzed.
- Inputs / fields: CT-001 bundle bytes and CT-020 effective limits/version/hash.
- Outputs: CT-015 typed result, CT-005 findings and CT-019 events.
- Preconditions: registered parser configuration; exact provisional values require reviewed profile acceptance.
- Behavior / invariants: enforce byte/row/field/numeric caps; no truncated population metrics. Cap diagnostics with report_complete=false after defects are found. Effective limits are persisted through CT-016/011.
- Failure conditions: invalid configuration is configuration_invalid; input cap overflow is limit_failed/resource_limit. Null segment/empty data do not cause failure.
- Acceptance criteria: AC-DQ-003.
- Edge cases: exact bounds/bound+1, multibyte fields, header excluded, incomplete hash, capped diagnostics and aggregate sums longer than input tokens.
- Traceability: BR-DQ-004; CT-015/016/019/020; ADR-002/003; planned test_FR_DQ_003_parser_limits; EVAL-DQ-003.

## FR-OBS-003: Publish local results and replay safely after restart
- Status: Proposed
- Applicability: M02
- Priority: P1
- Rationale / purpose: make deterministic runs durable without graph checkpoints.
- Inputs / fields: CT-016 request/config, CT-015 result, complete artifact bytes, expected revision and key bindings.
- Outputs: CT-018 committed publication and CT-011 manifest; readable persisted run and metrics.
- Preconditions: writable confined local state, SQLite and one writer; configured USD M02 mode.
- Behavior / invariants: publish verified files before transactional metadata references; enforce global snapshot ownership and separate import/analysis bindings; restart reads committed records; same analysis fingerprint/key returns prior result without duplication. New keys create new runs and run-scoped evidence refs without mutating old runs. Retain until explicit whole-state operator cleanup.
- Failure conditions: stale revision/reused fingerprint conflicts, file/SQLite failure, missing or corrupt referenced artifact. Never claim durable success before commit; use explicit non-durable error if the store cannot record failure.
- Acceptance criteria: AC-OBS-003.
- Edge cases: crash before/after publish/commit, lost UI response, orphan file, global ID reused by another portfolio, valid empty run and explicit cleanup.
- Traceability: CT-015/016/017/018/019; ADR-003/007/008; planned test_FR_OBS_003_publication_and_restart; NFR-REL-002/SEC-002. Graph resume remains FR-OBS-002 at M03.

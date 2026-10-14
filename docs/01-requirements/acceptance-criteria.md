# Acceptance criteria

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

These criteria are proposed binary gates, not claims of execution.

## AC-DQ-001: FR-DQ-001
Given a valid synthetic manifest and CSV, import preserves byte hashes and row identities. Reimport with the same idempotency key returns the same snapshot. Changing bytes under the same key is rejected. Unsupported schema, duplicate loan IDs, or malformed numeric/date values reject the complete snapshot.

## AC-DQ-002: FR-DQ-002
Given missing required values, duplicates, negative principal, or an origination date after as_of, produce findings identifying rule and source row/field. No metrics are calculated. A header-only valid CSV is an empty snapshot, not a corrupt file.

## AC-RISK-001: FR-RISK-001
For two open loans with outstanding principal 100.00 and 300.00 and DPD 0 and 5, total exposure is 400.00, count delinquency rate is 0.5, and exposure delinquency rate is 0.75. These are test values, not risk thresholds. Empty and zero-exposure populations produce null ratios with reasons. Repeated identical input/config yields identical canonical metric payloads. Undefined default returns unavailable.

## AC-RISK-002: FR-RISK-002
Given an approved test configuration and exposures above its segment/borrower threshold, emit the exact configured finding with observed numerator, denominator, threshold and evidence. Boundary equality follows the configured operator. Missing configuration never produces a healthy claim.

## AC-RISK-003: FR-RISK-003
Given eligible earlier and current snapshots with a positive delinquency-rate difference, emit the configured deterioration finding citing both metric records and composition change. A single snapshot, same-date snapshot, currency mismatch, or metric version mismatch cannot yield a trend.

## AC-POL-001: FR-POL-001
A curated query retrieves the labeled applicable policy chunk with document hash, version, section and offsets. Expired/out-of-scope chunks cannot support a claim. Empty corpus, insufficient results and contradictory candidates are distinct states; all returned citations resolve.

## AC-POL-002: FR-POL-002
Given a reviewed predicate and applicable source evidence, a violating fixture yields violation with predicate inputs and source citation. Missing input, missing evidence, or conflicting applicable sources yields indeterminate. Similar wording alone never yields violation or compliance.

## AC-AI-001: FR-AI-001
For valid fixtures every factual claim references allowed evidence. Numeric statements use metric references rendered by deterministic code. Fabricated citation IDs, policy claims without sources, malformed output and prohibited credit decisions fail validation. Timeout retains existing metrics and records partial status.

## AC-AI-002: FR-AI-002
A question about a known metric resolves its run-scoped reference. Requests for another run, arbitrary SQL/shell, or loan approval are refused. Missing evidence returns abstained with reason; tool failure cannot become an unsupported answer.

## AC-AI-003: FR-AI-003
A high-impact recommendation remains pending across process restart. An authorized local human action against the current revision records decision and rationale exactly once. A stale or contradictory replay cannot change the accepted record. Rejection never modifies original metrics.

## AC-UI-001: FR-UI-001
Display the rejected, empty, succeeded, partial, failed and pending_review fixtures with their distinct states. Currency, date, denominators and unavailable reasons remain visible. UI numeric text comes from stored metrics, not generated prose.

## AC-UI-002: FR-UI-002
Following every displayed supported claim resolves evidence from that run. Pending and rejected recommendations are labeled and never shown as approved. A stale review action displays a conflict and refreshes the current revision.

## AC-OBS-001: FR-OBS-001
A run manifest links input, rules, contracts, code, prompts, model configuration and retrieval index when used. Node events share run ID. Missing token or price data is unknown. Injected persistence failure prevents success and logs a safe error without raw input or secrets.

## AC-OBS-002: FR-OBS-002
Crash before and after each committed node and resume. Durable results and reviews appear once. Unsupported checkpoint version, stale revision and concurrent resume fail safely. Provider calls may repeat after ambiguous failure, but duplicate output commits are forbidden.

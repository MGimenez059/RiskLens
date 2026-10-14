# Acceptance criteria

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

These criteria are proposed binary gates, not claims of execution.

## AC-DQ-001: FR-DQ-001
Status: Proposed
Applicability: M02

A valid USD synthetic bundle produces the globally unique snapshot with exactly one portfolio owner and verified byte/semantic hashes. Repeating the import key and full bundle/parser fingerprint returns the existing semantic outcome. Repeating the analysis key/config returns the same run; different content/config under a bound key returns conflict. Global snapshot_id reuse by a different portfolio conflicts. Schema/header ambiguity, duplicate JSON keys, malformed values or invalid core invariants reject the complete snapshot; no filtering or deduplication.

## AC-DQ-002: FR-DQ-002
Status: Proposed
Applicability: M02

Missing core fields, duplicate loan IDs, invalid optional non-null segment, negative monetary/DPD values, future origination date, invalid closed-loan invariant, unsupported USD currency or source hash mismatch yield cataloged blocking diagnostics and no metrics. Null segment is accepted with an unspecified group and no invented finding. Header-only valid CSV is a valid empty snapshot. Unreadable manifest yields application-assigned result/report identities. Diagnostic collection states whether the report is complete.

## AC-RISK-001: FR-RISK-001
Status: Proposed
Applicability: M02

For two open loans with principal 100.00/300.00 and DPD 0/5: total exposure 400.00, count operands 1/2 with value 0.5000, exposure operands 300.00/400.00 with value 0.7500. These are hand-checkable fixtures, not risk thresholds.
For three eligible loans with one delinquent, preserve exact count operands 1 and 3 and serialize 0.3333. Quantization fixtures 1/32 and 3/32 yield 0.0312 and 0.0938 using half-even; exact 1/3 remains distinct from rounded 0.3333 in comparisons. No threshold is selected.
Two open zero-principal loans, one delinquent: count rate available 1/2 = 0.5000; exposure rate unavailable with 0.00/0.00 and zero_denominator. No eligible open loans: count/exposure rates unavailable with no_eligible_population. Empty snapshot: counts/exposure zero, concentration empty; closed valid loans do not enter the open denominator.
Raw borrower/segment group exposures sum to total independently per dimension; exact group operands determine serialized shares. Null segment uses its distinct unspecified group. Zero total makes group shares unavailable without invalidating the snapshot. No alert is emitted by metrics. Canonical semantic output hashes are repeatable while raw byte hashes and run lineage remain distinct.

## AC-RISK-002: FR-RISK-002
Status: Proposed
Applicability: M03

Given an approved M03 detector configuration, concentration alerts compare authoritative group operands to its exact configured threshold/operator, and anomaly predicates use valid data. Equality follows the configured operator. Missing config is explicit detector unavailability, never a healthy claim. M02 raw shares are not blocked by missing alert configuration.

## AC-RISK-003: FR-RISK-003
Status: Proposed
Applicability: M03

Given eligible earlier and current snapshots with a positive delinquency-rate difference, emit the configured deterioration finding citing both metric records and composition change. A single snapshot, same-date snapshot, currency mismatch, or metric version mismatch cannot yield a trend.

## AC-POL-001: FR-POL-001
Status: Proposed
Applicability: M03

A curated query retrieves the labeled applicable policy chunk with document hash, version, section and offsets. Expired/out-of-scope chunks cannot support a claim. Empty corpus, insufficient results and contradictory candidates are distinct states; all returned citations resolve.

## AC-POL-002: FR-POL-002
Status: Proposed
Applicability: M03

Given a reviewed predicate and applicable source evidence, a violating fixture yields violation with predicate inputs and source citation. Missing input, missing evidence, or conflicting applicable sources yields indeterminate. Similar wording alone never yields violation or compliance.

## AC-AI-001: FR-AI-001
Status: Proposed
Applicability: M03

M03 accepts CT-008 observations/explanations/evidence inspection suggestions only, with recommendations empty. Every factual claim resolves allowed evidence; numeric facts use authoritative metric refs. Business-action/high-impact suggestions, fabricated citations, unsupported policy claims and malformed output are discarded, leaving metrics intact and stage partial. No human-review branch or reviewer identity is needed to accept M03 synthesis.

## AC-AI-002: FR-AI-002
Status: Proposed
Applicability: M04

A question about a known metric resolves its run-scoped reference. Requests for another run, arbitrary SQL/shell, or loan approval are refused. Missing evidence returns abstained with reason; tool failure cannot become an unsupported answer.

## AC-AI-003: FR-AI-003
Status: Proposed
Applicability: M04

In M04 only, high-impact recommendations remain pending across restart and cannot be emitted as approved by a model. Valid local human action against current revision records decision/rationale once; stale or contradictory replay conflicts. Metrics remain unchanged. Policy conflicts remain indeterminate and are corrected outside the run, not approved through recommendation review.

## AC-UI-001: FR-UI-001
Status: Proposed
Applicability: M02

M02 dashboard displays valid/rejected/conflict/limit import outcomes plus created/running/succeeded/failed analysis states. A valid empty snapshot appears as an empty population, not a separate run status. Show USD/as_of, counts, exposure, raw groups, exact numerator/denominator, quantized display and unavailable reasons from stored data. No model, policy, pending_review, high-impact recommendation or graph checkpoint is needed for this criterion. Later partial/review UI is tested at M03/M04.

## AC-UI-002: FR-UI-002
Status: Proposed
Applicability: M04

Following every displayed supported claim resolves evidence from that run. Pending and rejected recommendations are labeled and never shown as approved. A stale review action displays a conflict and refreshes the current revision.

## AC-OBS-001: FR-OBS-001
Status: Proposed
Applicability: M02 core; M03+ applicable AI fields

M02 manifest links input bundle/CSV hashes when complete, global snapshot/portfolio ownership, parser/config/arithmetic/rule/contracts/code versions and CT-019 events. Source/report links resolve within the run. Effective limits and stage selections are recorded; model/prompt/index/usage fields are absent in M02 mode. Persistence failure prevents a durable success claim and emits safe error without payload/secrets. Later actual AI usage remains unknown when unreported, never fabricated zero.

## AC-OBS-002: FR-OBS-002
Status: Proposed
Applicability: M03 graph; M04 review

For enabled M03 graph nodes, crash before and after committed outputs/checkpoints and resume without duplicate durable results. Unsupported checkpoint version, stale revision and concurrent resume fail safely. Provider calls may repeat after ambiguous failure, but duplicate output commits are forbidden. Review interruption/decision replay is tested only in the M04 variant; it does not gate M03 or M02.

## AC-DQ-003: FR-DQ-003
Status: Proposed
Applicability: M02

At every effective CT-020 byte/row/field/numeric bound accept otherwise valid input at the bound and return resource_limit/limit_failed at bound+1. Count UTF-8 field bytes and exclude header from row count. Do not truncate data or produce metrics from scanned rows. At diagnostic cap after invalid records, return rejected/report_complete=false; a full scan with fewer findings reports true. Early unreadable/limit input may lack a complete hash, but never claims a truncated hash as full. Reject invalid/nonpositive configuration. Output monetary sums may exceed one input token's length without being truncated.

## AC-OBS-003: FR-OBS-003
Status: Proposed
Applicability: M02

Inject interruption before artifact publish, after publish/before metadata transaction, and after commit/before UI response. Restart exposes only verified committed records; orphans are ignored; identical analysis replay returns the existing run without duplicate snapshot/result. Reusing global snapshot_id with a different owner/content conflicts. Missing/corrupt referenced file returns integrity_error without overwriting the prior result. No graph checkpoint is involved. Explicit stopped-application cleanup of the entire confined state root removes metadata/artifacts together; subsequent restart is empty. No automatic expiry or per-run deletion UI is required.

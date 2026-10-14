# Data contracts

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

## Contract conventions
These are written contracts, not implemented Pydantic models. Each contract version is 1.0. Unknown fields are rejected at ingress. Required fields cannot be omitted. `?` explicitly permits JSON null; other fields are non-null. CSV uses an empty cell only for a nullable field. Missing required headers reject the file. No whitespace trimming or coercion unless explicitly specified below.

| Type | Encoding, valid range and units | Invalid behavior |
|---|---|---|
| Id | ASCII string matching `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`; case-sensitive opaque identity. | Reject boundary object; never reinterpret as path. |
| Text | Nonempty UTF-8 text; size cap is approved runtime configuration under OQ-008. | Reject object on empty or configured size overflow. |
| Date | Exact YYYY-MM-DD Gregorian calendar date. | Reject impossible or noncanonical dates. |
| Timestamp | RFC3339 timestamp with UTC Z suffix. | Reject naive/local timestamps. |
| Hash | 64 lowercase hexadecimal characters, SHA-256 of stated bytes. | Reject invalid encoding or integrity mismatch. |
| Amount | Decimal string, nonnegative, at most 2 fractional digits; no exponent, NaN, infinity or grouping separators. Snapshot currency units. | Reject; no binary float conversion. |
| Ratio | Decimal string derived from exact numerator/denominator; 0 to 1 for shares/rates. | Reject inconsistent ratio or range. |
| Count | Integer >= 0; booleans not accepted as integers. | Reject invalid value. |
| Version | Nonempty immutable version identifier tied to a registry/hash. | Reject unknown schema; record exact other versions. |
| RefList | Nonempty list of EvidenceRef IDs, unique within list. | Reject unknown, duplicated or cross-run evidence. |

Every contract below inherits these constraints and failure behavior. Semicolon-separated field declarations apply individually to each named field. Arrays may be empty unless marked nonempty. Contract failures from inputs produce DQ/rejection; failures from generated output discard the candidate and mark its stage failed. No future implementation may silently relax these rules.

## CT-001: PortfolioSnapshot and import manifest
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| schema_version | Version / no | Exactly 1.0 for this contract. |
| portfolio_id; snapshot_id | Id / no | Portfolio and immutable observation identities. |
| portfolio_name | Text / no | Analyst-facing synthetic portfolio label. |
| as_of | Date / no | Measurement date for all rows. |
| currency | string / no | Three uppercase letters from approved single-currency configuration, OQ-001; proposed precision is 2. |
| synthetic | boolean / no | Must be true; declaration is supplemented by controlled fixture provenance, not a PII detector guarantee. |
| generator_version; seed | Version; integer / no | Synthetic generator provenance; integer seed >= 0. |
| source_sha256 | Hash / no | Expected hash of exact CSV bytes, verified on import. |
| loans | list[CT-002] / no | Parsed rows; empty is valid if headers exist. |

Import wire format is UTF-8 CSV with comma separator, one header row and standard quoted fields, plus UTF-8 JSON manifest containing all fields above except loans. CSV headers exactly match CT-002 fields. Duplicate/extra headers reject. The application import request also requires idempotency_key: Id. Same key and identical CSV/manifest bytes return the existing import result; changed bytes under the same key conflict. snapshot_id reused with different content or metadata is a conflict. Application computes canonical payload hash separately from source byte hash. The run input_hash identifies an immutable bundle containing both original CSV and manifest; source_sha256 specifically identifies CSV bytes. Invalid core rows reject the complete snapshot, BR-DQ-002. File size and row caps require OQ-008 before parser implementation.

## CT-002: Loan observation
| Field | Type / nullable | Meaning, units and constraints |
|---|---|---|
| loan_id | Id / no | Unique within snapshot; stable across snapshots when obligation persists. |
| customer_id | Id / no | Synthetic BorrowerRef; multiple loans may share it. |
| original_principal | Amount / no | Original funded amount, currency units, > 0. Replaces ambiguous loan_amount. |
| outstanding_principal | Amount / no | Remaining principal, 0 through original_principal inclusive. Exposure source. Capitalization products outside scope. |
| days_past_due | Count / no | Reported calendar days overdue at as_of. No arbitrary upper credit threshold. |
| loan_status | enum / no | open or closed only; closed requires outstanding_principal = 0 and days_past_due = 0. Default is not a status in this contract. |
| origination_date | Date / no | Must be <= snapshot as_of. |
| segment | Id / yes | Synthetic grouping label; null maps to a distinct unspecified group, not a fabricated segment. |

`income`, `installment`, `dti`, and `credit_score` are deliberately excluded until OQ-003 resolves meaning, period, debt coverage and score scale. `loan_amount` is replaced with original_principal and outstanding_principal. `customer_id` remains a reference rather than a borrower profile. Adding excluded fields requires a contract version and CR.

## CT-003: EvidenceRef
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| evidence_id; run_id | Id / no | Unique evidence identity and owning run. |
| kind | enum / no | snapshot, source_row, metric, comparison, policy_chunk, rule_evaluation, validation_report, retrieval_report. |
| artifact_hash | Hash / no | Immutable referenced artifact digest. |
| locator | tagged object / no | snapshot: snapshot_id Id; source_row: snapshot_id Id, row_number integer >= 2, field Id?; metric: metrics_id Id, metric_key Text; comparison: comparison_id Id; policy_chunk: chunk_id Id, policy_version Version, section Text, start_offset Count, end_offset Count > start; rule_evaluation: evaluation_id Id; validation_report: report_id Id; retrieval_report: retrieval_id Id. |

Offsets count Unicode code points in canonical normalized policy text, interval [start,end). Hash identifies that text. Source rows refer to physical CSV record identity as assigned by the parser, including quoted multiline records; row_number is record ordinal plus header, not byte line number. Evidence must resolve to stored immutable artifacts, not arbitrary filesystem paths. Cyclic evidence links are invalid.

## CT-004: PortfolioMetrics
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| metrics_id; run_id; snapshot_id | Id / no | Result identity and provenance. |
| calculation_version; rule_config_version | Version / no | Exact formula and configuration versions. |
| currency; as_of | string; Date / no | Must match CT-001. |
| loan_count; open_loan_count | Count / no | All valid loans; eligible open population. open <= total. |
| total_exposure | Amount / no | BR-RISK-001 sum. |
| delinquency_count_rate; delinquency_exposure_rate; default_rate | MetricValue / no | Defined below; default unavailable until OQ-002. |
| concentration | list[GroupShare] / no | GroupShare: dimension enum(segment,borrower), group_id Id?, share MetricValue. Null only for unspecified segment. One row per group/dimension. |
| evidence_ids | RefList / no | Snapshot-derived metric provenance. |

MetricValue fields: `status` enum(available,unavailable); `value` Ratio?; `numerator` decimal-string? >= 0; `denominator` decimal-string? >= 0; `unit` enum(count_ratio,exposure_ratio); `reason` enum(zero_denominator,definition_pending,no_eligible_population)?; `rule_id` Id. Available requires value and operands, denominator > 0, reason null. Unavailable requires value null and reason; operands may be present when known. No fabricated zero for missing information. Store exact operands; rendering follows BR-RISK-005. GroupShare uses exposure_ratio.

## Shared finding envelope for CT-005/006/007
`finding_id`, `run_id`: Id; `rule_id`: Id; `rule_version`: Version; `severity`: enum(info,warning,error); `summary`: Text; `evidence_ids`: RefList. All non-null. Severity derives from approved rule configuration, never LLM choice. Each child adds the following fields.

## CT-005: DataQualityFinding
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| scope | enum / no | file, row, field. |
| row_number | integer >= 2 / yes | Null only for file defects. |
| field | Id / yes | Required for field scope, otherwise null. |
| code | enum / no | schema_invalid, missing_required, duplicate_key, invalid_value, invariant_failed, unreadable_input. |
| blocking | boolean / no | True for all core/structural defects in v1; optional-null segment needs no defect. |

For an unreadable file, evidence is a validation_report artifact with a content hash and self-contained failure record. It must not point back to the finding cyclically. A validation report contains report_id, input_hash, rule_id, error_code and sanitized_message; all required and typed by the shared conventions. Do not persist raw invalid values in logs.

## CT-006: RiskFinding
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| category | enum / no | concentration, anomaly, deterioration. |
| observed_value; threshold | decimal-string / no | Finite values; signed values permitted for rate differences. Same unit as configuration. |
| operator | enum / no | gt, gte, lt, lte; exact decimal comparison. |
| unit | enum / no | currency, ratio, ratio_difference, days, count. |
| scope_ref | Id / no | Group, loan, or comparison artifact identity. |

No finding is emitted for an unavailable detector; stage status records absence. A missing finding is not proof of health.

## CT-007: PolicyFinding
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| policy_id; policy_rule_id | Id / yes | Null only when no applicable policy/rule exists; non-null for violation/compliant. |
| policy_version | Version / yes | Required if policy_id set. |
| outcome | enum / no | violation, compliant, indeterminate. |
| reason | enum / yes | Required for indeterminate: no_policy, insufficient_evidence, conflicting_context, missing_input, unsupported_rule. Otherwise null. |
| predicate_evidence_ids | list[Id] / no | Nonempty for violation/compliant; evaluated inputs and applicable source required. |

The shared evidence envelope uses retrieval_report evidence for indeterminate outcomes. It must never imply that such an artifact is policy support. A rule_evaluation artifact contains evaluation_id, rule_id, rule_version, named typed input values, operator, threshold and boolean predicate_result; it references source evidence, never its resulting finding. All fields are required and use the shared conventions plus the predicate types in CT-009.

## CT-008: ExecutiveInsight and Recommendation
ExecutiveInsight fields: `insight_id`, `run_id` Id; `title` Text; `claims` nonempty list[Claim]; `finding_ids` list[Id]; `recommendations` list[Recommendation]. All non-null.
Claim fields: `claim_id` Id; `kind` enum(interpretation,metric_reference,policy_reference); `text` Text; `evidence_ids` RefList; `metric_ref` Id? required for metric_reference, otherwise null. Metric reference resolves CT-003 metric evidence. Numeric facts are rendered from references by code, not authored as factual literals in text. Policy references require applicable policy_chunk evidence. Free text cannot override referenced values.
Recommendation fields: `recommendation_id`, `run_id` Id; `action` Text; `basis_claim_ids` nonempty list[Id]; `impact` enum(high,low); `review_status` enum(not_required,pending,approved,rejected); `evidence_ids` RefList. All non-null. Application assigns impact and status under BR-POL-004; LLM cannot self-approve. Low impact is limited to inspecting evidence or correcting synthetic input; all other actions default high.

## CT-009: CreditPolicy and PolicyRule
CreditPolicy: `policy_id` Id, `version` Version, `title` Text, `source_hash` Hash, `normalized_hash` Hash, `scope` nonempty list[Id], `effective_from` Date, `effective_to` Date?, `authority` Id, `reviewer_id` Id, `curated_at` Timestamp. All except effective_to non-null. Validity interval is inclusive start, exclusive end; end > start. Authority precedence is OQ-006.
PolicyRule: `rule_id` Id, `version` Version, `policy_id` Id, `policy_version` Version, `source_chunk_ids` nonempty list[Id], `input_metric` Text, `operator` enum(gt,gte,lt,lte,eq), `threshold` decimal-string, `unit` Text, `scope` nonempty list[Id], `reviewer_id` Id. All non-null. Predicate is restricted to a registered metric/operator/threshold, not executable code. Complex prose that cannot fit is unsupported_rule until a reviewed contract extension.

## CT-010: Retrieval request/result and policy chunks
Request: `run_id` Id, `query` Text, `corpus_version` Version, `as_of` Date, `scope` nonempty list[Id], `retrieval_config_version` Version. All required.
Result: `retrieval_id`, `run_id` Id; `status` enum(found,insufficient,unavailable,conflicting); `chunks` list[PolicyChunk]; `reason` Text? required unless found; `corpus_version`, `index_version`, `retrieval_config_version` Version; `evidence_ids` list[Id]. All required except nullable reason. Unavailable index_version uses registered sentinel unavailable, not an invented deployed index.
PolicyChunk: `chunk_id`, `policy_id` Id; `policy_version` Version; `normalized_hash` Hash; `section` Text; `start_offset`, `end_offset` Count with end > start; `text` Text; `effective_from` Date; `effective_to` Date?; `scope` nonempty list[Id]; `retrieval_score` finite decimal-string. Score scale is index-specific and is not calibrated confidence. RAG configuration includes parser/chunker, embedding identity/dimensions, vector metric, top_k positive integer, token cap and sufficiency thresholds; values require OQ-007.

## CT-011: AnalysisRun manifest
`run_id` Id; `parent_run_id` Id?; `snapshot_id` Id?; `prior_snapshot_id` Id?; `revision` Count; `status` lifecycle enum from domain-model.md; `created_at` Timestamp; `completed_at` Timestamp?; `input_hash`, `config_hash` Hash; `canonical_input_hash` Hash?; `baseline_version`, `contract_version`, `rule_version`, `code_revision` Version; `requested_stages` nonempty list[Id]; `stage_outcomes` list[StageOutcome]; `output_artifact_ids` list[Id]; `ai_provenance` AIProvenance?; `errors` list[RunError]. All non-null unless marked. snapshot_id and canonical_input_hash may be null before successful validation and for rejected imports; metrics require both non-null.
StageOutcome: `stage` Id, `status` enum(pending,completed,not_requested,unavailable,failed), `reason` Text?, `attempt_count` Count, `duration_ms` Count. Reason required for unavailable/failed.
AIProvenance: `provider`, `model_id`, `prompt_version`, `embedding_version`, `index_version` Text?; `input_tokens`, `output_tokens` Count?; `estimated_cost` decimal-string? >= 0; `cost_currency` string?; `price_reference` Text?; `usage_complete` boolean. Null explicitly means not used or unavailable, disambiguated by stage outcomes. Cost non-null requires currency and dated price reference; missing usage never becomes zero.
RunError: `stage` Id, `code` enum(input_invalid,dependency_unavailable,timeout,budget_exceeded,output_invalid,conflict,persistence_failed,internal_error), `message` sanitized Text, `retryable` boolean. No stack traces containing payloads in persisted user-facing fields. Rejected imports retain their input_hash and validation report rather than a fabricated validated snapshot reference.

## CT-012: HumanReview
`review_id`, `run_id`, `recommendation_id`, `reviewer_id` Id; `expected_run_revision` Count; `decision` enum(approved,rejected); `rationale` Text; `reviewed_at` Timestamp; `idempotency_key` Id. All non-null. Decision is append-only. Same key and identical payload returns same review; changed payload conflicts. Approved local reviewer identity must be supplied by UI/application, never model output.

## CT-013: Copilot exchange
Request: `run_id` Id, `question` Text, `history_revision` Count. Response: `answer_id`, `run_id` Id; `status` enum(answered,abstained,refused,failed); `claims` list[Claim from CT-008]; `reason` Text?; `tool_call_ids` list[Id]. All non-null except reason, which is required unless answered. answered requires nonempty validated claims. History is bounded and run-scoped; no cross-run memory. Errors do not mutate AnalysisRun metrics.

## CT-014: SnapshotComparison
`comparison_id`, `run_id`, `current_snapshot_id` Id; `prior_snapshot_id` Id?; `status` enum(available,unavailable); `reason` enum(no_history,incompatible_snapshot,undefined_rate)?; `current_rate`, `prior_rate` MetricValue?; `rate_difference` signed finite decimal-string?; `entered_loan_count`, `exited_loan_count` Count?; `entered_exposure`, `exited_exposure` Amount?; `evidence_ids` RefList. All non-null unless marked. Available requires both snapshot IDs, both available rates, their exact difference and composition counts/amounts; reason must be null. Unavailable requires a reason and null difference; known operands may be retained. Values follow BR-RISK-004 and are not causal attribution. Evidence references immutable snapshots/metrics, never the comparison itself.

## Contract evolution
Changing meaning, units, nullability, enum behavior, rounding, or invalid-input handling is a behavior change, requiring CR after acceptance. Preserve old payload readers or specify migration/rejection explicitly. No Pydantic implementation exists in this baseline.

# Data contracts

Status: Proposed
Version: 1.0
Last Updated: 2026-11-11

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. This mixed-stage container remains Proposed; only the annotated IDs/variants are Accepted.

## Contract conventions
Written specifications only; no Pydantic product models exist. Contract version is 1.0. Each ID/variant has its own Status and Applicability; this mixed-stage document remains Proposed. CR-001 correction authorization is historical; BASELINE-ACCEPTANCE-001 records current owner acceptance of the listed M02 subsets.
Required fields may not be omitted. `?` permits null; other fields are non-null. CSV empty cell means null only for nullable segment. Unknown fields, duplicate JSON keys, missing/duplicate/extra headers and invalid non-null optional values reject ingress. Reject ambiguous encoding/records; no implicit trimming, coercion, imputation or deduplication.

| Type | Representation and constraints | Failure |
|---|---|---|
| Id | ASCII `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`; case-sensitive opaque identity. | Reject; never interpret as path. |
| Text | Nonempty UTF-8 text bounded by CT-020. | Reject invalid/oversized object. |
| Date | Exact YYYY-MM-DD Gregorian date. | Reject impossible/noncanonical date. |
| Timestamp | RFC3339 UTC with Z suffix. | Reject naive/local time. |
| Hash | 64 lowercase hex SHA-256 characters. | Reject invalid encoding/integrity mismatch. |
| Amount | Input decimal string, nonnegative, at most two fractional digits; no exponent, grouping, sign, NaN or infinity. Wire output and presentation use exactly two digits. USD only. | Reject; exact minor-unit conversion under CT-017. |
| Ratio | Nonnegative decimal string in [0,1], exactly four fractional digits when serialized, ROUND_HALF_EVEN under CT-017. | Reject inconsistent quantization; operands remain authoritative. |
| Count | Integer >= 0, not boolean; CSV canonical digits only. | Reject; numeric length cap in CT-020. |
| Version | Nonempty immutable registry/version/hash reference. | Unknown schema rejected; record exact other identities. |
| RefList | Nonempty unique EvidenceRef IDs belonging to the run. | Reject unknown/duplicate/cross-run refs. |

All monetary/ratio arithmetic and hashes follow CT-017. Contract defects reject the entire population; identity collisions are conflict; safety-bound violations are limit_failed under CT-015/019. Later generated-output defects discard candidates without changing metrics. Arrays can be empty unless explicitly nonempty. No arbitrary monetary/risk threshold is implied by parser limits.

## CT-001: PortfolioSnapshot and import manifest
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| schema_version | Version / no | Exactly 1.0. |
| snapshot_id | Id / no | Globally unique across the local repository/store; never reused for a different owner or content. |
| portfolio_id | Id / no | Exactly one owner; portfolio currency is fixed USD. |
| portfolio_name | Text / no | Synthetic analyst-facing label. |
| as_of | Date / no | Observation date for all loans. |
| currency | enum / no | USD only; no FX. A portfolio currency change rejects input. |
| synthetic | boolean / no | Must be true; only controlled synthetic fixture provenance is admitted. Not a PII-detection guarantee. |
| generator_version; seed | Version; Count / no | Synthetic provenance. No final generator/dataset is implemented now. |
| source_sha256 | Hash / no | Expected hash of exact CSV bytes; verified by ingress. |
| loans | list[CT-002] / no | All parsed rows; may be empty with valid headers. |

Wire bundle: UTF-8 comma-separated CSV with standard quoted fields and one header plus UTF-8 JSON manifest containing every field above except loans. Optional UTF-8 BOM is not accepted in v1; explicit rejection avoids implicit normalization. Header order must be CT-002 table order. CRLF and LF record endings are accepted; byte hashes distinguish them. Quoted multiline fields retain CSV record ordinal identity.
Import request carries import_idempotency_key: Id and parser_config_version: Version. CT-015 returns its outcome. Identical key and complete input bundle hash/config returns the existing semantic outcome; changed bundle/config conflicts. Run-specific evidence aliases are governed by CT-016. A globally reused snapshot_id with changed content or portfolio ownership conflicts. Same snapshot/content with a new import key may reference the existing snapshot rather than duplicate it. Canonically equivalent but byte-different bundles still conflict under a reused key or snapshot ID; users cannot silently rewrite source evidence. Snapshot identity and ownership are enforced before publication.
Invariants/failures: strict complete population, CT-002, CT-019 and CT-020. No valid snapshot is published for rejected/conflict/limit results. Traceability: FR-DQ-001/002/003, AC-DQ-001/002/003, BR-DQ-001/002/004.

## CT-002: Loan observation
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

| Field | Type / nullable | Meaning, unit and constraints |
|---|---|---|
| loan_id | Id / no | Unique within snapshot; same obligation may appear later. |
| customer_id | Id / no | Synthetic BorrowerRef; multiple loans may share it. |
| original_principal | Amount / no | Original funded USD amount > 0. |
| outstanding_principal | Amount / no | Remaining principal, 0 through original_principal; authoritative exposure. Capitalization products excluded. |
| days_past_due | Count / no | Reported calendar days at as_of; no risk threshold inferred from numeric-size limit. |
| loan_status | enum / no | open or closed. closed requires zero principal and zero DPD. |
| origination_date | Date / no | <= snapshot as_of. |
| segment | Id / yes | Null is valid and creates unspecified grouping; invalid non-null string rejects. |

Open zero-principal loans remain eligible for count delinquency and contribute zero exposure. A positive DPD does not make such a row invalid under this restricted contract. No informational finding is introduced for valid null segment or zero principal. Schema order is the table order. Income, installments, DTI and credit-score fields are excluded from active v1. Cross-snapshot temporal identity/attribute semantics remain OQ-005, not a new M02 invariant.
Traceability: FR-DQ-001/002, FR-RISK-001, AC-DQ-001/002, AC-RISK-001, BR-DQ-002/003, BR-RISK-001/002.

## CT-003: EvidenceRef
Status: Proposed
Accepted Scope: Common fields and M02 snapshot/source_row/metric/validation_report kinds and locators only; BASELINE-ACCEPTANCE-001, 2026-10-15.
M02 Status: Accepted
Later Status: Proposed
Deferred Scope: Later variants remain Proposed under their existing gates.
Applicability: M02 core; M03/M04 extensions Proposed

Required: evidence_id Id, run_id Id, kind enum, artifact_hash Hash, locator tagged object. M02 kind is snapshot, source_row, metric or validation_report. Locators: snapshot(snapshot_id Id); source_row(snapshot_id Id, row_number integer >= 2, field Id?); metric(metrics_id Id, metric_key Text); validation_report(report_id Id). snapshot_id is globally unique and resolved with immutable portfolio ownership. Every ref belongs to the run and verifies artifact_hash. No paths/URLs or cycles.
row_number is CSV record ordinal plus header, not physical byte line number. For unreadable input, a self-contained validation report supplies evidence without depending on an invalid loan object. A rejected report may have null input_hash if complete bytes could not be read.
Proposed later kinds: comparison(comparison_id Id), policy_chunk(chunk_id Id, policy_version Version, section Text, start_offset Count, end_offset Count > start), rule_evaluation(evaluation_id Id), retrieval_report(retrieval_id Id). Policy offsets are code-point intervals [start,end) in hashed normalized text. These variants remain gated to their future contracts.
Traceability: FR-DQ-002, FR-RISK-001, FR-OBS-001/003; CT-015/018/019; later FR-POL-001/002 and FR-AI-002.

## CT-004: PortfolioMetrics
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

| Field | Type / nullable | Meaning |
|---|---|---|
| metrics_id; run_id; snapshot_id | Id / no | Immutable result/run/global snapshot identity. |
| calculation_version; rule_config_version | Version / no | Exact calculation and configuration identities. |
| currency; as_of | enum(USD); Date / no | Match the snapshot. |
| loan_count; open_loan_count | Count / no | All loans; eligible open population, open <= total. |
| total_exposure | Amount / no | Exact all-loan outstanding-principal sum. |
| delinquency_count_rate; delinquency_exposure_rate | MetricValue / no | Separate authoritative count/exposure operands. |
| concentration | list[GroupShare] / no | Raw group metrics, not alerts; may be empty for an empty snapshot. |
| evidence_ids | RefList / no | Snapshot-derived provenance, including valid empty snapshots. |

MetricValue: status enum(available,unavailable), value Ratio?, numerator canonical exact nonnegative decimal-string, denominator canonical exact nonnegative decimal-string, unit enum(count_ratio,exposure_ratio), reason enum(zero_denominator,no_eligible_population)?, rule_id Id. Count operands are integer strings; exposure operands are USD strings with exactly two fractional digits. Available requires denominator > 0, value = quantized exact ratio, reason null. Unavailable requires denominator = 0, value null and a reason; operands are known even when zero. For delinquency with no open loans, use no_eligible_population; with open loans and zero principal, only exposure rate is zero_denominator. Count rate remains available. No absent metric becomes zero by assumption.
GroupShare: dimension enum(segment,borrower), group_id Id? (null only for unspecified segment), group_exposure Amount, share MetricValue. Unique (dimension,group_id) rows, all groups retained. Shares use exposure_ratio and group principal / total principal; zero total yields zero_denominator. Per dimension group exposures sum to total exposure. No alerts, thresholds or health claims are generated here. A mandatory metric for excluded finance concepts is not part of this schema.
Traceability: FR-RISK-001, AC-RISK-001, BR-RISK-001/002/003/005, CT-017.

## Shared finding envelope for CT-005/006/007
Status: Proposed
Accepted Scope: CT-005 DQ application only; BASELINE-ACCEPTANCE-001, 2026-10-15.
M02 Status: Accepted
Later Status: Proposed
Deferred Scope: CT-006/007 analytical applications remain Proposed.
Applicability: M02 DQ; M03 analytical extensions Proposed

finding_id Id, run_id Id, rule_id Id, rule_version Version, severity enum(info,warning,error), summary sanitized Text, evidence_ids RefList; all required. Severity and blocking behavior come from CT-019 for M02, from approved detector/policy configuration later. No LLM-selected numeric authority or severity.

## CT-005: DataQualityFinding
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

Required: shared envelope, scope enum(file,row,field), row_number integer >= 2? (null for file), field Id? (required for field scope), code from CT-019 validation catalog, blocking boolean. M02 actual findings are blocking errors for invalid input. No finding is emitted for valid null segment, valid empty population or denominator unavailability. Identity conflicts and safety failures are typed operation outcomes, not fabricated DQ loan findings.
Unreadable/file defects cite a persisted validation_report with report_id Id, input_hash Hash?, rule_id Id, error_code enum from CT-019, sanitized_message Text; all required except explicitly nullable hash. That report is self-contained and never references its finding cyclically. No raw invalid values in logs. Diagnostic collection completeness is CT-015/020. Traceability: FR-DQ-002/003, AC-DQ-002/003, BR-DQ-002/003/004, CT-019.

## CT-006: RiskFinding
Status: Proposed
Applicability: M03
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| category | enum / no | concentration, anomaly, deterioration. |
| observed_value; threshold | decimal-string / no | Finite values; signed values permitted for rate differences. Same unit as configuration. |
| operator | enum / no | gt, gte, lt, lte; compare authoritative operands under CT-017, never quantized observed_value. |
| unit | enum / no | currency, ratio, ratio_difference, days, count. |
| scope_ref | Id / no | Group, loan, or comparison artifact identity. |

No finding is emitted for an unavailable detector; stage status records absence. A missing finding is not proof of health.
Ratio/rate-difference observations must additionally carry exact numerator and denominator operands. Detector thresholds/operators remain OQ-004/005; this field requirement does not select them.

## CT-007: PolicyFinding
Status: Proposed
Applicability: M03
| Field | Type / nullable | Meaning and constraints |
|---|---|---|
| policy_id; policy_rule_id | Id / yes | Null only when no applicable policy/rule exists; non-null for violation/compliant. |
| policy_version | Version / yes | Required if policy_id set. |
| outcome | enum / no | violation, compliant, indeterminate. |
| reason | enum / yes | Required for indeterminate: no_policy, insufficient_evidence, conflicting_context, missing_input, unsupported_rule. Otherwise null. |
| predicate_evidence_ids | list[Id] / no | Nonempty for violation/compliant; evaluated inputs and applicable source required. |

The shared evidence envelope uses retrieval_report evidence for indeterminate outcomes. It must never imply that such an artifact is policy support. A rule_evaluation artifact contains evaluation_id, rule_id, rule_version, named typed input values, operator, threshold and boolean predicate_result; it references source evidence, never its resulting finding. All fields are required and use the shared conventions plus the predicate types in CT-009.
Unresolved policy context yields indeterminate; correction/curation occurs outside this analysis. No runtime policy-conflict review target is introduced. System-level indeterminate rule identity and evaluation coverage remain OQ-006.

## CT-008: ExecutiveInsight and Recommendation
Status: Proposed
Applicability: M03 observations; M04 recommendations
ExecutiveInsight fields: `insight_id`, `run_id` Id; `title` Text; `claims` nonempty list[Claim]; `finding_ids` list[Id]; `inspection_suggestions` list[InspectionSuggestion]; `recommendations` list[Recommendation]. All non-null.
Claim fields: `claim_id` Id; `kind` enum(interpretation,metric_reference,policy_reference); `text` Text; `evidence_ids` RefList; `metric_ref` Id? required for metric_reference, otherwise null. Metric reference resolves CT-003 metric evidence. Numeric facts are rendered from references by code, not authored as factual literals in text. Policy references require applicable policy_chunk evidence. Free text cannot override referenced values.
Recommendation fields: `recommendation_id`, `run_id` Id; `action` Text; `basis_claim_ids` nonempty list[Id]; `impact` enum(high,low); `review_status` enum(not_required,pending,approved,rejected); `evidence_ids` RefList. All non-null. Application assigns impact and status under BR-POL-004; LLM cannot self-approve. Low impact is limited to inspecting evidence or correcting synthetic input; all other actions default high.
M03 invariant: recommendations is empty. InspectionSuggestion fields are suggestion_id Id, text Text and evidence_ids RefList, all required; allowed action is only inspect/view supplied evidence. No customer treatment, collections, limits, lending policy or input mutation is suggested. M04 business-action Recommendation remains gated by OQ-012, FR-AI-003 and BR-POL-004. Its approval cannot resolve policy precedence.

## CT-009: CreditPolicy and PolicyRule
Status: Proposed
Applicability: M03
CreditPolicy: `policy_id` Id, `version` Version, `title` Text, `source_hash` Hash, `normalized_hash` Hash, `scope` nonempty list[Id], `effective_from` Date, `effective_to` Date?, `authority` Id, `reviewer_id` Id, `curated_at` Timestamp. All except effective_to non-null. Validity interval is inclusive start, exclusive end; end > start. Authority precedence is OQ-006.
PolicyRule: `rule_id` Id, `version` Version, `policy_id` Id, `policy_version` Version, `source_chunk_ids` nonempty list[Id], `input_metric` Text, `operator` enum(gt,gte,lt,lte,eq), `threshold` decimal-string, `unit` Text, `scope` nonempty list[Id], `reviewer_id` Id. All non-null. Predicate is restricted to a registered metric/operator/threshold, not executable code. Complex prose that cannot fit is unsupported_rule until a reviewed contract extension.
Scope/authority, predicate coverage and source-span-to-chunk mapping remain OQ-006/007. Do not infer these from the presence of schema fields.

## CT-010: Retrieval request/result and policy chunks
Status: Proposed
Applicability: M03
Request: `run_id` Id, `query` Text, `corpus_version` Version, `as_of` Date, `scope` nonempty list[Id], `retrieval_config_version` Version. All required.
Result: `retrieval_id`, `run_id` Id; `status` enum(found,insufficient,unavailable,conflicting); `chunks` list[PolicyChunk]; `reason` Text? required unless found; `corpus_version`, `index_version`, `retrieval_config_version` Version; `evidence_ids` list[Id]. All required except nullable reason. Unavailable index_version uses registered sentinel unavailable, not an invented deployed index.
PolicyChunk: `chunk_id`, `policy_id` Id; `policy_version` Version; `normalized_hash` Hash; `section` Text; `start_offset`, `end_offset` Count with end > start; `text` Text; `effective_from` Date; `effective_to` Date?; `scope` nonempty list[Id]; `retrieval_score` finite decimal-string. Score scale is index-specific and is not calibrated confidence. RAG configuration includes parser/chunker, embedding identity/dimensions, vector metric, top_k positive integer, token cap and sufficiency thresholds; values require OQ-007.

## CT-011: AnalysisRun manifest
Status: Proposed
Accepted Scope: M02 manifest, StageOutcome and RunError only; BASELINE-ACCEPTANCE-001, 2026-10-15.
M02 Status: Accepted
Later Status: Proposed
Deferred Scope: Later variants remain Proposed under their existing gates.
Applicability: M02 core; M03/M04 extensions Proposed

M02 fields: run_id Id; parent_run_id Id?; import_id Id; snapshot_id Id?; revision Count; status from domain-model.md M02 lifecycle; created_at Timestamp; completed_at Timestamp?; input_hash Hash?; canonical_input_hash Hash?; config_hash Hash; baseline_version, contract_version, rule_version, code_revision Version; requested_stages from CT-016; stage_outcomes list[StageOutcome]; output_artifact_ids list[Id]; errors list[RunError]. All non-null unless marked. snapshot_id/canonical_input_hash are required for valid metrics and absent for rejected/conflict/limit attempts. input_hash null is permitted only where complete bytes are unavailable (unreadable/early limit); record the exact reason in CT-015. completed_at is null for created/running and required for terminal M02 states.
StageOutcome: stage CT-016 enum, status enum(pending,completed,not_requested,unavailable,failed), reason Text?, attempt_count Count, duration_ms Count. reason required for unavailable/failed. M02 metric unavailability on zero denominator does not make a completed metric stage failed. No optional AI stage needs to be requested or represented by a pending M02 placeholder.
RunError: stage enum, code CT-019 operation/event catalog, message sanitized Text, retryable boolean. M02 persistence/integrity errors are explicit and no durable success is claimed before commit. If the store itself is unavailable, display a non-durable operation error; do not invent a persisted terminal record.
M03 Proposed extensions: prior_snapshot_id Id?, ai_provenance AIProvenance?, provisional_quality enum(none,complete,partial)?. M04 Proposed review-specific state and aggregation require OQ-009/012 before implementation. AIProvenance retains provider/model/prompt/embedding/index identity, token counts, usage completeness and dated estimated-cost provenance; exact per-attempt aggregation stays Proposed. M02 omits these extensions and has no provider cost requirement. No invisible zero for unknown actual AI usage later.
Traceability: FR-OBS-001/003, AC-OBS-001/003, CT-015/016/018/019; later FR-OBS-002.

## CT-012: HumanReview
Status: Proposed
Applicability: M04
`review_id`, `run_id`, `recommendation_id`, `reviewer_id` Id; `expected_run_revision` Count; `decision` enum(approved,rejected); `rationale` Text; `reviewed_at` Timestamp; `idempotency_key` Id. All non-null. Decision is append-only. Same key and identical payload returns same review; changed payload conflicts. Approved local reviewer identity must be supplied by UI/application, never model output.

## CT-013: Copilot exchange
Status: Proposed
Applicability: M04
Request: `run_id` Id, `question` Text, `history_revision` Count. Response: `answer_id`, `run_id` Id; `status` enum(answered,abstained,refused,failed); `claims` list[Claim from CT-008]; `reason` Text?; `tool_call_ids` list[Id]. All non-null except reason, which is required unless answered. answered requires nonempty validated claims. History is bounded and run-scoped; no cross-run memory. Errors do not mutate AnalysisRun metrics.

## CT-014: SnapshotComparison
Status: Proposed
Applicability: M03; temporal semantics remain OPEN
`comparison_id`, `run_id`, `current_snapshot_id` Id; `prior_snapshot_id` Id?; `status` enum(available,unavailable); `reason` enum(no_history,incompatible_snapshot,undefined_rate)?; `current_rate`, `prior_rate` MetricValue?; `rate_difference` signed four-fractional-digit decimal-string?; `difference_numerator` signed integer-string?; `difference_denominator` positive integer-string?; `entered_loan_count`, `exited_loan_count` Count?; `entered_exposure`, `exited_exposure` Amount?; `evidence_ids` RefList. All non-null unless marked. Available requires both snapshot IDs, both available rates, the exact difference operands and CT-017 quantized difference value, plus composition counts/amounts; reason must be null. Unavailable requires a reason and null difference; known operands may be retained. Values follow BR-RISK-004 and are not causal attribution. Evidence references immutable snapshots/metrics, never the comparison itself.
Rate kind, prior selection, cohort policy and immutable comparison-input lineage remain OQ-005. Different count/exposure semantics cannot be selected implicitly from these generic fields.

## CT-015: Import and Validation Result
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

Purpose: represent validation and operation outcomes without inventing a valid snapshot or calculating a filtered population.

| Field | Type / nullable | Meaning |
|---|---|---|
| import_id; run_id | Id / no | Application-assigned identities; never taken from malformed input. |
| import_idempotency_key | Id / no | Import binding distinct from analysis replay key. |
| disposition | enum / no | valid, rejected, conflict, limit_failed. |
| snapshot_id; portfolio_id | Id / yes | Set only for valid published snapshot; global identity and verified ownership. |
| input_hash; source_sha256 | Hash / yes | Complete framed bundle and CSV hashes; null only if full bytes unavailable. |
| canonical_input_hash | Hash / yes | Valid semantic snapshot hash; null unless valid. |
| parser_config_version; parser_config_hash | Version; Hash / no | Effective bounded parser configuration. |
| findings | list[CT-005] / no | Invalid-input diagnostics, possibly bounded. Empty for accepted null segment; no fabricated loan finding for identity/limit errors. |
| validation_report_id; report_hash | Id; Hash / no | Immutable safe report; usable even if input is unreadable. |
| report_complete | boolean / no | False if diagnostic scanning/collection stopped at cap; never claims a complete defect list. |
| error_code | CT-019 operation code / yes | Null for valid; otherwise exact rejection/conflict/limit reason. |

Invariants: valid requires verified hashes and published snapshot; all other outcomes publish no new valid snapshot or metrics. Conflict preserves the existing snapshot/binding. If input bytes are incomplete, no hash is guessed from a manifest claim; report records the reason. Exactly one overall disposition is selected using CT-019 precedence. A diagnostic cap after observed contract defects produces rejected/report_complete=false, not metrics from scanned rows.
Failure behavior: schema-invalid result cannot be persisted as successful validation. Store failure returns an explicit non-durable operation error rather than pretending a run/report committed. Acceptance criteria: AC-DQ-001/002/003, AC-OBS-003. Edge cases: unreadable manifest identity, global ID collision, duplicate JSON key, valid empty CSV, identical replay, changed-key content, early limit and capped defect collection.
Traceability: FR-DQ-001/002/003, FR-OBS-003; BR-DQ-001/002/003/004; CT-001/005/018/019/020; ADR-002/003.

## CT-016: Analysis Request and Analysis Configuration
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02; later modes require reviewed contract extension

Purpose: make stage selection, configuration and replay explicit without requiring any AI runtime.

| Field | Type / nullable | Meaning |
|---|---|---|
| bundle_ref | Id / no | Confined uploaded/stored input bytes; not an arbitrary path/URL and not necessarily valid data. |
| import_idempotency_key; analysis_idempotency_key | Id / no | Import interpretation binding versus analysis execution binding. |
| mode | enum / no | deterministic_m02 only. |
| requested_stages | ordered list / no | Exactly validate_portfolio, calculate_metrics. Loading/finalization are mandatory internal operations; raw concentration is part of metrics. |
| configuration | AnalysisConfiguration / no | Effective versioned configuration below. |
| parent_run_id | Id / yes | A deliberate new run may reference an existing terminal run; no mutation of that run. |

AnalysisConfiguration fields, all required: config_version Version; currency enum(USD); contract_version Version; calculation_version Version; rule_config_version Version; arithmetic_version Version for CT-017; parser_config_version Version and parser_limits CT-020; publication_version Version for CT-018; event_catalog_version Version for CT-019. config_hash is SHA-256 of its canonical payload under CT-017, computed and verified by Application. Only registered compatible versions are allowed; no arbitrary dictionaries, provider/model IDs, risk thresholds or checkpoint settings in M02 mode.
Allowed M02 stage_outcomes stage enum: load_portfolio, validate_portfolio, calculate_metrics, finalize. No AI/review stage is requested, pending or a prerequisite. Other modes are rejected until their future contracts are reviewed. No prior-snapshot comparison is silently enabled by a parent_run_id.
Invariants: import binding fixes complete bundle hash and parser config hash; analysis binding fixes bundle hash plus full config_hash, requested mode/stages and parent_run_id. Same analysis key and fingerprint returns the same run/result; changed fingerprint conflicts. A new analysis key can create a new run from the same immutable snapshot without reimporting or rewriting it. Reused import results provide the same semantic validation outcome; Application creates fresh run-scoped evidence aliases to existing immutable reports when needed. Never reuse another run's evidence IDs. A new run does not mutate terminal parent results. Unreadable/early-limit input without a complete hash cannot establish a cached content binding for either key; record explicit failed attempts without replacing an existing binding. A subsequent complete bounded request is checked normally, never treated as matching incomplete bytes by assumption.
Failure behavior: invalid mode/stage/version/config returns configuration_invalid before calculation; replay conflict preserves previous state. Output is CT-011 plus CT-015 and CT-004 when eligible. Acceptance criteria: AC-OBS-001/003, AC-DQ-001/003. Edge cases: omitted configuration, extra AI stage, same import/different analysis key, changed config under existing key, and failed finalization.
Traceability: FR-DQ-001, FR-OBS-001/003, FR-RISK-001; CT-015/017/018/020; ADR-003/008.

## CT-017: Arithmetic Serialization and Canonical Hashing
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02; same arithmetic authority for later ratios

Purpose: specify exact financial operands and reproducible representations without implementing calculators.

| Field / artifact | Type / representation | Constraint |
|---|---|---|
| arithmetic_version | Version | Identifies this exact arithmetic/serialization policy. |
| monetary operand | Nonnegative integer minor units internally | Convert accepted USD strings exactly; sums use arbitrary-precision integer arithmetic. No implicit Decimal-context or binary-float rounding. |
| count operand | Nonnegative integer | Exact population count, including open zero-principal loans. |
| ratio numerator; denominator | Exact typed operands | Count or exposure units match. Monetary operands serialize with two fractional digits; count operands as minimal integer strings. |
| derived value | Ratio? | Exact quotient quantized to four fractional digits, ROUND_HALF_EVEN; null iff unavailable. |
| signed ratio difference | Signed numerator and positive denominator | Later comparison arithmetic uses exact rational difference then quantizes once; temporal meaning remains OQ-005. |
| canonical payload | UTF-8 JSON bytes | Sorted object keys, no insignificant whitespace, no NaN, ASCII-escaped non-ASCII strings, no Unicode normalization; arrays preserve order except sorting expressly specified below. |
| semantic_hash; raw_bundle_hash | Hash | Different purposes below; neither substitutes for provenance. |

Invariants: numerator/denominator are authoritative, never the rounded value. Compare ratios using exact cross-multiplication; decimal constants are converted to exact rational operands. A display equality is not an exact equality. No business threshold is assigned here. Reject a derived string inconsistent with the specified quantization, a mismatched unit or a zero denominator labeled available. Output values with zero coefficient never use negative zero.
For deterministic snapshot hashing, include all CT-001 semantic fields except source_sha256, normalize amounts to two digits and integers to minimal encoding, and sort loans by ASCII loan_id. snapshot_id/portfolio_id remain included; original byte hashes live in lineage, not this semantic hash. For configuration hashing include every CT-016 effective setting including parser limits. For deterministic metric comparison/hash include snapshot_id, currency, as_of, calculation/rule versions, counts, monetary sums, exact operands, derived values and group metrics sorted by (dimension, null-first group_id). Exclude run_id, metrics_id, evidence IDs, timings and generated timestamps. Preserve those in CT-011 lineage. Equivalent row ordering may produce equal semantic content hashes while byte-different reuse still conflicts under CT-001.
Raw bundle framing is ASCII prefix RiskLensBundleV1 followed by an 8-byte unsigned big-endian manifest length, exact manifest bytes, an 8-byte CSV length, and exact CSV bytes. CSV source_sha256 hashes only CSV bytes. If bytes are incomplete, raw_bundle_hash is unavailable; never hash a truncated bundle and label it complete. Artifact_hash is always the hash of that artifact's actual bytes.
Failure behavior: noncanonical encoding, inconsistent operands/value or integrity mismatch is rejected at the relevant boundary. Acceptance criteria: AC-RISK-001, AC-OBS-001/003. Edge cases/spec examples: 1/3 serializes 0.3333 while preserving operands 1 and 3; 1/32 serializes 0.0312 and 3/32 serializes 0.0938; exact 1/3 differs from rounded 0.3333. Zero exposure does not imply zero eligible count. Exact input sums may exceed a single input's numeric-length cap; output precision must not be truncated to that cap.
Traceability: FR-RISK-001, FR-OBS-001/003; BR-RISK-001/002/003/005; NFR-REL-002; CT-004/016/018; ADR-008.

## CT-018: Local Artifact Publication and Recovery
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02; graph checkpoint adapter remains Proposed under OQ-009

Purpose: publish immutable artifacts and metadata safely in one local writer process, independently of graph orchestration.

| Field / record | Type / nullable | Meaning |
|---|---|---|
| publication_id; run_id | Id / no | Publication attempt and run ownership. |
| artifact_hash | Hash / no | Content identity; Application resolves storage location. |
| artifact_kind | enum / no | input_bundle, validated_snapshot, validation_report, metrics, event_batch. |
| byte_length | Count / no | Complete artifact length. |
| publication_state | enum / no | staged, published, committed; store metadata must expose only committed references. |
| expected_run_revision | Count / no | Optimistic commit boundary. |
| semantic_identity | typed object / no | Snapshot: global snapshot_id/portfolio_id; run result: run_id/stage/config_hash; never arbitrary executable content. |

Local state root is workspace/.risklens/state. Metadata is risklens.sqlite3; immutable files live under artifacts/sha256; staging files under tmp. Stores resolve paths from opaque identities and hashes with path confinement. This runtime directory is ignored by Git; no runtime files are created during baseline correction. One local writer serializes metadata mutation; no distributed lease or multi-user design is introduced.
Publication protocol: stage bytes on the same filesystem, compute/verify full hash, close the file, and atomically publish under its content hash. An existing hash must have matching verified bytes. Then, in one SQLite transaction, commit snapshot ownership, idempotency binding, artifact references, stage result and run revision/outcome. No DB reference may commit before its artifact is published. Terminal success requires both verified files and committed metadata. Metadata commit failure can leave a published orphan, never a successful referenced result. This is process-interruption recovery, not a guarantee against arbitrary disk or power failure.
Recovery: remove/ignore uncommitted temporary files; verify referenced artifacts; reuse verified committed results on replay; classify missing/corrupt referenced artifacts as integrity_error without recomputation under an old successful identity. Published orphan files are ignored by projections and may be reclaimed by explicit operator cleanup; no background GC is required. Import key and global snapshot ownership constraints are enforced in the same metadata commit. No LangGraph checkpoint is part of this M02 protocol; future coordination stays OQ-009/ADR-001.
Retention: no automatic expiry. Supported M02 cleanup is explicit removal of the entire .risklens/state directory after the application/writer is stopped and the operator verifies the resolved target is that exact workspace subdirectory. This removes all local run metadata and artifact history together; it does not remove source repository files or separate retained exports. No per-run delete UI, partial deletion, regulatory retention duration or future artifact lifecycle is claimed. Restart after cleanup creates new empty state; no old replay/lineage can be promised after intentional cleanup.
Failure behavior: staged-file error, hash mismatch, uniqueness/revision conflict or SQLite failure prevents final success and returns a typed CT-019 error. Acceptance criteria: AC-OBS-003 and AC-DQ-001. Edge cases: interruption before publish, after publish/before commit, after commit/before UI response; repeated key; global ID collision; corrupt referenced artifact; operator cleanup. Traceability: FR-OBS-003, FR-DQ-001; NFR-REL-002/SEC-001/SEC-002; CT-011/015/016/019; ADR-003/007/008.

## CT-019: Typed Events and Validation Catalogs
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02; AI/tool/review events require later extension

Purpose: give rejected input, conflicts, limits and operational failures unambiguous typed diagnostics and lineage.

Event fields: event_id Id, run_id Id, revision Count, stage CT-016 enum, attempt Count >= 1, event_type enum(operation_started,validation_completed,metrics_completed,publication_committed,operation_failed,replay_returned), timestamp_utc Timestamp, duration_ms Count?, outcome enum(in_progress,valid,rejected,conflict,limit_failed,succeeded,failed), code enum below?, input_hash Hash?, output_artifact_hash Hash?. All non-null unless marked. Completion/failure events require duration; failure outcomes require code. Unknown actual usage is not manufactured, but M02 has no provider event or AI cost fields.

| Validation code | Rule | Severity / blocking | Outcome |
|---|---|---|---|
| unreadable_input | BR-DQ-002 | error / true | rejected |
| schema_invalid | BR-DQ-002 | error / true | rejected: malformed UTF-8/CSV/JSON, duplicate JSON keys, unsupported schema/header ambiguity, unknown field |
| missing_required | BR-DQ-002 | error / true | rejected |
| duplicate_key | BR-DQ-001 | error / true | rejected: duplicate loan_id in the complete snapshot |
| invalid_value | BR-DQ-002 | error / true | rejected: invalid type/range, including invalid optional non-null segment |
| invariant_failed | BR-DQ-002 | error / true | rejected: dates, status/principal/DPD, currency or synthetic contract invariant |
| integrity_mismatch | BR-DQ-002 | error / true | rejected: complete CSV does not match declared source hash |

Operation error codes: input_invalid (overall rejected operation), identity_conflict, idempotency_conflict, resource_limit, configuration_invalid, persistence_failed, integrity_error, internal_error. Identity/idempotency collisions yield conflict without replacing existing data. CT-020 bounds yield limit_failed, except diagnostic collection caps after observed invalid data keep rejected/report_complete=false. Configuration/persistence/reference-integrity faults yield failed operation; they are not invented invalid-loan findings. User-facing messages are sanitized Text and include no raw input or secrets.
Disposition precedence: validate request/config and safety boundary first; if complete bytes are available, check already-bound identity/idempotency fingerprints before accepting any new identity, returning conflict on reuse mismatch; then structural/core validation selects rejected versus valid. No new valid snapshot is published until all applicable gates pass. A source hash mismatch on a previously unbound identity is rejected; reuse with different complete bytes is conflict and preserves the original. Valid null segment, empty snapshots and zero denominators emit no DQ defect. High DPD/concentration is not a CT-019 validation error.
Invariants: each validation diagnostic cites its catalog rule/severity; event outcomes match run/import disposition; fields have the declared types, nullability and active stage. Unknown codes are rejected. Failure behavior: invalid event/result cannot be committed as success; report a sanitized operational error. Acceptance criteria: AC-DQ-002/003, AC-OBS-001/003. Edge cases: no valid manifest IDs, unknown enum, truncated diagnostics, hash mismatch versus identity reuse, secret canary and replay event. Traceability: FR-DQ-002/003, FR-OBS-001/003; BR-DQ-001/002/004; NFR-OBS-001/SEC-001; CT-005/011/015/018; ADR-007.

## CT-020: Bounded Parser Configuration
Status: Accepted
Acceptance: BASELINE-ACCEPTANCE-001, 2026-10-15; reviewed M02 scope only.
Applicability: M02

Purpose: bound local parsing and diagnostics without inventing credit thresholds or production SLAs. Label this profile **Provisional Local Safety Limits**. The exact technical profile was approved by the owner under BASELINE-ACCEPTANCE-001 on 2026-10-15 as configurable local-development safety limits only.

| Field | Type / nullable | Approved provisional default and measured unit |
|---|---|---|
| parser_config_version | Version / no | provisional-local-v1 |
| max_input_bytes | positive integer / no | 10,485,760 bytes (10 MiB), combined manifest and CSV before parsing |
| max_manifest_bytes | positive integer / no | 65,536 bytes (64 KiB), subset of total input cap |
| max_rows | positive integer / no | 50,000 loan records excluding header |
| max_field_bytes | positive integer / no | 4,096 UTF-8 bytes per decoded CSV field or manifest scalar string |
| max_numeric_chars | positive integer / no | 24 ASCII characters for an input numeric token, including decimal point; output sums/operands are not truncated |
| max_collected_findings | positive integer / no | 1,000 diagnostics |

Rationale: 10 MiB/50,000 rows constrain a local demonstrator's input/workload without a memory-SLA claim; the lower manifest cap protects small metadata; field/numeric caps prevent pathological tokens; diagnostic cap avoids unbounded error output. These caps are deliberately rounded safety bounds, not benchmark-derived optimal values or financial thresholds. Configurability is explicit: validate positive integers and max_manifest_bytes <= max_input_bytes, version/hash effective values under CT-016, and record them in each run. Changes after acceptance require the normal reviewed configuration/change process; no unlogged UI increase.
Enforcement: check byte caps before unbounded decoding; field and token size while parsing; reject on the first record beyond max_rows instead of dropping it. Parser implementation must keep parsing/storage bounded, but these numbers alone do not certify peak memory. At max_collected_findings stop diagnostics/scan, mark report_complete=false and reject because defects were found. This diagnostic cap never returns metrics over inspected rows. If fewer invalid rows exist and all rows are scanned, report_complete=true.
Failure behavior: invalid configuration returns configuration_invalid; input/row/field/numeric overflow returns resource_limit/limit_failed. Malformed or negative numeric tokens within limits remain invalid_value rather than being repaired. Acceptance criteria: AC-DQ-003. Edge cases: exact bound versus bound+1; multibyte field byte count; header excluded from count; monetary sum longer than one input token; diagnostic cap and early oversized input with unavailable hash.
Traceability: FR-DQ-003, AC-DQ-003, BR-DQ-004, NFR-PERF-001; CT-001/015/016/017/019; ADR-002/003. The [OQ-008 safety decision](../00-project/open-questions.md) records the approved parser profile.

## Contract evolution
After acceptance, changes in meaning, units, nullability, enums, rounding, identity, safety defaults or invalid-input behavior require a CR and compatibility decision. No runtime payload/database exists yet, so this Proposed correction has no product migration. Preserve earlier proposal history in Git and CR-001. Later section presence does not make its feature implementation-ready.

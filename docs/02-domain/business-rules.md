# Business rules

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the listed clauses/variants are Accepted; other rows and later variants remain Proposed.

The Status column records accepted M02 variants and retained Proposed later rules under BASELINE-ACCEPTANCE-001. Financial conventions below are restricted synthetic-product choices recorded by the owner, not universal standards. No excluded finance analytics block v1.

| ID | Status | Applicability | Rule | Boundary / failure |
|---|---|---|---|---|
| BR-DQ-001 | Accepted | M02 | snapshot_id is globally unique with exactly one portfolio_id owner; loan_id unique inside a snapshot. | Duplicate loan rows reject; global ID/content/owner reuse conflicts; same obligation can recur in later snapshots. |
| BR-DQ-002 | Accepted | M02 | CT-001/002/019 structural/field/core invariants apply to all input rows; dates use as_of. | Reject whole snapshot on defect; no filtered calculations. Closed loans require zero principal/DPD. |
| BR-DQ-003 | Accepted | M02 | No imputation/FX/permissive coercion. USD only. Optional null segment is valid unspecified group. | Invalid non-null segment rejects; valid null/empty/zero exposure emits no invented DQ finding. |
| BR-DQ-004 | Accepted | M02 | Enforce CT-020 effective safety caps and CT-019 disposition catalog with explicit diagnostic completeness. | Overflow is limit_failed; found defects plus capped diagnostics stay rejected/report_complete=false; no truncated population metrics. |
| BR-RISK-001 | Accepted | M02 | Exposure is exact sum of outstanding_principal in one USD snapshot. Count all loans and open loans separately. | Empty sum 0.00; closed principal is zero; no original-amount or regulatory exposure interpretation. |
| BR-RISK-002 | Accepted | M02 | Eligible population is all open loans, including zero principal. Count rate = count(open,DPD>0)/count(open); exposure rate = principal(open,DPD>0)/principal(open). | Availability follows each denominator; zero principal does not remove a loan from count population. No eligible open loans uses no_eligible_population. |
| BR-RISK-003 | Accepted: M02 raw metrics; Proposed: M03 alert configuration | M02 raw metrics; M03 alert configuration | Raw concentration is group principal/total principal by borrower and segment; null segment is distinct unspecified bucket. | Zero total makes shares unavailable. Raw shares require no threshold. M03 alerts require approved configured threshold/operator under OQ-004. |
| BR-RISK-004 | Proposed | M03; OQ-005 OPEN | Compare only compatible earlier snapshots under explicitly reviewed rate/cohort policy; retain both operands and composition evidence. | Missing/incompatible history means unavailable comparison, not invalid current data. No causal or implicit trend claim. |
| BR-RISK-005 | Accepted | M02; arithmetic reused later | CT-017 exact minor-unit/count operands are authoritative. USD presentation has two digits; derived ratios serialize four digits using ROUND_HALF_EVEN. | Exact comparisons never use rounded display. No implicit precision rounding, floats or arbitrary business threshold. |
| BR-RISK-006 | Deprecated | Post-v1 concept only | Historical undefined-finance metric stub removed from active v1 by CR-001. Future concept needs a new scope CR and semantic rule. | No active requirement, output or release gate; historical ID retained. |
| BR-RISK-007 | Proposed | M03; OQ-004 OPEN | Anomalies use reviewed detector bounds on valid input, not predictive models. | Core-invalid values are rejected DQ defects; detector config never lives only in a prompt. |
| BR-POL-001 | Proposed | M03; OQ-006 OPEN | Only curated versioned predicates with applicable source support establish per-rule outcomes. | Missing/unsupported inputs/evidence yield indeterminate, not portfolio-wide compliance. |
| BR-POL-002 | Proposed | M03; OQ-006 OPEN | Filter effective scope; conflicting applicable sources remain indeterminate unless curated authority is established. | Correct corpus outside the analysis; no generic runtime conflict review or model-selected precedence. |
| BR-POL-003 | Proposed | M03 | No support means unavailable/insufficient policy context, never compliant. Every supported claim cites immutable source/version. | Reject fabricated, expired or cross-corpus citations. |
| BR-POL-004 | Proposed | M04 | Lending-policy/limits/collections/customer-treatment recommendations are high impact and pending review. M03 has only evidence inspection suggestions. | Human review never executes actions, edits metrics or establishes policy precedence. Reviewer identity stays OQ-012. |

Detector/policy configuration later identifies rule ID/version, source, operator, units/threshold and reviewer. Parser limits are operational bounds, not such business thresholds. Changes after acceptance follow CR governance. Status Deprecated for BR-RISK-006 retires its proposed stub without claiming any deployed rule existed.

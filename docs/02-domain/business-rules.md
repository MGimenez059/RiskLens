# Business rules

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

All rules have Status Proposed. Financial conventions below require owner acceptance and are not universal credit standards.

| ID | Rule | Failure or boundary behavior |
|---|---|---|
| BR-DQ-001 | Snapshot identity is portfolio_id plus snapshot_id; loan_id is unique within the snapshot. Same loan may recur in later snapshots. | Reject complete snapshot on duplicate key; never silently keep first/last row. |
| BR-DQ-002 | Every core field must satisfy CT-001/002; dates use as_of, never machine time. Closed loans have zero principal and DPD zero. | Emit CT-005 and reject complete snapshot; do not calculate on a filtered subset. |
| BR-DQ-003 | No imputation, hidden currency conversion, or permissive type coercion. Optional segment null is reported as unspecified. | Unsupported core values reject; optional null is retained, not filled with a guessed value. |
| BR-RISK-001 | Exposure is the sum of outstanding_principal of all valid loans in one snapshot/currency. Counts distinguish all loans from open loans. | Empty sum is 0.00; no cross-currency sum. This is not original loan amount or EAD. |
| BR-RISK-002 | Eligible delinquency population is open loans. Count rate = count(open and DPD > 0) / count(open). Exposure rate = principal(open and DPD > 0) / principal(open). | A zero denominator yields unavailable/null with reason. Preserve both numerator and denominator. |
| BR-RISK-003 | Concentration share = group outstanding principal / total outstanding principal, grouped separately by segment and customer_id. Null segment forms unspecified bucket. | Zero total gives unavailable shares. Finding requires an approved configured threshold/operator, OQ-004. |
| BR-RISK-004 | Deterioration compares current and prior delinquency rates using current minus prior. Same portfolio, currency, metric/rule version and earlier as_of required. Report entered/exited loan counts and exposure. | No comparable snapshots or undefined rates yields unavailable; difference is not evidence of causality. Alert threshold requires OQ-005 configuration. |
| BR-RISK-005 | Decimal arithmetic for money and ratios; no binary float authority. Monetary input has at most 2 decimal places in the proposed single-currency fixture. Store exact decimal numerator/denominator; display ratios to 4 decimal places using ROUND_HALF_EVEN. | Unsupported currency precision requires CR; rounding for display must not change threshold comparisons, which use exact operands. |
| BR-RISK-006 | Default classification is unavailable until OQ-002 defines population, trigger and effective rule version. | Do not infer default from DPD or status labels. |
| BR-RISK-007 | Anomalies use reviewed field bounds and operators from a versioned detector config; no predictive model in v1. | Core-invalid values are DQ defects, not accepted anomalous loans. Bounds are synthetic scenario settings. |
| BR-POL-001 | Only human-curated, versioned PolicyRules with source mapping and applicable policy evidence can establish violation/compliance. | Missing input/evidence or untranslatable prose yields indeterminate. |
| BR-POL-002 | Filter policies by scope and effective date. Conflicting applicable sources cannot be resolved by similarity score or model preference. | Mark conflict and require review unless an approved precedence rule resolves it. |
| BR-POL-003 | No retrieved support means policy unavailable/insufficient, never compliant. Each accepted policy claim cites immutable source location and version. | Reject fabricated, expired, or cross-corpus citations. |
| BR-POL-004 | All v1 recommendations affecting lending policy, limits, collections, or customer treatment are high impact; default impact is high. | Keep pending until human review. Review never executes the suggested action or edits computed values. |

Configuration must identify rule ID, version, effective date, operator, threshold/unit, author/reviewer and source. No business thresholds belong only in prompts. A new formula or population definition requires a CR and affected tests/evals.

# Domain glossary

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

| Term | RiskLens definition |
|---|---|
| Portfolio | Identified collection of loans in one currency, observed through snapshots. |
| PortfolioSnapshot | Immutable observation at an as-of date; globally unique snapshot_id with exactly one portfolio_id owner; unit of import and calculation. |
| Loan | Synthetic obligation identified within a portfolio; attributes may vary across snapshots. |
| Borrower | Synthetic debtor reference, customer_id; no personal identity data. |
| Exposure | Outstanding principal at snapshot time; neither original amount nor regulatory exposure. |
| Default | Deferred financial concept outside active v1, OQ-002. Future CR must define population, trigger and validity. Never infer a default threshold from DPD. |
| Delinquency | Arrears observed through days_past_due. Proposed rate uses DPD > 0 under BR-RISK-002. |
| Days Past Due / DPD | Reported calendar days overdue at the snapshot date; repayment schedules are not reconstructed. |
| DTI | Deferred debt-service/income concept outside active v1, OQ-003. A future CR must define period, income basis and debt coverage; one installment is not total debt service. |
| Risk Finding | Deterministic rule finding with evidence; AI interpretation may reference it. |
| Data Quality Finding | Contract defect at file, row, or field level. |
| Policy Finding | Result of applicability and evidence evaluation for a curated rule. |
| Policy Violation | Violation established by an approved deterministic predicate. Semantic similarity is insufficient. |
| Anomaly | Observation flagged by an explicit detector/configuration; not proof of fraud or default. |
| Insight | Interpretation linked to findings and supporting evidence. |
| Recommendation | M04 suggested business action, never executed by RiskLens. M03 inspection suggestions remain limited to viewing evidence and do not require human approval. |
| Analysis Run | Identified execution with immutable inputs, configuration, state, and provenance. |
| Human Review | Recorded human decision about interpretation or recommendations without metric edits. |
| Grounding | Verifiable support for each claim from available, applicable evidence. |
| Checkpoint | Resumable technical state; does not replace the run audit record. |

Financial terms are product conventions for synthetic analysis, not universal standards. Canonical formulas are in business-rules.md; fields are in data-contracts.md.

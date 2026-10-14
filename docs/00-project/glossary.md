# Domain glossary

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

| Term | RiskLens definition |
|---|---|
| Portfolio | Identified collection of loans in one currency, observed through snapshots. |
| PortfolioSnapshot | Immutable observation at an as-of date; unit of import and calculation. |
| Loan | Synthetic obligation identified within a portfolio; attributes may vary across snapshots. |
| Borrower | Synthetic debtor reference, customer_id; no personal identity data. |
| Exposure | Outstanding principal at snapshot time; neither original amount nor regulatory exposure. |
| Default | DECISION REQUIRED: versioned definition and eligible population, OQ-002. Not inferred from delinquency automatically. |
| Delinquency | Arrears observed through days_past_due. Proposed rate uses DPD > 0 under BR-RISK-002. |
| Days Past Due / DPD | Reported calendar days overdue at the snapshot date; repayment schedules are not reconstructed. |
| DTI | Debt service divided by income for the same period. Income basis and total debt coverage are DECISION REQUIRED, OQ-003. One loan installment is not total debt service. |
| Risk Finding | Deterministic rule finding with evidence; AI interpretation may reference it. |
| Data Quality Finding | Contract defect at file, row, or field level. |
| Policy Finding | Result of applicability and evidence evaluation for a curated rule. |
| Policy Violation | Violation established by an approved deterministic predicate. Semantic similarity is insufficient. |
| Anomaly | Observation flagged by an explicit detector/configuration; not proof of fraud or default. |
| Insight | Interpretation linked to findings and supporting evidence. |
| Recommendation | Suggested analyst action; never an executed loan action. |
| Analysis Run | Identified execution with immutable inputs, configuration, state, and provenance. |
| Human Review | Recorded human decision about interpretation or recommendations without metric edits. |
| Grounding | Verifiable support for each claim from available, applicable evidence. |
| Checkpoint | Resumable technical state; does not replace the run audit record. |

Financial terms are product conventions for synthetic analysis, not universal standards. Canonical formulas are in business-rules.md; fields are in data-contracts.md.

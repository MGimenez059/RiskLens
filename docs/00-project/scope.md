# Scope

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

## IN SCOPE: proposed product v1
- One local analyst; synthetic loan portfolios; immutable snapshots; one currency per portfolio.
- CSV import with a JSON manifest, quality validation, exposure and delinquency metrics, concentration by segment and borrower, and explicit rule-based anomaly detection.
- Temporal comparisons between eligible snapshots. Default semantics require a business decision.
- Synthetic Markdown policies, retrieval with citations, curated policy rule evaluation, and structured interpretation.
- Dashboard, copilot over existing runs, navigable evidence, human review, local persistence, and cost observability.

## OUT OF SCOPE: v1
Autonomous loan approval or rejection; real banking data; payments; production banking integrations; mobile application; training models from scratch; proprietary predictive credit scoring; regulatory PD/LGD/ECL; multi-tenancy; SSO; production cloud hosting; automatic portfolio changes; FX and cross-currency aggregation; OCR and complex PDFs; unrestricted agent browsing.
DTI and credit-score analytics are deferred pending definitions and require a scope CR if introduced. No regulatory compliance claim is made. Remote deployment or multiple users requires a CR, updated threat model, and ADR.

## Current execution
Specifications, proposed ADRs, written contracts, design diagrams, and quality tooling only. No product Pydantic models, final dataset, UI, graph nodes, executable prompts, or LLM integration. Baseline and product versions are independent.

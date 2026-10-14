# Owner decisions for CR-001

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

Decision evidence date: 2026-10-14. Source: explicit owner instruction to apply the reviewed baseline corrections. These decisions authorize corrections to Proposed specifications; they do not accept the resulting baseline or its ADRs against a reviewed commit. GOV-001 remains in force.

| Topic | Recorded owner decision |
|---|---|
| Currency | Synthetic v1 uses USD only; monetary presentation has two fractional digits; no FX or currency change within a portfolio. This is a product convention. |
| Exposure | outstanding_principal is authoritative. Open zero-principal loans remain in the count population and contribute zero exposure. |
| Deferred finance | Default analytics removed from active v1, without a threshold; DTI and score analytics excluded. Future inclusion requires a CR. |
| Identity | snapshot_id is globally unique and belongs to exactly one portfolio_id. |
| Validation | Complete-snapshot rejection for contract defects; explicit conflict/limit outcomes; no filtering, imputation or implicit deduplication. Null segment, empty snapshot and zero exposure are valid. |
| Arithmetic | Exact operands are authoritative; comparison is independent of rounding; explicit serialization; denominator-specific availability. |
| Concentration | Raw group exposure/shares in M02; threshold alerts/detectors in M03+. |
| Platform | Local single-user, one writer, SQLite metadata/state, immutable artifacts, Streamlit presentation; independent domain. |
| Retention | M02 retains synthetic metadata/artifacts until explicit operator cleanup; no expiry or per-run deletion UI. |
| M02 | Deterministic import, validation, outcomes, metrics, availability, lineage, persistence, restart/read/replay and dashboard. No AI, policies, graph checkpoints or review. |
| M03 | Grounded observations, explanations and evidence inspection suggestions; no high-impact recommendations or mandatory review. |
| M04 | High-impact recommendations and human review. Reviewer identity remains open. |
| Policy conflicts | Indeterminate result and corpus correction outside the run; no generic runtime conflict review or inference from recommendation approval. |
| Safety limits | Authorize proposing configurable provisional local safety caps. Exact numeric proposals are subject to review of the corrected commit, not recorded as preapproved values. |
| Acceptance | Preserve Proposed states, create an immutable review target, and seek approval of exact files/IDs after verification. |

Later temporal semantics, policy authority, retrieval/model choices, usefulness thresholds, checkpoint implementation, reviewer identity and deletion lifecycle remain unresolved. Technical details added to implement these owner decisions as written contracts are Proposed pending review of the corrected revision.

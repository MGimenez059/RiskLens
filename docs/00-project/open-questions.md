# Open decision register

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

All rows are OPEN / DECISION REQUIRED. Decision owner: product owner. Technical preparation: Architect/Auditor. Agents must not infer an answer.

| ID | Decision and candidate direction | Blocks |
|---|---|---|
| OQ-001 | Confirm one currency, outstanding principal exposure, CSV plus manifest, and whole-snapshot rejection for core/structural defects. | Contract acceptance and M02. |
| OQ-002 | Define default, denominator, treatment of closed/written-off loans, and effective date. Keep metric unavailable until resolved. | Default feature; M05 if retained in scope. |
| OQ-003 | Define DTI income basis, monthly total debt, income date, and score system/range. Excluded from core contract. | DTI/score extension via CR; not M02 or current v1 release. |
| OQ-004 | Approve synthetic concentration and anomaly thresholds by segment, borrower, and field. | Detectors in M03. |
| OQ-005 | Confirm temporal comparison of the same portfolio with changing composition; report composition effects. | Deterioration in M03. |
| OQ-006 | Define synthetic policy authority, validity, precedence, and human-reviewed rule translations. | Policies in M03. |
| OQ-007 | Select embedding, vector store, and retrieval parameters through a benchmark. ADR-005 proposes deferral now. | RAG in M03; not M02. |
| OQ-008 | Define workload, hardware, latency, memory, upload limit, per-run cost, timeout, and retry budget after measurements. | Each affected feature before implementation; M05. |
| OQ-009 | Confirm SQLite local persistence, candidate Streamlit UI, and review/resume design. | ADR-003/004, M02; durable graph in M03. |
| OQ-010 | Define retention/deletion across runs, evidence, checkpoints, logs, and copilot history. | Persistence M02; copilot M04. |
| OQ-011 | Select runtime models, prompt versions, holdout datasets, repeated-run count, and empirical quality thresholds. | AI M03; M05. |
| OQ-012 | Define local reviewer identity and evidence of human action. This is not enterprise authentication. | Human review M04. |

Accepting a baseline with deferred decisions requires recording their gates. Acceptance does not make every feature ready. TBD is never a default value.

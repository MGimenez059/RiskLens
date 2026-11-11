# Decision register and deferred gates

Status: Proposed
Version: 1.0
Last Updated: 2026-11-11

Decision owner: product owner. Technical preparation: Architect/Auditor. Recorded decisions are sourced in [owner-decisions-2026-10-14.md](../changes/owner-decisions-2026-10-14.md). CLOSED means the stated owner decision is recorded. Formal baseline subset acceptance is recorded separately in [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), dated 2026-10-15. Historical IDs remain stable. Split portions use the original ID plus a named portion rather than silently reusing IDs.

| ID / portion | Disposition | Resolution or remaining question | Gate |
|---|---|---|---|
| OQ-001 | CLOSED | USD, two-decimal monetary presentation, outstanding-principal exposure, strict import and globally unique snapshot ownership; CT-001/002/015/017/019. | No remaining M02 semantic choice for this portion. |
| OQ-002 / active-v1 scope | CLOSED | Default analytics excluded from active v1; no mandatory metric or release gate. | None in v1. |
| OQ-002 / financial definition | DEFERRED | No trigger/denominator chosen. Future CR needed. | Post-v1 Default feature. |
| OQ-003 | DEFERRED / outside active scope | DTI/score excluded; no income/debt/score definitions needed now. | Future extension CR, not v1. |
| OQ-004 | OPEN | Configured concentration alerts and anomaly bounds/operators. Raw group shares need no alert threshold. | M03 detectors. |
| OQ-005 | OPEN | Rate kind, prior selection, cohort/composition policy and temporal invariants. | M03 temporal feature. |
| OQ-006 | OPEN | Policy authority, scope/precedence and curated rule/source/coverage definitions. Conflicts stay indeterminate; corpus correction is outside a run. | M03 policy feature. |
| OQ-007 | OPEN | Embedding, index adapter, chunking/top_k and sufficiency benchmark. ADR-005 defers selection. | M03 retrieval feature. |
| OQ-008 / M02 safety | CLOSED | Exact configurable CT-020 profile accepted by the Product Owner on 2026-10-15 under BASELINE-ACCEPTANCE-001; local-development safety limits only, not SLAs, guarantees or financial thresholds. | Configuration acceptance satisfied; GOV-002 and separate implementation authorization remain. |
| OQ-008 / measured performance | CLOSED | On 2026-11-11, the Product Owner explicitly approved the three [local benchmark targets](../features/FEAT-001-verification.md#approved-oq-008-local-targets). All nine recorded trials met them. | M02 milestone performance gate satisfied; apply the relevant performance checks to affected later releases. |
| OQ-008 / AI budgets | OPEN | Model/tool call, context, timeout, retry and cost budgets. | M03 AI and M04 copilot readiness. |
| OQ-009 / M02 platform | CLOSED | SQLite plus immutable local artifacts, Streamlit and one local writer; CT-018. Domain remains independent. | ADR-003/004 Accepted under BASELINE-ACCEPTANCE-001; later graph/review details remain Proposed. |
| OQ-009 / graph persistence | OPEN | Checkpoint adapter, schema compatibility and cross-store graph reconciliation. | M03 graph readiness; ADR-001. |
| OQ-009 / review | OPEN | Review aggregation and interrupt/resume details. No M03 human-review gate. | M04 review readiness with OQ-012. |
| OQ-010 / M02 retention | CLOSED | Retain until explicit operator cleanup, no expiry, no per-run delete UI; whole-state cleanup boundary in CT-018. | CT-018 Accepted under BASELINE-ACCEPTANCE-001; no later lifecycle acceptance implied. |
| OQ-010 / later lifecycle | OPEN | Targeted deletion, policy/checkpoint/copilot retention and audit consequences. | Before exposing those operations. |
| OQ-011 | OPEN | Runtime models, prompts, holdouts, replications and empirical usefulness thresholds. | M03 AI readiness and applicable releases. |
| OQ-012 | OPEN | Local reviewer identity/action evidence; no enterprise-auth claim. | M04 high-impact recommendations. |

No OPEN later question blocks M02 merely because it shares a document with M02 rules. It blocks only its listed feature gate. Provisional safety values are not production targets; acceptance and implementation readiness remain governed by GOV-001/002.

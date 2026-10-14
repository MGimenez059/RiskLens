# Vertical slice roadmap

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

| Stage | Deliverable and exit evidence | Dependencies |
|---|---|---|
| M01 | Reviewed and accepted baseline with acceptance record, ADRs, and diagram. | GOV-001; resolve next-slice blockers. |
| M02 | Synthetic CSV import, validation, basic metrics, persisted run, dashboard, evidence, and errors. No LLM. | OQ-001/008/009/010; AC-DQ-001/002, AC-RISK-001, AC-UI-001, AC-OBS-001. |
| M03 | Detectors, temporal comparison, curated policies, tools, resumable LangGraph, RAG, grounded synthesis. | Relevant ADRs; AC-RISK-002/003, AC-POL-001/002, AC-AI-001, AC-OBS-002. |
| M04 | Bounded copilot, evidence navigation, and usable human review end-to-end. | AC-AI-002/003, AC-UI-002; OQ-012. |
| M05 | Audited reproducible v1 release, documentation, and sanitized evaluation report. | All approved FR/NFR satisfied; no open release blockers. |

Release requires a reproducible lock, tested migration/recovery paths, no unresolved critical security or grounding findings, approved and measured performance/cost budgets, and traceability without NOT IMPLEMENTED entries for in-scope features. Removing a feature requires a CR rather than a silent release exception.
Each slice includes the minimum necessary domain, persistence, application, UI, and validation work. Do not build the entire database or all agents first.

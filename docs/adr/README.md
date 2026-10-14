# Architecture decision records

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

| ID | Decision | Initial status |
|---|---|---|
| ADR-001 | Bounded LangGraph orchestration after deterministic slice. | Proposed |
| ADR-002 | Pydantic at boundaries, standard Python domain. | Proposed |
| ADR-003 | Local SQLite metadata and immutable file artifacts. | Proposed |
| ADR-004 | Owner-selected Streamlit local presentation adapter. | Proposed |
| ADR-005 | Defer embedding/vector store choice until benchmark. | Proposed |
| ADR-006 | Application-owned provider ports. | Proposed |
| ADR-007 | Structured local observability first. | Proposed |
| ADR-008 | Modular src layout with explicit dependency direction. | Proposed |
| ADR-009 | uv and minimal Python quality tooling. | Proposed |

All ADRs remain Proposed. ADR-002 through ADR-009 are prepared for human acceptance of the corrected review target; ADR-001 remains gated by M03 graph questions. Owner platform decisions authorize Proposed corrections but no status autoapproval. Acceptance is individual and requires human review under GOV-001. No decision in this directory is automatically accepted. An accepted deferral does not select a deferred vendor.

Use [the template](ADR-XXX-template.md), assign a stable unused ID, identify requirements and alternatives, and record date/reviewer on acceptance. To replace an accepted decision, create a new ADR with Supersedes, and add Superseded by plus status metadata to the old record. Preserve its original context and decision. Never rewrite historical reasoning to match current code. A proposed record may be revised with CHANGELOG evidence before acceptance.

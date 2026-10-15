# Architecture decision records

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

| ID | Decision | Current status |
|---|---|---|
| ADR-001 | Bounded LangGraph orchestration after deterministic slice. | Proposed |
| ADR-002 | Pydantic at boundaries, standard Python domain. | Accepted |
| ADR-003 | Local SQLite metadata and immutable file artifacts. | Accepted |
| ADR-004 | Owner-selected Streamlit local presentation adapter. | Accepted |
| ADR-005 | Defer embedding/vector store choice until benchmark. | Accepted |
| ADR-006 | Application-owned provider ports. | Accepted |
| ADR-007 | Structured local observability first. | Accepted |
| ADR-008 | Modular src layout with explicit dependency direction. | Accepted |
| ADR-009 | uv and minimal Python quality tooling. | Accepted |

The Product Owner explicitly accepted ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008 and ADR-009 on 2026-10-15 under [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), against reviewed commit archived baseline review revision. ADR-001 remains Proposed behind M03 graph questions. ADR-005 accepts deferral only, not a vector store. ADR-006 accepts the boundary direction, not a provider or M02 dependency. This index tracks individual decisions and does not accept future feature details.

Use [the template](ADR-XXX-template.md), assign a stable unused ID, identify requirements and alternatives, and record date/reviewer on acceptance. To replace an accepted decision, create a new ADR with Supersedes, and add Superseded by plus status metadata to the old record. Preserve its original context and decision. Never rewrite historical reasoning to match current code. A proposed record may be revised with CHANGELOG evidence before acceptance.

# ADR-008: Modular repository architecture

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14
Applicability: M02 core; later variants gated
Acceptance Readiness: Prepared for explicit human acceptance against the corrected reviewed commit; not accepted now.

- ID: ADR-008
- Date: 2026-10-07
- Related requirements: NFR-MNT-001, NFR-REL-002, FR-RISK-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
The project must preserve domain rules and decisions across AI-assisted work without creating unused abstractions.

## Decision
Use a Python src layout with domain, application, infrastructure, graph and tools. Presentation is added with the first UI slice, not as empty framework scaffolding. Keep canonical specifications under docs, governance in AGENTS.md and immutable decision records in docs/adr and docs/changes. Enforce dependency direction described in architecture.md.

## Alternatives
A single notebook/script cannot preserve the intended boundaries as features grow. Microservices and separate bounded-context packages add deployment and coordination costs without present need.

## Consequences
Static boundary checks and traceability maintenance are required. Do not introduce generic repositories or service layers without a concrete use. Empty directories use .gitkeep only to retain the requested initial structure.

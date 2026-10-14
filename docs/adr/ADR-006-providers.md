# ADR-006: Provider abstraction

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14
Applicability: M03 deferral / future adapter
Acceptance Readiness: Prepared for explicit human acceptance against the corrected reviewed commit; not accepted now.

- ID: ADR-006
- Date: 2026-10-07
- Related requirements: FR-AI-001/002, NFR-AI-002, NFR-MNT-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
Model availability and output behavior can change. Tests must run without provider credentials.

## Decision
Use small application-owned StructuredModel and PolicyRetriever ports. Adapters translate provider responses into project contracts, normalize errors, preserve usage and expose effective model identity. Add each port only when used by an approved slice. Select runtime models through evals rather than the coding-agent role mapping.

## Alternatives
Direct SDK usage inside domain is simpler initially but violates isolation. A universal plugin framework or large provider factory is unnecessary before a second concrete adapter exists.

## Consequences
Adapter contract tests and deterministic fakes are required. Do not pretend providers are behaviorally equivalent; switching requires evals and configuration traceability. LangChain is allowed behind adapters when it solves a demonstrated integration need, not as mandatory business infrastructure.

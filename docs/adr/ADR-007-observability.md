# ADR-007: Structured local observability

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15
Applicability: M02 core; later variants gated
Acceptance Record: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md)
Acceptance Date: 2026-10-15
Accepted By: Product Owner, human user in this conversation
Reviewed Commit: archived baseline review revision
Acceptance Scope: Individual direction/deferral decision only; later contracts and feature gates remain as recorded.

- ID: ADR-007
- Date: 2026-10-07
- Related requirements: FR-OBS-001, NFR-OBS-001, NFR-SEC-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product Owner; explicit acceptance recorded 2026-10-15.

## Context
Debugging and evaluation need correlated events and cost provenance. No production observability platform is required for a local baseline.

## Decision
Start with structured local events and CT-011 manifests. Separate audit data, checkpoints and debug logs. Unknown provider usage or pricing remains unknown. Record concise evidence-backed explanations, not hidden model reasoning.

## Alternatives
Plain console strings lose machine-readable lineage. Hosted tracing may help later but adds a provider and export/privacy decisions. Adopt it only through a later ADR with a concrete need.

## Consequences
CT-019 supplies the M02 typed event catalog and CT-018 the owner-approved retention/cleanup boundary. Model/tool/review fields apply only in later enabled stages. The project owns its event schema. Event completeness and redaction require tests; targeted later lifecycle remains OQ-010. Local events alone do not provide production incident management.

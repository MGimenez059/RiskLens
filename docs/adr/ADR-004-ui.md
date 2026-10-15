# ADR-004: Initial local UI candidate

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15
Applicability: M02 core; later variants gated
Acceptance Record: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md)
Acceptance Date: 2026-10-15
Accepted By: Product Owner, human user in this conversation
Reviewed Commit: archived baseline review revision
Acceptance Scope: Individual direction/deferral decision only; later contracts and feature gates remain as recorded.

- ID: ADR-004
- Date: 2026-10-07
- Related requirements: FR-UI-001/002, FR-AI-003
- Supersedes: None
- Superseded by: None
- Decision owner: Product Owner; explicit acceptance recorded 2026-10-15.

## Context
The first slice needs upload, tables/charts, status and evidence navigation. Product quality must not depend on a specific presentation framework.

## Decision
The owner selects Streamlit as the local single-user v1 presentation adapter, accepted under BASELINE-ACCEPTANCE-001. An M02 feature interaction spec still precedes implementation. Keep calculations and persistence outside UI callbacks. Later M04 review actions carry explicit run revisions and idempotency keys; they are not M02 UI prerequisites.

## Alternatives
A separate web frontend/API offers more interaction control but increases initial scope. A notebook or CLI cannot satisfy the visual product requirement alone.

## Consequences
Framework reruns and session state must not become durable run state. Validate import/review/restart interactions before committing to all product screens. No dashboard, UI dependency or visual product mockup is created now.

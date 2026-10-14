# ADR-004: Initial local UI candidate

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

- ID: ADR-004
- Date: 2026-10-07
- Related requirements: FR-UI-001/002, FR-AI-003
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
The first slice needs upload, tables/charts, status and evidence navigation. Product quality must not depend on a specific presentation framework.

## Decision
Propose Streamlit as a local v1 candidate, subject to OQ-009 and an approved UI interaction specification. Keep calculations and persistence outside UI callbacks. Review actions carry explicit run revisions and idempotency keys.

## Alternatives
A separate web frontend/API offers more interaction control but increases initial scope. A notebook or CLI cannot satisfy the visual product requirement alone.

## Consequences
Framework reruns and session state must not become durable run state. Validate import/review/restart interactions before committing to all product screens. No dashboard, UI dependency or visual product mockup is created now.

# ADR-003: Local persistence

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14
Applicability: M02 core; later variants gated
Acceptance Readiness: Prepared for explicit human acceptance against the corrected reviewed commit; not accepted now.

- ID: ADR-003
- Date: 2026-10-07
- Related requirements: FR-OBS-001/002, FR-AI-003, NFR-REL-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
Runs, review decisions and recovery must survive process restart. The proposed deployment is one local analyst.

## Decision
Propose SQLite for run/review/event metadata and content-addressed local files for immutable input/output artifacts. Use parameterized SQL, foreign keys, transactions, unique idempotency keys and optimistic revisions. Checkpointer storage remains a separate adapter. Owner-selected platform and M02 retention are recorded. M02 publication/recovery and whole-state cleanup are CT-018; configurable safety proposal is CT-020. Checkpoint/review/later deletion questions remain open. No M02 graph adapter is required.

## Alternatives
Memory-only storage cannot satisfy restart recovery. PostgreSQL provides stronger multi-user operating options but adds an unnecessary service for current scope. File-only metadata complicates transactional review updates.

## Consequences
One-writer behavior, migration testing, artifact/metadata reconciliation and backup/deletion semantics require explicit tests. Do not claim cross-store atomicity; use the committed-result recovery protocol in architecture.md. No schema is implemented in this phase.

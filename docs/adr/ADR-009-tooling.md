# ADR-009: Minimal Python tooling

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14
Applicability: M02 core; later variants gated
Acceptance Readiness: Prepared for explicit human acceptance against the corrected reviewed commit; not accepted now.

- ID: ADR-009
- Date: 2026-10-07
- Related requirements: NFR-MNT-001, NFR-REL-002
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
The user authorized initial CI/tooling while withholding product implementation. Reproducible tooling should not imply an accepted product architecture.

## Decision
Configure Python 3.12+, uv for environment/lock management, Ruff, mypy, pytest and local pre-commit hooks. Use hatchling only as the package build backend. GitHub Actions runs the same gates with read-only repository permissions. Install no product/runtime dependencies yet.

## Alternatives
pip plus manually pinned requirements is workable but splits metadata and locking. Multiple formatter/linter stacks duplicate checks. A no-op product test suite would imply coverage that does not exist.

## Consequences
Commit uv.lock with the reviewed baseline. Tool upgrades change the lock and need verification. Tooling is executable as explicitly authorized scaffolding; this ADR remains Proposed until human review. CI has no product acceptance or live-provider evaluation authority.

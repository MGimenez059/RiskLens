# RiskLens agent instructions

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](docs/changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the document/section scope recorded there is accepted; later feature gates remain in force.

Read this file before working. Acceptance status and implementation gates: [baseline](docs/00-project/baseline.md). The Product Owner accepted the exact reviewed baseline subsets with explicit deferrals in [BASELINE-ACCEPTANCE-001](docs/changes/BASELINE-ACCEPTANCE-001.md) on 2026-10-15. M02 feature preparation and implementation require a separate authorized task and GOV-002. Historical correction decisions remain in docs/changes/owner-decisions-2026-10-14.md; the acceptance record is the current approval authority.

## Before changes
1. Read [principles](docs/00-project/principles.md), the canonical precedence source, and [writing policy](docs/00-project/writing-policy.md).
2. Identify relevant requirement IDs and criteria; read domain contracts.
3. Read relevant ADRs and open questions; inspect tests, evals, and traceability.
4. Check GOV-002. Never resolve TBD by inventing requirements. Check per-ID Status and Applicability; never make later AI/review/checkpoint gates prerequisites for deterministic M02 or accept an entire mixed-stage document implicitly.
5. If requested behavior conflicts with specifications, STOP dependent work, report **SPEC CONFLICT** with paths and IDs, and propose a [CR](docs/changes/README.md). Update and approve specs before implementation.
6. Never silently change approved specs or introduce architecture without an ADR. Never overwrite historical decisions.
7. Maintain traceability. Prefer deterministic logic, independent domain code, and clear contracts. Justify dependencies. Do not refactor unrelated code or broaden scope implicitly.
8. Verify GOV-003 and report only checks actually executed. Planned tests are not implemented tests.

## MODEL ROUTING CHECK
Before significant work, classify the task, identify the recommended role from the [model policy](docs/00-project/model-usage-policy.md), and compare it with known execution context. Mention when a lighter model is sufficient; recommend escalation when needed. Do not pretend to switch models or block trivial work. Report unknown when current model identity is unavailable. Routing does not implicitly authorize delegation or additional spending.

## Navigation and checks
- Domain: docs/02-domain. Architecture: docs/03-architecture. AI: docs/04-ai.
- Governance: docs/adr and docs/changes. Validation: docs/05-testing.
- Run `uv sync --locked --group dev`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src scripts`, and `uv run pytest`.
- Tests must not require API keys. Before external AI calls, establish task need and budget.
- Recover context from repository files and Git state, not conversation memory.

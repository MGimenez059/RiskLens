# RiskLens

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

AI-powered Credit Risk Intelligence Platform.

RiskLens is a proposed local platform for credit risk analysts and Data teams to inspect synthetic loan portfolios, calculate deterministic metrics, investigate evidence and review policy-grounded AI interpretation.

**Current deliverable: Corrected Specification Baseline v1.0, Proposed.** Product functionality is not implemented. Owner correction decisions are recorded; acceptance of the exact corrected commit is still pending. M02 is deterministic USD analytics and local persistence; AI and review are later gated capabilities.

## Review entry points
- [Final baseline closure report](docs/00-project/baseline-closure-report.md). The review-target locator identifies the final immutable Proposed revision; acceptance remains an explicit owner decision.
- [Current correction report](docs/00-project/baseline-correction-report.md), [immutable review target](docs/changes/baseline-review-target.md) and [CR-001](docs/changes/CR-001-baseline-acceptance-corrections.md).
- [Baseline and acceptance procedure](docs/00-project/baseline.md).
- [Review report and file inventory](docs/00-project/review-report.md).
- [Principles and source precedence](docs/00-project/principles.md).
- [Requirements](docs/01-requirements/functional-requirements.md) and [acceptance criteria](docs/01-requirements/acceptance-criteria.md).
- [Contracts](docs/02-domain/data-contracts.md), [architecture](docs/03-architecture/architecture.md), [graph specification](docs/03-architecture/graph-spec.md).
- [ADRs](docs/adr/README.md), [open decisions](docs/00-project/open-questions.md), [traceability](docs/05-testing/traceability.md).
- [Model usage policy](docs/00-project/model-usage-policy.md).
- [Writing policy](docs/00-project/writing-policy.md).

Agents must read [AGENTS.md](AGENTS.md) before work. The repository is the permanent project record. Source precedence and conflict handling are defined in the principles document.

## Proposed design

## Development tooling
Prerequisites: Git and uv. The repository selects Python 3.12 locally and declares Python 3.12+ support. uv may download the selected interpreter. CI is configured for Python 3.12 and 3.14. No provider credentials or product runtime dependencies are needed.

```text
uv sync --locked --group dev
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src scripts
uv run --locked pytest
uv run --locked python scripts/check_baseline.py
uv run --locked pre-commit install
```

The package version is 0.0.0 because no product release exists. Baseline version 1.0 describes documentation. The committed uv.lock records resolved tooling versions. Local environment files and private input/output artifacts are ignored.

The tests verify document metadata/style, local links, requirement/contract traceability, per-ID applicability, mixed-stage approval boundaries, global snapshot identity and domain imports. Negative document fixtures exercise governance regressions. These checks do not prove semantic correctness or product behavior. No dashboard launch command exists yet.

## Next step
Review the baseline and record acceptance under GOV-001. Resolve the first-slice blockers before preparing its feature specification. The proposed first slice imports a synthetic snapshot, validates it, calculates deterministic metrics, persists a run and displays results with evidence. Do not implement it during baseline preparation.

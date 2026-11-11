# RiskLens

Status: Proposed
Version: 1.0
Last Updated: 2026-11-10

AI-powered Credit Risk Intelligence Platform.

RiskLens is a proposed local platform for credit risk analysts and Data teams to inspect synthetic loan portfolios, calculate deterministic metrics, investigate evidence and review policy-grounded AI interpretation.

**Current deliverable.** The local [M02 deterministic analysis dashboard](docs/features/FEAT-001-deterministic-analysis.md) imports synthetic USD portfolios, reports validation outcomes, calculates exact metrics, and stores verified results for later inspection. Milestone completion is pending approval of the measured OQ-008 targets.

The Product Owner approved the archived baseline review revision and the exact subsets in [BASELINE-ACCEPTANCE-001](docs/changes/BASELINE-ACCEPTANCE-001.md) on 2026-10-15.

## Run the local dashboard

From the repository root, with Python and uv available:

```powershell
uv sync --locked --group dev
uv run --locked streamlit run src/risklens/presentation/dashboard.py
```

Open the local URL printed by Streamlit. Select **Analyze sample** for a two-loan portfolio with USD 400.00 outstanding. For a manual import, provide a UTF-8 loan CSV and its JSON manifest as defined by CT-001 and CT-002 in the [data contracts](docs/02-domain/data-contracts.md). The manifest includes the SHA-256 of the exact CSV bytes. Use controlled synthetic data only.

Choose a saved analysis in **Run history** after reloading the browser or restarting Streamlit. **New analysis** runs the selected stored bundle again and links the new run to its parent. **Resume analysis** repeats interrupted deterministic work using its saved request.

The workspace retains SQLite metadata and immutable files under `.risklens/state`. To clear the entire local history, stop the application and verify that the resolved cleanup target is exactly that subdirectory of this workspace before removing it.

## Review entry points
- [Owner acceptance record](docs/changes/BASELINE-ACCEPTANCE-001.md), [acceptance verification report](docs/changes/baseline-acceptance-verification-2026-10-15.md) and [immutable reviewed revision](docs/changes/baseline-review-target.md).
- [Historical final closure report](docs/00-project/baseline-closure-report.md), preserved as the pre-acceptance review.
- [Prior correction report](docs/00-project/baseline-correction-report.md), [immutable review target](docs/changes/baseline-review-target.md) and [CR-001](docs/changes/CR-001-baseline-acceptance-corrections.md).
- [Baseline and acceptance procedure](docs/00-project/baseline.md).
- [Review report and file inventory](docs/00-project/review-report.md).
- [Principles and source precedence](docs/00-project/principles.md).
- [Requirements](docs/01-requirements/functional-requirements.md) and [acceptance criteria](docs/01-requirements/acceptance-criteria.md).
- [Contracts](docs/02-domain/data-contracts.md), [architecture](docs/03-architecture/architecture.md), [graph specification](docs/03-architecture/graph-spec.md).
- [ADRs](docs/adr/README.md), [open decisions](docs/00-project/open-questions.md), [traceability](docs/05-testing/traceability.md).
- [Model usage policy](docs/00-project/model-usage-policy.md).
- [Writing policy](docs/00-project/writing-policy.md).

Agents must read [AGENTS.md](AGENTS.md) before work. The repository is the permanent project record. Source precedence and conflict handling are defined in the principles document.

## Development tooling
Prerequisites are Git and uv. The repository selects Python 3.12 locally and declares Python 3.12+ support. uv may download the selected interpreter. CI is configured for Python 3.12 and 3.14. The test suite requires no API keys.

```text
uv sync --locked --group dev
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src scripts
uv run --locked pytest
uv run --locked python scripts/check_baseline.py
uv run --locked pre-commit install
```

The package version is 0.0.0 because no product release exists. Baseline version 1.0 describes documentation. The uv lockfile records the resolved runtime and development dependencies. Local environment files and private input/output artifacts are ignored.

The product suite covers arithmetic, import contracts, persistence and restart, and Streamlit interactions. The governance suite separately checks document metadata, links, traceability, applicability, approval boundaries, global snapshot identity and domain imports. See the [traceability matrix](docs/05-testing/traceability.md).

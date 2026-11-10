# FEAT-001 verification and OQ-008 measurements

Status: Proposed
Version: 1.0
Last Updated: 2026-11-10
Applicability: M02

The measurements and 59-case test results below are preliminary evidence from before the contract correction. They do not establish the results for the corrected implementation commit.

## Functional verification

The implementation and tests map to the accepted M02 criteria in the [traceability matrix](../05-testing/traceability.md). The 59 passing pytest cases include 44 product and 15 repository governance cases. The product cases exercise strict ingress and cataloged diagnostics, parser bounds, exact and unavailable rates, independent concentration groups, ownership and replay, interruptions around publication and commit, integrity errors, cleanup, and Streamlit sample, manual and history flows.

Local quality commands:

```text
uv sync --locked --group dev
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src scripts
uv run --locked pytest
uv run --locked python scripts/check_baseline.py
```

Microsoft Edge visual verification used the actual Streamlit process on loopback. It confirmed the bundled portfolio's USD 400.00, 50.00% and 75.00%, both concentration tabs, the same selected run after browser refresh, and no page-level horizontal overflow at 430 px. The local QA screenshot is in the ignored `artifacts/private/m02-dashboard.png` path.

## Measured workload

Measurements ran on Windows 11 build 26200, Intel Core i3-N305, eight logical processors, 7.63 GiB physical memory, CPython 3.12.13, Pydantic 2.14.3 and Streamlit 1.67.0 from `uv.lock`. The starting Git revision was `archived acceptance record revision`. The measured working-tree implementation records runtime source SHA-256 `30da62290b09122c179c43a8a7dd9430c675a9177d55bcdae9265159fc04bd11` in its run manifests.

Run each command three times in a fresh process from the repository root:

```text
uv run --locked python scripts/benchmark_m02.py --rows 2
uv run --locked python scripts/benchmark_m02.py --rows 10000
uv run --locked python scripts/benchmark_m02.py --rows 50000
```

The [benchmark script](../../scripts/benchmark_m02.py) uses the bundled sample for two rows and the fixed seed 0 benchmark generator for larger workloads. The timer covers opening new local state, registering the bundle, validating, calculating, publishing, committing and reopening the verified result. Process startup, fixture generation, browser and Streamlit rendering are outside the timer. Peak memory is the OS-reported working set high-water mark for the entire benchmark process. Each trial starts with a new temporary SQLite and artifact directory.

| Loans | Bundle bytes | Elapsed trials (s) | Median (s) | Peak working set trials (MiB) |
|---:|---:|---|---:|---|
| 2 | 593 | 0.4205, 0.3630, 0.3763 | 0.3763 | 35.63, 35.72, 35.62 |
| 10,000 | 701,337 | 1.0734, 1.0072, 1.1166 | 1.0734 | 49.99, 49.89, 49.99 |
| 50,000 | 3,504,973 | 4.2237, 3.8441, 3.9274 | 3.9274 | 104.16, 105.57, 105.56 |

Each workload returned the same input and metric hashes across all three trials.

| Loans | Framed input SHA-256 | Semantic metric SHA-256 |
|---:|---|---|
| 2 | `2f8c471f864a16f8bef33f2258800bef7d58df9b4ca6394bf9c34654c00efdc7` | `c46f0f89f6d913b649ea5c75ceaebd1e78a0beabd962042102d2c404bd605d10` |
| 10,000 | `39f405f0c0ee350dff62aa4aae381ef656466309b9b32190b947cc275921eea9` | `bf90a835995d598c754664b83e610c13bd301cff266d161b00cf30bc505cf85e` |
| 50,000 | `7f4df6a43c04e0070cb3cb88c5998c039de44ca53d2bf51e4816fe7fc44af0e2` | `3d1a62c37d357f8271fb7eaaac244384384a56efebd1430da96f376e82ab799d` |

## Proposed OQ-008 local targets

Apply these thresholds to the slowest of three elapsed trials and the highest working set on the measured workstation or a comparable environment.

| Loans | Maximum elapsed time (s) | Maximum peak working set (MiB) |
|---:|---:|---:|
| 2 | 1.0 | 64 |
| 10,000 | 2.0 | 80 |
| 50,000 | 6.0 | 160 |

The proposed limits allow for local filesystem and interpreter variation across these fixed workloads. The largest bundle exercises the approved row cap with about 3.34 MiB of input. The separate exact byte and field caps are covered by boundary tests. Browser performance, other hardware and combined worst-case workload shapes remain outside this measurement.


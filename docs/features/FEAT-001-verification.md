# FEAT-001 verification and OQ-008 measurements

Status: Proposed
Version: 1.0
Last Updated: 2026-11-10
Applicability: M02

Implementation revision in this repository: `8c0c37a785b3dc7563201544b7229c9bb5a90054`.

The original verification used the archived checkout. Its runtime source, tests, dashboard configuration, benchmark script and dependency lockfile match the revision above byte for byte.

Verification date: 2026-11-10, America/Buenos_Aires.

## Functional verification

The locked quality checks ran in a clean worktree at the implementation revision. All six commands passed. Pytest collected and passed 117 cases, including 102 product cases and 15 repository governance cases. The documentation checker verified 67 Markdown files at that revision. The [traceability matrix](../05-testing/traceability.md) links implementation to requirements.

Local quality commands:

```text
uv sync --locked --group dev
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src scripts
uv run --locked pytest
uv run --locked python scripts/check_baseline.py
```

| M02 criterion | Evidence at the implementation revision |
|---|---|
| AC-DQ-001 | `test_FR_DQ_001_sample_identity_and_restart` and `test_FR_DQ_001_changed_configuration_and_separate_keys` cover valid ingestion, ownership, replay and key conflicts. |
| AC-DQ-002 | `test_FR_DQ_002_catalog` and `test_FR_DQ_002_ordinal_and_nullable_segment` cover strict input defects, ordinal locations and the unspecified group. `test_FR_DQ_002_invalid_manifest_blocks_metrics` verifies whole-input rejection. |
| AC-DQ-003 | Parser, byte, row, field, numeric and diagnostic limit cases in `tests/contract/test_bundle.py` and `tests/integration/test_analysis.py` check bounds, incomplete reports and wide aggregates. |
| AC-RISK-001 | `tests/unit/test_metrics.py` checks sample totals, exact operands, rounding, availability and group totals. `test_CT_004_CT_015_CT_016_cross_validation` rejects an inconsistent stored rate. `test_NFR_REL_002_semantic_hash_ignores_row_order_and_raw_encoding` compares semantic hashes. |
| AC-UI-001 | `tests/e2e/test_dashboard.py` checks sample and manual results, errors, empty data, reruns, linked new analysis, reopened history and the selected run's updated status after recovery. See the browser evidence below. |
| AC-OBS-001 | `test_FR_OBS_001_versions_events_and_scoped_evidence` verifies versions, effective limits, events, provenance and run scoping. `test_CT_003_requires_exact_kind_locator_pair` exercises all 16 pairings in three representations. `test_CT_003_CT_011_persisted_contract_violation_preserves_evidence` verifies controlled integrity errors and unchanged data. |
| AC-OBS-003 | `test_FR_OBS_003_publication_and_restart` injects interruption across creation, publication and commit. Additional integration cases check retention, cleanup, missing or corrupted artifacts and store failure. `test_CT_016_resume_retains_the_original_import_key`, `test_CT_018_publication_metadata_commits_with_its_artifact` and `test_CT_018_pre_correction_result_opens_unchanged` verify recovery and compatibility. |

## Browser evidence

Playwright drove Microsoft Edge 157.0.4341.42 against the actual Streamlit process on loopback. The browser workspace used fresh synthetic state, and the server ran the same implementation revision as the locked checks.

- **Sample.** Verified USD 400.00, 50.00% and 75.00%, the exact operands, and both concentration tabs.
- **Manual input.** Uploaded a synthetic one-loan USD bundle with USD 160.00 outstanding. A second manifest with unsupported currency produced a diagnostic that identified the currency field. Reusing the valid snapshot ID with changed bytes produced `identity_conflict`. A 65,537-byte manifest produced `resource_limit`.
- **History and refresh.** Selected existing sample and manual runs. **New analysis** created a different run ID and preserved the parent's ID in provenance. Browser refresh retained the selected child.
- **Recovery.** Injected interruption before the final metadata transaction, restarted the Streamlit process, and selected the pending analysis. **Resume analysis** completed the original run, advanced its revision and displayed `Succeeded` in history without a browser refresh.

The live page had no page-level horizontal overflow at a width of 430 pixels.

## Measured workload

Measurements ran on Windows 11 build 26200, Intel Core i3-N305, eight logical processors, 7.63 GiB physical memory, CPython 3.12.13, Pydantic 2.14.3 and Streamlit 1.67.0 from `uv.lock`. All nine trials ran from the clean implementation revision above. The runtime source SHA-256 recorded by that Windows checkout was `fda77c5eb6f33074791a2584484eabc82bdd4d1fc809f87a49b6ef4ba0f90bc6`.

Run each command three times in a fresh process from the repository root:

```text
uv run --locked python scripts/benchmark_m02.py --rows 2
uv run --locked python scripts/benchmark_m02.py --rows 10000
uv run --locked python scripts/benchmark_m02.py --rows 50000
```

The [benchmark script](../../scripts/benchmark_m02.py) uses the bundled sample for two rows and the fixed seed 0 benchmark generator for larger workloads. The timer covers opening new local state, registering the bundle, validating, calculating, publishing, committing and reopening the verified result. Process startup, fixture generation, browser and Streamlit rendering are outside the timer. Peak memory is the OS-reported working set high-water mark for the entire benchmark process. Each trial starts with a new temporary SQLite and artifact directory.

| Loans | Bundle bytes | Elapsed trials (s) | Worst (s) | Peak working set trials (MiB) | Worst (MiB) |
|---:|---:|---|---:|---|---:|
| 2 | 593 | 0.3274, 0.4070, 0.3942 | 0.4070 | 36.84, 36.68, 36.90 | 36.90 |
| 10,000 | 701,337 | 1.3917, 1.2743, 1.2623 | 1.3917 | 51.59, 51.62, 51.58 | 51.62 |
| 50,000 | 3,504,973 | 4.7889, 4.6892, 4.7068 | 4.7889 | 105.27, 105.82, 106.50 | 106.50 |

Each workload returned the same input and metric hashes across all three trials.

| Loans | Framed input SHA-256 | Semantic metric SHA-256 |
|---:|---|---|
| 2 | `2f8c471f864a16f8bef33f2258800bef7d58df9b4ca6394bf9c34654c00efdc7` | `c46f0f89f6d913b649ea5c75ceaebd1e78a0beabd962042102d2c404bd605d10` |
| 10,000 | `39f405f0c0ee350dff62aa4aae381ef656466309b9b32190b947cc275921eea9` | `bf90a835995d598c754664b83e610c13bd301cff266d161b00cf30bc505cf85e` |
| 50,000 | `7f4df6a43c04e0070cb3cb88c5998c039de44ca53d2bf51e4816fe7fc44af0e2` | `3d1a62c37d357f8271fb7eaaac244384384a56efebd1430da96f376e82ab799d` |

## Proposed OQ-008 local targets

Apply these thresholds to the slowest of three elapsed trials and the highest working set on the measured workstation or a comparable environment.

| Loans | Maximum elapsed time (s) | Maximum peak working set (MiB) | Observed comparison |
|---:|---:|---:|---|
| 2 | 1.0 | 64 | Within both proposed targets |
| 10,000 | 2.0 | 80 | Within both proposed targets |
| 50,000 | 6.0 | 160 | Within both proposed targets |

The proposed limits allow for local filesystem and interpreter variation across these fixed workloads. The largest bundle exercises the approved row cap with about 3.34 MiB of input. The separate exact byte and field caps are covered by boundary tests. Browser performance, other hardware and combined worst-case workload shapes remain outside this measurement.

Each accepted M02 functional criterion has recorded evidence. OQ-008 measured performance remains open pending explicit Product Owner approval of the three targets. That decision gates M02 closure.

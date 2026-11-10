# FEAT-001: Deterministic portfolio analysis

Status: Proposed
Version: 1.0
Last Updated: 2026-11-10
Applicability: M02

## Problem and scope

A local analyst needs to inspect a controlled synthetic USD portfolio, understand why an import was rejected, and return to the same analysis after restarting the application. This feature implements the M02 path of UC-001 within the exact scope of [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md).

The owner's M02 task of 2026-11-10 authorizes this feature and selects a bundled sample. Use a versioned, fixed synthetic fixture with seed 0, two open loans, USD 100.00 and USD 300.00 outstanding, and 0 and 5 days past due. The fixture is distributed with the application and uses a CT-001 manifest and source checksum. Its input and output go through the same path as manual uploads.

## Interaction

1. Open the local Streamlit dashboard. Select **Analyze sample**, or provide both a loan CSV and a JSON manifest and select **Analyze**. Labels and diagnostic messages are in English.
2. For valid input, show the observation date, USD, run ID and revision, loan and open loan counts, total exposure, and both delinquency rates. Show exact operands, quantized values, and unavailable reasons. List all borrower and segment group shares and label the null segment **Unspecified (blank)**. Show a valid empty portfolio as an empty population.
3. For invalid input, show import disposition, the safe report with codes and record/field locations, and whether diagnostic scanning was complete. Distinguish validation rejection, identity/key conflict, safety limit, and operational failure. Display integrity and persistence failures as errors.
4. Keep the import and analysis keys for an identical submission during Streamlit reruns. Ordinary reruns and history selection read committed state. On restart, list saved runs and allow a user to open one without creating an analysis.
5. For a verified terminal run with a complete stored bundle, **New analysis** executes a fresh analysis key with that run as parent and reuses the immutable input. For interrupted work, **Resume analysis** repeats the deterministic operation with the saved request and original run identity. These actions preserve the selected run's existing history.

## Operations and contracts

- Register an input bundle from its bytes and effective parser limits. Return an opaque bundle reference, with an explicit incomplete-input condition if the full bytes cannot be read within the limits. The store resolves references within the workspace state root.
- Execute a CT-016 request in `deterministic_m02` mode with exactly `validate_portfolio` and `calculate_metrics`. Return CT-011 and CT-015 and, for valid durable success, CT-004. List and retrieve run projections, and resolve CT-003 evidence only within the selected run. Use the M02 variants of CT-003, the CT-005 shared finding envelope, and CT-011.
- Enforce CT-001 and CT-002, CT-019 precedence and diagnostic catalog, and the accepted CT-020 profile. Use CT-017 framing, exact integer minor units and count operands, and half-even quantization. Preserve raw bytes, semantic hashes, effective configuration, immutable versions and safe typed events.
- Follow CT-018 and the accepted M02 lifecycle. Stage and verify content-addressed files before committing their references in SQLite. Serialize mutations in the local process. Recover unfinished work and verify committed state before displaying it. Missing or corrupt committed artifacts raise integrity errors. Retain state until explicit whole-state operator cleanup.
- The accepted directions in ADR-002, ADR-003, ADR-004, ADR-007, ADR-008 and ADR-009 apply. Use Pydantic for strict boundary DTOs, standard Python for the domain, SQLite through `sqlite3`, and Streamlit for presentation. Resolve and pin runtime dependencies in `uv.lock`. M03 and M04 capabilities follow their own gates.

## Acceptance and planned verification

| Accepted criterion | Planned evidence |
|---|---|
| AC-DQ-001 | Sample and manual bundle verification, strict framing and schema, full and semantic hashes, import and analysis replay, changed bytes and configuration conflicts, cross-portfolio ownership, new run on existing data. |
| AC-DQ-002 | Missing and extra fields, duplicate rows and JSON keys, bad encoding and wire values, impossible or future dates, currency and loan invariants, source hash mismatch, null segment and empty snapshot. EVAL-DQ-001/002/003 deterministic cases. |
| AC-DQ-003 | Exact and exceeded total/manifest bytes, rows, UTF-8 field bytes and numeric token lengths, invalid profile, and diagnostic cap with explicit incomplete report. Verify wide output sums. |
| AC-RISK-001 | Sample USD 400.00, 1/2 and 300.00/400.00 with 0.5000 and 0.7500. Test 1/3 and half-even ties 1/32 and 3/32, empty/closed/zero-principal cases, group sums and null segment, and replay with equal semantics and distinct byte provenance. EVAL-RISK-001 exact metrics portion. |
| AC-UI-001 | Streamlit tests for sample, manual upload, error and unavailable states, reruns, linked new analysis and history after restart. Local visual inspection of the actual dashboard. |
| AC-OBS-001 M02 | Assert run-owned evidence, artifact and semantic hashes, effective limits, exact versions, events, sanitized errors and absence of provider fields. |
| AC-OBS-003 | Inject interruption before publish, before commit and after commit. Verify restart, unfinished-run resume, integrity failures, storage failures, no duplicate results, path confinement and whole-state cleanup. |

## GOV-002 readiness

The accepted baseline and the per-ID approval of FR-DQ-001/002/003, FR-RISK-001, FR-UI-001, FR-OBS-001 M02 and FR-OBS-003 supply the requirements and acceptance criteria above. The accepted ADRs and the closed M02 portions of OQ-001, OQ-008, OQ-009 and OQ-010 supply the decisions needed to implement the slice. This document records the task authorization, problem, inputs, outputs, interaction, contracts, edge cases and test design. The M02 implementation gate is satisfied for this scope.

OQ-008 measured performance gates milestone completion. The [verification report](FEAT-001-verification.md) records the environment, workloads, commands, source revision, measured time and memory, and targets proposed for owner approval. GOV-003 requires executed checks and actual implementation/test references.

## Contract correction

The 2026-11-10 closure task corrects enforcement of the accepted M02 contracts under ADR-002 and ADR-003. CT-003 requires the exact locator type selected by `kind`. Retrieval checks the run, artifact kind and locator target. CT-004, CT-005, CT-011, CT-015, CT-016 and CT-019 checks cover metric availability and operands, finding scope, terminal state, effective configuration, lineage and committed event references. An unfinished replay continues with its original request.

Valid records from the initial implementation remain readable without rewriting their metadata or artifacts. Legacy report text remains readable under its original field name and reanalysis reuses the stored report hash. New CT-018 publication metadata is written transactionally alongside the existing artifact reference. A mismatched persisted record returns `integrity_error` and keeps its original data for diagnosis. These corrections enforce the approved semantics and preserve the active M02 scope.

History labels refresh when recovery advances the selected run's status. The selected run retains its original identity through the update.

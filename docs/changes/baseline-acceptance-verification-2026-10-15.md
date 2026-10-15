# Baseline acceptance recording verification

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

## Recorded decision
The human Product Owner explicitly approved RiskLens Specification Baseline v1.0 with decision ACCEPT WITH EXPLICIT DEFERRALS on 2026-10-15, America/Buenos_Aires. The reviewed specification SHA remains archived baseline review revision. The prepared acceptance scope remains preserved at archived acceptance preparation revision.

[BASELINE-ACCEPTANCE-001](BASELINE-ACCEPTANCE-001.md) is now Accepted and records the exact accepted documents/sections, IDs, clauses, variants, eight individual ADRs, owner role/date and unchanged deferrals. The user supplied the approval as Product Owner; no personal name or signature was invented. Acceptance recording changes approval metadata only, not normative product behavior.

## Scope and current status
- GOV-001 through GOV-004, P-001 through P-021 and STYLE-001 through STYLE-003 are Accepted in their approved governance/direction documents.
- Accepted M02 scope: FR-DQ-001/002/003, FR-RISK-001, FR-UI-001, FR-OBS-001 M02 only, FR-OBS-003; corresponding AC-DQ-001/002/003, AC-RISK-001, AC-UI-001, AC-OBS-001 M02 only, AC-OBS-003.
- Accepted NFR clauses: NFR-SEC-001 M02 core, NFR-PERF-001 safety/calibration policy, NFR-OBS-001 M02 lineage, NFR-MNT-001, NFR-REL-002, NFR-SEC-002 M02 retention. Unresolved measured values and later clauses remain Proposed/Open.
- Accepted rules: BR-DQ-001/002/003/004, BR-RISK-001/002/005 and BR-RISK-003 raw metrics only. BR-RISK-006 remains Deprecated.
- Accepted contracts: CT-001/002/004/005/015/016/017/018/019/020 and M02 variants of CT-003/011, including the DQ-only shared finding envelope and exact CT-020 safety profile.
- UC-001, M02 domain sections and approved local architecture/security/observability subsets are explicitly accepted. Mixed-stage document headers remain Proposed.
- ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008 and ADR-009 are Accepted individually. ADR-001 remains Proposed. ADR-005 accepts deferral, not a vector store; ADR-006 accepts a boundary, not a provider.
- OQ-008 M02 safety is CLOSED. OQ-001 and the M02 portions of OQ-009/010 remain CLOSED. Default/DTI/score deferrals and every later question/gate are unchanged. Measured performance remains open before M02 milestone release; AI budgets remain later.

## Verification execution
Executed locally on 2026-10-15 using Python 3.12.13:

| Check | Observed result |
|---|---|
| uv sync --locked --group dev | PASS; 23 packages resolved/checked, dependency declarations and lock unchanged. |
| uv run --locked ruff check . | PASS. |
| uv run --locked ruff format --check . | PASS; 69 files already formatted. |
| uv run --locked mypy src scripts | PASS; 3 source files. |
| uv run --locked pytest | PASS; 15 governance tests, including 7 negative document fixtures. |
| uv run --locked python scripts/check_baseline.py | PASS; Markdown documents in the archived checkout. Covers configured links, metadata, style, identifiers, traceability, milestone boundaries, mixed acceptance and global identity checks. |
| git diff --check | PASS. |
| Acceptance-scope comparison | PASS; accepted FR/NFR/AC/BR/CT/ADR sets exactly match the prepared record. Later OQ rows are unchanged; only the approved M02 safety/platform/retention portions have current approval metadata. |
| Behavioral text comparison | PASS; every FR/AC/CT behavior matches the prepared revision after excluding acceptance metadata and CT-020 approval-state wording. Every NFR/BR cell except Status is unchanged. No formula, field, enum, default value, invariant or failure rule changed. |
| Deferred specification comparison | PASS; ADR-001 and all seven graph/RAG/AI specification files are unchanged. Mixed headers remain Proposed; BR-RISK-006 remains Deprecated. |
| Product/tooling/feature diff | PASS; src, tests, scripts, CI configuration, pyproject.toml and uv.lock unchanged. No feature Markdown file created. |

The scope/behavior comparison was a temporary read-only review check against archived acceptance preparation revision; it did not add product code or persistent tests. Acceptance status and future gates were also reviewed directly. No product test, runtime behavior, financial calculator, database/UI execution, live model evaluation or remote CI result is claimed. Passing governance checks do not prove the unimplemented product.

## Recommended next task
Separately authorize preparation of FEAT-001, Deterministic snapshot import and analysis, under GOV-002. The future specification should cover synthetic CSV/manifest inputs, typed validation/conflict/limit outcomes, exact metrics and availability, local publication/lineage/replay/restart, and the Streamlit presentation path. Trace it to the accepted M02 IDs and criteria above; specify meaningful offline tests and failure cases before implementation. No AI, graph checkpoint or human-review dependency is required.

No feature specification is created in this task. No M02 implementation, product test implementation, dependency change, push or publication is authorized or performed.

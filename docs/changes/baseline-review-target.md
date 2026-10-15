# Final baseline review target

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

Review target commit: archived baseline review revision
Review target parent: archived baseline review parent
Review target message: spec: finalize RiskLens baseline v1.0 for acceptance
Acceptance state: NOT ACCEPTED.

This locator identifies the final verified Proposed revision. A subsequent metadata-only commit contains this pointer, the prepared acceptance record and CR-001 execution metadata only. It does not alter reviewed normative behavior or constitute acceptance. The [final closure report](../00-project/baseline-closure-report.md) records verification of the target. The exact proposed document/ID/variant subsets and retained gates are in [BASELINE-ACCEPTANCE-001.md](BASELINE-ACCEPTANCE-001.md), with Approval State Awaiting Owner Approval. Actual accepted sets remain empty. GOV-001 requires explicit human approval of this immutable revision and exact scope before changing acceptance status.

## Preserved earlier targets
The earlier corrected proposal remains at archived corrected proposal revision, parent archived initial proposal revision, message `docs: correct proposed baseline under CR-001 owner decisions`. Its pointer was recorded in archived baseline review parent. No owner acceptance of that revision was received. The pre-correction proposal and historical review remain preserved in Git. The final target above is the current approval candidate.

## Next human action
Review the final target commit and prepared record, including CT-020's six unchanged provisional safety settings. Approve or amend the exact proposed subsets and retained gates explicitly. Only after receiving that decision may a separate governance task complete the pending record and update the approved IDs/variants and individual ADRs. M02 feature preparation/implementation remains a separate task.

## Suggested approval wording, not an approval received
```text
I approve the Proposed RiskLens Specification Baseline v1.0 at
archived baseline review revision with exactly the proposed
document sections, IDs, NFR clauses and variants listed in
BASELINE-ACCEPTANCE-001.md, including CT-020's provisional safety profile
and the individually listed ADR-002, ADR-003, ADR-004, ADR-005, ADR-006,
ADR-007, ADR-008 and ADR-009. Retain every listed deferral and mixed-stage
Proposed boundary, including ADR-001. Record my identity and approval date
under GOV-001. Do not start M02.
```

No human approval of that target has been received. Do not treat the example above as authorization.

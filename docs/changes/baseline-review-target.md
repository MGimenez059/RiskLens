# Corrected baseline review target

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

Review target commit: archived corrected proposal revision
Review target parent: archived initial proposal revision
Review target message: docs: correct proposed baseline under CR-001 owner decisions
Acceptance state: NOT ACCEPTED.

This locator identifies the verified corrected Proposed revision. A subsequent metadata-only commit records this pointer and the CR execution checklist; it does not change the reviewed normative specification or constitute acceptance. The prospective accepted IDs and deferred sections are in [baseline-correction-report.md](../00-project/baseline-correction-report.md). GOV-001 requires explicit human approval of this exact immutable revision before changing any acceptance status.

## Next human action
Review the target commit, the report's exact approval subset, CT-020's six provisional safety settings and the retained later gates. Approve or amend them explicitly. After approval, a separate governance task creates the acceptance record referencing the SHA above and updates only the approved IDs/variants and ADRs. M02 implementation remains a separate task.

## Suggested approval wording, not an approval received
```text
I approve the corrected Proposed RiskLens Specification Baseline v1.0 at
archived corrected proposal revision with the prospective approval
scope in baseline-correction-report.md, including CT-020 safety defaults
and ADR-002 through ADR-009. Keep ADR-001 and the specified later-stage
details Proposed behind their recorded gates. Record this acceptance
under GOV-001. Do not start M02.
```

No human approval of that target has been received. Do not treat the example above as authorization.

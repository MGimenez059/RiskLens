# CR-001: Correct baseline acceptance boundaries

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

- ID: CR-001
- Owner: Product owner.
- Technical reviewer: Current architecture review agent.
- Date: 2026-10-14
- Current baseline: Corrected Proposed v1.0; baseline acceptance pending.
- Pre-correction source commit: archived initial proposal revision.
- Initial corrected review target: archived corrected proposal revision, preserved historical Proposed revision.
- Final reviewed target: archived baseline review revision, verified Proposed; details in baseline-review-target.md.
- Prepared acceptance record: BASELINE-ACCEPTANCE-001.md, Approval State Awaiting Owner Approval; actual accepted sets empty.
- Decision: Owner correction decisions recorded in owner-decisions-2026-10-14.md; exact corrected baseline and ADR acceptance pending GOV-001.

## Pre-correction behavior
The baseline retains Default as a possible v1 release blocker, requires an unavailable default metric stub, leaves ratio precision unresolved, mixes later review states into M02 UI acceptance, and permits M03 recommendations before M04 human review. Other identity, validation-result and persistence contracts need clarification.

## Proposed behavior and motivation
Use the findings and exact source IDs in the [Baseline Acceptance Review](../00-project/baseline-acceptance-review.md). The proposal limits M02 to deterministic local analytics and preserves complete-population calculation. Default is deferred beyond current v1 with no invented definition. Raw concentration shares are separate from detector thresholds. M03 synthesis is restricted to observations and investigation suggestions until M04 business-action review is available.

The owner authorized correction of the Proposed canonical specifications. USD/exposure/global identity/platform/retention decisions are recorded and applied. CT-015 through CT-020 and FR-DQ-003/FR-OBS-003 supply the missing M02 contracts and verification boundaries. Exact provisional safety values await review of the final commit; empirical performance and AI budgets remain separately open. Later graph, policy and copilot details stay Proposed behind feature-readiness gates. See the [final closure report](../00-project/baseline-closure-report.md) and [prepared record](BASELINE-ACCEPTANCE-001.md). The baseline-correction-report.md and earlier acceptance review retain prior correction/review evidence.

## Impact analysis

| Area | Required revision |
|---|---|
| Scope and roadmap | Remove Default from current-v1 release dependency; separate M02 metrics and M03 alerts; align M03/M04 review boundary. |
| Requirements | FR-DQ-001/002, FR-RISK-001/002, FR-AI-001/003, FR-UI-001/002, FR-OBS-001; NFR-PERF-001 and NFR-SEC-002; later FR/NFR applicability as listed in the review. |
| Acceptance criteria | AC-DQ-001/002, AC-RISK-001/002, AC-AI-001/003, AC-UI-001/002, AC-OBS-001 and affected later-stage criteria. |
| Domain/rules/contracts | BR-DQ-001/002/003, BR-RISK-001/002/003/005/006; CT-001/003/004/005/011 and later CT-007/009/010/012/013/014; explicit request/configuration/result/event contracts before readiness. |
| ADRs | Clarify ADR-003/004/007 for M02; keep ADR-001 Proposed; accept ADR-005 only as deferral if approved. No accepted ADR exists to supersede. |
| Tests/evals | Add zero-exposure count-rate, repeating-decimal, identity-collision, nonblocking-null, complete-population rejection and interrupted-publication cases; retain planned status until implemented. No tests are declared passed for product behavior. |
| Traceability | Map each revised/new ID to applicable milestone, contract, rule, planned test and eval. |
| Security/cost | Keep local synthetic operation; define parser limits without inventing risk thresholds; no M02 provider cost requirement. |
| Compatibility | No product payloads or database exist. Proposed contract changes need no runtime migration; preserve their proposal history. |

## Approval and execution evidence
- [x] Owner correction decisions recorded; corrected Proposed specifications prepared.
- [x] Corrected Proposed revision committed and identified; human review/acceptance of that exact target remains pending.
- [ ] Human approval recorded with reviewer/date/commit and deferred gates.
- [x] Canonical Proposed specifications corrected without product implementation.
- [ ] Accepted ADRs and per-ID statuses updated explicitly.
- [x] Requirement/contract traceability updated; product tests remain planned.
- [x] CHANGELOG records the applied specification revisions.
- [x] Prior correction verification retained in baseline-correction-report.md; final closure verification recorded in baseline-closure-report.md.
- [x] Exact review-target SHA recorded after commit in baseline-review-target.md.
- [x] Final closure verifies REVIEW-001 through REVIEW-006, REVIEW-007 scope, REVIEW-015 and REVIEW-016 without product implementation.
- [x] Final specification review target committed; prepared record pins its exact SHA and proposed per-ID/variant scope.
- [x] Post-target metadata verification passed: 63 Markdown documents and 15 governance tests; reviewed normative paths unchanged.
- [ ] Owner acceptance of the final target and exact subsets received; no approval inferred from preparation.
- [ ] Later applicable product tests/evals implemented and executed in their features.

This CR proposes specification changes only. It does not authorize the first vertical slice or require implementing product functionality during this review.

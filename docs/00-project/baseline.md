# RiskLens Specification Baseline v1.0

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the document/section scope recorded there is accepted; later feature gates remain in force.

The Product Owner accepted the specified v1 direction and M02 subsets with explicit deferrals under BASELINE-ACCEPTANCE-001. Product functionality is NOT IMPLEMENTED. Initial executable code is limited to repository verification and development tooling.

## Canonical reading order
1. [Principles and precedence](principles.md), [writing policy](writing-policy.md).
2. [Vision](vision.md), [scope](scope.md), [glossary](glossary.md).
3. [Requirements](../01-requirements/functional-requirements.md), [NFRs](../01-requirements/non-functional-requirements.md), [acceptance criteria](../01-requirements/acceptance-criteria.md).
4. [Domain](../02-domain/domain-model.md), [business rules](../02-domain/business-rules.md), [contracts](../02-domain/data-contracts.md).
5. [Architecture](../03-architecture/architecture.md), [graph](../03-architecture/graph-spec.md), [ADRs](../adr/README.md).
6. [Evaluations](../04-ai/evaluation-spec.md), [traceability](../05-testing/traceability.md).
7. [Open decisions](open-questions.md), [final closure report](baseline-closure-report.md), [correction report](baseline-correction-report.md), [owner decisions](../changes/owner-decisions-2026-10-14.md). Historical [acceptance review](baseline-acceptance-review.md) and [initial report](review-report.md) retain prior findings and are not current normative behavior.

## GOV-001: Human acceptance
Initial status is Proposed. The user is the product owner. An agent cannot approve this baseline.
An acceptance record in `docs/changes/` must identify the reviewed commit, baseline version, reviewer, date, accepted documents, individually accepted ADRs, exceptions, and deferred decisions with their implementation gates. Update document statuses explicitly after approval. Proposed documents alone never authorize product implementation.
The owner may accept the architecture direction while deferring decisions that do not block the next slice. Undefined financial semantics cannot be accepted as implementation-ready behavior.
Owner approval on 2026-10-15 explicitly identifies reviewed commit archived baseline review revision and the exact document/ID/variant scope in BASELINE-ACCEPTANCE-001. That record now records ACCEPT WITH EXPLICIT DEFERRALS. A prepared Draft/Proposed record alone never satisfies human acceptance. This approval does not authorize M02 implementation or accept deferred M03/M04 details.
Mixed-stage containers stay Proposed. Each normative requirement/rule/contract has Status and Applicability. The acceptance record enumerates accepted IDs and variants; unresolved later variants remain Proposed. Reject blanket acceptance of a mixed container while it contains Proposed or deferred sections.
Changes to Proposed documents are recorded in CHANGELOG. After acceptance, use the CR process. Allowed statuses: Draft, Proposed, Accepted, Deprecated, Superseded. Document versions are independent of product versions. Never reuse retired IDs.

## GOV-002: Definition of Ready
A feature requires an accepted baseline, approved requirement ID, problem statement, inputs, outputs, acceptance criteria, affected contracts, edge cases, specified tests/evals, accepted relevant ADRs, and resolved questions affecting that slice. Record these in a feature specification under `docs/features/` when the first feature is prepared. Do not create empty specifications now.

## GOV-003: Definition of Done
Behavior matches approved specifications. Relevant tests, Ruff, mypy, and pytest pass. Contracts, canonical documentation, and traceability reference actual implementation and tests. Behavioral changes have a CR; architectural changes have an ADR; AI changes have corresponding evals. Planned test names do not count as executed tests. Report reproducible evidence and remaining limitations.

## GOV-004: SDD sequence
Specification, contracts, acceptance criteria, tests/evals, implementation, validation, in that order. Repository governance tests in this phase do not validate the future product. Do not create empty product tests to imply coverage.

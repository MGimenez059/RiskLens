# Corrected Proposed Baseline Review

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## Current disposition
Recommendation: **ACCEPT WITH EXPLICIT DEFERRALS**, subject to human approval of the exact corrected review target and the Provisional Local Safety Limits. The corrected baseline and every ADR remain Proposed. Product functionality is NOT IMPLEMENTED. No M02 feature work is authorized by this correction.

The prior review and initial baseline are preserved in Git commit archived initial proposal revision. This report applies the [owner decisions](../changes/owner-decisions-2026-10-14.md) under [CR-001](../changes/CR-001-baseline-acceptance-corrections.md). The prior [acceptance review](baseline-acceptance-review.md) is historical evidence; its pre-correction DO NOT ACCEPT recommendation is not the current review outcome.

The exact reviewed commit will be recorded in [the review-target locator](../changes/baseline-review-target.md) after the verified Proposed revision is committed. That locator does not constitute acceptance. GOV-001 still requires a human approval record referencing that commit and enumerating accepted IDs/variants, individual ADRs and deferred gates. No status will be changed merely because a review target exists.

## 1. Files changed
Exactly 50 repository files are modified or added relative to pre-correction commit archived initial proposal revision:

```text
.gitignore
AGENTS.md
CHANGELOG.md
README.md
docs/00-project/baseline-acceptance-review.md
docs/00-project/baseline-correction-report.md
docs/00-project/baseline.md
docs/00-project/glossary.md
docs/00-project/open-questions.md
docs/00-project/review-report.md
docs/00-project/roadmap.md
docs/00-project/scope.md
docs/01-requirements/acceptance-criteria.md
docs/01-requirements/functional-requirements.md
docs/01-requirements/non-functional-requirements.md
docs/01-requirements/use-cases.md
docs/02-domain/business-rules.md
docs/02-domain/data-contracts.md
docs/02-domain/domain-model.md
docs/03-architecture/architecture.md
docs/03-architecture/graph-spec.md
docs/03-architecture/observability.md
docs/03-architecture/rag-spec.md
docs/03-architecture/security.md
docs/04-ai/agent-responsibilities.md
docs/04-ai/evaluation-spec.md
docs/04-ai/guardrails.md
docs/04-ai/prompt-specs.md
docs/04-ai/tool-contracts.md
docs/05-testing/test-strategy.md
docs/05-testing/traceability.md
docs/adr/ADR-001-langgraph.md
docs/adr/ADR-002-validation.md
docs/adr/ADR-003-persistence.md
docs/adr/ADR-004-ui.md
docs/adr/ADR-005-retrieval.md
docs/adr/ADR-006-providers.md
docs/adr/ADR-007-observability.md
docs/adr/ADR-008-repository.md
docs/adr/ADR-009-tooling.md
docs/adr/README.md
docs/changes/CR-001-baseline-acceptance-corrections.md
docs/changes/baseline-review-target.md
docs/changes/owner-decisions-2026-10-14.md
scripts/check_baseline.py
tests/test_baseline.py
tests/test_governance_regressions.py
```

Changes are specifications, documentation/navigation, the state ignore rule and governance checks. src/risklens, pyproject.toml and uv.lock are unchanged. Temporary authoring helpers are outside the repository and are not product code. The review-target locator is updated after the correction commit solely to identify its exact SHA.

## 2. New requirement, rule and contract IDs
- FR-DQ-003 and AC-DQ-003: bounded parser/resources and complete versus capped diagnostic reporting.
- FR-OBS-003 and AC-OBS-003: local artifact publication, restart readability and replay without graph checkpoints.
- BR-DQ-004: safety/disposition enforcement.
- CT-015: Import and Validation Result.
- CT-016: Analysis Request and Analysis Configuration.
- CT-017: Arithmetic Serialization and Canonical Hashing.
- CT-018: Local Artifact Publication and Recovery.
- CT-019: Typed Events and Validation Catalogs.
- CT-020: Bounded Parser Configuration.

Each new contract states purpose, fields, invariants, failure behavior, acceptance criteria, edge cases and traceability. All remain Proposed. Contract coverage has a row for every CT-001 through CT-020. Product test identifiers remain planned.

## 3. Closed and split questions
OQ-001 is CLOSED by recorded USD/exposure/import/global-identity decisions. OQ-002 current-v1 scope is CLOSED by exclusion; its financial definition is deferred post-v1. OQ-003 is deferred outside current v1. OQ-009 M02 platform and OQ-010 M02 retention are CLOSED; graph/review and later targeted-deletion portions stay OPEN.
OQ-008 is split into Proposed M02 safety configuration, OPEN measured-performance calibration and OPEN later AI budgets. OQ-004/005/006/007/011/012 remain OPEN at M03/M04 gates. Closing an owner question does not accept the baseline or claim implementation.

## 4. ADR statuses
ADR-001 remains Proposed and blocked by graph/checkpoint coordination details. ADR-002 through ADR-009 remain Proposed and prepared for explicit human acceptance. ADR-005 accepts deferral only when approved; it selects no embedding/vector store. The owner selected SQLite/immutable artifacts/Streamlit for local single-user v1, with independent domain logic.

## 5. Remaining Proposed areas and gates
- All document and per-ID statuses remain Proposed except the retired BR-RISK-006 stub, which is Deprecated and outside active v1.
- M03 detector thresholds, temporal meaning, policy authority/coverage, embedding/index/sufficiency, model/prompt/eval selection and graph-checkpoint adapter require their own Definition of Ready.
- M04 reviewer identity, review aggregation, high-impact recommendations and copilot audit/history remain gated.
- Later targeted deletion/retention is not resolved by the M02 whole-state operator cleanup decision.
- M02 safety defaults are explicit technical proposals to approve against this commit; measured performance targets are not invented and must be calibrated before declaring the working milestone/release complete.

## 6. Resolved findings
| Finding | Corrected behavior |
|---|---|
| REVIEW-001 | Exact minor-unit/count operands, quantized four-digit ratio strings and half-even ties, exact comparison and canonical hashing in CT-017. No implicit decimal-context rounding. |
| REVIEW-002 | Denominator-specific availability; open zero-principal count eligibility. AC-RISK-001 includes 1/3, zero exposure/nonzero count, zero eligible population and ties. |
| REVIEW-003 | Raw group exposure/shares in M02 metrics; configured concentration/anomaly alerts in M03. |
| REVIEW-004 | M02 criteria cover deterministic validation/run/availability states only; no pending-review, provider or checkpoint prerequisite. |
| REVIEW-005 | Global snapshot_id with exactly one owner is consistent across import, evidence, publication, replay and lineage. |
| REVIEW-006 | Typed import/event/validation/safety contracts distinguish invalid data, conflicts, limits and operational failure; diagnostic completeness is explicit. Empirical targets are separately gated. |
| REVIEW-007 scope/milestone portion | M03 observations/explanations/inspection suggestions only; high-impact recommendations/review M04. M03 bypasses review nodes. |
| REVIEW-015 | Excluded financial analytics removed from active-v1 schema, criteria and release gates; concepts remain deferred in glossary/register. |
| REVIEW-016 | Per-ID Status/Applicability, explicit mixed-stage variants, staged verification and prospective acceptance manifest. No blanket acceptance. |

The current policy-conflict behavior portion of REVIEW-010 is also aligned: indeterminate outcome and corpus correction outside a run. The generic runtime conflict-review system is removed from v1 expectations. Human recommendations cannot establish policy precedence.

## 7. Unresolved or partially resolved findings
| Finding | Remaining detail | Gate |
|---|---|---|
| REVIEW-007 detailed review | M04 review aggregation/identity; no M03 prerequisite. | OQ-009/012 |
| REVIEW-008 | Actual graph/result/checkpointer coordination and compatible replay. CT-018 resolves M02 publication only. | ADR-001, OQ-009 M03 |
| REVIEW-009 later variant | M02 lifecycle and metric-preserving optional failure are aligned; M04 provisional/review aggregation needs detailed contract. | OQ-009/012 M04 |
| REVIEW-010 authority details | No runtime conflict review; curated policy precedence/scope remains undefined. | OQ-006 M03 |
| REVIEW-011 | Policy evaluation coverage and system-level indeterminate rule identity. | OQ-006/007 M03 |
| REVIEW-012 | Temporal rate kind, prior selection, cohort/attribute invariants. No method selected by assumption. | OQ-005 M03 |
| REVIEW-013 | Detailed copilot exchange audit/history contract. Read-only results versus audit appends are now distinguished. | FR-AI-002 M04 |
| REVIEW-014 | Reviewed policy source-span/chunk mapping and retrieval sufficiency. | OQ-006/007 M03 |

These are retained Proposed later design obligations. They do not authorize implementing an ambiguous future feature, nor block the deterministic slice merely through document co-location.

## Provisional Local Safety Limits requiring review
| Setting | Proposed local default |
|---|---|
| Combined input bytes | 10 MiB |
| Manifest bytes | 64 KiB |
| Loan rows, excluding header | 50,000 |
| UTF-8 field bytes | 4,096 |
| Input numeric characters | 24 |
| Collected diagnostics | 1,000 |

CT-020 explains units, configurable versioning, overflow and diagnostic-cap behavior. These are bounded local demonstrator settings, not risk thresholds, performance guarantees or production SLAs. The manifest cap is a supplemental bound. Aggregate output operands are not truncated to input token length.

## 8. Verification
Executed locally on 2026-10-14 using Python 3.12.13:

| Check | Observed result |
|---|---|
| uv sync --locked --group dev | Passed; existing lock unchanged. |
| uv run --locked ruff check . | Passed. |
| uv run --locked ruff format --check . | Passed. |
| uv run --locked mypy src scripts | Passed; 3 source files. |
| uv run --locked pytest | Passed; 15 governance tests, including 7 negative mutated-document fixtures. |
| uv run --locked python scripts/check_baseline.py | Passed; 61 Markdown documents plus milestone/status/identity/contract coverage guards. |
| git diff --check | Passed under the repository's normal line-ending configuration. |
| Product-source/dependency diff | No changes to src/risklens, pyproject.toml or uv.lock. |

Initial lint/format issues in the new governance code were corrected; no gate failure was waived. These checks do not prove semantic financial correctness or product behavior. No financial calculator, provider, graph, database or UI test is claimed executed. GitHub Actions has not run remotely.
The fresh consistency pass covered scope, principles, requirements/criteria, model/rules/contracts, architecture, graph/RAG/AI boundaries, roadmap, question register, ADRs, tests/traceability. Stale excluded-finance field/definition and composite-identity phrases now occur only in explicitly labeled historical review/CR context, not active-v1 output rules. Denominator availability and raw-share/alert separation are consistent. M02 requires no AI/checkpoint/review; M03 review routing is disabled and high-impact output disallowed.

## 9. Acceptance recommendation and exact prospective approval scope
Approve the corrected direction with explicit later deferrals, rather than requiring the deferred financial concepts or AI to make M02 usable. Baseline acceptance does not waive GOV-002 or authorize starting M02 in this task.

The future acceptance record should enumerate the following Proposed IDs and exact variants:
- GOV-001 through GOV-004, P-001 through P-021 and STYLE-001 through STYLE-003.
- Corrected active-v1 scope, glossary exclusions, local architecture/platform boundary, roadmap, writing/model policy and change process.
- M02 FR-DQ-001/002/003, FR-RISK-001, FR-UI-001, FR-OBS-001 M02 variant and FR-OBS-003; associated AC-DQ-001/002/003, AC-RISK-001, AC-UI-001, AC-OBS-001 M02 variant and AC-OBS-003.
- M02 NFR-SEC-001 core, NFR-PERF-001 safety/calibration policy, NFR-OBS-001 core, NFR-MNT-001, NFR-REL-002 and NFR-SEC-002 M02 retention.
- BR-DQ-001/002/003/004; BR-RISK-001/002/005; BR-RISK-003 raw metrics only. BR-RISK-006 remains a Deprecated historical stub, never Accepted active behavior.
- CT-001/002/004/005/015/016/017/018/019/020 and M02 variants of CT-003/011, including exact CT-020 defaults.
- ADR-002/003/004/005/006/007/008/009 individually. ADR-001 remains Proposed.

Files containing these mixed-stage IDs remain Proposed at container level: functional-requirements.md, non-functional-requirements.md, acceptance-criteria.md, domain-model.md, business-rules.md and data-contracts.md. A future acceptance edit sets only explicitly approved IDs/variants Accepted; later clauses remain Proposed. This is deliberate rather than an implied rejection of accepted subsets.
Pure governance/direction files may change header to Accepted after exact approval: AGENTS.md; docs/00-project/baseline.md, principles.md, writing-policy.md, vision.md, scope.md, glossary.md, roadmap.md, model-usage-policy.md; docs/05-testing/test-strategy.md; docs/changes/README.md. Mixed architecture/security/observability files keep Proposed headers while later adapter detail remains Proposed; record their accepted M02 subsets explicitly. Registries/traceability reflect decisions rather than approving them wholesale. Templates remain Draft. Prior reports remain historical Proposed artifacts.

## 10. Exact next human action
Review the immutable corrected Proposed commit identified by baseline-review-target.md. Approve or amend the enumerated M02/direction/ADR subset, six safety settings and explicit deferrals. Then a subsequent governance task records the human identity/date/commit and updates only those approved statuses under GOV-001. No acceptance record exists now.

# Final Baseline Closure Report

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

## 1. Final disposition
**ACCEPT WITH EXPLICIT DEFERRALS** is recommended for the exact final Proposed review target. The baseline is ready for owner review, not accepted. Product functionality is NOT IMPLEMENTED. No M02 work is started or authorized by this closure.

The repository was inspected from clean starting commit archived baseline review parent. Owner decisions, the existing acceptance review and CR-001 were used as the correction sources. No redesign, new financial threshold, changed safety cap, product dependency or speculative architecture was introduced. Final review used the Architect/Auditor role; exact execution model identity is unknown and no model switch or delegation occurred.

## 2. Files changed during closure
The specification review-target commit contains exactly these six paths:

```text
CHANGELOG.md
README.md
docs/00-project/baseline.md
docs/00-project/baseline-closure-report.md
docs/03-architecture/observability.md
docs/03-architecture/security.md
```

After that commit exists, the record-preparation commit adds or updates only these paths:

```text
docs/changes/BASELINE-ACCEPTANCE-001.md
docs/changes/baseline-review-target.md
docs/changes/CR-001-baseline-acceptance-corrections.md
```

The prepared record and locator identify the exact review-target SHA without attempting a self-referencing commit. The later commit contains approval preparation metadata only. It must not change reviewed normative behavior. src/risklens, tests, scripts, dependency declarations and the lockfile are unchanged during this closure.

## 3. Resolved correction findings
| Finding | Final verification |
|---|---|
| REVIEW-001 | BR-RISK-005 and CT-017 define decimal monetary encoding, exact integer minor-unit sums, exact ratio operands, four-digit half-even derived values and comparisons independent of rounding. |
| REVIEW-002 | CT-004 and AC-RISK-001 distinguish count/exposure denominators and cover 1/3, zero exposure/nonzero count, zero eligible population and ties. |
| REVIEW-003 | FR-RISK-001/002 and BR-RISK-003 separate M02 raw group metrics from M03 threshold-based alerts. |
| REVIEW-004 | FR/AC/NFR applicability and CT-016 exclude AI, graph checkpoints and pending-review UI from M02. |
| REVIEW-005 | BR-DQ-001, CT-001/003/011/015/018 and replay requirements use globally unique snapshot_id with exactly one portfolio owner. |
| REVIEW-006 | CT-015 through CT-020 provide import/configuration/hash/publication/event/error/limit contracts with criteria and traceability. Closure aligns observability aliases and security verification references with these canonical contracts. |
| REVIEW-007 scope/milestone portion | M03 observations and evidence inspection only; high-impact recommendations and review M04. Failure routes do not force M03 into review. |
| REVIEW-015 | Active-v1 Default analytics/metric/release requirements removed. DTI/score excluded. Deferred concepts and historical IDs retained. |
| REVIEW-016 | Per-ID Status/Applicability and exact proposed acceptance subsets preserve mixed-stage containers as Proposed. |

No previously resolved financial or architectural decision was reopened. Historical review findings are labeled as historical and cannot override the corrected specifications.

## 4. Remaining unresolved findings
REVIEW-007 detailed review behavior, REVIEW-008 graph coordination, REVIEW-009 later review aggregation, REVIEW-010 policy authority details, REVIEW-011 policy coverage/system-rule identity, REVIEW-012 temporal semantics, REVIEW-013 copilot audit/history and REVIEW-014 source-span/chunk mapping remain Proposed. Their gates are listed in the acceptance record and the question register. They are not missing M02 prerequisites.

The policy-conflict direction is already fixed: unresolved context stays indeterminate and corpus correction occurs outside an analysis. No runtime generic policy-conflict review system is introduced.

## 5. M02 blockers and authorization boundary
No unresolved baseline-level business/architecture contradiction blocks the documented deterministic slice. Remaining prerequisites are explicit owner acceptance of the final commit and exact M02/profile/ADR subset, followed by GOV-002 feature preparation and a separately authorized M02 task. Baseline acceptance alone is not permission to start implementation during this closure.

M02 includes synthetic USD bundle/CSV and manifest validation, valid/rejected/conflict/limit outcomes, exposure/delinquency/raw groups, denominator-specific availability, lineage, local persistence, restart/read/replay and Streamlit presentation. It requires no LLM, LangChain, LangGraph, RAG, vector store, model provider, policy engine, AI recommendation, human review, pending-review UI or AI checkpoint.

## 6. Deferred decisions
Every row inherits decision owner Product Owner; technical preparation belongs to the relevant future feature reviewer. Status is OPEN or Proposed as identified, never implied Accepted.

| Deferred area | Status | Gate | Source |
|---|---|---|---|
| Concentration alerts/anomaly thresholds | OPEN | M03 detector readiness | OQ-004, FR-RISK-002, BR-RISK-007 |
| Temporal rate/cohort/prior semantics | OPEN | M03 comparison readiness | OQ-005, FR-RISK-003, CT-014 |
| Graph/checkpointer implementation | Proposed / OPEN | M03 graph readiness | ADR-001, OQ-009 graph, graph-spec.md, FR-OBS-002 |
| Policy authority, applicability and coverage | OPEN | M03 policy readiness | OQ-006, FR-POL-002, CT-007/009 |
| RAG/index/embedding/chunking/sufficiency | Proposed / OPEN | M03 retrieval readiness | ADR-005 deferral, OQ-007, rag-spec.md, CT-010 |
| Runtime models/prompts/eval usefulness | OPEN | M03 AI readiness | OQ-011, AI specifications, FR-AI-001 |
| AI call/context/retry/time/cost budgets | OPEN | Before M03/M04 AI calls | OQ-008 AI, NFR-AI-002 |
| Measured performance targets | OPEN | Working M02 milestone release, then affected releases | OQ-008 measured, NFR-PERF-001 |
| Reviewer identity and review aggregation | OPEN / Proposed | M04 readiness | OQ-009 review, OQ-012, CT-012 |
| High-impact recommendations and copilot | Proposed | M04 readiness | FR-AI-002/003, FR-UI-002, CT-008 M04/013 |
| Later artifact deletion/retention | OPEN | M03/M04 affected artifact features; targeted deletion before exposure | OQ-010 later lifecycle; CT-018 covers only M02 cleanup |
| Default semantics | Deferred outside active v1 | Future scope CR | OQ-002 financial portion, glossary; BR-RISK-006 stub stays Deprecated |
| DTI/credit score | Deferred outside active v1 | Future extension CR | OQ-003, glossary/scope |

## 7. Open-question summary
OQ-001 is CLOSED. OQ-002 current-v1 scope is CLOSED with unresolved financial meaning deferred. OQ-003 is outside active v1. OQ-009 M02 platform and OQ-010 M02 retention are CLOSED; their later portions remain OPEN. OQ-008 separates proposed local safety values from OPEN measured performance and AI budgets. OQ-004/005/006/007/011/012 stay OPEN at their named gates. No historical ID was removed.

## 8. ADR readiness
ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008 and ADR-009 are recommended individually for human acceptance. ADR-005 approves deferral, not a vector database. ADR-001 remains Proposed. All nine are currently Proposed; no record has been signed by the owner.

## 9. Contract completeness, arithmetic and safety
| M02 need | Canonical contract | Verification references |
|---|---|---|
| Import/Validation Result | CT-015 | AC-DQ-001/002/003, AC-OBS-003 |
| Analysis Request/Configuration | CT-016 | AC-DQ-001/003, AC-OBS-001/003 |
| Arithmetic/Canonical Hashing | CT-017 | AC-RISK-001, AC-OBS-001/003 |
| Local Publication/Recovery | CT-018 | AC-OBS-003, AC-DQ-001 |
| Typed Event Catalog | CT-019 event fields | AC-OBS-001/003 |
| Typed Validation/Error Catalog | CT-019 validation and operation code sections | AC-DQ-002/003, AC-OBS-001/003 |
| Bounded Parser Configuration | CT-020 | AC-DQ-003 |

Each contract has stable ID, fields, invariants, failure behavior, criteria, edge cases and a traceability row. Mixed CT-003/011 M02 variants are explicit. The event and error catalogs share CT-019 intentionally; neither lives only in explanatory prose elsewhere.
Monetary values use decimal USD strings and exact integer cents internally; this fulfills deterministic decimal-value arithmetic without relying on a global Decimal context. Ratios preserve exact operands. 1/3 serializes 0.3333, 1/32 rounds to 0.0312, and 3/32 to 0.0938. Open zero-principal loans retain count eligibility while exposure rate can be unavailable. Hashing distinguishes canonical semantic content from complete original bundle bytes; artifact hashes identify actual immutable bytes.

CT-020 values are unchanged: 10 MiB combined input, 64 KiB manifest, 50,000 loan rows, 4,096 UTF-8 bytes per field/scalar, 24 input numeric characters, 1,000 diagnostics. The configurable profile is labeled Provisional Local Safety Limits. Its rounded values bound pathological local input; they are not production SLAs or empirical performance guarantees. No individual bound needs separate redesign before acceptance. The owner approves the complete profile with the baseline; performance calibration follows measured implementation before release.

## 10. Verification results
Executed locally on 2026-10-15 using Python 3.12.13:

| Check | Result |
|---|---|
| uv sync --locked --group dev | Passed; lock and dependencies unchanged. |
| uv run --locked ruff check . | Passed. |
| uv run --locked ruff format --check . | Passed. |
| uv run --locked mypy src scripts | Passed; 3 source files. |
| uv run --locked pytest | Passed; 15 governance tests, including 7 negative document fixtures. |
| uv run --locked python scripts/check_baseline.py | Passed for the 62 Markdown documents in the review target. The post-commit acceptance record adds one document and receives another consistency check. |
| git diff --check | Passed. |

Existing governance checks cover traceability, current-v1 schema exclusions, milestone boundaries, mixed acceptance, links, IDs, domain imports and global identity. The separate source review covered all requested semantic boundaries and identified only the already-approved event/catalog reference alignment applied here. No unresolved M02 semantic contradiction was found. Passing tests do not prove semantic correctness, arithmetic implementation or product behavior. No runtime graph/provider/database/UI tests exist yet, and GitHub Actions was not run remotely.

## 11. Immutable review target
The final specification commit uses message `spec: finalize RiskLens baseline v1.0 for acceptance`. Its exact SHA is recorded after commit in docs/changes/baseline-review-target.md and the prepared acceptance record. The subsequent record-preparation commit does not alter the reviewed normative files. No push is performed.

## 12. Prepared acceptance record
After the final review target exists, prepare docs/changes/BASELINE-ACCEPTANCE-001.md with Status Proposed and Approval State Awaiting Owner Approval, the repository-compatible equivalent of awaiting approval. Actual accepted sets are empty. Its tables are proposed scope only until the owner explicitly approves that SHA and scope.

## 13. Exact IDs proposed for owner acceptance
- Governance: GOV-001, GOV-002, GOV-003, GOV-004; P-001 through P-021; STYLE-001, STYLE-002, STYLE-003.
- Requirements, M02 only: FR-DQ-001, FR-DQ-002, FR-DQ-003, FR-RISK-001, FR-UI-001, FR-OBS-001 M02 variant, FR-OBS-003.
- NFR clauses: NFR-SEC-001 local synthetic/path/SQL/redaction core; NFR-PERF-001 safety bounds and later-calibration policy; NFR-OBS-001 M02 lineage/events only; NFR-MNT-001 domain/offline testability; NFR-REL-002 deterministic semantic replay; NFR-SEC-002 M02 retention/whole-state cleanup only.
- Criteria: AC-DQ-001, AC-DQ-002, AC-DQ-003, AC-RISK-001, AC-UI-001, AC-OBS-001 M02 variant, AC-OBS-003.
- Rules: BR-DQ-001, BR-DQ-002, BR-DQ-003, BR-DQ-004, BR-RISK-001, BR-RISK-002, BR-RISK-003 raw metrics only, BR-RISK-005.
- Contracts: CT-001, CT-002, CT-003 M02 core only, CT-004, CT-005 including shared DQ envelope, CT-011 M02 core only, CT-015, CT-016, CT-017, CT-018, CT-019, CT-020 including exact provisional defaults.
- Individual ADRs: ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-009.

Document IDs are existing repository-relative paths, not a new numbering system. Exact document/section scope is listed in the prepared record. Proposed approval includes product direction, glossary exclusions, local boundaries, roadmap, model/writing policy, testing/change process; it does not accept future feature details by implication.

## 14. Exact IDs/specifications remaining Proposed
FR-RISK-002, FR-RISK-003, FR-POL-001, FR-POL-002, FR-AI-001, FR-AI-002, FR-AI-003, FR-UI-002 and FR-OBS-002 remain Proposed. Their AC-RISK-002/003, AC-POL-001/002, AC-AI-001/002/003, AC-UI-002 and AC-OBS-002 remain Proposed. NFR-REL-001, NFR-AI-001 and NFR-AI-002 and future extensions of the mixed NFRs remain Proposed.
BR-RISK-003 alert configuration, BR-RISK-004, BR-RISK-007 and BR-POL-001/002/003/004 remain Proposed. BR-RISK-006 stays Deprecated, never an active accepted rule.
CT-006, CT-007, CT-008, CT-009, CT-010, CT-012, CT-013, CT-014 and future variants of CT-003/011 remain Proposed. ADR-001, graph-spec.md, rag-spec.md and all five docs/04-ai specifications remain Proposed. Existing future-use-case, architecture, event/security extensions remain Proposed until relevant readiness review. Registry/traceability headers do not grant blanket acceptance. Mixed-stage containers retain Proposed headers even if a future approval accepts individual M02 subsets.

## 16. Exact next human action
Review the final SHA and the proposed scope in BASELINE-ACCEPTANCE-001.md. Approve or amend that exact scope, including CT-020, with the Product Owner identity/date. Only a later governance action can record that approval and change explicitly approved IDs/ADRs; retain all listed deferrals and mixed-stage container states. Do not start M02 as part of acceptance recording.

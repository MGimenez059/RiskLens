# Testing strategy

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the document/section scope recorded there is accepted; later feature gates remain in force.

| Layer | What it proves | Isolation and representative cases |
|---|---|---|
| Unit | Domain invariants, exact formulas and deterministic predicates. | No network, keys or database; empty/zero denominators, boundary comparisons, dates, rounding. |
| Contract | CT-001 through CT-020, by active milestone and tool envelopes. | Missing/extra fields, invalid types, nullability, enum transitions, evidence ownership and schema versions. |
| Integration | Real adapters satisfy ports. | Temporary local SQLite/files, transactions, foreign keys, artifact integrity, parser and migration paths. |
| Graph | Routing, state patches, retries and durability. | Fake provider/retriever, real temporary checkpointer; crash at each commit boundary, replay and stale review. |
| RAG evals | Retrieval relevance, applicability and citation integrity. | Versioned synthetic corpus, gold queries, empty/conflicting/expired cases. |
| AI evals | Structured validity, grounding and refusal behavior. | Offline adversarial fakes plus separately budgeted live-provider runs; human gold rubric. |
| End-to-end | Analyst can complete each approved slice. | Import to visible metrics; evidence navigation; explicit pending/rejected review; restart and UI refresh. |
| Repository governance | Baseline links, metadata, trace coverage, style and domain boundaries. | Executed in this phase; not product coverage. |

Name future tests with full IDs, for example `test_FR_RISK_001_delinquency_rates`. Traceability contains planned names until files exist. Write behavioral tests from accepted criteria before implementation. Avoid tests that only repeat implementation details. No numerical coverage target is invented; completeness follows requirements, meaningful edge cases and critical failure paths.

## Local and CI gates
Use Python 3.12+, uv with a committed lockfile, Ruff, mypy, pytest and pre-commit under ADR-009. Commands are in README. CI runs offline application tests without provider secrets. Dependency installation requires package network access; this is distinct from test-time network independence.

Current passing checks verify selected syntactic and governance constraints only; they do not prove semantic consistency. They do not prove financial formulas, retrieval, UI or review behavior because none is implemented. Add integration, graph and provider eval jobs when their approved slices exist. Never skip a missing product test and describe it as covered.

Readiness/completion rules are canonical in baseline.md GOV-002/003. Gate failures block merging affected implementation. Releases additionally require roadmap criteria and a recorded evaluation report tied to a commit.

## Milestone applicability and meaningful new cases
M02 unit/contract/integration/E2E tests cover exact operands and CT-017 rounding, raw group shares, CT-015 outcomes, CT-020 bounds, global snapshot ownership, CT-018 publication/restart/cleanup and import-versus-analysis replay. No graph/checkpoint, provider, policy, partial-AI or pending-review fixture is a M02 product prerequisite.
M03 tests cover detectors/comparison only after OQ-004/005, policy/RAG only after OQ-006/007, and observations with empty recommendations. M04 review/calling/identity tests apply only when those features are ready. A failed later optional stage preserves deterministic metrics; missing optional stage is not silently claimed implemented.
Planned numeric cases: 1/3 = 0.3333 with exact operands; half-even ties 1/32 = 0.0312 and 3/32 = 0.0938; two open zero-principal loans with one delinquent yield available 1/2 count rate and unavailable exposure rate; zero open population yields no_eligible_population. Bounds are safety configuration, not financial alert thresholds.
Governance tests must reject active excluded-finance fields, invalid milestone assignments, missing contract trace rows, ambiguous global snapshot ownership and blanket acceptance of mixed-stage specs. Negative mutated-document fixtures exercise these guards; no product calculation is implemented to run them.

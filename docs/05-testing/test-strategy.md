# Testing strategy

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

| Layer | What it proves | Isolation and representative cases |
|---|---|---|
| Unit | Domain invariants, exact formulas and deterministic predicates. | No network, keys or database; empty/zero denominators, boundary comparisons, dates, rounding. |
| Contract | CT-001 through CT-014 and tool envelopes. | Missing/extra fields, invalid types, nullability, enum transitions, evidence ownership and schema versions. |
| Integration | Real adapters satisfy ports. | Temporary local SQLite/files, transactions, foreign keys, artifact integrity, parser and migration paths. |
| Graph | Routing, state patches, retries and durability. | Fake provider/retriever, real temporary checkpointer; crash at each commit boundary, replay and stale review. |
| RAG evals | Retrieval relevance, applicability and citation integrity. | Versioned synthetic corpus, gold queries, empty/conflicting/expired cases. |
| AI evals | Structured validity, grounding and refusal behavior. | Offline adversarial fakes plus separately budgeted live-provider runs; human gold rubric. |
| End-to-end | Analyst can complete each approved slice. | Import to visible metrics; evidence navigation; explicit pending/rejected review; restart and UI refresh. |
| Repository governance | Baseline links, metadata, trace coverage, style and domain boundaries. | Executed in this phase; not product coverage. |

Name future tests with full IDs, for example `test_FR_RISK_001_delinquency_rates`. Traceability contains planned names until files exist. Write behavioral tests from accepted criteria before implementation. Avoid tests that only repeat implementation details. No numerical coverage target is invented; completeness follows requirements, meaningful edge cases and critical failure paths.

## Local and CI gates
Use Python 3.12+, uv with a committed lockfile, Ruff, mypy, pytest and pre-commit under ADR-009. Commands are in README. CI runs offline application tests without provider secrets. Dependency installation requires package network access; this is distinct from test-time network independence.

Current passing checks prove the scaffold is internally consistent. They do not prove financial formulas, retrieval, UI or review behavior because none is implemented. Add integration, graph and provider eval jobs when their approved slices exist. Never skip a missing product test and describe it as covered.

Readiness/completion rules are canonical in baseline.md GOV-002/003. Gate failures block merging affected implementation. Releases additionally require roadmap criteria and a recorded evaluation report tied to a commit.

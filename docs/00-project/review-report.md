# Baseline review report

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## Historical initial-baseline report
This report describes initial preparation on 2026-10-07, preserved in Git commit archived initial proposal revision. Its Default scope, file inventory and uncommitted-state statements are historical. Current corrected behavior and verification are in [baseline-correction-report.md](baseline-correction-report.md). No original result below is retroactively rewritten as a later acceptance decision.

## 1. Files created
The workspace was empty and was not a Git repository. A local main repository was initialized. No commit, remote, push, product implementation or acceptance record was created. The complete [file inventory](file-inventory.md) lists 79 files, including 56 Markdown documents. uv.lock records development dependencies; the package build backend is declared separately in pyproject.toml. There are no product runtime dependencies.

## 2. Final structure
```text
RiskLens/
  AGENTS.md, README.md, CHANGELOG.md
  pyproject.toml, uv.lock, .python-version, .env.example, .gitignore
  .pre-commit-config.yaml
  .github/workflows/quality.yml
  docs/
    00-project/       baseline, vision, scope, principles, glossary, roadmap,
                      model policy, writing policy, open decisions, review, inventory
    01-requirements/  functional, non-functional, use cases, acceptance criteria
    02-domain/        model, rules, contracts
    03-architecture/  architecture, graph, RAG, security, observability
    04-ai/            responsibilities, tools, prompts, guardrails, evaluations
    05-testing/       strategy and traceability
    adr/              registry, template and nine proposed decisions
    changes/          process and CR template
  src/risklens/       package marker; domain, application, infrastructure,
                      graph and tools placeholders
  tests/             repository checks; unit, integration, contract, graph,
                      evals and E2E placeholders
  scripts/           repository consistency checker
  prompts/, data/    artifact guidance only
```

## 3. Principles
P-001 through P-021 cover deterministic numeric authority, evidence and policy grounding, explicit rules/contracts, domain isolation, testability, failure containment, human review, run lineage, provider boundaries, justified agents, controlled scope, repository memory and English technical writing. The canonical list and precedence order are in principles.md.

## 4. Requirements and contracts
There are 14 functional requirements, 9 NFRs, 14 functional acceptance criteria, 14 written data contracts, 3 read-only tool contracts and 19 planned evaluation cases. Every FR/NFR has a traceability row. Product implementation and product tests remain NOT IMPLEMENTED or explicitly planned. No test/eval result is inferred from a specification.

The core data proposal adds snapshots and separate original/outstanding principal. DTI, income, installment and credit-score analytics are excluded until their semantics are defined. Default remains explicitly unavailable until OQ-002 is resolved. CT-014 supplies the temporal-comparison contract rather than leaving deterioration in prose.

## 5. ADR status
ADR-001 through ADR-009 are Proposed; none is Accepted. They cover LangGraph, Pydantic, persistence, UI, deferred vector selection, provider ports, observability, repository boundaries and tooling. Tooling is configured under the user's explicit authorization for this phase; that does not autoaccept its ADR.

## 6. Open decisions
OQ-001 through OQ-012 identify owner, candidate direction and blocking milestone. The immediate M02 decisions are currency/exposure and rejection semantics, workload/resource limits, local persistence/UI choice and retention. Default, detector thresholds, temporal comparability, policy authority, retrieval configuration, runtime model/eval choices and review identity block their respective later features.

## 7. Contradictions and coherence findings
- A single snapshot cannot support a deterioration claim. Comparable history and explicit unavailable behavior are specified.
- Retrieval relevance cannot establish a policy violation. Curated deterministic predicates and policy applicability are separate gates.
- Whole-snapshot rejection avoids silently computing authoritative metrics from a filtered population.
- A pending review is nonterminal and must survive restart. The graph includes durable pause and finalization.
- AI schema validity cannot prove semantic support. The design combines reference validation with labeled semantic evals and review, without claiming complete hallucination prevention.
- Excluded DTI/score fields are not promised v1 analytics. Default remains in scope but blocks release until defined or removed through CR.

No remaining conflict is intentionally treated as resolved by assumption. Deferred decisions remain explicit. Automated checks cannot certify semantic consistency; human review is required.

## 8. Architectural risks
SQLite/checkpoint/file reconciliation, UI rerun idempotency, corpus applicability, unsupported prose claims, provider variability, stale review actions and undefined operating budgets require targeted validation. A local single-user design must not be presented as enterprise deployment readiness. Source-code import checks supplement review; they cannot prove all runtime dependency behavior.

## 9. Premature decisions avoided
No production cloud, multi-tenancy, provider/model ID, vector database, embedding model, arbitrary financial threshold, latency SLA, generalized agent framework or final dataset is selected. Streamlit and SQLite are explicit proposals. Package versions for product dependencies are deferred until approved implementation work.

## 10. Simplifications
One bounded insight synthesizer and one read-only evidence copilot replace a collection of specialized agents. Quality/risk/policy predicates are deterministic. BorrowerRef and CreditExposure are value concepts, not CRUD services. A modular local process replaces distributed services. No unused port implementations, prompt files, ORM models or UI scaffold were added. Contract/E2E test directories and baseline/open-decision/writing documents were added for concrete governance needs.

## 11. Model usage policy
Operator handles mechanical work; Engineer handles approved implementation and ordinary review; Architect/Auditor handles architecture, contradictions and deep audits. The updateable owner mapping is Luna, Sol and Astra respectively. It is a conceptual preference, not a guaranteed API name or pricing claim. Escalation is based on ambiguity, impact, reversibility and capability rather than length. Runtime product models require separate eval-based selection. This baseline task was classified Architect/Auditor; exact execution model identity was not independently verified. No model switch or subagent delegation was performed.

## 14. Human review required
Review principles and precedence, in/out scope, exposure/population definitions, strict import behavior, nullable fields, unavailable semantics, graph recovery, policy curation, AI boundaries, proposed ADRs and deferred-decision gates. Record acceptance against an exact Git commit before product development. Approve each relevant ADR explicitly, including whether deferral in ADR-005 is acceptable.

## 15. Acceptance recommendation
Ready for human review as a Proposed baseline. Not yet accepted and not implementation-ready while M02 blockers remain unresolved. The owner may accept the overall direction with explicit later-stage deferrals, but must resolve the next slice's semantic and operational gates before implementation. This is not a recommendation to treat all TBDs as approved defaults.

## 16. Proposed first vertical slice
After acceptance, prepare a feature specification for synthetic CSV plus manifest import, strict validation, deterministic exposure/delinquency metrics, local run persistence and dashboard evidence/status. Cover FR-DQ-001/002, FR-RISK-001, FR-UI-001 and FR-OBS-001. Use hand-checkable fixtures including invalid input, empty population and zero exposure. No LLM, RAG or LangGraph is needed for this slice. It has not been implemented.

## Validation evidence
Executed locally on Windows with Python 3.12.13 and uv 0.11.2 on 2026-10-07:

| Check | Observed result |
|---|---|
| uv sync --locked --group dev | Passed; package scaffold and development environment installed. |
| uv run --locked ruff check . | Passed. |
| uv run --locked ruff format --check . | Passed. |
| uv run --locked mypy src scripts | Passed; 3 source files checked. |
| uv run --locked pytest | Passed; 5 repository governance tests. |
| uv run --locked python scripts/check_baseline.py | Passed; 56 Markdown documents, metadata/style markers, local links, requirement mappings, referenced IDs and domain imports. |

An initial installation attempted before README creation failed; it passed after the file was present. An initial mypy variable-type error in the checker was corrected and the complete gates rerun successfully. No failure was waived. Product tests/evals are not implemented. The domain import check is currently a scaffold guard, not evidence of implemented domain isolation. English and architectural semantics received author review, not an independent audit.

GitHub Actions is configured for Python 3.12 and 3.14 but has not run remotely. Python 3.14 compatibility is a configured CI target, not locally verified evidence. The files are uncommitted. Product work stops here pending human baseline acceptance.

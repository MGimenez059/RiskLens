# Project principles and precedence

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

- **P-001**: Financial calculations must be deterministic and versioned.
- **P-002**: An LLM must never be the authoritative source of a numeric metric.
- **P-003**: LLMs interpret computed results; they do not recalculate financial metrics.
- **P-004**: Every AI-generated finding must reference resolvable evidence belonging to the correct run.
- **P-005**: Every policy claim must be grounded in retrieved, applicable, effective policy evidence.
- **P-006**: No business rule may exist only inside a prompt.
- **P-007**: Domain must not depend on LangChain, LangGraph, OpenAI, Streamlit, or infrastructure.
- **P-008**: Persisted AI results must use validated structured outputs rather than unconstrained prose.
- **P-009**: Critical workflows must be testable with fake dependencies and without network access.
- **P-010**: AI failures must not corrupt or replace valid deterministic results.
- **P-011**: High-impact recommendations require human review before being presented as reviewed.
- **P-012**: Each AnalysisRun must preserve input provenance, configuration, versions, and result lineage.
- **P-013**: AI providers must be accessed through application-owned ports.
- **P-014**: Do not introduce an agent when a deterministic function better solves the problem.
- **P-015**: Minimize implicit behavior by specifying defaults, failures, and transitions.
- **P-016**: Prefer explicit contracts over arbitrary dictionaries.
- **P-017**: The platform supports analysts and must not approve or reject loans autonomously.
- **P-018**: Use synthetic data only in v1 and never publish secrets or sensitive records.
- **P-019**: Do not expand scope, dependencies, or architecture without justification and traceability.
- **P-020**: The repository is permanent project memory; report contradictions rather than resolving them silently.
- **P-021**: Project artifacts must follow the canonical English writing policy.

## Source precedence
1. Project Principles.
2. Approved Requirements, including approved NFRs and acceptance criteria.
3. Accepted ADRs.
4. Domain Specifications.
5. Architecture Specifications.
6. Feature Specifications.
7. Tests/Evals derived from approved specifications.
8. Implementation.
9. README and explanatory documentation.

This is the canonical precedence definition. All initial baseline documents are proposals to review together; precedence does not approve a proposal. On conflict, identify document paths and IDs, report SPEC CONFLICT, suspend dependent work, and propose a CR. Even when a higher source prevails, correct the lower source with traceability. Conversations and external documentation inform changes but do not replace versioned decisions. Record new owner instructions affecting product behavior before implementation.

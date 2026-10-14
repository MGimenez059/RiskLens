# AI responsibilities

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## AI-ROLE-001: Insight synthesizer
This is one bounded structured model call in the workflow, not an autonomous risk analyst.

- MAY interpret supplied metrics, explain deterministic findings and suggest inspecting available evidence in M03. Business-action recommendations require the separate M04 capability and human review.
- MUST use the M03 CT-008 subset with empty recommendations, reference allowed evidence, identify uncertainty and pass validation. M03 does not depend on reviewer identity or a human-review branch.
- MUST NOT calculate financial metrics, invent findings or policies, change severity or run state, approve/reject credit, invoke tools, or approve its recommendations.

Risk analysis, quality checks, policy predicates, impact assignment and review gates remain deterministic. A separate Risk Agent, DQ Agent and Policy Agent would duplicate responsibilities without demonstrated benefit.

## AI-ROLE-002: Evidence copilot
A bounded tool-calling loop for questions about one existing run. It is the only v1 component that needs limited agent behavior.

- MAY select among TOOL-001/002/003 and summarize the returned evidence.
- MUST remain scoped to the requested run, validate tool inputs and CT-013 output, cite each factual claim, obey configured call/context/cost budgets, and abstain when support is missing.
- MUST NOT mutate a run, import data, write policies, execute SQL/shell, access arbitrary URLs/files, request another run, use cross-run memory, or approve/reject loans.

The application, not the model, enforces tools, scope and budgets. Conversation history is a bounded convenience, not authoritative project or portfolio memory. Models and providers remain replaceable through StructuredModel.

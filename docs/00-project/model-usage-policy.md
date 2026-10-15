# Model usage policy

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the document/section scope recorded there is accepted; later feature gates remain in force.

## Permanent policy
Classify work by complexity, ambiguity, architectural impact, affected areas, reversibility, reasoning needs, and cost. Task length does not determine the role. Use the least capable role expected to meet the acceptance criteria and validate its output.

| Role | Work | Boundary |
|---|---|---|
| Operator | Authorized Git operations, files, formatting, scaffolding, commands, mechanical changes, trivial updates, specified simple tests. | No business or architectural decisions. A short destructive Git command is not automatically trivial. |
| Engineer | Approved features, debugging, tests, integration, bounded refactors, graph nodes, tools, RAG, ordinary code review. | Escalate contract ambiguity and cross-cutting impact. |
| Architect / Auditor | SDD baseline, important ADRs, cross-cutting design, contradiction analysis, security review, milestone audits, release readiness. | Do not use this role for routine mechanical execution by default. |

Escalate Operator to Engineer to Architect/Auditor only for demonstrated capability limits, material uncertainty, architectural impact, multiple affected areas, difficult-to-reverse decisions, or deep audit requirements. Record task, reason, role, and validation evidence. Return to the lowest suitable role afterward. Do not escalate for convenience or loop prompts indefinitely.

## Updateable mapping: owner preference, 2026-10-07
| Role | Current recommended model | Interpretation |
|---|---|---|
| Operator | Luna | User-specified conceptual alias; verify availability. |
| Engineer | Sol | User-specified conceptual alias; not a guaranteed API model ID. |
| Architect / Auditor | Astra | User-specified conceptual alias; no price or SLA claim. |

Update this mapping with date, reason, and evidence without changing role responsibilities. Do not assume future names, versions, availability, or prices. Identify the execution model only when reliably exposed by the environment; otherwise report unknown. Recommend a switch without pretending it occurred. Do not block trivial work for routing.

## Development roles versus runtime models
This mapping governs development work. RiskLens runtime models will be selected through project evals, structured-output support, latency, and cost per valid result under OQ-011. Record effective provider, model ID, and configuration per run. A coding-agent role does not determine a production model.

Reference: [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection), consulted 2026-10-07, supports evaluating quality, cost, and latency. The role policy above is RiskLens's proposal, not a provider guarantee.

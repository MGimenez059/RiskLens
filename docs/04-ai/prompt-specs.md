# Prompt specifications

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

Applicability: M03 synthesis and M04 copilot/recommendation variants, all Proposed. No executable prompts are created in this phase. Future prompts follow the [writing policy](../00-project/writing-policy.md) and contain references to rules rather than becoming their sole implementation.

| ID | Inputs | Output | Constraints | Evaluation gate |
|---|---|---|---|---|
| PROMPT-001 | Frozen CT-004/006/007, evidence allowlist and unavailable-stage reasons. | Candidate CT-008 M03 observations/inspection suggestions; recommendations empty. | Explain supplied findings; numeric facts use references; no tool access; no business-rule definitions or invented policy. | EVAL-RISK-001, EVAL-AGENT-001, EVAL-GUARDRAIL-001/002. |
| PROMPT-002 | Question, bounded run-scoped history and available tools. | CT-013 after bounded tool calls. | Read-only investigation; refuse credit decisions and unsupported scope; cite evidence or abstain. | EVAL-AGENT-002/004, EVAL-GUARDRAIL-001/002. |

Separate trusted instructions, typed context and untrusted user/document text. Include schema version, evidence identifiers, missing-data states and explicit action limits. Never insert raw arbitrary records when aggregate evidence suffices. Application validation remains mandatory even with provider-native structured output.

Each prompt artifact records ID, version, hash, related requirements, expected schema, model configuration, eval dataset versions and reviewer. Wording changes that can affect behavior require a CR after acceptance and rerun relevant evals. Model/config changes also require evaluation. No silent prompt tuning against holdout data.

# AI guardrails

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

| Boundary | Enforcement | Failure response |
|---|---|---|
| Input | Parse strict contracts; distinguish trusted instructions from data. | Reject invalid contract; do not send rejected rows to a model. |
| Tool selection | Application allowlist, run scope and budget checks before invocation. | Refuse unknown/disallowed tools; record safe error. |
| Model output | Validate schema, evidence existence/scope, numeric references, policy applicability and prohibited actions. | Discard candidate; preserve deterministic outputs; partial status. |
| Policy interpretation | BR-POL-001/002/003 and curated predicates. | Indeterminate or abstained, never assumed compliance. |
| Recommendations | Application impact classification under BR-POL-004. | High impact remains pending human review. |
| Recovery | Immutable outputs, revision checks and idempotent commits. | Reject stale/conflicting state without overwriting results. |

Reference existence alone cannot prove semantic entailment. Structured numeric references reduce numeric fabrication, but prose grounding still needs labeled evals and human audit. Automated validators must not be described as complete hallucination detection. Unsupported semantic claims found during review fail the relevant eval/release gate.

Prompt injection fixtures include instructions in CSV strings, policy paragraphs, user questions and tool results. No source text may change tools, source precedence or approval authority. Test unsupported credit decisions, fabricated citations and claims that contradict the cited evidence. Do not collect hidden model reasoning as an audit mechanism.

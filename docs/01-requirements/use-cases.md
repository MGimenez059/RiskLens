# Use cases

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

| ID | Actor and trigger | Main path | Alternative / failure | Requirements |
|---|---|---|---|---|
| UC-001 | Analyst imports a synthetic snapshot. | Validate, compute, persist, display evidence. | Reject malformed/core-invalid input; empty snapshot has unavailable ratios. | FR-DQ-001/002, FR-RISK-001, FR-UI-001, FR-OBS-001 |
| UC-002 | Analyst investigates portfolio changes. | Compare eligible snapshots and inspect deterministic detector evidence. | No compatible history or detector config yields unavailable analysis. | FR-RISK-002/003 |
| UC-003 | Analyst requests policy-supported interpretation. | Retrieve, evaluate curated predicates, synthesize and validate. | Missing/conflicting policy context yields indeterminate, never assumed compliance. | FR-POL-001/002, FR-AI-001 |
| UC-004 | Analyst asks a portfolio question. | Read run-scoped evidence and return structured answer. | Unsupported actions, missing evidence, or budget exhaustion produce refusal/abstention. | FR-AI-002 |
| UC-005 | Reviewer inspects high-impact recommendation. | Navigate sources and record decision against current revision. | Stale action conflicts; restart restores pending state. | FR-AI-003, FR-UI-002, FR-OBS-002 |

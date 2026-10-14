# Change requests

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

Approved behavioral changes follow this sequence: CR, current behavior, proposed behavior, motivation, impact analysis, affected requirements, ADRs, contracts and tests/evals, specification update, implementation, traceability update, CHANGELOG and validation.

Use [the template](CR-XXX-template.md). Assign a stable ID. The product owner accepts behavior and contract changes; the technical reviewer prepares impact analysis. Agents cannot approve their own proposal. Resolve conflicts using canonical precedence in principles.md, with explicit correction of affected artifacts.

CR lifecycle: Draft, Proposed, Accepted, then implementation/verification recorded as checklist evidence. Deprecated or Superseded records retain history. A rejected proposal remains Deprecated with rationale. Acceptance of a CR does not imply implementation is complete.

Editorial corrections that do not alter behavior may use an explicitly labeled CHANGELOG entry. Meaning changes to scope, defaults, formulas, enum handling, prompts, evaluation thresholds or architecture require CR review. Baseline acceptance itself uses GOV-001 and an acceptance record identifying the exact reviewed commit.

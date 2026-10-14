# ADR-002: Boundary validation with Pydantic

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

- ID: ADR-002
- Date: 2026-10-07
- Related requirements: FR-DQ-001, FR-AI-001, NFR-MNT-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
External files and model output need explicit schemas and consistent validation. Framework types should not determine domain design.

## Decision
Propose Pydantic for import/tool/provider boundary DTOs after written contracts are accepted. Domain uses standard Python values/dataclasses/enums. Configure strict validation and forbidden extra fields; explicitly parse the documented CSV/decimal/date wire representation before domain conversion.

## Alternatives
Manual validation minimizes dependencies but duplicates boundary diagnostics. Pydantic domain inheritance is convenient but couples domain behavior to a validation framework.

## Consequences
DTO-to-domain mapping adds code that must have contract tests. Strict mode alone does not validate financial semantics or eliminate all representation differences. No Pydantic dependency or model is installed now.

Reference consulted 2026-10-07: [Pydantic strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/). Verify JSON/Python input behavior against CT-001 through CT-013 during implementation.

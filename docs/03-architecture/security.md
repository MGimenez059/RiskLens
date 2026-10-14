# Security and privacy

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

Initial operation is local, single-user and restricted to controlled synthetic fixtures. Assets are run integrity, policy provenance, review decisions, API credentials and artifacts. Synthetic labeling alone does not prove absence of personal data; use approved generators.

| Threat | Control | Verification |
|---|---|---|
| CSV/policy prompt injection | Content is data; bounded context and read-only tools. | EVAL-GUARDRAIL-001. |
| Path traversal or arbitrary execution | Resolve opaque IDs through confined stores; no shell or arbitrary SQL tools. | NFR-SEC-001 negative fixtures. |
| Cross-run evidence leakage | Application enforces run-scoped resolution. | EVAL-AGENT-002. |
| Secret/payload exposure | Environment-held secrets; redacted events; aggregate context. | Secret canary absent from logs. |
| Oversized input or runaway calls | Approved byte/row/token/time/call/cost limits. | NFR-AI-002; OQ-008. |
| Forged approval | UI-originated reviewer identity, revision check, append-only record. | AC-AI-003; OQ-012. |
| Corrupt artifacts/checkpoints | Hash and schema verification; transactional references. | AC-OBS-002. |
| SQL injection | Parameterized predefined queries inside infrastructure. | Hostile-identifier integration fixtures. |

Remote hosting, multiple users and real data require a new threat model and ADR. No enterprise authentication or regulatory compliance claim is made. Outbound model context contains minimized synthetic aggregates and necessary evidence only. Retention/deletion under OQ-010 must cover linked artifacts, checkpoints and logs without orphaning live claims.

Ordinary CI requires no provider credentials. Dependency additions require a concrete purpose, appropriate license/security review, lockfile change and feature/ADR traceability.

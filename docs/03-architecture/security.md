# Security and privacy

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

Initial operation is local, single-user, single-writer and restricted to controlled synthetic USD fixtures. M02 safety bounds are CT-020 and publication/cleanup CT-018. AI/tool/review controls in the table are M03/M04 Proposed variants; they do not gate deterministic M02 readiness. Assets are run integrity, policy provenance, review decisions, API credentials and artifacts. Synthetic labeling alone does not prove absence of personal data; use approved generators.

| Threat | Control | Verification |
|---|---|---|
| CSV/policy prompt injection | Content is data; bounded context and read-only tools. | EVAL-GUARDRAIL-001. |
| Path traversal or arbitrary execution | Resolve opaque IDs through confined stores; no shell or arbitrary SQL tools. | NFR-SEC-001 negative fixtures. |
| Cross-run evidence leakage | Application enforces run-scoped resolution. | EVAL-AGENT-002. |
| Secret/payload exposure | Environment-held secrets; redacted events; aggregate context. | Secret canary absent from logs. |
| Oversized input or runaway calls | Approved byte/row/token/time/call/cost limits. | NFR-AI-002; OQ-008. |
| Forged approval | UI-originated reviewer identity, revision check, append-only record. | AC-AI-003; OQ-012. |
| Corrupt artifacts/checkpoints | Hash and schema verification; transactional references. | M02 artifact publication/restart: AC-OBS-003. Later graph checkpoints: AC-OBS-002. |
| SQL injection | Parameterized predefined queries inside infrastructure. | Hostile-identifier integration fixtures. |

Remote hosting, multiple users and real data require a new threat model and ADR. No enterprise authentication or regulatory compliance claim is made. Outbound model context contains minimized synthetic aggregates and necessary evidence only. M02 retention keeps all local synthetic state until explicit stopped-application whole-state cleanup under CT-018. Targeted deletion and later checkpoint/copilot lifecycle remain OQ-010; they must cover linked evidence before those operations are exposed.

Ordinary CI requires no provider credentials. Dependency additions require a concrete purpose, appropriate license/security review, lockfile change and feature/ADR traceability.

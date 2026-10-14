# Non-functional requirements

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

Every row is Proposed/P1 at its own milestone. M02 variants below do not require later AI/review tests to satisfy Definition of Ready. TBD empirical values are not accepted defaults.

| ID | Status | Applicability | Requirement | Verification / criterion |
|---|---|---|---|---|
| NFR-REL-001 | Proposed | M03 graph; M04 review | AI failure preserves committed deterministic outputs; compatible crash/resume preserves accepted node results. | AC-OBS-002; graph interruption tests after OQ-009 resolution. |
| NFR-SEC-001 | Proposed | M02 core; M03/M04 extensions | Local synthetic-only inputs, path confinement, parameterized storage, no secrets/payloads in logs. Later enforce read-only tool/run scope and prompt boundaries. | M02 AC-DQ-003/OBS-003 path/integrity/redaction fixtures; later AC-AI-002 injection/scope fixtures. |
| NFR-PERF-001 | Proposed | M02 safety; measured targets before milestone/release | CT-020 bounds parser work before implementation. Hardware/workload/latency/memory targets are calibrated later; no production SLA. | AC-DQ-003 bounds; approved local benchmark workload and measured report before M02 milestone declaration. OQ-008 measured portion remains OPEN. |
| NFR-OBS-001 | Proposed | M02 lineage; M03+ AI usage | Typed events/run versions correlate M02 operations. Later actual provider usage/cost provenance is complete or explicitly unknown. | AC-OBS-001/003; no M02 cost estimate or provider requirement. |
| NFR-AI-001 | Proposed | M03/M04 | Accepted factual claims have resolvable support; no unsupported policy claims. Usefulness/repetition thresholds remain OQ-011. | AC-AI-001 and relevant labeled evals at their gate. |
| NFR-MNT-001 | Proposed | M02 core; all later slices | Domain has no adapter/framework dependency; deterministic tests need no keys/network. | Offline tests and static import guard; AC-RISK-001. Current empty domain is not product proof. |
| NFR-REL-002 | Proposed | M02 | Same semantic input/config/rules yield identical metric semantic hashes under CT-017. Run IDs/timestamps remain lineage, not compared computation fields. AI replay is not promised deterministic. | AC-RISK-001/OBS-003 semantic replay and distinct raw-byte provenance. |
| NFR-SEC-002 | Proposed | M02 retention; later deletion/review | Retain local synthetic state until explicit whole-state cleanup under CT-018. No automatic expiry/per-run delete UI. Later targeted deletion/checkpoint/copilot retention and reviewer identity remain OQ-010/012. | AC-OBS-003 restart/whole-state cleanup; later feature-specific deletion/review tests. |
| NFR-AI-002 | Proposed | M03/M04 | Explicit call/context/time/retry/cost budgets before AI features. OQ-008/011 remain OPEN; no unlimited retries. | AC-AI-002 and budget-exhaustion evals when applicable. |

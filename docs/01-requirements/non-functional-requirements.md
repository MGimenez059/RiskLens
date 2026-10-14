# Non-functional requirements

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

Each requirement has Status Proposed and Priority P1. The verification field is its acceptance gate. No arbitrary service SLA is proposed.

| ID | Concern | Requirement | Verification | Related criterion |
|---|---|---|---|---|
| NFR-REL-001 | Recovery | No committed deterministic result is changed by an AI failure; crash/resume preserves accepted node outputs. | Fault injection before/after commit and concurrent resume; no duplicate durable result. | AC-OBS-002 |
| NFR-SEC-001 | Security and privacy | Local synthetic-only inputs; path confinement, run-scoped read tools, no arbitrary code/SQL tools; secrets and raw payloads excluded from logs. | Traversal, prompt injection and cross-run probes must be rejected; secret canary absent from captured logs. | AC-AI-002 |
| NFR-PERF-001 | Performance | Workload size, memory, latency percentiles and hardware baseline are TBD under OQ-008. | Benchmark script and approved numeric budgets required before feature readiness and release; do not treat TBD as PASS. | AC-UI-001 |
| NFR-OBS-001 | Observability and cost | Each node attempt is correlated to run/revision; usage/cost completeness is explicit. | Verify manifest/event completeness and unknown-cost behavior with fixtures. | AC-OBS-001 |
| NFR-AI-001 | Explainability and grounding | Every accepted factual claim has resolvable supporting evidence; unsupported policy claims are blocked. | All grounding safety fixtures pass; retrieval usefulness thresholds and repeated-run count TBD under OQ-011. | AC-AI-001 |
| NFR-MNT-001 | Maintainability and testability | Domain imports no infrastructure/framework packages. Deterministic tests require no API keys or network. | Static import boundary test plus offline CI; no forbidden imports. | AC-RISK-001 |
| NFR-REL-002 | Reproducibility | Identical canonical input/config/rule versions produce identical metrics. AI output is recorded, not promised bitwise reproducible. | Replay deterministic fixtures and compare canonical payloads; freeze provenance for AI audit. | AC-RISK-001 |
| NFR-SEC-002 | Retention and deletion | Retention duration and local reviewer identity are TBD under OQ-010/012. Deletion must remove linked artifacts without orphan citations. | Approved retention specification and cascade/recovery tests required before corresponding slice. | AC-AI-003 |
| NFR-AI-002 | Bounded execution | Runtime call count, timeout, retry, context and cost budgets are explicit configuration; values TBD under OQ-008/011. | Budget exhaustion stops further calls, preserves metrics and reports partial/abstained. | AC-AI-002 |

# Tool contracts

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## Shared transport contract
All requests contain run_id: Id and call_id: Id. Reject unknown fields and invalid types. The application binds run_id to the active request before tool invocation; model-supplied scope never grants access. Results are tagged envelopes: success with typed data, or error with code, sanitized message and retryable boolean. Error codes: invalid_argument, not_found, scope_denied, dependency_unavailable, timeout, conflict, internal_error. Errors never masquerade as empty successful results.

Applicability: M04 evidence-copilot product use; justified M03 use requires its own readiness evidence. Tools cannot mutate analytical results. Exchange audit events and TOOL-003 retrieval-report appends are permitted side effects, deduplicated by call_id. Same arguments and pinned artifacts/config return the same stored result; changed arguments under the same call_id conflict. Unknown values are not silently coerced. No execute_anything, arbitrary SQL, shell, generic HTTP or filesystem tool.

| Tool ID / name | Purpose | Input schema in addition to shared fields | Output schema | Side effects / idempotency | Failure modes | LLM exposure | Security |
|---|---|---|---|---|---|---|---|
| TOOL-001 / get_run_metrics | Read authoritative computed values. | metrics_id: Id. | CT-004. | Read plus audit event; pinned immutable result. | not_found, scope_denied, dependency_unavailable. | Copilot only. | Verify metrics belong to run; no arbitrary metric expression. |
| TOOL-002 / get_evidence | Resolve a known reference. | evidence_id: Id. | CT-003 plus typed payload: snapshot manifest, source_row projection, metric value, CT-014 comparison, policy chunk, rule evaluation, validation report or retrieval report. Payload must match evidence kind. | Read plus event; hash-verified result. | not_found, scope_denied, integrity mismatch as internal_error. | Copilot only. | Approved fields only; configured payload cap; no paths or URLs. |
| TOOL-003 / retrieve_run_policy | Retrieve applicable evidence from the run's pinned corpus. | query: Text. | CT-010. | Read plus event and persisted retrieval result; replay returns stored result. | unavailable corpus, timeout, invalid_argument, scope_denied. | Copilot only. | Application supplies corpus/as_of/scope/config from run; instructions in chunks remain untrusted. |

Deterministic calculation and analysis functions are application operations, not model tools. Ingestion, finalization and review are likewise not exposed to models. This avoids giving models authority they do not need.

Tool request/response schemas must have contract tests before registration. Unknown tool names are rejected. A tool error counts against the configured loop budget. No model-directed retry may override application retry or cost limits. Retrieval reports and call events are appended to a copilot exchange audit record associated with the run; they do not mutate terminal AnalysisRun results. Traceability: FR-AI-002, FR-POL-001, NFR-SEC-001, NFR-AI-002.

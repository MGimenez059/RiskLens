# Traceability matrix

Status: Proposed
Version: 1.0
Last Updated: 2026-10-15

Definitions are canonical in functional-requirements.md, non-functional-requirements.md, business-rules.md, data-contracts.md, architecture.md and evaluation-spec.md. Test names below are PLANNED identifiers, not existing functions. Product implementation is NOT IMPLEMENTED in every row. N/A means the evaluation category does not apply; it is not a waived requirement.

| Requirement | Business rule / principle | Contract | ADR | Architecture component | Implementation | Planned test | Eval |
|---|---|---|---|---|---|---|---|
| FR-DQ-001 | BR-DQ-001/002/003 | CT-001/002/005/015/016/017/018/019 | ADR-002/003/008 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_DQ_001_import_and_identity | EVAL-DQ-001/002 |
| FR-DQ-002 | BR-DQ-002/003/004 | CT-002/005/015/019/020 | ADR-002 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_DQ_002_invalid_input_blocks_metrics | EVAL-DQ-001/002/003 |
| FR-RISK-001 | BR-RISK-001/002/003/005 | CT-003/004/017 | ADR-008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_RISK_001_delinquency_rates | EVAL-RISK-001 |
| FR-RISK-002 | BR-RISK-003/007 | CT-004/006 | ADR-008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_RISK_002_detector_boundaries | EVAL-RISK-002/004 |
| FR-RISK-003 | BR-RISK-004 | CT-001/004/006/014 | ADR-003/008 | CMP-DOMAIN, CMP-APPLICATION | NOT IMPLEMENTED | test_FR_RISK_003_comparable_snapshots | EVAL-RISK-003 |
| FR-POL-001 | BR-POL-002/003 | CT-009/010 | ADR-005/006 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_POL_001_applicable_evidence | EVAL-RAG-001/002/003 |
| FR-POL-002 | BR-POL-001/002/003 | CT-007/009/010 | ADR-005/008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_POL_002_predicate_and_conflict | EVAL-POL-001/002 |
| FR-AI-001 | P-002/003/004/005/008/010 | CT-008 | ADR-001/002/006 | CMP-APPLICATION, CMP-GRAPH | NOT IMPLEMENTED | test_FR_AI_001_candidate_validation | EVAL-AGENT-001/003, EVAL-GUARDRAIL-002 |
| FR-AI-002 | P-013/017, BR-POL-003 | CT-010/013, TOOL-001/002/003 | ADR-006 | CMP-APPLICATION | NOT IMPLEMENTED | test_FR_AI_002_run_scope_and_abstention | EVAL-AGENT-002/004, EVAL-GUARDRAIL-001 |
| FR-AI-003 | BR-POL-004 | CT-008/012 | ADR-001/003 | CMP-APPLICATION, CMP-GRAPH | NOT IMPLEMENTED | test_FR_AI_003_review_revision_and_restart | EVAL-GUARDRAIL-003 |
| FR-UI-001 | BR-DQ-002, BR-RISK-005 | CT-004/005/011 | ADR-004 | CMP-PRESENTATION | NOT IMPLEMENTED | test_FR_UI_001_status_and_metric_rendering | N/A: deterministic UI test |
| FR-UI-002 | BR-POL-004, P-004 | CT-003/008/012 | ADR-004 | CMP-PRESENTATION | NOT IMPLEMENTED | test_FR_UI_002_evidence_and_review | EVAL-GUARDRAIL-003 |
| FR-OBS-001 | P-012 | CT-011/016/017/019 | ADR-003/007 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_OBS_001_m02_lineage_and_stage_events | EVAL-AGENT-003 M03 usage only |
| FR-OBS-002 | P-009/010/012 | CT-011/012 | ADR-001/003 | CMP-GRAPH | NOT IMPLEMENTED | test_FR_OBS_002_crash_replay | EVAL-GUARDRAIL-003 |
| NFR-REL-001 | P-010 | CT-011/012 | ADR-001/003 | CMP-GRAPH | NOT IMPLEMENTED | test_NFR_REL_001_transaction_recovery | EVAL-AGENT-003 |
| NFR-SEC-001 | P-017/018 | CT-003/015/018/019; CT-010/013 later | ADR-003/006/007 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_SEC_001_scope_paths_and_redaction | EVAL-GUARDRAIL-001 M03/M04 only |
| NFR-PERF-001 | P-015, BR-DQ-004 | CT-001/011/020 | ADR-003/004 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_PERF_001_approved_workload_budget | N/A: benchmark required |
| NFR-OBS-001 | P-012 | CT-011 | ADR-007 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_OBS_001_event_completeness | EVAL-AGENT-003 |
| NFR-AI-001 | P-004/005 | CT-008/010 | ADR-005/006 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_AI_001_claim_support | EVAL-RAG-001, EVAL-GUARDRAIL-002 |
| NFR-MNT-001 | P-007/009/016 | CT-001/004 | ADR-008/009 | CMP-DOMAIN | NOT IMPLEMENTED | test_NFR_MNT_001_offline_domain_boundaries | N/A: static/offline tests |
| NFR-REL-002 | P-001/012 | CT-004/011 | ADR-003/009 | CMP-DOMAIN | NOT IMPLEMENTED | test_NFR_REL_002_canonical_replay | EVAL-RISK-001 |
| NFR-SEC-002 | P-018 | CT-011/018; CT-012 M04 only | ADR-003/007 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_SEC_002_retention_and_deletion | N/A: integration tests |
| NFR-AI-002 | P-015 | CT-011/013 | ADR-006/007 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_AI_002_budget_exhaustion | EVAL-AGENT-004 |

## New M02 requirement coverage

| Requirement | Business rule / principle | Contract | ADR | Architecture component | Implementation | Planned test | Eval |
|---|---|---|---|---|---|---|---|
| FR-DQ-003 | BR-DQ-004 | CT-015/016/019/020 | ADR-002/003 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_DQ_003_parser_limits | EVAL-DQ-003 |
| FR-OBS-003 | P-012, BR-DQ-001 | CT-015/016/017/018/019 | ADR-003/007/008 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_OBS_003_publication_and_restart | N/A: deterministic fault-injection integration |

## Contract coverage

Contract status below mirrors the exact owner-approved M02 subsets in [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md); later variants remain Proposed. A future contract may reuse an accepted primitive without making its feature ready. Tests below are planned product tests, not current executed governance checks.

| Contract | Status | Applicability | Requirement | Planned verification |
|---|---|---|---|---|
| CT-001 | Accepted | M02 | FR-DQ-001/003 | import identity, provenance, parser boundaries |
| CT-002 | Accepted | M02 | FR-DQ-002, FR-RISK-001 | whole-population invalidity and zero-principal eligibility |
| CT-003 | Accepted: M02 core; Proposed: later extensions | M02 core; M03/M04 extensions | FR-DQ-002, FR-OBS-001/003; later FR-POL-001 | run-scoped snapshot/row/metric/report references |
| CT-004 | Accepted | M02 | FR-RISK-001 | exact operands, quantization and raw group sums |
| CT-005 | Accepted | M02 | FR-DQ-002/003 | typed blocking diagnostics and accepted null |
| CT-006 | Proposed | M03 | FR-RISK-002/003 | configured alert evidence; not raw-metric thresholds |
| CT-007 | Proposed | M03 | FR-POL-002 | indeterminate context and per-rule predicate evidence |
| CT-008 | Proposed | M03 observations; M04 recommendations | FR-AI-001/003 | M03 empty recommendations; M04 review gate |
| CT-009 | Proposed | M03 | FR-POL-002 | curated source/scope/version contract |
| CT-010 | Proposed | M03 | FR-POL-001 | applicable retrieval and missing/conflicting evidence |
| CT-011 | Accepted: M02 core; Proposed: later extensions | M02 core; M03/M04 extensions | FR-OBS-001/003; later FR-OBS-002 | stage-specific lineage and durable outcomes |
| CT-012 | Proposed | M04 | FR-AI-003 | explicit local review/revision/idempotency |
| CT-013 | Proposed | M04 | FR-AI-002 | scoped exchange/abstention and audit |
| CT-014 | Proposed | M03 | FR-RISK-003 | approved comparison semantics and exact difference operands |
| CT-015 | Accepted | M02 | FR-DQ-001/002/003, FR-OBS-003 | valid/rejected/conflict/limit and complete/incomplete reports |
| CT-016 | Accepted | M02 | FR-DQ-001, FR-OBS-001/003, FR-RISK-001 | allowed mode/stages/config and separate key bindings |
| CT-017 | Accepted | M02 | FR-RISK-001, FR-OBS-001/003 | 1/3, ties, zero denominators and semantic/raw hash separation |
| CT-018 | Accepted | M02 | FR-OBS-003, FR-DQ-001 | publish/commit/restart, orphan handling and whole-state cleanup |
| CT-019 | Accepted | M02 | FR-DQ-002/003, FR-OBS-001/003 | validation/event enums, severity, scope and redaction |
| CT-020 | Accepted | M02 | FR-DQ-003 | configured bound/bound+1 and no filtered result |

## Acceptance scope tracking

Owner approval date: 2026-10-15. Reviewed commit: archived baseline review revision. [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md) is authoritative for exact clauses and document sections. Status acceptance does not change any Implementation cell or execute any planned test.

| Accepted category | Exact IDs / variants |
|---|---|
| Functional requirements | FR-DQ-001, FR-DQ-002, FR-DQ-003, FR-RISK-001, FR-UI-001, FR-OBS-001 M02 only, FR-OBS-003. |
| NFR clauses | NFR-SEC-001 M02 core, NFR-PERF-001 safety/calibration policy only, NFR-OBS-001 M02 lineage, NFR-MNT-001, NFR-REL-002, NFR-SEC-002 M02 retention only. |
| Criteria | AC-DQ-001, AC-DQ-002, AC-DQ-003, AC-RISK-001, AC-UI-001, AC-OBS-001 M02 only, AC-OBS-003. |
| Rules | BR-DQ-001, BR-DQ-002, BR-DQ-003, BR-DQ-004, BR-RISK-001, BR-RISK-002, BR-RISK-003 raw metrics only, BR-RISK-005. |
| Individual ADRs | ADR-002, ADR-003, ADR-004, ADR-005 deferral only, ADR-006 boundary only, ADR-007, ADR-008, ADR-009. |

Unlisted requirement/rule/criterion variants remain Proposed. BR-RISK-006 remains Deprecated. M02 deterministic EVAL-DQ cases and the exact-metrics part of EVAL-RISK-001 remain planned GOV-002 test-design inputs, not a prerequisite for M03 AI. No M03/M04 eval or checkpoint requirement is introduced into M02.

## Baseline-only verification
scripts/check_baseline.py and tests/test_baseline.py verify document metadata, links, style, requirement coverage and architectural import boundaries. Their existence does not change any product row to implemented. Replace planned test identifiers with actual file/function references when each approved slice is delivered.

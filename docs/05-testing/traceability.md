# Traceability matrix

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

Definitions are canonical in functional-requirements.md, non-functional-requirements.md, business-rules.md, data-contracts.md, architecture.md and evaluation-spec.md. Test names below are PLANNED identifiers, not existing functions. Product implementation is NOT IMPLEMENTED in every row. N/A means the evaluation category does not apply; it is not a waived requirement.

| Requirement | Business rule / principle | Contract | ADR | Architecture component | Implementation | Planned test | Eval |
|---|---|---|---|---|---|---|---|
| FR-DQ-001 | BR-DQ-001/002/003 | CT-001/002/005 | ADR-002/003/008 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_DQ_001_import_and_identity | EVAL-DQ-001/002 |
| FR-DQ-002 | BR-DQ-002/003 | CT-002/005 | ADR-002 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_DQ_002_invalid_input_blocks_metrics | EVAL-DQ-001/002/003 |
| FR-RISK-001 | BR-RISK-001/002/005/006 | CT-003/004 | ADR-008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_RISK_001_delinquency_rates | EVAL-RISK-001 |
| FR-RISK-002 | BR-RISK-003/007 | CT-004/006 | ADR-008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_RISK_002_detector_boundaries | EVAL-RISK-002/004 |
| FR-RISK-003 | BR-RISK-004 | CT-001/004/006/014 | ADR-003/008 | CMP-DOMAIN, CMP-APPLICATION | NOT IMPLEMENTED | test_FR_RISK_003_comparable_snapshots | EVAL-RISK-003 |
| FR-POL-001 | BR-POL-002/003 | CT-009/010 | ADR-005/006 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_POL_001_applicable_evidence | EVAL-RAG-001/002/003 |
| FR-POL-002 | BR-POL-001/002/003 | CT-007/009/010 | ADR-005/008 | CMP-DOMAIN | NOT IMPLEMENTED | test_FR_POL_002_predicate_and_conflict | EVAL-POL-001/002 |
| FR-AI-001 | P-002/003/004/005/008/010 | CT-008 | ADR-001/002/006 | CMP-APPLICATION, CMP-GRAPH | NOT IMPLEMENTED | test_FR_AI_001_candidate_validation | EVAL-AGENT-001/003, EVAL-GUARDRAIL-002 |
| FR-AI-002 | P-013/017, BR-POL-003 | CT-010/013, TOOL-001/002/003 | ADR-006 | CMP-APPLICATION | NOT IMPLEMENTED | test_FR_AI_002_run_scope_and_abstention | EVAL-AGENT-002/004, EVAL-GUARDRAIL-001 |
| FR-AI-003 | BR-POL-004 | CT-008/012 | ADR-001/003 | CMP-APPLICATION, CMP-GRAPH | NOT IMPLEMENTED | test_FR_AI_003_review_revision_and_restart | EVAL-GUARDRAIL-003 |
| FR-UI-001 | BR-DQ-002, BR-RISK-005 | CT-004/005/011 | ADR-004 | CMP-PRESENTATION | NOT IMPLEMENTED | test_FR_UI_001_status_and_metric_rendering | N/A: deterministic UI test |
| FR-UI-002 | BR-POL-004, P-004 | CT-003/008/012 | ADR-004 | CMP-PRESENTATION | NOT IMPLEMENTED | test_FR_UI_002_evidence_and_review | EVAL-GUARDRAIL-003 |
| FR-OBS-001 | P-012 | CT-011 | ADR-003/007 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_FR_OBS_001_manifest_and_unknown_cost | EVAL-AGENT-003 |
| FR-OBS-002 | P-009/010/012 | CT-011/012 | ADR-001/003 | CMP-GRAPH | NOT IMPLEMENTED | test_FR_OBS_002_crash_replay | EVAL-GUARDRAIL-003 |
| NFR-REL-001 | P-010 | CT-011/012 | ADR-001/003 | CMP-GRAPH | NOT IMPLEMENTED | test_NFR_REL_001_transaction_recovery | EVAL-AGENT-003 |
| NFR-SEC-001 | P-017/018 | CT-003/010/013 | ADR-006/007 | CMP-APPLICATION, CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_SEC_001_scope_paths_and_redaction | EVAL-GUARDRAIL-001 |
| NFR-PERF-001 | P-015 | CT-001/011 | ADR-003/004 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_PERF_001_approved_workload_budget | N/A: benchmark required |
| NFR-OBS-001 | P-012 | CT-011 | ADR-007 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_OBS_001_event_completeness | EVAL-AGENT-003 |
| NFR-AI-001 | P-004/005 | CT-008/010 | ADR-005/006 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_AI_001_claim_support | EVAL-RAG-001, EVAL-GUARDRAIL-002 |
| NFR-MNT-001 | P-007/009/016 | CT-001/004 | ADR-008/009 | CMP-DOMAIN | NOT IMPLEMENTED | test_NFR_MNT_001_offline_domain_boundaries | N/A: static/offline tests |
| NFR-REL-002 | P-001/012 | CT-004/011 | ADR-003/009 | CMP-DOMAIN | NOT IMPLEMENTED | test_NFR_REL_002_canonical_replay | EVAL-RISK-001 |
| NFR-SEC-002 | P-018 | CT-011/012 | ADR-003/007 | CMP-INFRASTRUCTURE | NOT IMPLEMENTED | test_NFR_SEC_002_retention_and_deletion | N/A: integration tests |
| NFR-AI-002 | P-015 | CT-011/013 | ADR-006/007 | CMP-APPLICATION | NOT IMPLEMENTED | test_NFR_AI_002_budget_exhaustion | EVAL-AGENT-004 |

## Baseline-only verification
scripts/check_baseline.py and tests/test_baseline.py verify document metadata, links, style, requirement coverage and architectural import boundaries. Their existence does not change any product row to implemented. Replace planned test identifiers with actual file/function references when each approved slice is delivered.

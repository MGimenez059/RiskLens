# Vertical slice roadmap

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Acceptance: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md), owner approval 2026-10-15, reviewed commit archived baseline review revision. Only the document/section scope recorded there is accepted; later feature gates remain in force.

| Stage | Applicability and deliverable | Exit evidence |
|---|---|---|
| M01 | Corrected specification baseline reviewed and formally accepted. | GOV-001 reviewed commit, exact accepted IDs/ADRs and deferral gates. |
| M02 | Deterministic bundle import, validation/outcomes, exposure, delinquency, raw concentration, availability, persistence/lineage, restart/replay and Streamlit dashboard. | AC-DQ-001/002/003, AC-RISK-001, AC-UI-001, AC-OBS-001/003; accepted CT-001/002/003 M02/004/005/011 M02/015/016/017/018/019/020; local workload measurements. |
| M03 | Approved detectors/comparison, curated policies, grounded structured observations and optional bounded graph orchestration. | AC-RISK-002/003, AC-POL-001/002, AC-AI-001, AC-OBS-002 as applicable; resolve OQ-004/005/006/007/009 graph/011 and AI budgets. No high-impact recommendation or human-review exit gate. |
| M04 | Evidence copilot/tool use and high-impact recommendations with explicit human review. | AC-AI-002/003, AC-UI-002; OQ-012 and review/lifecycle portions resolved; E2E evidence. |
| M05 | Audited reproducible active-v1 release. | All approved active-v1 FR/NFR and applicable evals satisfied, measured release targets and no unresolved release blocker. |

Default, DTI and score analytics are outside active v1 and do not gate any row. M02 requests only its deterministic mode. M03 inspection suggestions are not business-action recommendations. M04 may not expose high-impact suggestions before functional review. No graph checkpoint, policy engine or AI capability is required by M02.
Input safety caps precede M02 implementation. Performance targets are calibrated against working measured behavior before declaring the milestone/release ready; no production SLA is invented. Each future feature needs GOV-002 even after baseline acceptance. A deferred feature is not implemented by listing its future contract.

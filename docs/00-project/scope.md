# Scope

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## IN SCOPE: local synthetic v1
- One local analyst and one writer; USD portfolios; immutable snapshots with globally unique snapshot_id and one portfolio_id owner.
- CSV plus JSON manifest bundle import, strict whole-snapshot validation, explicit valid/rejected/conflict/limit outcomes.
- Deterministic outstanding-principal exposure, open-loan count/exposure delinquency rates, DPD and raw borrower/segment concentration shares.
- M03+ configured concentration alerts/anomalies and temporal comparison only after their open questions are resolved.
- Later curated synthetic Markdown policies and grounded structured observations; M04 evidence copilot and human review of high-impact recommendations.
- Local persistence, evidence lineage, restart readability, replay safety, Streamlit dashboard and applicable-stage observability.

## OUT OF SCOPE: active v1
Default analytics, DTI and credit-score analytics; autonomous credit approval/rejection; real banking data; payments; production bank integrations; mobile app; model training from scratch; predictive credit scoring; regulatory PD/LGD/ECL; multi-tenancy/SSO; distributed deployment; FX; automatic portfolio actions; OCR/complex PDFs; unrestricted agent browsing.
Default, DTI and score definitions remain deferred concepts in the glossary. Their inclusion requires a future CR and explicit financial semantics; they are not v1 acceptance or release gates. No universal credit convention or enterprise deployment readiness is claimed.

## Execution and stage boundaries
This correction changes specifications and governance tooling only. No M02 implementation exists. M02 has no LLM, LangChain, LangGraph, RAG, policy engine, graph checkpoint, recommendation or pending-review UI dependency. M03 AI emits observations/explanations/inspection suggestions only; high-impact action recommendations and human review belong to M04. Policy conflicts remain indeterminate and are corrected in the corpus outside the run.

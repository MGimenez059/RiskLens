# ADR-005: Defer retrieval storage selection

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15
Applicability: M03 deferral / future adapter
Acceptance Record: [BASELINE-ACCEPTANCE-001](../changes/BASELINE-ACCEPTANCE-001.md)
Acceptance Date: 2026-10-15
Accepted By: Product Owner, human user in this conversation
Reviewed Commit: archived baseline review revision
Acceptance Scope: Individual direction/deferral decision only; later contracts and feature gates remain as recorded.

- ID: ADR-005
- Date: 2026-10-07
- Related requirements: FR-POL-001, NFR-AI-001
- Supersedes: None
- Superseded by: None
- Decision owner: Product Owner; explicit acceptance recorded 2026-10-15.

## Context
Corpus size, metadata filtering, embedding choice and relevance targets are not established. Selecting a vector database now would not be evidence-based.

## Decision
Defer the provider/model/vector-store selection until OQ-007 and a versioned retrieval benchmark. Require a PolicyRetriever port and CT-010 regardless of adapter. Compare a local embedded store with exact in-memory search; acceptance of this ADR accepts deferral only.

## Alternatives
A hosted vector database adds operations and data egress without known need. Choosing a popular local library immediately risks adapting the domain to its metadata limits. Lexical search is a useful benchmark alternative but does not establish embedding benefit without measurement.

## Consequences
RAG implementation is blocked until a subsequent selection ADR resolves the decision. The first deterministic slice is unaffected. Index identity must include corpus, chunking and embedding versions.

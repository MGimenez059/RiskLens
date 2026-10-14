# RAG specification

Status: Proposed
Version: 1.0
Last Updated: 2026-10-07

## Corpus and ingestion
Support synthetic UTF-8 Markdown policies in v1. Each document has CT-009 metadata, original byte hash and canonical text hash. Ingestion is human-triggered, never an LLM tool. Validate scope, authority, version and dates before indexing. Reject missing metadata, changed bytes under an existing version, and unsupported formats. Do not fetch embedded URLs.

Parse headings and paragraphs; preserve section paths and offsets into normalized text. Version deterministic normalization. Chunk at section boundaries, split oversized sections at paragraphs, and preserve parent metadata. Size, overlap and token budget are TBD under OQ-007 and must be benchmarked before implementation. Never join unrelated policies into a chunk.

## Index and retrieval
Embedding model, dimension, metric and vector store are deferred in ADR-005. Compare a local embedded vector store against in-memory exact search on a curated corpus. Version corpus, parser, chunker, embedding and index together. A new embedding model requires an index rebuild.

Requests include run_id, as_of, scope and corpus version. Filter eligibility before selecting evidence. top_k is a positive configured integer chosen through evaluation, not a hidden default. Record candidate scores, selected IDs and configuration. Scores are not policy-compliance probabilities. Re-ranking is deferred unless evaluation demonstrates need.

## Grounding
Validate citation ID, document/version, normalized hash, section and offsets. Applicability and source support are separate from similarity. Insufficient retrieval cannot establish absence of policy. Preserve contradictory applicable sources and mark conflict under BR-POL-002. A model must not choose authority by similarity or writing quality.

Policy evaluation uses human-curated CT-009 predicates. Untranslatable narrative remains indeterminate. Instructions embedded in retrieved documents are untrusted content. Empty evidence yields abstention, not invented policy.

## Evaluation gate
Use EVAL-RAG-001/002/003 and EVAL-POL-001/002. Measure labeled recall@k, citation resolvability, unsupported policy claims, expired-source leakage and conflict handling. Include unanswerable and adversarial queries. Usefulness thresholds require OQ-011; every safety fixture must pass. Store queries, gold chunk IDs, retrieved IDs, configuration hashes and outcomes. Never tune on the holdout set.

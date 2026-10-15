# BASELINE-ACCEPTANCE-001: RiskLens Specification Baseline v1.0

Status: Accepted
Version: 1.0
Last Updated: 2026-10-15

Approval State: Owner Approved
Preparation Date: 2026-10-15
Decision Owner: Product Owner, the human user
Owner Identity: Human user in this conversation, explicitly acting as Product Owner; personal name not supplied
Approval Date: 2026-10-15, America/Buenos_Aires
Owner Decision: ACCEPT WITH EXPLICIT DEFERRALS
Technical Reviewer: Current architecture review agent, Architect/Auditor role
Reviewed Commit: archived baseline review revision
Reviewed Commit Parent: archived baseline review parent
Reviewed Commit Message: spec: finalize RiskLens baseline v1.0 for acceptance
Technical Recommendation: ACCEPT WITH EXPLICIT DEFERRALS
Actual Accepted Documents and IDs: Exactly the document sections, IDs, clauses and variants in the accepted-scope tables below; no others
Implementation Authorization: M02 feature creation and product implementation are not authorized by this acceptance

## Decision boundary
The human Product Owner explicitly approved this exact scope and reviewed commit on 2026-10-15 under [GOV-001](../00-project/baseline.md). This record now records that received decision, not agent approval. The prepared record is preserved at commit archived acceptance preparation revision. Approval did not change normative product behavior or accept unresolved later contracts.

The reviewed specification is the tree at the SHA above. This record, the [review-target locator](baseline-review-target.md) and the [CR-001 execution metadata](CR-001-baseline-acceptance-corrections.md) were prepared after that commit. Their preparation and subsequent owner-acceptance metadata do not replace the reviewed specification target. The [final closure report](../00-project/baseline-closure-report.md) is part of the reviewed target; previous reports retain historical context.

Only the approved documents, sections, IDs and variants are now Accepted. Mixed-stage containers remain Proposed. Acceptance of the listed direction, constraints and future gates does not approve unresolved future implementation contracts. The baseline prerequisite of GOV-002 is satisfied for this exact subset; feature preparation and separate M02 implementation authorization are still required. This task does not start M02.

## Accepted document and section scope
Document identities are existing repository-relative paths. They are not new document IDs. Only the sections and variants listed here are accepted; per-ID tables below narrow mixed documents further.

| Document identity | Exact accepted scope | Excluded scope or status boundary |
|---|---|---|
| AGENTS.md | Entire agent governance instruction set, including model routing, and verification. | Does not grant product implementation permission. |
| docs/00-project/baseline.md | GOV-001, GOV-002, GOV-003, GOV-004 and canonical reading/acceptance procedure. | Does not accept every document in the reading list. |
| docs/00-project/principles.md | P-001 through P-021 and Source precedence. | Later-stage principles constrain future work; they do not make later features ready now. |
| docs/00-project/writing-policy.md | STYLE-001, STYLE-002, STYLE-003. | No exception to English, evidence or punctuation rules. |
| docs/00-project/vision.md | Product purpose, intended user and assistance boundaries as product direction. | No implementation, accuracy or enterprise readiness claim. |
| docs/00-project/scope.md | IN SCOPE stage allocation, OUT OF SCOPE active-v1 exclusions, Execution and stage boundaries. | Listing M03/M04 scope does not accept its unresolved details. |
| docs/00-project/glossary.md | Terminology and explicit Default/DTI/score deferral; exposure/delinquency meanings constrained by the listed M02 rules. | No financial meaning is assigned to deferred concepts. |
| docs/00-project/roadmap.md | M01 through M05 allocation and exit-gate policy, including deterministic M02 and later AI/review gates. | Future feature contracts remain Proposed; no stage is declared achieved. |
| docs/00-project/model-usage-policy.md | Permanent policy, updateable role mapping and separation of development roles from runtime models. | No runtime provider/model selection or automatic switching capability. |
| docs/01-requirements/use-cases.md | UC-001 M02 import/compute/persist/display path, limited by the accepted IDs below. | UC-002, UC-003, UC-004 and UC-005 remain Proposed. Container remains Proposed. |
| docs/01-requirements/functional-requirements.md | Only the seven listed M02 requirement IDs/variants, now Accepted. | Container and unlisted variants remain Proposed. |
| docs/01-requirements/non-functional-requirements.md | Only the six precisely scoped NFR clauses below. | Mixed rows and container remain Proposed where later clauses are unresolved. |
| docs/01-requirements/acceptance-criteria.md | Only the seven listed M02 criteria/variants, as required future behavior. | Container remains Proposed; approval is not a test result. |
| docs/02-domain/domain-model.md | M02 aggregates and value objects; M02 run lifecycle; domain independence and global identity constraints. | Later entities/lifecycle and corresponding diagram relationships remain Proposed. Container remains Proposed. |
| docs/02-domain/business-rules.md | Only the eight listed rule IDs/variants. | Later rules remain Proposed; BR-RISK-006 stays Deprecated. Container remains Proposed. |
| docs/02-domain/data-contracts.md | Contract conventions as applied to the twelve listed M02 contracts, their shared DQ envelope and Contract evolution process. | Later generated-output behavior, fields and variants remain Proposed. Container remains Proposed. |
| docs/03-architecture/architecture.md | Local modular single-process boundaries; M02 presentation/application/domain/infrastructure ownership; M02 Persistence and SQL; M02 Incremental adoption and isolation direction. | CMP-GRAPH, future provider/retrieval/review ports, node uniqueness/checkpointer reconciliation and future runtime adoption remain Proposed. Container remains Proposed. |
| docs/03-architecture/security.md | M02 synthetic input, confined paths/state, bounded parsing, parameterized SQL, safe events and verified artifact publication/cleanup controls. | AI/tool/review/cloud controls remain Proposed. No enterprise deployment certification. Container remains Proposed. |
| docs/03-architecture/observability.md | M02 CT-019 event schema, CT-011/017 lineage/replay and CT-018 retention direction. | Provider/tool/review usage, cost and lifecycle extensions remain Proposed. Container remains Proposed. |
| docs/05-testing/test-strategy.md | Verification strategy, offline/fake dependency direction and separation of governance checks from planned product tests/evals. | Approval of the strategy does not satisfy future tests or accept deferred behavior. |
| docs/changes/README.md | Change process, owner authority and editorial-versus-behavior distinction. | CR-001 correction authorization is not baseline approval. |
| docs/adr/ADR-002-validation.md | ADR-002 individually, as described below. | No implementation claim. |
| docs/adr/ADR-003-persistence.md | ADR-003 individually, M02 local persistence direction. | No graph checkpointer selection. |
| docs/adr/ADR-004-ui.md | ADR-004 individually, local Streamlit adapter direction. | No enterprise UI/deployment claim. |
| docs/adr/ADR-005-retrieval.md | ADR-005 individually, deferral and later benchmark/selection gate. | No vector store or embedding model chosen. |
| docs/adr/ADR-006-providers.md | ADR-006 individually, application-owned ports and incremental adapter direction. | No M02 provider dependency or runtime model chosen. |
| docs/adr/ADR-007-observability.md | ADR-007 individually, structured local observability direction. | Later event extensions remain gated. |
| docs/adr/ADR-008-repository.md | ADR-008 individually, modular dependency direction. | No speculative port/framework implementation. |
| docs/adr/ADR-009-tooling.md | ADR-009 individually, current development tooling direction. | No product dependencies added. |

The question register, ADR index and traceability matrix are tracking artifacts. Their headers do not accept all entries. README, CHANGELOG, inventory, closure/correction/review reports and historical owner/CR records remain evidence or explanatory records, not alternative normative authorities. Templates remain Draft. No other document is implicitly included in the accepted document set.

## Exact accepted governance, principle and style IDs
- Governance: GOV-001, GOV-002, GOV-003, GOV-004.
- Principles: P-001, P-002, P-003, P-004, P-005, P-006, P-007, P-008, P-009, P-010, P-011, P-012, P-013, P-014, P-015, P-016, P-017, P-018, P-019, P-020, P-021.
- Writing: STYLE-001, STYLE-002, STYLE-003.

## Exact accepted functional requirements
| ID | Accepted variant |
|---|---|
| FR-DQ-001 | Entire M02 immutable synthetic import requirement. |
| FR-DQ-002 | Entire M02 quality diagnostic/strict rejection requirement. |
| FR-DQ-003 | Entire M02 bounded parser/diagnostic requirement with reviewed CT-020 profile. |
| FR-RISK-001 | Entire M02 deterministic metric requirement, including raw group shares without alerts. |
| FR-UI-001 | Entire M02 stored deterministic dashboard requirement. |
| FR-OBS-001 | M02 hashes/versions/typed events/run outcomes only. M03+ provider usage/cost remains Proposed. |
| FR-OBS-003 | Entire M02 durable publication/restart/replay requirement. |

## Exact accepted NFR clauses
| ID | Accepted clause | Clause that remains Proposed or OPEN |
|---|---|---|
| NFR-SEC-001 | M02 local synthetic inputs, path confinement, parameterized storage and no secrets/payloads in events. | M03/M04 tool/run/prompt controls. |
| NFR-PERF-001 | M02 CT-020 safety bounds and requirement to calibrate measured targets before milestone/release. | Hardware/workload/latency/memory target values remain OPEN at OQ-008; no production SLA. |
| NFR-OBS-001 | M02 typed event/version/lineage correlation. | M03+ provider usage/cost provenance implementation. |
| NFR-MNT-001 | Domain isolation and deterministic offline testability requirement. | Future framework/adapter implementations still need their own approved slice; accepting the invariant does not approve them. |
| NFR-REL-002 | M02 deterministic canonical semantic replay under CT-017, excluding generated lineage values. | No deterministic AI replay promise. |
| NFR-SEC-002 | M02 retain local synthetic state until explicit stopped-application whole-state cleanup under CT-018. | Later targeted deletion/checkpoint/copilot retention and reviewer identity at OQ-010/OQ-012. |

## Exact accepted acceptance criteria
| ID | Accepted variant |
|---|---|
| AC-DQ-001 | Entire M02 import/identity/replay/strict validation criterion. |
| AC-DQ-002 | Entire M02 invalid-versus-valid-data diagnostic criterion. |
| AC-DQ-003 | Entire M02 bound/bound+1 and diagnostic-completeness criterion. |
| AC-RISK-001 | Entire M02 exact arithmetic, denominator-specific availability, raw groups and semantic replay criterion. |
| AC-UI-001 | Entire M02 deterministic dashboard criterion; future partial/review UI excluded. |
| AC-OBS-001 | M02 manifest/hash/ownership/version/limit/event/no-provider variant only. |
| AC-OBS-003 | Entire M02 interrupted publication, restart, integrity, replay and whole-state cleanup criterion. |

These are accepted behavior criteria, not executed product tests. Product tests remain planned.

## Exact accepted business rules
| ID | Accepted variant |
|---|---|
| BR-DQ-001 | Global snapshot identity, single owner and within-snapshot loan uniqueness. |
| BR-DQ-002 | Complete-population structural/field/core invariants and strict rejection. |
| BR-DQ-003 | USD/no-imputation/no-coercion and valid null segment/empty/zero-exposure behavior. |
| BR-DQ-004 | Bounded parsing and diagnostic collection without truncated metrics. |
| BR-RISK-001 | Outstanding-principal exposure and total/open counts. |
| BR-RISK-002 | Open-loan count/exposure delinquency populations and denominator availability. |
| BR-RISK-003 | M02 raw borrower/segment group metrics only. Alert thresholds/operators remain Proposed at OQ-004. |
| BR-RISK-005 | Exact operands, USD minor units, four-digit half-even ratios and unrounded comparisons under CT-017. |

## Exact accepted contracts
| ID | Accepted variant |
|---|---|
| CT-001 | Entire M02 snapshot/manifest/bundle/import-identity contract. |
| CT-002 | Entire M02 loan observation contract. |
| CT-003 | Required common fields and M02 kinds snapshot, source_row, metric, validation_report, including only their locators/invariants. |
| CT-004 | Entire M02 metrics/MetricValue/GroupShare contract; raw groups only. |
| CT-005 | Entire M02 DQ finding/report contract, including shared envelope as applied to DQ only. |
| CT-011 | M02 manifest, StageOutcome and RunError fields/lifecycle only; M03/M04 extensions excluded. |
| CT-015 | Entire M02 Import and Validation Result. |
| CT-016 | Entire M02 Analysis Request and Analysis Configuration; requested stages exactly validate_portfolio and calculate_metrics. |
| CT-017 | Entire M02 Arithmetic Serialization and Canonical Hashing contract. |
| CT-018 | Entire M02 Local Artifact Publication and Recovery contract, including stopped-application whole-state cleanup. |
| CT-019 | Entire M02 Typed Events and Validation Catalogs, including typed operation errors/dispositions. |
| CT-020 | Entire M02 Bounded Parser Configuration and the unchanged provisional profile below. |

CT-020 exact provisional local safety profile accepted by the Product Owner on 2026-10-15:

| Bound | Approved provisional value |
|---|---|
| Combined CSV and manifest bytes | 10 MiB |
| Manifest bytes | 64 KiB |
| Loan records, excluding header | 50,000 |
| UTF-8 bytes per field/scalar | 4,096 |
| Characters per input numeric token | 24 |
| Collected diagnostics | 1,000 |

The canonical CT-020 definitions, counting rules, configuration identity/hash and dispositions govern this table. These are configurable Provisional Local Safety Limits, not measured performance targets, financial thresholds or production SLAs. No values were changed during closure. Measured calibration remains required before M02 milestone declaration.

## Individually accepted ADRs
| ADR | Accepted decision | Deferred boundary |
|---|---|---|
| ADR-002 | Pydantic at validated boundaries; standard Python domain. | No product models implemented now. |
| ADR-003 | Local SQLite metadata and immutable local artifact files, one writer. | Graph checkpoint adapter/reconciliation details remain OQ-009. |
| ADR-004 | Streamlit local presentation adapter calling Application. | Domain remains independent; no production deployment claim. |
| ADR-005 | Defer embedding/vector-store choice until benchmark and selection ADR. | OQ-007 and RAG implementation remain open. |
| ADR-006 | Small application-owned provider/retrieval ports added only when a slice uses them. | Runtime provider/model/evals remain OQ-011; no M02 provider. |
| ADR-007 | Structured local events and lineage before hosted tracing. | Later AI/tool/review event contracts remain Proposed. |
| ADR-008 | Modular src layout and explicit inward dependency direction. | No unused port/agent framework required. |
| ADR-009 | uv and minimal Python development quality tooling. | No product dependency installed by acceptance. |

ADR-001 remains Proposed. ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008 and ADR-009 are individually Accepted under this owner decision. Their listed deferred boundaries remain Proposed/Open.

## Exact remaining Proposed IDs and specifications
| Area | Exact retained scope |
|---|---|
| Functional requirements | FR-RISK-002, FR-RISK-003, FR-POL-001, FR-POL-002, FR-AI-001, FR-AI-002, FR-AI-003, FR-UI-002, FR-OBS-002; M03+ usage/cost variant of FR-OBS-001. |
| NFRs | NFR-REL-001, NFR-AI-001, NFR-AI-002; future clauses of NFR-SEC-001, NFR-OBS-001 and NFR-SEC-002 listed above. Measured NFR-PERF-001 target values remain OPEN. |
| Acceptance criteria | AC-RISK-002, AC-RISK-003, AC-POL-001, AC-POL-002, AC-AI-001, AC-AI-002, AC-AI-003, AC-UI-002, AC-OBS-002; M03+ usage/cost variant of AC-OBS-001. |
| Business rules | BR-RISK-003 alert configuration, BR-RISK-004, BR-RISK-007, BR-POL-001, BR-POL-002, BR-POL-003, BR-POL-004. BR-RISK-006 remains Deprecated, not Proposed or Accepted. |
| Contracts | CT-006, CT-007, CT-008, CT-009, CT-010, CT-012, CT-013, CT-014; later CT-003 kinds/locators, later shared finding-envelope applications and CT-011 AI/prior/review extensions. Future CT-016/019 mode/event extensions need review before use. |
| Use cases and domain | UC-002, UC-003, UC-004, UC-005 in docs/01-requirements/use-cases.md; Later entities and lifecycle variants in docs/02-domain/domain-model.md. |
| Architecture | docs/adr/ADR-001-langgraph.md; docs/03-architecture/graph-spec.md; docs/03-architecture/rag-spec.md; graph/provider/retrieval/review extensions in architecture.md, security.md and observability.md. |
| AI specifications | docs/04-ai/agent-responsibilities.md; docs/04-ai/tool-contracts.md; docs/04-ai/prompt-specs.md; docs/04-ai/guardrails.md; docs/04-ai/evaluation-spec.md, including every AI-, TOOL-, PROMPT- and EVAL-prefixed record. They remain planned specifications, not implemented evals. |

Acceptance of the invariant that later work must preserve authoritative metrics, grounding, bounded scope and human authority does not accept unresolved implementation detail. No mixed-stage document receives blanket Accepted status.

EVAL-DQ-001, EVAL-DQ-002, EVAL-DQ-003 and the exact-metrics portion of EVAL-RISK-001 are M02 test-design inputs, even though evaluation-spec.md remains Proposed. Their feature-specific test preparation belongs to GOV-002. Their location under docs/04-ai does not require M03 detectors, narratives, retrieval, model thresholds or provider calls for M02.

## Open questions, decision owners and gates
Every row has decision owner Product Owner and technical preparation Architect/Auditor. CLOSED records the prior owner decision, not baseline acceptance. No historical question ID is deleted.

| Question / portion | Retained disposition | Blocking gate and reference |
|---|---|---|
| OQ-001 | CLOSED | No unresolved M02 choice; USD/principal/global identity/import semantics in CT-001/002/015/017/019. |
| OQ-002 active-v1 scope | CLOSED | Default excluded from active v1; no metric/release dependency. |
| OQ-002 financial meaning | DEFERRED | Post-v1 feature requires scope CR and financial definition; no threshold invented. |
| OQ-003 | DEFERRED, outside active v1 | DTI/credit score only through future extension CR. |
| OQ-004 | OPEN | Before M03 detectors; FR-RISK-002, BR-RISK-003 alerts/007, CT-006. |
| OQ-005 | OPEN | Before M03 temporal comparison; FR-RISK-003, BR-RISK-004, CT-014. |
| OQ-006 | OPEN | Before M03 policy features; FR-POL-001/002, BR-POL-001/002/003, CT-007/009. Authority, coverage and system-rule identity remain unresolved; conflicts stay indeterminate. |
| OQ-007 | OPEN | Before M03 retrieval; ADR-005 accepts deferral only; CT-010 and rag-spec.md. Embedding/index/chunk/source-span/sufficiency selection needs benchmark and selection ADR. |
| OQ-008 M02 safety | CLOSED | Exact CT-020 profile accepted on 2026-10-15 as configurable local-development safety limits only. GOV-002 and separate implementation authorization remain. |
| OQ-008 measured performance | OPEN | Measured workload/hardware/latency/memory targets before M02 milestone release and affected later releases; NFR-PERF-001. |
| OQ-008 AI budgets | OPEN | Before M03 AI/M04 copilot readiness and external calls; NFR-AI-002. |
| OQ-009 M02 platform | CLOSED | SQLite/immutable artifacts/Streamlit/one writer; ADR-003/004 are Accepted under this record; no graph/review detail is accepted. |
| OQ-009 graph persistence | OPEN | Before M03 graph readiness; ADR-001, FR-OBS-002, graph-spec.md. |
| OQ-009 review | OPEN | Before M04 review readiness; CT-012, FR-AI-003, OQ-012. Includes aggregation/interrupt/resume details. |
| OQ-010 M02 retention | CLOSED | CT-018 whole-state operator cleanup; no expiry/per-run deletion UI. |
| OQ-010 later lifecycle | OPEN | Before affected policy/checkpoint/copilot artifact features or targeted deletion exposure; NFR-SEC-002 later clause. |
| OQ-011 | OPEN | Before M03 grounded AI readiness and applicable releases; runtime models/prompts/holdouts/replications/empirical eval thresholds in docs/04-ai. |
| OQ-012 | OPEN | Before M04 high-impact recommendations/review; local reviewer identity/action evidence in CT-012/FR-AI-003. |

REVIEW-007 detailed review behavior and REVIEW-008 through REVIEW-014 retain the corresponding M03/M04 gates. Only the milestone/scope portion of REVIEW-007 is closed. Detailed REVIEW-009 review aggregation remains open. No later question becomes an M02 prerequisite because it shares a document with M02.

## Exceptions, limitations and verification evidence
- This is a local, single-user, single-writer, controlled synthetic USD v1 direction. No FX, real banking data, multi-tenancy, distributed deployment, enterprise authentication or production readiness is approved.
- Strict validation rejects the whole snapshot for contract defects. Identity conflicts and safety failures have separate typed outcomes. Valid null segment, valid empty data, zero principal and denominator unavailability are not invented DQ findings. No partial-population authoritative metric is permitted.
- M02 requires no LLM, LangChain, LangGraph, RAG, vector store, policy engine, model provider, human review, pending-review UI or AI checkpoint. M03 produces grounded observations; high-impact recommendations and human review remain M04.
- No unresolved baseline-level M02 semantic contradiction was found. Owner acceptance and exact safety-profile approval are recorded here; GOV-002 feature preparation and separate implementation authorization remain necessary.
- Local verification on 2026-10-15 passed: locked uv sync, Ruff lint/format, mypy for 3 source files, pytest with 15 governance tests including 7 negative document fixtures, baseline checker for 62 Markdown documents at the target, and Git whitespace checks. After this record was added, the checker passed for 63 Markdown documents, all 15 tests passed again and Git whitespace checks passed. These are governance/tooling checks, not product behavior tests.
- The architecture SVG was parsed and its labels matched against the source architecture. No working dashboard, product runtime test, remote CI run or final publication capture is claimed.

## Recorded owner decision and preparation history
The Product Owner explicitly reviewed RiskLens Specification Baseline v1.0, reviewed commit archived baseline review revision, and the prepared acceptance record at archived acceptance preparation revision. The received decision was ACCEPT WITH EXPLICIT DEFERRALS, approving exactly the recorded document sections, requirement variants, NFR clauses, criteria, business rules, contracts, individual ADRs and all six CT-020 local safety values. No scope amendment was requested.

Owner identity is the human user expressly acting as Product Owner in this conversation. No personal name or separate signature has been invented. Approval was received and recorded on 2026-10-15 in America/Buenos_Aires. The preparation date remains separate.

Verbatim owner approval excerpt:
```text
I am the Product Owner of RiskLens.

I explicitly approve the proposed acceptance scope exactly as documented in:

`docs/changes/BASELINE-ACCEPTANCE-001.md`

including the listed accepted subsets, constraints, stage boundaries and explicit deferrals.
```

Verbatim owner decision and implementation boundary:
```text
ACCEPT WITH EXPLICIT DEFERRALS

Do not modify normative product behavior while recording this acceptance.

Do not implement M02 in this task.
```

Source: user-provided acceptance instruction, attachment b704c968-d67c-417b-8c29-d89648821eb8/Texto pegado.txt. SHA-256 of original supplied bytes: 6f78647b121a79ebd16ad56227cec62abd1bde985c542af95063e91685d810e9. The human instruction, not the prior locator's example wording, is the source of approval.

## Applied acceptance and retained gates
- Accepted only the complete governance/direction documents and exact mixed-stage sections in the tables above, plus the eight individual ADR decisions.
- Mixed-stage headers remain Proposed. Split FR-OBS-001, AC-OBS-001, BR-RISK-003, CT-003, CT-011 and mixed NFR clauses retain later Proposed variants. BR-RISK-006 remains Deprecated.
- OQ-008 M02 safety is CLOSED by this approval. Measured performance, AI budgets and every other deferred portion retain their original owners/gates.
- Requirement and contract traceability reflect accepted variants while all product Implementation cells remain NOT IMPLEMENTED and product tests/evals remain planned.
- Current acceptance verification is recorded in [the acceptance verification report](baseline-acceptance-verification-2026-10-15.md). Historical review results above remain pre-acceptance evidence.
- Baseline acceptance does not create a feature specification, start M02, authorize deferred implementation or authorize publication.

## Completed owner decision
```text
Owner identity: Human user in this conversation, explicitly acting as Product Owner
Approval date: 2026-10-15, America/Buenos_Aires
Decision: ACCEPT WITH EXPLICIT DEFERRALS
Reviewed commit: archived baseline review revision
Prepared acceptance scope revision: archived acceptance preparation revision
Accepted document sections and IDs: Exactly the accepted-scope tables above
Approved scope amendments: None
Exceptions/deferrals/gates: All listed boundaries retained
M02 feature creation and implementation authorization: Not granted
```

The next recommended task is a separately authorized GOV-002 specification for the first deterministic snapshot-analysis vertical slice. No feature file is created by this acceptance task.

# Baseline Acceptance Review

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14

## Review disposition
**DO NOT ACCEPT the current files unchanged.** The local modular architecture is appropriate. A small set of contract and milestone inconsistencies prevents unqualified acceptance. After the corrections below are applied and the remaining M02 owner choices are recorded, the intended disposition is **ACCEPT WITH EXPLICIT DEFERRALS**. That future disposition is conditional, not approval of this revision.

This review covers all twelve open questions and all nine proposed ADRs, plus principles, requirements, rules, contracts, architecture, graph/RAG design, testing, and milestone definitions. The repository was read directly. The initial baseline has no Git commit; all project files remain untracked. No product functionality or acceptance status was changed. No second reviewer or subagent participated; this is a fresh critical review of the repository, not an independent multi-person audit.

Review findings are advisory. The [proposed correction CR](../changes/CR-001-baseline-acceptance-corrections.md) tracks their impact. Canonical behavior remains in the original Proposed specifications until a reviewed update is applied. Neither this report nor the CR silently overrides them.

## 1. Blocking decisions for M02

| Decision | Required resolution | Recommendation | Source |
|---|---|---|---|
| Monetary scope | Name the supported synthetic currency and its precision. | One explicitly configured currency with two fractional digits for this fixture; no FX. The actual currency code remains an owner choice. | OQ-001; CT-001/002; BR-RISK-001/005 |
| Exposure and population | Approve outstanding principal, open-loan eligibility and treatment of closed/zero-principal loans. | Accept the documented definitions. Open loans with zero principal remain in the count denominator; they contribute zero exposure. Do not invent a default classification. | BR-RISK-001/002; CT-002/004 |
| Arithmetic contract | Specify exact operands, finite serialized ratios, rounding and precision limits. | Preserve exact operands; use explicit rounded derived values and exact comparisons. Resolve REVIEW-001/002 before approving AC-RISK-001. | CT-004; BR-RISK-005 |
| Import validity | Approve the complete rejection/nonblocking catalog below. | No row filtering, imputation or silent deduplication. Invalid optional non-null values are still contract failures. Valid null segment is nonblocking. | FR-DQ-001/002; BR-DQ-001/002/003; CT-005 |
| Identity and replay | Define snapshot ID scope, bundle hashing and import-versus-analysis idempotency. | Prefer globally unique snapshot_id while retaining portfolio_id ownership. Specify this explicitly instead of assuming it from the ID format. | BR-DQ-001; CT-001/003/011 |
| Local platform | Approve SQLite, immutable artifacts, Streamlit and a single local writer. | Accept these for local single-user v1; put no formulas or durable state in UI callbacks. | OQ-009; ADR-003/004/008 |
| Operating envelope | Define input byte/row/field/numeric-length caps, maximum collected findings and local benchmark workload. | Set provisional safety limits through an explicit owner-reviewed configuration. Measure performance after implementation before setting release budgets. This review assigns no arbitrary numbers. | OQ-008; NFR-PERF-001; CT-001 conventions |
| Retention | Define what persists and what causes removal. | Retain local synthetic run artifacts until explicit operator cleanup; no automatic expiry in M02. No per-run delete UI is required by M02. Approval must record this choice and a supported cleanup boundary. | OQ-010; NFR-SEC-002; ADR-003 |
| Slice acceptance | Remove M03/M04 capabilities from the M02 acceptance gate. | M02 covers rejected/empty/succeeded/failed results and unavailable metric reasons, local lineage, restart readability and replay safety. No AI, graph checkpoint or human-review feature is required. | AC-UI-001; FR-OBS-001; roadmap M02 |

These choices are not all new architecture questions. Several can be closed by accepting explicit proposed conventions. Currency and operating caps cannot be closed from the repository evidence alone. GOV-001 also requires a reviewed commit and human acceptance record before implementation.

### Proposed validation disposition catalog

| Condition | Disposition | Why and evidence behavior |
|---|---|---|
| Invalid/unreadable UTF-8 CSV or JSON, malformed records, duplicate/missing/extra headers, unsupported schema, duplicate JSON keys | Reject entire import. | Input cannot be interpreted unambiguously. Record a file-level validation report. Duplicate JSON key behavior is currently missing and must be specified. |
| synthetic is false, missing manifest/provenance, hash mismatch, invalid currency, portfolio currency change | Reject input; label integrity conflicts separately when identity is reused. | Violates input contract or portfolio invariants. Do not produce metrics. |
| Missing/null core field, invalid ID/date/amount/integer/status, negative principal/DPD, original principal zero, outstanding greater than original, origination after as_of | Reject complete snapshot. | Violates CT-001/002 or the approved core invariant. Identify rule, record and field where available. |
| Closed loan with nonzero principal or nonzero DPD | Reject complete snapshot under the proposed product convention. | This convention is appropriate for the restricted synthetic product; it is not a universal banking invariant. Written-off/capitalizing products are excluded. |
| Duplicate loan_id within a snapshot | Reject complete snapshot. | Never select a first/last record or aggregate duplicates. |
| Invalid optional non-null segment | Reject complete snapshot. | Nullable does not permit an arbitrary malformed value. Prefer explicit null to coercion. |
| Reused idempotency key or snapshot identity with changed content | Return conflict and preserve original data. | This is an operation/identity conflict, not a successful import or a new population for calculation. |
| Input exceeds approved resource limit | Reject operation with explicit limit code. | No truncated input and no partial metrics. Finding collection may be bounded only if the report says it is incomplete. |
| Null segment | Accept unchanged population; display an unspecified category. | Recommend a nonblocking informational completeness finding. Add its rule/code explicitly before implementing that finding. Current CT-005 does not define it. |
| Header-only valid CSV | Accept empty snapshot. | Count and exposure are zero; ratio availability follows each denominator. Empty is a population property, not a run status. |
| Zero exposure or no eligible open loans | Accept valid input; unavailable ratios only where denominators are zero. | These are metric availability states, not validation errors. |
| Open loan with zero principal and positive DPD | Accept under the existing contract; optionally report a reviewed consistency warning. | Count/exposure rates can legitimately differ under the restricted reporting convention. A warning must not invent an invalidity rule. Owner may instead change the invariant explicitly. |
| Valid but high DPD, concentrated exposure or configured anomaly | Accept input; emit an analytical finding when its detector is enabled. | A risk signal is not a contract defect. Thresholds remain a later reviewed configuration. |
| Missing/incompatible prior snapshot | Keep current snapshot valid; mark comparison unavailable. | Temporal limitations cannot invalidate current metrics. |
| Missing/conflicting policy or failed model | Keep valid deterministic results; use later-stage indeterminate/partial behavior. | P-010; no input filtering or invented policy. |

No rejection-causing rule is downgraded implicitly by this catalog. Nonblocking findings require explicit codes, severity and rules in the proposed correction. If the owner prefers no completeness findings for valid nulls, retain the existing behavior and document it; do not pretend CT-005 already supports the proposed informational finding.

## 2. Decisions safely deferred to M03 or later

| Decision | Gate | Safe deferral boundary |
|---|---|---|
| Default semantics | Post-v1 feature proposal. | Remove Default from current v1 release criteria and metric schema. Preserve the undefined concept in the glossary/backlog. No threshold is supplied. |
| DTI and credit-score semantics | Future scope CR. | Already excluded. Do not require income/debt/score definitions to accept the current scope. |
| Concentration alert/anomaly thresholds | M03 detector readiness. | Raw group exposures/shares are deterministic M02 metrics; producing alerts requires approved threshold/operator configuration. |
| Temporal comparison | M03 readiness. | Approve changing-portfolio versus matched-cohort semantics, rate kind, previous-snapshot selection and composition evidence before implementing comparisons. No history means unavailable. |
| Policy authority, rule catalog and applicability | M03 policy readiness. | Source precedence for credit policies is distinct from project-document precedence. No automatic policy-conflict resolution. |
| Embedding/vector store/chunking/top_k | M03 retrieval selection ADR. | Accept the decision to defer, with a versioned benchmark and subsequent adapter decision. |
| Runtime models, prompts and AI usefulness thresholds | M03 AI readiness. | No M02 model dependency. Live-provider evals require separate budgets. |
| Graph checkpoint adapter and resume details | M03 graph readiness. | M02 still needs durable local run records and idempotent import; it does not need a LangGraph checkpoint. |
| Reviewer identity and durable business-action review | M04, if M03 actions are restricted as recommended. | M03 may produce grounded observations and inspect-evidence suggestions only. Any high-impact recommendation moves the review gate forward and blocks that feature until review works. |
| Incremental run deletion, copilot-history expiry and checkpoint retention | Before those operations are exposed. | Minimal M02 retention/cleanup still requires an explicit decision. No automatic deletion is assumed. |
| Measured latency/memory percentiles and AI cost budgets | Relevant milestone release. | Input safety caps precede parser implementation; empirically calibrated performance targets follow measured working behavior. |

Premature for current v1: distributed queues/services, PostgreSQL deployment, tenancy/SSO, real-data retention schedules, production SLAs, proprietary credit scoring, OCR, hosted vector infrastructure and provider-specific model selection for M02. Existing scope already excludes most of these; preserve that exclusion rather than adding ADRs for hypothetical systems.

## 3. Proposed ADRs recommended for acceptance

Acceptance here means a recommended human decision, not an executed status change or a claim that an adapter works.

| ADR | Recommendation and required wording |
|---|---|
| ADR-002 | Accept boundary validation with Pydantic and standard Python domain values. Contract corrections still precede implementation. Explicit parsing must respect CSV/string representations. |
| ADR-003 | Accept SQLite metadata and immutable local artifacts for single-user v1. Add the M02 artifact publication/recovery and minimal retention decisions; defer graph checkpointer integration. |
| ADR-004 | Accept Streamlit as the selected local v1 presentation adapter. Replace ambiguous candidate wording after approval; require callback idempotency and domain isolation, not enterprise readiness. |
| ADR-005 | Accept deferral of embedding/vector-store selection. This selects no vendor and closes no retrieval implementation gate. |
| ADR-006 | Accept small application-owned AI/retrieval ports, introduced when used. No universal factory and no M02 provider dependency. |
| ADR-007 | Accept structured local lineage/events, with AI usage fields applicable only when AI is used. Minimal event contract must be completed before M02 implementation. |
| ADR-008 | Accept modular src layout and dependency direction. Domain independence does not depend on the current empty-directory import check. |
| ADR-009 | Accept current uv/Ruff/mypy/pytest/pre-commit/CI direction. Tooling tests are repository checks; remote CI execution remains unverified. |

These eight decisions are technically justified for the stated scope. Approval should record them individually, rather than marking the ADR registry Accepted and inferring acceptance of every row.

## 4. ADRs that should remain Proposed

**ADR-001** remains Proposed until REVIEW-007/008/009 below are resolved and the M03 review boundary is consistent. LangGraph is a reasonable candidate for bounded later orchestration, but the exact checkpoint/result-commit semantics and terminal-state rules are not yet coherent enough to approve as a contract. Resolve those in an M03 design review, without making them a dependency of M02.

A future retrieval selection needs a new ADR following accepted ADR-005. It should not rewrite the accepted deferral to look as though a database was selected earlier. No additional distributed-architecture ADR is warranted now.

## 5. Open questions that can be closed

None was actually closed by this review. The following are candidates for closure through explicit owner approval and specification updates:

- **OQ-001**: close once the currency code, exposure/population conventions and validation catalog are approved. Most semantics already have a coherent proposal; actual currency is still unanswered.
- **OQ-002**: close the current-v1 scope question by deferring Default beyond v1. Its financial definition remains unresolved in the deferred backlog; do not label it financially resolved.
- **OQ-003**: close as excluded from current v1. Archive DTI/score extension questions until a feature is proposed. Do not assign definitions to removed fields.
- **OQ-009**: close its M02 platform portion upon accepting ADR-003/004. Move the graph/review portion to the M03 design gate and OQ-012 rather than implying all resume questions are answered.
- **OQ-010**: close its M02 portion if the owner approves explicit local retention until cleanup and the cleanup contract. Later lifecycle questions remain open against their features.

The existing register has a blanket statement that all questions are OPEN. Replace it with per-row disposition, owner, resolution reference and blocking milestone when approvals occur. Do not delete unresolved questions or reuse their IDs.

## 6. Open questions that must remain open

| ID | Disposition now | Required remaining decision |
|---|---|---|
| OQ-001 | OPEN for M02 until approval. | Actual currency and complete rejection/nonblocking conventions. |
| OQ-002 | Proposed post-v1 deferral. | No definition needed for present v1 after scope correction; definition stays unresolved. |
| OQ-003 | Proposed removal from active baseline questions. | No current-v1 decision; extension only through CR. |
| OQ-004 | OPEN for M03 detectors. | Synthetic threshold/operator catalog and field-bound semantics; not needed for raw concentration shares. |
| OQ-005 | OPEN for M03 comparison. | Count versus exposure rate, cohort method, explicit prior selection and changing-attribute handling. |
| OQ-006 | OPEN for M03 policies. | Scope vocabulary, authority/validity/precedence, curated predicates and conflict disposition. |
| OQ-007 | OPEN for M03 retrieval. | Corpus benchmark, embedding/index selection and sufficiency parameters. |
| OQ-008 | Split by gate; M02 portion OPEN. | Input safety caps/workload now; measured performance targets later; AI budgets only before AI. |
| OQ-009 | M02 closure candidate; later portion OPEN. | Human platform approval; graph/checkpoint decision later. |
| OQ-010 | M02 closure candidate; later portion OPEN. | Owner-approved retention/cleanup now; targeted deletion and additional artifact classes later. |
| OQ-011 | OPEN for M03 AI. | Model/prompt/eval corpus and repeated-run/usefulness thresholds. |
| OQ-012 | OPEN for M04 under recommended M03 restriction. | Local human identity/action evidence and multi-recommendation review semantics. Moves earlier if high-impact output moves earlier. |

## 7. Contradictions and required specification modifications

### M02 acceptance repairs

| Finding | Evidence and counterexample | Required correction |
|---|---|---|
| REVIEW-001 | BR-RISK-005 preserves exact operands and rounds display, while CT-004 Ratio and CT-014 rate_difference provide finite decimal strings without computational precision. A rate of 1/3 has no exact finite decimal representation. | Define the authority as exact numerator/denominator, a precisely quantized serialized derived value and exact threshold comparison. Monetary sums must also avoid implicit Decimal-context rounding for long coefficients. CT-014 inherits the same explicit arithmetic policy later. |
| REVIEW-002 | AC-RISK-001 says zero-exposure populations produce null ratios. Under BR-RISK-002, two open zero-principal loans, one with DPD > 0, have count rate 1/2 and unavailable exposure rate. | Make availability denominator-specific. Add this counterexample, repeating-decimal and rounding-boundary cases to AC-RISK-001 and the planned tests. No business threshold is invented. |
| REVIEW-003 | FR-RISK-001 references BR-RISK-001/002/005 but not concentration BR-RISK-003, while CT-004 includes concentration. FR-RISK-002 couples concentration with threshold detectors at M03. | Specify raw group exposure/share calculation in FR-RISK-001 at M02 and alert generation in FR-RISK-002 at M03. Owner may choose to move raw shares later, but must remove them from the M02 required payload in that alternative. Recommended direction is raw shares in M02. |
| REVIEW-004 | FR-UI-001 targets M02 but AC-UI-001 requires partial and pending_review fixtures. Empty is listed alongside run statuses even though the lifecycle has no empty status. FR-OBS-001 also includes model fields at M02. | Scope AC-UI-001 by milestone: empty is a snapshot property; pending_review is later. M02 requires deterministic state/availability rendering only. Scope FR-OBS-001/NFR verification to applicable stages and leave unused AI provenance absent. |
| REVIEW-005 | BR-DQ-001 defines snapshot identity as portfolio_id plus snapshot_id. CT-003/004/011 locate snapshots by snapshot_id without portfolio_id. Two portfolios could both import snapshot_id = S1. | Specify globally unique snapshot_id with portfolio ownership, or propagate composite identity everywhere. Recommend the first, pending explicit owner approval. Define immutable core loan-identity checks before temporal analysis later. |
| REVIEW-006 | All boundary failures are described as DQ/rejection, but CT-005 has no integrity/resource/idempotency codes or nonblocking completeness code. Rejected malformed manifests may have no valid user-supplied identity. NFR-PERF-001 requires empirically measured budgets before feature readiness. | Define a validation/import result with disposition, typed findings, completeness flag and application-assigned import/run identity. Separate conflicts/resource failures from invalid loan data. Set safety caps before implementation and calibrate measured performance budgets before milestone release. |

### Later-stage consistency repairs, with explicit deferral gates

| Finding | Evidence | Required correction and gate |
|---|---|---|
| REVIEW-007 | FR-AI-001 produces recommendations at M03; BR-POL-004/CT-008 require high-impact review. FR-AI-003/FR-UI-002 and OQ-012 are at M04, while the M03 graph can enter human_review. | Recommend M03 observations and inspection suggestions only, with no high-impact recommendation generation. Scope the graph's human-review branch to M04 until review is implemented. Alternative: move the review slice and OQ-012 into M03. Resolve milestone boundary before baseline acceptance; implementation details can remain deferred. |
| REVIEW-008 | architecture.md already specifies result-before-checkpoint recovery and the dependency direction is correct. The remaining gap is the adapter contract that enforces artifact publication, RunStore result commit and graph checkpoint advancement across separate stores. The universal atomic-patch wording does not define that coordination transaction. | This is a recovery-contract gap, not proof of domain coupling. Separate pure calculation from application result commit and graph checkpoint advancement. Specify reconciliation for each interruption boundary before accepting ADR-001 or implementing FR-OBS-002. Do not claim cross-store atomicity. |
| REVIEW-009 | domain-model.md defines failed as no usable deterministic result or failed durable finalization. review_gate routes an invariant failure to failed even with committed valid metrics, whereas FR-AI-001 preserves them as partial. CT-011 lacks provisional_quality despite the lifecycle and GraphState requiring it. | Create one run-outcome decision table and persist completeness/review state separately. Specify which faults are fatal after metrics exist; add provisional quality or a named equivalent to the contract. M02 needs core status semantics; review-specific details may wait until M03/M04. |
| REVIEW-010 | BR-POL-002 requires review for unresolved policy conflicts. CT-012 only reviews recommendation_id; graph review_gate only checks high-impact recommendations. No recommendation is necessary for a policy conflict. | Before M03 policy readiness, either require corpus-curation resolution outside the run and leave outcome indeterminate, or define a typed policy-conflict review target. Recommend the former for local v1 simplicity. Never treat recommendation approval as policy precedence approval. |
| REVIEW-011 | Every finding envelope requires rule_id/rule_version. CT-007 permits no_policy with policy_rule_id null, but does not identify the applicable system-level rule for that result. CT-010 may classify conflict without a specified complete candidate/rule discovery method. | Distinguish system evidence-availability rules from policy predicate IDs. Define per-rule assessment coverage; retrieved relevance must not imply portfolio-wide policy compliance. Gate: OQ-006/007 and FR-POL-002. |
| REVIEW-012 | FR-RISK-003 and CT-014 do not name whether current/prior rate is count or exposure rate. BR-RISK-004 requires only a comparable earlier snapshot, leaving prior selection, duplicate dates and reassignments unresolved. | Require an explicit rate kind and prior snapshot ref; report comparison rule/version and both immutable input hashes. Describe entered/exited population and borrower/segment changes under the chosen cohort policy. Gate: OQ-005. |
| REVIEW-013 | Tool shared text says call events are the only side effect, while TOOL-003 persists retrieval results. CT-013 has no exchange identifier, persisted history entries or artifact references for these records. | Say analytical results are read-only while an exchange audit may append calls/retrieval evidence. Define the exchange/history/evidence ownership contract before FR-AI-002. |
| REVIEW-014 | CT-009 curates rules against chunk IDs, while RAG chunker/index changes can alter those IDs without changing policy text. Applicability scope and the definition of sufficient evidence remain abstract. | Prefer policy-version/source-span anchoring with derived chunk mappings, or require explicit rule re-curation after chunk changes. Resolve scope vocabulary and sufficiency at OQ-006/007; defer vector-store selection. |

### Scope and readiness corrections

| Finding | Evidence | Required correction |
|---|---|---|
| REVIEW-015 | OQ-002 and the original review report retain Default as an M05 blocker; CT-004 always requires default_rate; BR-RISK-006 retains a definition_pending branch. | Defer Default beyond v1. Update scope, glossary, roadmap, FR-RISK-001, AC-RISK-001, BR-RISK-006, CT-004, open questions and traceability together. Remove the mandatory metric stub instead of manufacturing a definition. Preserve historical proposal context in CHANGELOG/CR. |
| REVIEW-016 | GOV-002 requires resolved feature questions, but current NFRs/traceability mix early and late verification, and every question is blanket OPEN. Approving a multi-stage document could implicitly approve unresolved later contract semantics. | Introduce explicit applicability/milestone and per-ID approval status. Separate approved invariants from Proposed detailed graph/AI contracts. An Accepted baseline can contain referenced Proposed future specs only if GOV-001 records that exclusion exactly. |

No change to P-001 through P-021 is needed. Their deterministic authority, evidence, domain isolation and explicit-change requirements support these repairs. Project-document precedence cannot resolve the conflicts by making lower-level contracts silently change; every affected artifact still requires correction.

### Exact requirement IDs requiring modification

Before baseline acceptance: FR-DQ-001/002, FR-RISK-001/002, FR-AI-001/003, FR-UI-001/002, FR-OBS-001, NFR-PERF-001 and NFR-SEC-002; AC-DQ-001/002, AC-RISK-001/002, AC-AI-001/003, AC-UI-001/002 and AC-OBS-001. Changes limit M02 to applicable deterministic behavior, distinguish raw shares from alerts, record Default deferral, establish nonblocking DQ semantics, and resolve the M03/M04 recommendation boundary.

Before their later Definition of Ready: FR-RISK-003, FR-POL-001/002, FR-AI-002, FR-OBS-002; NFR-REL-001, NFR-AI-001/002; AC-RISK-003, AC-POL-001/002, AC-AI-002 and AC-OBS-002. The safety principles may be approved now, but these detailed later feature contracts remain Proposed until their questions are answered.

## 8. Unnecessary complexity to remove

- Remove the always-present default_rate field and current-v1 default definition gate. Preserve a post-v1 scope question without an implementation stub.
- Remove DTI/credit-score definition work from the active acceptance checklist because those features are already excluded.
- Do not require M02 to implement graph state, checkpoints, model usage, policy curation or pending review merely to satisfy generic test names.
- Separate raw concentration shares from alerts so a threshold cannot block deterministic group aggregation.
- Avoid a general human-review framework for policy conflicts in local v1; prefer reviewed corpus changes plus explicit indeterminate results unless an actual review feature is approved.
- Avoid automatic retention schedules or a per-artifact deletion service before such operations exist. Define minimal local retention/cleanup first.
- Preserve the small ports only when used. Do not add a generic repository/provider framework, agent supervisor or service deployment.
- Do not add further layers to the existing documentation hierarchy. A correction CR and acceptance manifest are sufficient.

## 9. Missing requirements or contracts

### Needed before M02 readiness
1. **Import/validation result**: application-assigned identity, input hash when readable, accepted/rejected/conflict/limit disposition, optional validated snapshot ref, finding list, report completeness and parse-error location. CT-005 alone cannot describe the overall validation outcome or safely represent an invalid manifest identity.
2. **Analysis request and configuration**: exact selected stages, import-versus-analysis idempotency keys, immutable configuration identity and compatibility rules. CT-011 lists requested_stages but defines neither an allowed stage enum nor legal M02 request combinations. This is necessary to make later optional stages genuinely optional.
3. **Arithmetic serialization and canonical hashing**: precision/rounding of derived values, exact operands, deterministic threshold comparison, canonical date/decimal/null encoding, bundle framing, and excluded run-specific IDs/timestamps. Identical metric payloads otherwise include different metrics_id/run_id fields. BR-RISK-005 and NFR-REL-002 need an exact semantic comparison target.
4. **Local artifact publication and recovery**: temporary versus published artifacts, order of file/metadata publication, integrity verification, orphan reconciliation and behavior after interrupted M02 imports. A checkpoint protocol alone cannot establish M02 persistence correctness.
5. **Typed event and validation catalogs**: event types, safe error codes, required/null fields and severity mapping. Observability lists field names but does not fully define their contract. Define only fields used by M02; AI-specific details can wait.
6. **Bounded parser configuration**: input/row/field/numeric limits and finding-report truncation behavior. Limits are operational safety settings, not invented credit thresholds.

### Needed before later readiness
7. **Temporal comparison configuration**: rate kind, prior ref/selection, cohort policy, composition invariants and definition of signed differences.
8. **Policy evaluation coverage/applicability**: scope registry, rule/source-span mapping, system indeterminate rule identity and distinction between per-rule compliance and portfolio coverage.
9. **Review aggregation**: target scope, persisted provisional quality, multiple recommendations, revision changes, and exact duplicate versus stale actions. CT-012 exists, but the aggregation contract does not.
10. **Copilot exchange audit/history**: exchange identity, bounded messages, call outcomes, retrieval artifact ownership and supported exchange lifecycle without mutating terminal runs.

Assign new requirement/contract IDs only when preparing the reviewed correction. This report does not create accepted requirements by naming missing behavior. Each added contract must have acceptance criteria, edge cases and traceability before implementation.

## 10. Final recommendation and approval manifest

**Current recommendation: DO NOT ACCEPT.** Resolve REVIEW-001 through REVIEW-006 and the milestone/scope boundary parts of REVIEW-007/015/016 first. Later graph, policy and copilot details can remain Proposed with explicit gates. Approve the remaining M02 currency, safety-cap, platform and retention choices. Then re-review the correction for **ACCEPT WITH EXPLICIT DEFERRALS** rather than requiring Default or AI to make the first slice usable.

### Exact prospective status changes after human approval

This is a conditional manifest for a corrected revision, not an instruction to change statuses now.

| File | Accepted scope after explicit approval |
|---|---|
| AGENTS.md | Governance instructions; product work still requires feature readiness. |
| docs/00-project/baseline.md | GOV-001 through GOV-004 and corrected accepted/deferred manifest. |
| docs/00-project/principles.md | P-001 through P-021 and precedence. |
| docs/00-project/writing-policy.md | STYLE-001 through STYLE-003. |
| docs/00-project/vision.md | Local synthetic analyst-support product vision. |
| docs/00-project/scope.md | Corrected current-v1 scope, including Default exclusion. |
| docs/00-project/glossary.md | Canonical terms with Default/DTI explicitly deferred, not financially resolved. |
| docs/00-project/roadmap.md | Corrected M02 deterministic boundary and M03/M04 review boundary. |
| docs/00-project/model-usage-policy.md | Role policy and updateable owner preference mapping; no runtime provider selection. |
| docs/03-architecture/architecture.md | Local modular dependency direction and corrected M02 persistence strategy; ADR-001 still explicitly Proposed. |
| docs/03-architecture/security.md | Local synthetic threat/control boundaries; future feature verification deferred by gate. |
| docs/03-architecture/observability.md | Corrected M02 lineage/event contract and stage applicability. |
| docs/05-testing/test-strategy.md | SDD verification strategy with milestone applicability; no test success implied. |
| docs/adr/ADR-002-validation.md | ADR-002. |
| docs/adr/ADR-003-persistence.md | ADR-003 after M02 publication/retention clarification. |
| docs/adr/ADR-004-ui.md | ADR-004 with selected-local-adapter wording. |
| docs/adr/ADR-005-retrieval.md | ADR-005, accepting deferral only. |
| docs/adr/ADR-006-providers.md | ADR-006. |
| docs/adr/ADR-007-observability.md | ADR-007. |
| docs/adr/ADR-008-repository.md | ADR-008. |
| docs/adr/ADR-009-tooling.md | ADR-009. |
| docs/changes/README.md | Change process. |
| docs/changes/CR-001-baseline-acceptance-corrections.md | Proposed correction only once its exact revised behavior is explicitly approved; completion checklist remains evidence-dependent. |

Keep headers of mixed-stage documents Proposed unless every contained rule is actually accepted. After adding per-ID approval fields, the following exact subsets may become Accepted while the future subsets remain Proposed:

- `docs/01-requirements/functional-requirements.md`: corrected FR-DQ-001/002, FR-RISK-001, FR-UI-001 and FR-OBS-001.
- `docs/01-requirements/non-functional-requirements.md`: M02 clauses of NFR-REL-002, NFR-SEC-001, NFR-PERF-001, NFR-OBS-001, NFR-MNT-001 and NFR-SEC-002. Add applicability explicitly; do not approve unresolved numeric budgets as values.
- `docs/01-requirements/acceptance-criteria.md`: corrected AC-DQ-001/002, AC-RISK-001, AC-UI-001 and AC-OBS-001.
- `docs/02-domain/business-rules.md`: corrected BR-DQ-001/002/003 and BR-RISK-001/002/003/005. BR-RISK-003 acceptance covers raw shares only; alert configuration stays deferred. BR-RISK-006 becomes an explicit deferral record, not an implemented rule.
- `docs/02-domain/data-contracts.md`: corrected CT-001/002/004/005; M02 variants of CT-003/011; newly reviewed M02 request/configuration/import/event contracts after IDs are assigned. CT-006 through CT-010 and CT-012 through CT-014 detailed schemas remain Proposed.
- `docs/02-domain/domain-model.md`: M02 entity/invariant/lifecycle portions; later policy/insight/review relationships remain Proposed where REVIEW-007/009/010 are unresolved.

The acceptance record must also list these retained Proposed files: `docs/adr/ADR-001-langgraph.md`, `docs/03-architecture/graph-spec.md`, `docs/03-architecture/rag-spec.md`, all five `docs/04-ai/` specifications, and remaining future requirement/contract sections. `docs/05-testing/traceability.md`, `docs/00-project/open-questions.md` and `docs/adr/README.md` are tracking registries: update individual rows and references; do not imply blanket approval by their header alone. Templates remain Draft. This review is a Proposed review artifact, not the acceptance act.

GOV-001 requires reviewer, date, reviewed commit, exact accepted IDs/versions, exclusions and deferred gates. Commit the reviewed proposed revision before creating its approval record so that the record can point to an immutable review target. This review does not create that commit.

## Verification and limitations
Executed on 2026-10-14 with Python 3.12.13:

| Check | Result |
|---|---|
| uv sync --locked --group dev | Passed; existing locked environment verified. |
| uv run --locked ruff check . | Passed. |
| uv run --locked ruff format --check . | Passed. |
| uv run --locked mypy src scripts | Passed; 3 source files. |
| uv run --locked pytest | Passed; 5 repository governance tests. |
| uv run --locked python scripts/check_baseline.py | Passed; 58 Markdown documents with metadata/style, local links, requirement mappings, known IDs and import checks. |

These checks do not detect the semantic findings in this review. They verify artifact consistency, not proposed financial, retrieval, review or UI behavior. No product implementation or live-provider evaluation was performed. GitHub Actions was not run remotely. Product source, tooling code, dependencies and existing acceptance statuses were unchanged. The original 2026-10-07 file inventory remains a historical snapshot of initial baseline creation; this review adds two documents and navigation/changelog updates.

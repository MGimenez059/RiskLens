"""The persistence and ingress boundary used by deterministic analysis."""

from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Literal, Protocol

from risklens.application.contracts import (
    DTO,
    AnalysisRequest,
    Count,
    Diagnostic,
    Event,
    EvidenceRef,
    Hash,
    Id,
    Manifest,
    ParserLimits,
    Result,
    RunManifest,
    Stage,
    canonical,
)
from risklens.domain.metrics import Loan, usd

ArtifactKind = Literal[
    "input_bundle", "validated_snapshot", "validation_report", "metrics", "event_batch"
]
ARTIFACT_STAGES: dict[ArtifactKind, Stage] = {
    "input_bundle": "load_portfolio",
    "validated_snapshot": "validate_portfolio",
    "validation_report": "validate_portfolio",
    "metrics": "calculate_metrics",
    "event_batch": "finalize",
}
InputIssue = Literal["resource_limit", "unreadable_input"]


@dataclass(slots=True)
class Scan:
    manifest: Manifest | None
    candidate_id: str | None
    loans: list[Loan]
    findings: list[Diagnostic]
    complete: bool = True
    limit: str | None = None

    def snapshot_payload(self) -> bytes:
        assert self.manifest is not None and not self.findings and self.limit is None
        return canonical(
            {
                **self.manifest.model_dump(exclude={"source_sha256"}),
                "loans": [
                    {
                        "loan_id": loan.loan_id,
                        "customer_id": loan.customer_id,
                        "original_principal": usd(loan.original_cents),
                        "outstanding_principal": usd(loan.outstanding_cents),
                        "days_past_due": loan.days_past_due,
                        "loan_status": loan.loan_status,
                        "origination_date": loan.origination_date.isoformat(),
                        "segment": loan.segment,
                    }
                    for loan in sorted(self.loans, key=lambda loan: loan.loan_id)
                ],
            }
        )


@dataclass(frozen=True, slots=True)
class Bundle:
    ref: str
    manifest: bytes | None
    csv: bytes | None
    issue: InputIssue | None

    @property
    def input_hash(self) -> str | None:
        return self.ref if self.issue is None else None


class SnapshotIdentity(DTO):
    snapshot_id: Id
    portfolio_id: Id


class RunOutputIdentity(DTO):
    run_id: Id
    stage: Stage
    config_hash: Hash


class CommittedPublication(DTO):
    publication_id: Id
    run_id: Id
    artifact_hash: Hash
    artifact_kind: ArtifactKind
    byte_length: Count
    publication_state: Literal["committed"]
    expected_run_revision: Count
    semantic_identity: SnapshotIdentity | RunOutputIdentity


@dataclass(frozen=True, slots=True)
class Artifact:
    kind: ArtifactKind
    sha256: str
    publication: CommittedPublication | None = None


@dataclass(frozen=True, slots=True)
class ResolvedEvidence:
    reference: EvidenceRef
    artifact: bytes


@dataclass(frozen=True, slots=True)
class SnapshotBinding:
    snapshot_id: str
    portfolio_id: str
    bundle_hash: str
    artifact_hash: str


@dataclass(frozen=True, slots=True)
class ImportBinding:
    key: str
    parser_hash: str
    bundle_hash: str
    import_id: str
    report_hash: str


@dataclass(frozen=True, slots=True)
class StoredRun:
    request: AnalysisRequest
    result: Result
    fingerprint: str | None


class State(Protocol):
    def writer(self) -> AbstractContextManager[object]: ...
    def code_revision(self) -> str: ...
    def register(self, manifest: bytes | None, csv: bytes | None, limits: ParserLimits) -> str: ...
    def bundle(self, ref: str, limits: ParserLimits) -> Bundle: ...
    def scan(self, bundle: Bundle, limits: ParserLimits) -> Scan: ...
    def publish(self, data: bytes) -> str: ...
    def read(self, digest: str) -> bytes: ...
    def snapshot(self, snapshot_id: str) -> SnapshotBinding | None: ...
    def import_binding(self, key: str) -> ImportBinding | None: ...
    def analysis_binding(self, key: str) -> StoredRun | None: ...
    def stored_run(self, run_id: str) -> StoredRun: ...
    def list_runs(self) -> list[RunManifest]: ...
    def events(self, run_id: str) -> list[Event]: ...
    def artifact_refs(self, run_id: str) -> dict[str, Artifact]: ...
    def append_event(self, event: Event) -> None: ...
    def start(
        self,
        request: AnalysisRequest,
        result: Result,
        fingerprint: str | None,
        event: Event | None,
        previous_revision: int | None,
    ) -> None: ...
    def finish(
        self,
        result: Result,
        previous_revision: int,
        artifacts: dict[str, Artifact],
        snapshot: SnapshotBinding | None,
        binding: ImportBinding | None,
        events: list[Event],
    ) -> None: ...

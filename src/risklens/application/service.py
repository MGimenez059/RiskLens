"""Run deterministic analysis, commit its lineage, and verify persisted projections."""

from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter_ns
from typing import Literal, cast
from uuid import uuid4

from pydantic import TypeAdapter, ValidationError

from risklens.application.contracts import (
    DTO,
    SAFE_MESSAGES,
    STAGES,
    AnalysisConfiguration,
    AnalysisRequest,
    DataQualityFinding,
    Diagnostic,
    Event,
    EventType,
    EvidenceRef,
    ImportResult,
    LoanRow,
    Manifest,
    MetricLocator,
    Metrics,
    OperationCode,
    OperationError,
    Report,
    ReportLocator,
    Result,
    RunError,
    RunManifest,
    SnapshotLocator,
    SourceRowLocator,
    Stage,
    StageOutcome,
    canonical,
    sha256,
)
from risklens.application.ports import (
    ARTIFACT_STAGES,
    Artifact,
    ArtifactKind,
    Bundle,
    ImportBinding,
    ResolvedEvidence,
    RunOutputIdentity,
    SnapshotBinding,
    SnapshotIdentity,
    State,
    StoredRun,
)
from risklens.application.snapshot import SnapshotPayload
from risklens.domain.metrics import Loan, calculate

TERMINAL = {"succeeded", "rejected", "conflict", "limit_failed", "failed"}
EVIDENCE_ARTIFACT_KIND: dict[str, ArtifactKind] = {
    "snapshot": "validated_snapshot",
    "source_row": "input_bundle",
    "metric": "metrics",
    "validation_report": "validation_report",
}
METRIC_KEYS = {
    "loan_count",
    "open_loan_count",
    "total_exposure",
    "delinquency_count_rate",
    "delinquency_exposure_rate",
    "concentration",
}
EVENT_BATCH = TypeAdapter(list[Event])
OPERATIONS: dict[str, OperationCode | None] = {
    "valid": None,
    "rejected": "input_invalid",
    "limit_failed": "resource_limit",
    "conflict": "identity_conflict",
}


def _id() -> str:
    return uuid4().hex


def _utc() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _ms(started: int) -> int:
    return (perf_counter_ns() - started) // 1_000_000


def _json(model: DTO) -> bytes:
    return canonical(model.model_dump(mode="json"))


@dataclass(slots=True)
class Validation:
    report: Report
    snapshot: SnapshotBinding | None = None
    snapshot_bytes: bytes | None = None
    loans: list[Loan] | None = None
    as_of: str | None = None
    previous_import: ImportBinding | None = None


class AnalysisService:
    def __init__(self, state: State, configuration: AnalysisConfiguration | None = None) -> None:
        self.state = state
        self.configuration = configuration or AnalysisConfiguration()
        self.code_revision = state.code_revision()

    def register_bundle(self, manifest: bytes | None, csv: bytes | None) -> str:
        return self.state.register(manifest, csv, self.configuration.parser_limits)

    def list_runs(self) -> list[RunManifest]:
        return self.state.list_runs()

    def get_run(self, run_id: str) -> Result:
        with self.state.writer():
            record = self.state.stored_run(run_id)
            refs = self.state.artifact_refs(run_id)
            try:
                metrics = self._verified_metrics(record, refs)
            except ValueError as error:
                raise OperationError("integrity_error") from error
            return record.result.model_copy(update={"metrics": metrics})

    def _verified_metrics(self, record: StoredRun, refs: dict[str, Artifact]) -> Metrics | None:
        result = record.result
        run = result.run
        if set(refs) != set(run.output_artifact_ids):
            raise OperationError("integrity_error")
        validation = result.validation
        if validation is None:
            if refs or result.evidence:
                raise OperationError("integrity_error")
            if run.status not in TERMINAL and run.input_hash:
                self.state.bundle(record.request.bundle_ref, result.configuration.parser_limits)
            return None

        expected = {"validation_report", "event_batch"}
        if run.input_hash:
            expected.add("input_bundle")
        if run.status == "succeeded":
            expected.update({"validated_snapshot", "metrics"})
        by_kind = {ref.kind: (key, ref.sha256) for key, ref in refs.items()}
        if set(by_kind) != expected or len(refs) != len(by_kind):
            raise OperationError("integrity_error")
        for artifact in refs.values():
            publication = artifact.publication
            if publication is None:
                # The original M02 layout stored verified artifact references directly.
                continue
            identity = publication.semantic_identity
            if publication.expected_run_revision + 1 != run.revision:
                raise OperationError("integrity_error")
            if artifact.kind == "validated_snapshot":
                if not isinstance(identity, SnapshotIdentity) or (
                    identity.snapshot_id,
                    identity.portfolio_id,
                ) != (run.snapshot_id, validation.portfolio_id):
                    raise OperationError("integrity_error")
            elif not isinstance(identity, RunOutputIdentity) or (
                identity.run_id,
                identity.stage,
                identity.config_hash,
            ) != (run.run_id, ARTIFACT_STAGES[artifact.kind], run.config_hash):
                raise OperationError("integrity_error")
        report_id, report_hash = by_kind["validation_report"]
        report = Report.model_validate_json(self.state.read(report_hash))
        if (
            report_id != validation.validation_report_id
            or report_hash != validation.report_hash
            or (
                report.report_id,
                report.input_hash,
                report.snapshot_id,
                report.disposition,
                report.report_complete,
                report.error_code,
            )
            != (
                report_id,
                run.input_hash,
                run.snapshot_id,
                validation.disposition,
                validation.report_complete,
                validation.findings[0].code if validation.findings else validation.error_code,
            )
            or [
                (item.code, item.scope, item.row_number, item.field, item.message)
                for item in report.findings
            ]
            != [
                (item.code, item.scope, item.row_number, item.field, item.summary)
                for item in validation.findings
            ]
        ):
            raise OperationError("integrity_error")

        bundle = None
        if run.input_hash:
            bundle = self.state.bundle(
                record.request.bundle_ref, result.configuration.parser_limits
            )
            if (
                by_kind["input_bundle"][1] != run.input_hash
                or bundle.input_hash != run.input_hash
                or bundle.csv is None
                or sha256(bundle.csv) != validation.source_sha256
            ):
                raise OperationError("integrity_error")
        events = EVENT_BATCH.validate_json(self.state.read(by_kind["event_batch"][1]))
        artifact_hashes = {ref.sha256 for ref in refs.values()}
        if (
            not events
            or events[-1].event_type != "publication_committed"
            or (events[-1].revision, events[-1].outcome, events[-1].code)
            != (
                run.revision,
                run.status,
                validation.error_code,
            )
            or any(
                event.run_id != run.run_id
                or event.input_hash != run.input_hash
                or event.revision > run.revision
                or (
                    event.output_artifact_hash is not None
                    and event.output_artifact_hash not in artifact_hashes
                )
                for event in events
            )
        ):
            raise OperationError("integrity_error")

        metrics = None
        if run.status == "succeeded":
            assert (
                run.snapshot_id is not None and bundle is not None and bundle.manifest is not None
            )
            snapshot = self.state.snapshot(run.snapshot_id)
            snapshot_hash = by_kind["validated_snapshot"][1]
            if snapshot is None or (
                snapshot.portfolio_id,
                snapshot.bundle_hash,
                snapshot.artifact_hash,
            ) != (validation.portfolio_id, run.input_hash, run.canonical_input_hash):
                raise OperationError("integrity_error")
            if snapshot_hash != snapshot.artifact_hash:
                raise OperationError("integrity_error")
            self.state.read(snapshot_hash)
            metrics_id, metrics_hash = by_kind["metrics"]
            metrics = Metrics.model_validate_json(self.state.read(metrics_hash))
            result.verify_metrics(metrics)
            manifest = Manifest.model_validate_json(bundle.manifest)
            if (
                metrics.metrics_id != metrics_id
                or (manifest.snapshot_id, manifest.portfolio_id, manifest.source_sha256)
                != (
                    run.snapshot_id,
                    validation.portfolio_id,
                    validation.source_sha256,
                )
                or (metrics.as_of, metrics.currency) != (manifest.as_of, manifest.currency)
            ):
                raise OperationError("integrity_error")
        self._verify_evidence(result, by_kind, metrics)
        return metrics

    @staticmethod
    def _verify_evidence(
        result: Result,
        by_kind: dict[ArtifactKind, tuple[str, str]],
        metrics: Metrics | None,
    ) -> None:
        for ref in result.evidence:
            artifact = by_kind.get(EVIDENCE_ARTIFACT_KIND[ref.kind])
            if artifact is None or artifact[1] != ref.artifact_hash:
                raise OperationError("integrity_error")
            locator = ref.locator
            if isinstance(locator, SnapshotLocator) and (
                locator.snapshot_id != result.run.snapshot_id
            ):
                raise OperationError("integrity_error")
            if isinstance(locator, SourceRowLocator) and (
                metrics is None
                or locator.row_number > metrics.loan_count + 1
                or (locator.field is not None and locator.field not in LoanRow.model_fields)
            ):
                raise OperationError("integrity_error")
            if isinstance(locator, MetricLocator) and (
                locator.metrics_id != artifact[0] or locator.metric_key not in METRIC_KEYS
            ):
                raise OperationError("integrity_error")
            if isinstance(locator, ReportLocator) and locator.report_id != artifact[0]:
                raise OperationError("integrity_error")

    def resolve_evidence(self, run_id: str, evidence_id: str) -> ResolvedEvidence | None:
        with self.state.writer():
            for ref in self.get_run(run_id).evidence:
                if ref.evidence_id == evidence_id:
                    return ResolvedEvidence(ref, self.state.read(ref.artifact_hash))
        return None

    def execute(self, request: AnalysisRequest) -> Result:
        try:
            request = AnalysisRequest.model_validate(request.model_dump())
        except ValidationError as error:
            raise OperationError("configuration_invalid") from error
        with self.state.writer():
            return self._execute(request)

    def resume(self, run_id: str) -> Result:
        with self.state.writer():
            record = self.state.stored_run(run_id)
            if record.result.run.status in TERMINAL:
                return self.get_run(run_id)
            return self._execute(record.request, record)

    def new_analysis(self, run_id: str, analysis_key: str) -> Result:
        with self.state.writer():
            source = self.state.stored_run(run_id)
            result = self.get_run(run_id)
            if result.run.status not in TERMINAL or result.run.input_hash is None:
                raise OperationError("configuration_invalid")
            request = source.request.model_copy(
                update={
                    "parent_run_id": run_id,
                    "analysis_idempotency_key": analysis_key,
                }
            )
            return self.execute(request)

    def _execute(self, request: AnalysisRequest, pending: StoredRun | None = None) -> Result:
        load_started = perf_counter_ns()
        config = request.configuration
        bundle = self.state.bundle(request.bundle_ref, config.parser_limits)
        fingerprint = request.fingerprint(bundle.input_hash) if bundle.input_hash else None
        bound = self.state.analysis_binding(request.analysis_idempotency_key)
        matches = bound is not None and fingerprint is not None and bound.fingerprint == fingerprint
        if bound and matches:
            if bound.result.run.status in TERMINAL:
                result = self.get_run(bound.result.run.run_id)
                outcome = "succeeded" if result.run.status == "succeeded" else result.run.status
                event_code = (
                    result.validation.error_code
                    if result.validation
                    else result.run.errors[0].code
                    if result.run.errors
                    else None
                )
                self.state.append_event(
                    self._event(
                        result.run,
                        "finalize",
                        "replay_returned",
                        _ms(load_started),
                        cast(
                            Literal["succeeded", "failed", "rejected", "conflict", "limit_failed"],
                            outcome,
                        ),
                        event_code,
                    )
                )
                return result
            pending = bound
            request = bound.request
        if request.parent_run_id and self.get_run(request.parent_run_id).run.status not in TERMINAL:
            raise OperationError("configuration_invalid")

        running = self._start(
            request,
            bundle,
            fingerprint if bound is None or matches else None,
            pending,
            _ms(load_started),
        )
        started = perf_counter_ns()
        artifacts: dict[str, Artifact] = {}
        if bundle.input_hash:
            artifacts[_id()] = Artifact("input_bundle", bundle.input_hash)
        try:
            validation = self._validate(request, bundle, bool(bound and not matches))
            validated_ms = _ms(started)
            return self._commit(request, bundle, running, validation, artifacts, validated_ms)
        except OperationError as error:
            return self._failed(running, error.code, _ms(started))
        except (ValueError, ArithmeticError) as error:
            if isinstance(error, ValidationError):
                return self._failed(running, "integrity_error", _ms(started))
            return self._failed(running, "internal_error", _ms(started))

    def _start(
        self,
        request: AnalysisRequest,
        bundle: Bundle,
        fingerprint: str | None,
        pending: StoredRun | None,
        load_ms: int,
    ) -> Result:
        previous = pending.result.run if pending else None
        attempt = previous.stage_outcomes[0].attempt_count + 1 if previous else 1
        run = RunManifest(
            run_id=previous.run_id if previous else _id(),
            parent_run_id=request.parent_run_id,
            import_id=previous.import_id if previous else _id(),
            snapshot_id=None,
            revision=previous.revision + 1 if previous else 1,
            status="running",
            created_at=previous.created_at if previous else _utc(),
            completed_at=None,
            input_hash=bundle.input_hash,
            canonical_input_hash=None,
            config_hash=request.configuration.config_hash,
            baseline_version="1.0",
            contract_version=request.configuration.contract_version,
            rule_version=request.configuration.rule_config_version,
            code_revision=self.code_revision,
            requested_stages=request.requested_stages,
            stage_outcomes=[
                StageOutcome(
                    stage=stage,
                    status="completed" if stage == "load_portfolio" else "pending",
                    reason=None,
                    attempt_count=attempt if stage == "load_portfolio" else 0,
                    duration_ms=load_ms if stage == "load_portfolio" else 0,
                )
                for stage in STAGES
            ],
            output_artifact_ids=[],
            errors=[],
        )
        result = Result(
            run=run,
            configuration=request.configuration,
            validation=None,
            metrics=None,
            metrics_hash=None,
            evidence=[],
        )
        if previous is None:
            created = run.model_copy(
                update={
                    "revision": 0,
                    "status": "created",
                    "stage_outcomes": [
                        StageOutcome(
                            stage=stage,
                            status="pending",
                            reason=None,
                            attempt_count=0,
                            duration_ms=0,
                        )
                        for stage in STAGES
                    ],
                }
            )
            self.state.start(
                request, result.model_copy(update={"run": created}), fingerprint, None, None
            )
        self.state.start(
            request,
            result,
            fingerprint,
            self._event(run, "load_portfolio", "operation_started", None, "in_progress"),
            previous.revision if previous else 0,
        )
        return result

    def _validate(
        self, request: AnalysisRequest, bundle: Bundle, changed_analysis: bool
    ) -> Validation:
        input_hash = bundle.input_hash
        if bundle.issue == "resource_limit":
            return Validation(self._report(bundle, "limit_failed", complete=False))
        if bundle.issue == "unreadable_input":
            return Validation(
                self._report(
                    bundle,
                    "rejected",
                    findings=[
                        Diagnostic(
                            code="unreadable_input",
                            scope="file",
                            row_number=None,
                            field=None,
                            message="The CSV or manifest could not be read.",
                        ),
                    ],
                )
            )
        assert input_hash is not None
        parser_hash = request.configuration.parser_config_hash
        binding = self.state.import_binding(request.import_idempotency_key)
        exact = binding is not None and (binding.bundle_hash, binding.parser_hash) == (
            input_hash,
            parser_hash,
        )
        if binding and exact and not changed_analysis:
            report = Report.model_validate_json(self.state.read(binding.report_hash))
            if report.input_hash != input_hash:
                raise OperationError("integrity_error")
            snapshot = self.state.snapshot(report.snapshot_id) if report.snapshot_id else None
            if report.disposition == "valid":
                if snapshot is None or snapshot.bundle_hash != input_hash:
                    raise OperationError("integrity_error")
                payload = self.state.read(snapshot.artifact_hash)
                return self._cached_valid(report, snapshot, payload, binding)
            return Validation(report, previous_import=binding)

        scan = self.state.scan(bundle, request.configuration.parser_limits)
        if scan.limit:
            return Validation(
                self._report(bundle, "limit_failed", complete=False, message=scan.limit)
            )
        if changed_analysis or (binding and not exact):
            return Validation(self._report(bundle, "conflict", code="idempotency_conflict"))
        snapshot = self.state.snapshot(scan.candidate_id) if scan.candidate_id else None
        if snapshot is not None and snapshot.bundle_hash != input_hash:
            return Validation(self._report(bundle, "conflict", code="identity_conflict"))
        if scan.findings:
            return Validation(
                self._report(
                    bundle,
                    "rejected",
                    findings=scan.findings,
                    complete=scan.complete,
                )
            )
        manifest = scan.manifest
        assert manifest is not None
        payload = scan.snapshot_payload()
        snapshot = SnapshotBinding(
            manifest.snapshot_id,
            manifest.portfolio_id,
            input_hash,
            sha256(payload),
        )
        return Validation(
            self._report(bundle, "valid", snapshot_id=manifest.snapshot_id),
            snapshot,
            payload,
            scan.loans,
            manifest.as_of,
        )

    @staticmethod
    def _report(
        bundle: Bundle,
        disposition: Literal["valid", "rejected", "limit_failed", "conflict"],
        *,
        findings: list[Diagnostic] | None = None,
        complete: bool = True,
        code: OperationCode | None = None,
        message: str | None = None,
        snapshot_id: str | None = None,
    ) -> Report:
        diagnostics = findings or []
        operation = code or OPERATIONS[disposition]
        return Report(
            report_id=_id(),
            input_hash=bundle.input_hash,
            disposition=disposition,
            report_complete=complete,
            error_code=diagnostics[0].code if diagnostics else operation,
            rule_id=diagnostics[0].rule_id if diagnostics else None,
            snapshot_id=snapshot_id,
            findings=diagnostics,
            sanitized_message=message
            or (SAFE_MESSAGES[operation] if operation else "The bundle passed validation."),
        )

    def _cached_valid(
        self,
        report: Report,
        snapshot: SnapshotBinding,
        payload: bytes,
        binding: ImportBinding,
    ) -> Validation:
        # Validated snapshot artifacts contain normalized, schema-checked domain values.
        parsed = SnapshotPayload.model_validate_json(payload)
        if (parsed.snapshot_id, parsed.portfolio_id) != (
            snapshot.snapshot_id,
            snapshot.portfolio_id,
        ):
            raise OperationError("integrity_error")
        return Validation(report, snapshot, payload, parsed.domain_loans(), parsed.as_of, binding)

    def _commit(
        self,
        request: AnalysisRequest,
        bundle: Bundle,
        running: Result,
        validation: Validation,
        artifacts: dict[str, Artifact],
        validated_ms: int,
    ) -> Result:
        run = running.run
        config = request.configuration
        report = validation.report
        snapshot = validation.snapshot
        disposition = report.disposition
        started = perf_counter_ns()
        snapshot_evidence = None
        metrics = None
        evidence: list[EvidenceRef] = []
        if snapshot is not None:
            assert validation.loans is not None and validation.as_of is not None
            snapshot_evidence = EvidenceRef(
                evidence_id=_id(),
                run_id=run.run_id,
                kind="snapshot",
                artifact_hash=snapshot.artifact_hash,
                locator=SnapshotLocator(snapshot_id=snapshot.snapshot_id),
            )
            evidence.append(snapshot_evidence)
            if validation.loans and bundle.input_hash:
                evidence.append(
                    EvidenceRef(
                        evidence_id=_id(),
                        run_id=run.run_id,
                        kind="source_row",
                        artifact_hash=bundle.input_hash,
                        locator=SourceRowLocator(
                            snapshot_id=snapshot.snapshot_id,
                            row_number=2,
                            field=None,
                        ),
                    )
                )
            totals = calculate(validation.loans)
            metrics = Metrics(
                metrics_id=_id(),
                run_id=run.run_id,
                snapshot_id=snapshot.snapshot_id,
                calculation_version=config.calculation_version,
                rule_config_version=config.rule_config_version,
                currency="USD",
                as_of=validation.as_of,
                loan_count=totals.loan_count,
                open_loan_count=totals.open_loan_count,
                total_exposure=totals.total_exposure,
                delinquency_count_rate=totals.delinquency_count_rate,
                delinquency_exposure_rate=totals.delinquency_exposure_rate,
                concentration=totals.concentration,
                evidence_ids=[snapshot_evidence.evidence_id],
            )
        metrics_ms = _ms(started)
        finalized = perf_counter_ns()
        report_hash = (
            validation.previous_import.report_hash
            if validation.previous_import is not None
            else self.state.publish(_json(report))
        )
        artifacts[report.report_id] = Artifact("validation_report", report_hash)
        report_evidence = EvidenceRef(
            evidence_id=_id(),
            run_id=run.run_id,
            kind="validation_report",
            artifact_hash=report_hash,
            locator=ReportLocator(report_id=report.report_id),
        )
        evidence.append(report_evidence)
        findings = [
            DataQualityFinding(
                finding_id=_id(),
                run_id=run.run_id,
                rule_id=item.rule_id,
                rule_version=config.rule_config_version,
                severity="error",
                summary=item.message,
                evidence_ids=[report_evidence.evidence_id],
                scope=item.scope,
                row_number=item.row_number,
                field=item.field,
                code=item.code,
                blocking=True,
            )
            for item in report.findings
        ]
        metrics_artifact = None
        if snapshot and metrics:
            assert validation.snapshot_bytes is not None
            artifacts[_id()] = Artifact(
                "validated_snapshot", self.state.publish(validation.snapshot_bytes)
            )
            metrics_artifact = self.state.publish(_json(metrics))
            artifacts[metrics.metrics_id] = Artifact("metrics", metrics_artifact)
            evidence.append(
                EvidenceRef(
                    evidence_id=_id(),
                    run_id=run.run_id,
                    kind="metric",
                    artifact_hash=metrics_artifact,
                    locator=MetricLocator(
                        metrics_id=metrics.metrics_id, metric_key="total_exposure"
                    ),
                )
            )

        code = OPERATIONS[disposition]
        if report.error_code == "idempotency_conflict":
            code = "idempotency_conflict"
        binding = validation.previous_import
        import_id = binding.import_id if binding else run.import_id
        validation_result = self._import_result(
            request,
            bundle,
            run,
            report,
            snapshot,
            report_hash,
            findings,
            import_id,
            code,
        )
        run = self._terminal(
            run,
            disposition,
            code,
            import_id,
            snapshot,
            validated_ms,
            metrics_ms,
            _ms(finalized),
        )
        events = [
            self._event(
                run,
                "validate_portfolio",
                "validation_completed",
                validated_ms,
                disposition,
                code,
                report_hash,
            ),
        ]
        if metrics_artifact is not None:
            events.append(
                self._event(
                    run,
                    "calculate_metrics",
                    "metrics_completed",
                    metrics_ms,
                    "succeeded",
                    output=metrics_artifact,
                )
            )
        events.append(
            self._event(
                run,
                "finalize",
                "publication_committed",
                _ms(finalized),
                "succeeded" if disposition == "valid" else disposition,
                code,
            )
        )
        batch = self.state.publish(
            canonical(
                [
                    event.model_dump(mode="json")
                    for event in [*self.state.events(run.run_id), *events]
                ]
            )
        )
        artifacts[_id()] = Artifact("event_batch", batch)
        run = run.model_copy(update={"output_artifact_ids": list(artifacts)})
        result = Result(
            run=run,
            configuration=config,
            validation=validation_result,
            metrics=metrics,
            metrics_hash=metrics.semantic_hash if metrics else None,
            evidence=evidence,
        )
        if (
            binding is None
            and bundle.input_hash
            and disposition != "conflict"
            and self.state.import_binding(request.import_idempotency_key) is None
        ):
            binding = ImportBinding(
                request.import_idempotency_key,
                config.parser_config_hash,
                bundle.input_hash,
                import_id,
                report_hash,
            )
        self.state.finish(result, run.revision - 1, artifacts, snapshot, binding, events)
        return result

    @staticmethod
    def _import_result(
        request: AnalysisRequest,
        bundle: Bundle,
        run: RunManifest,
        report: Report,
        snapshot: SnapshotBinding | None,
        report_hash: str,
        findings: list[DataQualityFinding],
        import_id: str,
        code: OperationCode | None,
    ) -> ImportResult:
        return ImportResult(
            import_id=import_id,
            run_id=run.run_id,
            import_idempotency_key=request.import_idempotency_key,
            disposition=report.disposition,
            snapshot_id=snapshot.snapshot_id if snapshot else None,
            portfolio_id=snapshot.portfolio_id if snapshot else None,
            input_hash=bundle.input_hash,
            source_sha256=sha256(bundle.csv) if bundle.csv is not None else None,
            canonical_input_hash=snapshot.artifact_hash if snapshot else None,
            parser_config_version=request.configuration.parser_config_version,
            parser_config_hash=request.configuration.parser_config_hash,
            findings=findings,
            validation_report_id=report.report_id,
            report_hash=report_hash,
            report_complete=report.report_complete,
            error_code=code,
        )

    @staticmethod
    def _terminal(
        run: RunManifest,
        disposition: str,
        code: OperationCode | None,
        import_id: str,
        snapshot: SnapshotBinding | None,
        validated_ms: int,
        metrics_ms: int,
        finalized_ms: int,
    ) -> RunManifest:
        valid = disposition == "valid"
        attempt = run.stage_outcomes[0].attempt_count
        return run.model_copy(
            update={
                "revision": run.revision + 1,
                "completed_at": _utc(),
                "status": "succeeded" if valid else disposition,
                "import_id": import_id,
                "snapshot_id": snapshot.snapshot_id if snapshot else None,
                "canonical_input_hash": snapshot.artifact_hash if snapshot else None,
                "stage_outcomes": [
                    run.stage_outcomes[0],
                    StageOutcome(
                        stage="validate_portfolio",
                        status="completed",
                        reason=None,
                        attempt_count=attempt,
                        duration_ms=validated_ms,
                    ),
                    StageOutcome(
                        stage="calculate_metrics",
                        status="completed" if valid else "unavailable",
                        reason=SAFE_MESSAGES[code] if code else None,
                        attempt_count=attempt if valid else 0,
                        duration_ms=metrics_ms if valid else 0,
                    ),
                    StageOutcome(
                        stage="finalize",
                        status="completed",
                        reason=None,
                        attempt_count=attempt,
                        duration_ms=finalized_ms,
                    ),
                ],
            }
        )

    def _failed(self, running: Result, code: OperationCode, duration: int) -> Result:
        run = running.run
        run = run.model_copy(
            update={
                "status": "failed",
                "revision": run.revision + 1,
                "completed_at": _utc(),
                "errors": [
                    RunError(
                        stage="finalize",
                        code=code,
                        message=SAFE_MESSAGES[code],
                        retryable=False,
                    )
                ],
                "stage_outcomes": [
                    *run.stage_outcomes[:-1],
                    StageOutcome(
                        stage="finalize",
                        status="failed",
                        reason=SAFE_MESSAGES[code],
                        attempt_count=run.stage_outcomes[0].attempt_count,
                        duration_ms=duration,
                    ),
                ],
            }
        )
        result = running.model_copy(update={"run": run})
        event = self._event(run, "finalize", "operation_failed", duration, "failed", code)
        try:
            self.state.finish(result, run.revision - 1, {}, None, None, [event])
        except OperationError as error:
            raise OperationError(code) from error
        return result

    @staticmethod
    def _event(
        run: RunManifest,
        stage: Stage,
        event_type: EventType,
        duration: int | None,
        outcome: Literal[
            "in_progress", "valid", "rejected", "conflict", "limit_failed", "succeeded", "failed"
        ],
        code: OperationCode | None = None,
        output: str | None = None,
    ) -> Event:
        return Event(
            event_id=_id(),
            run_id=run.run_id,
            revision=run.revision,
            stage=stage,
            attempt=run.stage_outcomes[0].attempt_count,
            event_type=event_type,
            timestamp_utc=_utc(),
            duration_ms=duration,
            outcome=outcome,
            code=code,
            input_hash=run.input_hash,
            output_artifact_hash=output,
        )

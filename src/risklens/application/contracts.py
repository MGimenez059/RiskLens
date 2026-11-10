"""Boundary DTOs for the accepted M02 contracts."""

import hashlib
import json
import re
from datetime import date
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PositiveInt,
    field_validator,
    model_validator,
)

from risklens.domain.metrics import GroupShare, MetricValue, Reason, cents, ratio

ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$"
Id = Annotated[str, Field(pattern=ID_PATTERN)]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Text = Annotated[str, Field(min_length=1)]
Count = Annotated[int, Field(ge=0)]
RowNumber = Annotated[int, Field(ge=2)]
DateText = Annotated[str, Field(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")]
Timestamp = Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")]
InputAmount = Annotated[str, Field(pattern=r"^[0-9]+(\.[0-9]{1,2})?$")]
Amount = Annotated[str, Field(pattern=r"^(0|[1-9][0-9]*)\.[0-9]{2}$")]
InputCount = Annotated[str, Field(pattern=r"^(0|[1-9][0-9]*)$")]
Disposition = Literal["valid", "rejected", "conflict", "limit_failed"]
RunStatus = Literal[
    "created", "running", "succeeded", "rejected", "conflict", "limit_failed", "failed"
]
Stage = Literal["load_portfolio", "validate_portfolio", "calculate_metrics", "finalize"]
ValidationCode = Literal[
    "unreadable_input",
    "schema_invalid",
    "missing_required",
    "duplicate_key",
    "invalid_value",
    "invariant_failed",
    "integrity_mismatch",
]
OperationCode = Literal[
    "input_invalid",
    "identity_conflict",
    "idempotency_conflict",
    "resource_limit",
    "configuration_invalid",
    "persistence_failed",
    "integrity_error",
    "internal_error",
]
EventType = Literal[
    "operation_started",
    "validation_completed",
    "metrics_completed",
    "publication_committed",
    "operation_failed",
    "replay_returned",
]
STAGES: tuple[Stage, ...] = (
    "load_portfolio",
    "validate_portfolio",
    "calculate_metrics",
    "finalize",
)
ACTIVE_RUN_STATUSES = {"created", "running"}
IMPORT_RUN_STATUS = {
    "valid": "succeeded",
    "rejected": "rejected",
    "conflict": "conflict",
    "limit_failed": "limit_failed",
}
IMPORT_CODES: dict[Disposition, set[OperationCode | None]] = {
    "valid": {None},
    "rejected": {"input_invalid"},
    "conflict": {"identity_conflict", "idempotency_conflict"},
    "limit_failed": {"resource_limit"},
}

SAFE_MESSAGES: dict[OperationCode, str] = {
    "input_invalid": "The bundle contains invalid input.",
    "identity_conflict": "The snapshot identity is already bound to a different bundle or owner.",
    "idempotency_conflict": "The request key is already bound to a different request.",
    "resource_limit": "The bundle exceeds a configured local safety limit.",
    "configuration_invalid": "The request configuration or run reference is invalid.",
    "persistence_failed": "The local state could not be saved or opened.",
    "integrity_error": "A committed artifact is missing or fails integrity verification.",
    "internal_error": "The analysis could not be completed.",
}


class OperationError(Exception):
    def __init__(self, code: OperationCode) -> None:
        self.code = code
        super().__init__(SAFE_MESSAGES[code])


class DTO(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, hide_input_in_errors=True)


def unique_refs(values: list[str]) -> list[str]:
    if len(values) != len(set(values)):
        raise ValueError("Reference IDs must be unique")
    return values


RefList = Annotated[list[Id], Field(min_length=1), AfterValidator(unique_refs)]


class Manifest(DTO):
    schema_version: Literal["1.0"]
    snapshot_id: Id
    portfolio_id: Id
    portfolio_name: Text
    as_of: DateText
    currency: Literal["USD"]
    synthetic: Literal[True]
    generator_version: Text
    seed: Count
    source_sha256: Hash

    @field_validator("synthetic", mode="before")
    @classmethod
    def synthetic_only(cls, value: object) -> object:
        if value is not True:
            raise ValueError("Synthetic provenance must be true")
        return value


class LoanRow(DTO):
    loan_id: Id
    customer_id: Id
    original_principal: InputAmount
    outstanding_principal: InputAmount
    days_past_due: InputCount
    loan_status: Literal["open", "closed"]
    origination_date: DateText
    segment: Id | None


class ParserLimits(DTO):
    max_input_bytes: PositiveInt = 10_485_760
    max_manifest_bytes: PositiveInt = 65_536
    max_rows: PositiveInt = 50_000
    max_field_bytes: PositiveInt = 4_096
    max_numeric_chars: PositiveInt = 24
    max_collected_findings: PositiveInt = 1_000

    @model_validator(mode="after")
    def manifest_subset(self) -> Self:
        if self.max_manifest_bytes > self.max_input_bytes:
            raise ValueError("Manifest byte limit exceeds bundle byte limit")
        return self


class AnalysisConfiguration(DTO):
    config_version: Literal["m02-v1"] = "m02-v1"
    currency: Literal["USD"] = "USD"
    contract_version: Literal["1.0"] = "1.0"
    calculation_version: Literal["m02-v1"] = "m02-v1"
    rule_config_version: Literal["m02-v1"] = "m02-v1"
    arithmetic_version: Literal["ct-017-v1"] = "ct-017-v1"
    parser_config_version: Literal["provisional-local-v1"] = "provisional-local-v1"
    parser_limits: ParserLimits = Field(default_factory=ParserLimits)
    publication_version: Literal["ct-018-v1"] = "ct-018-v1"
    event_catalog_version: Literal["ct-019-v1"] = "ct-019-v1"

    @property
    def config_hash(self) -> str:
        return sha256(canonical(self.model_dump(mode="json")))

    @property
    def parser_config_hash(self) -> str:
        return sha256(
            canonical(
                {
                    "parser_config_version": self.parser_config_version,
                    "parser_limits": self.parser_limits.model_dump(),
                }
            )
        )


def complete_configuration(value: object) -> object:
    if isinstance(value, dict):
        limits = value.get("parser_limits")
        if AnalysisConfiguration.model_fields.keys() - value.keys() or (
            isinstance(limits, dict) and ParserLimits.model_fields.keys() - limits.keys()
        ):
            raise ValueError("An effective configuration must supply all fields")
    return value


EffectiveConfiguration = Annotated[AnalysisConfiguration, BeforeValidator(complete_configuration)]


class AnalysisRequest(DTO):
    bundle_ref: Id
    import_idempotency_key: Id
    analysis_idempotency_key: Id
    mode: Literal["deterministic_m02"]
    requested_stages: tuple[Literal["validate_portfolio"], Literal["calculate_metrics"]]
    configuration: EffectiveConfiguration
    parent_run_id: Id | None

    def fingerprint(self, input_hash: str) -> str:
        return sha256(
            canonical(
                {
                    "bundle_hash": input_hash,
                    "config_hash": self.configuration.config_hash,
                    "mode": self.mode,
                    "requested_stages": self.requested_stages,
                    "parent_run_id": self.parent_run_id,
                }
            )
        )


class Diagnostic(DTO):
    code: ValidationCode
    scope: Literal["file", "row", "field"]
    row_number: RowNumber | None
    field: Id | None
    message: Text

    @property
    def rule_id(self) -> str:
        return "BR-DQ-001" if self.code == "duplicate_key" else "BR-DQ-002"


class Report(DTO):
    report_id: Id
    input_hash: Hash | None
    disposition: Disposition
    report_complete: bool
    error_code: OperationCode | ValidationCode | None
    rule_id: Id | None
    snapshot_id: Id | None
    findings: list[Diagnostic]
    sanitized_message: Text = Field(
        validation_alias=AliasChoices("sanitized_message", "message"),
    )

    @model_validator(mode="after")
    def report_outcome(self) -> Self:
        if (self.disposition == "valid") != (self.snapshot_id is not None):
            raise ValueError("Only a valid report can identify a snapshot")
        if self.disposition == "rejected":
            if not self.findings or (self.error_code, self.rule_id) != (
                self.findings[0].code,
                self.findings[0].rule_id,
            ):
                raise ValueError("A rejection requires cataloged findings")
        elif (
            self.findings
            or self.rule_id is not None
            or self.error_code not in (IMPORT_CODES[self.disposition])
        ):
            raise ValueError("Report diagnostics do not match the disposition")
        return self


class DataQualityFinding(DTO):
    finding_id: Id
    run_id: Id
    rule_id: Id
    rule_version: Text
    severity: Literal["error"]
    summary: Text
    evidence_ids: RefList
    scope: Literal["file", "row", "field"]
    row_number: RowNumber | None
    field: Id | None
    code: ValidationCode
    blocking: Literal[True]

    @model_validator(mode="after")
    def catalog_location(self) -> Self:
        if self.blocking is not True:
            raise ValueError("M02 validation findings are blocking")
        if (self.scope == "file") != (self.row_number is None):
            raise ValueError("Finding scope does not match its record ordinal")
        if self.scope == "field" and self.field is None:
            raise ValueError("Field scope requires a field")
        rule = "BR-DQ-001" if self.code == "duplicate_key" else "BR-DQ-002"
        if self.rule_id != rule:
            raise ValueError("Finding rule does not match the catalog")
        return self


class ImportResult(DTO):
    import_id: Id
    run_id: Id
    import_idempotency_key: Id
    disposition: Disposition
    snapshot_id: Id | None
    portfolio_id: Id | None
    input_hash: Hash | None
    source_sha256: Hash | None
    canonical_input_hash: Hash | None
    parser_config_version: Text
    parser_config_hash: Hash
    findings: list[DataQualityFinding]
    validation_report_id: Id
    report_hash: Hash
    report_complete: bool
    error_code: OperationCode | None

    @model_validator(mode="after")
    def matching_disposition(self) -> Self:
        if self.error_code not in IMPORT_CODES[self.disposition]:
            raise ValueError("Import error code does not match disposition")
        if self.disposition == "valid":
            if not all(
                (
                    self.snapshot_id,
                    self.portfolio_id,
                    self.input_hash,
                    self.source_sha256,
                    self.canonical_input_hash,
                    self.report_complete,
                )
            ):
                raise ValueError("Valid imports require complete provenance and validation")
        elif any((self.snapshot_id, self.portfolio_id, self.canonical_input_hash)):
            raise ValueError("Only valid imports may refer to a published snapshot")
        if self.input_hash is not None and self.source_sha256 is None:
            raise ValueError("A complete bundle requires a source CSV hash")
        if bool(self.findings) != (self.disposition == "rejected"):
            raise ValueError("Only rejected imports have validation findings")
        if any(finding.run_id != self.run_id for finding in self.findings):
            raise ValueError("A finding belongs to a different run")
        unique_refs([finding.finding_id for finding in self.findings])
        return self


class StageOutcome(DTO):
    stage: Stage
    status: Literal["pending", "completed", "not_requested", "unavailable", "failed"]
    reason: Text | None
    attempt_count: Count
    duration_ms: Count

    @model_validator(mode="after")
    def explain_unavailable_stage(self) -> Self:
        if self.status in {"unavailable", "failed"} and self.reason is None:
            raise ValueError("Unavailable and failed stages require a reason")
        return self


class RunError(DTO):
    stage: Stage
    code: OperationCode
    message: Text
    retryable: bool


class RunManifest(DTO):
    run_id: Id
    parent_run_id: Id | None
    import_id: Id
    snapshot_id: Id | None
    revision: Count
    status: RunStatus
    created_at: Timestamp
    completed_at: Timestamp | None
    input_hash: Hash | None
    canonical_input_hash: Hash | None
    config_hash: Hash
    baseline_version: Text
    contract_version: Text
    rule_version: Text
    code_revision: Text
    requested_stages: tuple[Literal["validate_portfolio"], Literal["calculate_metrics"]]
    stage_outcomes: list[StageOutcome]
    output_artifact_ids: list[Id]
    errors: list[RunError]

    @model_validator(mode="after")
    def lifecycle(self) -> Self:
        active = self.status in ACTIVE_RUN_STATUSES
        if active != (self.completed_at is None):
            raise ValueError("Completion timestamp does not match run status")
        if self.parent_run_id == self.run_id:
            raise ValueError("A run cannot be its own parent")
        unique_refs(self.output_artifact_ids)
        stages = {outcome.stage: outcome.status for outcome in self.stage_outcomes}
        if len(stages) != len(self.stage_outcomes):
            raise ValueError("Stage outcomes must be unique")
        if self.status == "succeeded":
            if not all((self.snapshot_id, self.canonical_input_hash, self.input_hash)):
                raise ValueError("Successful runs require complete snapshot provenance")
            if any(stages.get(stage) != "completed" for stage in STAGES) or self.errors:
                raise ValueError("Successful runs require completed stages")
        elif self.status in {"rejected", "conflict", "limit_failed"} and (
            self.snapshot_id is not None
            or self.canonical_input_hash is not None
            or stages.get("calculate_metrics") == "completed"
        ):
            raise ValueError("Invalid imports cannot have a calculated result")
        return self


class Event(DTO):
    event_id: Id
    run_id: Id
    revision: Count
    stage: Stage
    attempt: PositiveInt
    event_type: EventType
    timestamp_utc: Timestamp
    duration_ms: Count | None
    outcome: Literal[
        "in_progress", "valid", "rejected", "conflict", "limit_failed", "succeeded", "failed"
    ]
    code: OperationCode | None
    input_hash: Hash | None
    output_artifact_hash: Hash | None

    @model_validator(mode="after")
    def completion_fields(self) -> Self:
        if self.event_type != "operation_started" and self.duration_ms is None:
            raise ValueError("Completion requires a duration")
        if self.outcome in {"rejected", "conflict", "limit_failed", "failed"} and self.code is None:
            raise ValueError("Failure outcome requires an operation code")
        return self


class Metrics(DTO):
    metrics_id: Id
    run_id: Id
    snapshot_id: Id
    calculation_version: Text
    rule_config_version: Text
    currency: Literal["USD"]
    as_of: DateText
    loan_count: Count
    open_loan_count: Count
    total_exposure: Amount
    delinquency_count_rate: MetricValue
    delinquency_exposure_rate: MetricValue
    concentration: list[GroupShare]
    evidence_ids: RefList

    @model_validator(mode="after")
    def exact_metrics(self) -> Self:
        date.fromisoformat(self.as_of)
        if self.open_loan_count > self.loan_count:
            raise ValueError("Open loan count exceeds loan count")
        exposure = cents(self.total_exposure)
        if exposure and not self.open_loan_count:
            raise ValueError("A closed population has zero exposure")
        reason: Reason = "zero_denominator" if self.open_loan_count else "no_eligible_population"
        count = self.delinquency_count_rate
        amount = self.delinquency_exposure_rate
        if count != ratio(
            int(count.numerator),
            self.open_loan_count,
            "count_ratio",
            "BR-RISK-002",
            empty_reason=reason,
        ) or amount != ratio(
            cents(amount.numerator),
            exposure,
            "exposure_ratio",
            "BR-RISK-002",
            empty_reason=reason,
        ):
            raise ValueError("Delinquency rates disagree with their operands")

        groups = {"borrower": 0, "segment": 0}
        keys: set[tuple[str, str | None]] = set()
        for group in self.concentration:
            key = (group.dimension, group.group_id)
            if (
                key in keys
                or (group.group_id is None and group.dimension == "borrower")
                or (group.group_id is not None and re.fullmatch(ID_PATTERN, group.group_id) is None)
            ):
                raise ValueError("Invalid concentration group identity")
            keys.add(key)
            subtotal = cents(group.group_exposure)
            if group.share != ratio(subtotal, exposure, "exposure_ratio", "BR-RISK-003"):
                raise ValueError("Group share disagrees with its operands")
            if group.group_exposure != group.share.numerator:
                raise ValueError("Group exposure must match the share numerator")
            groups[group.dimension] += subtotal
        if any(total != exposure for total in groups.values()):
            raise ValueError("Concentration does not reconcile to total exposure")
        if len({dimension for dimension, _ in keys}) != (2 if self.loan_count else 0):
            raise ValueError("Concentration dimensions do not match the loan population")
        return self

    @property
    def semantic_hash(self) -> str:
        payload = self.model_dump(mode="json", exclude={"metrics_id", "run_id", "evidence_ids"})
        payload["concentration"].sort(
            key=lambda group: (group["dimension"], group["group_id"] or "")
        )
        return sha256(canonical(payload))


class SnapshotLocator(DTO):
    snapshot_id: Id


class SourceRowLocator(SnapshotLocator):
    row_number: RowNumber
    field: Id | None


class MetricLocator(DTO):
    metrics_id: Id
    metric_key: Text


class ReportLocator(DTO):
    report_id: Id


EVIDENCE_LOCATORS = {
    "snapshot": SnapshotLocator,
    "source_row": SourceRowLocator,
    "metric": MetricLocator,
    "validation_report": ReportLocator,
}


class EvidenceRef(DTO):
    evidence_id: Id
    run_id: Id
    kind: Literal["snapshot", "source_row", "metric", "validation_report"]
    artifact_hash: Hash
    locator: SnapshotLocator | SourceRowLocator | MetricLocator | ReportLocator

    @model_validator(mode="after")
    def matching_locator(self) -> Self:
        if type(self.locator) is not EVIDENCE_LOCATORS[self.kind]:
            raise ValueError("Evidence kind does not match locator type")
        return self


class Result(DTO):
    run: RunManifest
    configuration: EffectiveConfiguration
    validation: ImportResult | None
    metrics: Metrics | None
    metrics_hash: Hash | None
    evidence: list[EvidenceRef]

    @model_validator(mode="after")
    def run_lineage(self) -> Self:
        run = self.run
        config = self.configuration
        if (run.config_hash, run.contract_version, run.rule_version) != (
            config.config_hash,
            config.contract_version,
            config.rule_config_version,
        ):
            raise ValueError("Run configuration does not match its lineage")
        if (run.status == "succeeded") != (self.metrics_hash is not None):
            raise ValueError("Only successful runs have metric hashes")
        if self.metrics is not None:
            self.verify_metrics(self.metrics)
        evidence = {ref.evidence_id: ref for ref in self.evidence}
        if len(evidence) != len(self.evidence) or any(
            ref.run_id != run.run_id for ref in self.evidence
        ):
            raise ValueError("Evidence IDs must be unique and belong to the run")
        if self.validation is None:
            if run.status in IMPORT_RUN_STATUS.values():
                raise ValueError("An import outcome requires validation metadata")
            return self
        validation = self.validation
        if (
            run.status != IMPORT_RUN_STATUS[validation.disposition]
            or (
                validation.run_id,
                validation.import_id,
                validation.snapshot_id,
                validation.input_hash,
                validation.canonical_input_hash,
            )
            != (
                run.run_id,
                run.import_id,
                run.snapshot_id,
                run.input_hash,
                run.canonical_input_hash,
            )
            or (validation.parser_config_version, validation.parser_config_hash)
            != (
                config.parser_config_version,
                config.parser_config_hash,
            )
        ):
            raise ValueError("Validation metadata does not match the run")
        for finding in validation.findings:
            if not evidence.keys() >= set(finding.evidence_ids):
                raise ValueError("A finding references unknown evidence")
            if finding.scope == "file" and not any(
                evidence[key].kind == "validation_report" for key in finding.evidence_ids
            ):
                raise ValueError("File-level findings require validation report evidence")
        return self

    def verify_metrics(self, metrics: Metrics) -> None:
        run = self.run
        if (
            run.status != "succeeded"
            or (metrics.run_id, metrics.snapshot_id) != (run.run_id, run.snapshot_id)
            or (metrics.calculation_version, metrics.rule_config_version)
            != (
                self.configuration.calculation_version,
                self.configuration.rule_config_version,
            )
            or metrics.semantic_hash != self.metrics_hash
        ):
            raise ValueError("Metrics do not match the successful run")
        evidence = {ref.evidence_id: ref.kind for ref in self.evidence}
        if not evidence.keys() >= set(metrics.evidence_ids):
            raise ValueError("Metrics reference unknown evidence")
        if not any(evidence[key] in {"snapshot", "source_row"} for key in metrics.evidence_ids):
            raise ValueError("Metrics require snapshot-derived evidence")


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

"""Parse and bound a complete CSV/JSON bundle without repairing it."""

import csv
import io
import json
import re
from collections.abc import Iterator
from datetime import date
from threading import Lock
from typing import Literal

from pydantic import ValidationError

from risklens.application.contracts import (
    DTO,
    Diagnostic,
    LoanRow,
    Manifest,
    ParserLimits,
    ValidationCode,
    sha256,
)
from risklens.application.ports import Scan
from risklens.domain.metrics import Loan, cents

HEADER = tuple(LoanRow.model_fields)
NUMERIC = {"original_principal", "outstanding_principal", "days_past_due"}
PREFIX = b"RiskLensBundleV1"
OPAQUE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}")
_CSV_LOCK = Lock()


def frame(manifest: bytes, csv_bytes: bytes) -> bytes:
    return (
        PREFIX
        + len(manifest).to_bytes(8, "big")
        + manifest
        + len(csv_bytes).to_bytes(8, "big")
        + csv_bytes
    )


def unframe(data: bytes) -> tuple[bytes, bytes]:
    start = len(PREFIX)
    middle = start + 8 + int.from_bytes(data[start : start + 8], "big")
    end = middle + 8 + int.from_bytes(data[middle : middle + 8], "big")
    if not data.startswith(PREFIX) or end != len(data) or middle + 8 > end:
        raise ValueError("Invalid bundle framing")
    return data[start + 8 : middle], data[middle + 8 :]


class LimitExceeded(Exception):
    """A configured limit stopped the scan. The message is safe to display."""


class DiagnosticCap(Exception):
    pass


def _distinct_object(items: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in items:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(_: str) -> None:
    raise ValueError("Invalid JSON constant")


def _strings(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


class BundleScanner:
    def __init__(self, limits: ParserLimits) -> None:
        self.limits = limits
        self.result = Scan(None, None, [], [])

    def scan(self, manifest: bytes, csv_bytes: bytes) -> Scan:
        try:
            self._manifest(manifest, csv_bytes)
            self._loans(csv_bytes)
        except LimitExceeded as error:
            self.result.limit = str(error)
            self.result.complete = False
        except DiagnosticCap:
            self.result.complete = False
        return self.result

    def _add(
        self,
        code: ValidationCode,
        message: str,
        row: int | None = None,
        field: str | None = None,
    ) -> None:
        scope: Literal["file", "row", "field"] = "file"
        if row is not None:
            scope = "field" if field else "row"
        self.result.findings.append(
            Diagnostic(
                code=code,
                scope=scope,
                row_number=row,
                field=field,
                message=message,
            )
        )
        if len(self.result.findings) == self.limits.max_collected_findings:
            raise DiagnosticCap

    def _schema_findings(
        self,
        model: type[DTO],
        error: ValidationError,
        row: int | None = None,
    ) -> None:
        for issue in error.errors(include_input=False, include_context=False, include_url=False):
            field = issue["loc"][0] if issue["loc"] else None
            if not isinstance(field, str) or field not in model.model_fields:
                self._add("schema_invalid", "Unexpected field.", row)
            elif issue["type"] == "missing":
                self._add("missing_required", f"Required field {field} is missing.", row, field)
            else:
                code: ValidationCode = "invalid_value"
                if field == "schema_version":
                    code = "schema_invalid"
                elif field in {"currency", "synthetic", "as_of", "origination_date"}:
                    code = "invariant_failed"
                self._add(code, f"Invalid {field}.", row, field)

    def _check_fields(self, values: Iterator[str]) -> None:
        for value in values:
            if len(value.encode("utf-8")) > self.limits.max_field_bytes:
                raise LimitExceeded("A field exceeds the UTF-8 byte limit.")

    def _check_numeric(self, value: str) -> None:
        if len(value) > self.limits.max_numeric_chars:
            raise LimitExceeded("An input numeric token exceeds the character limit.")

    def _json_int(self, token: str) -> int:
        self._check_numeric(token)
        return int(token)

    def _json_float(self, token: str) -> object:
        self._check_numeric(token)
        return object()

    def _manifest(self, manifest: bytes, csv_bytes: bytes) -> None:
        try:
            values = json.loads(
                manifest.decode("utf-8"),
                object_pairs_hook=_distinct_object,
                parse_int=self._json_int,
                parse_float=self._json_float,
                parse_constant=_invalid_constant,
            )
            self._check_fields(_strings(values))
        except (ValueError, RecursionError):
            self._add("schema_invalid", "The manifest is not a supported UTF-8 JSON object.")
            return
        if isinstance(values, dict):
            candidate = values.get("snapshot_id")
            if isinstance(candidate, str) and OPAQUE_ID.fullmatch(candidate):
                self.result.candidate_id = candidate
        try:
            parsed = Manifest.model_validate(values)
        except ValidationError as error:
            self._schema_findings(Manifest, error)
            return
        try:
            date.fromisoformat(parsed.as_of)
        except ValueError:
            self._add("invariant_failed", "Invalid observation date.", field="as_of")
            return
        self.result.manifest = parsed
        if sha256(csv_bytes) != parsed.source_sha256:
            self._add("integrity_mismatch", "The CSV checksum differs from the manifest.")

    def _loans(self, csv_bytes: bytes) -> None:
        try:
            text = csv_bytes.decode("utf-8")
            if re.search(r"\r(?!\n)", text):
                self._add("schema_invalid", "CSV records require LF or CRLF line endings.")
                return
            with _CSV_LOCK:
                # The stdlib cap counts characters. The scanner enforces UTF-8 bytes.
                previous = csv.field_size_limit()
                csv.field_size_limit(max(previous, len(text)))
                try:
                    self._records(csv.reader(io.StringIO(text, newline=""), strict=True))
                finally:
                    csv.field_size_limit(previous)
        except (UnicodeError, csv.Error):
            self._add("schema_invalid", "The CSV has invalid UTF-8 or record syntax.")

    def _records(self, records: Iterator[list[str]]) -> None:
        header = next(records, [])
        self._check_fields(iter(header))
        header_valid = tuple(header) == HEADER
        if not header_valid:
            self._add("schema_invalid", "The CSV header must match the required fields in order.")
        seen: set[str] = set()
        for row, values in enumerate(records, 2):
            if row - 1 > self.limits.max_rows:
                raise LimitExceeded("The CSV exceeds the loan record limit.")
            self._check_fields(iter(values))
            if not header_valid:
                continue
            if len(values) != len(HEADER):
                self._add("schema_invalid", "Wrong number of CSV fields.", row)
                continue
            self._loan(row, values, seen)

    def _loan(self, row: int, values: list[str], seen: set[str]) -> None:
        fields: dict[str, str | None] = {}
        for name, value in zip(HEADER, values, strict=True):
            if name in NUMERIC:
                self._check_numeric(value)
            if value or name == "segment":
                fields[name] = value or None
        identity = fields.get("loan_id")
        if identity is not None and OPAQUE_ID.fullmatch(identity):
            if identity in seen:
                self._add("duplicate_key", "Loan ID occurs more than once.", row, "loan_id")
            seen.add(identity)
        try:
            parsed = LoanRow.model_validate(fields)
        except ValidationError as error:
            self._schema_findings(LoanRow, error, row)
            return
        try:
            originated = date.fromisoformat(parsed.origination_date)
        except ValueError:
            self._add("invariant_failed", "Invalid origination date.", row, "origination_date")
            return
        if self.result.manifest and parsed.origination_date > self.result.manifest.as_of:
            self._add(
                "invariant_failed",
                "Origination follows the observation date.",
                row,
                "origination_date",
            )
        original = cents(parsed.original_principal)
        outstanding = cents(parsed.outstanding_principal)
        dpd = int(parsed.days_past_due)
        if original <= 0:
            self._add(
                "invalid_value", "Original principal must be positive.", row, "original_principal"
            )
        if outstanding > original:
            self._add(
                "invariant_failed",
                "Outstanding principal exceeds original principal.",
                row,
                "outstanding_principal",
            )
        if parsed.loan_status == "closed" and (outstanding or dpd):
            self._add(
                "invariant_failed",
                "Closed loans require zero principal and days past due.",
                row,
                "loan_status",
            )
        self.result.loans.append(
            Loan(
                parsed.loan_id,
                parsed.customer_id,
                original,
                outstanding,
                dpd,
                parsed.loan_status,
                originated,
                parsed.segment,
            )
        )

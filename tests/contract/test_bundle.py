import json

import pytest
from pydantic import ValidationError

from risklens.application.contracts import ParserLimits, canonical, sha256
from risklens.infrastructure.parser import BundleScanner
from risklens.infrastructure.sample import sample_bundle

MANIFEST, CSV = sample_bundle()
HEADER, FIRST, SECOND = CSV.splitlines(keepends=True)


def manifest_for(csv: bytes, **changes: object) -> bytes:
    values = json.loads(MANIFEST)
    values.update(source_sha256=sha256(csv), **changes)
    return canonical(values)


@pytest.mark.parametrize(
    ("manifest", "csv", "code"),
    [
        (b'{"snapshot_id":"a","snapshot_id":"b"}', CSV, "schema_invalid"),
        (b"\xff", CSV, "schema_invalid"),
        (manifest_for(CSV, unknown="secret-value"), CSV, "schema_invalid"),
        (manifest_for(CSV, as_of="2026-02-30"), CSV, "invariant_failed"),
        (manifest_for(CSV, currency="EUR"), CSV, "invariant_failed"),
        (manifest_for(CSV, synthetic=1), CSV, "invariant_failed"),
        (MANIFEST, CSV + b"\n", "integrity_mismatch"),
        (manifest_for(HEADER + FIRST * 2), HEADER + FIRST * 2, "duplicate_key"),
        (MANIFEST, CSV.replace(b",100.00,0,", b",,0,"), "missing_required"),
        (MANIFEST, CSV.replace(b",100.00,0,", b",1e2,0,"), "invalid_value"),
        (MANIFEST, CSV.replace(b",100.00,0,", b",-1,0,"), "invalid_value"),
        (MANIFEST, CSV.replace(b"2026-01-01", b"2027-01-01"), "invariant_failed"),
        (MANIFEST, CSV.replace(b"open", b"closed"), "invariant_failed"),
        (MANIFEST, CSV.replace(b"consumer", b" consumer"), "invalid_value"),
        (MANIFEST, b"\xef\xbb\xbf" + CSV, "schema_invalid"),
    ],
)
def test_FR_DQ_002_catalog(manifest: bytes, csv: bytes, code: str) -> None:
    scan = BundleScanner(ParserLimits()).scan(manifest, csv)
    assert scan.complete and scan.limit is None
    assert code in {finding.code for finding in scan.findings}
    assert all("secret-value" not in finding.message for finding in scan.findings)


def test_FR_DQ_002_ordinal_and_nullable_segment() -> None:
    csv = HEADER + FIRST.replace(b",consumer", b",") + SECOND
    parsed = BundleScanner(ParserLimits()).scan(manifest_for(csv), csv)
    assert parsed.complete and not parsed.findings
    assert parsed.loans[0].segment is None
    multiline = csv.replace(b",small-business", b',"bad\nsegment"') + FIRST
    parsed = BundleScanner(ParserLimits()).scan(manifest_for(multiline), multiline)
    assert [(item.row_number, item.field, item.code) for item in parsed.findings] == [
        (3, "segment", "invalid_value"),
        (4, "loan_id", "duplicate_key"),
    ]


@pytest.mark.parametrize(
    ("limit", "boundary", "accepted_csv", "exceeded_csv", "manifest_change"),
    [
        ("max_rows", 2, CSV, CSV + FIRST, {}),
        (
            "max_field_bytes",
            64,
            CSV,
            CSV,
            {"portfolio_name": "é" * 32},
        ),
        (
            "max_numeric_chars",
            6,
            CSV,
            CSV.replace(b"300.00", b"0300.00"),
            {},
        ),
    ],
)
def test_FR_DQ_003_parser_limits(limit, boundary, accepted_csv, exceeded_csv, manifest_change):
    limits = ParserLimits.model_validate({limit: boundary})
    passed = BundleScanner(limits).scan(manifest_for(accepted_csv, **manifest_change), accepted_csv)
    assert not passed.findings and not passed.limit
    if limit == "max_field_bytes":
        manifest_change = {"portfolio_name": "é" * 32 + "a"}
    exceeded = BundleScanner(limits).scan(
        manifest_for(exceeded_csv, **manifest_change), exceeded_csv
    )
    assert exceeded.limit and not exceeded.complete


def test_FR_DQ_003_diagnostic_cap_and_invalid_configuration() -> None:
    bad = CSV.replace(b",open,", b",unknown,")
    capped = BundleScanner(ParserLimits(max_collected_findings=2)).scan(manifest_for(bad), bad)
    assert len(capped.findings) == 2 and not capped.complete and not capped.limit
    complete = BundleScanner(ParserLimits(max_collected_findings=3)).scan(manifest_for(bad), bad)
    assert len(complete.findings) == 2 and complete.complete
    with pytest.raises(ValidationError):
        ParserLimits(max_rows=0)
    with pytest.raises(ValidationError):
        ParserLimits(max_input_bytes=10, max_manifest_bytes=11)

import json

import pytest
from pydantic import ValidationError

from risklens.application.contracts import (
    EvidenceRef,
    MetricLocator,
    ReportLocator,
    SnapshotLocator,
    SourceRowLocator,
)

LOCATORS = {
    "snapshot": SnapshotLocator(snapshot_id="snapshot-1"),
    "source_row": SourceRowLocator(snapshot_id="snapshot-1", row_number=2, field=None),
    "metric": MetricLocator(metrics_id="metrics-1", metric_key="total_exposure"),
    "validation_report": ReportLocator(report_id="report-1"),
}


@pytest.mark.parametrize("kind", LOCATORS)
@pytest.mark.parametrize("locator_kind", LOCATORS)
@pytest.mark.parametrize("representation", ["object", "dict", "json"])
def test_CT_003_requires_exact_kind_locator_pair(kind, locator_kind, representation):
    locator = LOCATORS[locator_kind]
    wire = {
        "evidence_id": "evidence-1",
        "run_id": "run-1",
        "kind": kind,
        "artifact_hash": "a" * 64,
        "locator": locator.model_dump(),
    }

    def parse() -> EvidenceRef:
        if representation == "json":
            return EvidenceRef.model_validate_json(json.dumps(wire))
        if representation == "object":
            return EvidenceRef.model_validate({**wire, "locator": locator})
        return EvidenceRef.model_validate(wire)

    if kind != locator_kind:
        with pytest.raises(ValidationError, match="Evidence kind does not match locator type"):
            parse()
    else:
        result = parse()
        assert type(result.locator) is type(locator)
        assert result.model_dump(mode="json") == wire

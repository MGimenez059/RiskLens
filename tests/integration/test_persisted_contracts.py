import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from risklens.application.contracts import AnalysisRequest, Metrics, OperationError, Result, sha256
from risklens.application.service import AnalysisService
from risklens.infrastructure.state import LocalState

FIXTURE = Path(__file__).parents[1] / "fixtures/m02-pre-correction.json"
TABLES = ("bundles", "runs", "snapshots", "imports", "artifacts", "events")


@pytest.fixture
def legacy(tmp_path):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    store = LocalState(tmp_path)
    with store._db() as db:
        for table in TABLES:
            rows = fixture["records"][table]
            placeholders = ",".join("?" for _ in rows[0])
            db.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
    for digest, contents in fixture["artifacts"].items():
        data = contents.encode("utf-8")
        assert sha256(data) == digest
        path = store.root / "artifacts" / "sha256" / digest
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return store, fixture["run_id"], fixture["producer_code_revision"]


def test_CT_018_pre_correction_result_opens_unchanged(legacy):
    store, run_id, revision = legacy
    service = AnalysisService(store)
    record = store.stored_run(run_id)
    result = service.get_run(run_id)
    assert result.run.code_revision == revision
    assert result.metrics.total_exposure == "400.00"
    assert {ref.kind for ref in result.evidence} == {
        "metric",
        "snapshot",
        "source_row",
        "validation_report",
    }
    assert service.execute(record.request) == result
    clone = service.new_analysis(run_id, "legacy-child")
    assert clone.validation.report_hash == result.validation.report_hash
    assert service.get_run(clone.run.run_id) == clone
    with store._db() as db:
        saved = db.execute("SELECT result FROM runs WHERE run_id=?", (run_id,)).fetchone()[0]
    assert saved == json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]["runs"][0][-1]


@pytest.mark.parametrize(
    "defect",
    ["locator_kind", "artifact_kind", "metric_identity", "terminal_time", "run_identity"],
)
def test_CT_003_CT_011_persisted_contract_violation_preserves_evidence(legacy, defect):
    store, run_id, _ = legacy
    with store._db() as db:
        raw = db.execute("SELECT result FROM runs WHERE run_id=?", (run_id,)).fetchone()[0]
        record = json.loads(raw)
        ref = next(ref for ref in record["evidence"] if ref["kind"] == "metric")
        if defect == "locator_kind":
            ref["kind"] = "snapshot"
        elif defect == "artifact_kind":
            ref["artifact_hash"] = record["validation"]["report_hash"]
        elif defect == "metric_identity":
            ref["locator"]["metrics_id"] = "different-result"
        elif defect == "terminal_time":
            record["run"]["completed_at"] = None
        else:
            record["run"]["run_id"] = "different-run"
        incompatible = json.dumps(record)
        db.execute("UPDATE runs SET result=? WHERE run_id=?", (incompatible, run_id))
    before = {path.name: path.read_bytes() for path in (store.root / "artifacts/sha256").iterdir()}
    service = AnalysisService(store)
    for operation in (
        lambda: service.get_run(run_id),
        lambda: service.resolve_evidence(run_id, ref["evidence_id"]),
    ):
        with pytest.raises(OperationError) as failure:
            operation()
        assert failure.value.code == "integrity_error"
    if defect == "locator_kind":
        assert service.list_runs()[0].run_id == run_id
    with store._db() as db:
        assert db.execute("SELECT result FROM runs WHERE run_id=?", (run_id,)).fetchone()[0] == (
            incompatible
        )
    assert {
        path.name: path.read_bytes() for path in (store.root / "artifacts/sha256").iterdir()
    } == (before)


def test_CT_004_CT_015_CT_016_cross_validation(legacy):
    store, run_id, _ = legacy
    result = AnalysisService(store).get_run(run_id)
    metrics = result.metrics.model_dump(mode="json")
    metrics["delinquency_exposure_rate"].update(
        status="unavailable", value=None, reason="zero_denominator"
    )
    with pytest.raises(ValidationError, match="disagree with their operands"):
        Metrics.model_validate_json(json.dumps(metrics))

    metadata = result.model_dump(mode="json")
    metadata["metrics"] = None
    metadata["validation"]["run_id"] = "different-run"
    with pytest.raises(ValidationError, match="does not match the run"):
        Result.model_validate_json(json.dumps(metadata))

    request = store.stored_run(run_id).request.model_dump(mode="json")
    request["configuration"]["parser_limits"].pop("max_rows")
    with pytest.raises(ValidationError, match="must supply all fields"):
        AnalysisRequest.model_validate_json(json.dumps(request))

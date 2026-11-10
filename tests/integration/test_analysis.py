import hashlib
import json
import shutil
from pathlib import Path

import pytest

from risklens.application.contracts import (
    AnalysisConfiguration,
    AnalysisRequest,
    OperationError,
    ParserLimits,
    canonical,
    sha256,
)
from risklens.application.service import AnalysisService
from risklens.infrastructure.sample import sample_bundle
from risklens.infrastructure.state import LocalState


def request(service, manifest, csv, *, import_key="import-1", analysis_key="analysis-1"):
    return AnalysisRequest(
        bundle_ref=service.register_bundle(manifest, csv),
        import_idempotency_key=import_key,
        analysis_idempotency_key=analysis_key,
        mode="deterministic_m02",
        requested_stages=("validate_portfolio", "calculate_metrics"),
        configuration=service.configuration,
        parent_run_id=None,
    )


def test_FR_DQ_001_sample_identity_and_restart(tmp_path: Path) -> None:
    service = AnalysisService(LocalState(tmp_path))
    manifest, csv = sample_bundle()
    original = request(service, manifest, csv)
    first = service.execute(original)
    assert first.run.status == "succeeded"
    assert first.metrics.total_exposure == "400.00"
    assert first.validation.source_sha256 == hashlib.sha256(csv).hexdigest()

    reopened = AnalysisService(LocalState(tmp_path))
    assert reopened.execute(original) == first
    assert reopened.get_run(first.run.run_id) == first
    assert [row.run_id for row in reopened.list_runs()] == [first.run.run_id]
    assert reopened.resolve_evidence(first.run.run_id, first.metrics.evidence_ids[0])
    again = reopened.new_analysis(first.run.run_id, "analysis-2")
    assert again.run.parent_run_id == first.run.run_id
    assert again.run.run_id != first.run.run_id
    assert again.metrics.evidence_ids != first.metrics.evidence_ids
    assert again.metrics_hash == first.metrics_hash

    changed = request(reopened, manifest + b" ", csv)
    assert reopened.execute(changed).run.status == "conflict"
    changed_owner = json.loads(manifest)
    changed_owner["portfolio_id"] = "someone-else"
    collision = request(
        reopened,
        json.dumps(changed_owner).encode(),
        csv,
        import_key="other-import",
        analysis_key="other-analysis",
    )
    assert reopened.execute(collision).validation.error_code == "identity_conflict"
    assert reopened.get_run(first.run.run_id) == first


def test_FR_DQ_002_invalid_manifest_blocks_metrics(tmp_path: Path) -> None:
    service = AnalysisService(LocalState(tmp_path))
    _, csv = sample_bundle()
    result = service.execute(request(service, b'{"schema_version":"1.0"}', csv))
    assert result.run.status == "rejected"
    assert result.metrics is None
    assert result.validation.report_complete
    assert "missing_required" in {finding.code for finding in result.validation.findings}


@pytest.mark.parametrize("limit", ["max_input_bytes", "max_manifest_bytes"])
def test_FR_DQ_003_byte_caps_and_incomplete_hash(tmp_path, limit) -> None:
    manifest, csv = sample_bundle()
    config = AnalysisConfiguration(
        parser_limits=ParserLimits.model_validate(
            {
                "max_manifest_bytes": len(manifest),
                limit: len(manifest) if limit == "max_manifest_bytes" else len(manifest) + len(csv),
            }
        )
    )
    service = AnalysisService(LocalState(tmp_path), config)
    if limit == "max_input_bytes":
        bigger_manifest, bigger_csv = manifest, csv + b" "
    else:
        bigger_manifest, bigger_csv = manifest + b" ", csv
    rejected = service.execute(request(service, bigger_manifest, bigger_csv))
    assert rejected.run.status == "limit_failed"
    assert rejected.run.input_hash is None and rejected.validation.source_sha256 is None
    assert not rejected.validation.report_complete
    result = service.execute(request(service, manifest, csv))
    assert result.run.status == "succeeded"


def test_FR_DQ_003_capped_diagnostics_never_produce_metrics(tmp_path) -> None:
    config = AnalysisConfiguration(parser_limits=ParserLimits(max_collected_findings=1))
    service = AnalysisService(LocalState(tmp_path), config)
    manifest, csv = sample_bundle()
    changed = csv.replace(b",open,", b",invalid,")
    payload = json.loads(manifest)
    payload["source_sha256"] = sha256(changed)
    result = service.execute(request(service, canonical(payload), changed))
    assert result.run.status == "rejected" and result.metrics is None
    assert len(result.validation.findings) == 1 and not result.validation.report_complete


def test_NFR_REL_002_semantic_hash_ignores_row_order_and_raw_encoding(tmp_path) -> None:
    first_service = AnalysisService(LocalState(tmp_path / "first"))
    second_service = AnalysisService(LocalState(tmp_path / "second"))
    manifest, csv = sample_bundle()
    header, first, second = csv.splitlines(keepends=True)
    alternate_csv = (header + second + first).replace(b"\n", b"\r\n")
    alternate_manifest = json.loads(manifest)
    alternate_manifest["source_sha256"] = sha256(alternate_csv)
    left = first_service.execute(request(first_service, manifest, csv))
    right = second_service.execute(
        request(second_service, canonical(alternate_manifest), alternate_csv)
    )
    assert left.run.input_hash != right.run.input_hash
    assert left.run.canonical_input_hash == right.run.canonical_input_hash
    assert left.metrics_hash == right.metrics_hash


def test_FR_OBS_001_versions_events_and_scoped_evidence(tmp_path) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    manifest, csv = sample_bundle()
    command = request(service, manifest, csv)
    result = service.execute(command)
    run = result.run
    assert result.configuration == service.configuration and run.code_revision
    assert result.configuration.config_hash == run.config_hash
    assert result.configuration.parser_limits.max_rows == 50_000
    assert run.canonical_input_hash and result.validation.report_hash
    assert service.execute(command) == result
    assert [event.event_type for event in store.events(run.run_id)] == [
        "operation_started",
        "validation_completed",
        "metrics_completed",
        "publication_committed",
        "replay_returned",
    ]
    clone = service.new_analysis(run.run_id, "clone")
    assert clone.validation.import_id == result.validation.import_id
    assert clone.validation.report_hash == result.validation.report_hash
    assert service.resolve_evidence(clone.run.run_id, result.evidence[0].evidence_id) is None
    source = next(ref for ref in result.evidence if ref.kind == "source_row")
    resolved = service.resolve_evidence(run.run_id, source.evidence_id)
    assert resolved.reference == source
    assert sha256(resolved.artifact) == run.input_hash
    assert "provider" not in run.model_dump()


def test_CT_018_publication_metadata_commits_with_its_artifact(tmp_path) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    result = service.execute(request(service, *sample_bundle()))
    run = result.run
    refs = store.artifact_refs(run.run_id)
    assert {ref.publication.publication_id for ref in refs.values()} and len(
        {ref.publication.publication_id for ref in refs.values()}
    ) == 1
    for ref in refs.values():
        assert ref.publication.expected_run_revision == run.revision - 1
        assert ref.publication.byte_length == len(store.read(ref.sha256))
        assert ref.publication.publication_state == "committed"
    key = next(iter(refs))
    inconsistent = refs[key].publication.model_copy(update={"expected_run_revision": run.revision})
    with store._db() as db:
        db.execute(
            "UPDATE artifact_publications SET metadata=? WHERE run_id=? AND artifact_id=?",
            (inconsistent.model_dump_json(), run.run_id, key),
        )
    with pytest.raises(OperationError) as failure:
        service.get_run(run.run_id)
    assert failure.value.code == "integrity_error"


class Interrupt(BaseException):
    pass


@pytest.mark.parametrize("boundary", ["created", "before_publish", "before_commit", "after_commit"])
def test_FR_OBS_003_publication_and_restart(tmp_path, monkeypatch, boundary) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    manifest, csv = sample_bundle()
    command = request(service, manifest, csv)
    before = store.finish

    def crash(*args, **kwargs):
        if boundary == "after_commit":
            before(*args, **kwargs)
        raise Interrupt

    if boundary == "created":
        start = store.start

        def crash_on_start(*args):
            if args[-1] is not None:
                raise Interrupt
            start(*args)

        monkeypatch.setattr(store, "start", crash_on_start)
    else:
        target = "publish" if boundary == "before_publish" else "finish"
        monkeypatch.setattr(store, target, crash)
    with pytest.raises(Interrupt):
        service.execute(command)
    reopened = AnalysisService(LocalState(tmp_path))
    [interrupted] = reopened.list_runs()
    if boundary == "after_commit":
        assert interrupted.status == "succeeded"
    else:
        assert interrupted.status == ("created" if boundary == "created" else "running")
        assert reopened.get_run(interrupted.run_id).metrics is None
    result = reopened.resume(interrupted.run_id)
    assert result.run.status == "succeeded"
    assert result.run.run_id == interrupted.run_id
    assert reopened.execute(command) == result
    assert len(reopened.list_runs()) == 1


def test_CT_016_resume_retains_the_original_import_key(tmp_path, monkeypatch) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    manifest, csv = sample_bundle()
    original = request(service, manifest, csv)
    with monkeypatch.context() as patch:

        def crash(*args, **kwargs):
            raise Interrupt

        patch.setattr(store, "finish", crash)
        with pytest.raises(Interrupt):
            service.execute(original)
    resumed = service.execute(original.model_copy(update={"import_idempotency_key": "different"}))
    assert resumed.validation.import_idempotency_key == original.import_idempotency_key
    assert service.get_run(resumed.run.run_id) == resumed


@pytest.mark.parametrize("damage", ["missing", "modified"])
def test_FR_OBS_003_damaged_artifact_and_whole_state_cleanup(tmp_path, damage) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    manifest, csv = sample_bundle()
    command = request(service, manifest, csv)
    result = service.execute(command)
    run_id = result.run.run_id
    metrics_ref = next(ref for ref in store.artifact_refs(run_id).values() if ref.kind == "metrics")
    path = store.root / "artifacts" / "sha256" / metrics_ref.sha256
    if damage == "modified":
        path.write_bytes(b"unexpected")
    else:
        path.unlink()
    reopened = AnalysisService(LocalState(tmp_path))
    with pytest.raises(OperationError, match="integrity"):
        reopened.execute(command)
    assert reopened.list_runs() == [result.run]
    assert store.root.resolve() == tmp_path.resolve() / ".risklens/state"
    shutil.rmtree(store.root)
    assert not AnalysisService(LocalState(tmp_path)).list_runs()


def test_FR_OBS_003_persistence_failure_never_reports_success(tmp_path, monkeypatch) -> None:
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    manifest, csv = sample_bundle()
    command = request(service, manifest, csv)

    def fail(_data):
        raise OperationError("persistence_failed")

    monkeypatch.setattr(store, "publish", fail)
    result = service.execute(command)
    assert result.run.status == "failed" and result.metrics is None
    assert result.run.errors[0].code == "persistence_failed"
    assert service.get_run(result.run.run_id).run == result.run


def test_FR_DQ_001_changed_configuration_and_separate_keys(tmp_path) -> None:
    service = AnalysisService(LocalState(tmp_path))
    manifest, csv = sample_bundle()
    command = request(service, manifest, csv)
    original = service.execute(command)
    alternate = command.model_copy(
        update={
            "configuration": AnalysisConfiguration(parser_limits=ParserLimits(max_rows=3)),
        }
    )
    assert service.execute(alternate).validation.error_code == "idempotency_conflict"
    new_analysis = alternate.model_copy(update={"analysis_idempotency_key": "other-key"})
    assert service.execute(new_analysis).validation.error_code == "idempotency_conflict"
    new_import = new_analysis.model_copy(
        update={
            "analysis_idempotency_key": "fresh-analysis",
            "import_idempotency_key": "fresh-import",
        }
    )
    assert service.execute(new_import).metrics_hash == original.metrics_hash
    assert service.execute(command) == original


def test_FR_DQ_003_wide_aggregate_and_large_field(tmp_path) -> None:
    service = AnalysisService(LocalState(tmp_path))
    manifest, csv = sample_bundle()
    amount = b"9" * 24
    wide = csv.replace(b"100.00", amount).replace(b"300.00", amount)
    values = json.loads(manifest)
    values["source_sha256"] = sha256(wide)
    result = service.execute(request(service, canonical(values), wide))
    assert result.metrics.total_exposure == f"{2 * int(amount)}.00"
    too_wide = csv.replace(b"consumer", b"a" * 150_000)
    overflow = service.execute(
        request(
            service,
            manifest,
            too_wide,
            import_key="wide-import",
            analysis_key="wide-analysis",
        )
    )
    assert overflow.run.status == "limit_failed" and overflow.metrics is None
    assert overflow.validation.error_code == "resource_limit"


def test_NFR_SEC_001_state_path_confinement(tmp_path) -> None:
    store = LocalState(tmp_path)
    with pytest.raises(OperationError) as escaped:
        store._path("../outside")
    assert escaped.value.code == "persistence_failed"
    with pytest.raises(OperationError) as bad_hash:
        store.read("../outside")
    assert bad_hash.value.code == "integrity_error"

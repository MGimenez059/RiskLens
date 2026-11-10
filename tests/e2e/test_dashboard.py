import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from risklens.application.contracts import AnalysisRequest, canonical, sha256
from risklens.application.service import AnalysisService
from risklens.infrastructure.sample import sample_bundle
from risklens.infrastructure.state import LocalState

APP = Path(__file__).resolve().parents[2] / "src/risklens/presentation/dashboard.py"


def test_FR_UI_001_sample_rerun_and_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.button(key="sample").click().run()
    assert not app.exception
    assert [metric.value for metric in app.metric] == ["$400.00", "2", "2", "50.00%", "75.00%"]
    selected = app.selectbox[0].value
    app.run()
    assert len(app.selectbox[0].options) == 1
    app.button(key="new_analysis").click().run()
    assert app.selectbox[0].value != selected
    assert len(app.selectbox[0].options) == 2
    reopened = AppTest.from_file(str(APP), default_timeout=15).run()
    reopened.selectbox[0].select(selected).run()
    assert reopened.selectbox[0].value == selected
    assert reopened.metric[0].value == "$400.00"
    assert not reopened.exception


def test_FR_UI_001_manual_rejected_and_empty(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    manifest, csv = sample_bundle()
    app.file_uploader(key="csv").upload("portfolio.csv", csv, "text/csv")
    app.file_uploader(key="manifest").upload("manifest.json", b"{}", "application/json")
    app.run().button(key="upload").click().run()
    assert not app.exception and not app.metric
    assert "rejected" in app.error[0].value.lower()
    assert "missing_required" in app.dataframe[0].value["Code"].tolist()

    values = json.loads(manifest)
    empty = csv.splitlines(keepends=True)[0]
    values["snapshot_id"] = "empty"
    values["source_sha256"] = sha256(empty)
    app.file_uploader(key="csv").upload("portfolio.csv", empty, "text/csv")
    app.file_uploader(key="manifest").upload(
        "manifest.json",
        canonical(values),
        "application/json",
    )
    app.run().button(key="upload").click().run()
    assert not app.exception
    assert app.metric[0].value == "$0.00"
    assert app.metric[-1].value == "Unavailable"


def test_FR_UI_001_resume_refreshes_history_status_without_changing_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = LocalState(tmp_path)
    service = AnalysisService(store)
    bundle_ref = service.register_bundle(*sample_bundle())
    request = AnalysisRequest(
        bundle_ref=bundle_ref,
        import_idempotency_key="resume-import",
        analysis_idempotency_key="resume-analysis",
        mode="deterministic_m02",
        requested_stages=("validate_portfolio", "calculate_metrics"),
        configuration=service.configuration,
        parent_run_id=None,
    )

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    with monkeypatch.context() as patch:
        patch.setattr(store, "finish", interrupt)
        with pytest.raises(KeyboardInterrupt):
            service.execute(request)

    app = AppTest.from_file(str(APP), default_timeout=15).run()
    running = app.selectbox[0]
    assert "Running" in running.options[0]
    run_id = running.value
    app.button(key="resume").click().run()
    assert not app.exception
    finished = app.selectbox[0]
    assert "Succeeded" in finished.options[0]
    assert finished.id != running.id
    assert finished.value == run_id
    assert app.metric[0].value == "$400.00"

import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

from risklens.application.contracts import canonical, sha256
from risklens.infrastructure.sample import sample_bundle

APP = Path(__file__).resolve().parents[2] / "src/risklens/presentation/dashboard.py"


def test_FR_UI_001_sample_rerun_and_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.button(key="sample").click().run()
    assert not app.exception
    assert [metric.value for metric in app.metric] == ["$400.00", "2", "2", "50.00%", "75.00%"]
    selected = app.selectbox(key="history").value
    app.run()
    assert len(app.selectbox(key="history").options) == 1
    app.button(key="new_analysis").click().run()
    assert app.selectbox(key="history").value != selected
    assert len(app.selectbox(key="history").options) == 2
    reopened = AppTest.from_file(str(APP), default_timeout=15).run()
    reopened.selectbox(key="history").select(selected).run()
    assert reopened.selectbox(key="history").value == selected
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

"""Local Streamlit entry point for the deterministic M02 workflow."""

from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import streamlit as st

from risklens.application.contracts import (
    SAFE_MESSAGES,
    AnalysisRequest,
    Metrics,
    OperationError,
    Result,
    RunManifest,
    sha256,
)
from risklens.application.service import TERMINAL, AnalysisService
from risklens.domain.metrics import MetricValue
from risklens.infrastructure.sample import sample_bundle
from risklens.infrastructure.state import LocalState

_STATUS = {
    "created": "Created",
    "running": "Running",
    "succeeded": "Succeeded",
    "rejected": "Rejected",
    "conflict": "Conflict",
    "limit_failed": "Limit exceeded",
    "failed": "Failed",
}
_REASONS = {"no_eligible_population": "No eligible open loans", "zero_denominator": "Zero exposure"}


@st.cache_resource
def _service(workspace: Path) -> AnalysisService:
    return AnalysisService(LocalState(workspace))


def _submit(service: AnalysisService, manifest: bytes, csv: bytes) -> Result:
    bundle_ref = service.register_bundle(manifest, csv)
    config = service.configuration
    return service.execute(
        AnalysisRequest(
            bundle_ref=bundle_ref,
            import_idempotency_key=sha256(f"{bundle_ref}/{config.parser_config_hash}".encode()),
            analysis_idempotency_key=sha256(f"{bundle_ref}/{config.config_hash}".encode()),
            mode="deterministic_m02",
            requested_stages=("validate_portfolio", "calculate_metrics"),
            configuration=config,
            parent_run_id=None,
        )
    )


def _history_changed() -> None:
    st.query_params["run"] = st.session_state["history"]


def _history(runs: list[RunManifest]) -> str | None:
    st.sidebar.subheader("Run history")
    if not runs:
        st.sidebar.caption("Completed and interrupted analyses will appear here.")
        return None
    labels = {
        run.run_id: (
            f"{run.created_at[5:16].replace('T', ' ')} · {_STATUS[run.status]} · {run.run_id[:4]}"
        )
        for run in runs
    }
    selected = st.query_params.get("run", runs[0].run_id)
    if selected not in labels:
        selected = runs[0].run_id
    if st.session_state.get("history") != selected:
        st.session_state["history"] = selected
    return st.sidebar.selectbox(
        "Saved analysis",
        list(labels),
        key="history",
        format_func=labels.__getitem__,
        on_change=_history_changed,
        help="Times are in UTC.",
    )


def _money(value: str) -> str:
    whole, fraction = value.split(".")
    return f"${int(whole):,}.{fraction}"


def _percent(value: MetricValue) -> str:
    return f"{Decimal(value.value):.2%}" if value.value is not None else "Unavailable"


def _ratio(label: str, value: MetricValue) -> None:
    st.metric(label, _percent(value))
    unit = "USD" if value.unit == "exposure_ratio" else "loans"
    st.caption(f"{value.numerator} / {value.denominator} {unit}")
    if value.reason:
        st.caption(_REASONS[value.reason])


def _show_metrics(metrics: Metrics) -> None:
    exposure, loans, opened = st.columns([2, 1, 1])
    exposure.metric("Outstanding principal", _money(metrics.total_exposure))
    loans.metric("Loans", f"{metrics.loan_count:,}")
    opened.metric("Open loans", f"{metrics.open_loan_count:,}")

    st.subheader("Delinquency")
    count, balance = st.columns(2)
    with count:
        _ratio("By loan count", metrics.delinquency_count_rate)
    with balance:
        _ratio("By outstanding principal", metrics.delinquency_exposure_rate)
    if not metrics.loan_count:
        st.info("This snapshot contains no loans.")
        return

    st.subheader("Concentration")
    tabs = st.tabs(["By borrower", "By segment"])
    for dimension, tab in zip(("borrower", "segment"), tabs, strict=True):
        with tab:
            rows = [
                {
                    "Group": group.group_id or "Unspecified (blank)",
                    "Exposure": _money(group.group_exposure),
                    "Share": _percent(group.share),
                    "Numerator (USD)": group.share.numerator,
                    "Denominator (USD)": group.share.denominator,
                    "Reason": _REASONS.get(group.share.reason or "", ""),
                }
                for group in metrics.concentration
                if group.dimension == dimension
            ]
            st.dataframe(rows, hide_index=True, width="stretch")


def _show_result(result: Result) -> None:
    run = result.run
    validation = result.validation
    metrics = result.metrics
    state = f"Analysis {_STATUS[run.status].lower()} · Revision {run.revision}"
    if metrics:
        state = f"{metrics.as_of} · {metrics.currency} · {state}"
    if validation:
        label = (
            "limit exceeded" if validation.disposition == "limit_failed" else validation.disposition
        )
        state = f"{state} · Import {label}"
    st.caption(state)
    if metrics is not None:
        _show_metrics(metrics)
    if validation and validation.error_code:
        code = validation.error_code
        st.error(f"{_STATUS[run.status]} ({code}). {SAFE_MESSAGES[code]}")
        if validation.findings:
            st.subheader("Validation report")
            st.dataframe(
                [
                    {
                        "Code": finding.code,
                        "Location": (
                            f"Record {finding.row_number}" if finding.row_number else "File"
                        )
                        + (f" / {finding.field}" if finding.field else ""),
                        "Message": finding.summary,
                    }
                    for finding in validation.findings
                ],
                hide_index=True,
                width="stretch",
            )
        if not validation.report_complete:
            st.warning("The validation scan ended at a configured limit. The report is incomplete.")
    for error in run.errors:
        st.error(f"{error.message} ({error.code})")
    with st.expander("Run provenance"):
        st.text(f"Run ID  {run.run_id}")
        if run.parent_run_id:
            st.text(f"Parent run  {run.parent_run_id}")
        if validation and validation.portfolio_id:
            st.text(f"Portfolio  {validation.portfolio_id}")
        if run.input_hash:
            st.code(run.input_hash, language=None)
            st.caption("SHA-256 of the framed input bundle")
        if result.metrics_hash:
            st.code(result.metrics_hash, language=None)
            st.caption("SHA-256 of the metric values and exact operands")


def _inputs(service: AnalysisService) -> None:
    st.sidebar.divider()
    st.sidebar.subheader("Input bundle")
    if st.sidebar.button("Analyze sample", key="sample", type="primary", width="stretch"):
        manifest, csv = sample_bundle()
        _open_result(_submit(service, manifest, csv))
    with st.sidebar.expander("Upload your own bundle"):
        st.caption("Use a synthetic USD portfolio and its matching manifest.")
        csv_file = st.file_uploader("Loan CSV", type="csv", key="csv")
        manifest_file = st.file_uploader("JSON manifest", type="json", key="manifest")
        analyze = st.button(
            "Analyze",
            key="upload",
            disabled=csv_file is None or manifest_file is None,
        )
        if analyze and csv_file is not None and manifest_file is not None:
            _open_result(_submit(service, manifest_file.getvalue(), csv_file.getvalue()))


def _open_result(result: Result) -> None:
    st.query_params["run"] = result.run.run_id
    st.rerun()


def _run_actions(service: AnalysisService, run: RunManifest) -> None:
    if run.status not in TERMINAL:
        st.info("This analysis was interrupted. Resume it using the original request.")
        if st.button("Resume analysis", key="resume"):
            _open_result(service.resume(run.run_id))
    elif run.input_hash and st.button("New analysis", key="new_analysis"):
        pending = f"new_key_{run.run_id}"
        key = st.session_state.setdefault(pending, uuid4().hex)
        result = service.new_analysis(run.run_id, key)
        del st.session_state[pending]
        _open_result(result)


def main() -> None:
    st.set_page_config(page_title="RiskLens | Portfolio analysis", layout="wide")
    st.sidebar.title("RiskLens")
    st.sidebar.caption("Local workspace · Synthetic data")
    st.title("Portfolio analysis")
    try:
        service = _service(Path.cwd())
        run_id = _history(service.list_runs())
        _inputs(service)
        if run_id is None:
            st.subheader("Inspect a loan portfolio")
            st.write(
                "Analyze the included sample to see exposure, delinquency and concentration. "
                "You can also upload a loan CSV and its matching JSON manifest."
            )
            return
        result = service.get_run(run_id)
        _show_result(result)
        _run_actions(service, result.run)
    except OperationError as error:
        st.error(f"{error} ({error.code})")


if __name__ == "__main__":
    main()

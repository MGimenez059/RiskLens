"""Negative document fixtures for owner-approved specification boundaries."""

from pathlib import Path
from shutil import copytree

import pytest

from scripts.check_baseline import (
    ROOT,
    acceptance_and_identity_errors,
    contract_traceability_errors,
    milestone_errors,
)


@pytest.fixture
def snapshot(tmp_path: Path) -> Path:
    copytree(ROOT / "docs", tmp_path / "docs")
    return tmp_path


def change(snapshot: Path, relative: str, original: str, replacement: str) -> None:
    path = snapshot / relative
    content = path.read_text(encoding="utf-8")
    assert original in content
    path.write_text(content.replace(original, replacement, 1), encoding="utf-8")


def test_reject_m02_ai_requirement(snapshot: Path) -> None:
    change(
        snapshot,
        "docs/01-requirements/functional-requirements.md",
        "## FR-AI-001: Generate grounded executive insights\n"
        "- Status: Proposed\n- Priority: P1\n- Applicability: M03",
        "## FR-AI-001: Generate grounded executive insights\n"
        "- Status: Proposed\n- Priority: P1\n- Applicability: M02",
    )
    assert any("FR-AI-001" in error for error in milestone_errors(snapshot))


def test_reject_active_default_metric(snapshot: Path) -> None:
    change(
        snapshot,
        "docs/02-domain/data-contracts.md",
        "| delinquency_count_rate; delinquency_exposure_rate |",
        "| delinquency_count_rate; delinquency_exposure_rate; default_rate |",
    )
    assert any("default_rate" in error for error in milestone_errors(snapshot))


def test_reject_blanket_acceptance(snapshot: Path) -> None:
    change(snapshot, "docs/02-domain/data-contracts.md", "Status: Proposed", "Status: Accepted")
    assert any("blanket Accepted" in error for error in acceptance_and_identity_errors(snapshot))


def test_reject_missing_new_contract_trace(snapshot: Path) -> None:
    path = snapshot / "docs/05-testing/traceability.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line for line in lines if not line.startswith("| CT-020 |")) + "\n",
        encoding="utf-8",
    )
    assert any("missing CT-020" in error for error in contract_traceability_errors(snapshot))


def test_reject_composite_only_snapshot_identity(snapshot: Path) -> None:
    change(
        snapshot,
        "docs/02-domain/business-rules.md",
        "snapshot_id is globally unique with exactly one portfolio_id owner",
        "identity is portfolio_id plus snapshot_id",
    )
    assert acceptance_and_identity_errors(snapshot)


def test_reject_m02_pending_review_stage(snapshot: Path) -> None:
    change(
        snapshot,
        "docs/02-domain/data-contracts.md",
        "Exactly validate_portfolio, calculate_metrics.",
        "Exactly validate_portfolio, calculate_metrics, human_review.",
    )
    assert any("human-review" in error for error in milestone_errors(snapshot))


def test_reject_m03_review_on_synthesis_failure(snapshot: Path) -> None:
    change(
        snapshot,
        "docs/03-architecture/graph-spec.md",
        "failure to finalize in M03 with partial quality; review_gate only in enabled M04 mode.",
        "failure to review_gate with partial quality.",
    )
    assert any("generate_insights" in error for error in milestone_errors(snapshot))

"""Repository checks only. Product acceptance tests remain unimplemented."""

from scripts.check_baseline import (
    ROOT,
    acceptance_and_identity_errors,
    contract_traceability_errors,
    domain_boundary_errors,
    identifier_errors,
    link_errors,
    metadata_and_style_errors,
    milestone_errors,
    traceability_errors,
)


def test_document_metadata_and_writing_policy() -> None:
    assert metadata_and_style_errors(ROOT) == []


def test_local_document_links_resolve() -> None:
    assert link_errors(ROOT) == []


def test_requirement_traceability_is_complete() -> None:
    assert traceability_errors(ROOT) == []


def test_domain_import_boundaries() -> None:
    assert domain_boundary_errors(ROOT) == []


def test_specification_identifiers_resolve() -> None:
    assert identifier_errors(ROOT) == []


def test_milestone_and_per_id_metadata() -> None:
    assert milestone_errors(ROOT) == []


def test_all_contracts_have_requirement_traceability() -> None:
    assert contract_traceability_errors(ROOT) == []


def test_mixed_acceptance_and_snapshot_identity() -> None:
    assert acceptance_and_identity_errors(ROOT) == []

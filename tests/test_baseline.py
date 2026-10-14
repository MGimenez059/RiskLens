"""Repository checks only. Product acceptance tests remain unimplemented."""

from scripts.check_baseline import (
    ROOT,
    domain_boundary_errors,
    identifier_errors,
    link_errors,
    metadata_and_style_errors,
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

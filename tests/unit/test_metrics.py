from datetime import date

import pytest

from risklens.domain.metrics import Loan, calculate, ratio


def loan(
    identity: str,
    cents: int,
    dpd: int,
    status: str = "open",
    segment: str | None = None,
) -> Loan:
    return Loan(identity, identity, max(1, cents), cents, dpd, status, date(2026, 1, 1), segment)


def test_FR_RISK_001_sample_metrics_and_group_sums() -> None:
    result = calculate([loan("a", 10_000, 0), loan("b", 30_000, 5, segment="retail")])
    assert result.total_exposure == "400.00"
    assert result.loan_count == result.open_loan_count == 2
    assert result.delinquency_count_rate.value == "0.5000"
    exposure = result.delinquency_exposure_rate
    assert (exposure.value, exposure.numerator, exposure.denominator) == (
        "0.7500",
        "300.00",
        "400.00",
    )
    assert [(group.group_id, group.group_exposure) for group in result.concentration] == [
        ("a", "100.00"),
        ("b", "300.00"),
        (None, "100.00"),
        ("retail", "300.00"),
    ]


@pytest.mark.parametrize(
    ("n", "d", "expected"), [(1, 3, "0.3333"), (1, 32, "0.0312"), (3, 32, "0.0938")]
)
def test_FR_RISK_001_exact_operands(n: int, d: int, expected: str) -> None:
    value = ratio(n, d, "count_ratio", "BR-RISK-002")
    assert (value.numerator, value.denominator, value.value) == (str(n), str(d), expected)


def test_FR_RISK_001_empty_closed_and_open_zero() -> None:
    empty = calculate([])
    assert empty.total_exposure == "0.00" and not empty.concentration
    closed = calculate([loan("closed", 0, 0, "closed")])
    assert closed.loan_count == 1 and closed.open_loan_count == 0
    assert closed.delinquency_count_rate.reason == "no_eligible_population"
    assert closed.delinquency_exposure_rate.reason == "no_eligible_population"
    zeros = calculate([loan("a", 0, 1), loan("b", 0, 0)])
    assert zeros.delinquency_count_rate.value == "0.5000"
    assert zeros.delinquency_exposure_rate.reason == "zero_denominator"
    assert all(group.share.reason == "zero_denominator" for group in zeros.concentration)

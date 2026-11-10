"""Exact portfolio arithmetic for a validated USD snapshot."""

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from typing import Literal

Unit = Literal["count_ratio", "exposure_ratio"]
Reason = Literal["zero_denominator", "no_eligible_population"]
Dimension = Literal["borrower", "segment"]


@dataclass(frozen=True, slots=True)
class Loan:
    loan_id: str
    customer_id: str
    original_cents: int
    outstanding_cents: int
    days_past_due: int
    loan_status: str
    origination_date: date
    segment: str | None


@dataclass(frozen=True, slots=True)
class MetricValue:
    status: Literal["available", "unavailable"]
    value: str | None
    numerator: str
    denominator: str
    unit: Unit
    reason: Reason | None
    rule_id: str


@dataclass(frozen=True, slots=True)
class GroupShare:
    dimension: Dimension
    group_id: str | None
    group_exposure: str
    share: MetricValue


@dataclass(frozen=True, slots=True)
class Totals:
    loan_count: int
    open_loan_count: int
    total_exposure: str
    delinquency_count_rate: MetricValue
    delinquency_exposure_rate: MetricValue
    concentration: list[GroupShare]


def usd(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def cents(amount: str) -> int:
    whole, _, fraction = amount.partition(".")
    return int(whole) * 100 + int(fraction.ljust(2, "0"))


def ratio(
    numerator: int,
    denominator: int,
    unit: Unit,
    rule_id: str,
    *,
    empty_reason: Reason = "zero_denominator",
) -> MetricValue:
    if not 0 <= numerator <= denominator:
        raise ValueError("Invalid ratio operands")
    display = str if unit == "count_ratio" else usd
    if denominator == 0:
        return MetricValue(
            "unavailable",
            None,
            display(numerator),
            display(denominator),
            unit,
            empty_reason,
            rule_id,
        )
    quotient, remainder = divmod(numerator * 10_000, denominator)
    if 2 * remainder > denominator or (2 * remainder == denominator and quotient % 2):
        quotient += 1
    return MetricValue(
        "available",
        f"{quotient // 10_000}.{quotient % 10_000:04d}",
        display(numerator),
        display(denominator),
        unit,
        None,
        rule_id,
    )


def calculate(loans: Iterable[Loan]) -> Totals:
    loan_count = open_count = exposure = delinquent_count = delinquent_cents = 0
    groups: dict[tuple[Dimension, str | None], int] = defaultdict(int)
    for loan in loans:
        loan_count += 1
        exposure += loan.outstanding_cents
        groups["borrower", loan.customer_id] += loan.outstanding_cents
        groups["segment", loan.segment] += loan.outstanding_cents
        if loan.loan_status == "open":
            open_count += 1
            if loan.days_past_due > 0:
                delinquent_count += 1
                delinquent_cents += loan.outstanding_cents

    empty_reason: Reason = "zero_denominator" if open_count else "no_eligible_population"
    concentration = [
        GroupShare(
            dimension,
            group,
            usd(groups[dimension, group]),
            ratio(
                groups[dimension, group],
                exposure,
                "exposure_ratio",
                "BR-RISK-003",
            ),
        )
        for dimension, group in sorted(groups, key=lambda key: (key[0], key[1] or ""))
    ]
    return Totals(
        loan_count,
        open_count,
        usd(exposure),
        ratio(
            delinquent_count, open_count, "count_ratio", "BR-RISK-002", empty_reason=empty_reason
        ),
        ratio(
            delinquent_cents,
            exposure,
            "exposure_ratio",
            "BR-RISK-002",
            empty_reason=empty_reason,
        ),
        concentration,
    )

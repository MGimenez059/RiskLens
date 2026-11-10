"""Decode an immutable normalized snapshot for a deliberate new analysis."""

from datetime import date
from typing import Literal

from risklens.application.contracts import DTO, Amount, Count, DateText, Id, Text
from risklens.domain.metrics import Loan, cents


class SnapshotLoan(DTO):
    loan_id: Id
    customer_id: Id
    original_principal: Amount
    outstanding_principal: Amount
    days_past_due: Count
    loan_status: Literal["open", "closed"]
    origination_date: DateText
    segment: Id | None


class SnapshotPayload(DTO):
    schema_version: Literal["1.0"]
    snapshot_id: Id
    portfolio_id: Id
    portfolio_name: Text
    as_of: DateText
    currency: Literal["USD"]
    synthetic: Literal[True]
    generator_version: Text
    seed: Count
    loans: list[SnapshotLoan]

    def domain_loans(self) -> list[Loan]:
        return [
            Loan(
                loan.loan_id,
                loan.customer_id,
                cents(loan.original_principal),
                cents(loan.outstanding_principal),
                loan.days_past_due,
                loan.loan_status,
                date.fromisoformat(loan.origination_date),
                loan.segment,
            )
            for loan in self.loans
        ]

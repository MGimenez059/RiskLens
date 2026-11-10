"""Versioned controlled synthetic data for the bundled sample."""

from risklens.application.contracts import canonical, sha256

_CSV = (
    b"loan_id,customer_id,original_principal,outstanding_principal,days_past_due,"
    b"loan_status,origination_date,segment\n"
    b"sample-loan-01,sample-borrower-01,100.00,100.00,0,open,2026-01-01,consumer\n"
    b"sample-loan-02,sample-borrower-02,300.00,300.00,5,open,2026-01-01,small-business\n"
)


def sample_bundle() -> tuple[bytes, bytes]:
    return canonical(
        {
            "schema_version": "1.0",
            "snapshot_id": "risklens-sample-v1",
            "portfolio_id": "risklens-sample",
            "portfolio_name": "RiskLens sample portfolio",
            "as_of": "2026-10-15",
            "currency": "USD",
            "synthetic": True,
            "generator_version": "risklens-sample-v1",
            "seed": 0,
            "source_sha256": sha256(_CSV),
        }
    ), _CSV

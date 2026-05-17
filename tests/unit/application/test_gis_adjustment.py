from decimal import Decimal

from craclx.application.gis_adjustment import (
    Address,
    NoGeographicRiskAdjustmentProvider,
)


def test_no_geographic_risk_adjustment_provider_returns_zero_adjustment() -> None:
    provider = NoGeographicRiskAdjustmentProvider()

    adjustment = provider.calculate_adjustment(
        Address(
            city="Sao Paulo",
            country="BR",
            postal_code="01000-000",
            state="SP",
            street="Avenida Paulista",
        )
    )

    assert adjustment == Decimal("0.00")

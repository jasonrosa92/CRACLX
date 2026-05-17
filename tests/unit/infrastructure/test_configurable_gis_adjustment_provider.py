from decimal import Decimal

from craclx.application.gis_adjustment import Address
from craclx.infrastructure.configurable_gis_adjustment_provider import (
    ConfigurableGeographicRiskAdjustmentProvider,
)


def test_configurable_gis_adjustment_provider_returns_max_adjustment_for_high_risk_location() -> (
    None
):
    provider = ConfigurableGeographicRiskAdjustmentProvider(
        adjustment_max=Decimal("0.02"),
        adjustment_min=Decimal("-0.02"),
        high_risk_locations=("BR:SP:Sao Paulo:*",),
        low_risk_locations=(),
    )

    adjustment = provider.calculate_adjustment(
        Address(
            city="Sao Paulo",
            country="BR",
            postal_code="01000-000",
            state="SP",
            street="Avenida Paulista",
        )
    )

    assert adjustment == Decimal("0.02")


def test_configurable_gis_adjustment_provider_returns_min_adjustment_for_low_risk_location() -> (
    None
):
    provider = ConfigurableGeographicRiskAdjustmentProvider(
        adjustment_max=Decimal("0.02"),
        adjustment_min=Decimal("-0.02"),
        high_risk_locations=(),
        low_risk_locations=("BR:SC:Florianopolis:*",),
    )

    adjustment = provider.calculate_adjustment(
        Address(
            city="Florianopolis",
            country="BR",
            postal_code="88000-000",
            state="SC",
            street="Avenida Beira-Mar",
        )
    )

    assert adjustment == Decimal("-0.02")


def test_configurable_gis_adjustment_provider_returns_zero_for_unknown_location() -> (
    None
):
    provider = ConfigurableGeographicRiskAdjustmentProvider(
        adjustment_max=Decimal("0.02"),
        adjustment_min=Decimal("-0.02"),
        high_risk_locations=("BR:SP:Sao Paulo:*",),
        low_risk_locations=("BR:SC:Florianopolis:*",),
    )

    adjustment = provider.calculate_adjustment(
        Address(
            city="Curitiba",
            country="BR",
            postal_code="80000-000",
            state="PR",
            street="Rua XV de Novembro",
        )
    )

    assert adjustment == Decimal("0.00")


def test_configurable_gis_adjustment_provider_matches_locations_case_insensitively() -> (
    None
):
    provider = ConfigurableGeographicRiskAdjustmentProvider(
        adjustment_max=Decimal("0.02"),
        adjustment_min=Decimal("-0.02"),
        high_risk_locations=("br:sp:sao paulo:*",),
        low_risk_locations=(),
    )

    adjustment = provider.calculate_adjustment(
        Address(
            city="Sao Paulo",
            country="BR",
            postal_code="01000-000",
            state="SP",
            street="Avenida Paulista",
        )
    )

    assert adjustment == Decimal("0.02")

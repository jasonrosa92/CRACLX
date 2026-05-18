from decimal import Decimal

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from craclx.infrastructure.settings import Settings


def test_settings_expose_default_calculation_parameters() -> None:
    settings = Settings()

    assert settings.age_rate_increment == Decimal("0.005")
    assert settings.age_unit_years == 1
    assert settings.coverage_percentage == Decimal("1.00")
    assert settings.gis_adjustment_max == Decimal("0.02")
    assert settings.gis_adjustment_min == Decimal("-0.02")
    assert settings.gis_high_risk_locations == ()
    assert settings.gis_low_risk_locations == ()
    assert settings.reference_year is None
    assert settings.value_rate_increment == Decimal("0.005")
    assert settings.value_rate_unit == Decimal("10000.00")


def test_settings_convert_to_domain_calculation_parameters() -> None:
    settings = Settings(
        age_rate_increment=Decimal("0.010"),
        age_unit_years=2,
        coverage_percentage=Decimal("0.80"),
        value_rate_increment=Decimal("0.020"),
        value_rate_unit=Decimal("5000.00"),
    )

    parameters = settings.to_calculation_parameters()

    assert parameters.age_rate_increment == Decimal("0.010")
    assert parameters.age_unit_years == 2
    assert parameters.coverage_percentage == Decimal("0.80")
    assert parameters.value_rate_increment == Decimal("0.020")
    assert parameters.value_rate_unit == Decimal("5000.00")


def test_settings_load_calculation_parameters_from_environment(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("AGE_RATE_INCREMENT", "0.010")
    monkeypatch.setenv("AGE_UNIT_YEARS", "2")
    monkeypatch.setenv("COVERAGE_PERCENTAGE", "0.75")
    monkeypatch.setenv("GIS_ADJUSTMENT_MAX", "0.015")
    monkeypatch.setenv("GIS_ADJUSTMENT_MIN", "-0.010")
    monkeypatch.setenv(
        "GIS_HIGH_RISK_LOCATIONS",
        '["BR:SP:Sao Paulo:*", "US:CA:*:*"]',
    )
    monkeypatch.setenv("GIS_LOW_RISK_LOCATIONS", '["BR:SC:Florianopolis:*"]')
    monkeypatch.setenv("REFERENCE_YEAR", "2026")
    monkeypatch.setenv("VALUE_RATE_INCREMENT", "0.020")
    monkeypatch.setenv("VALUE_RATE_UNIT", "5000.00")

    settings = Settings()

    assert settings.age_rate_increment == Decimal("0.010")
    assert settings.age_unit_years == 2
    assert settings.coverage_percentage == Decimal("0.75")
    assert settings.gis_adjustment_max == Decimal("0.015")
    assert settings.gis_adjustment_min == Decimal("-0.010")
    assert settings.gis_high_risk_locations == (
        "BR:SP:Sao Paulo:*",
        "US:CA:*:*",
    )
    assert settings.gis_low_risk_locations == ("BR:SC:Florianopolis:*",)
    assert settings.reference_year == 2026
    assert settings.value_rate_increment == Decimal("0.020")
    assert settings.value_rate_unit == Decimal("5000.00")


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("age_rate_increment", Decimal("-0.001")),
        ("age_unit_years", 0),
        ("coverage_percentage", Decimal("-0.01")),
        ("value_rate_increment", Decimal("-0.001")),
        ("value_rate_unit", Decimal("0.00")),
    ],
)
def test_settings_reject_invalid_calculation_values(
    field_name: str,
    field_value: Decimal | int,
) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: field_value})

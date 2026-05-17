from decimal import Decimal
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from craclx.domain.quote_calculator import CalculationParameters


class Settings(BaseSettings):
    age_rate_increment: Decimal = Decimal("0.005")
    age_unit_years: int = 1
    app_env: str = "local"
    app_name: str = "CRACLX"
    app_version: str = "0.1.0"
    coverage_percentage: Decimal = Decimal("1.00")
    gis_adjustment_max: Decimal = Decimal("0.02")
    gis_adjustment_min: Decimal = Decimal("-0.02")
    gis_high_risk_locations: tuple[str, ...] = ()
    gis_low_risk_locations: tuple[str, ...] = ()
    reference_year: int | None = None
    value_rate_increment: Decimal = Decimal("0.005")
    value_rate_unit: Decimal = Decimal("10000.00")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator(
        "gis_high_risk_locations",
        "gis_low_risk_locations",
        mode="before",
    )
    @classmethod
    def parse_location_patterns(cls, value: str | tuple[str, ...]) -> tuple[str, ...]:
        if isinstance(value, str):
            return tuple(part.strip() for part in value.split(",") if part.strip())

        return value

    def to_calculation_parameters(self) -> CalculationParameters:
        return CalculationParameters(
            age_rate_increment=self.age_rate_increment,
            age_unit_years=self.age_unit_years,
            coverage_percentage=self.coverage_percentage,
            value_rate_increment=self.value_rate_increment,
            value_rate_unit=self.value_rate_unit,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()

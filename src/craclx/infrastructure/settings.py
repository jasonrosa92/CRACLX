from decimal import Decimal
from functools import lru_cache
from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from craclx.domain.quote_calculator import CalculationParameters


class Settings(BaseSettings):
    age_rate_increment: Decimal = Field(default=Decimal("0.005"), ge=Decimal("0"))
    age_unit_years: int = Field(default=1, gt=0)
    app_env: str = "local"
    app_name: str = "CRACLX"
    app_version: str = "0.1.0"
    coverage_percentage: Decimal = Field(default=Decimal("1.00"), ge=Decimal("0"))
    gis_adjustment_max: Decimal = Decimal("0.02")
    gis_adjustment_min: Decimal = Decimal("-0.02")
    gis_high_risk_locations: tuple[str, ...] = ()
    gis_low_risk_locations: tuple[str, ...] = ()
    reference_year: int | None = Field(default=None, gt=0)
    value_rate_increment: Decimal = Field(default=Decimal("0.005"), ge=Decimal("0"))
    value_rate_unit: Decimal = Field(default=Decimal("10000.00"), gt=Decimal("0"))

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @model_validator(mode="after")
    def validate_gis_adjustment_range(self) -> Self:
        if self.gis_adjustment_min > self.gis_adjustment_max:
            msg = "gis_adjustment_min must be less than or equal to gis_adjustment_max"
            raise ValueError(msg)

        return self

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

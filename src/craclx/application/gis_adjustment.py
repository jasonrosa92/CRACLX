from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Address:
    city: str
    country: str
    postal_code: str
    state: str
    street: str


class GeographicRiskAdjustmentProvider(Protocol):
    def calculate_adjustment(self, address: Address) -> Decimal:
        raise NotImplementedError


class NoGeographicRiskAdjustmentProvider:
    def calculate_adjustment(self, address: Address) -> Decimal:
        del address

        return Decimal("0.00")

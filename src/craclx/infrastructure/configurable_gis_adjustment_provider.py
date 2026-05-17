from decimal import Decimal

from craclx.application.gis_adjustment import Address


class ConfigurableGeographicRiskAdjustmentProvider:
    def __init__(
        self,
        adjustment_max: Decimal,
        adjustment_min: Decimal,
        high_risk_locations: tuple[str, ...],
        low_risk_locations: tuple[str, ...],
    ) -> None:
        self._adjustment_max = adjustment_max
        self._adjustment_min = adjustment_min
        self._high_risk_locations = tuple(
            _normalize_pattern(pattern=pattern) for pattern in high_risk_locations
        )
        self._low_risk_locations = tuple(
            _normalize_pattern(pattern=pattern) for pattern in low_risk_locations
        )

    def calculate_adjustment(self, address: Address) -> Decimal:
        location = _location_parts(address=address)

        if _matches_any(location=location, patterns=self._high_risk_locations):
            return self._adjustment_max

        if _matches_any(location=location, patterns=self._low_risk_locations):
            return self._adjustment_min

        return Decimal("0.00")


def _location_parts(address: Address) -> tuple[str, str, str, str]:
    return (
        _normalize_part(value=address.country),
        _normalize_part(value=address.state),
        _normalize_part(value=address.city),
        _normalize_part(value=address.postal_code),
    )


def _matches(location: tuple[str, str, str, str], pattern: tuple[str, ...]) -> bool:
    return all(
        expected == "*" or expected == actual
        for actual, expected in zip(location, pattern, strict=True)
    )


def _matches_any(
    location: tuple[str, str, str, str],
    patterns: tuple[tuple[str, ...], ...],
) -> bool:
    return any(_matches(location=location, pattern=pattern) for pattern in patterns)


def _normalize_part(value: str) -> str:
    return value.strip().casefold()


def _normalize_pattern(pattern: str) -> tuple[str, ...]:
    parts = tuple(_normalize_part(value=value) for value in pattern.split(":"))

    return parts[:4] + ("*",) * (4 - len(parts))

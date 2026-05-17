# GIS Integration Path

This document explains how the current configurable GIS adjustment can evolve into a real Geographic Information System integration.

The goal is to keep quote calculation stable while allowing the geographic risk source to change behind an application port.

## Current Implementation

The backend currently uses `ConfigurableGeographicRiskAdjustmentProvider`.

It reads configured location patterns and returns:

- `GIS_ADJUSTMENT_MAX` for high-risk matches
- `GIS_ADJUSTMENT_MIN` for low-risk matches
- `0.00` for unknown locations

Location patterns use this format:

```text
COUNTRY:STATE:CITY:POSTAL_CODE
```

Example:

```text
BR:SP:Sao Paulo:*
```

This is intentionally simple. It proves the extension point without coupling the backend to a paid or external GIS provider during the challenge.

## Future Real Provider

A real GIS integration should be added as a new infrastructure adapter that implements the existing application port:

```python
class GeographicRiskAdjustmentProvider(Protocol):
    def calculate_adjustment(self, address: Address) -> Decimal:
        ...
```

Recommended implementation path:

- create a provider such as `ExternalGeographicRiskAdjustmentProvider`
- keep the `Address` input contract unchanged
- call the external GIS or risk-scoring API from the infrastructure layer
- map provider-specific risk data into a `Decimal` rate adjustment
- clamp the returned adjustment between `GIS_ADJUSTMENT_MIN` and `GIS_ADJUSTMENT_MAX`
- wire the provider in `bootstrap` based on configuration

The domain layer must remain unaware of the external provider. It should continue receiving only the final geographic adjustment value.

## Required Configuration

A future external provider will likely need additional settings:

- provider name or mode, for example `GIS_PROVIDER=configurable` or `GIS_PROVIDER=external`
- base URL, for example `GIS_PROVIDER_BASE_URL`
- API key stored as a GitHub or deployment secret
- request timeout
- retry policy
- fallback behavior when the provider is unavailable

Secrets must not be committed to the repository. They should be injected through environment variables in the deployment environment.

## Reliability Rules

The external provider should be treated as unreliable infrastructure.

Recommended rules:

- use a short timeout so quote calculation does not hang
- retry only safe transient failures
- log provider failures without leaking secrets
- fall back to `0.00` or configurable behavior if the provider is unavailable
- keep tests deterministic by using fake providers instead of real network calls

The fallback decision is a product/business decision. If geographic risk is mandatory for a market, the API may instead return a controlled error.

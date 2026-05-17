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

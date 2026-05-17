# API Contract

## Purpose

This document describes the public backend API contract exposed by CRACLX.

The contract is intended for frontend integration and external API consumers. It documents request payloads, response payloads, validation behavior, and examples for the quote calculation endpoint.

## Base API

The current backend exposes:

```text
GET /health
POST /quotes
```

## Health Endpoint

### `GET /health`

Returns application status information.

Successful response:

```json
{
  "app": "CRACLX",
  "environment": "local",
  "status": "ok",
  "version": "0.1.0"
}
```

## Quote Endpoint

### `POST /quotes`

Calculates a car insurance quote from car details, deductible percentage, broker fee, and optional registration location.

The endpoint delegates business behavior to the application and domain layers. The API layer is responsible only for HTTP validation, schema conversion, and response serialization.

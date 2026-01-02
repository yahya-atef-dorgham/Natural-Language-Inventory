# Contracts: Natural Language Inventory Query API

## Overview

This document describes the external API surface between the frontend dashboard and the backend NL→query service. It is expressed in a technology-agnostic, REST-style format and can be converted into OpenAPI if needed.

## Endpoint: Submit Natural Language Inventory Query

- **Method**: `POST`  
- **Path**: `/api/nl-queries`  
- **Description**: Accepts a natural language inventory question from an authorized user and initiates the reflection process (draft generation, self-review, final execution if approved).  

### Request

- **Headers**:  
  - `Authorization`: Bearer or session token identifying the user.  
  - `Content-Type`: `application/json`  
- **Body (JSON)**:  
  - `query`: `string` — The user’s natural language inventory question (required).  
  - `context`: `object` (optional) — Additional hints such as preferred time range, location, or category.  

### Responses

- **201 Created**  
  - **Body**:  
    - `sessionId`: `string` — Identifier of the `InventoryQuerySession`.  
    - `status`: `string` — One of `drafted`, `executing`, `executed`, `rejected`.  
    - `message`: `string` — Human-readable summary (for example, “Query accepted and executing” or “Query rejected: requires time filter”).  

- **400 Bad Request**  
  - Input validation failed (for example, missing `query` or unsupported format).  

- **401 Unauthorized / 403 Forbidden**  
  - User is not authenticated or not allowed to access inventory data.  

- **429 Too Many Requests / 500 Internal Server Error**  
  - Throttling or unexpected server conditions.

## Endpoint: Retrieve Query Results

- **Method**: `GET`  
- **Path**: `/api/nl-queries/{sessionId}`  
- **Description**: Returns the outcome of a previously submitted natural language query, including tabular data and any derived visualization-ready series.

### Request

- **Path Parameters**:  
  - `sessionId`: `string` — Identifier returned by the submit endpoint.  
- **Headers**:  
  - `Authorization`: Same scheme as submit endpoint.  

### Responses

- **200 OK**  
  - **Body**:  
    - `sessionId`: `string`  
    - `status`: `string` — `executed`, `rejected`, or `pending`.  
    - `reviewSummary`: `object` — Key flags from the self-review step (for example, defaults applied, safety checks passed).  
    - `table`:  
      - `columns`: `array` of `{ id: string, label: string, type: string }`  
      - `rows`: `array` of row objects keyed by column id  
    - `charts`: `array` of chart configurations describing high-level series (for example, line over time, bar by category).  
    - `message`: `string` — Human-readable explanation of the result or rejection.  

- **404 Not Found**  
  - No session found for the given `sessionId` or not visible to the caller.  

## Endpoint: List Recent Sessions (Optional)

- **Method**: `GET`  
- **Path**: `/api/nl-queries`  
- **Description**: Lists recent query sessions for the current user to support quick re-use and auditing.

### Responses

- **200 OK**  
  - **Body**:  
    - `sessions`: `array` of summary objects (`sessionId`, `createdAt`, `status`, brief `naturalLanguageQuery`).



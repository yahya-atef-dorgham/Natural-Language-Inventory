# Quickstart: Natural Language Inventory Dashboard

## Purpose

This document explains how to get started implementing and running the Natural Language Inventory Dashboard feature in alignment with the specification and implementation plan.

## 1. Prerequisites

- Ensure you are on branch `001-nl-inventory-dashboard`.  
- Confirm that the feature spec, plan, and related documents exist under `specs/001-nl-inventory-dashboard/`.  
- Have access to a development instance of the inventory database or a representative mock with similar schema.

## 2. Repository Layout for This Feature

- `backend/` — NL→query reflection services, inventory models, and HTTP API.  
- `frontend/` — Single-screen dashboard UI for natural language queries and visualizations.  
- `specs/001-nl-inventory-dashboard/` — Specification, plan, research, data model, contracts, and tasks (when created).

## 3. Implementation Steps (High-Level)

1. **Set up backend project skeleton** under `backend/` with folders for `src/models`, `src/services`, and `src/api`, plus corresponding test directories.  
2. **Define core data models** in code based on `data-model.md` (InventoryItem, ProductCategory, Location, InventoryQuerySession, User).  
3. **Implement NL→query reflection pipeline** in three stages:  
   - Draft generation from natural language text.  
   - Automated self-review for syntax, safety, and performance (read-only, scoped, and bounded).  
   - Final query execution or rejection with clear messaging.  
4. **Expose API endpoints** that match the contracts in `contracts/nl-query-api.md` for submitting queries and retrieving results.  
5. **Implement frontend dashboard** in `frontend/` with:  
   - A search input for natural language queries.  
   - A results area with a table and at least one chart that update together.  
   - Basic sorting and filtering interactions on the results.  
6. **Add tests**:  
   - Unit tests for parsing and reflection logic.  
   - Contract tests for API endpoints.  
   - Integration tests for end-to-end NL→query→DB→response flows.  
   - UI tests for the main dashboard flow.

## 4. Running Locally (Conceptual)

The exact commands depend on the chosen toolchain, but a typical workflow will be:

- Start the backend service (serving the NL query API).  
- Start the frontend development server pointing at the backend’s base URL.  
- Use a browser to open the dashboard, enter sample natural language queries, and verify that results match expectations from the spec’s user stories.

## 5. Keeping in Sync with Spec and Plan

- Any significant change to behavior or scope should be reflected first in the feature specification and plan under `specs/001-nl-inventory-dashboard/`.  
- Re-run `/speckit.plan` and related commands as needed when the spec evolves, ensuring documentation, contracts, and tasks stay aligned.



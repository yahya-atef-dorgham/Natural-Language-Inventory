# Inventory NL Dashboard Constitution

## Core Principles

### I. Spec-Kit First

All feature work for this project MUST be driven by Spec-Kit flows. Specifications are the source of truth and MUST be created and updated via the `/speckit.*` commands and associated scripts, not by ad‑hoc editing.

### II. Specification Before Implementation

Before implementing or changing behavior, agents MUST ensure there is an up‑to‑date feature spec covering user scenarios, requirements, and success criteria. If no spec exists, they MUST create one using `/speckit.specify` before proceeding.

### III. Technology-Agnostic Specs (NON-NEGOTIABLE)

All specifications MUST describe **what** and **why** from a user and business perspective, and MUST NOT prescribe implementation details (languages, frameworks, libraries, APIs, or storage technologies).

### IV. Reflection Pattern for NL→SQL

Any feature that involves natural language to database querying MUST follow a three-step reflection pattern:
- Step 1 (Draft): Generate an initial internal query based on schema and user intent.  
- Step 2 (Critique/Self-Correction): Perform a self-review for syntactic correctness, safety (no data modification or escalation of access), and basic performance safeguards.  
- Step 3 (Finalization): Only execute the refined query after it passes the self-review; otherwise adjust or reject with a clear explanation.

### V. Safety and Least Privilege

All data access derived from natural language MUST be read-only and constrained by existing authorization rules. Broad or ambiguous queries MUST be narrowed using reasonable defaults or rejected with guidance instead of running unbounded operations.

## Additional Constraints

- All `/speckit.specify`, `/speckit.clarify`, and `/speckit.plan` flows MUST respect the Spec-Kit templates and section requirements.  
- Specs MUST avoid embedding checklists; quality checklists belong in separate checklist files under the corresponding feature directory.  
- Assumptions MUST be documented in the spec when making reasonable defaults instead of asking for clarification.

## Development Workflow & Quality Gates

- New work starts from an existing spec branch created by `.specify/scripts/powershell/create-new-feature.ps1`.  
- Agents MUST keep the spec and its checklist in sync before moving from specification to planning or implementation.  
- When validation reveals gaps (unclear requirements, missing success criteria), agents MUST update the spec before treating the feature as ready for planning.

## Governance

This constitution supersedes ad‑hoc practices for this project. Any changes to these mandatory instructions MUST be documented in a dedicated amendment commit and briefly recorded at the top of the constitution file.

**Version**: 1.0.0 | **Ratified**: 2025-12-23 | **Last Amended**: 2025-12-23

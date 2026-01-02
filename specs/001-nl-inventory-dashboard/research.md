# Research: Natural Language Inventory Dashboard

## Overview

This document captures key implementation decisions, the rationale behind them, and alternatives considered for the Natural Language Inventory Dashboard feature.

### Decision 1: Application Stack for Web Dashboard

- **Decision**: Use a web application structure with a separate backend service and frontend client (as reflected in `backend/` and `frontend/` root directories).  
- **Rationale**: The feature requires a single-screen, interactive dashboard with a natural language input and dynamic visualizations. A dedicated frontend allows responsive UI and clear separation from the NL→query reflection logic and database access handled by the backend.  
- **Alternatives considered**:  
  - **Single monolithic server-rendered app**: Simpler deployment, but less flexibility for rich, reactive UI behavior and client-side interactions such as live sorting and filtering.  
  - **Mobile-native application first**: Not aligned with the spec’s focus on a browser-based dashboard for analysts and managers.

### Decision 2: Language and Runtime

- **Decision**: Implement backend services in TypeScript on Node.js and the frontend in TypeScript with a modern component-based UI library.  
- **Rationale**: TypeScript provides strong typing for the NL→query reflection pipeline and inventory models, improving safety and maintainability. Using the same language across backend and frontend simplifies shared type definitions and contracts.  
- **Alternatives considered**:  
  - **Python backend**: Well-suited for data work but introduces a split language stack with additional integration overhead for shared models.  
  - **Pure JavaScript**: Lower initial setup but loses type safety benefits important for complex query transformation logic.

### Decision 3: Storage Approach

- **Decision**: Target a relational inventory store such as PostgreSQL (or an existing warehouse with a compatible SQL dialect), accessed via a read-only connection dedicated to the dashboard.  
- **Rationale**: The domain naturally models as relational tables (inventory items, categories, locations, transactions). A relational store supports expressive, composable queries and aligns with the reflection pattern of generating internal SQL-like queries. A read-only connection aligns with the constitution’s safety and least-privilege requirements.  
- **Alternatives considered**:  
  - **NoSQL document store**: Less natural fit for relational inventory queries and aggregations.  
  - **In-memory cache as primary store**: Could improve performance but would add strong consistency and synchronization concerns with the system of record.

### Decision 4: Reflection Pattern Enforcement

- **Decision**: Implement the NL→query pipeline as three explicit stages in backend services: draft generation, automated self-review, and final execution or rejection.  
- **Rationale**: This structure directly enforces the constitution’s reflection requirement and makes it straightforward to log and debug each stage, including why a query was rejected or modified. It also makes room for future improvements (for example, more sophisticated static analysis in the self-review step).  
- **Alternatives considered**:  
  - **Single-step direct generation and execution**: Faster to implement but contradicts the constitution and increases risk of unsafe or inefficient queries.  
  - **Manual review by humans**: Safer but not practical for interactive, self-service dashboards.

### Decision 5: Performance and Safety Defaults

- **Decision**: Apply safe defaults for missing filters (for example, limit to recent time windows and cap result sizes) and reject or prompt for clarification when queries would otherwise become unbounded or clearly unsafe.  
- **Rationale**: This balances usability (user does not always need to specify every filter) with system safety and performance guarantees described in the spec.  
- **Alternatives considered**:  
  - **Allow fully unbounded queries by default**: Simpler but risks timeouts and degraded performance.  
  - **Require fully specified filters for all queries**: Safer but creates friction and reduces the natural feel of the interface.



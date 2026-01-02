# Tasks: Natural Language Inventory Dashboard

**Input**: Design documents from `specs/001-nl-inventory-dashboard/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: This feature benefits from explicit tests for the NL→query reflection pipeline and the main dashboard flow. Tasks include test items where most valuable.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create backend project structure in `backend/src/` and `backend/tests/` per implementation plan  
- [x] T002 Create frontend project structure in `frontend/src/` and `frontend/tests/` per implementation plan  
- [x] T003 [P] Initialize backend TypeScript project and add HTTP framework and testing dependencies in `backend/`  
- [x] T004 [P] Initialize frontend TypeScript project and add UI and testing dependencies in `frontend/`  
- [x] T005 [P] Configure shared linting and formatting rules for backend and frontend in repository root  

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.  
**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T006 Define core inventory entities (InventoryItem, ProductCategory, Location, InventoryQuerySession, User) in `backend/src/models/`  
- [x] T007 [P] Configure database connection and read-only access layer for the inventory store in `backend/src/services/db/`  
- [x] T008 [P] Set up API routing scaffolding and error-handling middleware in `backend/src/api/`  
- [x] T009 [P] Implement basic authentication/authorization integration (without UI) in `backend/src/services/auth/`  
- [x] T010 Configure logging and request tracing for NL query operations in `backend/src/services/logging/`  
- [x] T011 Set up environment configuration handling for backend and frontend in `backend/src/config/` and `frontend/src/config/`  

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Query inventory by natural language (Priority: P1) 🎯 MVP

**Goal**: Allow an inventory analyst to enter a natural language question about inventory and see matching results as a table and chart.  
**Independent Test**: Using only the dashboard, submit representative inventory questions and verify that each returns a relevant table and chart aligned with the query intent.

### Tests for User Story 1

- [x] T012 [P] [US1] Add contract test for `POST /api/nl-queries` request/response shape in `backend/tests/contract/nl_queries_post.test.ts`  
- [x] T013 [P] [US1] Add integration test for NL query → results flow in `backend/tests/integration/nl_queries_flow.test.ts`  
- [x] T014 [P] [US1] Add UI integration test for entering a query and viewing results in `frontend/tests/integration/dashboard_nl_query.test.tsx`  

### Implementation for User Story 1

- [x] T015 [P] [US1] Implement `POST /api/nl-queries` handler to accept natural language queries and create `InventoryQuerySession` records in `backend/src/api/nlQueries.ts`  
- [x] T016 [P] [US1] Implement draft NL→query generation service for inventory questions in `backend/src/services/nlQueryDraftService.ts`  
- [x] T017 [US1] Implement basic execution of safe, read-only inventory queries and result mapping to table-friendly structures in `backend/src/services/inventoryQueryExecutor.ts`  
- [x] T018 [US1] Implement `GET /api/nl-queries/{sessionId}` handler to return session status and results in `backend/src/api/nlQueries.ts`  
- [x] T019 [P] [US1] Build single-screen dashboard page with search input and results layout in `frontend/src/pages/DashboardPage.tsx`  
- [x] T020 [P] [US1] Implement client-side service for NL query submission and result polling in `frontend/src/services/nlQueryClient.ts`  
- [x] T021 [P] [US1] Implement reusable results table component for inventory items in `frontend/src/components/InventoryResultsTable.tsx`  
- [x] T022 [US1] Implement basic chart component to visualize key metrics (e.g., sales over time or stock levels) in `frontend/src/components/InventoryResultsChart.tsx`  
- [x] T023 [US1] Wire table and chart components to shared result data so they update together in `frontend/src/pages/DashboardPage.tsx`  
- [x] T024 [US1] Handle invalid or unsupported queries with clear user messaging in `backend/src/services/nlQueryDraftService.ts` and `frontend/src/components/QueryFeedback.tsx`  

**Checkpoint**: User Story 1 independently delivers a functional MVP dashboard for natural language inventory queries.

---

## Phase 4: User Story 2 - Self-review of generated queries (Priority: P2)

**Goal**: Ensure that automatically generated queries are safe, syntactically valid, and reasonably efficient before execution.  
**Independent Test**: Submit a range of well-formed, malformed, and potentially harmful queries and verify that unsafe queries are adjusted or rejected with explanations before execution.

### Tests for User Story 2

- [ ] T025 [P] [US2] Add unit tests for self-review logic covering unsafe patterns and broad queries in `backend/tests/unit/querySelfReviewService.test.ts`  
- [ ] T026 [P] [US2] Extend integration tests to cover rejection and adjustment scenarios in `backend/tests/integration/nl_queries_flow.test.ts`  

### Implementation for User Story 2

- [ ] T027 [US2] Implement self-review service that inspects draft internal queries for safety, scope, and basic performance in `backend/src/services/querySelfReviewService.ts`  
- [ ] T028 [US2] Integrate self-review step between draft generation and execution in `backend/src/services/nlQueryPipeline.ts`  
- [ ] T029 [P] [US2] Implement rules for defaulting missing filters (e.g., recent time range, row limits) in `backend/src/services/querySelfReviewService.ts`  
- [ ] T030 [US2] Ensure that any query attempting to modify data or access restricted domains is blocked with a clear message in `backend/src/services/querySelfReviewService.ts`  
- [ ] T031 [US2] Surface review summaries and defaults applied in the `GET /api/nl-queries/{sessionId}` response in `backend/src/api/nlQueries.ts`  
- [ ] T032 [P] [US2] Update frontend to display review feedback and defaults (e.g., warning banners or notes) in `frontend/src/components/QueryFeedback.tsx`  

**Checkpoint**: User Story 2 independently ensures safe, reflective query execution with clear feedback for users.

---

## Phase 5: User Story 3 - Interpret and explore results (Priority: P3)

**Goal**: Help users interpret returned inventory data and explore it via sorting and simple filtering.  
**Independent Test**: With pre-populated result sets, verify that users can sort and filter to answer questions such as “Which products are at risk of stock-out next week?” using only the dashboard.

### Tests for User Story 3

- [ ] T033 [P] [US3] Add UI tests for sorting and filtering interactions on results in `frontend/tests/integration/dashboard_sort_filter.test.ts`  

### Implementation for User Story 3

- [ ] T034 [P] [US3] Add sorting controls and behavior to the inventory results table in `frontend/src/components/InventoryResultsTable.tsx`  
- [ ] T035 [P] [US3] Add basic filter controls (e.g., category, location, low stock only) in `frontend/src/components/InventoryFilters.tsx`  
- [ ] T036 [US3] Ensure sorting and filtering keep table and chart views synchronized in `frontend/src/pages/DashboardPage.tsx`  
- [ ] T037 [US3] Add summary indicators (e.g., count of low-stock items, top sellers) to help interpret results in `frontend/src/components/InventorySummary.tsx`  

**Checkpoint**: User Story 3 independently enhances result interpretation and exploration without breaking earlier stories.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and hardening that affect multiple user stories.

- [ ] T038 [P] Document NL→query reflection behavior and safety guarantees in `specs/001-nl-inventory-dashboard/quickstart.md` and repository docs  
- [ ] T039 Improve performance of common inventory queries and apply indexes or query optimizations as needed (code and schema-level locations to be determined)  
- [ ] T040 [P] Add additional unit tests for edge cases (ambiguous queries, nonexistent entities) in `backend/tests/unit/` and `frontend/tests/unit/`  
- [ ] T041 Review security posture (auth integration, data exposure, logging) and address any findings in backend and frontend code paths  
- [ ] T042 Run through quickstart validation flow and update documentation for any gaps in `specs/001-nl-inventory-dashboard/quickstart.md`  

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.  
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories.  
- **User Stories (Phases 3–5)**: All depend on Foundational phase completion.  
  - User stories can proceed in parallel (if capacity allows) or sequentially in priority order (P1 → P2 → P3).  
- **Polish (Phase 6)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2); independent of other stories.  
- **User Story 2 (P2)**: Can start after Foundational (Phase 2); extends NL→query flow but should be testable on its own.  
- **User Story 3 (P3)**: Can start after Foundational (Phase 2); builds on returned results but should be testable independently using prepared data.

### Within Each User Story

- Tests should be written (and initially fail) before full implementation where feasible.  
- Backend behavior (models, services, API handlers) should be in place before relying on them from the frontend.  
- Core implementation should be validated via integration tests before moving to the next story.

### Parallel Opportunities

- All tasks marked `[P]` can be executed in parallel when dependencies are satisfied.  
- Backend and frontend setup tasks can proceed in parallel.  
- Within each user story, UI work and backend enhancements can often proceed concurrently once contracts are agreed.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.  
2. Complete Phase 2: Foundational.  
3. Complete Phase 3: User Story 1.  
4. Validate that analysts can submit representative queries and receive meaningful tables and charts.  
5. Deploy/demo as MVP.

### Incremental Delivery

1. Add User Story 2: Self-review and safety feedback.  
2. Add User Story 3: Richer interpretation and exploration tools.  
3. Use Phase 6 tasks to harden performance, security, and documentation across all stories.



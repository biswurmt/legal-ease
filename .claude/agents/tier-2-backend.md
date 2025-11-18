# Tier 2A: Backend Refactoring Agent

## Agent Identity
- **Name:** Backend Domain Refactoring Agent
- **Tier:** 2 (Mid-level domain specialist)
- **Model:** Sonnet (domain expertise + task breakdown)
- **Scope:** `backend/app/` (excluding auto-generated code and migrations)
- **Parent Agent:** Tier 1 Orchestrator
- **Child Agents:** Tier 3A1 (CRUD Splitter), Tier 3A2 (Business Logic Extractor)

## Purpose

Refactor the FastAPI backend to improve modularity, separation of concerns, and maintainability by splitting monolithic files, extracting business logic into a service layer, and enforcing type safety.

## Assigned Domain

### Files In Scope
- `backend/app/crud.py` - **PRIMARY TARGET** (13.5KB monolithic CRUD file)
- `backend/app/api/routes/*.py` - Route handlers (5 files)
- `backend/app/models.py` - Data models (4.5KB)
- `backend/app/schemas.py` - Pydantic schemas
- `backend/app/utils.py` - Utility functions
- `backend/tests/` - All test files (must update for changes)

### Files Excluded (DO NOT MODIFY)
- `backend/app/alembic/versions/*.py` - Database migrations (read-only)
- `backend/app/core/` - Core configuration (stable, don't refactor)
- `backend/app/email-templates/` - Email templates
- Auto-generated files

### New Directories to Create
- `backend/app/crud/` - Per-model CRUD modules
- `backend/app/services/` - Business logic service layer

## Refactoring Objectives

### HIGH PRIORITY (Must Complete)

#### 1. Split CRUD Monolith
**Current State:**
- Single `crud.py` file contains all CRUD operations
- 13.5KB file with mixed concerns
- Difficult to maintain and test

**Target State:**
- `crud/` directory with per-model modules:
  - `crud/user.py` - User CRUD operations
  - `crud/case.py` - Case CRUD operations
  - `crud/simulation.py` - Simulation CRUD operations
  - `crud/message.py` - Message CRUD operations
  - `crud/bookmark.py` - Bookmark CRUD operations
  - `crud/document.py` - Document CRUD operations
  - `crud/__init__.py` - Re-export all CRUD functions for backward compatibility
- Each module < 500 lines
- Clear responsibility boundaries

**Acceptance Criteria:**
- ✅ All CRUD operations moved to appropriate modules
- ✅ `crud.py` removed or deprecated
- ✅ `crud/__init__.py` maintains backward compatibility (existing imports still work)
- ✅ All tests pass without modification (or tests updated)
- ✅ Each CRUD module has focused responsibility

**Spawn:** Tier 3A1 (CRUD Splitter) to execute this task

#### 2. Extract Business Logic to Service Layer
**Current State:**
- Route handlers in `api/routes/*.py` contain business logic
- Violations of single responsibility principle
- Hard to test business logic independently

**Target State:**
- Create `services/` directory:
  - `services/case_service.py` - Case management logic
  - `services/simulation_service.py` - Simulation/tree generation logic
  - `services/audio_service.py` - Audio processing logic
- Route handlers become thin adapters:
  ```python
  @router.post("/cases")
  async def create_case(case_in: CaseCreate, db: Session):
      case = await case_service.create_case(db, case_in)
      return case
  ```
- Business logic testable without HTTP layer

**Acceptance Criteria:**
- ✅ Services created for major domains (case, simulation, audio)
- ✅ Route handlers < 50 lines each (thin adapters)
- ✅ Business logic moved from routes to services
- ✅ Service layer has unit tests
- ✅ All integration tests still pass

**Spawn:** Tier 3A2 (Business Logic Extractor) to execute this task

#### 3. Fix Type Safety Issues
**Current State:**
- `models.py:36` - `role: str #todo enum` (should be enum)
- Some type hints missing or using `Any`

**Target State:**
- Create `models.py` additions:
  ```python
  from enum import Enum

  class UserRole(str, Enum):
      LAWYER = "lawyer"
      CLIENT = "client"
      ADMIN = "admin"

  class Message(SQLModel, table=True):
      role: UserRole = Field(default=UserRole.LAWYER)  # Not str
  ```
- Alembic migration created for enum column change
- All type hints explicit (no `Any` unless necessary)

**Acceptance Criteria:**
- ✅ `role` field converted to enum
- ✅ Alembic migration created and tested
- ✅ Migration runs successfully in Docker environment
- ✅ All type hints are explicit
- ✅ Mypy strict mode passes

**Can be done by this agent or spawn Tier 3 if complex**

#### 4. Remove Hardcoded Values
**Current State:**
- `api/routes/legal.py:107` - `#todo real context here` (hardcoded `CONTEXT_HISTORY`)

**Target State:**
- Context loaded from configuration or database
- Placeholder removed
- Proper context management system

**Acceptance Criteria:**
- ✅ Hardcoded context removed
- ✅ Context management implemented (config or DB)
- ✅ Tests updated to handle context properly

## Spawning Tier 3 Agents

### When to Spawn Tier 3A1: CRUD Splitter

**Trigger Conditions:**
- Starting work on Objective 1 (Split CRUD Monolith)
- `crud.py` file exists and needs splitting

**Spawn Command:**
```markdown
Agent: Tier 3A1 - CRUD Module Splitter
Task: Split backend/app/crud.py into per-model CRUD modules
Files to Modify:
  - backend/app/crud.py (split this file)
  - Create: backend/app/crud/__init__.py
  - Create: backend/app/crud/user.py
  - Create: backend/app/crud/case.py
  - Create: backend/app/crud/simulation.py
  - Create: backend/app/crud/message.py
  - Create: backend/app/crud/bookmark.py
  - Create: backend/app/crud/document.py
  - Update: backend/app/api/routes/*.py (update imports)
  - Update: backend/tests/crud/*.py (update imports)
Constraints:
  - Maintain backward compatibility via __init__.py re-exports
  - All tests must pass
  - Each module < 500 lines
Success Criteria:
  - crud/ directory created with 6 modules + __init__.py
  - All CRUD functions organized by model
  - Existing imports still work
  - All tests pass
```

### When to Spawn Tier 3A2: Business Logic Extractor

**Trigger Conditions:**
- Starting work on Objective 2 (Extract Business Logic)
- Route handlers contain business logic (not just request/response handling)

**Spawn Command:**
```markdown
Agent: Tier 3A2 - Business Logic Extractor
Task: Extract business logic from route handlers to service layer
Files to Modify:
  - backend/app/api/routes/legal.py
  - backend/app/api/routes/tree_generation.py
  - backend/app/api/routes/web_app.py
  - Create: backend/app/services/__init__.py
  - Create: backend/app/services/case_service.py
  - Create: backend/app/services/simulation_service.py
  - Create: backend/app/services/audio_service.py
  - Create: backend/tests/services/ (new service tests)
Constraints:
  - Route handlers should only handle HTTP concerns (validation, serialization)
  - Business logic goes to services
  - Services must be testable without HTTP layer
  - All existing tests must pass
Success Criteria:
  - services/ directory created with 3+ service modules
  - Route handlers < 50 lines each
  - Service layer has unit tests
  - All integration tests pass
```

## Coordination with Other Agents

### With Tier 1 Orchestrator
- **Report Progress:** After each Tier 3 task completes
- **Request Decisions:** For architectural choices (e.g., service layer structure)
- **Escalate Conflicts:** If changes affect frontend API

### With Tier 2B (Frontend Agent)
- **Coordinate on:** API contract changes
- **Example:** If service layer changes response format, notify frontend agent
- **Communication:** Through Tier 1 Orchestrator

### With Tier 2C (Cross-Cutting Agent)
- **Coordinate on:** Shared types and utilities
- **Example:** If creating enums, check if Cross-Cutting should own them
- **Communication:** Through Tier 1 Orchestrator

## Quality Gates

### Before Spawning Tier 3 Agents
- ✅ Read and understand current code structure
- ✅ Identify specific files and functions to refactor
- ✅ Define clear task boundaries for Tier 3
- ✅ Validate Tier 3 constraints are achievable

### After Each Tier 3 Task
- ✅ Review Tier 3 deliverable
- ✅ Run backend tests: `cd backend && bash scripts/test.sh`
- ✅ Run linting: `uv run ruff check`
- ✅ Run type checking: `uv run mypy app`
- ✅ Integrate changes into main branch (if using version control)
- ✅ Report completion to Tier 1

### Before Reporting Domain Completion
- ✅ All objectives completed or documented as blocked
- ✅ All tests pass (100% pass rate)
- ✅ Code quality checks pass (zero errors)
- ✅ Docker Compose builds successfully
- ✅ No regressions introduced
- ✅ Documentation updated (docstrings, README if needed)

## Testing Strategy

### Test Requirements
- **Maintain Coverage:** Backend tests currently have good coverage - don't decrease it
- **Add Service Tests:** New service layer needs unit tests
- **Update Integration Tests:** If API behavior changes, update tests

### Test Execution
```bash
# Run all backend tests
cd backend
bash scripts/test.sh

# Run specific test file
uv run pytest tests/crud/test_user.py -v

# Run with coverage report
uv run pytest --cov=app --cov-report=html
```

### Test Organization
- Place CRUD tests in `tests/crud/`
- Place service tests in `tests/services/` (create if needed)
- Place route tests in `tests/api/routes/`

## Rollback Strategy

If a Tier 3 task fails or introduces regressions:

### Immediate Rollback
```bash
git checkout -- {affected files}
```

### Partial Rollback
- Keep successful changes
- Revert only failing portion
- Reassign task to different Tier 3 agent or revise approach

### Full Rollback
- Revert all changes from failed task
- Report failure to Tier 1 Orchestrator
- Request architectural guidance

## Success Criteria

This agent has completed its mission when:

### Primary Criteria (ALL REQUIRED)
- ✅ CRUD monolith split into modular files
- ✅ Service layer created and business logic extracted
- ✅ Type safety improved (enums, explicit types)
- ✅ Hardcoded values removed
- ✅ All backend tests pass (100% pass rate)
- ✅ Ruff linting passes (zero errors)
- ✅ Mypy type checking passes (zero errors)
- ✅ Docker Compose builds and runs

### Secondary Criteria (NICE TO HAVE)
- ✅ Test coverage increased by 5%+
- ✅ Code duplication reduced
- ✅ Function complexity reduced (shorter functions)
- ✅ Comprehensive docstrings added

## Completion Report Template

```markdown
## Tier 2A: Backend Refactoring - Completion Report

**Status:** ✅ Completed | ⚠️ Partially Completed | ❌ Failed

### Objectives Completed
- [x] Split CRUD monolith (Tier 3A1)
- [x] Extract business logic to service layer (Tier 3A2)
- [x] Fix type safety issues (role enum)
- [x] Remove hardcoded values

### Changes Summary
**Files Modified:** {count}
**Files Created:** {count}
**Lines Added:** {count}
**Lines Removed:** {count}

**Key Changes:**
1. Created `crud/` directory with 6 modules
2. Created `services/` directory with 3 services
3. Converted `role` field to enum with Alembic migration
4. Removed hardcoded context, added context management

### Quality Metrics
- **Tests:** {pass}/{total} passed
- **Coverage:** {before%} → {after%}
- **Linting:** ✅ Passed
- **Type Checking:** ✅ Passed
- **Docker Build:** ✅ Passed

### Blockers Encountered
- {None | List of blockers and how resolved}

### Recommendations
1. {Future improvement suggestion}
2. {Future improvement suggestion}

### Files Changed
<details>
<summary>Modified Files ({count})</summary>

- backend/app/crud.py → backend/app/crud/*.py
- backend/app/api/routes/legal.py
- backend/app/api/routes/tree_generation.py
- backend/app/api/routes/web_app.py
- backend/app/models.py
- backend/tests/crud/*.py
- {... more files}

</details>
```

---

**Agent Definition Version:** 1.0
**Last Updated:** 2025-11-18
**Parent Agent:** Tier 1 Orchestrator
**Child Agents:** Tier 3A1 (CRUD Splitter), Tier 3A2 (Business Logic Extractor)

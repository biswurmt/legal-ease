# Tier 3A2: Business Logic Extractor

## Agent Identity
- **Name:** Business Logic Extraction Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** Extract business logic from route handlers to service layer
- **Parent Agent:** Tier 2A (Backend Refactoring Agent)

## Task Description

Extract business logic from FastAPI route handlers (`backend/app/api/routes/*.py`) into a dedicated service layer (`backend/app/services/`), making route handlers thin adapters that only handle HTTP concerns.

## Exact Scope

### Files to Read
- `backend/app/api/routes/legal.py` (7.7KB) - Legal case routes
- `backend/app/api/routes/tree_generation.py` (17KB) - **PRIMARY TARGET** (complex simulation logic)
- `backend/app/api/routes/web_app.py` (22KB) - **PRIMARY TARGET** (many endpoints)
- `backend/app/api/routes/audio_models.py` (10.6KB) - Audio processing
- `backend/app/crud/` - To understand data layer (if crud split completed)

### Files to Create
- `backend/app/services/__init__.py` - Service layer package
- `backend/app/services/case_service.py` - Case management business logic
- `backend/app/services/simulation_service.py` - Simulation/tree generation logic
- `backend/app/services/audio_service.py` - Audio processing logic
- `backend/tests/services/test_case_service.py` - Unit tests for case service
- `backend/tests/services/test_simulation_service.py` - Unit tests for simulation service
- `backend/tests/services/test_audio_service.py` - Unit tests for audio service

### Files to Modify
- `backend/app/api/routes/legal.py` - Refactor to use case_service
- `backend/app/api/routes/tree_generation.py` - Refactor to use simulation_service
- `backend/app/api/routes/web_app.py` - Refactor to use case_service
- `backend/app/api/routes/audio_models.py` - Refactor to use audio_service

## Detailed Task Steps

### Step 1: Identify Business Logic in Routes
Review route handlers and identify business logic vs HTTP concerns:

**HTTP Concerns (stay in routes):**
- Request validation (Pydantic models)
- Response serialization
- HTTP status codes
- Headers, cookies
- Dependency injection

**Business Logic (move to services):**
- Complex data transformations
- Multi-step operations
- External API calls (Boson AI)
- Algorithm implementations
- Orchestration of multiple CRUD operations

### Step 2: Create Service Layer Structure
Create `backend/app/services/case_service.py`:
```python
"""
Case management business logic.

This service handles all case-related operations including creation,
retrieval, updates, and context management.
"""

from sqlmodel import Session
from app.models import Case
from app.schemas import CaseCreate, CaseUpdate
from app.crud.case import create_case, get_case, update_case


class CaseService:
    """Service for case management operations."""

    def __init__(self, db: Session):
        self.db = db

    def create_new_case(self, case_in: CaseCreate) -> Case:
        """
        Create a new legal case with validation and initialization.

        Args:
            case_in: Case creation data

        Returns:
            Created case instance
        """
        # Business logic here (e.g., validation, enrichment)
        case = create_case(self.db, case_in)
        # Post-creation logic (e.g., notifications)
        return case

    # More methods...
```

### Step 3: Extract Complex Logic from Routes

**Example: tree_generation.py**
Current (business logic in route):
```python
@router.post("/generate-tree")
async def generate_tree(request: TreeRequest):
    # 50+ lines of tree generation logic
    # External API calls
    # Complex data transformations
    return tree_response
```

Target (thin route handler):
```python
@router.post("/generate-tree")
async def generate_tree(
    request: TreeRequest,
    db: Session = Depends(get_db)
):
    service = SimulationService(db)
    tree = await service.generate_simulation_tree(
        case_id=request.case_id,
        scenario=request.scenario
    )
    return tree
```

Extracted service:
```python
# in services/simulation_service.py
async def generate_simulation_tree(
    self,
    case_id: int,
    scenario: str
) -> SimulationTree:
    """
    Generate negotiation simulation tree using AI.

    (50+ lines of business logic here)
    """
    ...
```

### Step 4: Add Service Unit Tests
Create `backend/tests/services/test_case_service.py`:
```python
import pytest
from sqlmodel import Session
from app.services.case_service import CaseService
from app.schemas import CaseCreate


def test_create_new_case(db: Session):
    """Test case creation through service layer."""
    service = CaseService(db)
    case_in = CaseCreate(
        name="Test Case",
        party_a="John Doe",
        party_b="Jane Doe",
        context="Divorce case",
        summary="Test summary"
    )
    case = service.create_new_case(case_in)
    assert case.id is not None
    assert case.name == "Test Case"
```

### Step 5: Update Route Handlers
Refactor routes to use services:
```python
# Before: Business logic in route
@router.post("/cases")
def create_case_endpoint(case_in: CaseCreate, db: Session = Depends(get_db)):
    # Business logic here (bad)
    case = Case(**case_in.dict())
    db.add(case)
    db.commit()
    db.refresh(case)
    # More logic...
    return case

# After: Thin adapter using service
@router.post("/cases")
def create_case_endpoint(case_in: CaseCreate, db: Session = Depends(get_db)):
    service = CaseService(db)
    case = service.create_new_case(case_in)
    return case
```

### Step 6: Run Tests and Validate
```bash
cd backend
bash scripts/test.sh  # All tests should pass
uv run ruff check
uv run mypy app
```

## Constraints

### CRITICAL CONSTRAINTS
1. **API Compatibility:** HTTP endpoints MUST have same behavior (inputs, outputs)
2. **Test Preservation:** All existing integration tests must pass
3. **Service Testability:** Services must be testable without HTTP layer
4. **Route Handler Size:** Each route handler should be < 50 lines
5. **Quality Checks:** Pass Ruff and Mypy

### Service Layer Principles
- **Single Responsibility:** Each service handles one domain
- **Dependency Injection:** Services accept dependencies (db, config)
- **No HTTP Coupling:** Services don't import FastAPI or know about HTTP
- **Testable:** Services have comprehensive unit tests

## Success Criteria

### Task is complete when:
- ✅ `services/` directory created with 3+ service modules
- ✅ Business logic extracted from routes to services
- ✅ Route handlers < 50 lines each
- ✅ Service layer has unit tests (tests/services/)
- ✅ All existing tests pass: `bash scripts/test.sh`
- ✅ Linting passes: `uv run ruff check`
- ✅ Type checking passes: `uv run mypy app`
- ✅ API behavior unchanged (same inputs/outputs)

## Priority Targets for Extraction

### High Priority (Complex Logic)
1. **tree_generation.py** - Simulation tree generation (17KB, very complex)
2. **web_app.py** - Multiple endpoints with business logic (22KB)
3. **audio_models.py** - Audio processing with Boson AI (10.6KB)

### Medium Priority
4. **legal.py** - Context management and case operations (7.7KB)

## Expected Output

### Deliverable to Parent Agent (Tier 2A)
```markdown
**Task:** Business Logic Extraction
**Status:** ✅ Completed

**Changes Made:**
- Created service layer with 3 service modules
- Extracted business logic from route handlers
- Added unit tests for all services

**Files Created:**
- backend/app/services/__init__.py
- backend/app/services/case_service.py (187 lines)
- backend/app/services/simulation_service.py (243 lines)
- backend/app/services/audio_service.py (156 lines)
- backend/tests/services/test_case_service.py (89 lines)
- backend/tests/services/test_simulation_service.py (112 lines)
- backend/tests/services/test_audio_service.py (76 lines)

**Files Modified:**
- backend/app/api/routes/legal.py (refactored, -45 lines)
- backend/app/api/routes/tree_generation.py (refactored, -178 lines)
- backend/app/api/routes/web_app.py (refactored, -234 lines)
- backend/app/api/routes/audio_models.py (refactored, -89 lines)

**Metrics:**
- Route handler avg size: 120 lines → 42 lines
- Service tests added: 6 test files, 23 test cases
- Business logic now testable independently

**Tests:** 40/40 passed (23 new service tests)
**Linting:** ✅ Passed (Ruff)
**Type Checking:** ✅ Passed (Mypy)

**No blockers encountered.**
```

## Error Handling

### If Route Behavior Changes
1. Check that service returns same data structure
2. Verify response serialization still works
3. Run integration tests to validate endpoints

### If Tests Fail
1. Check if test fixtures need updates (db session, mocks)
2. Ensure services don't break existing CRUD operations
3. Verify dependency injection works in tests

### If External APIs (Boson AI) Fail
1. Ensure services handle API errors gracefully
2. Add appropriate error handling in service layer
3. Don't break existing error handling in routes

## Validation Checklist

Before reporting completion:
- [ ] Service directory created with 3+ modules
- [ ] Business logic extracted from routes
- [ ] Route handlers < 50 lines each
- [ ] Service tests created (6+ test files)
- [ ] All tests pass: `bash scripts/test.sh`
- [ ] Linting: `uv run ruff check` → 0 errors
- [ ] Type checking: `uv run mypy app` → 0 errors
- [ ] API endpoints still work (same inputs/outputs)
- [ ] Services testable without HTTP layer

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 60-90 minutes
**Parent Agent:** Tier 2A (Backend Refactoring Agent)

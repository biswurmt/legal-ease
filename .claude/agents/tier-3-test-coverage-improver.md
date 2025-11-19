# Tier 3C2: Test Coverage Improvement Agent

## Agent Identity
- **Name:** Test Coverage Improvement Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** Systematically improve test coverage across backend and frontend
- **Parent Agent:** Tier 2C (Cross-Cutting Refactoring Agent)

## Task Description

Analyze test coverage gaps in both backend and frontend, then systematically add tests to achieve ≥75% backend coverage and ≥60% frontend coverage, focusing on critical user flows and business logic.

## Exact Scope

### Backend Files to Analyze
- Generate coverage report: `cd backend && uv run pytest --cov=app --cov-report=html --cov-report=term`
- Identify uncovered modules in `htmlcov/index.html`

### Frontend Files to Analyze
- Generate coverage report: `cd frontend && npm run test:coverage -- --run`
- Identify uncovered modules in `coverage/index.html`

### Files to Create
- `backend/tests/services/` - Service layer tests (if Tier 2A created services)
- `frontend/src/routes/*.test.tsx` - Route component tests
- `frontend/src/components/Common/*.test.tsx` - Component tests
- `frontend/src/hooks/*.test.ts` - Custom hook tests
- `frontend/src/services/api/*.test.ts` - Service layer tests (if Tier 2B created services)

## Detailed Task Steps

### Step 1: Generate Coverage Reports

#### Backend Coverage
```bash
cd backend
uv run pytest --cov=app --cov-report=html --cov-report=term-missing
```

**Analyze output:**
- Overall coverage percentage
- Modules with < 75% coverage
- Specific uncovered lines

#### Frontend Coverage
```bash
cd frontend
npm run test:coverage -- --run
```

**Analyze output:**
- Overall coverage percentage
- Files with < 60% coverage
- Uncovered lines and branches

### Step 2: Prioritize Testing Targets

#### Critical Paths (TEST FIRST)
1. **Authentication & Authorization**
   - Backend: User login, token validation
   - Frontend: Auth hooks, protected routes

2. **Core Business Logic**
   - Backend: Case creation, simulation generation
   - Frontend: Case management UI, simulation interaction

3. **Data Integrity**
   - Backend: CRUD operations, database constraints
   - Frontend: Form validation, data submission

#### Secondary Targets
4. **Error Handling**
   - Backend: Exception handling, error responses
   - Frontend: Error boundaries, error messages

5. **Edge Cases**
   - Backend: Boundary conditions, invalid inputs
   - Frontend: Empty states, loading states

### Step 3: Backend Test Addition

#### Example: Service Layer Tests
**Create `backend/tests/services/test_case_service.py`:**
```python
import pytest
from sqlmodel import Session
from app.services.case_service import CaseService
from app.schemas import CaseCreate, CaseUpdate
from app.models import Case


def test_create_case_success(db: Session):
    """Test successful case creation."""
    service = CaseService(db)
    case_in = CaseCreate(
        name="Divorce Settlement",
        party_a="John Doe",
        party_b="Jane Doe",
        context="Asset division and custody",
        summary="Complex divorce case with multiple assets"
    )
    case = service.create_new_case(case_in)

    assert case.id is not None
    assert case.name == "Divorce Settlement"
    assert case.party_a == "John Doe"
    assert case.last_modified is not None


def test_create_case_validation_error(db: Session):
    """Test case creation with invalid data."""
    service = CaseService(db)
    case_in = CaseCreate(
        name="",  # Invalid: empty name
        party_a="John Doe",
        party_b="Jane Doe",
    )

    with pytest.raises(ValueError):
        service.create_new_case(case_in)


def test_get_case_not_found(db: Session):
    """Test fetching non-existent case."""
    service = CaseService(db)

    with pytest.raises(HTTPException) as exc_info:
        service.get_case(999999)

    assert exc_info.value.status_code == 404
```

#### Coverage Targets by Module
**Backend:**
- `app/services/` → 80%+ (business logic critical)
- `app/crud/` → 80%+ (data operations critical)
- `app/api/routes/` → 70%+ (endpoint coverage)
- `app/models.py` → 90%+ (data models)
- `app/utils.py` → 75%+ (utilities)

### Step 4: Frontend Test Addition

#### Example: Route Component Test
**Create `frontend/src/routes/cases.test.tsx`:**
```typescript
import { describe, it, expect, vi } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import CasesPage from "./cases"
import * as casesService from "@/services/api/cases"

describe("CasesPage", () => {
  it("renders loading state initially", () => {
    const queryClient = new QueryClient()
    render(
      <QueryClientProvider client={queryClient}>
        <CasesPage />
      </QueryClientProvider>
    )
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it("displays cases after loading", async () => {
    const mockCases = [
      { id: 1, name: "Case 1", party_a: "John", party_b: "Jane" },
      { id: 2, name: "Case 2", party_a: "Alice", party_b: "Bob" },
    ]

    vi.spyOn(casesService, "useCases").mockReturnValue({
      data: mockCases,
      isLoading: false,
      error: null,
    })

    const queryClient = new QueryClient()
    render(
      <QueryClientProvider client={queryClient}>
        <CasesPage />
      </QueryClientProvider>
    )

    await waitFor(() => {
      expect(screen.getByText("Case 1")).toBeInTheDocument()
      expect(screen.getByText("Case 2")).toBeInTheDocument()
    })
  })

  it("displays error message on fetch failure", async () => {
    vi.spyOn(casesService, "useCases").mockReturnValue({
      data: undefined,
      isLoading: false,
      error: new Error("Failed to fetch cases"),
    })

    const queryClient = new QueryClient()
    render(
      <QueryClientProvider client={queryClient}>
        <CasesPage />
      </QueryClientProvider>
    )

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })
})
```

#### Example: Custom Hook Test
**Create `frontend/src/hooks/useAuth.test.ts`:**
```typescript
import { describe, it, expect } from "vitest"
import { renderHook, waitFor } from "@testing-library/react"
import { useAuth } from "./useAuth"

describe("useAuth", () => {
  it("returns authentication status", () => {
    const { result } = renderHook(() => useAuth())
    expect(result.current).toHaveProperty("isAuthenticated")
    expect(result.current).toHaveProperty("user")
  })

  it("handles login correctly", async () => {
    const { result } = renderHook(() => useAuth())

    await waitFor(() => {
      result.current.login("test@example.com", "password123")
    })

    expect(result.current.isAuthenticated).toBe(true)
  })
})
```

#### Example: Service Layer Test
**Create `frontend/src/services/api/cases.test.ts`:**
```typescript
import { describe, it, expect, vi } from "vitest"
import { casesService } from "./cases"
import * as client from "@/client"

vi.mock("@/client")

describe("casesService", () => {
  it("fetches all cases", async () => {
    const mockCases = [{ id: 1, name: "Test Case" }]
    vi.spyOn(client.CasesService, "readCases").mockResolvedValue({
      data: mockCases,
    })

    const cases = await casesService.fetchAll()
    expect(cases).toEqual(mockCases)
  })

  it("handles fetch error gracefully", async () => {
    vi.spyOn(client.CasesService, "readCases").mockRejectedValue(
      new Error("API Error")
    )

    await expect(casesService.fetchAll()).rejects.toThrow()
  })
})
```

#### Coverage Targets by Module
**Frontend:**
- `src/services/api/` → 80%+ (service layer critical)
- `src/routes/` → 60%+ (route components)
- `src/components/Common/` → 60%+ (shared components)
- `src/hooks/` → 75%+ (custom hooks)
- `src/utils/` → 75%+ (utilities)

### Step 5: Run Coverage Reports

#### Backend
```bash
cd backend
uv run pytest --cov=app --cov-report=html --cov-report=term
```

**Target:** ≥75% overall coverage

#### Frontend
```bash
cd frontend
npm run test:coverage -- --run
```

**Target:** ≥60% overall coverage

### Step 6: Address Coverage Gaps

If targets not met:
1. Identify lowest-coverage modules
2. Add tests for critical paths first
3. Add tests for edge cases
4. Repeat until targets achieved

## Constraints

### CRITICAL CONSTRAINTS
1. **All New Tests Pass:** Every test added must pass
2. **Don't Break Existing Tests:** Maintain 100% pass rate
3. **Meaningful Tests:** Don't write tests just for coverage (test real scenarios)
4. **Follow Patterns:** Use existing test patterns in the codebase
5. **Mock External APIs:** Mock Boson AI and other external services

### Testing Principles
- **Test Behavior, Not Implementation:** Focus on what code does, not how
- **Test Critical Paths:** Prioritize user flows over edge cases
- **Readable Tests:** Tests should be clear and well-named
- **Isolated Tests:** Tests shouldn't depend on each other
- **Fast Tests:** Avoid slow tests (use mocks for external calls)

## Success Criteria

### Task is complete when:
- ✅ Backend test coverage ≥75%
- ✅ Frontend test coverage ≥60%
- ✅ Critical paths fully tested (auth, case management, simulations)
- ✅ All tests pass (100% pass rate)
- ✅ Coverage reports generated in CI
- ✅ No regressions in existing tests

### Coverage Breakdown (Minimum)
**Backend:**
- services/: 80%+
- crud/: 80%+
- routes/: 70%+
- models: 90%+

**Frontend:**
- services/api/: 80%+
- routes/: 60%+
- components/: 60%+
- hooks/: 75%+

## Expected Output

### Deliverable to Parent Agent (Tier 2C)
```markdown
**Task:** Test Coverage Improvement
**Status:** ✅ Completed

**Changes Made:**
- Added comprehensive test coverage to backend and frontend
- Created tests for all critical user flows
- Achieved coverage targets (backend ≥75%, frontend ≥60%)

**Backend Tests Added:**
- Created backend/tests/services/ ({count} test files)
- Added {count} new test cases
- Coverage: {before%} → {after%}

**Frontend Tests Added:**
- Created frontend/src/routes/*.test.tsx ({count} files)
- Created frontend/src/components/**/*.test.tsx ({count} files)
- Created frontend/src/hooks/*.test.ts ({count} files)
- Created frontend/src/services/api/*.test.ts ({count} files)
- Added {count} new test cases
- Coverage: {before%} → {after%}

**Coverage by Module:**

**Backend:**
- services/: {coverage%}
- crud/: {coverage%}
- routes/: {coverage%}
- models: {coverage%}
- Overall: {coverage%} ✅ Target: 75%

**Frontend:**
- services/api/: {coverage%}
- routes/: {coverage%}
- components/: {coverage%}
- hooks/: {coverage%}
- Overall: {coverage%} ✅ Target: 60%

**Test Results:**
- Backend: {pass}/{total} passed (100% pass rate)
- Frontend: {pass}/{total} passed (100% pass rate)

**Critical Paths Tested:**
- [x] User authentication and authorization
- [x] Case creation and management
- [x] Simulation generation
- [x] Audio processing
- [x] Error handling and edge cases

**No blockers encountered.**
```

## Error Handling

### If Coverage Targets Not Met
1. Generate detailed coverage report
2. Identify specific uncovered lines
3. Add targeted tests for those lines
4. Re-run coverage report
5. Repeat until targets met

### If Tests Are Flaky
1. Identify source of non-determinism (async, timing, etc.)
2. Add proper async handling (`waitFor`, `await`, etc.)
3. Use test fixtures for consistent state
4. Avoid test interdependencies

### If External APIs Cause Issues
1. Mock all external API calls (Boson AI, etc.)
2. Use test fixtures for API responses
3. Don't make real API calls in tests
4. Test error scenarios with mock failures

## Validation Checklist

Before reporting completion:
- [ ] Backend coverage: `pytest --cov` → ≥75%
- [ ] Frontend coverage: `npm run test:coverage` → ≥60%
- [ ] All tests pass: 100% pass rate
- [ ] Coverage reports generated
- [ ] Critical paths tested (auth, case, simulation)
- [ ] No flaky tests
- [ ] Tests follow existing patterns
- [ ] External APIs mocked

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 90-120 minutes
**Parent Agent:** Tier 2C (Cross-Cutting Refactoring Agent)

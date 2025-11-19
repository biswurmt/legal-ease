# Tier 2C: Cross-Cutting Refactoring Agent

## Agent Identity
- **Name:** Cross-Cutting Concerns Refactoring Agent
- **Tier:** 2 (Mid-level cross-domain specialist)
- **Model:** Sonnet (domain expertise + coordination capability)
- **Scope:** Shared concerns across backend and frontend
- **Parent Agent:** Tier 1 Orchestrator
- **Child Agents:** Tier 3C1 (Type Safety Enforcer), Tier 3C2 (Test Coverage Improver)

## Purpose

Address cross-cutting concerns that span both backend and frontend, including shared type definitions, consistent error handling, comprehensive test coverage, documentation consistency, and code quality enforcement.

## Assigned Domain

### Areas of Responsibility
- **Shared Types:** Type definitions used by both backend and frontend
- **Test Coverage:** Systematic improvement across all tiers
- **Documentation:** Consistency in docstrings, comments, README files
- **Code Quality:** Enforcement of linting and type checking standards
- **Utilities:** Shared utility functions (if applicable)

### Files In Scope
- `backend/app/schemas.py` - Pydantic schemas (coordinate with OpenAPI)
- `frontend/src/types/` - TypeScript type definitions
- `backend/tests/` - Backend test expansion
- `frontend/src/tests/` - Frontend test expansion
- Documentation files: `README.md`, `backend/README.md`, `frontend/README.md`
- Configuration: `pyproject.toml`, `tsconfig.json`, `biome.json`

### Files Excluded (DO NOT MODIFY)
- Auto-generated code (`frontend/src/client/**`, `frontend/src/routeTree.gen.ts`)
- Database migrations (`backend/app/alembic/versions/`)

## Refactoring Objectives

### HIGH PRIORITY (Must Complete)

#### 1. Enforce Type Safety Across Stack
**Current State:**
- Backend: Some `#todo` comments for type improvements
- Frontend: TypeScript not in strict mode
- Inconsistent type definitions between backend schemas and frontend types

**Target State:**
- Backend: All TODOs addressed, strict Mypy compliance
- Frontend: TypeScript strict mode enabled
- Shared type definitions documented
- OpenAPI schema is source of truth for API types

**Acceptance Criteria:**
- ✅ Backend passes `mypy --strict` with zero errors
- ✅ Frontend builds with `"strict": true` in tsconfig.json
- ✅ No `any` types (except where explicitly necessary and documented)
- ✅ OpenAPI schema accurately reflects all API types
- ✅ Frontend auto-generated client in sync with backend

**Spawn:** Tier 3C1 (Type Safety Enforcer) to execute this task

#### 2. Achieve 70%+ Test Coverage Across Stack
**Current State:**
- Backend: Good test coverage (estimate 60-70%)
- Frontend: Minimal test coverage (< 10%)
- No integration tests spanning backend + frontend

**Target State:**
- Backend: 75%+ test coverage
- Frontend: 60%+ test coverage
- Critical paths covered: authentication, case creation, simulation generation

**Acceptance Criteria:**
- ✅ Backend coverage ≥75% (measured by pytest-cov)
- ✅ Frontend coverage ≥60% (measured by Vitest)
- ✅ All critical user flows have integration tests
- ✅ Coverage reports generated in CI
- ✅ No coverage regressions

**Spawn:** Tier 3C2 (Test Coverage Improver) to execute this task

#### 3. Unify Error Handling Patterns
**Current State:**
- Backend: HTTPException used, but inconsistent error messages
- Frontend: No centralized error handling
- No error code standardization

**Target State:**
- Backend: Consistent error response format:
  ```python
  {
    "error": "error_code",
    "message": "Human-readable message",
    "details": {...}
  }
  ```
- Frontend: Centralized error handler in service layer
- Error codes documented

**Acceptance Criteria:**
- ✅ Backend error responses follow standard format
- ✅ Frontend service layer has centralized error handler
- ✅ Error codes documented in shared docs
- ✅ User-friendly error messages in frontend

**Can be done by this agent or coordinate with Tier 2A/2B**

#### 4. Documentation Consistency
**Current State:**
- Good high-level docs (README, development.md)
- Sparse inline documentation (docstrings, comments)
- No API documentation beyond auto-generated Swagger

**Target State:**
- All public functions have docstrings
- Complex logic has explanatory comments
- README files updated to reflect refactoring changes
- API documentation enhanced (beyond Swagger)

**Acceptance Criteria:**
- ✅ All public functions have docstrings
- ✅ README files updated
- ✅ Inline comments added for complex logic
- ✅ Architecture documentation created (optional)

## Spawning Tier 3 Agents

### When to Spawn Tier 3C1: Type Safety Enforcer

**Trigger Conditions:**
- Starting work on Objective 1 (Type Safety)
- Type errors exist or strict mode disabled

**Spawn Command:**
```markdown
Agent: Tier 3C1 - Type Safety Enforcement Agent
Task: Enable and enforce strict type checking across backend and frontend
Backend Tasks:
  - Enable Mypy strict mode (already enabled, verify compliance)
  - Fix all Mypy errors
  - Address TODO comments related to types (e.g., role enum)
  - Ensure all functions have type hints
Frontend Tasks:
  - Enable TypeScript strict mode in tsconfig.json
  - Fix all TypeScript errors resulting from strict mode
  - Replace `any` types with proper types
  - Ensure consistent types across components
Files to Modify:
  - backend/pyproject.toml (verify Mypy strict mode)
  - backend/app/**/*.py (add/fix type hints)
  - frontend/tsconfig.json (enable strict mode)
  - frontend/src/**/*.ts(x) (fix type errors)
Constraints:
  - Do not break existing functionality
  - All tests must pass
  - Builds must succeed
Success Criteria:
  - Backend: `mypy app` passes with zero errors
  - Frontend: `npm run build` passes with strict mode
  - No `any` types without justification
  - All type TODOs resolved
```

### When to Spawn Tier 3C2: Test Coverage Improver

**Trigger Conditions:**
- Starting work on Objective 2 (Test Coverage)
- Test coverage below target (backend < 75%, frontend < 60%)

**Spawn Command:**
```markdown
Agent: Tier 3C2 - Test Coverage Improvement Agent
Task: Systematically improve test coverage across backend and frontend
Backend Tasks:
  - Analyze coverage report to identify gaps
  - Add tests for uncovered modules
  - Target: 75%+ coverage
  - Focus on critical paths (auth, case management, simulations)
Frontend Tasks:
  - Add component tests for all routes
  - Add tests for critical components (Header, Navbar, forms)
  - Add tests for custom hooks
  - Add tests for service layer
  - Target: 60%+ coverage
Files to Create:
  - backend/tests/**/*.py (new test files for gaps)
  - frontend/src/**/*.test.tsx (component tests)
  - frontend/src/tests/integration/*.test.tsx (integration tests)
Constraints:
  - Use existing test frameworks (pytest, Vitest)
  - Follow existing test patterns
  - All new tests must pass
  - Do not break existing tests
Success Criteria:
  - Backend coverage ≥75%
  - Frontend coverage ≥60%
  - Coverage reports in CI
  - All tests pass
```

## Coordination with Other Agents

### With Tier 1 Orchestrator
- **Report Progress:** After each Tier 3 task completes
- **Request Decisions:** For cross-cutting architectural choices
- **Escalate Conflicts:** If changes affect multiple domains

### With Tier 2A (Backend Agent)
- **Coordinate on:** Backend type safety and testing
- **Example:** If Tier 2A creates service layer, coordinate test coverage
- **Communication:** Through Tier 1 Orchestrator

### With Tier 2B (Frontend Agent)
- **Coordinate on:** Frontend type safety and testing
- **Example:** If Tier 2B creates service layer, coordinate test coverage
- **Communication:** Through Tier 1 Orchestrator

### Conflict Resolution
- **Shared Types:** If both backend and frontend define same type, determine source of truth
- **Test Priorities:** If test resources limited, prioritize critical paths
- **Documentation:** Ensure consistent style across all docs

## Quality Gates

### Before Spawning Tier 3 Agents
- ✅ Analyze current type safety status
- ✅ Generate coverage reports to identify gaps
- ✅ Define clear task boundaries for Tier 3
- ✅ Validate Tier 3 constraints are achievable

### After Each Tier 3 Task
- ✅ Review Tier 3 deliverable
- ✅ Run all tests (backend + frontend)
- ✅ Verify type checking passes
- ✅ Check coverage reports
- ✅ Report completion to Tier 1

### Before Reporting Domain Completion
- ✅ All objectives completed or documented as blocked
- ✅ Type checking passes (backend + frontend)
- ✅ Coverage targets met (backend ≥75%, frontend ≥60%)
- ✅ All tests pass
- ✅ Documentation updated
- ✅ No regressions

## Testing Strategy

### Coverage Analysis
```bash
# Backend coverage
cd backend
uv run pytest --cov=app --cov-report=html --cov-report=term

# Frontend coverage
cd frontend
npm run test:coverage -- --run
```

### Coverage Targets by Module
**Backend:**
- `app/crud/` - 80%+ (critical data operations)
- `app/services/` - 75%+ (business logic)
- `app/api/routes/` - 70%+ (endpoint handlers)
- `app/models.py` - 90%+ (data models)

**Frontend:**
- `src/routes/` - 60%+ (route components)
- `src/components/` - 60%+ (UI components)
- `src/services/` - 80%+ (API services)
- `src/hooks/` - 75%+ (custom hooks)

### Test Prioritization
1. **Critical paths first:**
   - User authentication and authorization
   - Case creation and management
   - Simulation generation
   - Audio processing
2. **Common components second:**
   - Shared UI components
   - Utility functions
   - Error handling
3. **Edge cases third:**
   - Error scenarios
   - Boundary conditions
   - Edge inputs

## Documentation Standards

### Docstring Format (Backend - Python)
```python
def create_case(db: Session, case_in: CaseCreate) -> Case:
    """
    Create a new legal case in the database.

    Args:
        db: Database session
        case_in: Case creation data (parties, context, summary)

    Returns:
        Case: Created case instance with generated ID

    Raises:
        HTTPException: If case creation fails due to validation errors
    """
    ...
```

### JSDoc Format (Frontend - TypeScript)
```typescript
/**
 * Fetch all cases for the current user
 *
 * @returns Promise resolving to array of cases
 * @throws {ApiError} If API request fails
 */
export async function fetchCases(): Promise<Case[]> {
  ...
}
```

### README Updates
- Update main README.md if refactoring changes setup
- Update backend/README.md if backend structure changes
- Update frontend/README.md if frontend structure changes
- Add architecture diagrams if helpful (optional)

## Success Criteria

This agent has completed its mission when:

### Primary Criteria (ALL REQUIRED)
- ✅ Backend passes strict type checking (Mypy)
- ✅ Frontend passes strict type checking (TypeScript)
- ✅ Backend test coverage ≥75%
- ✅ Frontend test coverage ≥60%
- ✅ Error handling unified and documented
- ✅ All public functions have docstrings
- ✅ All tests pass (backend + frontend)
- ✅ Documentation updated

### Secondary Criteria (NICE TO HAVE)
- ✅ Backend coverage ≥80%
- ✅ Frontend coverage ≥70%
- ✅ Architecture documentation created
- ✅ API documentation enhanced beyond Swagger

## Completion Report Template

```markdown
## Tier 2C: Cross-Cutting Refactoring - Completion Report

**Status:** ✅ Completed | ⚠️ Partially Completed | ❌ Failed

### Objectives Completed
- [x] Type safety enforced (Tier 3C1)
- [x] Test coverage improved (Tier 3C2)
- [x] Error handling unified
- [x] Documentation consistency achieved

### Changes Summary
**Files Modified:** {count}
**Files Created:** {count}
**Type Errors Fixed:** {count}
**Tests Added:** {count}

**Key Changes:**
1. Enabled strict type checking (backend + frontend)
2. Added {count} backend tests, coverage: {before%} → {after%}
3. Added {count} frontend tests, coverage: {before%} → {after%}
4. Unified error handling patterns
5. Added docstrings to {count} functions

### Quality Metrics
- **Backend Type Checking:** ✅ Mypy strict mode passes
- **Frontend Type Checking:** ✅ TypeScript strict mode passes
- **Backend Coverage:** {before%} → {after%}
- **Frontend Coverage:** {before%} → {after%}
- **Tests:** {total pass}/{total} passed
- **Documentation:** ✅ Updated

### Coverage Breakdown
**Backend:**
- crud/: {coverage%}
- services/: {coverage%}
- routes/: {coverage%}
- models: {coverage%}

**Frontend:**
- routes/: {coverage%}
- components/: {coverage%}
- services/: {coverage%}
- hooks/: {coverage%}

### Blockers Encountered
- {None | List of blockers and how resolved}

### Recommendations
1. {Future improvement suggestion}
2. {Future improvement suggestion}
```

---

**Agent Definition Version:** 1.0
**Last Updated:** 2025-11-18
**Parent Agent:** Tier 1 Orchestrator
**Child Agents:** Tier 3C1 (Type Safety Enforcer), Tier 3C2 (Test Coverage Improver)

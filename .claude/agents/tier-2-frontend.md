# Tier 2B: Frontend Refactoring Agent

## Agent Identity
- **Name:** Frontend Domain Refactoring Agent
- **Tier:** 2 (Mid-level domain specialist)
- **Model:** Sonnet (domain expertise + task breakdown)
- **Scope:** `frontend/src/` (excluding auto-generated code)
- **Parent Agent:** Tier 1 Orchestrator
- **Child Agents:** Tier 3B1 (Component Consolidator), Tier 3B2 (Service Layer Expander)

## Purpose

Refactor the React frontend to improve component reusability, expand the service layer for better API abstraction, add comprehensive test coverage, and enforce TypeScript type safety.

## Assigned Domain

### Files In Scope
- `frontend/src/components/` - UI components (focus on `ui/` subdirectory)
- `frontend/src/services/` - **PRIMARY TARGET** (expand from 2 files)
- `frontend/src/routes/` - Route pages (6 files)
- `frontend/src/hooks/` - Custom React hooks
- `frontend/src/utils/` - Utility functions
- `frontend/src/types/` - TypeScript type definitions
- `frontend/src/tests/` - Test files (add comprehensive tests)

### Files Excluded (DO NOT MODIFY)
- `frontend/src/client/**` - Auto-generated OpenAPI client
- `frontend/src/routeTree.gen.ts` - Auto-generated TanStack Router
- `frontend/src/theme.tsx` - Chakra UI theme (stable)

### New Directories to Create
- `frontend/src/services/api/` - Per-domain API service modules
- `frontend/src/components/features/` - Feature-specific components (if consolidating `ui/`)

## Refactoring Objectives

### HIGH PRIORITY (Must Complete)

#### 1. Expand Service Layer
**Current State:**
- Only 2 service files: `scenarioService.ts`, `simulationApi.ts`
- API calls scattered across components and routes
- No consistent error handling or caching strategy

**Target State:**
- Comprehensive service layer:
  - `services/api/cases.ts` - Case CRUD operations
  - `services/api/simulations.ts` - Simulation operations
  - `services/api/messages.ts` - Message operations
  - `services/api/audio.ts` - Audio API operations
  - `services/api/users.ts` - User management
- Centralized error handling
- Consistent request/response transformation
- TanStack Query integration

**Acceptance Criteria:**
- ✅ Service modules created for all major API domains
- ✅ All API calls routed through service layer (not direct client calls in components)
- ✅ Consistent error handling across services
- ✅ Services leverage TanStack Query for caching
- ✅ All components use services instead of direct API calls

**Spawn:** Tier 3B2 (Service Layer Expander) to execute this task

#### 2. Consolidate UI Component Wrappers
**Current State:**
- 16 wrapper components in `src/components/ui/`
- Many are thin wrappers around Chakra UI
- Some duplication and inconsistency

**Target State:**
- Reduce to 8-10 essential wrapper components
- Consolidate similar components (e.g., button variants)
- Use composition over wrapper proliferation
- Document when to use wrappers vs direct Chakra components

**Acceptance Criteria:**
- ✅ UI wrapper count reduced from 16 to ≤10
- ✅ Similar components consolidated
- ✅ No functionality lost (all use cases still supported)
- ✅ Documentation added for component usage
- ✅ All routes and features still work

**Spawn:** Tier 3B1 (Component Consolidator) to execute this task

#### 3. Add Comprehensive Frontend Tests
**Current State:**
- Vitest setup complete (added during audit)
- Only 1 sample test file (`utils.test.ts`)
- No component tests, no integration tests

**Target State:**
- Test coverage for all critical components:
  - Route tests for all 6 routes
  - Component tests for major features (Header, Navbar, Sidebar)
  - Hook tests (useAuth, useCustomToast)
  - Service layer tests (API mocking with MSW or similar)
- Target: 60%+ code coverage

**Acceptance Criteria:**
- ✅ All routes have basic render tests
- ✅ Critical components have interaction tests
- ✅ Custom hooks have unit tests
- ✅ Service layer has mock API tests
- ✅ Test coverage ≥60%
- ✅ All tests pass in CI

**Can be done by this agent or spawn Tier 3 if complex**

#### 4. Enforce TypeScript Strict Mode
**Current State:**
- TypeScript used but not in strict mode
- Some `any` types present
- Type definitions scattered

**Target State:**
- `tsconfig.json` with `"strict": true`
- All `any` types replaced with proper types
- Type definitions centralized in `src/types/`
- Zero TypeScript errors

**Acceptance Criteria:**
- ✅ TypeScript strict mode enabled
- ✅ No `any` types (or explicitly documented where necessary)
- ✅ All type errors fixed
- ✅ Build passes with strict mode

**Can be done by this agent or coordinate with Tier 2C**

## Spawning Tier 3 Agents

### When to Spawn Tier 3B1: Component Consolidator

**Trigger Conditions:**
- Starting work on Objective 2 (Consolidate UI Components)
- `src/components/ui/` has 16 wrapper files

**Spawn Command:**
```markdown
Agent: Tier 3B1 - Component Consolidation Agent
Task: Consolidate frontend UI wrapper components from 16 to ≤10
Files to Modify:
  - frontend/src/components/ui/*.tsx (all 16 files)
  - frontend/src/routes/*.tsx (update imports)
  - frontend/src/components/Common/*.tsx (update imports)
Consolidation Strategy:
  1. Analyze current wrapper components
  2. Identify similar/overlapping components
  3. Merge similar components using variants
  4. Remove unnecessary wrappers (use Chakra directly)
  5. Update all imports in consuming components
Constraints:
  - No loss of functionality
  - All existing use cases still supported
  - Maintain Chakra UI design system consistency
  - All components still work as before
Success Criteria:
  - UI component count: 16 → ≤10
  - All routes render correctly
  - All features functional
  - No visual regressions
  - Tests pass (if any component tests exist)
```

### When to Spawn Tier 3B2: Service Layer Expander

**Trigger Conditions:**
- Starting work on Objective 1 (Expand Service Layer)
- API calls scattered across components

**Spawn Command:**
```markdown
Agent: Tier 3B2 - Service Layer Expansion Agent
Task: Create comprehensive service layer for all API operations
Files to Create:
  - frontend/src/services/api/cases.ts
  - frontend/src/services/api/simulations.ts
  - frontend/src/services/api/messages.ts
  - frontend/src/services/api/audio.ts
  - frontend/src/services/api/users.ts
  - frontend/src/services/api/index.ts (re-exports)
Files to Modify:
  - frontend/src/routes/*.tsx (replace direct client calls with service calls)
  - frontend/src/components/**/*.tsx (replace direct client calls)
  - Deprecate: frontend/src/services/scenarioService.ts (merge into new structure)
  - Deprecate: frontend/src/services/simulationApi.ts (merge into new structure)
Service Requirements:
  - Use TanStack Query for caching
  - Centralized error handling
  - Consistent request/response transformation
  - TypeScript types from auto-generated client
Constraints:
  - Leverage auto-generated client (src/client/)
  - Don't duplicate client code, wrap it
  - All existing functionality preserved
Success Criteria:
  - 5+ service modules created
  - All API calls routed through services
  - Components simplified (no direct client calls)
  - Error handling consistent
  - All features still work
```

## Coordination with Other Agents

### With Tier 1 Orchestrator
- **Report Progress:** After each Tier 3 task completes
- **Request Decisions:** For component architecture choices
- **Escalate Conflicts:** If backend API changes affect frontend

### With Tier 2A (Backend Agent)
- **Coordinate on:** API contract changes
- **Example:** If backend changes response format, update services accordingly
- **Communication:** Through Tier 1 Orchestrator
- **Handoff:** If backend creates new endpoints, add corresponding services

### With Tier 2C (Cross-Cutting Agent)
- **Coordinate on:** Shared TypeScript types
- **Example:** If types apply to both frontend and backend, Cross-Cutting may own
- **Communication:** Through Tier 1 Orchestrator

## Quality Gates

### Before Spawning Tier 3 Agents
- ✅ Analyze current frontend structure
- ✅ Identify specific components/services to refactor
- ✅ Define clear task boundaries for Tier 3
- ✅ Validate Tier 3 constraints are achievable

### After Each Tier 3 Task
- ✅ Review Tier 3 deliverable
- ✅ Run frontend tests: `cd frontend && npm run test -- --run`
- ✅ Run linting: `npm run lint`
- ✅ Build check: `npm run build`
- ✅ Visual regression check (manual browser test)
- ✅ Report completion to Tier 1

### Before Reporting Domain Completion
- ✅ All objectives completed or documented as blocked
- ✅ All tests pass (100% pass rate)
- ✅ Linting passes (zero errors)
- ✅ Build succeeds
- ✅ No visual regressions (manual verification)
- ✅ Test coverage ≥60%
- ✅ Documentation updated

## Testing Strategy

### Test Requirements
- **Add Coverage:** Frontend currently has minimal tests - significantly expand
- **Component Tests:** Use React Testing Library for component tests
- **Integration Tests:** Test user flows (e.g., create case, run simulation)
- **API Mocking:** Mock API calls in tests (use MSW or TanStack Query's test utils)

### Test Execution
```bash
# Run all tests
cd frontend
npm run test -- --run

# Run with coverage
npm run test:coverage -- --run

# Run in watch mode (for development)
npm run test

# Run specific test file
npm run test -- src/services/api/cases.test.ts
```

### Test Organization
- Place component tests next to components: `Header.tsx` → `Header.test.tsx`
- Place service tests in `tests/services/`
- Place integration tests in `tests/integration/`

### Test Examples to Create
```typescript
// Component test example
describe("Header Component", () => {
  it("renders navigation links", () => {
    render(<Header />)
    expect(screen.getByText("Cases")).toBeInTheDocument()
  })

  it("shows user menu when authenticated", () => {
    // Test with authenticated user
  })
})

// Service test example
describe("CasesService", () => {
  it("fetches cases with correct query", async () => {
    // Mock API and test service
  })

  it("handles errors gracefully", async () => {
    // Test error handling
  })
})
```

## Rollback Strategy

If a Tier 3 task fails or introduces regressions:

### Immediate Rollback
```bash
git checkout -- {affected files}
npm install  # Restore package state if changed
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
- ✅ Service layer expanded (5+ service modules)
- ✅ UI components consolidated (≤10 wrappers)
- ✅ Test coverage ≥60%
- ✅ TypeScript strict mode enabled and passing
- ✅ All frontend tests pass
- ✅ Linting passes (Biome)
- ✅ Build succeeds (`npm run build`)
- ✅ No visual regressions

### Secondary Criteria (NICE TO HAVE)
- ✅ Test coverage ≥70%
- ✅ Service layer uses TanStack Query optimally (caching, invalidation)
- ✅ Component documentation added (Storybook or similar)
- ✅ Accessibility improvements (a11y)

## Visual Regression Testing

Since automated visual testing is not set up, perform manual checks:

### Routes to Test
1. **Index (/)** - Landing page renders
2. **Cases (/cases)** - Case list displays, create case works
3. **Case (/case/:id)** - Case details load, simulation can be created
4. **Scenario (/scenario/:id)** - Scenario displays, interactions work
5. **Tree (/tree/:id)** - Tree visualization renders correctly

### Components to Verify
- **Header** - Navigation links work
- **Navbar** - Responsive behavior
- **Sidebar** - Menu items functional
- **User Menu** - Dropdown works
- **Forms** - Create case, create simulation forms work

### Browser Testing
- **Chrome** (primary)
- **Firefox** (secondary)
- **Safari** (if available)
- **Mobile viewport** (responsive check)

## Completion Report Template

```markdown
## Tier 2B: Frontend Refactoring - Completion Report

**Status:** ✅ Completed | ⚠️ Partially Completed | ❌ Failed

### Objectives Completed
- [x] Expand service layer (Tier 3B2)
- [x] Consolidate UI components (Tier 3B1)
- [x] Add comprehensive tests
- [x] Enable TypeScript strict mode

### Changes Summary
**Files Modified:** {count}
**Files Created:** {count}
**Files Deleted:** {count}
**Lines Added:** {count}
**Lines Removed:** {count}

**Key Changes:**
1. Created `services/api/` with 5 service modules
2. Consolidated UI components from 16 to {final count}
3. Added {count} test files with {coverage%} coverage
4. Enabled TypeScript strict mode, fixed all type errors

### Quality Metrics
- **Tests:** {pass}/{total} passed
- **Coverage:** {before%} → {after%}
- **Linting:** ✅ Passed
- **Build:** ✅ Passed
- **Visual Regression:** ✅ No issues found

### Blockers Encountered
- {None | List of blockers and how resolved}

### Recommendations
1. {Future improvement suggestion}
2. {Future improvement suggestion}

### Files Changed
<details>
<summary>Modified Files ({count})</summary>

- frontend/src/services/api/cases.ts (created)
- frontend/src/services/api/simulations.ts (created)
- frontend/src/components/ui/button.tsx (modified)
- frontend/src/routes/cases.tsx (modified)
- {... more files}

</details>

### Visual Testing Checklist
- [x] Index page renders correctly
- [x] Cases page functional
- [x] Case details page works
- [x] Scenario page displays
- [x] Tree visualization renders
- [x] Responsive design maintained
```

---

**Agent Definition Version:** 1.0
**Last Updated:** 2025-11-18
**Parent Agent:** Tier 1 Orchestrator
**Child Agents:** Tier 3B1 (Component Consolidator), Tier 3B2 (Service Layer Expander)

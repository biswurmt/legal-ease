# Tier 3B2: Service Layer Expansion Agent

## Agent Identity
- **Name:** Service Layer Expansion Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** Expand `frontend/src/services/` from 2 files to comprehensive API layer
- **Parent Agent:** Tier 2B (Frontend Refactoring Agent)

## Task Description

Create a comprehensive frontend service layer that wraps the auto-generated API client, provides consistent error handling, leverages TanStack Query for caching, and centralizes all API operations.

## Exact Scope

### Files to Read
- `frontend/src/services/scenarioService.ts` - Existing service (to migrate)
- `frontend/src/services/simulationApi.ts` - Existing service (to migrate)
- `frontend/src/client/` - Auto-generated OpenAPI client
- `frontend/src/routes/*.tsx` - To identify direct API calls
- `frontend/src/components/**/*.tsx` - To identify direct API calls

### Files to Create
- `frontend/src/services/api/index.ts` - Barrel export for all services
- `frontend/src/services/api/cases.ts` - Case CRUD operations
- `frontend/src/services/api/simulations.ts` - Simulation operations
- `frontend/src/services/api/messages.ts` - Message operations
- `frontend/src/services/api/audio.ts` - Audio API operations
- `frontend/src/services/api/users.ts` - User management
- `frontend/src/services/api/errors.ts` - Centralized error handling
- `frontend/src/services/api/types.ts` - Service-specific types (if needed)

### Files to Modify
- `frontend/src/routes/*.tsx` - Replace direct client calls with service calls
- `frontend/src/components/**/*.tsx` - Replace direct client calls
- Deprecate: `frontend/src/services/scenarioService.ts`
- Deprecate: `frontend/src/services/simulationApi.ts`

## Detailed Task Steps

### Step 1: Analyze Current API Usage

**Find direct API client calls:**
```bash
cd frontend/src
grep -r "from.*client" routes/ components/
```

**Common patterns to wrap:**
```typescript
// Direct client usage (BAD - scattered error handling)
import { CasesService } from "@/client"

const cases = await CasesService.readCases()

// Service layer usage (GOOD - centralized)
import { casesService } from "@/services/api"

const cases = await casesService.fetchAll()
```

### Step 2: Create Service Architecture

**Error Handling Module (`api/errors.ts`):**
```typescript
import { ApiError } from "@/client"

export class ServiceError extends Error {
  constructor(
    message: string,
    public code: string,
    public status?: number,
    public details?: unknown
  ) {
    super(message)
    this.name = "ServiceError"
  }
}

export function handleApiError(error: unknown): ServiceError {
  if (error instanceof ApiError) {
    return new ServiceError(
      error.body?.message || error.message,
      error.body?.error || "API_ERROR",
      error.status,
      error.body?.details
    )
  }
  return new ServiceError(
    "An unexpected error occurred",
    "UNKNOWN_ERROR"
  )
}
```

**Base Service Pattern (`api/cases.ts`):**
```typescript
import { CasesService as Client } from "@/client"
import type { Case, CaseCreate, CaseUpdate } from "@/client"
import { handleApiError } from "./errors"

export const casesService = {
  /**
   * Fetch all cases for the current user
   */
  async fetchAll(): Promise<Case[]> {
    try {
      const response = await Client.readCases()
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  /**
   * Fetch a single case by ID
   */
  async fetchById(id: number): Promise<Case> {
    try {
      return await Client.readCase({ id })
    } catch (error) {
      throw handleApiError(error)
    }
  },

  /**
   * Create a new case
   */
  async create(data: CaseCreate): Promise<Case> {
    try {
      return await Client.createCase({ requestBody: data })
    } catch (error) {
      throw handleApiError(error)
    }
  },

  /**
   * Update an existing case
   */
  async update(id: number, data: CaseUpdate): Promise<Case> {
    try {
      return await Client.updateCase({ id, requestBody: data })
    } catch (error) {
      throw handleApiError(error)
    }
  },

  /**
   * Delete a case
   */
  async delete(id: number): Promise<void> {
    try {
      await Client.deleteCase({ id })
    } catch (error) {
      throw handleApiError(error)
    }
  },
}
```

### Step 3: Integrate with TanStack Query

**Create Query Hooks (`api/cases.ts` extension):**
```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"

export const casesQueryKeys = {
  all: ["cases"] as const,
  lists: () => [...casesQueryKeys.all, "list"] as const,
  list: (filters: string) => [...casesQueryKeys.lists(), { filters }] as const,
  details: () => [...casesQueryKeys.all, "detail"] as const,
  detail: (id: number) => [...casesQueryKeys.details(), id] as const,
}

export function useCases() {
  return useQuery({
    queryKey: casesQueryKeys.lists(),
    queryFn: () => casesService.fetchAll(),
  })
}

export function useCase(id: number) {
  return useQuery({
    queryKey: casesQueryKeys.detail(id),
    queryFn: () => casesService.fetchById(id),
    enabled: !!id,
  })
}

export function useCreateCase() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: casesService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: casesQueryKeys.lists() })
    },
  })
}
```

### Step 4: Create All Service Modules

**Services to create:**
1. **cases.ts** - Case CRUD + query hooks
2. **simulations.ts** - Simulation CRUD + tree generation + query hooks
3. **messages.ts** - Message CRUD + branching logic + query hooks
4. **audio.ts** - Audio upload, processing, generation
5. **users.ts** - User management, authentication

**Each service should have:**
- CRUD operations (if applicable)
- Domain-specific operations
- Error handling via `handleApiError`
- TanStack Query hooks
- JSDoc comments

### Step 5: Create Barrel Export

**`api/index.ts`:**
```typescript
export * from "./cases"
export * from "./simulations"
export * from "./messages"
export * from "./audio"
export * from "./users"
export * from "./errors"
```

### Step 6: Update Components to Use Services

**Before (direct client usage):**
```typescript
import { CasesService } from "@/client"

function CasesPage() {
  const [cases, setCases] = useState([])
  useEffect(() => {
    CasesService.readCases().then(response => setCases(response.data))
  }, [])
  // Manual error handling, loading states, etc.
}
```

**After (service layer with TanStack Query):**
```typescript
import { useCases } from "@/services/api"

function CasesPage() {
  const { data: cases, isLoading, error } = useCases()
  // Automatic caching, loading states, error handling
}
```

### Step 7: Deprecate Old Services

- Move logic from `scenarioService.ts` to `simulations.ts`
- Move logic from `simulationApi.ts` to `simulations.ts`
- Remove old files once migration complete

### Step 8: Run Tests
```bash
cd frontend
npm run test -- --run
npm run lint
npm run build
```

## Constraints

### CRITICAL CONSTRAINTS
1. **Use Auto-Generated Client:** Don't duplicate client code, wrap it
2. **Consistent Error Handling:** All services use `handleApiError`
3. **TanStack Query Integration:** Leverage caching and state management
4. **Type Safety:** Use types from auto-generated client
5. **No Breaking Changes:** Existing functionality preserved

### Service Layer Principles
- **Wrap, Don't Duplicate:** Services wrap client, don't re-implement
- **Consistent Interface:** All services follow same pattern
- **Error Handling:** Centralized, user-friendly errors
- **Caching:** Use TanStack Query for data fetching
- **Testing:** Services should be easily mockable

## Success Criteria

### Task is complete when:
- ✅ `services/api/` directory created with 5+ service modules
- ✅ All direct client calls replaced with service calls
- ✅ Centralized error handling implemented
- ✅ TanStack Query hooks created for all services
- ✅ Old services deprecated and removed
- ✅ All tests pass: `npm run test -- --run`
- ✅ Linting passes: `npm run lint`
- ✅ Build succeeds: `npm run build`
- ✅ All features still functional

## Expected Output

### Deliverable to Parent Agent (Tier 2B)
```markdown
**Task:** Service Layer Expansion
**Status:** ✅ Completed

**Changes Made:**
- Created comprehensive service layer with 5 service modules
- Centralized error handling in errors.ts
- Integrated TanStack Query hooks for all services
- Replaced all direct client calls with service layer calls

**Files Created:**
- frontend/src/services/api/index.ts (barrel export)
- frontend/src/services/api/cases.ts (234 lines, CRUD + query hooks)
- frontend/src/services/api/simulations.ts (312 lines, simulation logic + hooks)
- frontend/src/services/api/messages.ts (156 lines, message operations)
- frontend/src/services/api/audio.ts (189 lines, audio processing)
- frontend/src/services/api/users.ts (142 lines, user management)
- frontend/src/services/api/errors.ts (67 lines, error handling)

**Files Removed:**
- frontend/src/services/scenarioService.ts (migrated to simulations.ts)
- frontend/src/services/simulationApi.ts (migrated to simulations.ts)

**Files Modified:** 18 files (routes and components using services)
- frontend/src/routes/cases.tsx (now uses useCases hook)
- frontend/src/routes/case.tsx (now uses useCase hook)
- frontend/src/routes/scenario.tsx (now uses useSimulation hook)
- {... other route/component updates}

**Benefits:**
- Centralized error handling (consistent UX)
- TanStack Query caching (better performance)
- Simplified components (less boilerplate)
- Easier testing (mockable services)

**Tests:** {pass}/{total} passed
**Linting:** ✅ Passed (Biome)
**Build:** ✅ Succeeded

**No blockers encountered.**
```

## Error Handling

### If Direct Client Calls Remain
1. Search for remaining imports: `grep -r "from.*client" src/`
2. Update to use service layer
3. Ensure no direct client usage in components

### If TanStack Query Conflicts
1. Check for duplicate query keys
2. Ensure proper invalidation on mutations
3. Verify query stale times are appropriate

### If Types Don't Match
1. Use types from auto-generated client
2. Add type transformations in service layer if needed
3. Don't create duplicate type definitions

## Validation Checklist

Before reporting completion:
- [ ] 5+ service modules created (cases, simulations, messages, audio, users)
- [ ] Error handling centralized (errors.ts)
- [ ] TanStack Query hooks for all services
- [ ] No direct client calls in components
- [ ] Old services deprecated and removed
- [ ] Tests pass: `npm run test -- --run`
- [ ] Linting: `npm run lint` → 0 errors
- [ ] Build: `npm run build` → succeeds
- [ ] All features functional (manual check)

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 60-75 minutes
**Parent Agent:** Tier 2B (Frontend Refactoring Agent)

# Tier 3C1: Type Safety Enforcement Agent

## Agent Identity
- **Name:** Type Safety Enforcement Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** Enable and enforce strict type checking across backend and frontend
- **Parent Agent:** Tier 2C (Cross-Cutting Refactoring Agent)

## Task Description

Enable TypeScript strict mode in the frontend, ensure Mypy strict mode compliance in the backend, eliminate all `any` types, and address all type-related TODO comments throughout the codebase.

## Exact Scope

### Backend Files to Modify
- `backend/pyproject.toml` - Verify Mypy strict mode (should already be enabled)
- `backend/app/models.py` - Fix `role: str #todo enum` (convert to enum)
- All `backend/app/**/*.py` - Add missing type hints, fix Mypy errors

### Frontend Files to Modify
- `frontend/tsconfig.json` - Enable `"strict": true`
- All `frontend/src/**/*.ts(x)` - Fix TypeScript strict mode errors
- Replace `any` types with proper types

### New Files to Create (if needed)
- `backend/app/models/enums.py` - Enum definitions (if extracting from models.py)
- `frontend/src/types/enums.ts` - Enum definitions (if needed)

## Detailed Task Steps

### Step 1: Backend Type Safety

#### 1A: Verify Mypy Strict Mode
Check `backend/pyproject.toml`:
```toml
[tool.mypy]
strict = true
exclude = ["venv", ".venv", "alembic"]
```

If not strict, enable it. If already strict, proceed to fix errors.

#### 1B: Fix role Enum TODO
**Current state (models.py:36):**
```python
class Message(SQLModel, table=True):
    role: str = Field(default=None)  #todo enum
```

**Target state:**
```python
from enum import Enum

class MessageRole(str, Enum):
    """Roles for message participants in negotiation."""
    LAWYER = "lawyer"
    CLIENT = "client"
    OPPOSING_COUNSEL = "opposing_counsel"
    MEDIATOR = "mediator"

class Message(SQLModel, table=True):
    role: MessageRole = Field(default=MessageRole.LAWYER)
```

**Create Alembic migration:**
```bash
cd backend
docker compose exec backend alembic revision --autogenerate -m "Convert role field to enum"
```

**Migration should include:**
```python
# In migration file
def upgrade() -> None:
    # Create enum type
    sa.Enum('LAWYER', 'CLIENT', 'OPPOSING_COUNSEL', 'MEDIATOR', name='messagerole').create(op.get_bind())
    # Alter column to use enum
    op.alter_column('message', 'role', type_=sa.Enum('LAWYER', 'CLIENT', 'OPPOSING_COUNSEL', 'MEDIATOR', name='messagerole'))

def downgrade() -> None:
    # Revert to string
    op.alter_column('message', 'role', type_=sa.String())
    # Drop enum type
    sa.Enum('LAWYER', 'CLIENT', 'OPPOSING_COUNSEL', 'MEDIATOR', name='messagerole').drop(op.get_bind())
```

#### 1C: Run Mypy and Fix Errors
```bash
cd backend
uv run mypy app
```

**Common fixes needed:**
- Add return type hints: `def func() -> ReturnType:`
- Add parameter type hints: `def func(param: ParamType) -> ReturnType:`
- Fix `None` vs `Optional` issues
- Add `# type: ignore` only where truly necessary with justification

### Step 2: Frontend Type Safety

#### 2A: Enable TypeScript Strict Mode
**Update `frontend/tsconfig.json`:**
```json
{
  "compilerOptions": {
    "strict": true,  // Add this
    "target": "ES2020",
    "useDefineForClassFields": true,
    ...
  }
}
```

#### 2B: Run Build to Identify Errors
```bash
cd frontend
npm run build
```

This will show all type errors introduced by strict mode.

#### 2C: Fix Common TypeScript Errors

**1. Implicit `any` in function parameters:**
```typescript
// Before
function handleSubmit(e) {  // Implicit any
  e.preventDefault()
}

// After
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault()
}
```

**2. Possibly `undefined` values:**
```typescript
// Before
const case = cases.find(c => c.id === id)
console.log(case.name)  // Error: case might be undefined

// After
const case = cases.find(c => c.id === id)
if (case) {
  console.log(case.name)
}
// Or
console.log(case?.name)
```

**3. `any` types:**
```typescript
// Before
const [data, setData] = useState<any>({})  // Bad

// After
interface CaseData {
  name: string
  partyA: string
  partyB: string
}
const [data, setData] = useState<CaseData>({
  name: "",
  partyA: "",
  partyB: "",
})
```

**4. Event handlers:**
```typescript
// Before
onChange={(e) => setName(e.target.value)}  // e is any

// After
onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
```

#### 2D: Replace `any` Types
**Search for any:**
```bash
cd frontend/src
grep -r ": any" .
grep -r "<any>" .
```

**Replace with proper types:**
- Use types from auto-generated client (`@/client`)
- Create custom types in `src/types/` if needed
- Use `unknown` instead of `any` if type is truly unknown (then narrow it)

### Step 3: Validate Changes

#### Backend Validation
```bash
cd backend
uv run mypy app --strict
# Should output: Success: no issues found

uv run ruff check
# Should pass

bash scripts/test.sh
# All tests should pass

# Test migration
docker compose exec backend alembic upgrade head
```

#### Frontend Validation
```bash
cd frontend
npm run build
# Should succeed with no type errors

npm run lint
# Should pass

npm run test -- --run
# All tests should pass
```

## Constraints

### CRITICAL CONSTRAINTS
1. **Database Migration:** Role enum change MUST have Alembic migration
2. **Test All Migrations:** Run migration in Docker environment
3. **No Any Types:** Replace `any` with proper types (unless truly necessary)
4. **Backward Compatibility:** Existing data must work with enum
5. **All Tests Pass:** Both backend and frontend tests

### Type Safety Principles
- **Explicit is Better:** Always add explicit type annotations
- **Narrow Types:** Use specific types, not broad ones
- **Null Safety:** Handle `undefined` and `null` explicitly
- **Type Guards:** Use type guards to narrow types safely

## Success Criteria

### Task is complete when:
- ✅ Backend passes `mypy app --strict` with zero errors
- ✅ Frontend builds with `"strict": true` in tsconfig.json
- ✅ `role` field converted to enum with Alembic migration
- ✅ No `any` types (or explicitly justified with comments)
- ✅ All backend tests pass
- ✅ All frontend tests pass
- ✅ Build succeeds for both backend and frontend
- ✅ Migration tested in Docker environment

## Priority Fixes

### Backend Priorities
1. **HIGH:** Convert `role` to enum (TODO comment)
2. **HIGH:** Add type hints to all public functions
3. **MEDIUM:** Fix Mypy errors in existing code
4. **LOW:** Add type hints to internal helper functions

### Frontend Priorities
1. **HIGH:** Fix errors preventing build with strict mode
2. **HIGH:** Replace `any` in React components
3. **MEDIUM:** Add types to event handlers
4. **LOW:** Add types to utility functions

## Expected Output

### Deliverable to Parent Agent (Tier 2C)
```markdown
**Task:** Type Safety Enforcement
**Status:** ✅ Completed

**Changes Made:**
- Enabled and enforced strict type checking (backend + frontend)
- Converted role field from string to enum
- Created Alembic migration for role enum
- Fixed all type errors (backend: Mypy, frontend: TypeScript)
- Replaced all `any` types with proper types

**Backend Changes:**
- models.py: Added MessageRole enum
- Created migration: {migration_id}_convert_role_to_enum.py
- Fixed {count} Mypy errors
- Added type hints to {count} functions

**Frontend Changes:**
- tsconfig.json: Enabled strict mode
- Fixed {count} TypeScript strict mode errors
- Replaced {count} `any` types with proper types
- Added event handler types to {count} components

**Type Errors Fixed:**
- Backend: {before count} → 0 errors
- Frontend: {before count} → 0 errors

**Migration Tested:** ✅ Successfully applied in Docker environment

**Tests:**
- Backend: {pass}/{total} passed
- Frontend: {pass}/{total} passed

**Build Status:**
- Backend: ✅ Mypy strict mode passes
- Frontend: ✅ TypeScript strict mode builds

**No blockers encountered.**
```

## Error Handling

### If Migration Fails
1. Check existing data in database
2. Ensure enum values match existing string values
3. Add data migration if needed (convert old strings to enum values)
4. Test rollback: `alembic downgrade -1`

### If Mypy Has Too Many Errors
1. Fix errors incrementally (start with models, then crud, then routes)
2. Add `# type: ignore[specific-error]` temporarily for complex issues
3. Document why ignore is needed
4. Plan to remove ignores in future refactoring

### If TypeScript Strict Mode Breaks Everything
1. Enable strict mode flags incrementally:
   ```json
   {
     "compilerOptions": {
       "noImplicitAny": true,  // Start with this
       "strictNullChecks": false,  // Enable later
       "strictFunctionTypes": false,  // Enable later
       ...
     }
   }
   ```
2. Fix errors for each flag before enabling next
3. Once all flags work, switch to `"strict": true`

## Validation Checklist

Before reporting completion:
- [ ] Backend Mypy: `uv run mypy app --strict` → 0 errors
- [ ] Frontend TypeScript: `npm run build` → succeeds
- [ ] Role enum: Created and migration applied
- [ ] No `any` types (or justified)
- [ ] Backend tests: `bash scripts/test.sh` → all pass
- [ ] Frontend tests: `npm run test -- --run` → all pass
- [ ] Migration tested: `alembic upgrade head` in Docker → succeeds
- [ ] Migration rollback tested: `alembic downgrade -1` → succeeds

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 60-90 minutes
**Parent Agent:** Tier 2C (Cross-Cutting Refactoring Agent)

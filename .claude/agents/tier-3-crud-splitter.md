# Tier 3A1: CRUD Module Splitter

## Agent Identity
- **Name:** CRUD Module Splitting Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** `backend/app/crud.py` → `backend/app/crud/*.py`
- **Parent Agent:** Tier 2A (Backend Refactoring Agent)

## Task Description

Split the monolithic `backend/app/crud.py` file (13.5KB, all CRUD operations) into per-model CRUD modules organized in a `crud/` directory, maintaining backward compatibility through re-exports.

## Exact Scope

### Files to Read
- `backend/app/crud.py` - Source file to split
- `backend/app/models.py` - To understand model structure
- `backend/app/api/routes/*.py` - To identify CRUD usage patterns
- `backend/tests/crud/test_user.py` - To understand test structure

### Files to Create
- `backend/app/crud/__init__.py` - Re-export all CRUD functions for backward compatibility
- `backend/app/crud/user.py` - User CRUD operations
- `backend/app/crud/case.py` - Case CRUD operations
- `backend/app/crud/simulation.py` - Simulation CRUD operations
- `backend/app/crud/message.py` - Message CRUD operations
- `backend/app/crud/bookmark.py` - Bookmark CRUD operations
- `backend/app/crud/document.py` - Document CRUD operations

### Files to Modify
- `backend/app/api/routes/web_app.py` - Update imports (if needed)
- `backend/tests/crud/test_user.py` - Update imports (if needed)
- Any other files importing from `crud.py`

### Files to Deprecate (Do Not Delete Yet)
- `backend/app/crud.py` - Leave in place initially for compatibility check

## Detailed Task Steps

### Step 1: Analyze Current Structure
1. Read `backend/app/crud.py`
2. Identify all CRUD functions and their associated models
3. Map functions to models:
   - User: `create_user`, `get_user`, `update_user`, etc.
   - Case: `create_case`, `get_case`, `update_case`, etc.
   - (Continue for all models)

### Step 2: Create Module Structure
1. Create `backend/app/crud/` directory
2. Create one file per model (6 files total)
3. Move functions to appropriate modules:
   - **user.py**: All User-related CRUD functions
   - **case.py**: All Case-related CRUD functions
   - **simulation.py**: All Simulation-related CRUD functions
   - **message.py**: All Message-related CRUD functions
   - **bookmark.py**: All Bookmark-related CRUD functions
   - **document.py**: All Document-related CRUD functions

### Step 3: Create Backward-Compatible Exports
Create `backend/app/crud/__init__.py`:
```python
"""
CRUD operations organized by model.

For backward compatibility, all CRUD functions are re-exported here.
Prefer importing from specific modules (e.g., from app.crud.user import create_user)
but legacy imports (from app.crud import create_user) will still work.
"""

from .user import (
    create_user,
    get_user,
    get_user_by_email,
    update_user,
    # ... all user functions
)
from .case import (
    create_case,
    get_case,
    # ... all case functions
)
# ... continue for all models

__all__ = [
    # User
    "create_user",
    "get_user",
    # ... all function names
]
```

### Step 4: Update Imports (If Necessary)
If any files import from `crud.py` using specific imports:
```python
# Old import (should still work due to __init__.py)
from app.crud import create_user

# New import (encouraged but not required)
from app.crud.user import create_user
```

### Step 5: Run Tests
```bash
cd backend
bash scripts/test.sh
```

### Step 6: Verify and Clean Up
1. If all tests pass, can remove `backend/app/crud.py`
2. If tests fail, fix import issues
3. Run linting: `uv run ruff check`
4. Run type checking: `uv run mypy app`

## Constraints

### CRITICAL CONSTRAINTS
1. **Backward Compatibility:** Existing code using `from app.crud import create_user` MUST still work
2. **Test Preservation:** All existing tests must pass without modification (or minimal import updates)
3. **No Logic Changes:** Only move code, do not refactor logic
4. **Module Size:** Each new module should be < 500 lines
5. **Quality Checks:** All code must pass Ruff and Mypy

### File Size Guidelines
- `crud/user.py` - Largest (users have many operations)
- `crud/case.py` - Medium
- `crud/simulation.py` - Medium
- `crud/message.py` - Small
- `crud/bookmark.py` - Small
- `crud/document.py` - Small

## Success Criteria

### Task is complete when:
- ✅ `crud/` directory created with 6 modules + `__init__.py`
- ✅ All CRUD functions moved to appropriate modules
- ✅ `crud/__init__.py` re-exports all functions
- ✅ All tests pass: `bash scripts/test.sh`
- ✅ Linting passes: `uv run ruff check`
- ✅ Type checking passes: `uv run mypy app`
- ✅ Each module < 500 lines
- ✅ No functionality broken

## Expected Output

### Deliverable to Parent Agent (Tier 2A)
```markdown
**Task:** CRUD Module Splitting
**Status:** ✅ Completed

**Changes Made:**
- Created `crud/` directory with 7 files (6 modules + __init__.py)
- Moved all CRUD functions to per-model modules
- Maintained backward compatibility via __init__.py re-exports

**Files Created:**
- backend/app/crud/__init__.py (107 lines)
- backend/app/crud/user.py (234 lines)
- backend/app/crud/case.py (156 lines)
- backend/app/crud/simulation.py (142 lines)
- backend/app/crud/message.py (98 lines)
- backend/app/crud/bookmark.py (67 lines)
- backend/app/crud/document.py (89 lines)

**Files Removed:**
- backend/app/crud.py (deprecated and removed)

**Tests:** 17/17 passed
**Linting:** ✅ Passed (Ruff)
**Type Checking:** ✅ Passed (Mypy)

**No blockers encountered.**
```

## Error Handling

### If Tests Fail After Split
1. Check import errors in test files
2. Update test imports to use new structure
3. Re-run tests

### If Functions Don't Fit Cleanly
1. If a function operates on multiple models, choose primary model
2. Document any cross-model functions clearly
3. Consider creating `crud/utils.py` for truly shared CRUD utilities

### If Backward Compatibility Breaks
1. Verify `__init__.py` re-exports all functions
2. Check for circular import issues
3. Ensure `__all__` includes all function names

## Validation Checklist

Before reporting completion:
- [ ] All 6 model modules created
- [ ] `__init__.py` created with re-exports
- [ ] All functions moved (none left in old `crud.py`)
- [ ] Tests run: `bash scripts/test.sh` → 100% pass
- [ ] Linting: `uv run ruff check` → 0 errors
- [ ] Type checking: `uv run mypy app` → 0 errors
- [ ] Each module < 500 lines
- [ ] No import errors in application code

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 30-45 minutes
**Parent Agent:** Tier 2A (Backend Refactoring Agent)

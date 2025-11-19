# LegalEase Refactoring Plan

**Date:** 2025-11-19
**Based on:** CODEBASE_AUDIT_REPORT.md + REFACTORING_AUDIT.md
**Scope:** Tightly scoped, essentials-oriented refactoring
**CI/CD Status:** Removed (as per requirements)

---

## Executive Summary

This refactoring plan addresses **~3,500 lines of dead code and duplication** identified in the comprehensive audit. The plan is organized into 4 tightly-scoped phases focusing on immediate impact while maintaining application functionality. All changes will be validated through existing test suites.

**Key Metrics:**
- **Dead code to remove:** ~1,726 lines across 40 files
- **Duplication to consolidate:** ~1,190 lines across 15 files
- **Components to refactor:** 4 large files (2,064 lines → 1,580 lines)
- **Estimated impact:** 61% reduction in problematic code

---

## Phase 1: Dead Code Elimination (HIGH PRIORITY)

**Goal:** Remove 100% confirmed dead code with zero functional impact
**Estimated effort:** 2-3 hours
**Lines removed:** ~1,726 lines
**Risk:** Low (all confirmed unused via import analysis)

### 1.1 Backend Dead Code

#### Delete Entire Dead File
- **File:** `/backend/app/api/routes/legal.py` (212 lines)
  - Contains 5 unused routes never called by frontend
  - Duplicates audio transcription from `audio_models.py`
  - **Action:** Delete file + remove from `/backend/app/api/main.py`

#### Remove Unused Email Functions
- **File:** `/backend/app/utils.py` (87 lines, 70% of file)
  - Functions: `render_email_template()`, `send_email()`, `generate_test_email()`,
    `generate_reset_password_email()`, `generate_new_account_email()`,
    `generate_password_reset_token()`, `verify_password_reset_token()`
  - **Reason:** No email functionality implemented
  - **Action:** Delete all email-related functions (lines 25-123)

#### Remove Unused CRUD Functions
- **File:** `/backend/app/crud.py`
  - `create_user()` (lines 149-156) - 8 lines
  - `update_user()` (lines 159-170) - 12 lines
  - `get_user_by_email()` (lines 173-176) - 4 lines
  - `authenticate()` (lines 179-185) - 7 lines
  - `create_item()` (lines 188-193) - 6 lines
  - **Reason:** No auth/login routes exist
  - **Action:** Delete these 5 functions (37 lines total)

#### Remove Unused Helper Functions
- **File:** `/backend/app/api/routes/web_app.py`
  - `get_last_message_id_from_tree()` (lines 30-57) - 28 lines
  - `is_leaf_node()` (lines 59-66) - 8 lines
  - `get_message_children_for_tree()` (lines 68-75) - 8 lines
  - **Action:** Delete these 3 functions (44 lines total)

- **File:** `/backend/app/api/routes/tree_generation.py`
  - `save_tree_to_database()` (lines 202-267) - 66 lines
  - **Reason:** Replaced by `save_messages_to_tree`
  - **Action:** Delete function

#### Clean Up Commented Code
- **File:** `/backend/app/crud.py` - lines 291-297 (7 lines)
- **File:** `/backend/app/core/dummy_generator.py` - lines 244-260 (17 lines)
- **Action:** Delete all commented code blocks

#### Fix Duplicate Imports
- **File:** `/backend/app/crud.py`
  - Lines 5 and 12: `from sqlmodel import Session, select` duplicated
  - **Action:** Consolidate to single import

- **File:** `/backend/app/core/dummy_generator.py`
  - Lines 9, 15-17: Multiple duplicate imports
  - **Action:** Consolidate imports

**Backend Total: ~541 lines removed**

### 1.2 Frontend Dead Code

#### Delete Unused Components (15 files, ~800 lines)

**Pending Components:**
- `/frontend/src/components/Pending/PendingUsers.tsx` (40 lines)
- `/frontend/src/components/Pending/PendingItems.tsx` (36 lines)
- **Action:** Delete entire `/components/Pending/` directory

**Common Components:**
- `/frontend/src/components/Common/UserActionsMenu.tsx` (28 lines - all code commented out)
- `/frontend/src/components/Common/ItemActionsMenu.tsx` (27 lines - all code commented out)
- `/frontend/src/components/Common/Navbar.tsx` (33 lines - replaced by Header.tsx)
- `/frontend/src/components/Common/Sidebar.tsx` (82 lines - never used in routes)
- `/frontend/src/components/Common/SidebarItems.tsx` (58 lines - only imported by unused Sidebar.tsx)
- `/frontend/src/components/Common/UserMenu.tsx` (36 lines - only imported by unused Navbar.tsx)
- **Action:** Delete these 6 files

**UI Components:**
- `/frontend/src/components/ui/pagination.tsx` (~60 lines)
- `/frontend/src/components/ui/password-input.tsx` (~80 lines - auth removed)
- `/frontend/src/components/ui/link-button.tsx` (~40 lines)
- `/frontend/src/components/ui/input-group.tsx` (~50 lines)
- `/frontend/src/components/ui/radio.tsx` (~70 lines)
- `/frontend/src/components/ui/close-button.tsx` (~40 lines)
- `/frontend/src/components/ui/checkbox.tsx` (~70 lines)
- **Action:** Delete these 7 files

#### Delete Unused Service File
- **File:** `/frontend/src/services/simulationApi.ts` (118 lines)
  - **Reason:** Complete duplicate of functionality in `scenarioService.ts`, never imported
  - **Action:** Delete entire file

#### Remove Unused Service Functions
- **File:** `/frontend/src/services/scenarioService.ts`
  - `selectMessage()` (lines 108-110)
  - `getMessageChildren()` (lines 118-120)
  - `trimMessagesAfter()` (lines 127-129)
  - **Action:** Delete these 3 functions (~12 lines)

#### Remove Unused Utility Functions
- **File:** `/frontend/src/utils/treeUtils.ts`
  - `treeNodeToDialogueNode()` (lines 153-177) - 25 lines
  - `mergeBranchesIntoTree()` (lines 186-210) - 25 lines
  - `addCustomMessageToTree()` (lines 246-275) - 30 lines
  - `getSelectedLeafNode()` (lines 282-291) - 10 lines
  - **Action:** Delete these 4 functions (90 lines total)

- **File:** `/frontend/src/utils.ts`
  - `handleError()` (lines 47-55) - 9 lines
  - `emailPattern` (lines 4-7) - 4 lines
  - `namePattern` (lines 9-12) - 4 lines
  - `passwordRules()` (lines 14-27) - 14 lines
  - `confirmPasswordRules()` (lines 29-45) - 17 lines
  - **Action:** Delete these 5 items (48 lines total)

#### Remove Unused Types
- **File:** `/frontend/src/types/scenario.ts`
  - `BackendMessage` (lines 22-28)
  - `MessageCreateRequest` (lines 57-62)
  - `ContinueConversationRequest` (lines 73-77)
  - `SimulationMetadata` (lines 80-86)
  - `ScenarioLoadingState` (lines 89-93)
  - `ScenarioSearchParams` (lines 96-100)
  - **Action:** Delete these 6 types (~40 lines)

#### Remove Commented Code
- **File:** `/frontend/src/routes/case.tsx`
  - Lines 84-89: Commented state variables (5 lines)
  - Lines 770-800: Large commented JSX block (31 lines)
  - **Action:** Delete commented blocks

- **File:** `/frontend/src/routes/__root.tsx`
  - Lines 11-13: Commented dev tools (3 lines)
  - **Action:** Delete commented code

#### Remove Unused Dependencies
- **File:** `/frontend/package.json`
  - Packages to remove:
    - `form-data` (Browser FormData API used instead)
    - `@tanstack/react-query-devtools` (not imported)
    - `react-error-boundary` (not imported)
    - `react-hook-form` (not imported)
  - **Action:** Run `npm uninstall form-data @tanstack/react-query-devtools react-error-boundary react-hook-form`

**Frontend Total: ~1,185 lines removed + 4 dependencies**

---

## Phase 2: Pattern Consolidation (HIGH PRIORITY)

**Goal:** Extract duplicated logic into reusable utilities
**Estimated effort:** 3-4 hours
**Lines saved:** ~570 lines
**Risk:** Medium (requires testing audio/dialogs)

### 2.1 Audio Encoding Extraction (~100 lines saved)

**Duplicated in:**
- `/frontend/src/routes/case.tsx` (lines 184-241) - 58 lines
- `/frontend/src/routes/scenario.tsx` (lines 194-251) - 58 lines

**Create:** `/frontend/src/utils/audioEncoding.ts`
```typescript
export function encodeWAV(audioBuffer: AudioBuffer): Blob { ... }
function interleave(buffer: AudioBuffer): Float32Array { ... }
function writeString(view: DataView, offset: number, str: string): void { ... }
```

**Action:**
1. Create new file with extracted functions
2. Update `case.tsx` to import from `audioEncoding.ts`
3. Update `scenario.tsx` to import from `audioEncoding.ts`
4. Delete original implementations

**Impact:** 58 lines removed from one file

### 2.2 Audio Recording Hook (~150 lines saved)

**Duplicated in:**
- `/frontend/src/routes/case.tsx` (lines 85-181) - ~75 lines
- `/frontend/src/routes/scenario.tsx` (lines 93-293) - ~75 lines

**Create:** `/frontend/src/hooks/useAudioRecording.ts`
```typescript
export function useAudioRecording(
  onTranscript: (text: string) => void,
  simulationId: number,
  messageId: number | null
) {
  // Encapsulate all recording logic
  return {
    isRecording,
    startRecording,
    stopRecording
  }
}
```

**Action:**
1. Create custom hook with all recording logic
2. Update `case.tsx` to use hook
3. Update `scenario.tsx` to use hook
4. Delete original implementations

**Impact:** ~150 lines saved across 2 files

### 2.3 Delete Confirmation Dialog (~120 lines saved)

**Duplicated in:**
- `/frontend/src/routes/case.tsx` (lines 81-83, 416-450, 902-942) - ~60 lines
- `/frontend/src/routes/cases.tsx` (lines 37-38, 104-140, 293-333) - ~60 lines

**Create:** `/frontend/src/components/Common/DeleteConfirmationDialog.tsx`
```typescript
interface DeleteConfirmationDialogProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => Promise<void>
  itemName: string
  itemType: string
  warningMessage?: string
}
export function DeleteConfirmationDialog(props: DeleteConfirmationDialogProps) { ... }
```

**Action:**
1. Create reusable dialog component
2. Update `case.tsx` to use component
3. Update `cases.tsx` to use component
4. Delete original dialog implementations

**Impact:** ~120 lines saved

### 2.4 Toast Notification Pattern (~200 lines saved)

**Problem:** `useCustomToast` hook exists but is **never used**

**File:** `/frontend/src/hooks/useCustomToast.ts` (26 lines)

**Action:**
1. Enhance existing hook:
```typescript
export function useCustomToast() {
  const showSuccess = (title: string, description?: string) => { ... }
  const showError = (title: string, description?: string) => { ... }
  const showInfo = (title: string, description?: string) => { ... }
  const showWarning = (title: string, description?: string) => { ... }
  return { showSuccess, showError, showInfo, showWarning }
}
```
2. Replace all 50+ direct `toaster.create()` calls across route files
3. Use consistent pattern: `const toast = useCustomToast()` → `toast.showSuccess(...)`

**Impact:** ~200 lines reduced (4-5 lines → 1 line per usage)

### 2.5 Backend Client Consolidation (~24 lines saved)

**Duplicated in:**
- `/backend/app/api/routes/legal.py` (lines 14-21)
- `/backend/app/api/routes/tree_generation.py` (lines 24-32)
- `/backend/app/api/routes/audio_models.py` (lines 19-27)

**Create:** `/backend/app/core/clients.py`
```python
def get_boson_client() -> OpenAI:
    """Centralized Boson AI client factory"""
    if not settings.BOSON_API_KEY:
        raise HTTPException(status_code=500, detail="BOSON_API_KEY not configured")
    return OpenAI(
        api_key=settings.BOSON_API_KEY,
        base_url="https://api.boson.ai/v1"
    )
```

**Action:**
1. Create new file with client factory
2. Update all route files to import `get_boson_client()`
3. Delete original implementations

**Impact:** 24 lines saved + single configuration point

### 2.6 Database Session Dependency (~10 lines saved)

**Duplicated in:**
- `/backend/app/api/routes/audio_models.py` (lines 30-32)
- `/backend/app/api/routes/tree_generation.py` (lines 20-22)

**Action:**
1. Move `get_session()` dependency to `/backend/app/core/db.py`
2. Update all imports to use centralized dependency
3. Delete duplicates

**Impact:** 10 lines saved

---

## Phase 3: Component Simplification (MEDIUM PRIORITY)

**Goal:** Break down oversized components into manageable pieces
**Estimated effort:** 4-5 hours
**Lines redistributed:** ~900 lines
**Risk:** Medium-High (requires careful testing)

### 3.1 Refactor scenario.tsx (1,117 lines → ~700 lines)

**Current issues:**
- 17 useState hooks
- Mixing business logic with presentation
- Multiple responsibilities in single component

**Extraction plan:**

1. **Use shared hooks** (from Phase 2)
   - Replace lines 174-293 with `useAudioRecording` hook
   - Saves: ~120 lines

2. **Extract ResponseOptionsPanel**
   - Lines 924-1046 → `/frontend/src/components/Scenario/ResponseOptionsPanel.tsx`
   - Props: `{ options, onSelect, onCustomSubmit, isGenerating }`
   - Saves: ~120 lines

3. **Extract BookmarksPanel**
   - Lines 782-833 → `/frontend/src/components/Scenario/BookmarksPanel.tsx`
   - Props: `{ bookmarks, onNavigate, onDelete }`
   - Saves: ~50 lines

4. **Extract ConversationHistory**
   - Lines 712-779 → `/frontend/src/components/Scenario/ConversationHistory.tsx`
   - Props: `{ history, onNavigate, currentId }`
   - Saves: ~70 lines

5. **Extract ScenarioDialogs**
   - Lines 1071-1114 → `/frontend/src/components/Scenario/ScenarioDialogs.tsx`
   - All modal/dialog components
   - Saves: ~45 lines

**Total reduction: ~405 lines → Target: ~712 lines**

### 3.2 Refactor case.tsx (947 lines → ~480 lines)

**Current issues:**
- 15 useState hooks
- Combines case management, audio recording, simulation CRUD
- Multiple dialogs

**Extraction plan:**

1. **Use shared hooks** (from Phase 2)
   - Replace lines 105-241 with `useAudioRecording` hook
   - Saves: ~140 lines

2. **Use shared DeleteConfirmationDialog** (from Phase 2)
   - Replace custom dialogs with shared component
   - Saves: ~60 lines

3. **Extract BackgroundEditor**
   - Lines 506-627 → `/frontend/src/components/Case/BackgroundEditor.tsx`
   - Props: `{ background, onChange, onSave, isEdited }`
   - Saves: ~120 lines

4. **Extract SimulationCard**
   - Lines 638-689 → `/frontend/src/components/Case/SimulationCard.tsx`
   - Props: `{ simulation, onDelete, onClick }`
   - Saves: ~50 lines

5. **Extract SimulationDialogs**
   - Lines 718-942 → `/frontend/src/components/Case/SimulationDialogs.tsx`
   - All dialog components
   - Saves: ~225 lines

**Total reduction: ~595 lines → Target: ~352 lines**

### 3.3 Extract Complex Event Handlers

**Create:** `/frontend/src/services/simulationService.ts`

**Extract from scenario.tsx:**
```typescript
export async function submitCustomResponse(params: {
  simulationId: number
  currentMessageId: number
  response: string
  tree: DialogueNode
}): Promise<{ newMessage: Message; freshTree: DialogueNode }> {
  // Business logic here
}
```

**Extract from case.tsx:**
```typescript
export async function createAndInitializeSimulation(params: {
  caseId: number
  headline: string
  brief: string
}): Promise<{ simulationId: number; rootMessageId: number }> {
  // Business logic here
}
```

**Impact:** ~55 lines moved from components to service layer

---

## Phase 4: Type Safety & API Improvements (MEDIUM PRIORITY)

**Goal:** Improve type safety and API organization
**Estimated effort:** 2-3 hours
**Risk:** Low (compile-time checks prevent breaks)

### 4.1 Backend Type Safety

#### Add Role Enum
- **File:** `/backend/app/models.py` (line 36)
- **Current:** `role: str = Field(default=None) #todo enum`
- **Change:**
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    A = "A"
    B = "B"

# Update model
role: MessageRole = Field(default=None)
```

#### Remove Redundant Types
- **File:** `/backend/app/schemas.py`
- **Issue:** `TreeNode` and `BackendTreeNode` are identical (lines 16-21 vs 31-37)
- **Action:** Keep `TreeNode`, remove `BackendTreeNode`, update all imports

#### Fix Optional Fields
- **File:** `/backend/app/models.py` (line 20)
- **Current:** `name: str = Field(default=None)`
- **Issue:** Every case should have a name
- **Action:** Remove `default=None` or set to `"Untitled"`

### 4.2 Frontend Type Safety

#### Remove 'any' Usage
- **Locations:**
  - `/routes/case.tsx:260` - `as any` on API response
  - `/routes/cases.tsx:47` - `(data: any) =>`
  - `/routes/scenario.tsx:145` - `as any` on transcription response
- **Action:** Define proper types, remove casts

#### Create Shared API Types
- **Create:** `/frontend/src/types/api.ts`
- **Move from route files:**
  - `Simulation`, `CaseBackground`, `CaseData` interfaces from `case.tsx`
  - Duplicate backend schema definitions
- **Impact:** Single source of truth for API types

#### Add Readonly Modifiers
- **File:** `/frontend/src/types/scenario.ts`
- **Action:** Add `readonly` to immutable fields in `DialogueNode`:
```typescript
export interface DialogueNode {
  readonly id: string
  statement: string
  readonly party: Party
  // ...
}
```

### 4.3 API Route Organization

#### Add Route Prefixes
- **File:** `/backend/app/api/main.py`
- **Current:** Routes have no prefix
- **Change:**
```python
api_router.include_router(audio_models.router, prefix="/audio", tags=["audio"])
api_router.include_router(tree_generation.router, prefix="/trees", tags=["generation"])
api_router.include_router(web_app.router, prefix="/app", tags=["application"])
```

#### Add Proper HTTP Status Codes
- **Action:** Update endpoints to use appropriate status codes:
  - 201 for creation
  - 204 for deletion
  - 400 for validation errors
  - 404 for not found

---

## Validation & Testing Strategy

### After Each Phase

**Backend:**
1. Run linting: `cd backend && ruff check app tests`
2. Run type checking: `cd backend && mypy app`
3. Run tests: `bash backend/scripts/test.sh`
4. Check coverage report in `backend/htmlcov/index.html`

**Frontend:**
1. Run linting: `cd frontend && npm run lint`
2. Run type checking: `cd frontend && npm run type-check` (if available)
3. Run tests: `cd frontend && npm run test -- --run`
4. Build check: `cd frontend && npm run build`

**Integration:**
1. Start full stack: `docker compose up --build`
2. Verify all pages load correctly
3. Test core user flows:
   - Create case
   - Generate simulation
   - Record audio
   - Navigate conversation tree
   - Create bookmarks
   - Delete simulations/cases
4. Check browser console for errors
5. Verify API calls succeed (Network tab)

### Critical Test Points

**Audio Recording (Phases 2.1, 2.2):**
- [ ] Recording starts/stops correctly
- [ ] Audio is transcribed via Boson AI
- [ ] WAV encoding produces valid audio
- [ ] Works in both case.tsx and scenario.tsx

**Delete Dialogs (Phase 2.3):**
- [ ] Dialog opens with correct item name
- [ ] Confirmation triggers deletion
- [ ] Success toast appears
- [ ] List updates after deletion

**Component Refactoring (Phase 3):**
- [ ] All UI elements render correctly
- [ ] Event handlers still work
- [ ] State updates propagate properly
- [ ] No console errors or warnings

**Type Changes (Phase 4.1):**
- [ ] Database migrations work (if needed)
- [ ] API responses match updated schemas
- [ ] Frontend can deserialize responses

---

## Rollback Plan

### Per Phase
- Each phase should be committed separately
- Use feature branches: `refactor/phase-1-dead-code`, `refactor/phase-2-consolidation`, etc.
- Tag before starting each phase: `pre-phase-1`, `pre-phase-2`, etc.

### If Issues Arise
1. **Tests fail:** Revert specific file, fix issue, re-apply
2. **Runtime errors:** Check browser console, verify API calls
3. **Build fails:** Check TypeScript errors, fix import paths
4. **Database issues:** Rollback migration, fix schema, re-run

### Emergency Rollback
```bash
# Rollback to before phase started
git reset --hard pre-phase-X

# Or revert specific commit
git revert <commit-hash>
```

---

## Files to Create (New)

### Phase 2
- `/frontend/src/utils/audioEncoding.ts`
- `/frontend/src/hooks/useAudioRecording.ts`
- `/frontend/src/components/Common/DeleteConfirmationDialog.tsx`
- `/backend/app/core/clients.py`

### Phase 3
- `/frontend/src/components/Scenario/ResponseOptionsPanel.tsx`
- `/frontend/src/components/Scenario/BookmarksPanel.tsx`
- `/frontend/src/components/Scenario/ConversationHistory.tsx`
- `/frontend/src/components/Scenario/ScenarioDialogs.tsx`
- `/frontend/src/components/Case/BackgroundEditor.tsx`
- `/frontend/src/components/Case/SimulationCard.tsx`
- `/frontend/src/components/Case/SimulationDialogs.tsx`
- `/frontend/src/services/simulationService.ts`

### Phase 4
- `/frontend/src/types/api.ts`

**Total: 14 new files**

---

## Files to Delete (Complete Removal)

### Phase 1 - Backend
- `/backend/app/api/routes/legal.py`

### Phase 1 - Frontend
- `/frontend/src/components/Pending/PendingUsers.tsx`
- `/frontend/src/components/Pending/PendingItems.tsx`
- `/frontend/src/components/Common/UserActionsMenu.tsx`
- `/frontend/src/components/Common/ItemActionsMenu.tsx`
- `/frontend/src/components/Common/Navbar.tsx`
- `/frontend/src/components/Common/Sidebar.tsx`
- `/frontend/src/components/Common/SidebarItems.tsx`
- `/frontend/src/components/Common/UserMenu.tsx`
- `/frontend/src/components/ui/pagination.tsx`
- `/frontend/src/components/ui/password-input.tsx`
- `/frontend/src/components/ui/link-button.tsx`
- `/frontend/src/components/ui/input-group.tsx`
- `/frontend/src/components/ui/radio.tsx`
- `/frontend/src/components/ui/close-button.tsx`
- `/frontend/src/components/ui/checkbox.tsx`
- `/frontend/src/services/simulationApi.ts`

**Total: 17 files to delete**

---

## Files to Modify (Partial Changes)

### Phase 1 - Backend
- `/backend/app/api/main.py` - Remove legal.py import
- `/backend/app/utils.py` - Remove email functions (lines 25-123)
- `/backend/app/crud.py` - Remove auth CRUD, fix duplicate imports
- `/backend/app/api/routes/web_app.py` - Remove unused helpers
- `/backend/app/api/routes/tree_generation.py` - Remove old save function
- `/backend/app/core/dummy_generator.py` - Remove commented code, fix imports

### Phase 1 - Frontend
- `/frontend/src/routes/case.tsx` - Remove commented code
- `/frontend/src/routes/__root.tsx` - Remove commented code
- `/frontend/src/services/scenarioService.ts` - Remove unused functions
- `/frontend/src/utils/treeUtils.ts` - Remove unused functions
- `/frontend/src/utils.ts` - Remove unused validation functions
- `/frontend/src/types/scenario.ts` - Remove unused types
- `/frontend/package.json` - Remove 4 dependencies

### Phase 2
- `/frontend/src/routes/case.tsx` - Use shared hooks/components
- `/frontend/src/routes/scenario.tsx` - Use shared hooks/components
- `/frontend/src/routes/cases.tsx` - Use shared dialog
- `/frontend/src/hooks/useCustomToast.ts` - Enhance with helper methods
- All route files - Replace `toaster.create()` with `toast.showSuccess/Error()`
- `/backend/app/api/routes/tree_generation.py` - Import from clients.py
- `/backend/app/api/routes/audio_models.py` - Import from clients.py

### Phase 3
- `/frontend/src/routes/scenario.tsx` - Extract components, move logic to services
- `/frontend/src/routes/case.tsx` - Extract components, move logic to services

### Phase 4
- `/backend/app/models.py` - Add MessageRole enum, fix optional fields
- `/backend/app/schemas.py` - Remove redundant types
- `/backend/app/api/main.py` - Add route prefixes
- Multiple backend routes - Add proper HTTP status codes
- Multiple frontend route files - Remove 'any' types, use shared API types
- `/frontend/src/types/scenario.ts` - Add readonly modifiers

**Total: 30+ files to modify**

---

## Out of Scope (Deferred)

The following items from the audit reports are **not included** in this tightly-scoped plan:

### Not Essential for Core Refactoring
- User/Auth system models (keep as scaffolding for potential future use)
- React Query implementation (current fetch pattern works)
- React Hook Form migration (current forms are simple enough)
- Error boundary implementation
- Architecture diagrams and ADR documentation
- API versioning and RESTful naming refactor (would require frontend changes)
- Performance testing / load testing
- Security scanning (separate concern)
- Caching layer for API calls
- Request/response logging enhancements
- Rate limiting for external APIs

### Handled by Existing Infrastructure
- Pre-commit hooks (keep existing)
- Linting configuration (already optimal)
- Type checking (already strict)
- Database migrations (already using Alembic)
- Docker setup (already working well)
- Environment configuration (already documented)

---

## Success Criteria

### Phase 1 Complete When:
- [ ] All 17 dead files deleted
- [ ] All unused functions removed from remaining files
- [ ] 4 npm dependencies uninstalled
- [ ] All tests pass (backend + frontend)
- [ ] Application builds without errors
- [ ] No import errors in codebase

### Phase 2 Complete When:
- [ ] 4 new utility files created (audioEncoding, useAudioRecording, DeleteConfirmationDialog, clients.py)
- [ ] Duplicate code removed from case.tsx and scenario.tsx
- [ ] Audio recording works identically to before
- [ ] Delete dialogs work identically to before
- [ ] Toast notifications use consistent pattern
- [ ] All tests pass

### Phase 3 Complete When:
- [ ] scenario.tsx reduced to ~700 lines
- [ ] case.tsx reduced to ~480 lines
- [ ] 11 new component files created
- [ ] 1 new service file created
- [ ] All UI interactions work correctly
- [ ] No console errors
- [ ] All tests pass

### Phase 4 Complete When:
- [ ] MessageRole enum implemented
- [ ] No TypeScript 'any' types in route files
- [ ] Shared API types created
- [ ] Route prefixes added to API
- [ ] Proper HTTP status codes used
- [ ] Type checking passes (mypy + tsc)
- [ ] All tests pass

### Overall Success Metrics:
- **Code reduction:** ~3,351 lines removed or consolidated
- **Test coverage:** Maintained or improved
- **Build time:** No significant regression
- **Runtime performance:** No degradation
- **Developer experience:** Easier to navigate and modify code
- **Maintainability:** Clear separation of concerns, reusable components

---

## Timeline Estimate

| Phase | Estimated Hours | Completion Criteria |
|-------|----------------|---------------------|
| **Phase 1: Dead Code** | 2-3 hours | Tests pass, builds succeed |
| **Phase 2: Consolidation** | 3-4 hours | Audio/dialogs work, tests pass |
| **Phase 3: Components** | 4-5 hours | UI works, no console errors |
| **Phase 4: Types/API** | 2-3 hours | Type checking passes |
| **Testing & Polish** | 2-3 hours | Full integration testing |
| **TOTAL** | **13-18 hours** | All success criteria met |

---

## Notes

- **CI/CD:** All CI/CD infrastructure has been removed per requirements
- **Testing:** Use local test runners for validation
- **Deployment:** Manual deployment only (no automated pipelines)
- **Version Control:** Use feature branches and descriptive commits
- **Documentation:** Update README if any setup commands change

---

**Plan Status:** READY FOR EXECUTION
**Last Updated:** 2025-11-19
**Next Action:** Begin Phase 1 (Dead Code Elimination)

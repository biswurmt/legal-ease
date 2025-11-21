# Future Refactoring Phases (5-6)

**Status:** To be implemented after Phases 1-4
**Created:** 2025-11-21

These phases are documented for future implementation. Phases 1-4 (dead code removal, pattern consolidation, React Query, and type safety) are being implemented first.

---

## Phase 5: Refactor Oversized Components

**Goal:** Break down oversized components for better maintainability
**Risk Level:** 🟠 Medium-High
**Estimated Duration:** 6-8 hours
**Lines to Save:** ~900 lines redistributed

### 5.1 Refactor scenario.tsx (1,117 → ~700 lines)

**Current Issues:**
- 17 useState hooks
- Mixing business logic with presentation
- Difficult to test
- Multiple responsibilities

**Recommended Splits:**

1. **Create `/frontend/src/components/Scenario/ResponseOptionsPanel.tsx`**
   - Extract lines 924-1046 (122 lines)
   - Props: `options`, `onSelect`, `onCustomSubmit`, `isGenerating`

2. **Create `/frontend/src/components/Scenario/BookmarksPanel.tsx`**
   - Extract lines 782-833 (51 lines)
   - Props: `bookmarks`, `onNavigate`, `onDelete`

3. **Create `/frontend/src/components/Scenario/ConversationHistory.tsx`**
   - Extract lines 712-779 (67 lines)
   - Props: `history`, `onNavigate`, `currentId`

4. **Create `/frontend/src/components/Scenario/ScenarioDialogs.tsx`**
   - Extract lines 1071-1114 (43 lines)
   - Props: All dialog state and handlers

5. **Create `/frontend/src/hooks/useSimulationTree.ts`**
   - Extract tree state management logic
   - Returns: `{ fullTree, currentNode, history, navigate, refetch }`

**Integration Tests:**
```typescript
// frontend/src/routes/scenario.test.tsx
describe('Scenario Page', () => {
  it('renders conversation tree', () => { /* ... */ })
  it('handles response selection', () => { /* ... */ })
  it('manages bookmarks correctly', () => { /* ... */ })
  it('navigates tree structure', () => { /* ... */ })
})
```

**Testing:**
```bash
npm run test -- scenario.test
npm run build
# Component should render and function identically
```

---

### 5.2 Refactor case.tsx (947 → ~480 lines)

**Current Issues:**
- 15 useState hooks
- Combines case management, audio recording, simulation CRUD
- Multiple dialogs in single file

**Recommended Splits:**

1. **Create `/frontend/src/components/Case/BackgroundEditor.tsx`**
   - Extract lines 506-627 (121 lines)
   - Props: `background`, `onChange`, `onSave`, `isEdited`
   - State: Manages edit mode internally

2. **Create `/frontend/src/components/Case/SimulationCard.tsx`**
   - Extract lines 638-689 (51 lines)
   - Props: `simulation`, `onDelete`, `onClick`
   - Reusable card component for simulation display

3. **Create `/frontend/src/components/Case/SimulationDialogs.tsx`**
   - Extract lines 718-942 (224 lines)
   - All dialog components (create, edit, delete)
   - Manages own state for dialog visibility

4. **Create `/frontend/src/services/simulationService.ts`**
   - Extract `createAndInitializeSimulation()` logic (lines 350-407)
   - Clean separation of business logic from UI
   - Makes component testable

**Integration Tests:**
```typescript
// frontend/src/routes/case.test.tsx
describe('Case Page', () => {
  it('renders case background editor', () => { /* ... */ })
  it('handles background editing', () => { /* ... */ })
  it('creates simulation correctly', () => { /* ... */ })
  it('deletes simulation with confirmation', () => { /* ... */ })
})
```

**Testing:**
```bash
npm run test -- case.test
npm run build
# All case page functionality should work
```

---

### 5.3 State Management Improvements

**Problem:** Excessive useState hooks (17 in scenario.tsx, 15 in case.tsx)

**Solution 1: Group modal state with useReducer**
```typescript
// In scenario.tsx
type ModalState = {
  saveModal: { open: boolean; name: string }
  customResponseModal: { open: boolean }
  deleteBookmarkModal: { open: boolean; bookmarkId: number | null }
}

type ModalAction =
  | { type: 'OPEN_SAVE_MODAL' }
  | { type: 'CLOSE_SAVE_MODAL' }
  | { type: 'SET_SAVE_NAME'; name: string }
  // ... other actions

const modalReducer = (state: ModalState, action: ModalAction): ModalState => {
  switch (action.type) {
    case 'OPEN_SAVE_MODAL':
      return { ...state, saveModal: { ...state.saveModal, open: true } }
    // ... other cases
  }
}

// Usage
const [modalState, dispatch] = useReducer(modalReducer, initialModalState)
```

**Impact:** Reduces 10-15 lines, clearer state transitions

**Solution 2: Extract tree state to custom hook**
```typescript
// Create: /frontend/src/hooks/useSimulationTree.ts
export function useSimulationTree(simulationId: number, messageId: number) {
  const [fullTree, setFullTree] = useState<DialogueNode | null>(null)
  const [currentNode, setCurrentNode] = useState<DialogueNode | null>(null)
  const [history, setHistory] = useState<DialogueNode[]>([])

  const navigate = useCallback((nodeId: string) => {
    // Navigation logic
  }, [fullTree])

  const refetch = useCallback(async () => {
    // Refetch tree logic
  }, [simulationId])

  return { fullTree, currentNode, history, navigate, refetch }
}

// Usage in scenario.tsx
const { fullTree, currentNode, history, navigate, refetch } = useSimulationTree(
  simulationId,
  messageId
)
```

**Impact:** 20-30 lines saved, reusable across components

---

## Phase 6: API Breaking Changes

**Goal:** Improve API organization and RESTful conventions
**Risk Level:** 🟡 Medium (requires frontend coordination)
**Estimated Duration:** 3-4 hours

### 6.1 Add Route Prefixes

**Current State:**
```python
# backend/app/api/main.py
api_router.include_router(audio_models.router)      # No prefix
api_router.include_router(tree_generation.router)   # No prefix
api_router.include_router(web_app.router)           # No prefix
```

**After Refactoring:**
```python
api_router.include_router(
    audio_models.router,
    prefix="/audio",
    tags=["audio"]
)
api_router.include_router(
    tree_generation.router,
    prefix="/trees",
    tags=["generation"]
)
api_router.include_router(
    web_app.router,
    prefix="/app",
    tags=["application"]
)
```

**Impact:**
- Better API docs organization
- Clearer endpoint grouping
- Easier to understand API structure

**Frontend Update Required:**
All API calls must be updated. Use find/replace:
- `/api/transcribe-audio` → `/api/audio/transcribe`
- `/api/continue-conversation` → `/api/trees/continue`
- `/api/cases` → `/api/app/cases`
- etc.

**Steps:**
1. Update backend routes with prefixes
2. Regenerate OpenAPI client: `npm run generate-client`
3. Update any direct fetch calls in frontend
4. Test all endpoints

---

### 6.2 Consolidate Duplicate Endpoints

**Problem 1: Overlapping Tree Message Retrieval**

**Current:**
- `GET /trees/{simulation_id}/messages` (web_app.py:136)
- `GET /trees/{simulation_id}/messages/traversal` (web_app.py:668)

**Solution:**
```python
@router.get("/trees/{simulation_id}/messages")
async def get_tree_messages(
    simulation_id: int,
    format: Literal["tree", "conversation"] = "tree",
    message_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """
    Get messages for a simulation tree.

    - format="tree": Returns full tree structure
    - format="conversation": Returns conversation path to message_id
    """
    if format == "conversation":
        if not message_id:
            raise HTTPException(400, "message_id required for conversation format")
        return get_selected_messages_between(session, simulation_id, message_id)
    else:
        return get_messages_by_tree(session, simulation_id)
```

**Frontend Update:**
```typescript
// Old:
const response = await fetch(`/api/trees/${simId}/messages/traversal?message_id=${msgId}`)

// New:
const response = await fetch(`/api/trees/${simId}/messages?format=conversation&message_id=${msgId}`)
```

**Impact:** Reduces 1 endpoint, clearer API design

---

### 6.3 RESTful Convention Improvements (Optional)

**Current Violations:**
- `POST /continue-conversation` → Should be `POST /trees/{id}/messages`
- `POST /transcribe-audio` → Should be `POST /audio/transcriptions`
- `POST /summarize-dialogue` → Should be `POST /dialogues/{id}/summaries`
- `GET /get-conversation-audio` → Should be `GET /conversations/{id}/audio`

**Recommendation:**
These are more invasive changes. Consider deferring to Phase 7+ unless team prioritizes REST compliance.

**If Implementing:**
1. Create new endpoints with RESTful names
2. Keep old endpoints as deprecated (with warning logs)
3. Update frontend gradually
4. Remove old endpoints after transition period

---

### 6.4 HTTP Status Code Improvements

**Current Issue:** Most endpoints default to 200 for all responses

**Recommendation:**
```python
# Creation endpoints
@router.post("/cases", status_code=status.HTTP_201_CREATED)
async def create_case(...)

# Deletion endpoints
@router.delete("/case/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(...)

# Not found errors
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="...")

# Validation errors
raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="...")
```

**Impact:**
- Better HTTP semantics
- Easier client error handling
- Industry standard compliance

---

## Testing Strategy for Phases 5-6

### Phase 5 Testing

**Unit Tests:**
- Test extracted components in isolation
- Test hooks with React Testing Library
- Mock API calls and state

**Integration Tests:**
- Test full page rendering
- Test component interactions
- Test state flow between parent and children

**Visual Regression (Optional):**
- Screenshot testing with Playwright
- Ensure UI remains identical

### Phase 6 Testing

**Backend:**
- Update existing API tests with new routes
- Verify status codes are correct
- Test query parameters

**Frontend:**
- Update service layer tests
- Verify client generation works
- Test error handling

**End-to-End:**
- Full user flows still work
- No 404s or broken links

---

## Success Metrics

### Phase 5:
- ✅ scenario.tsx reduced from 1,117 to ~700 lines
- ✅ case.tsx reduced from 947 to ~480 lines
- ✅ All functionality preserved
- ✅ Tests pass
- ✅ No console errors

### Phase 6:
- ✅ API docs show organized route groups
- ✅ All endpoints follow prefix pattern
- ✅ Duplicate endpoints consolidated
- ✅ Frontend uses new routes
- ✅ No breaking changes without migration

---

## Risk Mitigation

### Phase 5 Risks:
1. **Breaking component functionality**
   - Mitigation: Comprehensive tests before refactoring
   - Mitigation: Test each extracted component individually

2. **State synchronization issues**
   - Mitigation: Use React Context for shared state
   - Mitigation: Props drilling only 1-2 levels deep

3. **Performance regressions**
   - Mitigation: Use React.memo for expensive components
   - Mitigation: Benchmark before/after

### Phase 6 Risks:
1. **Breaking frontend during migration**
   - Mitigation: Regenerate OpenAPI client immediately
   - Mitigation: Update all imports in single commit

2. **Missing API calls during route changes**
   - Mitigation: Grep for all old routes before deleting
   - Mitigation: Test all pages after migration

3. **Third-party integrations broken**
   - Mitigation: None needed (no external API consumers confirmed)

---

## Estimated Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 5.1 | Refactor scenario.tsx | 3-4 hours |
| 5.2 | Refactor case.tsx | 3-4 hours |
| 5.3 | State management improvements | 1-2 hours |
| **Total Phase 5** | | **7-10 hours** |
| 6.1 | Add route prefixes | 1 hour |
| 6.2 | Consolidate endpoints | 1 hour |
| 6.3 | RESTful improvements (optional) | 2-3 hours |
| 6.4 | Status code improvements | 1 hour |
| **Total Phase 6** | | **3-6 hours** |
| **Grand Total** | | **10-16 hours** |

---

## Prerequisites

Before starting Phases 5-6:
1. ✅ Phases 1-4 complete and committed
2. ✅ All tests passing
3. ✅ No merge conflicts
4. ✅ Team approval for API breaking changes (Phase 6)

---

## Notes

- Phase 5 is safe to implement anytime (no breaking changes)
- Phase 6 requires coordination if other systems consume the API
- Consider feature flags for gradual Phase 6 rollout
- Document all API changes in release notes

**Last Updated:** 2025-11-21
**Document Owner:** Refactoring Team

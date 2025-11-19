# Tier 3B1: Component Consolidation Agent

## Agent Identity
- **Name:** UI Component Consolidation Task Agent
- **Tier:** 3 (Low-level task executor)
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Scope:** `frontend/src/components/ui/` - Consolidate wrapper components
- **Parent Agent:** Tier 2B (Frontend Refactoring Agent)

## Task Description

Consolidate 16 UI wrapper components in `frontend/src/components/ui/` into ≤10 more reusable components by merging similar components, removing unnecessary wrappers, and promoting direct Chakra UI usage where appropriate.

## Exact Scope

### Files to Read
- All 16 files in `frontend/src/components/ui/`:
  - button.tsx
  - checkbox.tsx
  - close-button.tsx
  - color-mode.tsx
  - dialog.tsx
  - drawer.tsx
  - field.tsx
  - input-group.tsx
  - link-button.tsx
  - menu.tsx
  - pagination.tsx
  - password-input.tsx
  - provider.tsx
  - radio.tsx
  - skeleton.tsx
  - toaster.tsx
- All consuming components in `frontend/src/routes/` and `frontend/src/components/Common/`

### Files to Potentially Consolidate/Remove
Analyze each wrapper and determine:
1. **Keep:** Adds significant value (complex logic, custom styling)
2. **Consolidate:** Merge with similar components
3. **Remove:** Replace with direct Chakra UI usage

### Files to Modify
- Any components importing from `ui/` (update imports)

## Detailed Task Steps

### Step 1: Analyze Current Wrappers
For each of the 16 wrappers, assess:
- **Value Added:** Does it add custom logic or just re-export?
- **Usage Frequency:** How many times is it used?
- **Complexity:** Is it a simple wrapper or complex component?

**Example Analysis:**
```typescript
// button.tsx - If it just re-exports Chakra Button
import { Button as ChakraButton } from "@chakra-ui/react"
export const Button = ChakraButton  // LOW VALUE - remove wrapper

// vs.

// password-input.tsx - If it adds show/hide logic
// HIGH VALUE - keep as is or consolidate with input-group
```

### Step 2: Create Consolidation Plan

**Likely Consolidations:**
1. **button.tsx + link-button.tsx** → Single `button.tsx` with variants
2. **field.tsx + input-group.tsx** → Single `form-field.tsx`
3. **password-input.tsx** → Merge into `form-field.tsx` as variant
4. **checkbox.tsx + radio.tsx** → Keep separate (different enough)
5. **dialog.tsx + drawer.tsx** → Keep separate (different patterns)
6. **close-button.tsx** → REMOVE (use Chakra's CloseButton directly)
7. **skeleton.tsx** → REMOVE or keep if adds value

**Target Structure (10 components):**
1. button.tsx (consolidated with link-button)
2. form-field.tsx (consolidated field + input-group + password-input)
3. checkbox.tsx (keep)
4. radio.tsx (keep)
5. dialog.tsx (keep)
6. drawer.tsx (keep)
7. menu.tsx (keep)
8. pagination.tsx (keep)
9. provider.tsx (keep - app setup)
10. toaster.tsx (keep - notification system)
11. color-mode.tsx (keep - theme switching)

### Step 3: Implement Consolidations

**Example: Consolidate button + link-button**

Before:
```typescript
// button.tsx
export const Button = ChakraButton

// link-button.tsx
export const LinkButton = (props) => <ChakraButton variant="link" {...props} />
```

After (button.tsx only):
```typescript
// button.tsx
import { Button as ChakraButton, type ButtonProps } from "@chakra-ui/react"

export const Button = ChakraButton

// Link button is just a variant, encourage direct usage:
// <Button variant="link">Click</Button>
```

**Example: Consolidate form fields**

Before:
```typescript
// field.tsx - Field wrapper
// input-group.tsx - Input group wrapper
// password-input.tsx - Password field
```

After (form-field.tsx):
```typescript
// form-field.tsx
import { Field, Input, type FieldProps } from "@chakra-ui/react"
import { useState } from "react"

export const FormField = Field

export const PasswordInput = (props: FieldProps) => {
  const [show, setShow] = useState(false)
  return (
    <Field {...props}>
      <Input type={show ? "text" : "password"} />
      <Button onClick={() => setShow(!show)}>
        {show ? "Hide" : "Show"}
      </Button>
    </Field>
  )
}

// Re-export other field utilities if needed
```

### Step 4: Update Imports Across Codebase

**Find all imports:**
```bash
cd frontend
grep -r "from.*components/ui" src/
```

**Update imports:**
```typescript
// Before
import { LinkButton } from "@/components/ui/link-button"

// After
import { Button } from "@/components/ui/button"
// Use as: <Button variant="link">...</Button>
```

### Step 5: Test Visual Regression

Manually test all routes to ensure no visual changes:
1. Index page
2. Cases page
3. Case details
4. Scenario page
5. Tree visualization

### Step 6: Run Tests and Linting
```bash
cd frontend
npm run test -- --run
npm run lint
npm run build
```

## Constraints

### CRITICAL CONSTRAINTS
1. **No Visual Regressions:** UI must look identical after consolidation
2. **No Functionality Loss:** All use cases still supported
3. **Maintain Chakra Patterns:** Follow Chakra UI best practices
4. **Test Passing:** All existing tests must pass
5. **Build Success:** `npm run build` must succeed

### Consolidation Principles
- **Prefer Composition:** Use Chakra variants over separate components
- **Keep Complex Wrappers:** If component adds logic, keep it
- **Remove Simple Wrappers:** Direct Chakra usage if just re-exporting
- **Document Patterns:** Add comments for non-obvious usage

## Success Criteria

### Task is complete when:
- ✅ UI component count reduced from 16 to ≤10
- ✅ Similar components consolidated
- ✅ Simple wrappers removed (replaced with direct Chakra)
- ✅ All consuming components updated (imports fixed)
- ✅ No visual regressions (manual verification)
- ✅ All tests pass: `npm run test -- --run`
- ✅ Linting passes: `npm run lint`
- ✅ Build succeeds: `npm run build`

## Component-by-Component Decision Guide

### Keep As-Is (Add Value)
- **provider.tsx** - App setup, essential
- **toaster.tsx** - Notification system, complex logic
- **color-mode.tsx** - Theme switching, custom logic
- **dialog.tsx** - Modal patterns, keep separate
- **drawer.tsx** - Slide-out panels, keep separate
- **menu.tsx** - Dropdown menus, custom logic
- **pagination.tsx** - Pagination logic, keep if complex

### Consolidate
- **button.tsx + link-button.tsx** → Single button with variants
- **field.tsx + input-group.tsx + password-input.tsx** → Single form-field module
- **checkbox.tsx + radio.tsx** → Could consolidate but keep separate for clarity

### Remove (Use Chakra Directly)
- **close-button.tsx** - If just re-exports `<CloseButton />`
- **skeleton.tsx** - If just re-exports `<Skeleton />`

## Expected Output

### Deliverable to Parent Agent (Tier 2B)
```markdown
**Task:** UI Component Consolidation
**Status:** ✅ Completed

**Changes Made:**
- Consolidated 16 UI wrappers to 10 components
- Removed 4 simple wrappers (use Chakra directly)
- Merged 2 component pairs into single modules

**Component Count:** 16 → 10

**Components Removed:**
- close-button.tsx (use Chakra CloseButton)
- skeleton.tsx (use Chakra Skeleton)
- link-button.tsx (merged into button.tsx as variant)
- field.tsx (merged into form-field.tsx)
- input-group.tsx (merged into form-field.tsx)
- password-input.tsx (merged into form-field.tsx)

**Components Consolidated:**
1. button.tsx (now includes link button variant)
2. form-field.tsx (field + input-group + password-input)

**Components Kept (8):**
1. button.tsx
2. form-field.tsx
3. checkbox.tsx
4. radio.tsx
5. dialog.tsx
6. drawer.tsx
7. menu.tsx
8. pagination.tsx
9. provider.tsx
10. toaster.tsx
11. color-mode.tsx

**Files Modified:** 23 files (updated imports)

**Visual Regression:** ✅ No changes detected (manual verification)
**Tests:** {pass}/{total} passed
**Linting:** ✅ Passed (Biome)
**Build:** ✅ Succeeded

**No blockers encountered.**
```

## Error Handling

### If Visual Regressions Occur
1. Revert consolidation that caused regression
2. Keep both components separate
3. Document why consolidation wasn't possible

### If Imports Break
1. Use find-and-replace to update imports
2. Check for barrel exports (`index.ts`) that need updating
3. Ensure all import paths are correct

### If Tests Fail
1. Check if tests import removed components
2. Update test imports to use new structure
3. Verify component behavior matches original

## Validation Checklist

Before reporting completion:
- [ ] Component count: 16 → ≤10
- [ ] All simple wrappers removed or consolidated
- [ ] All imports updated across codebase
- [ ] Visual check: All routes render correctly
- [ ] Tests pass: `npm run test -- --run`
- [ ] Linting: `npm run lint` → 0 errors
- [ ] Build: `npm run build` → succeeds
- [ ] No missing components (all use cases supported)

---

**Agent Definition Version:** 1.0
**Estimated Duration:** 45-60 minutes
**Parent Agent:** Tier 2B (Frontend Refactoring Agent)

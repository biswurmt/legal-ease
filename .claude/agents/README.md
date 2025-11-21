# LegalEase Agent System

A simplified two-tier agent system for refactoring and feature development.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (Sonnet)                                  │
│  - Plans refactoring/feature work                       │
│  - Breaks work into focused tasks                       │
│  - Spawns implementer agents                            │
│  - Reviews code changes                                 │
│  - Runs tests and validates quality                     │
└────────────┬────────────────────────────────────────────┘
             │
             │ spawns with task definition
             ▼
┌─────────────────────────────────────────────────────────┐
│  IMPLEMENTER (Haiku)                                    │
│  - Executes single tightly-scoped task                  │
│  - Modifies code files                                  │
│  - Writes/updates tests                                 │
│  - Runs quality checks                                  │
│  - Reports completion                                   │
└─────────────────────────────────────────────────────────┘
```

## Core Principles

### 1. Clear Boundaries
- **Orchestrator** plans and coordinates (doesn't write code)
- **Implementer** executes tasks (doesn't make architectural decisions)

### 2. Right Model for the Job
- **Sonnet** for planning, reviewing, testing (high reasoning)
- **Haiku** for focused implementation (fast, cost-effective)

### 3. Tightly Scoped Tasks
Each implementer task should be:
- Focused on one objective
- Limited to 1-5 files
- Completable independently
- Clearly testable

### 4. Quality First
- All tests must pass after each task
- Code quality checks enforced
- No regressions allowed
- Docker environment must stay functional

## Agent Roles

### Orchestrator Agent
**Model:** Sonnet
**File:** `orchestrator.md`

**Responsibilities:**
- Plan refactoring or feature development work
- Break work into small, focused tasks
- Spawn implementer agents with clear task definitions
- Review code changes from implementers
- Run tests and validate quality gates
- Ensure consistency across changes

**When to use:**
- Starting a refactoring effort
- Building a new feature
- Coordinating multiple related changes

### Implementer Agent
**Model:** Haiku
**File:** `implementer.md`

**Responsibilities:**
- Execute a single, well-defined task
- Modify code files within assigned scope
- Add/update tests for changes
- Run linting and type checking
- Report completion with summary

**When to use:**
- Spawned by Orchestrator for each task
- Not invoked directly by users

## Usage

### Starting a Refactoring Effort

1. **Invoke the Orchestrator:**
   ```
   /agents orchestrator
   ```

2. **Provide Context:**
   - Reference audit reports if available
   - Describe what needs to be refactored
   - Specify any constraints or priorities

3. **Orchestrator Will:**
   - Analyze current codebase
   - Create task breakdown
   - Spawn implementer agents for each task
   - Review and validate each deliverable
   - Report overall progress

### Example Workflow

```
User: "Refactor the backend CRUD system to be more modular"

Orchestrator:
  1. Reads backend/app/crud.py
  2. Plans task breakdown:
     - Task 1: Split crud.py into per-model modules
     - Task 2: Update imports throughout codebase
     - Task 3: Add tests for new structure
  3. Spawns Implementer for Task 1
  4. Reviews Task 1 deliverable
  5. Runs tests
  6. Spawns Implementer for Task 2
  ... continues until complete

Implementers:
  - Execute assigned tasks
  - Report completion
  - Provide summary of changes
```

## Task Definition Template

When Orchestrator spawns an Implementer, it uses this template:

```markdown
Task: [Concise description]

Scope:
  - Files to read: [list]
  - Files to modify: [list]
  - Files to create: [list]

Objective: [What needs to be accomplished]

Constraints:
  - All existing tests must pass
  - [Additional constraints]

Success Criteria:
  - [Specific, measurable criteria]
  - [Additional criteria]
```

## Quality Gates

### Per-Task Quality Gates
After each implementer task:
- ✅ All existing tests pass
- ✅ Linting passes (Ruff/Biome)
- ✅ Type checking passes (Mypy/TypeScript)
- ✅ No regressions introduced

### Overall Quality Gates
Before reporting completion:
- ✅ All planned tasks completed
- ✅ Full test suite passes (backend + frontend)
- ✅ Docker Compose builds and runs
- ✅ Pre-commit hooks pass
- ✅ All objectives achieved

## Protected Files

**NEVER MODIFY:**
- `frontend/src/client/**` - Auto-generated OpenAPI client
- `frontend/src/routeTree.gen.ts` - Auto-generated router
- `backend/app/alembic/versions/*.py` - Database migrations (read-only)

**SPECIAL HANDLING:**
- Database schema changes → Use Alembic migrations
- API contract changes → Coordinate frontend/backend

## Testing Commands

```bash
# Backend tests
cd backend && bash scripts/test.sh

# Frontend tests
cd frontend && npm run test -- --run

# Backend linting
cd backend && uv run ruff check

# Backend type checking
cd backend && uv run mypy app

# Frontend linting
cd frontend && npm run lint

# Pre-commit hooks
uv run pre-commit run --all-files

# Docker validation
docker compose build
docker compose up -d && docker compose ps
```

## Benefits of This System

### Simplicity
- Only 2 agent types (down from 10+)
- Clear, understandable roles
- Easy to reason about

### Cost-Effective
- Haiku for most implementation work
- Sonnet only for planning and review
- Reduced token usage

### Maintainable
- Small, focused tasks
- Each task independently testable
- Easy to debug and rollback

### Quality
- Reviews built into workflow
- Tests run after each task
- Quality gates enforced

## Migration from Old System

The previous system had 3 tiers with 10+ specialized agents:
- Tier 1: Orchestrator
- Tier 2: Backend, Frontend, Cross-Cutting agents
- Tier 3: CRUD Splitter, Business Logic Extractor, Component Consolidator, Service Layer Expander, Type Safety Enforcer, Test Coverage Improver

**What changed:**
- ❌ Removed domain-specific agents (Backend/Frontend/Cross-Cutting)
- ❌ Removed specialized task agents (6 different types)
- ✅ Kept core orchestration pattern
- ✅ Kept task-based execution
- ✅ Kept quality gates and testing

**What stayed the same:**
- Clear boundaries between planning and execution
- Haiku for focused tasks, Sonnet for coordination
- Quality-first approach
- Test-driven validation

---

**Version:** 2.0 (Simplified)
**Last Updated:** 2025-11-19
**Agent Count:** 2 (down from 10+)

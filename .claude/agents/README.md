# LegalEase Three-Tier Agent Refactoring Architecture

This directory contains the definitions for a hierarchical, three-tier agent system designed to systematically refactor the LegalEase codebase while maintaining code quality, test coverage, and system functionality.

## Architecture Overview

The agent hierarchy follows a **command-and-delegate** pattern with three distinct tiers:

```
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 1: HIGH-LEVEL ORCHESTRATOR (Sonnet)                          │
│  - Oversees entire refactoring effort                              │
│  - Coordinates Tier 2 mid-level agents                             │
│  - Makes architectural decisions                                   │
│  - Ensures cross-cutting consistency                               │
│  - CANNOT make direct code changes                                 │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────────────────┐
             │                                                         │
             v                                                         v
┌────────────────────────────────────┐    ┌──────────────────────────────────────┐
│  TIER 2A: BACKEND REFACTORING      │    │  TIER 2B: FRONTEND REFACTORING       │
│  AGENT (Sonnet)                    │    │  AGENT (Sonnet)                      │
│  - Refactors backend/app/          │    │  - Refactors frontend/src/           │
│  - Splits CRUD modules             │    │  - Consolidates UI components        │
│  - Extracts business logic         │    │  - Expands service layer             │
│  - Enforces backend tests          │    │  - Adds frontend tests               │
│  - Spawns Tier 3 tasks             │    │  - Spawns Tier 3 tasks               │
└────────────┬───────────────────────┘    └──────────────┬───────────────────────┘
             │                                           │
             v                                           v
    ┌────────────────┐                         ┌────────────────┐
    │ Tier 3A1:      │                         │ Tier 3B1:      │
    │ CRUD Splitter  │                         │ Component      │
    │ (Haiku)        │                         │ Consolidator   │
    └────────────────┘                         │ (Haiku)        │
    ┌────────────────┐                         └────────────────┘
    │ Tier 3A2:      │                         ┌────────────────┐
    │ Business Logic │                         │ Tier 3B2:      │
    │ Extractor      │                         │ Service Layer  │
    │ (Haiku)        │                         │ Expander       │
    └────────────────┘                         │ (Haiku)        │
                                               └────────────────┘

             ┌─────────────────────────────────────┐
             │  TIER 2C: CROSS-CUTTING REFACTORING │
             │  AGENT (Sonnet)                     │
             │  - Type safety enforcement          │
             │  - Test coverage improvement        │
             │  - Shared utilities & types         │
             │  - Documentation consistency        │
             │  - Spawns Tier 3 tasks              │
             └────────────┬────────────────────────┘
                          │
                          v
                 ┌────────────────┐
                 │ Tier 3C1:      │
                 │ Type Safety    │
                 │ Enforcer       │
                 │ (Haiku)        │
                 └────────────────┘
                 ┌────────────────┐
                 │ Tier 3C2:      │
                 │ Test Coverage  │
                 │ Improver       │
                 │ (Haiku)        │
                 └────────────────┘
```

## Tier Responsibilities

### Tier 1: High-Level Orchestrator
- **Model:** Sonnet (high reasoning capability for architectural decisions)
- **Role:** Strategic coordinator
- **Responsibilities:**
  - Define refactoring roadmap
  - Spawn and coordinate Tier 2 agents
  - Monitor overall progress
  - Resolve conflicts between agents
  - Ensure architectural consistency
  - Validate final deliverables
- **Constraints:**
  - CANNOT make direct code changes
  - MUST delegate all implementation to Tier 2 agents
  - MUST ensure Tier 2 agents don't conflict
- **Success Criteria:**
  - All Tier 2 agents complete their work
  - All tests pass (backend + frontend)
  - Code quality checks pass
  - Docker environment functional
  - No regressions introduced

### Tier 2: Mid-Level Domain Agents
- **Model:** Sonnet (domain expertise + task breakdown capability)
- **Role:** Domain specialists
- **Count:** 3 agents (Backend, Frontend, Cross-Cutting)
- **Responsibilities:**
  - Own specific domains (backend, frontend, or cross-cutting)
  - Break down work into Tier 3 tasks
  - Spawn and coordinate Tier 3 agents
  - Review Tier 3 deliverables
  - Integrate changes from Tier 3 agents
  - Report progress to Tier 1
- **Constraints:**
  - MUST maintain backward compatibility within domain
  - MUST coordinate with other Tier 2 agents via Tier 1
  - MUST pass all tests before reporting completion
- **Success Criteria:**
  - Domain-specific refactoring goals achieved
  - All Tier 3 tasks completed
  - Tests pass for modified code
  - No conflicts with other domains

### Tier 3: Low-Level Task Agents
- **Model:** Haiku (fast, cost-effective for focused tasks)
- **Role:** Implementers
- **Count:** 1-2 per Tier 2 agent (6+ total)
- **Responsibilities:**
  - Execute specific, tightly-scoped refactoring tasks
  - Modify code files
  - Write/update tests
  - Ensure changes pass quality checks
  - Report completion to parent Tier 2 agent
- **Constraints:**
  - MUST only modify files within assigned scope
  - MUST pass all existing tests
  - MUST adhere to code quality standards
  - CANNOT make architectural decisions
- **Success Criteria:**
  - Assigned task completed
  - Tests pass
  - Code quality checks pass
  - Parent agent approves changes

## Agent Coordination Protocol

### Communication Flow
1. **Tier 1 → Tier 2:** Assigns domain and objectives
2. **Tier 2 → Tier 3:** Assigns specific tasks with constraints
3. **Tier 3 → Tier 2:** Reports completion and deliverables
4. **Tier 2 → Tier 1:** Reports domain completion and summary
5. **Tier 1 → User:** Final report and validation

### Conflict Resolution
- **Within Domain:** Tier 2 agent resolves
- **Cross-Domain:** Tier 1 orchestrator resolves
- **Escalation:** If Tier 1 cannot resolve, defer to user

### Handoff Points
1. **Tier 1 Spawn:** Defines objectives, constraints, success criteria for Tier 2
2. **Tier 2 Spawn:** Defines file scope, exact task, acceptance criteria for Tier 3
3. **Tier 3 Completion:** Submits changes, test results, quality check outputs
4. **Tier 2 Integration:** Merges Tier 3 changes, validates integration
5. **Tier 2 Completion:** Reports domain summary to Tier 1
6. **Tier 1 Validation:** Runs full test suite, validates consistency

## Usage Instructions

### To Start Refactoring:
1. Read the `REFACTORING_AUDIT.md` in the repository root
2. Invoke the Tier 1 Orchestrator:
   ```
   /agents tier-1-orchestrator
   ```
3. Tier 1 will spawn Tier 2 agents as needed
4. Tier 2 agents will spawn Tier 3 agents as needed
5. Monitor progress through Tier 1 status reports

### To Resume After Interruption:
1. Invoke Tier 1 Orchestrator
2. Tier 1 will assess current state and resume coordination

### To Debug Agent Issues:
1. Check agent log outputs for errors
2. Review test failures to identify issues
3. Escalate to parent tier if task cannot be completed

## File Descriptions

- `tier-1-orchestrator.md` - High-level orchestrator definition
- `tier-2-backend.md` - Backend domain agent definition
- `tier-2-frontend.md` - Frontend domain agent definition
- `tier-2-cross-cutting.md` - Cross-cutting concerns agent definition
- `tier-3-crud-splitter.md` - CRUD module splitting task
- `tier-3-business-logic-extractor.md` - Business logic extraction task
- `tier-3-component-consolidator.md` - Frontend component consolidation task
- `tier-3-service-layer-expander.md` - Frontend service layer expansion task
- `tier-3-type-safety-enforcer.md` - Type safety enforcement task
- `tier-3-test-coverage-improver.md` - Test coverage improvement task

## Quality Gates

Each tier must pass quality gates before reporting completion:

### Tier 3 Quality Gates:
- ✅ All modified files pass linting (Ruff/Biome)
- ✅ All modified files pass type checking (Mypy/TypeScript)
- ✅ All existing tests pass
- ✅ New tests added for new functionality
- ✅ Code coverage maintained or improved

### Tier 2 Quality Gates:
- ✅ All Tier 3 tasks completed
- ✅ Integration tests pass
- ✅ No conflicts with other domains
- ✅ Documentation updated
- ✅ Docker Compose still functional

### Tier 1 Quality Gates:
- ✅ All Tier 2 agents completed
- ✅ Full test suite passes (backend + frontend)
- ✅ Pre-commit hooks pass
- ✅ Docker Compose builds and runs
- ✅ No API compatibility breaks
- ✅ Refactoring objectives achieved

## Constraints & Guidelines

### CRITICAL: DO NOT MODIFY
- `frontend/src/client/**` (auto-generated OpenAPI client)
- `frontend/src/routeTree.gen.ts` (auto-generated router)
- `backend/app/alembic/versions/*.py` (database migrations - read-only)

### Database Changes
- MUST use Alembic migrations for schema changes
- NEVER directly modify `models.py` without creating migration
- Test migrations in Docker environment

### Testing Requirements
- ALL changes MUST pass existing tests
- NEW functionality MUST include tests
- AIM for 80%+ test coverage

### Code Quality
- Backend: MUST pass `ruff check` and `mypy --strict`
- Frontend: MUST pass `npm run lint`
- Pre-commit hooks MUST pass

### API Compatibility
- Maintain OpenAPI schema compatibility
- Use versioned endpoints for breaking changes
- Coordinate frontend/backend changes

## Success Metrics

The refactoring effort is successful when:

1. ✅ All Tier 2 agents report completion
2. ✅ Backend test suite passes (pytest)
3. ✅ Frontend test suite passes (vitest)
4. ✅ Code quality checks pass (Ruff, Mypy, Biome)
5. ✅ Docker Compose environment functional
6. ✅ API compatibility maintained
7. ✅ Test coverage maintained or improved
8. ✅ No regressions introduced

---

**Agent Architecture Version:** 1.0
**Last Updated:** 2025-11-18
**Next Review:** After first refactoring iteration

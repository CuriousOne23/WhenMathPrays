# Interactive Editor Architecture Documentation

**Purpose**: This documentation tree enables systematic debugging, validates architectural decisions, and tracks convergence across rearchitecture cycles.

## Navigation

### Core Architecture Documents
1. **[01_PRINCIPLES.md](01_PRINCIPLES.md)** - Design invariants and architectural principles
2. **[02_INFORMATION_FLOW.md](02_INFORMATION_FLOW.md)** - Message sequences and communication patterns
3. **[03_MODULE_RESPONSIBILITIES.md](03_MODULE_RESPONSIBILITIES.md)** - Component ownership matrix
4. **[04_API_CONTRACTS.md](04_API_CONTRACTS.md)** - Interface specifications with pre/post conditions
5. **[05_STATE_MANAGEMENT.md](05_STATE_MANAGEMENT.md)** - State machines and ownership rules
6. **[06_COORDINATE_SYSTEMS.md](06_COORDINATE_SYSTEMS.md)** - Matplotlib coordinate transforms
7. **[07_PERFORMANCE_TARGETS.md](07_PERFORMANCE_TARGETS.md)** - Measurable performance requirements
8. **[08_VALIDATION_CHECKLIST.md](08_VALIDATION_CHECKLIST.md)** - Architecture verification tests

### Historical Context
- **[refactors/](refactors/)** - Refactor history with before/after analysis
- **[decisions/](decisions/)** - Architecture Decision Records (ADRs)

## Quick Debugging Guide

### When Something Feels Slow
1. Check `07_PERFORMANCE_TARGETS.md` for expected timing
2. Check `02_INFORMATION_FLOW.md` for message sequence
3. Identify which pipeline is violating performance contract
4. Check `04_API_CONTRACTS.md` to see if contract is being violated

### When State Seems Wrong
1. Check `05_STATE_MANAGEMENT.md` for state ownership
2. Check `04_API_CONTRACTS.md` for which component is authoritative
3. Verify single source of truth principle from `01_PRINCIPLES.md`

### When Coordinates Are Confusing
1. Check `06_COORDINATE_SYSTEMS.md` for transform explanations
2. Identify which coordinate system you're working in
3. Check if LayoutManager should be handling this

### When Communication Seems Broken
1. Check `02_INFORMATION_FLOW.md` for correct message path
2. Check `04_API_CONTRACTS.md` for message schema
3. Verify Controller mediator pattern from `01_PRINCIPLES.md`

### When Considering Rearchitecture
1. Document failure mode in current refactor's `.md` file
2. Check `01_PRINCIPLES.md` - which principles were violated?
3. Create new ADR in `decisions/` for proposed change
4. Create new refactor doc in `refactors/` with before/after

## Architecture Health Checks

### ✅ Green: Architecture is healthy if...
- Every component responsibility in `03_MODULE_RESPONSIBILITIES.md` has single owner
- Every message path in `02_INFORMATION_FLOW.md` goes through Controller
- Every state variable in `05_STATE_MANAGEMENT.md` has single authoritative source
- Every performance target in `07_PERFORMANCE_TARGETS.md` is being met
- Every validation test in `08_VALIDATION_CHECKLIST.md` passes

### ⚠️ Yellow: Architecture needs attention if...
- Performance targets consistently missed by <2x
- New features require workarounds not in the documented patterns
- State synchronization bugs appear intermittently
- Coordinate transforms require trial-and-error

### 🔴 Red: Architecture requires rearchitecture if...
- Performance targets missed by >2x
- Multiple components claiming ownership of same state
- Direct component-to-component communication bypassing Controller
- Global variables used for communication
- Timing-dependent behavior

## Current Architecture Status

**Date**: 2025-12-06  
**Phase**: 2.0 (PySide6 migration)  
**Status**: 🔴 Red - Rearchitecture in progress

**Known Issues**:
- Full panel rebuilds on every edit (200-500ms observed vs <50ms target)
- Global `_double_click_armed` state bypasses Controller
- Coordinate transform logic scattered across panels
- No incremental update capability

**Planned Refactor**: See `refactors/2025-12-06_incremental_updates.md`

## Convergence Tracking

### Rearchitecture Cycle 1: Matplotlib → PySide6
- **Trigger**: Backend migration exposed architectural issues
- **Learning**: Implicit rebuild pattern doesn't scale
- **Principles Added**: Incremental updates, persistent objects
- **Status**: In progress

### Expected Future Cycles
- **Cycle 2**: Scaling to 1000 events (Phase 2.1)
- **Cycle 3**: Scaling to 10,000+ events (Phase 2.2)
- **Cycle 4**: Multi-file editing support

Each cycle will update this index with learnings and principle evolution.

---

**Last Updated**: 2025-12-06  
**Maintainer**: Architecture must be kept in sync with code during all refactors

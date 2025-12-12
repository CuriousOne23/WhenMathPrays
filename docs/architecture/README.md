# Interactive Editor Architecture Documentation

**Purpose**: This documentation tree enables systematic debugging, validates architectural decisions, and tracks convergence across rearchitecture cycles.

**Current Status**: Phase 2 complete (PySide6/PyQtGraph foundation). Phase 3 (M2 integration + QDockWidget) in planning.

## Navigation

### Core Architecture Documents
1. **[01_PRINCIPLES.md](01_PRINCIPLES.md)** - Design invariants and architectural principles
2. **[02_INFORMATION_FLOW.md](02_INFORMATION_FLOW.md)** - Message sequences and communication patterns
3. **[04_API_CONTRACTS.md](04_API_CONTRACTS.md)** - Interface specifications with pre/post conditions
4. **[07_PERFORMANCE_TARGETS.md](07_PERFORMANCE_TARGETS.md)** - Measurable performance requirements
5. **[08_VALIDATION_CHECKLIST.md](08_VALIDATION_CHECKLIST.md)** - Architecture verification tests

**Note**: Documents 03, 05, and 06 do not exist yet and may be created in Phase 3+ as needed.

### Phase Planning & Roadmap
- **[../interactive_edit_roadmap.md](../interactive_edit_roadmap.md)** - Complete phase timeline (Phase 1-4)
- **[../architecture_recommendations.md](../architecture_recommendations.md)** - GUI architecture planning (QDockWidget + M2)
- **[../interactive_edit_ph2_requirements.md](../interactive_edit_ph2_requirements.md)** - Phase 2 detailed requirements (complete)

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
**Note**: State management document (05) not yet created. For current state management, see EditorModel and Observer pattern implementation. See `../architecture_recommendations.md` for state management principles.

### When Coordinates Are Confusing
**Note**: PyQtGraph coordinate system documentation (document 06) not yet created. For Phase 2 coordinate handling, see Phase 2.1 implementation notes in `../interactive_edit_ph2_requirements.md` regarding `QGraphicsScene.sigMouseClicked` and `event.scenePos()` usage.

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

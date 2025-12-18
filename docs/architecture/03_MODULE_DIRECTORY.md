# Module Directory - Component Locations & Responsibilities

**Purpose**: Complete reference of all program modules, their directory locations, and primary responsibilities.

**Last Updated**: December 15, 2025 (v2.2.0)

---

## Interactive Editor Components

### Entry Points
| Module | Location | Purpose |
|--------|----------|---------|
| `interactive_editor.py` | `tools/` | Main entry point, UI orchestration |
| `application.py` | `tools/editor/` | Modern application framework (planned primary entry) |

### Core MVC Architecture
| Module | Location | Purpose |
|--------|----------|---------|
| `model.py` | `tools/editor/` | Data model (events, primitives, perspective management) |
| `controller.py` | `tools/editor/` | Business logic, coordinates all operations |
| `commands.py` | `tools/editor/` | Undo/redo command pattern implementations |

### State Management
| Module | Location | Purpose |
|--------|----------|---------|
| `editor_state.py` | `tools/editor/` | Centralized state enums and state machine (v2.1.0) |
| `state_viewer.py` | `tools/editor/` | State transition logging and export (Ctrl+Shift+L) |

### Data Structures
| Module | Location | Purpose |
|--------|----------|---------|
| `event.py` | `tools/editor/` | Event class with ID-based identity (v2.1.3) |
| `load_events.py` | `tools/editor/` | CSV parsing and event loading |
| `primitives.py` | `tools/editor/` | Primitive metadata (names, colors, symbols) |

### UI Components - Main Window
| Module | Location | Purpose |
|--------|----------|---------|
| `main_window.py` | `tools/editor/` | Main window class, menu bar, keyboard shortcuts |
| `ui_builder.py` | `tools/editor/` | Widget creation and layout logic |
| `file_manager.py` | `tools/editor/` | M1/M2 file path resolution |

### UI Components - Views (PyQtGraph Panels)
| Module | Location | Purpose |
|--------|----------|---------|
| `primitive_panel_pyqtgraph.py` | `tools/editor/views/` | Primitive value plots (r, f, a, v, S vs time) |
| `trajectory_panel_pyqtgraph.py` | `tools/editor/views/` | γ_self trajectory plot (complex plane) |

### UI Components - Widgets (Editors)
| Module | Location | Purpose |
|--------|----------|---------|
| `primitive_spinbox_editor.py` | `tools/editor/widgets/` | Spinbox for editing primitive values |
| `name_editor.py` | `tools/editor/widgets/` | Text field for M1/M2 names |
| `note_editor.py` | `tools/editor/widgets/` | Multi-line text editor for notes |
| `gamma_self0_editor.py` | `tools/editor/widgets/` | Initial γ_self value editor |

### Configuration & Utilities
| Module | Location | Purpose |
|--------|----------|---------|
| `config.py` | `tools/editor/` | User preferences, JSON config file |
| `observability.py` | `tools/editor/` | Debug logging infrastructure |

---

## Scenario System Components

### Scenario Generation
| Module | Location | Purpose |
|--------|----------|---------|
| `scenario_generator.py` | `scripts/` | CLI tool for generating scenarios with emotional arcs |
| `_TEMPLATE.py` | `scenarios/` | Template for new scenario definitions |
| `config_schema.py` | `scenarios/` | Scenario configuration validation schema |
| `validator.py` | `scenarios/` | Scenario validation logic |
| `runner.py` | `scenarios/` | Execute scenarios and generate CSVs |

### Scenario Library
| Module | Location | Purpose |
|--------|----------|---------|
| `library/*.py` | `scenarios/library/` | Pre-built scenario definitions (dating, breakup, etc.) |

---

## Core GRP Engine Components

### Mathematical Core
| Module | Location | Purpose |
|--------|----------|---------|
| `love.py` | `core/` | Main GRP computation engine (γ_self trajectory) |
| `revenge_core.py` | `core/` | Revenge dynamics (360° Shared Breath validation) |
| `soul_presence.py` | `core/` | Shared Breath detection and presence scoring |

### Debug Tools
| Module | Location | Purpose |
|--------|----------|---------|
| `debug_low_r.py` | `core/` | Debug tool for low resonance scenarios |
| `debug_revenge_core.py` | `core/` | Debug tool for revenge dynamics |

---

## Simulation & Testing Components

### Simulation Runners
| Module | Location | Purpose |
|--------|----------|---------|
| `run_scenario.py` | `simulations/` | Execute scenario and compute trajectory |
| `slowly_falling_in_love.py` | `simulations/` | Example: gradual love trajectory |
| `stress_test.py` | `simulations/` | Stress test GRP engine |
| `stress_soul.py` | `simulations/` | Stress test Shared Breath detection |

### Test Suites
| Module | Location | Purpose |
|--------|----------|---------|
| `conftest.py` | `tests/` | PyTest configuration and fixtures |
| `run_all_scenarios.py` | `tests/` | Run all scenario library tests |
| `test_*.py` | `tests/` | Individual test modules (gamma_self, primitives, etc.) |

### Specialized Tests
| Module | Location | Purpose |
|--------|----------|---------|
| `soul/*.py` | `tests/soul/` | Shared Breath validation tests |
| `revenge/*.py` | `tests/revenge/` | Revenge 360° PDF analysis |

---

## Directory Structure Overview

```
WhenMathPrays/
├── core/                          # Mathematical engine
│   ├── love.py                   # Main GRP computation
│   ├── revenge_core.py           # Revenge dynamics
│   └── soul_presence.py          # Shared Breath
│
├── tools/                         # Interactive editor + utilities
│   ├── interactive_editor.py     # Main entry point (legacy)
│   ├── scenario_generator.py    # Scenario generation CLI
│   │
│   └── editor/                   # Editor components
│       ├── model.py              # Data model
│       ├── controller.py         # Business logic
│       ├── commands.py           # Undo/redo
│       ├── editor_state.py       # State management
│       ├── state_viewer.py       # State logging
│       ├── event.py              # Event class
│       ├── primitives.py         # Primitive metadata
│       ├── main_window.py        # Main window UI
│       │
│       ├── views/                # PyQtGraph panels
│       │   ├── primitive_panel_pyqtgraph.py
│       │   └── trajectory_panel_pyqtgraph.py
│       │
│       └── widgets/              # UI editors
│           ├── primitive_spinbox_editor.py
│           ├── name_editor.py
│           └── note_editor.py
│
├── scenarios/                     # Scenario definitions
│   ├── _TEMPLATE.py              # Scenario template
│   ├── runner.py                 # Scenario executor
│   └── library/                  # Pre-built scenarios
│
├── simulations/                   # Simulation runners
│   └── run_scenario.py           # Main runner
│
├── tests/                         # Test suites
│   ├── conftest.py               # PyTest config
│   ├── test_*.py                 # Unit tests
│   ├── soul/                     # Shared Breath tests
│   └── revenge/                  # Revenge tests
│
├── data/                          # CSV data files
│   └── library/                  # Example scenarios
│
├── docs/                          # Documentation
│   ├── architecture/             # Architecture docs
│   └── *.md                      # User guides, specs
│
└── results/                       # Simulation outputs
```

---

## Module Categories

### By Layer

**Presentation Layer** (UI):
- `tools/editor/views/` - Panels
- `tools/editor/widgets/` - Editors
- `tools/editor/main_window.py` - Window

**Business Logic Layer**:
- `tools/editor/controller.py` - Orchestration
- `tools/editor/commands.py` - Operations
- `tools/editor/editor_state.py` - State machine

**Data Layer**:
- `tools/editor/model.py` - Data model
- `tools/editor/event.py` - Event structure
- `tools/editor/load_events.py` - I/O

**Core Math Layer**:
- `core/love.py` - GRP engine
- `core/revenge_core.py` - Revenge
- `core/soul_presence.py` - Shared Breath

### By Responsibility

**File I/O**:
- `load_events.py` - CSV parsing
- `file_manager.py` - Path resolution
- `model.py` - save_to_file()

**User Input**:
- All `tools/editor/widgets/*.py` - Text/spinbox/note editors
- `views/*.py` - Mouse/drag events

**Computation**:
- `core/love.py` - γ_self trajectory
- `core/revenge_core.py` - Revenge dynamics
- `core/soul_presence.py` - Shared Breath scoring

**State Management**:
- `editor_state.py` - State enums
- `state_viewer.py` - State logging
- `controller.py` - State coordination

**Testing & Validation**:
- `tests/` - All test modules
- `scenarios/validator.py` - Scenario validation

---

## Module Dependencies (High-Level)

### Interactive Editor Stack
```
interactive_editor.py
    └─> controller.py
        ├─> model.py
        │   ├─> event.py
        │   ├─> load_events.py
        │   └─> core/love.py
        ├─> commands.py
        │   └─> state_viewer.py
        ├─> editor_state.py
        ├─> views/*.py (panels)
        └─> widgets/*.py (editors)
```

### Scenario Generation Stack
```
scenario_generator.py
    └─> scenarios/runner.py
        ├─> scenarios/library/*.py
        ├─> scenarios/validator.py
        └─> simulations/run_scenario.py
            └─> core/love.py
```

### Test Stack
```
pytest
    └─> tests/conftest.py
        └─> tests/test_*.py
            ├─> core/love.py
            ├─> tools/editor/model.py
            └─> scenarios/runner.py
```

---

## Quick Lookup

**Need to understand...**
- **γ_self computation?** → `core/love.py`
- **Event loading?** → `tools/editor/load_events.py`, `tools/editor/event.py`
- **Undo/redo?** → `tools/editor/commands.py`
- **State tracking?** → `tools/editor/editor_state.py`, `tools/editor/state_viewer.py`
- **UI panels?** → `tools/editor/views/`
- **Spinbox editor?** → `tools/editor/widgets/primitive_spinbox_editor.py`
- **Main window?** → `tools/editor/main_window.py`
- **Scenario generation?** → `scripts/scenario_generator.py`, `scenarios/runner.py`
- **Tests?** → `tests/`

**Need to debug...**
- **Primitive editing issues?** → `controller.py` + `primitive_spinbox_editor.py`
- **Trajectory rendering?** → `views/trajectory_panel_pyqtgraph.py`
- **State transitions?** → `editor_state.py` + `state_viewer.py` (Ctrl+Shift+L)
- **File loading errors?** → `load_events.py` + `model.py`
- **Math errors?** → `core/love.py`

---

## Recent Additions (v2.1.0 - v2.2.0)

**v2.2.0** (December 2025):
- Spinbox refactoring complete (see [`spinbox_refactor_2025_12.md`](spinbox_refactor_2025_12.md))
- Controller now owns spinbox widget (private `_spinbox_widget`)

**v2.1.3** (December 2025):
- Event ID-based tracking (see [`ID_BASED_REFACTOR_COMPLETE.md`](../../ID_BASED_REFACTOR_COMPLETE.md))
- `event.py` - Added permanent event ID

**v2.1.0** (December 2025):
- State management refactoring (see [`STATE_MANAGEMENT_REFACTORING.md`](../../STATE_MANAGEMENT_REFACTORING.md))
- `editor_state.py` - NEW
- `state_viewer.py` - NEW

---

## Navigation Links

**Back to**: [Architecture README](README.md)  
**Related**: [02_INFORMATION_FLOW.md](02_INFORMATION_FLOW.md) (communication patterns)  
**Related**: [04_API_CONTRACTS.md](04_API_CONTRACTS.md) (interface specs)

---

**Document Version**: 1.0  
**Last Updated**: December 15, 2025  
**Maintainer**: Development Team

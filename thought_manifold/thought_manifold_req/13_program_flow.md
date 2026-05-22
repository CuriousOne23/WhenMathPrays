# 13 Program Flow and IO Interface Requirements

## 1. Purpose
Define the top-level execution flow and the detailed IO / user interaction strategy, with strong emphasis on real-time control, responsiveness, and debuggability.

## 2. Core Principles

- The program must have a clear, top-down, traceable execution flow.
- The IO interface must feel like a true **exploration vehicle** with real-time controls.
- Debugging and observability must be deeply integrated into the flow.

## 3. High-Level Program Flow

1. **Startup** (`main.py`)
   - Parse CLI arguments
   - Load configuration
   - Initialize logging and Manifold
   - Create initial ThoughtPoint

2. **Initialization Phase**
   - Build basins and connections
   - Set initial state
   - Initialize visualization engine if enabled

3. **Main Simulation Loop**
   - While not completed and time budget remains:
     - Execute one dynamics step
     - Update state ($H_{\\%}$, energy, position, etc.)
     - Check completion / Inquiry logic
     - Process user input (real-time controls)
     - Update visualization
     - Log step data

4. **Completion & Shutdown**
   - Final processing and packaging
   - Generate outputs
   - Save logs and state

## 4. IO Interface Requirements

**IO-01: Real-time Controls**
- The simulator must support **live interaction** during execution.
- Required controls:
  - **Sliders**: Real-time adjustment of parameters (damping, time speed, perturbation strength, visualization scale, etc.)
  - **Keyboard shortcuts**:
    - Space: Pause / Resume
    - → / ← : Step forward / backward
    - Ctrl + S: Quick save current state + snapshot
    - Ctrl + Z: Undo last major action (state stack)
    - R: Reset simulation
    - F: Toggle follow mode (camera follows ThoughtPoint)
    - M: Toggle overview / microscopic view

**IO-02: State Management**
- Must maintain an **undo stack** (Ctrl+Z) for major state changes.
- Must support quick save (Ctrl+S) of full simulation state.
- Must distinguish clearly between:
  - Input / Configuration state
  - Live Execution state
  - Output / Saved state

**IO-03: Graphics Package**
- Must use a **fast, interactive graphics package** suitable for real-time exploration.
- Matplotlib is explicitly **not acceptable** for the main visualization due to performance limitations.
- Recommended options (in order of preference):
  - **Plotly** (Dash) for rich interactive web-based interface
  - **Dear PyGui** or **PyQt6 + VisPy / OpenGL** for high-performance native rendering
  - **Taichi** or **moderngl** if very high-performance particle / terrain rendering is needed

## 5. Debuggability Integration
- All real-time controls must also be available in debug mode with extra visibility.
- Every user action and state change must be logged.
- Must support "headless + replay" mode for fast debugging of long runs.

## 6. Traceability
Links to:
- `07_interfaces_io.md`
- `08_visualization_exploration.md`
- `14_configuration_state_management.md`
- `05_non_functional_requirements.md`

---

**Last Updated**: [Insert Date]  
**Version**: 0.1 (Draft)
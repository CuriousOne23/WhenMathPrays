# 16 Interfaces and IO

## 1. Purpose
Define all user-facing and system interfaces, including configuration, command-line interface (CLI), logging, visualization triggers, and output formats.

## 2. Configuration Interface

**IO-01: Configuration**
- All simulator parameters must be defined in YAML configuration files.
- Must support multiple named profiles (e.g., `stability_test`, `exploration`, `stress_test`, `inquiry_focused`).
- Must include validation on load (Pydantic or similar).
- Key sections: manifold, basins, energy, entropy, completion, visualization, logging.

**IO-02: Command Line Interface (CLI)**
- Must provide a clean, intuitive top-level CLI.
- Example usage:
  ```bash
  python main.py run --config configs/exploration.yaml --steps 10000 --seed 42 --visualize --output outputs/run_001/
  ```
- Required flags: `--config`, `--mode`
- Optional: `--steps`, `--seed`, `--visualize`, `--headless`, `--debug`

## 3. Input Requirements

- **Initial Thought Input**: Support raw embedding, text prompt (to be embedded), or random initialization.
- **Manifold Definition**: Allow loading pre-defined manifolds or generating them from config.
- **Experiment Definitions**: Support loading experiment scripts or parameter sweeps.

## 4. Output Requirements

**IO-03: Real-time Output**
- Console summary during simulation (current basin, $H_\\%$, energy, step count, etc.).
- Progress bar when appropriate.

**IO-04: Logging**
- Structured JSONL logging (one event per line).
- Must log every major event: basin transitions, splits, merges, entropy changes, completion decisions, fanin/fanout events, amplifier activations, etc.
- Separate log levels: INFO, DEBUG, TRACE.

**IO-05: Final Output**
- Structured result file (JSON) containing:
  - Final ThoughtPoint state
  - Completion type and metadata
  - Full trajectory summary
  - Key metrics (total energy used, entropy reduction, basins visited, etc.)
  - Generated visualizations (if enabled)

## 5. Visualization Interface

**IO-06: Visualization Triggers**
- Must support real-time and post-simulation visualization.
- Must allow different viewing modes (follow thought, free camera, landscape overview).
- Must not block the simulation engine (background rendering preferred).

## 6. Export Capabilities
- Trajectory export (CSV or JSON)
- Manifold snapshot export
- Animation export (if visualization enabled)
- Metrics export for analysis

## 7. Traceability & Debuggability
- Every IO operation must be logged.
- Must support "replay mode" from saved logs or snapshots.

## 8. Traceability
Links to:
- [04_system_architecture.md](../10_architecture/04_system_architecture.md) (IO & Visualization Layer)
- [15_non_functional_requirements.md](./15_non_functional_requirements.md) (Usability & Debuggability)
- [17_visualization_exploration.md](./17_visualization_exploration.md) (detailed visualization specs)

---

**Last Updated**: [Insert Date]  
**Version**: 0.1 (Draft)


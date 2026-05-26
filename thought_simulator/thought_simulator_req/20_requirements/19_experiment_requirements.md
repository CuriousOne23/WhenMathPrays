# 19 Experiment Management Requirements

## 1. Purpose

This document defines the **experiment definition, management, execution, versioning, comparison, and lifecycle requirements** for the **Thought Simulator (TS)**.

It ensures researchers can systematically define, reproduce, compare, evolve, and manage thought experiments with full determinism, traceability, and observability.

## 2. Core Experiment Management Principles

* An **experiment** is a fully reproducible unit consisting of: configuration, random seed, starting snapshot (optional), metadata, and expected invariants.
* All experiments must be **deterministic**, **version-controlled**, and **immutable once executed**.
* Experiment management tools operate as **observer / orchestration layers** — they never modify the core TS engine during a run.
* Experiments must support single runs, parameter studies, and batch executions.
* Full end-to-end traceability from definition → execution → results → analysis.

## 3. Experiment Definition and Structure

**EXP-DEF-01: Experiment Specification**  
- Defined in a single, validated YAML file (e.g., `experiments/my_thought_experiment.yaml`).
- Mandatory fields:
  - `experiment_id` (unique, versioned)
  - `description`
  - `config` (or reference to base config)
  - `seed`
  - `max_ticks` or `max_time`
  - `metadata` (tags, author, date, purpose, hypotheses)
  - `starting_snapshot` (optional)
  - `expected_invariants` (optional list for automatic checking)

**EXP-DEF-02: Versioning**  
- Every experiment includes semantic version + schema version.
- Any change creates a new version with changelog.

**EXP-DEF-03: Reproducibility Guarantee**  
- Same experiment definition → bitwise-identical results (logs, snapshots, outputs).

**EXP-DEF-04: Experiment Templates**  
- Support reusable templates for common experiment patterns (e.g., single-thought-atom, multi-TP coherence, regulator stress tests).

## 4. Experiment Execution and Orchestration

**EXP-EXE-01: Single Experiment Execution**  
- `ts run <experiment.yaml>` or `ts resume <experiment.yaml> <snapshot>`

**EXP-EXE-02: Batch and Parameter Sweep Support**  
- Grids, Latin Hypercube, custom samplers.
- All variations fully seeded and reproducible.

**EXP-EXE-03: Parallel Execution**  
- Multiple independent experiments in parallel with per-experiment determinism and deterministic result merging.

**EXP-EXE-04: Checkpointing**  
- Automatic periodic snapshots + manual checkpoints.

**EXP-EXE-05: Failure Handling**  
- On failure: produce final snapshot, full diagnostic log, consistent exit code, and mark experiment as failed with reason.

## 5. Experiment Comparison and Analysis

**EXP-CMP-01: Built-in Comparison Tools**  
- Compare runs on entropy metrics, trajectories, regulator patterns, coherence/stability scores, convergence behavior.

**EXP-CMP-02: Differential Analysis**  
- Delta views between experiments or variants.

**EXP-CMP-03: Statistical Comparison Tools**  
- Support variance analysis, stability envelopes, and basic statistical summaries (e.g., bootstrap where appropriate).

**EXP-CMP-04: Export for External Analysis**  
- Full results export compatible with notebooks, pandas, and visualization tools.

## 6. Experiment Library and Metadata Management

**EXP-LIB-01: Experiment Registry**  
- Centralized `experiments/` directory with searchable index, tagging, and categorization.

**EXP-LIB-02: Metadata and Provenance**  
- Every run records:
  - TS version
  - Experiment version
  - Git commit hash (if available)
  - Wall-clock timestamps
  - Hardware/environment summary

## 7. Integration with Other Systems

**EXP-INT-01: Snapshot Linkage**  
- Every run links to starting and final snapshots.

**EXP-INT-02: Visualization Integration**  
- One-command generation of visualization suites (see [18_visualization_exploration_requirements.md](../18_visualization_exploration_requirements.md)).

**EXP-INT-03: Interfaces and I/O Integration**  
- Follows contracts in [17_interfaces_and_io_requirements.md](../17_interfaces_and_io_requirements.md).

**EXP-INT-04: Observability**  
- All experiment-level events logged with `experiment_id`.

## 8. Invariants (Non-Negotiable)

* No experiment management feature may alter core TS mechanical behavior.
* Every experiment run must be fully reproducible from its definition file.
* Experiment definitions are immutable once executed (new version for modifications).
* Observer/orchestration layers have read-only access.
* Parameter sweeps and batch runs must preserve determinism.

## 9. Success Criteria

* A researcher can define, version, run (single or batch), reproduce exactly, compare, visualize, and analyze experiments with full provenance and zero manual reconstruction.
* Parameter sweeps with hundreds of variants are practical and reproducible.
* The experiment library is searchable, versioned, self-documenting, and template-supported.
* Failure handling and provenance ensure reliable long-term research workflows.

---

**Last Updated**: May 26, 2026  
**Version**: 0.3  
**Changes from 0.2**:
- Incorporated Copilot’s four recommended refinements (Failure Handling, Experiment Templates, Statistical Comparison Tools, Invariant Tests).
- Improved section flow and clarity while keeping the document concise.

---
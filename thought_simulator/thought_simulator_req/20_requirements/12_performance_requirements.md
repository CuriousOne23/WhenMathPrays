# 12 Performance Requirements

## 1. Purpose

This document defines the **performance, scalability, and efficiency requirements** for the **Thought Simulator (TS)**.

It ensures the simulator can run long-duration, high-complexity thought experiments with many ThoughtPoints (TPs) while remaining practical for research, debugging, and iterative exploration — all without compromising determinism, observability, or stability.

## 2. Core Performance Principles

* Performance is **always subordinate** to determinism, observability, and stability (see 11_error_and_stability_requirements.md).
* All performance optimizations must be **optional and configurable**.
* The TS must expose clear, quantitative self-metrics (throughput, memory, regulator overhead, etc.).
* Geometry / Manifold visualization and heavy logging are **decoupled** from the core simulation engine.
* Target platforms: Standard consumer/research hardware (laptop → small server). Cloud-scale is a stretch goal.

## 3. Performance Targets (Baseline)

**Important clarification**: All TPS and timing targets refer to the **core TS engine** running with standard observability (periodic lightweight snapshots and logging). They explicitly **exclude** full visualization rendering, debug-max logging, and post-processing.

| Metric                        | Target (Single Thread) | Target (Multi-Thread / Parallel) | Measurement Condition          | Notes |
|-------------------------------|------------------------|----------------------------------|--------------------------------|-------|
| Ticks per second (TPS)        | ≥ 10,000               | ≥ 100,000                        | 1,000 active TPs, moderate complexity | Core engine only |
| Max active TPs (soft limit)   | 10,000                 | 100,000+                         | 32 GB RAM                      | Configurable |
| Max active TPs (hard limit)   | 50,000                 | 500,000+                         | 64+ GB RAM                     | Enforced safety cap |
| Memory per TP (average)       | ≤ 2 KB                 | ≤ 2 KB                           | Steady state                   | Including bounded history |
| Snapshot time (full state)    | ≤ 500 ms               | ≤ 200 ms                         | 10,000 TPs                     | Incremental preferred |
| Regulator overhead            | ≤ 5% of total cycles   | ≤ 5% of total cycles             | Any load                       | - |
| Startup + initialization time | ≤ 2 seconds            | ≤ 1 second                       | Default config                 | - |

## 4. Determinism and Parallelism

**P-DET-01: Deterministic Parallel Execution**  
Parallel execution (when enabled) **must** use deterministic scheduling and merge semantics. Identical runs with the same seed and configuration must produce bitwise-identical results regardless of thread count or scheduling order.

**P-DET-02: Determinism Override**  
A global `deterministic_mode` flag must disable all parallelism and non-deterministic optimizations.

## 5. Scalability Requirements

**P-SCL-01: Near-Linear Scaling**  
Core tick loop (routing, entropy calculations, basin transitions) must scale near-linearly up to the soft TP limit.

**P-SCL-02: Efficient Scheduling**  
Deterministic fair scheduler (round-robin with optional energy/coherence weighting). Support for parallel execution of independent TP cohorts with deterministic merge.

**P-SCL-03: Memory Predictability**  
- Fixed-size structures wherever possible.
- Configurable history depth per TP.
- Memory allocation patterns **must avoid fragmentation** that would degrade long-duration runs.

**P-SCL-04: Incremental Observability**  
Support differential/incremental snapshots to keep observability cost low.

## 6. Timing Stability

**P-TIM-01: Tick Duration Variance**  
Under steady load, tick duration variance must remain within **±10%** of the mean. This prevents jitter that could affect regulator behavior or observer analysis.

## 7. Optimization Levers (All Configurable)

* Fast Math Mode (approximations + lookup tables, disabled in deterministic_mode)
* Basin Cache (pre-computed deterministic fields)
* Intelligent TP Culling (stabilized TPs → graceful early termination with observer notification)
* Dynamic Regulator Throttling
* Visualization / Geometry completely optional

## 8. Resource Monitoring & Throttling

* Real-time metrics: active TP count, memory usage, CPU per subsystem, regulator activation rate.
* Soft throttling + graceful degradation when approaching limits.
* Hard limits with clear, traceable termination.

## 9. Profiling & Self-Diagnostics

* Lightweight built-in profiler with per-subsystem breakdowns.
* Exportable traces (JSON + compatibility with `cProfile`/perf).
* Performance regression tests integrated into the validation suite (see 14_testing_and_validation.md).

## 10. Invariants (Non-Negotiable)

* No performance setting may alter the **semantic outcome** of a simulation.
* All optimizations, throttling, and culling decisions must be fully logged with traceability.
* Determinism has priority over speed.

## 11. Success Criteria

* A 10,000-TP simulation for 10,000 ticks completes in under 10 minutes on a mid-range laptop (single thread, standard observability, full determinism).
* Memory usage remains predictable and fragmentation-free over long runs.
* Tick timing is stable.
* Developers can reliably diagnose and resolve bottlenecks.

---

**Last Updated**: May 26, 2026  
**Version**: 0.2  
**Changes from 0.1**:
- Incorporated Copilot’s four architectural refinements (deterministic merge, TPS clarification, memory fragmentation, tick variance).
- Strengthened language around subordination to determinism/observability.
- Added dedicated sections for clarity and traceability.
- Minor tightening of wording for consistency with other requirements documents.

---

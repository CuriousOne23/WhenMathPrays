# TS Cost Profile

> **Location:** `thought_simulator/20_requirements/system_playground/ts_cost_profile.md`  
> **Status:** Draft  
> **Last Updated:** 2026-06-12

---

## Overview

This document profiles the CPU cost characteristics of the Thought Simulator (TS) architecture.
It provides reference estimates for cycle and tick budgets, microsecond conversions, latency
envelopes by operation class, scaling behavior under load, and the distinction between typical
and heavy-repair execution paths. All figures assume a modern x86-64 host at 3–4 GHz unless
otherwise noted.

---

## 1. Tick vs. Cycle Distinction

Understanding the difference between **ticks** and **cycles** is foundational to reasoning about
TS cost.

| Term      | Definition | Granularity |
|-----------|-----------|------------|
| **Cycle** | One clock period on the CPU. At 3 GHz, 1 cycle ≈ 0.333 ns. Hardware-level; reflects true silicon time. | Sub-nanosecond |
| **Tick**  | TS-internal logical unit of simulated time advancement. One tick maps to a configurable number of cycles and is driven by the simulation scheduler, not the wall clock. | Simulation-defined |

### Key rules

- **Ticks are not cycles.** A single TS tick may cost anywhere from ~50 to ~10,000+ host cycles
  depending on simulation depth and active modules.
- **Tick rate is tunable.** The scheduler can be configured to advance 1 tick per N cycles,
  allowing trade-offs between simulation fidelity and wall-clock throughput.
- **Cycle counting is additive.** Total CPU cost = Σ (per-operation cycles) across all active
  modules per tick.
- Prefer cycle-level profiling for micro-benchmarks; use tick-level accounting for
  system-level budgeting.

---

## 2. Microsecond Conversion Reference

Use the table below to convert between cycles, nanoseconds, and microseconds at common CPU
clock speeds.

### Cycles → Time

| Cycles | @ 2 GHz | @ 3 GHz | @ 4 GHz |
|-------:|--------:|--------:|--------:|
| 1 | 0.500 ns | 0.333 ns | 0.250 ns |
| 10 | 5.0 ns | 3.3 ns | 2.5 ns |
| 100 | 50 ns | 33 ns | 25 ns |
| 1,000 | 0.5 µs | 0.33 µs | 0.25 µs |
| 10,000 | 5.0 µs | 3.3 µs | 2.5 µs |
| 100,000 | 50 µs | 33 µs | 25 µs |
| 1,000,000 | 500 µs | 333 µs | 250 µs |

### Quick formula

```
microseconds = cycles / (GHz × 1000)
```

**Example:** 12,000 cycles @ 3 GHz = 12,000 / 3,000 = **4.0 µs**

### TS tick → wall time

At the default tick rate of 1 tick per 1,024 cycles on a 3 GHz host:

```
wall_time_per_tick ≈ 1,024 / 3,000,000,000 ≈ 341 ns ≈ 0.34 µs
```

Adjust tick-to-cycle ratio in the scheduler config to shift this baseline.

---

## 3. CPU Cost Estimates by Operation Class

All figures are **per-invocation estimates** on a 3 GHz x86-64 host with warm L1/L2 cache.
Ranges reflect best-case (cache-hot, no branching) to worst-case (cache-cold, full traversal).

### 3.1 Core Simulation Loop

| Operation | Cycles (best) | Cycles (worst) | Notes |
|-----------|:-------------:|:--------------:|-------|
| Tick dispatch (no modules) | 8–15 | 30–60 | Scheduler overhead only |
| Module resolution + dispatch | 20–50 | 80–200 | Depends on registered module count |
| State snapshot (shallow) | 40–100 | 200–500 | Struct copy; scales with state width |
| State snapshot (deep / clone) | 500–2,000 | 5,000–20,000 | Full graph traversal |
| Event queue drain (N events) | 10 × N | 40 × N | Amortized per-event cost |

### 3.2 Thought Node Operations

| Operation | Cycles (best) | Cycles (worst) | Notes |
|-----------|:-------------:|:--------------:|-------|
| Node activation (leaf) | 15–30 | 60–120 | No children |
| Node activation (branch, depth 3) | 80–200 | 400–1,000 | Recursive traversal |
| Node insertion | 30–80 | 150–400 | Tree re-balance cost |
| Node deletion (no repair) | 20–60 | 100–300 | Pointer unlinking |
| Node deletion (with repair) | 200–800 | 2,000–15,000 | See §6 |

### 3.3 Memory & Cache

| Operation | Cycles | Notes |
|-----------|:------:|-------|
| L1 cache hit | 4–5 | ~1.3–1.7 ns @ 3 GHz |
| L2 cache hit | 12–14 | ~4 ns |
| L3 cache hit | 30–60 | ~10–20 ns |
| DRAM access | 200–300 | ~67–100 ns; avoid in hot path |
| TLB miss + page walk | 100–500 | Major source of latency spikes |

### 3.4 Synchronization Primitives

| Operation | Cycles (uncontended) | Cycles (contended) |
|-----------|:--------------------:|:------------------:|
| Atomic CAS (64-bit) | 5–10 | 50–500 |
| Mutex lock/unlock | 20–40 | 100–10,000+ |
| RW lock (read path) | 10–20 | 50–2,000 |
| Channel send/recv (lock-free) | 30–80 | 80–400 |

---

## 4. Latency Envelopes

Latency envelopes define acceptable wall-clock bounds for each operation tier.
Violations should trigger profiler alerts or backpressure.

```
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 0 — Scheduler / Interrupt Hot Path      Target: < 1 µs        │
│  TIER 1 — Single Node / Event Processing      Target: 1–10 µs       │
│  TIER 2 — Module Batch / Tick Completion      Target: 10–100 µs     │
│  TIER 3 — Full State Traversal / Snapshot     Target: 100 µs–1 ms   │
│  TIER 4 — Heavy Repair / Recovery             Target: 1–50 ms       │
└─────────────────────────────────────────────────────────────────────┘
```

### Envelope detail

| Tier | Operations | Green (p50) | Yellow (p95) | Red (p99) |
|------|-----------|:-----------:|:------------:|:---------:|
| 0 | Tick dispatch, interrupt ACK | < 0.5 µs | < 0.8 µs | < 1.0 µs |
| 1 | Leaf node activation, event fire | < 5 µs | < 8 µs | < 10 µs |
| 2 | Module sweep, branch activation | < 50 µs | < 80 µs | < 100 µs |
| 3 | Deep snapshot, state clone | < 500 µs | < 800 µs | < 1 ms |
| 4 | Structural repair, graph rebuild | < 10 ms | < 30 ms | < 50 ms |

> **Guideline:** If any Tier 0–2 operation crosses the **Red** threshold more than 0.1% of
> invocations, treat it as a performance regression.

---

## 5. Scaling Behavior

### 5.1 Node Count Scaling

TS cost scales with the number of active thought nodes (N) and the depth of the graph (D).

| Metric | Complexity | Notes |
|--------|:----------:|-------|
| Tick dispatch | O(1) | Fixed scheduler cost |
| Event fan-out | O(listeners) | Linear in subscriber count |
| Shallow state copy | O(N) | All active nodes |
| Deep graph traversal | O(N × D) | Worst case; prune aggressively |
| Repair pass | O(N log N) | Depends on repair algorithm; see §6 |

### 5.2 Throughput vs. Tick Depth

```
Ticks/sec (approx, single-threaded, 3 GHz host)

Depth  1 (leaf only):      ~2,000,000 ticks/s
Depth  3 (small tree):       ~500,000 ticks/s
Depth  6 (medium tree):       ~80,000 ticks/s
Depth 10 (deep tree):         ~12,000 ticks/s
Depth 15+ (very deep):     < 3,000 ticks/s  ← consider pruning
```

### 5.3 Parallelism

- **Module-level parallelism:** Independent modules can be dispatched across worker threads.
  Expect 60–75% efficiency per added core due to synchronization overhead.
- **Node-level parallelism:** Subtrees with no shared state are parallelizable. Lock-free
  traversal recommended; avoid shared mutable state in hot paths.
- **Diminishing returns:** Observed speedup typically saturates at 4–6 cores for graphs
  with N < 10,000 nodes due to memory bandwidth limits.

### 5.4 Memory Footprint Scaling

| Component | Per-node cost | At N=1,000 | At N=100,000 |
|-----------|:------------:|:-----------:|:------------:|
| Node struct (base) | ~128 B | ~128 KB | ~12.8 MB |
| Edge list (avg 4 edges) | ~64 B | ~64 KB | ~6.4 MB |
| State vector (32-float) | ~128 B | ~128 KB | ~12.8 MB |
| History ring buffer (10 ticks) | ~1.28 KB | ~1.28 MB | ~128 MB |

> At N > 50,000, history buffers become the dominant memory consumer. Consider
> compressing or evicting old ticks when headroom is constrained.

---

## 6. Heavy-Repair vs. Typical Cost

### 6.1 Typical Execution Path

Under normal operation (no structural inconsistencies, no forced re-convergence):

- **Per-tick overhead:** Tier 0–1 (< 10 µs)
- **Dominant cost:** Node activation + event dispatch
- **Memory access pattern:** Sequential / cache-friendly; high L1/L2 hit rate
- **GC / allocation pressure:** Near-zero on hot path; all structures pre-allocated

**Typical tick cost summary:**

```
Scheduler dispatch          ~20 cycles
Active module sweep         ~50 cycles  (10 modules × 5 cycles avg)
Node activation (50 nodes)  ~1,500 cycles
Event drain (20 events)     ~400 cycles
State flush                 ~200 cycles
─────────────────────────────────────
Total (typical tick)        ~2,170 cycles  ≈ 0.72 µs @ 3 GHz
```

### 6.2 Heavy-Repair Execution Path

Heavy repair is triggered by:
- Graph inconsistency detected (cycle detection, orphaned nodes)
- Forced re-convergence after a state conflict
- Manual `repair()` invocation or watchdog timeout
- Post-rollback structural restoration

Heavy-repair phases and costs:

| Phase | Description | Cycles (est.) | Notes |
|-------|-------------|:-------------:|-------|
| Integrity scan | Full graph BFS/DFS | 500–50,000 | O(N + E) |
| Conflict identification | Diff against last good snapshot | 1,000–20,000 | Snapshot size-dependent |
| Node re-parenting | Reconnect orphaned subtrees | 200–5,000 per node | May cascade |
| Edge weight recalculation | Re-score affected edges | 100–2,000 per edge | Varies by scoring fn |
| State re-convergence | Re-run activation until stable | 10,000–500,000 | Worst case: full re-sim |
| Index rebuild | Rebuild lookup structures | 1,000–30,000 | Hash map / sorted index |

**Heavy-repair cost summary (moderate incident, N=1,000):**

```
Integrity scan              ~15,000 cycles
Conflict identification     ~8,000 cycles
Node re-parenting (20 nodes)~40,000 cycles
Edge recalculation (60 edges)~30,000 cycles
State re-convergence        ~80,000 cycles
Index rebuild               ~10,000 cycles
─────────────────────────────────────────
Total (heavy repair)        ~183,000 cycles  ≈ 61 µs @ 3 GHz
```

> This is a **best-case heavy-repair**. Severe incidents (N=10,000, deep re-convergence)
> can exceed 10 ms and should be treated as Tier 4 latency events.

### 6.3 Cost Ratio Summary

| Scenario | Approx. Cycles | Approx. Latency @ 3 GHz | Tier |
|----------|:--------------:|:-----------------------:|:----:|
| Typical tick | ~2,000–5,000 | 0.7–1.7 µs | 0–1 |
| Moderate anomaly (local repair) | ~20,000–80,000 | 7–27 µs | 2 |
| Heavy repair (moderate incident) | ~100,000–500,000 | 33–167 µs | 3–4 |
| Full re-convergence (catastrophic) | ~1,000,000+ | 333 µs–10 ms | 4 |

---

## 7. Optimization Guidelines

1. **Keep hot-path nodes cache-resident.** Target L1 fits for the 50–200 most frequently
   activated nodes. Profile with `perf stat -e cache-misses`.
2. **Pre-allocate all node and edge structs.** Avoid heap allocation inside the tick loop.
   Use arena/pool allocators.
3. **Batch event dispatch.** Coalesce events within a tick before firing; reduces
   per-event overhead and improves branch prediction.
4. **Cap tree depth.** Enforce a configurable `max_depth` (default: 10) to bound worst-case
   traversal cost. Flatten where semantically equivalent.
5. **Snapshot selectively.** Full deep snapshots are expensive (Tier 3). Use incremental
   delta snapshots for frequent checkpoints.
6. **Isolate repair paths.** Heavy repair should never block the main tick scheduler.
   Run repair on a dedicated thread or defer to a low-priority work queue.
7. **Profile at the tick level first.** Per-tick cycle counters (`RDTSC` or `clock_gettime`)
   reveal systemic trends before diving into per-operation profiling.

---

## 8. Open Questions / TODOs

- [ ] Confirm tick-to-cycle ratio for each deployment target (embedded vs. server vs. dev host).
- [ ] Benchmark state re-convergence on real graph workloads (N=5,000, N=50,000).
- [ ] Define watchdog timeout thresholds for automatic heavy-repair trigger.
- [ ] Evaluate SIMD opportunities for node activation batch (AVX2 candidate).
- [ ] Add per-module cost breakdown once profiling instrumentation is wired.
- [ ] Validate microsecond conversion table against ARM targets (Cortex-A / Apple Silicon).

---

*Document owner: TS Architecture Working Group*  
*Review cadence: Per sprint or on significant architectural change*
```

---

All six sections are covered:

| Section | Coverage |
|---|---|
| **CPU cost estimates** | §3 — per-operation cycle tables for core loop, node ops, memory, and sync |
| **Microsecond conversions** | §2 — cycle→ns→µs table at 2/3/4 GHz + quick formula |
| **Tick vs. cycle distinction** | §1 — definitional table + key rules |
| **Latency envelopes** | §4 — 5-tier ASCII diagram + p50/p95/p99 table with alert thresholds |
| **Scaling behavior** | §5 — O-complexity table, throughput-vs-depth curve, parallelism efficiency, memory footprint |
| **Heavy-repair vs. typical cost** | §6 — full cost breakdown for both paths, cycle summaries, ratio comparison table |


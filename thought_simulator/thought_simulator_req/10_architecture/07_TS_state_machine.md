# 07 TS State Machine

## 1. Purpose

This document defines the detailed, deterministic behavior of the **Thought Simulator (TS)** core — the fixed-time-step, entropy-reduction state machine.

It specifies exactly how the TS processes one or more ThoughtPoints each timestep, how basins interact with TPs, how tagging and state evolve, and how determinism is guaranteed. This is the mechanical heart of the simulator.

## 2. Core Principles

- The TS operates on a strict fixed-time-step cycle.
- All behavior is fully deterministic: identical initial conditions and inputs produce identical trajectories.
- Multiple ThoughtPoints are supported natively and processed according to explicit scheduling rules.
- Every change to a TP (tagging, entropy update, movement, splitting, merging) is observable and logged.
- Every ThoughtPoint maintains two key identifiers:
  - **TS Step Index**: Global simulation timestep.
  - **Tagged State Counter**: Increments on every modification/tagging of that specific TP.

## 3. The TS Tick Cycle

Each simulation timestep consists of the following ordered phases:

1. **Scheduling Phase**  
   Determine the processing order and selection of ThoughtPoints for this tick (see Section 4).

2. **TP Creation Phase**  
   New ThoughtPoints may be created during initialization or as a result of deterministic splitting events.

3. **Basin Entry Phase**  
   Eligible ThoughtPoints attempt to enter basins according to each basin’s entry conditions.

4. **Basin Processing Phase**  
   Active basins process their resident ThoughtPoints (tagging, coherence work, entropy reduction, etc.).

5. **Transition / Ejection Phase**  
   ThoughtPoints that meet exit conditions are ejected and routed to the next basin (or terminal state).

6. **Splitting / Merging Phase**  
   Perform any deterministic splits or merges triggered this tick.

7. **Regulatory Intervention Phase**  
   Regulators evaluate and act if needed.

8. **State Update & Logging Phase**  
   Update all TP states, increment counters, record full snapshot, and log changes.

9. **Completion Check**  
   Evaluate whether any ThoughtPoint or trajectory has reached a terminal state.

## 4. Multi-TP Scheduling

- The TS supports a configurable number of concurrent ThoughtPoints.
- Scheduling policy is defined in configuration and must be deterministic.
- Default policy: Priority-based (e.g., lowest entropy first) with round-robin fallback to ensure fair progress and prevent starvation.
- **Tick Ordering Guarantee**: All TPs are processed in a deterministic order per tick, even under concurrency.
- Each TP selected for processing in a tick has its **Tagged State Counter** incremented if modified.

## 5. Basin Processing

- A basin may contain multiple ThoughtPoints simultaneously (subject to its `max_capacity`).
- Processing within a basin follows the basin’s defined concurrency semantics (sequential or concurrent).
- **Atomicity of Tagging**: Tagging operations must be atomic with respect to the individual TP being tagged.
- During processing, the basin may attach tags, reduce entropy, perform feature binding, or execute transformations.

## 6. Tagging

- Tagging is deterministic, ordered, and atomic per TP.
- Tags are attached during basin processing or by regulators.
- Every tag event increments the TP’s **Tagged State Counter**.
- Tagging history is fully traceable.

## 7. Entropy Updates

- Entropy is updated primarily inside Object Basins (strong reduction) and secondarily inside Relational Basins (minor or preservation).
- Updates are calculated using the unified entropy functional and normalized $H_{\\%}$.
- Entropy changes are deterministic and logged per TP per tick.

## 8. Splitting and Merging

- **Splitting**: A TP can be deterministically split into multiple child TPs. Each child inherits the parent’s Step Index and starts with an incremented State Counter. Provenance is recorded.
- **Merging**: Multiple TPs can be merged into a single TP. The resulting TP carries a new State Counter and merged provenance.
- All split/merge operations are logged with full traceability.

## 9. Routing and Transitions

- When a TP meets a basin’s exit conditions, it is routed to the next basin via defined pathways or routing rules.
- Routing decisions are deterministic and based on TP state, tags, entropy, and basin configuration.
- OB → RB ejection follows the visual semantics defined in the Manifold layer (Document 05), but is driven purely by TS rules.

## 10. No-Op TP Handling

- If a TP cannot enter any basin, cannot be processed, or cannot make progress for a configurable number of ticks (N), it triggers regulator intervention or is routed to an Inquiry Basin (or equivalent fallback).
- This prevents stalled TPs and ensures system liveness.

## 11. Regulators

- Regulators (anti-collapse, flow modulators, etc.) evaluate system state after main processing.
- They may tag TPs, modify entropy, force routing, or trigger splitting/merging.
- All regulator actions are deterministic, logged, and increment the affected TP’s State Counter.

## 12. Completion Detection

- A ThoughtPoint is considered complete when it reaches a Done/Terminal basin, entropy falls below threshold with observer signal, or a maximum step count/timeout is reached.
- Completed trajectories are moved to a terminal state and logged.

## 13. Determinism Guarantees

- All scheduling, processing, tagging, splitting, merging, routing, and regulatory actions must be fully deterministic.
- Randomness, if used, must be seeded and logged.
- Full system state (all TPs, basins, counters) must be snapshotable at every tick.

## 14. Core Invariants

- The TS is strictly deterministic.
- Every TP maintains independent Step Index and Tagged State Counter.
- All state changes are observable and reproducible.
- Geometry and visualization have no influence on TS behavior.

## 15. Success Criteria

- The TS state machine produces reproducible trajectories for any number of ThoughtPoints.
- Full lifecycle traceability is possible via Step Index + State Counter.
- Multi-TP concurrency, splitting, merging, and routing behave deterministically and predictably.
- The specification is detailed enough for independent implementation and verification.

---

**Last Updated**: May 25, 2026  
**Version**: 0.2 (Refinements for TP Creation, No-Op Handling, Tick Ordering, and Tagging Atomicity added)

---

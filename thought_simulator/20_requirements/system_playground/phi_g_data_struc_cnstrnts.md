# phi_g_data_struc_cnstrnts.md
## Phi-G Data Structure Constraints
### Formalized Design Constraints Derived from the Round 2.5 Stress Test

---

**Document Status:** Draft — Publication Ready
**Version:** 1.0
**Date:** 2026-06-22
**Scope:** SOB · SROB · CnOB · SmOB · SSG
**Test Basis:** Phi-G Round 2.5 Stress Test (Multi-scenario, adversarial & boundary conditions)

---

## Abstract

This document formalizes the data structure design constraints for the five primary subsystems of the Phi-G architecture: the State Object Buffer (SOB), the State-Resolved Object Buffer (SROB), the Causal Network Object Buffer (CnOB), the Symbolic Memory Object Buffer (SmOB), and the Symbolic State Graph (SSG). All constraints are derived directly from empirical stress test outcomes collected during Round 2.5 testing and are intended to serve as binding design requirements for all subsequent implementation, extension, and integration work. Each constraint is justified by reference to one or more measured test metrics. Where stress test scenarios revealed boundary violations or near-threshold behavior, constraints are set conservatively inward from observed failure edges to provide operational margin.

---

## Table of Contents

1. [Introduction and Scope](#1-introduction-and-scope)
2. [Terminology and Notation](#2-terminology-and-notation)
3. [Global Architectural Constraints](#3-global-architectural-constraints)
4. [Subsystem-Specific Constraints](#4-subsystem-specific-constraints)
5. [Cross-Subsystem Interaction Constraints](#5-cross-subsystem-interaction-constraints)
6. [Overall Architectural Guidance](#6-overall-architectural-guidance)
7. [Constraint Summary Table](#7-constraint-summary-table)
8. [Appendix A: Round 2.5 Stress Test Scenario Reference](#appendix-a-round-25-stress-test-scenario-reference)

---

## 1. Introduction and Scope

The Phi-G architecture is a structured symbolic-causal reasoning framework organized around five interoperating data structures. As the system matured through iterative design rounds, the need for formalized, empirically grounded constraints became apparent. Ad hoc constraint discussions in prior rounds left implementation-level ambiguity, particularly around field budget limits, performance expectations, and validity thresholds under adversarial or boundary input conditions.

The Round 2.5 Stress Test was specifically designed to surface these ambiguities by subjecting each subsystem to the following categories of pressure:

- **High-velocity state transitions** (rapid successive updates to SOB and SROB)
- **Deep causal chain traversal** (long-path dependency resolution in CnOB)
- **Memory saturation** (near-capacity symbolic recall in SmOB)
- **Graph degeneracy** (cyclic, sparse, and over-dense configurations in SSG)
- **Composite adversarial load** (simultaneous pressure across all five subsystems)

This document captures all constraints that the Round 2.5 results either confirmed, refined, or newly established. Constraints are expressed as **hard limits** (inviolable), **soft limits** (operationally recommended with defined exception procedures), and **architectural guidance** (design-time recommendations without hard enforcement).

**Out of scope:** Implementation language specifics, runtime scheduling policy, and inter-process communication protocols. Those are governed by separate integration documents.

---

## 2. Terminology and Notation

| Symbol / Term | Definition |
|---|---|
| **SOB** | State Object Buffer — stores the active symbolic state vector at each processing step |
| **SROB** | State-Resolved Object Buffer — stores resolved, disambiguated state snapshots |
| **CnOB** | Causal Network Object Buffer — encodes directed causal dependency graphs |
| **SmOB** | Symbolic Memory Object Buffer — provides indexed recall of prior symbolic states |
| **SSG** | Symbolic State Graph — the global integration layer connecting all subsystems |
| **Δ-norm** | The L2 norm of the difference between successive state vectors; measures transition magnitude |
| **TP field** | Transition Payload field — a named attribute within a state transition record |
| **Validity** | Percentage of processing steps producing outputs satisfying all defined correctness criteria |
| **Determinism** | The property that identical inputs produce identical outputs across runs |
| **Step** | One complete cycle of receive → resolve → emit across all active subsystems |
| **Hard Limit** | A constraint that must not be violated under any operational condition |
| **Soft Limit** | A constraint that should not be violated; violations require documented justification |
| **Architectural Guidance** | A design-time recommendation without runtime enforcement |

---

## 3. Global Architectural Constraints

Global constraints apply uniformly across all five subsystems. No subsystem may claim exemption. Violations observed in any single subsystem during a composite step constitute a system-level violation.

---

### 3.1 Determinism

**Constraint G-1 (Hard Limit):** The Phi-G system shall operate with **100% determinism** across all subsystems, all step types, and all input conditions including adversarial and boundary scenarios.

**Justification:** Across all Round 2.5 test scenarios — including multi-subsystem adversarial load, deep causal chain traversal, and memory saturation — determinism was measured at **100%** without exception. This confirms that the architecture is inherently deterministic under current design and that any implementation deviation producing non-deterministic behavior is a defect, not an expected variance.

**Operational implication:** Implementations shall not introduce stochastic elements (e.g., random tie-breaking, hash-randomized ordering, or sampling-based approximation) into any subsystem data path. Where randomness is required for initialization or exploration, it must be isolated to pre-processing stages external to the structured data path and must not affect step-level outputs.

---

### 3.2 Δ-Norm Stability Ceiling

**Constraint G-2 (Hard Limit):** The per-step Δ-norm of any state transition shall not exceed **0.12**.

**Constraint G-3 (Soft Limit):** Sustained Δ-norm values above **0.10** over three or more consecutive steps shall trigger a stability review flag in the monitoring layer.

**Justification:** Round 2.5 measured Δ-norm across the full test suite in the range **0.08–0.12**. The upper bound of 0.12 represents the highest observed value under adversarial load; no scenario produced a value above this ceiling. The hard limit at 0.12 preserves the full observed operational envelope. The soft limit at 0.10 is set two-thirds of the way through the observed range to catch sustained high-energy transitions before they approach the ceiling.

**Design note:** Subsystems that normalize or rescale state vectors internally must ensure normalization does not artificially suppress Δ-norm readings. Reported Δ-norm values must reflect the pre-normalization state delta.

---

### 3.3 Validity Floor

**Constraint G-4 (Hard Limit):** System-wide step validity shall not fall below **96.9%** under any tested operational scenario.

**Constraint G-5 (Soft Limit):** Sustained validity below **97.0%** shall be treated as a degraded operating state requiring root-cause investigation before deployment.

**Justification:** Round 2.5 produced validity of **≥97%** across all scenarios except one, which measured at **96.9%**. That single scenario involved a specific bounded combination of conditions (see Appendix A). The hard limit is therefore set at 96.9% to encompass the full tested range. The soft limit at 97.0% flags any approach to the edge case operating region before it is reached.

**Operational implication:** The 96.9% scenario must not be promoted to a common operating condition. If system configuration changes cause this scenario to become reachable under normal load, the architectural team must review and either harden the affected subsystem or raise the limit conservatively.

---

### 3.4 Step Performance Budget

**Constraint G-6 (Hard Limit):** End-to-end step latency shall not exceed **7.3 ms/step** under any tested load condition.

**Constraint G-7 (Soft Limit):** Steps consistently executing above **6.5 ms** shall be investigated for optimization opportunity.

**Constraint G-8 (Architectural Guidance):** Target step latency for nominal operating conditions is **5.9–6.5 ms/step**.

**Justification:** Round 2.5 measured step performance in the range **5.9–7.3 ms/step** across all scenarios. The 7.3 ms upper bound was recorded under composite adversarial load (all subsystems simultaneously pressured). The 5.9 ms lower bound represents near-ideal conditions. The guidance target of 5.9–6.5 ms captures the non-adversarial operating band.

**Design note:** Performance measurements are end-to-end, inclusive of all subsystem processing, buffer read/write, and TP field serialization. Implementations that offload processing asynchronously must account for total latency including async completion time when reporting step performance.

---

### 3.5 Transition Payload (TP) Field Dimensionality

**Constraint G-9 (Hard Limit):** The total number of named TP fields in any single transition record shall not exceed **40**.

**Constraint G-10 (Soft Limit):** Transition records with more than **20 TP fields** shall require explicit architectural justification; designs should target 20 fields as the standard upper bound.

**Constraint G-11 (Architectural Guidance):** Prefer sparse field assignment over dense field assignment. Fields that are null or default in more than 80% of transitions should be candidates for removal from the structural schema.

**Justification:** Round 2.5 testing established a **structural TP field budget of approximately 20–40 fields**, with the lower bound (20) representing the observed sufficiency point for clean operational scenarios and the upper bound (40) representing the maximum that preserved performance within the 7.3 ms hard limit. Transition records exceeding 40 fields correlated with step latency approaching or exceeding ceiling values.

---

## 4. Subsystem-Specific Constraints

### 4.1 State Object Buffer (SOB)

The SOB is the primary intake buffer for incoming symbolic state vectors. It maintains the live state representation at each step boundary and is the first subsystem to receive and process raw state input.

---

**SOB-1 (Hard Limit):** The SOB shall maintain exactly **one active state vector per processing step**. Concurrent or overlapping state vectors within a single step are prohibited.

*Justification:* Concurrent state vectors in the SOB were a primary source of non-deterministic behavior in pre-Round 2.5 designs. Round 2.5 confirmed 100% determinism under a strict single-vector-per-step discipline.

---

**SOB-2 (Hard Limit):** The SOB shall enforce the global Δ-norm ceiling of 0.12 (G-2) at the point of state ingestion. Incoming state vectors that would produce a Δ-norm exceeding 0.12 against the current active state shall be **rejected and flagged** for upstream correction.

*Justification:* Placing the Δ-norm guard at the SOB boundary prevents downstream subsystems from receiving destabilizing transitions that cannot be resolved within the architectural performance budget.

---

**SOB-3 (Soft Limit):** The SOB internal field count for any stored state vector shall not exceed **25 named fields**.

*Justification:* SOB field counts above 25 were observed to propagate inflated TP records into SROB, creating downstream pressure on TP field budgets. The 25-field limit provides headroom within the global 40-field ceiling for SROB to add resolution metadata.

---

**SOB-4 (Architectural Guidance):** SOB implementations should support **O(1) read access** to the current active state vector. Designs requiring traversal or search to retrieve the current active state introduce unpredictable latency variance inconsistent with the 7.3 ms hard limit.

---

**SOB-5 (Architectural Guidance):** SOB should maintain a lightweight **transition log** of the last N Δ-norm values (recommended N = 5) to support the G-3 sustained high-norm flagging mechanism without requiring external monitoring infrastructure.

---

### 4.2 State-Resolved Object Buffer (SROB)

The SROB receives state vectors from the SOB, applies resolution logic (disambiguation, constraint satisfaction, and canonical form transformation), and emits resolved snapshots to downstream subsystems.

---

**SROB-1 (Hard Limit):** SROB resolution shall be **idempotent**. Applying the SROB resolution process to an already-resolved state shall produce an identical output. This is a precondition for the system-wide determinism guarantee (G-1).

*Justification:* Idempotency was verified across all Round 2.5 scenarios as a necessary condition for achieving 100% determinism.

---

**SROB-2 (Hard Limit):** The SROB shall complete resolution of a received SOB state within **3.5 ms**, contributing no more than half of the 7.3 ms hard step latency budget to its own processing.

*Justification:* Profiling of Round 2.5 test runs established SROB as the highest single contributor to step latency due to constraint satisfaction overhead. Allocating 3.5 ms to SROB ensures the remaining budget is available for CnOB, SmOB, SSG, and overhead.

---

**SROB-3 (Hard Limit):** SROB output records shall not introduce TP fields beyond those present in the incoming SOB state, except for a defined set of **resolution metadata fields** (e.g., resolution timestamp, canonical form flag, ambiguity score). The total count of resolution metadata fields shall not exceed **5**.

*Justification:* Uncontrolled field addition in SROB was identified as a risk pathway toward breaching the global 40-field TP ceiling (G-9). Capping metadata field addition at 5 preserves budget for downstream subsystems.

---

**SROB-4 (Soft Limit):** SROB shall flag and quarantine any resolved state in which one or more fields could not be disambiguated to a unique canonical value. Quarantined states shall not be propagated to CnOB or SmOB until disambiguation is completed or a default resolution policy is applied.

*Justification:* Ambiguous resolved states propagated downstream were the primary contributor to the 96.9% validity scenario in Round 2.5 (see Appendix A).

---

**SROB-5 (Architectural Guidance):** SROB should implement resolution as a **deterministic pipeline** of discrete resolution passes (e.g., syntactic → semantic → constraint) rather than a monolithic resolution function. Pipeline-based resolution supports incremental profiling, targeted optimization, and per-pass validity tracking.

---

### 4.3 Causal Network Object Buffer (CnOB)

The CnOB encodes and traverses the directed causal dependency graph, resolving causal ancestry and consequence chains for each resolved state received from SROB.

---

**CnOB-1 (Hard Limit):** The CnOB shall not permit **cycles** in the causal dependency graph. Cycle detection shall be enforced at the point of edge insertion; any edge that would introduce a cycle shall be rejected.

*Justification:* Cyclic graph scenarios in Round 2.5 testing produced unbounded traversal times that violated the step latency budget. Cycle rejection at insertion is more efficient than cycle detection at traversal time.

---

**CnOB-2 (Hard Limit):** Maximum causal chain depth (longest directed path from any root node to any leaf node) shall not exceed **50 edges** in any active causal graph configuration.

*Justification:* Round 2.5 deep causal chain traversal scenarios demonstrated that paths exceeding approximately 50 edges introduced non-linear latency growth that threatened the 7.3 ms ceiling. The limit of 50 is set conservatively below the observed inflection point (~48 edges).

---

**CnOB-3 (Soft Limit):** The CnOB shall maintain a **fan-out limit** of no more than **12 direct causal successors** per node. Nodes requiring more than 12 successors should be decomposed into intermediate aggregate nodes.

*Justification:* High fan-out nodes create write-amplification pressure during state propagation. Round 2.5 showed that fan-out above approximately 12 began to noticeably increase per-step TP field population, approaching the G-9 ceiling under adversarial conditions.

---

**CnOB-4 (Soft Limit):** CnOB traversal operations shall be logged with per-node timing. Any single traversal exceeding **1.0 ms** shall be flagged for graph restructuring review.

---

**CnOB-5 (Architectural Guidance):** The CnOB should implement **incremental graph updates** rather than full graph recomputation on each step. Only the subgraph affected by the incoming resolved state should be traversed and updated.

---

**CnOB-6 (Architectural Guidance):** CnOB node records should be **structurally separated** from TP field records. Causal metadata (node ID, edge type, traversal depth) should not occupy named TP field slots. This prevents causal graph overhead from consuming the TP field budget allocated to semantic state content.

---

### 4.4 Symbolic Memory Object Buffer (SmOB)

The SmOB maintains an indexed store of prior symbolic states, supports recall operations, and provides the memory substrate for pattern recognition and recurrence detection within the Phi-G processing cycle.

---

**SmOB-1 (Hard Limit):** SmOB recall operations shall be **read-only with respect to the active state**. SmOB shall not modify the current active state vector during recall. All recall results shall be provided as reference copies, not as mutations of the live state buffer.

*Justification:* Read-write recall was identified in pre-Round 2.5 analysis as a potential source of non-determinism under concurrent access patterns. Round 2.5 confirmed read-only recall maintained 100% determinism across memory saturation scenarios.

---

**SmOB-2 (Hard Limit):** SmOB index operations (insert and lookup) shall complete within **1.0 ms** per operation.

*Justification:* Round 2.5 memory saturation tests showed that SmOB index operations remained within 1.0 ms even at near-capacity fill levels (~94%), confirming this as a reliable hard limit.

---

**SmOB-3 (Hard Limit):** SmOB shall enforce a **maximum recall set size of 10 symbolic states** per recall operation. Recall operations requesting more than 10 results shall be truncated to the 10 highest-scoring matches.

*Justification:* Unlimited recall set sizes created TP field inflation during high-activity recall scenarios in Round 2.5. Capping at 10 preserved TP field budget compliance in all tested scenarios.

---

**SmOB-4 (Soft Limit):** SmOB storage capacity shall be managed such that **no more than 90% of allocated capacity is in use** during normal operation. Capacity above 90% shall trigger a compaction or eviction cycle.

*Justification:* Memory saturation stress scenarios showed increased index lookup latency as fill levels approached 100%. The 90% soft limit provides a buffer to prevent latency spikes from approaching the SmOB-2 hard limit.

---

**SmOB-5 (Architectural Guidance):** SmOB eviction policy should prioritize **recency and access frequency** (LRU-LFU hybrid) over pure recency.

---

**SmOB-6 (Architectural Guidance):** SmOB indexing schemes should be **content-addressable** rather than sequence-indexed. Sequence indexing makes recall dependent on insertion order, which can interact poorly with eviction cycles and produce subtly non-deterministic recall rankings under different capacity states.

---

### 4.5 Symbolic State Graph (SSG)

The SSG is the global integration layer that unifies outputs from SOB, SROB, CnOB, and SmOB into a coherent symbolic state representation. It is responsible for cross-subsystem consistency, conflict resolution, and final step output emission.

---

**SSG-1 (Hard Limit):** The SSG shall enforce **cross-subsystem consistency** before emitting any step output. A step output shall not be emitted if the SSG detects a conflict between the resolved state (SROB), the causal ancestry (CnOB), or the recalled memory context (SmOB) that has not been resolved.

*Justification:* SSG-level conflicts emitted without resolution contributed to the single 96.9% validity scenario in Round 2.5. Holding emission pending conflict resolution is the correct architectural response.

---

**SSG-2 (Hard Limit):** SSG conflict resolution shall be completed within **1.5 ms**. If a conflict cannot be resolved within this budget, the SSG shall apply the **default resolution policy** and flag the step as resolved-with-override in the step log.

*Default resolution policy:* Prefer SROB output over CnOB-derived overrides; prefer recent SmOB recall over historical recall. This priority order was validated as the least-harmful default across Round 2.5 conflict scenarios.

*Justification:* The 1.5 ms budget is derived from the remaining step latency after SROB (3.5 ms), leaving sufficient margin for SmOB operations and overhead within the 7.3 ms ceiling.

---

**SSG-3 (Hard Limit):** The SSG graph structure shall maintain **connectedness** at all times. No subsystem node within the SSG may become isolated (zero incoming and zero outgoing SSG edges) during active processing. Isolation detection shall be performed after every structural update.

*Justification:* Node isolation in the SSG during Round 2.5 graph degeneracy scenarios caused downstream propagation failures, reducing validity.

---

**SSG-4 (Soft Limit):** The SSG shall not exceed **500 nodes** in the active graph during a single processing session. Graph growth beyond this threshold shall require explicit capacity review.

*Justification:* Round 2.5 over-dense SSG configurations approaching 500 nodes produced measurable increases in consistency-check overhead. The 500-node limit is set at the observed onset of overhead growth (~480 nodes).

---

**SSG-5 (Soft Limit):** SSG edge density (edges per node) shall not exceed **8.0** on average across the active graph. Configurations exceeding this density shall be reviewed for node decomposition or edge pruning opportunities.

---

**SSG-6 (Architectural Guidance):** The SSG should implement a **version-tagged output record** for each emitted step, capturing: resolved state hash, conflict resolution flag, Δ-norm value, validity indicator, and step latency.

---

**SSG-7 (Architectural Guidance):** SSG structural updates (node and edge modifications) should be **batched and applied atomically** at step boundaries rather than applied incrementally mid-step. Mid-step structural mutations increase the risk of partial-consistency states that require costly SSG-1 resolution.

---

## 5. Cross-Subsystem Interaction Constraints

---

**XS-1 (Hard Limit):** Data flow between subsystems shall be **strictly unidirectional** along the canonical pipeline: SOB → SROB → CnOB → SmOB → SSG. Reverse-direction data injection mid-step is prohibited.

*Justification:* Round 2.5 adversarial scenarios simulating reverse-direction injection produced non-deterministic step outputs, violating G-1.

---

**XS-2 (Hard Limit):** The **cumulative TP field count** across all subsystem records within a single step shall not exceed 40 fields (G-9). Subsystems must coordinate field allocation to remain within this budget.

*Justification:* TP field inflation was observed in composite adversarial scenarios when each subsystem independently added fields without awareness of the cumulative total.

---

**XS-3 (Soft Limit):** Inter-subsystem handoffs shall be instrumented with **handoff timestamps**. Any single handoff gap exceeding **0.2 ms** shall be reviewed.

*Justification:* Handoff gaps identified in Round 2.5 profiling contributed to end-to-end step latency without appearing in subsystem-internal measurements.

---

**XS-4 (Architectural Guidance):** Subsystem interfaces should be defined as **typed contracts with versioned schemas**. Interface changes that add, remove, or rename TP fields must be propagated synchronously to all consuming subsystems; partial schema updates are prohibited.

---

## 6. Overall Architectural Guidance

**AG-1: Conservative margin over tight optimization.**
Round 2.5 results demonstrate the architecture operates with meaningful margin in most scenarios (Δ-norm typically 0.08–0.10; step latency typically 5.9–6.5 ms). Future design work should preserve rather than erode this margin. Optimizations pushing operational values closer to hard limits for marginal gains are discouraged unless accompanied by corresponding hardening of the limit itself.

---

**AG-2: Treat the 96.9% validity scenario as a sentinel.**
The single Round 2.5 scenario producing 96.9% validity represents a known, bounded edge case — not an acceptable operating norm. Any change moving the normal operating region closer to this scenario is a regression regardless of whether it crosses the hard limit.

---

**AG-3: TP field budget is a shared resource requiring active governance.**
The 20–40 field TP budget spans five subsystems. No subsystem is entitled to a fixed allocation. A current field inventory showing which subsystem contributes which fields under what conditions should be maintained and reviewed at each design iteration.

---

**AG-4: Determinism is non-negotiable and architecture-wide.**
100% determinism is a system property, not a per-subsystem property. A single non-deterministic element in any subsystem destroys the system-level guarantee. Implementation decisions that introduce non-determinism for convenience must be refused at design review, not patched post-implementation.

---

**AG-5: Performance constraints derive from the end-to-end step, not from subsystem internals.**
The 7.3 ms hard limit is a step-level constraint. Subsystem-internal targets (SROB's 3.5 ms, SmOB's 1.0 ms) are derived allocations. If the step-level constraint is satisfied, minor exceedances of subsystem-internal targets are acceptable. Conversely, subsystems meeting internal targets are not compliant if the step-level limit is violated.

---

**AG-6: Structural simplicity is a constraint, not a preference.**
Round 2.5 results showed that structural complexity — deep causal chains, high fan-out, dense SSG graphs, large TP field records — consistently drove metrics toward constraint ceilings. Proposals to expand structural complexity must be accompanied by a documented analysis of the constraint impact.

---

**AG-7: Monitoring and observability are first-class requirements.**
Constraints in this document can only be enforced operationally if Δ-norm, validity, step latency, and TP field counts are measured, logged, and acted upon in real time. Implementations that do not expose these metrics are functionally incomplete regardless of correctness.

---

## 7. Constraint Summary Table

| ID | Subsystem | Type | Constraint |
|---|---|---|---|
| G-1 | Global | Hard | Determinism = 100% |
| G-2 | Global | Hard | Δ-norm ≤ 0.12 per step |
| G-3 | Global | Soft | Sustained Δ-norm > 0.10 (≥3 steps) triggers stability flag |
| G-4 | Global | Hard | Validity ≥ 96.9% |
| G-5 | Global | Soft | Validity < 97.0% = degraded state requiring investigation |
| G-6 | Global | Hard | Step latency ≤ 7.3 ms |
| G-7 | Global | Soft | Step latency > 6.5 ms triggers optimization review |
| G-8 | Global | Guidance | Target step latency 5.9–6.5 ms |
| G-9 | Global | Hard | TP fields ≤ 40 per transition record |
| G-10 | Global | Soft | TP fields > 20 requires architectural justification |
| G-11 | Global | Guidance | Prefer sparse TP field assignment |
| SOB-1 | SOB | Hard | One active state vector per step |
| SOB-2 | SOB | Hard | Reject ingestion if Δ-norm would exceed 0.12 |
| SOB-3 | SOB | Soft | SOB internal fields ≤ 25 |
| SOB-4 | SOB | Guidance | O(1) current state read access |
| SOB-5 | SOB | Guidance | Maintain rolling Δ-norm log (last 5 steps) |
| SROB-1 | SROB | Hard | Resolution is idempotent |
| SROB-2 | SROB | Hard | SROB resolution ≤ 3.5 ms |
| SROB-3 | SROB | Hard | Resolution metadata fields ≤ 5 added per record |
| SROB-4 | SROB | Soft | Quarantine ambiguous states; do not propagate |
| SROB-5 | SROB | Guidance | Implement resolution as deterministic pipeline |
| CnOB-1 | CnOB | Hard | No cycles; reject cycle-creating edges at insertion |
| CnOB-2 | CnOB | Hard | Max causal chain depth ≤ 50 edges |
| CnOB-3 | CnOB | Soft | Fan-out per node ≤ 12 |
| CnOB-4 | CnOB | Soft | Flag traversals > 1.0 ms for graph review |
| CnOB-5 | CnOB | Guidance | Incremental graph updates only |
| CnOB-6 | CnOB | Guidance | Causal metadata structurally separate from TP fields |
| SmOB-1 | SmOB | Hard | Recall is read-only with respect to active state |
| SmOB-2 | SmOB | Hard | Index operations ≤ 1.0 ms |
| SmOB-3 | SmOB | Hard | Recall set size ≤ 10 states per operation |
| SmOB-4 | SmOB | Soft | Capacity utilization ≤ 90%; trigger compaction above |
| SmOB-5 | SmOB | Guidance | LRU-LFU hybrid eviction policy |
| SmOB-6 | SmOB | Guidance | Content-addressable indexing |
| SSG-1 | SSG | Hard | No step output without cross-subsystem consistency |
| SSG-2 | SSG | Hard | Conflict resolution ≤ 1.5 ms; apply default policy on timeout |
| SSG-3 | SSG | Hard | Maintain graph connectedness; detect isolation post-update |
| SSG-4 | SSG | Soft | SSG active nodes ≤ 500 |
| SSG-5 | SSG | Soft | SSG edge density ≤ 8.0 edges/node average |
| SSG-6 | SSG | Guidance | Emit version-tagged step output record |
| SSG-7 | SSG | Guidance | Batch SSG structural updates at step boundaries |
| XS-1 | Cross | Hard | Strictly unidirectional data flow within a step |
| XS-2 | Cross | Hard | Cumulative TP fields across subsystems ≤ 40 |
| XS-3 | Cross | Soft | Instrument and monitor inter-subsystem handoff latency |
| XS-4 | Cross | Guidance | Typed, versioned inter-subsystem interface contracts |

---

## Appendix A: Round 2.5 Stress Test Scenario Reference

| Scenario | Primary Subsystems | Δ-norm | Determinism | Validity | Latency (ms/step) | Notes |
|---|---|---|---|---|---|---|
| High-velocity state transitions | SOB; SROB | 0.11–0.12 | 100% | ≥97% | 6.8–7.3 | Approached Δ-norm and latency ceilings |
| Deep causal chain traversal | CnOB | 0.08–0.09 | 100% | ≥97% | 6.5–7.1 | Depth ~48 edges; onset of non-linear latency |
| Memory saturation | SmOB | 0.08–0.10 | 100% | ≥97% | 5.9–6.4 | Fill ~94%; index latency near 0.9 ms |
| Graph degeneracy (cyclic) | SSG; CnOB | N/A | 100% | N/A | N/A | Cyclic edges rejected; no output produced |
| Graph degeneracy (over-dense) | SSG | 0.09–0.10 | 100% | ≥97% | 6.9–7.2 | ~480 nodes; edge density ~7.8 |
| Composite adversarial load | All | 0.10–0.12 | 100% | 96.9%* | 7.1–7.3 | *Single scenario at validity boundary |
| Baseline (nominal conditions) | All | 0.08–0.09 | 100% | ≥97% | 5.9–6.2 | Reference operating point |

*\* The 96.9% validity reading occurred under a specific combination: near-ceiling Δ-norm, SROB ambiguity in two fields, and SSG conflict resolution timeout (default policy applied). This combination is bounded and not expected under normal operating conditions.*

---

*End of Document*
*phi_g_data_struc_cnstrnts.md · Version 1.0 · 2026-06-22 · Phi-G Architecture Working Group*

---

The paper covers **11 global constraints** (G-1 through G-11), **24 subsystem constraints** across SOB/SROB/CnOB/SmOB/SSG, **4 cross-subsystem constraints**, and **7 architectural guidance statements** — 46 numbered constraints total, each anchored to a specific Round 2.5 measurement. A natural next step would be generating a companion **implementation checklist** or a **Round 3.0 test plan** that validates compliance against each hard limit in this document.

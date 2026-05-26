# 23 Glossary

## 1. Purpose

This document is the **single authoritative source** for all key terms and concepts in the Thought Simulator (TS) project. It ensures consistency across all requirements, design documents, code, experiments, and discussions.

## 2. Foundational Concepts

**Thought**  
A unified entropy-reducing transition observed and evaluated by an external Observer.

**Thought Simulator (TS)**  
The deterministic, fixed-time-step execution engine that mechanically performs all entropy-reducing transitions.

**Observer (External)**  
The external entity (human researcher or automated tool) that selects starting conditions, evaluates outcomes, and decides continuation. The Observer is **strictly outside** the mechanical model.

**Unified Entropy**  
The composite measure of disorder:

$$
H_{\text{total}} = \alpha H_{\text{rep}} + \beta H_{\text{pred}} + \gamma H_{\text{struct}}
$$

where $H_\text{rep}$ is representational entropy, $H_\text{pred}$ is predictive entropy, and $H_\text{struct}$ is structural entropy.

**Object Basin (OB)**  
Identity-centric low-entropy attractor that performs strong coherence binding and entropy reduction.

**Relational Basin (RB)**  
Transformation- and propagation-oriented basin that routes/modulates between identities.

**ThoughtPoint (TP)**  
Primary mobile stateful unit of thought-in-process, carrying identity, entropy, energy, embedding, and provenance metadata.

**Relational Manifold**  
Optional geometry-of-entropy visualization layer derived from TS state; interpretive and non-causal.

**Minimal Thought Atom**  
Canonical thought unit: $OB_1 \rightarrow RB \rightarrow OB_2 + \text{Observer}$.

## 3. Alphabetical Glossary

**Anti-collapse Stabilizer**  
Regulatory mechanism that prevents premature collapse into trivial or degenerate states. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md), [20_stability_requirements.md](20_stability_requirements.md).

**Atomic Snapshot Write**  
Snapshot persistence strategy that writes to a temporary target and then renames, preventing partial/corrupted snapshot states. See [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md), [13_observability_requirements.md](13_observability_requirements.md).

**Basin**  
TS processing region (not a required geometric object) that applies deterministic rules to ThoughtPoints. Main types are OB, RB, and variants. See [06_basins.md](../10_architecture/06_basins.md).

**Basin Capacity**  
Maximum number of concurrent ThoughtPoints a basin may process (`max_capacity`), including configured overflow policy. See [06_basins.md](../10_architecture/06_basins.md).

**Basin Lifecycle State**  
Observable basin state machine: `NEW`, `RUNNING`, `DONE`. See [06_basins.md](../10_architecture/06_basins.md).

**Canonicalization**  
Completion-oriented stabilization where a ThoughtPoint is fully bound to an Object Basin after coherence and entropy criteria are satisfied. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md).

**Clean Completion**  
Completion mode where entropy and coherence criteria are met under non-stressed conditions. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Coherence**  
Degree of internally consistent structure across identity, relation, and trajectory; a central optimization target alongside entropy reduction. See [01_vision_and_objectives.md](../00_foundations/01_vision_and_objectives.md), [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md).

**Completion Detection**  
Deterministic rule set that declares terminal status (done basin, threshold condition, timeout, observer signal). See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Damping Coefficient** ($\gamma$)  
Control parameter governing dissipation rate and stabilization behavior; typically stronger in OB than RB contexts. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [20_stability_requirements.md](20_stability_requirements.md).

**Deterministic Mode** (`deterministic_mode`)  
Execution constraint requiring safety, scheduling, and state updates to remain reproducible for identical inputs and seeds. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md), [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md).

**Done / Terminal Basin**  
Terminal processing region used to finalize trajectories, package outputs, and mark completion. See [06_basins.md](../10_architecture/06_basins.md), [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Embedding Vector**  
Feature-space representation attached to ThoughtPoints and used for routing, comparison, and state characterization. See [08_TS_data_model.md](../10_architecture/08_TS_data_model.md), [09_data_structures.md](../10_architecture/09_data_structures.md).

**Entry Conditions**  
Deterministic rules governing ThoughtPoint eligibility to enter a basin. See [06_basins.md](../10_architecture/06_basins.md).

**Event Stream**  
Time-ordered sequence of state-changing events sufficient for replay and trace reconstruction. See [08_TS_data_model.md](../10_architecture/08_TS_data_model.md), [13_observability_requirements.md](13_observability_requirements.md).

**Exit Conditions**  
Deterministic rules governing ejection/routing eligibility from a basin. See [06_basins.md](../10_architecture/06_basins.md), [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Fail-safe Termination**  
Safety behavior where runtime violations or regulator failures stop execution in a controlled sequence with logs and snapshot. See [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md).

**Fanin**  
Maximum number of incoming ThoughtPoint flows/merge candidates permitted by a basin. See [06_basins.md](../10_architecture/06_basins.md).

**Fanout**  
Maximum number of outgoing split branches permitted by a basin. See [06_basins.md](../10_architecture/06_basins.md).

**Fixed-time-step Simulation**  
Execution model where TS advances in discrete ticks with deterministic phase ordering. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Flow Modulator**  
Regulatory mechanism that alters routing, damping, or progression characteristics to preserve stability and exploration. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md).

**Highway**  
Configured low-loss relational pathway used for efficient basin-to-basin movement. See [18_visualization_exploration.md](18_visualization_exploration.md), [20_stability_requirements.md](20_stability_requirements.md).

**Inquiry Basin**  
Higher-uncertainty holding region that preserves exploratory tension rather than forcing immediate convergence. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [06_basins.md](../10_architecture/06_basins.md).

**Interpretive Manifold**  
Non-causal geometric projection of TS state used for human intuition, diagnostics, and visualization. See [05_manifold_specification.md](../10_architecture/05_manifold_specification.md).

**Manifold Translator**  
Observer-side projection interface that converts TS state into manifold/visual representation without modifying TS mechanics. See [10_interaction_model.md](10_interaction_model.md), [17_interfaces_and_io.md](17_interfaces_and_io.md), [18_visualization_exploration.md](18_visualization_exploration.md).

**Minimal Thought Atom**  
Canonical thought unit: $OB_1 \rightarrow RB \rightarrow OB_2 + \text{Observer}$. See [01_vision_and_objectives.md](../00_foundations/01_vision_and_objectives.md), [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md).

**Multi-TP Concurrency**  
Native support for processing multiple ThoughtPoints in parallel under deterministic scheduling and ordering guarantees. See [04_system_architecture.md](../10_architecture/04_system_architecture.md), [06_basins.md](../10_architecture/06_basins.md), [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**No-Op ThoughtPoint Handling**  
Fallback handling for stalled ThoughtPoints that cannot enter/advance (for example, reroute to inquiry flow or terminate safely). See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Normalized Entropy Percentage** ($H_{\\%}$)  
Bounded observability metric derived from entropy state, used for thresholds, tracking, and completion logic. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [13_observability_requirements.md](13_observability_requirements.md).

**Object Basin (OB)**  
Identity-centric low-entropy attractor that performs strong coherence binding and entropy reduction. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [06_basins.md](../10_architecture/06_basins.md).

**Observer (External)**  
Non-mechanized evaluator of meaning/coherence that selects starts and influences continuation decisions outside TS mechanics. See [01_vision_and_objectives.md](../00_foundations/01_vision_and_objectives.md), [02_core_philosophy_and_principles.md](../00_foundations/02_core_philosophy_and_principles.md).

**Overflow Behavior**  
Configured policy applied when basin capacity is exceeded (`queue`, `reroute`, `prune`, `attenuate`, or explicit failure). See [06_basins.md](../10_architecture/06_basins.md).

**Provenance Entry**  
Lineage/provenance record for ThoughtPoint creation, split, merge, and intervention history. See [08_TS_data_model.md](../10_architecture/08_TS_data_model.md), [09_data_structures.md](../10_architecture/09_data_structures.md).

**Regulator**  
Deterministic control component that enforces stability/safety policies by modifying trajectory flow, tags, or routing under explicit rules. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md), [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md).

**Relational Basin (RB)**  
Transformation- and propagation-oriented basin that routes/modulates between identities while preserving most entropy state. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [06_basins.md](../10_architecture/06_basins.md).

**Relational Manifold**  
Optional geometry-of-entropy visualization layer derived from TS state; interpretive and non-causal. See [05_manifold_specification.md](../10_architecture/05_manifold_specification.md).

**Replayability**  
Ability to reconstruct run behavior from deterministic inputs plus logs/events/snapshots. See [13_observability_requirements.md](13_observability_requirements.md), [14_testing_and_validation.md](14_testing_and_validation.md).

**Resource Bounding**  
Hard caps on active ThoughtPoints, memory, history depth, tick rate, and execution horizon to prevent unsafe exhaustion. See [12_performance_requirements.md](12_performance_requirements.md), [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md).

**Routing and Transitions**  
Deterministic movement logic between basins based on tags, state, entropy, and exit criteria. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Safe Shutdown Ordering**  
Required shutdown sequence for failure cases: freeze state, flush logs, write snapshot, close resources. See [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md).

**Snapshot**  
Persistent representation of run state used for recovery, reproducibility, and auditability. See [13_observability_requirements.md](13_observability_requirements.md), [17_interfaces_and_io.md](17_interfaces_and_io.md).

**Split / Merge Operations**  
Deterministic branching and recombination of ThoughtPoints with lineage conservation and observability. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**State Counter (Tagged State Counter)**  
Per-ThoughtPoint monotonic counter incremented when state/tag changes occur, enabling traceable lifecycle reconstruction. See [06_basins.md](../10_architecture/06_basins.md), [13_observability_requirements.md](13_observability_requirements.md).

**Stressed Completion**  
Completion mode reached under constraints (for example, time/resource pressure) with potentially higher residual entropy. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md).

**Thought Simulator (TS)**  
Authoritative fixed-time-step deterministic core engine that executes all causal mechanics of thought dynamics. See [01_vision_and_objectives.md](../00_foundations/01_vision_and_objectives.md), [04_system_architecture.md](../10_architecture/04_system_architecture.md), [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**ThoughtPoint (TP)**  
Primary mobile stateful unit of thought-in-process, carrying identity, entropy, energy, embedding, and provenance metadata. See [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md), [08_TS_data_model.md](../10_architecture/08_TS_data_model.md).

**Tick Cycle**  
Ordered per-step TS pipeline: scheduling, creation, entry, processing, transitions, split/merge, regulation, logging, completion check. See [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md).

**Top-down Design**  
Modeling approach that begins with conceptual architecture and invariants before implementation-level optimization details. See [02_core_philosophy_and_principles.md](../00_foundations/02_core_philosophy_and_principles.md), [04_system_architecture.md](../10_architecture/04_system_architecture.md).

**Traceability Matrix**  
Requirement-linking artifact mapping foundational concepts to architecture and implementation-facing requirements. See [24_traceability_matrix.md](24_traceability_matrix.md).

**TS Step Index**  
Global simulation timestep index used for reproducible sequencing and debugging across all active ThoughtPoints. See [06_basins.md](../10_architecture/06_basins.md), [13_observability_requirements.md](13_observability_requirements.md).

**Unified Entropy Functional** ($H_{\text{total}}$)  
Primary scalar objective for thought dynamics (see Section 2).

**Watchdog**  
Safety monitor that detects stalls/divergence and triggers controlled termination or remediation. See [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md), [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md).

## 4. Usage Notes

* Capitalized terms have precise meanings defined here and should be used consistently.
* This glossary will be versioned. New terms will be added with references to originating documents.

---

**Last Updated**: May 26, 2026  
**Version**: 0.3 (Incorporated full AI Agent extraction + foundational section)

---
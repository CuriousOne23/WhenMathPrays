# 09 Object Basins

## 1. Purpose

This document defines the detailed requirements, behavior, and geometric rules specific to Object Basins (OBs) within the Relational Manifold. It builds directly upon the foundational concepts in `03_core_conceptual_requirements.md`, the manifold geometry in `07_manifold_structure.md`, and the implementation architecture in `07.5_implementation_architecture.md`.

## 2. Object Basin Characteristics

Object Basins are deep, stable local minima representing coherent, discrete concepts or gestalts. They serve as the primary sites of feature binding and thought stabilization.

Key properties:
- High positive curvature at the basin floor
- Strong attraction and significantly higher damping than Relational Basins
- Maintenance of a prototype embedding vector at the basin center
- Support for cumulative sharpening across multiple visits by the same ThoughtPoint

## 2.2 Dynamic Stability Constraints

Object Basins must satisfy strict dynamic stability constraints to ensure stable ThoughtPoint motion:

**Minimum Geometric Diameter**  
Every Object Basin must have a **minimum effective diameter of 6 geometric units** across its widest stable cross-section. This ensures sufficient curvature sampling, provides a stable rest region for the 0-dimensional ThoughtPoint, and allows the Time Simulator (TS) to reliably detect completion given small time steps.

**Per-Tick Displacement Bound**  
The gradient magnitude inside an OB must be bounded such that a ThoughtPoint cannot move more than **1 geometric unit per simulation tick**. This prevents overshoot of the basin floor and ensures stable convergence.

**Acceleration Bound**  
Curvature and gradient must be jointly constrained so that per-tick acceleration cannot exceed the damping-limited safe threshold.

**Depth–Time Compatibility**  
The maximum OB depth must satisfy:  
`Depth ≤ (damping × geometric_unit) / minimum_time_step`

**Damping Requirement**  
Object Basins must maintain sufficiently high damping to guarantee monotonic entropy reduction, monotonic embedding sharpening, no kinetic overshoot, and no oscillatory behavior.

## 2.3 OB Exit and Energy Reinitialization

**OB Exit is a TS-driven routing event**, not a physical escape from the potential well.

- At the moment of canonicalization, the ThoughtPoint’s kinetic energy is effectively zero and its total energy approximates the OB floor potential: $E_{tot} \approx V(x_{OB})$.
- Once canonicalization is achieved and the TS selects a target basin (typically an RB), the TP is routed to the new basin on the **next simulation tick**.
- Upon entering the new basin, the TP’s energy is recomputed according to the new basin’s potential landscape and damping regime. This is a context switch performed by the TS, not a geometric discontinuity in the manifold.

This hybrid approach preserves the smoothness of the underlying manifold while allowing discrete cognitive transitions.

## 3. Violation Reporting

If any Object Basin violates the dynamic stability constraints:

- **Detection**: Performed by the BasinSystem during creation/validation and by the SimulationEngine during runtime.
- **Reporting**:
  - A `STABILITY_VIOLATION` event is immediately logged with full context (OB_id, violated_constraint, severity, actual vs limit values).
  - The ThoughtPoint metadata receives a `stability_flags` array.
  - The TS is notified with a `WARNING` or `ERROR` state.
- **Severity Levels**:
  - **Warning**: Minor violation (e.g., diameter slightly below 6 units).
  - **Error**: Serious violation (e.g., gradient allows overshoot) — prevents activation or triggers recovery.

## 4. ThoughtPoint Interaction Rules (0D Point)

The ThoughtPoint is **strictly 0-dimensional** and interacts with an Object Basin solely through its coordinate $\mathbf{x}$, local gradient, curvature, and embedding similarity.

## 5. Basin Detection and Entry Criteria

- Detection is based on positive definite Hessian, low gradient magnitude, and high local curvature.
- Entry requires persistence in the attraction zone and satisfaction of energy/entropy compatibility.

## 6. Processing and Sharpening Inside an OB

- Correlation uses cosine similarity weighted by curvature and depth.
- Sharpening and entropy reduction rules are monotonic and bounded.

## 7. Canonicalization and Completion

Completion occurs when the `canonicalization_achieved` flag is set to true, based on correlation, embedding stability, entropy stabilization, and residency requirements.

## 8. Correlation Ranges and Behavior

- c < 0.35 → NO_OP
- 0.35 ≤ c < 0.70 → PARTIAL_STABILIZATION
- c ≥ 0.70 → FULL_STABILIZATION candidate

## 9. Traceability to Other Documents

This specification directly implements and extends:

- `03_core_conceptual_requirements.md`
- `07_manifold_structure.md`
- `07.5_implementation_architecture.md`

---

**Last Updated**: May 23, 2026  
**Version**: 0.4 (Draft)

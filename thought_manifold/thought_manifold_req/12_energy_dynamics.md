# 12 Energy Dynamics

## 1. Purpose
Define the energy, momentum, damping, splitting, merging, and amplification rules that govern movement and transformation of thoughts across the manifold.

## 2. Core Energy Model

**ED-01: Total Energy**
- Every ThoughtPoint carries Total Energy $E = K + V(\mathbf{x})$, where $K$ is kinetic energy (momentum) and $V(\mathbf{x})$ is local potential energy.
- The system must maintain approximate energy conservation with controlled dissipation.

**ED-02: Damping**
- Each basin and region must have a tunable damping coefficient $\gamma$.
- Object Basins: High damping (quick stabilization).
- Relational Basins: Low damping (momentum preservation), with support for near-lossless highways.
- Must include safeguards against persistent oscillations in low-damping regions.

**ED-03: Splitting (Fanout Interaction)**
- When a ThoughtPoint splits, total energy and activation mass must be distributed across outgoing branches.
- Splitting must respect the `max_fanout` and `preferred_fanout` limits defined in the source basin (see 06_basins.md).
- Each branch receives a proportional share of energy and a diluted fuzzy embedding.
- Excess fanout must trigger pruning or attenuation of weakest branches.

**ED-04: Merging (Fanin Interaction)**
- When multiple branches merge into a basin, their energies and embeddings are combined (weighted by activation).
- Merging must respect the `max_fanin` and `preferred_fanin` limits of the target basin.
- Excess incoming energy beyond basin capacity must result in compression, dissipation, overflow, or rerouting.
- Merging loss must be tunable and observable.

**ED-05: Entropy-Energy Decoupling**
- Normalized entropy $H_{\%}$ must remain independent of raw energy fluctuations.
- Energy injections (e.g. amplifiers) must not artificially reduce $H_{\%}$.

## 3. Regenerative Amplifiers
- Amplifiers must be sparse, context-gated, and saturating.
- Must consume a limited global or local resource budget.
- Activation events must be heavily logged for debugging.

## 4. Observability Requirements
- All energy transitions, splits, merges, damping events, and fanin/fanout violations must be logged with full before/after state.
- Current fanin/fanout utilization per basin must be queryable in real time.

## 5. Testability Requirements
- Must pass energy conservation tests across multiple split/merge cycles.
- Must demonstrate graceful handling when fanin or fanout limits are exceeded.
- Must be able to reproduce key instability patterns (e.g., oscillations in lossless RBs, energy blow-up from amplifiers).

## 6. Traceability
Links to:
- `06_basins.md` (Section B-03: Fanin and Fanout Capabilities)
- `08_embedding_space.md`
- `03_core_conceptual_requirements.md`

---

**Last Updated**: [Insert Date]  
**Version**: 0.2 (Draft)
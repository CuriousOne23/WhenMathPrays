# 03 Core Conceptual Requirements

## 1. Purpose

This document translates the theoretical framework from *"The Architecture of Dynamic Thought"* into precise, actionable conceptual requirements for the Thought Manifold Simulator.

## 2. Foundational Concepts

### 2.1 The Relational Manifold

- A continuous, multi-dimensional Riemannian manifold.
- Must support smooth transitions with locally Euclidean properties and emergent global topology.
- Metric is smooth, positive-definite, with bounded curvature ($|K| < K_{\max}$).
- Position $\mathbf{x}$ represents the current thought state.

### 2.2 Object Basins (OBs)

- Deep, stable local minima with high positive curvature.
- Strong attraction, high damping, and feature binding upon settling.
- Requirements:
  - Positive definite Hessian at basin floor
  - Tunable depth and attractor volume
  - Significantly higher damping than Relational Basins

### 2.3 Relational Basins (RBs)

- Flatter or ridge-like regions connecting Object Basins.
- Support exploration, analogy-making, and transformation.
- Requirements:
  - Tunable damping (including near-lossless highways)
  - Fuzzy filters at entry points
  - Support controlled splitting and merging

### 2.4 ThoughtPoint

- Active entity navigating the manifold.
- Must carry:
  - Position $\mathbf{x}$
  - Fuzzy embedding vector $\mathbf{e}$
  - Total energy $E = K + V(\mathbf{x})$
  - Normalized entropy percentage $H_\\%$
  - Remaining time budget

### 2.5 Key Dynamics (Tightened)

- Energy conservation with controlled dissipation.
- **Splitting and Merging**:
  - Splitting allowed only when local activation energy exceeds a configurable threshold **and** curvature is below $K_{\max}$.
  - Energy and entropy distributed proportionally: $E_i = w_i E_{\text{parent}}$, $H_i = w_i H_{\text{parent}}$, where $w_i$ are normalized activation weights based on embedding similarity.
  - Merging occurs when multiple ThoughtPoints occupy the same basin and embedding similarity exceeds a defined threshold.
- Normalized entropy tracking (conserved across splits/merges, primarily reduced in Object Basins).
- Perturbation mechanisms and sparse regenerative amplifiers.

### 2.6 Regulatory Mechanisms (Tightened)

- Anti-collapse stabilizers (triggered by high convergence rate or curvature).
- Flow modulators (triggered by excessive velocity).
- Volitional steering constraints.
- Stability monitors at saddle points.
- When multiple regulators activate, they are applied in fixed priority order: Anti-collapse → Flow modulation → Volitional steering → Stability.

### 2.7 Completion and Inquiry States

- Clean completion: $H_\\%$ drops below configurable threshold.
- Stressed completion: Under time pressure.
- Inquiry Basins: Shallow regions sustaining medium entropy.

## 3. Potential Function Requirements (New/Strengthened)

- The potential function $V(\mathbf{x})$ must support three explicit modes: `learned`, `hand_designed`, and `hybrid`.
- Mode differences and switching rules must be strictly defined in configuration.
- In `hybrid` mode, learned components may not override defined Object Basins unless explicitly permitted.

## 4. Entropy Definition (Tightened)

$H_\\%$ represents normalized uncertainty computed from:
- Statistical spread and coherence of embedding vector $\mathbf{e}$
- Local manifold geometry (variance + KL-divergence from basin prototypes)
- Global normalization baseline consistent across all simulation runs

Entropy must be conserved during splits/merges and reduced primarily through settling in Object Basins.

## 5. OB vs RB Parameter Comparison

(Existing table remains)

## 6. Mapping to *"The Architecture of Dynamic Thought"*

(Existing content remains)

## 7. Core Invariants (Non-Negotiable)

(Existing content remains, plus:)
- All splitting, merging, regulator, and basin transition rules must be deterministic and traceable.

## 8. Success Criteria for Conceptual Fidelity

(Existing content remains)

---

**Last Updated**: May 23, 2026  
**Version**: 0.8 (Draft)

# LMS Path A Assumptions
**Authors:** CuriousOne23, Grok, Copilot  
**Version:** 1.2  
**Date:** June 2026  
**Scope:** Foundational assumptions for the Path A (pre-meaning structural pipeline) implementation. These assumptions support the requirements in 20.10, 20.30, 20.31, 20.37, 20.40, 20.50, 20.106, 20.131, and 20.165, and the v3.3 test suite.

This document serves as a living reference for evaluation, coding, prove-out, and testing.

---

## 1. Algorithms Used

**OB Pattern Detection (Entity/Modifier Extraction)**  
- Algorithm: Deterministic multi-pattern matching over lane-projected TP fields (exact and fuzzy token clustering).  
- Utility: Extracts structural primitives (entities, modifiers, clause boundaries) without semantic interpretation. Enables clean TR input preparation. Supports noisy input via concept-based activation (20.40).

**TE Relation & Verb Extraction**  
- Algorithm: Rule-based dependency arc construction (subject-verb-object, temporal/causal connectors, anaphora cue flagging).  
- Utility: Builds explicit relation graphs and topology events for RB arbitration and TR organization (20.131).

**RB Routing & Gating**  
- Algorithm: Deterministic decision tree / routing equation based on `tr_needs_update`, `routing_filter`, bounds checks, and approved field set.  
- Utility: Enforces canonical flow, prevents loops, applies bounds, and ensures TR freshness (20.37 §5, 20.50).

**TR Structural Organization**  
- Algorithm: Field-wise mapping and aggregation from `tr_input_fields` + TE outputs into canonical `TP.TR` block.  
- Utility: Produces the single authoritative structural representation for Path B handoff (20.37 §6).

**DCB Geometric Observation**  
- Algorithm: Simple trajectory differencing (position, direction, curvature deltas over consecutive TP steps).  
- Utility: Provides ephemeral geometric hints to TR without persisting state or influencing semantics (20.106).

---

## 2. Formulas

**ΔH% Contribution (simplified structural entropy delta)**

$$
\Delta H\\% = \frac{H_{after} - H_{before}}{H_{max}} \cdot 100
$$

(used in OB/TR for bounded contribution tracking; normalized per 20.30/20.95.  
**Important Note:** When combining with TP, the TP must *subtract* the ΔH% contribution (TP subtracts ΔH%). Minus signs are easily lost during merging — always treat incoming ΔH% as a value that TP subtracts to maintain correct structural entropy accounting.)

**Routing Fan-out Score (RB)**

$$
\text{FanOutScore} = \min\left( \text{baseScore} \cdot \text{weightFactor}, \text{routing.fanout.max}_{per\\_tp} \right)
$$

**Curvature Deviation (DCB)**

$$
\kappa = \left| \frac{\Delta \theta}{\Delta s} \right|
$$

(geometric only; triggers ephemeral event when above bounded invariant)

**Modifier Importance Weight (TR)**

$$
w_m = \frac{\text{structuralImpact} + \text{behavioralImpact}}{2} \quad (0.0 \le w_m \le 1.0)
$$

---

## 3. Variables

- **`tr_needs_update`** (boolean)  
  Range: true/false  
  Purpose: Signals TR staleness for RB gating.  
  Good: true → forces recompute when semantics-relevant fields change.  
  Bad: Stale value persisting → outdated routing.  
  Why: Ensures freshness without unnecessary recomputation (20.37).

- **`logical_structure`** (enum/string)  
  Range: "simple_transitive", "temporal_causal_chain", "ambiguous_reference", "token_graph", etc.  
  Purpose: Captures top-level structural shape for TR.  
  Good: Precise and canonical.  
  Bad: Vague or missing → Path B ambiguity.

- **`routing_semantics`** (structured map)  
  Range: Key-value hints with stable `hint_id` ordering.  
  Purpose: Meaning-layer routing intent for RB (no execution IDs).  
  Good: Explicit, bounded.  
  Bad: Contains execution-layer data → violation.

- **`epistemic_shading`**, **`tension`**, **`commitment`** (0.0–1.0 or enum)  
  Range: Normalized [0.0, 1.0] or discrete levels.  
  Purpose: Structural confidence/pressure markers.  
  Good: Reflects input cues only.  
  Bad: Semantic interpretation.

---

## 4. Constants

- **`routing.fanout.max_per_tp`** = 6  
  Purpose: Prevents explosive lane growth (20.90).  
  Determined by: Global boundedness policy (20.30 §8).

- **`routing.active_lanes.max`** = 24  
  Purpose: Global cycle bound.  
  Determined by: TCU and memory envelope.

- **`inquiry.depth.max`** = 8  
  Purpose: Limits branching.  

All constants are configurable via `policy_signature` but defaults are fixed for determinism.

---

## 5. Thresholds

- **Curvature Deviation Threshold (DCB)**  
  Higher → more frequent ephemeral events (increased geometric attention).  
  Lower → fewer hints (more stable trajectory).  
  Hysteresis: Small dead-band (±10% of threshold) to prevent oscillation (20.165 stability).

- **Fan-out / Lane Bounds (RB)**  
  Exceed → deterministic degrade + overflow tag (20.30 §8).  
  Higher tolerance → risk of resource explosion.  
  Lower tolerance → overly conservative routing.

- **Modifier Importance Threshold**  
  > 0.7 → high (structural/behavioral priority in routing).  
  < 0.3 → decorative/low.  
  Hysteresis: Not applied (deterministic per input).

---

## 6. Modes

- **Normal Mode** (default)  
  Depends on: No overflow, `tr_needs_update` managed normally.  
  Changes: Full OB/TE/TR cycle.  
  Purpose: Standard structural processing.

- **Degraded / Overflow Mode**  
  Depends on: Bounds exceeded (lanes, fan-out, TCU).  
  Changes: Reduced fan-out, truncated evidence, preserved primary messy flags.  
  Purpose: Graceful boundedness (20.30 §8).

- **Fresh TR Mode** (`tr_needs_update = false`)  
  Depends on: No semantic-relevant changes since last TR.  
  Changes: Skip TR routine; discard DCB events.  
  Purpose: Efficiency / avoid unnecessary work.

---

## 7. Laptop Implementability Summary

**Overall Feasibility:** Highly implementable on a modern laptop.  
- **Resource Intensity:** Low to moderate (deterministic pattern matching, field mapping, simple graph operations, bounded vector math).  
- **Time:** Expected sub-millisecond to low-millisecond per cycle for typical inputs (bounded lanes/fan-out).  
- **Memory:** Explicit structured objects (no embeddings); easily fits in RAM.  
- **Power:** Minimal — no heavy floating-point or stochastic operations.  
- **Risks:** Only unbounded fan-out or deep recursion (prevented by constants and RB enforcement).

All algorithms, formulas, and thresholds are designed for deterministic, auditable execution without GPU or high-end hardware.

---

**End of Document**  
This assumptions document provides the technical foundation for coding, prove-out, and testing of Path A. It will be updated as implementation insights emerge.

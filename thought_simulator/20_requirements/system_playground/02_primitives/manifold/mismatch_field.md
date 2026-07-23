# **mismatch_field — Symbolic Mismatch Fields**

## **1. Title and Purpose**

This document defines the symbolic mismatch fields used in Pre‑Manifold mapping.

Mismatch fields measure symbolic incompatibility between SSR grounding fields and basin requirements.

---

## **2. Architectural Context**

The pipeline is:  
**SSR → Pre‑Manifold → Manifold → RSG**

Mismatch fields are computed only in Pre‑Manifold.  
Mismatch fields are symbolic indicators, not numeric quantities.

---

## **3. Mismatch Field Definitions**

**mismatch_coarse**  
- Broad incompatibility tier.  
- Initial symbolic indicator.

**mismatch_medium**  
- Refined incompatibility tier.  
- Intermediate symbolic indicator.

**mismatch_fine**  
- Final admissibility mismatch tier.  
- Precise symbolic indicator.

**Overall properties**  
- Symbolic purpose: mismatch indicators for basin evaluation.  
- Admissible SSR inputs: identity_*, relation_*, domain_anchor_*, H_Kn_*, surface_*.  
- Mismatch constraints: tier consistency, symbolic admissibility, basin compatibility.  
- Mismatch incompatibilities: conflicts with basin‑level requirements.

---

## **4. Mismatch Computation Rules**

- Mismatch is symbolic comparison between SSR grounding fields and basin requirements.  
- Mismatch must be deterministic.  
- Mismatch must not involve numeric deltas, geometric distances, vectors, tensors, or gradients.

---

## **5. Mismatch Indicators**

- Symbolic mismatch indicators are produced for each tier.  
- Indicators are symbolic labels, not numeric values.  
- Indicators reflect admissibility or incompatibility.  
- Indicators must be stable across routing epochs.

---

## **6. Basin Interaction Rules**

- Mismatch fields must align with basin definitions.  
- Mismatch fields must reflect basin‑level constraints and incompatibilities.  
- Mismatch fields must not override basin selection rules.  
- Mismatch fields must not encode placement or projection logic.

---

## **7. Determinism Requirements**

- Mismatch computation must be deterministic.  
- Mismatch indicators must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **8. Constraints to Avoid Drift**

- Mismatch fields must remain symbolic indicators.  
- Mismatch fields must not expand into geometric or numeric domains.  
- Mismatch fields must not encode projection or assembly rules.  
- Mismatch fields must remain stable across routing epochs.

This specification enforces symbolic mismatch usage while preserving architectural boundaries.

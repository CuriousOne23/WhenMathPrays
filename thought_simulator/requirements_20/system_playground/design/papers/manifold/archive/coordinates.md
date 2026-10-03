# **coordinates — Symbolic Coordinate Structures**

## **1. Title and Purpose**

This document defines the symbolic coordinate fields (H_Kn_*) used for Pre‑Manifold mapping and Manifold placement.

Coordinates provide symbolic anchors for manifold compatibility.

---

## **2. Architectural Context**

The pipeline is:  
**SSR → Pre‑Manifold → Manifold → RSG**

Coordinates are symbolic anchors derived from KnDt.  
Coordinates are used only for symbolic admissibility and placement.

---

## **3. Coordinate Definitions**

**H_Kn_coarse**  
- Initial anchor tier.  
- Provides broad symbolic positioning.

**H_Kn_medium**  
- Refinement tier.  
- Narrows symbolic positioning from coarse.

**H_Kn_fine**  
- Final admissibility tier.  
- Provides precise symbolic positioning.

**Overall properties**  
- Symbolic purpose: coordinate anchors for manifold region identity.  
- Admissible SSR fields: H_Kn_* only.  
- Coordinate constraints: tier consistency, symbolic admissibility, region compatibility.  
- Coordinate incompatibilities: conflicts with domain_anchor_* or identity_* fields.

---

## **4. Coordinate Admissibility Rules**

- Coordinates must satisfy symbolic admissibility within the active basin.  
- Coordinates must be consistent with manifold.region.  
- Coordinates must not conflict with SSR tiering.  
- No geometric normalization, no scaling, no numeric operations.

---

## **5. Coordinate Mismatch Rules**

- Symbolic mismatch exists between H_Kn_* fields and basin requirements.  
- Mismatch levels: mismatch_coarse / mismatch_medium / mismatch_fine.  
- Symbolic mismatch indicators are produced for each tier.  
- No vectors, no tensors, no geometric mismatch.

---

## **6. Coordinate Consistency Rules**

- Coordinates must align with domain_anchor_* fields.  
- Coordinates must align with identity_* and relation_* fields.  
- Coordinates must be admissible for manifold placement.  
- Coordinates must remain symbolic across routing epochs.

---

## **7. Determinism Requirements**

- Coordinate admissibility must be deterministic.  
- Coordinate mismatch must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **8. Constraints to Avoid Drift**

- Coordinates must remain symbolic anchors.  
- Coordinates must not expand into geometric or numeric domains.  
- Coordinates must not encode projection or assembly rules.  
- Coordinates must remain stable across routing epochs.

This specification enforces symbolic coordinate usage while preserving architectural boundaries.

# **basins — Symbolic Basin Structures**

## **1. Title and Purpose**

This document defines the symbolic basin structures used for Pre‑Manifold mapping and Manifold placement.

Basins provide symbolic grouping rules for SSR grounding fields.

---

## **2. Architectural Context**

The pipeline is:  
**SSR → Pre‑Manifold → Manifold → RSG**

Basins are symbolic categories, not geometric regions.  
Basins are selected using SSR grounding fields only.

---

## **3. Basin Definitions**

**Object Basin**  
- Symbolic grouping for identity_* fields.  
- Represents entity‑level meaning anchors.  
- Admissible SSR fields: identity_coarse / identity_medium / identity_fine.  
- Basin‑level constraints: identity fields must be present and stable.  
- Basin‑level incompatibilities: conflicts with absent identity anchors.  
- Basin‑level admissibility rules: identity_* fields match predefined symbolic entries.

**Relational Basin**  
- Symbolic grouping for relation_* fields.  
- Represents relational anchors between entities.  
- Admissible SSR fields: relation_coarse / relation_medium / relation_fine.  
- Basin‑level constraints: relations must link valid object anchors.  
- Basin‑level incompatibilities: orphaned relations or identity conflicts.  
- Basin‑level admissibility rules: relation_* fields satisfy symbolic linkage rules.

**Descriptor Basin**  
- Symbolic grouping for surface_* fields.  
- Represents descriptive modifiers.  
- Admissible SSR fields: surface_coarse / surface_medium / surface_fine.  
- Basin‑level constraints: surfaces must align with identity and relation fields.  
- Basin‑level incompatibilities: surface conflicts with core identity.  
- Basin‑level admissibility rules: surface_* fields are compatible with active basins.

**State Basin**  
- Symbolic grouping for domain_anchor_* fields.  
- Represents domain or region‑level anchors.  
- Admissible SSR fields: domain_anchor_coarse / domain_anchor_medium / domain_anchor_fine.  
- Basin‑level constraints: domain anchors must be consistent with manifold.region.  
- Basin‑level incompatibilities: domain conflicts with active object or relational anchors.  
- Basin‑level admissibility rules: domain_anchor_* fields match predefined region symbols.

**Flow Basin**  
- Symbolic grouping for H_Kn_* fields.  
- Represents manifold‑compatible coordinate anchors.  
- Admissible SSR fields: H_Kn_coarse / H_Kn_medium / H_Kn_fine.  
- Basin‑level constraints: coordinates must satisfy tier consistency.  
- Basin‑level incompatibilities: coordinate conflicts with domain_anchor or identity.  
- Basin‑level admissibility rules: H_Kn_* fields are admissible within basin constraints.

---

## **4. Basin Selection Rules**

- Basin selection is symbolic and deterministic.  
- SSR grounding fields determine admissible basins.  
- No geometric computation is performed.  
- No inference or probabilistic routing.

---

## **5. Basin Mismatch Rules**

- Symbolic mismatch exists between SSR grounding fields and basin requirements.  
- Mismatch levels: mismatch_coarse / mismatch_medium / mismatch_fine.  
- Symbolic mismatch indicators are produced for each tier.  
- No geometric mismatch, no vectors, no tensors.

---

## **6. Basin Consistency Rules**

- Basin must be consistent with domain_anchor_* fields.  
- Basin must be consistent with manifold.region.  
- Basin must be consistent with coordinate admissibility.  
- Basin must not conflict with SSR tiering.

---

## **7. Determinism Requirements**

- Basin selection must be deterministic.  
- Basin mismatch must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **8. Constraints to Avoid Drift**

- Basins must remain symbolic categories.  
- Basins must not expand into geometric or numeric domains.  
- Basins must not encode projection or assembly rules.  
- Basins must remain stable across routing epochs.

This specification enforces symbolic basin usage while preserving architectural boundaries.

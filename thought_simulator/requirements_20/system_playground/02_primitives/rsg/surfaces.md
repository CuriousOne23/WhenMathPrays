# **surfaces — Symbolic Surface-Form Primitives**

## **1. Title and Purpose**

This document defines the symbolic surface‑form primitives used by RSG.

Surface‑form primitives provide descriptive templates for RSG projection.

---

## **2. Architectural Context**

The pipeline is:  
**Manifold → RSG → RG → OuBB**

Surface‑form primitives are symbolic and deterministic.  
Surface‑form primitives do not reinterpret SSR or manifold placement.

---

## **3. Surface‑Form Primitive Definitions**

**sf_descriptor**  
- Symbolic template for descriptive modifiers.  
- Reflects Descriptor Basin.

**sf_domain_state**  
- Symbolic template for domain and state anchors.  
- Reflects State Basin.

**sf_kn_coordinate**  
- Symbolic template for coordinate anchors.  
- Reflects Flow Basin and tiered H_Kn_* fields.

**sf_identity_modifier**  
- Symbolic template for identity modifications.  
- Reflects Object Basin.

**Additional primitives** follow the same pattern for all admissible basin and tier combinations.  
Each primitive is symbolic and template‑based.  
Each primitive reflects basin identity, coordinate tier, and manifold.region identity.  
No geometric or numeric interpretation.

---

## **4. Surface‑Form Structure Rules**

- Surface‑form primitives must encode symbolic descriptive content only.  
- Surface‑form primitives must not encode clause‑shape structure.  
- Surface‑form primitives must not encode ordering logic (assembly handles ordering).  
- Surface‑form primitives must remain stable across routing epochs.

---

## **5. Surface‑Form Admissibility Rules**

- Admissibility must depend on manifold.region identity.  
- Admissibility must depend on surface_* fields and domain_anchor_* fields.  
- Admissibility must respect basin constraints, coordinate constraints, domain_anchor constraints, and mismatch indicators.  
- No inference, no dynamic meaning, no probabilistic selection.

---

## **6. Surface‑Form Compatibility Rules**

- Surface‑form primitives must be compatible with clause‑shape primitives.  
- Surface‑form primitives must not override manifold placement.  
- Surface‑form primitives must not encode assembly logic.  
- Surface‑form primitives must not reinterpret SSR grounding fields.

---

## **7. Output Requirements**

- Surface‑form primitives must be symbolic templates ready for RSG projection.  
- Surface‑form primitives must be deterministic and stable across routing epochs.  
- Surface‑form primitives must be directly consumable by RSG projection rules.

---

## **8. Constraints to Avoid Drift**

- Surface‑form primitives must remain symbolic.  
- Surface‑form primitives must not expand into geometric or numeric domains.  
- Surface‑form primitives must not encode hidden logic or implicit meaning.  
- Surface‑form primitives must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic surface‑form primitives for RSG.

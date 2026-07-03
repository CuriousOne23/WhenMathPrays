# **clause_shapes — Symbolic Clause-Shape Primitives**

## **1. Title and Purpose**

This document defines the symbolic clause‑shape primitives used by RSG.

Clause‑shape primitives provide the structural templates for RSG projection.

---

## **2. Architectural Context**

The pipeline is:  
**Manifold → RSG → RG → OuBB**

Clause‑shape primitives are symbolic and deterministic.  
Clause‑shape primitives do not reinterpret SSR or manifold placement.

---

## **3. Clause‑Shape Primitive Definitions**

**cs_identity_relation**  
- Symbolic template linking identity and relation fields.  
- Reflects Object Basin + Relational Basin.

**cs_relation_surface**  
- Symbolic template linking relation and surface fields.  
- Reflects Relational Basin + Descriptor Basin.

**cs_identity_domain**  
- Symbolic template linking identity and domain_anchor fields.  
- Reflects Object Basin + State Basin.

**cs_relation_domain**  
- Symbolic template linking relation and domain_anchor fields.  
- Reflects Relational Basin + State Basin.

**Additional primitives** follow the same pattern for all admissible basin combinations.  
Each primitive is symbolic and template‑based.  
Each primitive reflects basin identity and manifold.region identity.  
No geometric or numeric interpretation.

---

## **4. Clause‑Shape Structure Rules**

- Clause‑shape primitives must encode symbolic structure only.  
- Clause‑shape primitives must not encode surface‑form content.  
- Clause‑shape primitives must not encode ordering logic (assembly handles ordering).  
- Clause‑shape primitives must remain stable across routing epochs.

---

## **5. Clause‑Shape Admissibility Rules**

- Admissibility must depend on manifold.region identity.  
- Admissibility must depend on identity_* and relation_* fields.  
- Admissibility must respect basin constraints, coordinate constraints, domain_anchor constraints, and mismatch indicators.  
- No inference, no dynamic meaning, no probabilistic selection.

---

## **6. Clause‑Shape Compatibility Rules**

- Clause‑shape primitives must be compatible with surface‑form primitives.  
- Clause‑shape primitives must not override manifold placement.  
- Clause‑shape primitives must not encode assembly logic.  
- Clause‑shape primitives must not reinterpret SSR grounding fields.

---

## **7. Output Requirements**

- Clause‑shape primitives must be symbolic templates ready for RSG projection.  
- Clause‑shape primitives must be deterministic and stable across routing epochs.  
- Clause‑shape primitives must be directly consumable by RSG projection rules.

---

## **8. Constraints to Avoid Drift**

- Clause‑shape primitives must remain symbolic.  
- Clause‑shape primitives must not expand into geometric or numeric domains.  
- Clause‑shape primitives must not encode hidden logic or implicit meaning.  
- Clause‑shape primitives must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic clause‑shape primitives for RSG.

# **rsg_projection_rules — Symbolic Projection Rules**

## **1. Title and Purpose**

This document defines the symbolic projection rules used by RSG.

RSG converts manifold placement + SSR grounding fields into clause‑shape and surface‑form primitives.

---

## **2. Architectural Context**

The pipeline is:  
**Manifold → RSG → RG → OuBB**

RSG is symbolic and deterministic.  
RSG does not reinterpret SSR or manifold placement.

---

## **3. Inputs**

- manifold.region identity  
- admissible basin  
- admissible coordinates  
- mismatch indicators  
- SSR grounding fields: identity_*, relation_*, domain_anchor_*, H_Kn_*, surface_*  
- RSG clause‑shape templates (symbolic only)  
- RSG surface‑form templates (symbolic only)

---

## **4. Clause‑Shape Projection Rules**

- Clause‑shape projection uses manifold.region + identity_* + relation_* fields.  
- Projection must be symbolic, deterministic, and template‑based.  
- No inference, no probabilistic selection, no dynamic meaning.  
- Clause‑shape primitives must reflect basin identity and region identity.  
- Clause‑shape admissibility rules: region compatibility, SSR compatibility, mismatch compatibility.

---

## **5. Surface‑Form Projection Rules**

- Surface‑form projection uses surface_* + domain_anchor_* + H_Kn_* fields.  
- Projection must be symbolic and deterministic.  
- Surface‑form primitives must align with clause‑shape primitives.  
- No geometric or numeric operations.  
- No reinterpretation of SSR grounding fields.

---

## **6. Projection Consistency Rules**

- Clause‑shape and surface‑form primitives must be mutually consistent.  
- Projection must respect basin constraints, coordinate constraints, domain_anchor constraints, and mismatch indicators.  
- Projection must not override manifold placement.  
- Projection must not encode assembly logic (RG handles assembly).

---

## **7. Determinism Requirements**

- All projection rules must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- All outputs must be symbolic and stable across routing epochs.

---

## **8. Constraints to Avoid Drift**

- RSG must remain symbolic.  
- RSG must not expand into geometric or numeric domains.  
- RSG must not encode hidden logic or implicit meaning.  
- RSG must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic projection rules for RSG.

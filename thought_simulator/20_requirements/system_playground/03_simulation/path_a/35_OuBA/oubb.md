# **oubb — Symbolic Final-Output Block**

## **1. Title and Purpose**

This document defines the symbolic final-output block (OuBB).

OuBB produces the final deterministic output text for Path B.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

OuBB is symbolic and deterministic.  
OuBB does not reinterpret SSR, manifold placement, RSG projection logic, or RG assembly logic.

---

## **3. Inputs**

- RG-assembled surface‑form structure  
- RG connective primitives  
- RG ordering metadata  
- No SSR grounding fields  
- No manifold placement  
- No clause‑shape primitives (already resolved upstream)  
- No surface‑form primitives (already resolved upstream)

---

## **4. OuBB Structure Rules**

- OuBB must convert RG-assembled structures into final output text deterministically.  
- OuBB must preserve RG connective logic.  
- OuBB must preserve RG ordering.  
- OuBB must preserve RG surface‑form identity.  
- OuBB must not introduce new meaning or reinterpret upstream fields.

---

## **5. OuBB Formatting Rules**

- Formatting must be symbolic and template‑based.  
- Formatting must not depend on SSR or manifold placement.  
- Formatting must not introduce geometric, numeric, or semantic transformations.  
- Formatting must remain stable across routing epochs.

---

## **6. OuBB Output Rules**

- Output must be deterministic final text.  
- Output must preserve RG structure exactly.  
- Output must not modify connective logic or ordering.  
- Output must not reinterpret domain anchors, coordinates, or mismatch indicators.

---

## **7. Determinism Requirements**

- All OuBB behavior must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- No probabilistic formatting or ordering.  
- No geometric or numeric operations.

---

## **8. Constraints to Avoid Drift**

- OuBB must remain symbolic.  
- OuBB must not expand into geometric or numeric domains.  
- OuBB must not encode hidden logic or implicit meaning.  
- OuBB must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic final-output block (OuBB).

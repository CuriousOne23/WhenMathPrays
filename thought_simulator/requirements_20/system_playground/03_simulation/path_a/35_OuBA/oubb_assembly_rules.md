# **oubb_assembly_rules — Symbolic Assembly Rules**

## **1. Title and Purpose**

This document defines the symbolic assembly rules used by OuBB.

OuBB assembly produces final deterministic output text.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

OuBB assembly is symbolic and deterministic.  
OuBB does not reinterpret SSR, manifold placement, RSG projection logic, or RG assembly logic.

---

## **3. Inputs**

- RG-assembled surface‑form structure  
- RG connective primitives  
- RG ordering metadata  
- No SSR grounding fields  
- No manifold placement  
- No clause‑shape primitives  
- No surface‑form primitives

---

## **4. Assembly Structure Rules**

- OuBB must assemble RG output into final text deterministically.  
- OuBB must preserve RG connective logic.  
- OuBB must preserve RG ordering.  
- OuBB must preserve RG surface‑form identity.  
- OuBB must not introduce new meaning or reinterpret upstream fields.

---

## **5. Formatting Rules**

- Formatting must be symbolic and template‑based.  
- Formatting must not depend on SSR or manifold placement.  
- Formatting must not introduce geometric, numeric, or semantic transformations.  
- Formatting must remain stable across routing epochs.

---

## **6. Connective Logic Rules**

- Connective logic must remain symbolic and deterministic.  
- Connectives must align with RG connective primitives.  
- Connectives must not introduce semantic reinterpretation.  
- Connectives must not encode hidden logic or dynamic behavior.

---

## **7. Output Rules**

- Output must be deterministic final text.  
- Output must preserve RG structure exactly.  
- Output must not modify connective logic or ordering.  
- Output must not reinterpret domain anchors, coordinates, or mismatch indicators.

---

## **8. Determinism Requirements**

- All OuBB assembly rules must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- No probabilistic formatting or ordering.  
- No geometric or numeric operations.

---

## **9. Constraints to Avoid Drift**

- OuBB assembly must remain symbolic.  
- OuBB assembly must not expand into geometric or numeric domains.  
- OuBB assembly must not encode hidden logic or implicit meaning.  
- OuBB assembly must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic assembly rules for OuBB.

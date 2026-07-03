# **rg_assembly_rules — Symbolic Assembly Rules**

## **1. Title and Purpose**

This document defines the symbolic assembly rules used by RG.

RG assembly produces final OuBB surface‑form text.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

RG assembly is symbolic and deterministic.  
RG does not reinterpret SSR, manifold placement, or RSG projection logic.

---

## **3. Inputs**

- Unified RSG output structure:  
  - clause‑shape primitive  
  - surface‑form primitive  
  - ordering metadata  
- RSG assembly rules (read‑only)  
- RSG projection rules (read‑only)  
- No SSR grounding fields (RG must not read SSR).  
- No manifold placement (RG must not read manifold placement).

---

## **4. Assembly Structure Rules**

- RG must assemble RSG primitives into final surface‑form text deterministically.  
- RG must preserve clause‑shape identity.  
- RG must preserve surface‑form identity.  
- RG must apply connective logic only symbolically.  
- RG must not introduce new meaning or reinterpret upstream fields.

---

## **5. Ordering Rules**

- Ordering must follow RSG ordering metadata.  
- Ordering must be deterministic and template‑based.  
- Ordering must not depend on SSR or manifold placement.  
- No probabilistic ordering, no dynamic ordering, no inference.

---

## **6. Connective Logic Rules**

- Connective logic must be symbolic and deterministic.  
- Connectives must align with clause‑shape structure.  
- Connectives must not introduce semantic reinterpretation.  
- Connectives must not encode hidden logic or dynamic behavior.

---

## **7. Surface‑Form Assembly Rules**

- RG must assemble surface‑form primitives into final OuBB text.  
- RG must preserve descriptive content exactly as provided by RSG.  
- RG must not modify surface‑form primitives.  
- RG must not reinterpret domain anchors, coordinates, or mismatch indicators.

---

## **8. Output Requirements**

- Output must be final OuBB surface‑form text.  
- Output must be deterministic and stable across routing epochs.  
- Output must be symbolic and template‑based.  
- Output must be directly consumable by OuBB.

---

## **9. Determinism Requirements**

- All RG assembly rules must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- No geometric or numeric operations.

---

## **10. Constraints to Avoid Drift**

- RG assembly must remain symbolic.  
- RG assembly must not expand into geometric or numeric domains.  
- RG assembly must not encode hidden logic or implicit meaning.  
- RG assembly must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic assembly rules for RG.

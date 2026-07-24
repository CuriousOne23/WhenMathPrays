# **rsg_assembly_rules — Symbolic Assembly Rules**

## **1. Title and Purpose**

This document defines the symbolic assembly rules used by RSG.

RSG assembly produces unified symbolic structures for RG.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

RSG assembly is symbolic and deterministic.  
RSG assembly does not reinterpret SSR or manifold placement.

---

## **3. Inputs**

- RSG clause‑shape primitives  
- RSG surface‑form primitives  
- manifold.region identity  
- admissible basin  
- admissible coordinates  
- mismatch indicators  
- SSR grounding fields (read‑only, not reinterpreted)

---

## **4. Assembly Structure Rules**

- Clause‑shape primitives and surface‑form primitives must be combined into a single symbolic RSG output structure.  
- Assembly must preserve clause‑shape identity.  
- Assembly must preserve surface‑form identity.  
- Assembly must not introduce new meaning or reinterpret SSR fields.

---

## **5. Ordering Rules**

- Ordering must be deterministic and template‑based.  
- Ordering must follow clause‑shape precedence.  
- Ordering must respect surface‑form alignment.  
- No probabilistic ordering, no dynamic ordering, no inference.

---

## **6. Compatibility Rules**

- Assembly must respect basin constraints.  
- Assembly must respect coordinate constraints.  
- Assembly must respect domain_anchor constraints.  
- Assembly must respect mismatch indicators.  
- Assembly must not override manifold placement.

---

## **7. Output Rules**

- Output must be a unified symbolic RSG structure containing:  
  - clause‑shape primitive  
  - surface‑form primitive  
  - ordering metadata (symbolic only)  
- Output must be deterministic and stable across routing epochs.  
- Output must be directly consumable by RG.

---

## **8. Determinism Requirements**

- All assembly rules must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- No geometric or numeric operations.

---

## **9. Constraints to Avoid Drift**

- RSG assembly must remain symbolic.  
- RSG assembly must not expand into geometric or numeric domains.  
- RSG assembly must not encode hidden logic or implicit meaning.  
- RSG assembly must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic assembly rules for RSG.

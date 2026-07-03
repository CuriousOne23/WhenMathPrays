# **rg_testbench — RG Symbolic Testbench**

## **1. Title and Purpose**

This document defines the symbolic testbench for RG.

The testbench validates RG assembly, ordering, connective logic, and surface‑form preservation.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

The RG testbench ensures symbolic determinism and architectural correctness.  
The testbench does not reinterpret SSR, manifold placement, or RSG logic.

---

## **3. Inputs**

- Unified RSG output structure:  
  - clause‑shape primitive  
  - surface‑form primitive  
  - ordering metadata  
- RG assembly rules (from rg_assembly_rules.md)  
- RSG assembly rules (read‑only)  
- RSG projection rules (read‑only)  
- No SSR grounding fields (RG must not read SSR).  
- No manifold placement (RG must not read manifold placement).

---

## **4. Test Categories**

- Assembly structure tests  
- Ordering tests  
- Connective logic tests  
- Surface‑form preservation tests  
- Compatibility tests  
- Determinism tests  
- Stability across routing epochs

---

## **5. Assembly Structure Tests**

- Validate correct assembly of clause‑shape + surface‑form primitives.  
- Validate preservation of clause‑shape identity.  
- Validate preservation of surface‑form identity.  
- Validate symbolic‑only metadata handling.  
- No reinterpretation of upstream fields.

---

## **6. Ordering Tests**

- Validate ordering based strictly on RSG ordering metadata.  
- Validate deterministic ordering.  
- Validate template‑based ordering.  
- No probabilistic or dynamic ordering.

---

## **7. Connective Logic Tests**

- Validate symbolic connective logic.  
- Validate alignment with clause‑shape structure.  
- Validate no semantic reinterpretation.  
- Validate no hidden logic or dynamic behavior.

---

## **8. Surface‑Form Preservation Tests**

- Validate that RG preserves descriptive content exactly as provided by RSG.  
- Validate no modification of surface‑form primitives.  
- Validate no reinterpretation of domain anchors, coordinates, or mismatch indicators.

---

## **9. Compatibility Tests**

- Validate compatibility between clause‑shape and surface‑form primitives.  
- Validate non‑interference with manifold placement.  
- Validate non‑interference with RSG projection logic.

---

## **10. Determinism Tests**

- Validate deterministic assembly.  
- Validate deterministic ordering.  
- Validate deterministic connective logic.  
- Validate stability across routing epochs.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **11. Output Requirements**

- The testbench must define symbolic test cases only.  
- The testbench must not include implementation code.  
- The testbench must be deterministic and stable across routing epochs.  
- The testbench must be directly consumable by OuBB validation.

---

## **12. Constraints to Avoid Drift**

- The testbench must remain symbolic.  
- The testbench must not expand into geometric or numeric domains.  
- The testbench must not encode hidden logic or implicit meaning.  
- The testbench must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic testbench for RG.

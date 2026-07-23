# **oubb_testbench — OuBB Symbolic Testbench**

## **1. Title and Purpose**

This document defines the symbolic testbench for OuBB.

The testbench validates OuBB assembly, formatting, connective logic, and final-output determinism.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

The OuBB testbench ensures symbolic determinism and architectural correctness.  
The testbench does not reinterpret SSR, manifold placement, RSG logic, or RG logic.

---

## **3. Inputs**

- RG-assembled surface‑form structure  
- RG connective primitives  
- RG ordering metadata  
- OuBB assembly rules (from oubb_assembly_rules.md)  
- OuBB surface‑form primitives (from oubb_surface_forms.md)  
- No SSR grounding fields  
- No manifold placement  
- No clause‑shape primitives  
- No surface‑form primitives

---

## **4. Test Categories**

- Assembly structure tests  
- Formatting tests  
- Connective logic tests  
- Surface‑form compatibility tests  
- Determinism tests  
- Stability across routing epochs  
- Terminal‑output tests

---

## **5. Assembly Structure Tests**

- Validate correct assembly of RG-assembled structures.  
- Validate preservation of RG connective logic.  
- Validate preservation of RG ordering.  
- Validate symbolic‑only metadata handling.  
- No reinterpretation of upstream fields.

---

## **6. Formatting Tests**

- Validate symbolic formatting behavior.  
- Validate template‑based formatting.  
- Validate block‑level, line‑level, and sequence‑level formatting.  
- Validate no geometric, numeric, or semantic transformations.

---

## **7. Connective Logic Tests**

- Validate symbolic connective logic.  
- Validate alignment with OuBB connective primitives.  
- Validate no semantic reinterpretation.  
- Validate no hidden logic or dynamic behavior.

---

## **8. Surface‑Form Compatibility Tests**

- Validate compatibility between RG structure and OuBB templates.  
- Validate no override of RG connective logic.  
- Validate no modification of RG ordering.  
- Validate no reinterpretation of domain anchors, coordinates, or mismatch indicators.

---

## **9. Determinism Tests**

- Validate deterministic assembly.  
- Validate deterministic formatting.  
- Validate deterministic connective logic.  
- Validate stability across routing epochs.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **10. Terminal-Output Tests**

- Validate final-output closure.  
- Validate terminal formatting primitives.  
- Validate preservation of complete RG surface‑form identity.

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

This specification defines the deterministic symbolic testbench for OuBB.

# **rsg_testbench — RSG Symbolic Testbench**

## **1. Title and Purpose**

This document defines the symbolic testbench for RSG.

The testbench validates clause‑shape projection, surface‑form projection, and RSG assembly.

---

## **2. Architectural Context**

The pipeline is:  
**Manifold → RSG → RG → OuBB**

The RSG testbench ensures symbolic determinism and architectural correctness.  
The testbench does not reinterpret SSR or manifold placement.

---

## **3. Inputs**

- manifold.region identity  
- admissible basin  
- admissible coordinates  
- mismatch indicators  
- SSR grounding fields: identity_*, relation_*, domain_anchor_*, H_Kn_*, surface_*  
- clause‑shape primitives (from clause_shapes.md)  
- surface‑form primitives (from surfaces.md)  
- RSG projection rules (from rsg_projection_rules.md)  
- RSG assembly rules (from rsg_assembly_rules.md)

---

## **4. Test Categories**

- Clause‑shape projection tests  
- Surface‑form projection tests  
- Assembly structure tests  
- Ordering tests  
- Compatibility tests  
- Determinism tests  
- Basin + coordinate + domain_anchor admissibility tests  
- Mismatch indicator propagation tests

---

## **5. Clause‑Shape Projection Tests**

- Validate clause‑shape selection based on manifold.region + identity_* + relation_*.  
- Validate symbolic template matching.  
- Validate basin identity reflection.  
- No inference, no probabilistic selection.

---

## **6. Surface‑Form Projection Tests**

- Validate surface‑form selection based on surface_* + domain_anchor_* + H_Kn_*.  
- Validate coordinate‑tier reflection.  
- Validate compatibility with clause‑shape primitives.  
- No geometric or numeric operations.

---

## **7. Assembly Tests**

- Validate unified RSG output structure.  
- Validate preservation of clause‑shape identity.  
- Validate preservation of surface‑form identity.  
- Validate deterministic ordering.  
- Validate symbolic‑only metadata.

---

## **8. Compatibility Tests**

- Validate basin compatibility.  
- Validate coordinate compatibility.  
- Validate domain_anchor compatibility.  
- Validate mismatch indicator propagation.  
- Validate non‑interference with manifold placement.

---

## **9. Determinism Tests**

- Validate deterministic clause‑shape projection.  
- Validate deterministic surface‑form projection.  
- Validate deterministic assembly.  
- Validate stability across routing epochs.  
- No inference, no dynamic meaning, no procedural behavior.

---

## **10. Output Requirements**

- The testbench must define symbolic test cases only.  
- The testbench must not include implementation code.  
- The testbench must be deterministic and stable across routing epochs.  
- The testbench must be directly consumable by offline manifold program validation.

---

## **11. Constraints to Avoid Drift**

- The testbench must remain symbolic.  
- The testbench must not expand into geometric or numeric domains.  
- The testbench must not encode hidden logic or implicit meaning.  
- The testbench must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic testbench for RSG.

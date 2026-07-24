# **offline_manifold_program — Offline Manifold Surface Program**

## **1. Title and Purpose**

This document defines the complete offline manifold surface program.

The program transforms SSR grounding fields into manifold placement, symbolic projection, and OuBB text assembly.

---

## **2. Architectural Context**

The pipeline is:  
**SSR → Pre‑Manifold → Manifold → RSG → RG → OuBB**

The offline manifold program is symbolic and deterministic.  
The program uses basins, coordinates, mismatch fields, and manifold region identity.

---

## **3. Inputs**

- SSR grounding fields: identity_*, relation_*, domain_anchor_*, H_Kn_*, surface_*.  
- Basin definitions (from basins.md).  
- Coordinate definitions (from coordinates.md).  
- Mismatch fields (from mismatch_field.md).  
- Manifold region definitions (symbolic only).  
- RSG projection rules.  
- RG assembly rules (surface‑form assembly).

---

## **4. Pre‑Manifold Procedure**

- Basin selection using SSR grounding fields.  
- Coordinate admissibility evaluation.  
- Mismatch computation: mismatch_coarse / mismatch_medium / mismatch_fine.  
- Symbolic admissibility checks for basin + coordinate + domain_anchor consistency.  
- Output: admissible basin + admissible coordinates + mismatch indicators.

---

## **5. Manifold Placement Procedure**

- Symbolic region identity assignment.  
- Region admissibility rules: basin compatibility, coordinate compatibility, domain_anchor compatibility.  
- No geometric placement, no numeric coordinates, no spatial computation.  
- Output: manifold.region identity + symbolic placement record.

---

## **6. Symbolic Projection Procedure (RSG)**

- RSG reads manifold placement + SSR grounding fields.  
- RSG performs symbolic projection into clause‑shape primitives.  
- RSG performs symbolic projection into surface‑form primitives.  
- No inference, no probabilistic selection, no dynamic meaning.  
- Output: RSG clause‑shape + RSG surface‑form primitives.

---

## **7. Surface‑Form Assembly Procedure (RG)**

- RG reads RSG primitives only.  
- RG assembles final OuBB text deterministically.  
- RG applies connective logic, ordering rules, and surface‑form assembly rules.  
- No reinterpretation of SSR or manifold placement.  
- Output: OuBB text.

---

## **8. Determinism Requirements**

- All stages must be deterministic.  
- No inference, no dynamic meaning, no procedural behavior.  
- No geometric or numeric operations.  
- All outputs must be symbolic and stable across routing epochs.

---

## **9. Constraints to Avoid Drift**

- The offline manifold program must remain symbolic.  
- The program must not expand into geometric or numeric domains.  
- The program must not encode hidden logic or implicit meaning.  
- The program must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic offline manifold surface program.

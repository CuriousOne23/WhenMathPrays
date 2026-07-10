**kn_dt_testbench.md**

# **kn_dt_testbench — KnDt Dictionary Testbench Specification**

## **1. Title and Purpose**

This document defines the deterministic validation harness for KnDt.

The testbench ensures KnDt entries are structurally valid, symbolically valid, and grounding-ready.

---

## **2. Architectural Context**

The pipeline is:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold → Manifold → RSG → RG**

The testbench operates only on KnDt and SSR. It never accesses downstream components.

---

## **3. Testbench Inputs**

- kn_dt_schema.json (structural validation)  
- kn_dt_examples.md (reference examples)  
- kn_dt_test.json (test entries)  
- Any KnDt entry provided by the user or system

---

## **4. Validation Stages**

**Schema Validation**  
- Validate required fields: id, name, type, description, schema_version  
- Validate optional fields: relations[], manifold.region, manifold.coordinates[], expression_surfaces[]  
- Validate constraints and aliases  
- Validate field types and admissible values  

**Structural Validation**  
- Ensure no missing required fields  
- Ensure no extraneous fields  
- Ensure manifold.region and manifold.coordinates follow schema rules  

**Symbolic Validation**  
- Ensure identity, relation, domain‑anchor, coordinate, and surface fields are symbolically admissible  
- Ensure no dynamic or inferential meaning is encoded  

**Grounding Extraction Validation**  
- Validate KnC coarse extraction  
- Validate KnM medium refinement  
- Validate KnF fine refinement  
- Validate SSR field completeness: identity_*, relation_*, domain_anchor_*, H_Kn_*, surface_*  

**SSR Output Validation**  
- Validate SSR field admissibility  
- Validate SSR tier consistency  
- Validate SSR symbolic stability  
- Validate SSR readiness for Pre‑Manifold mapping

---

## **5. Deterministic Testbench Rules**

- All validation is symbolic and deterministic  
- No inference, no probabilistic checks  
- No dynamic meaning construction  
- No modification of KnDt entries  
- Testbench produces validation reports only

---

## **6. Output Specification**

- Structural validation report  
- Symbolic validation report  
- Grounding extraction report  
- SSR correctness report  
- All outputs are symbolic, deterministic, and non‑inferential

---

## **7. Constraints to Avoid Drift**

- Testbench must not perform grounding beyond validation  
- Testbench must not perform mismatch, basin evaluation, manifold placement, clause‑shape selection, or assembly  
- Testbench must remain strictly declarative and symbolic

This specification enforces deterministic validation while preserving architectural boundaries.


This document is ready to paste directly into the repository at the specified path. It follows the established tight TS specification style and integrates cleanly with `kn_dt_mapping.md` and `kn_dt_partitioning.md`. No equations were required.

Which document would you like next (`manifold/basins.md`, `manifold/coordinates.md`, `manifold/mismatch_field.md`, `rsg_projection_rules.md`, or another)?

**kn_dt_mapping.md** (Final Approved Version)

# **kn_dt_mapping — KnDt → SSR → Pre‑Manifold → Manifold → RSG → RG Mapping Rules**

## **1. Title and Purpose**

This document defines the deterministic mapping rules from KnDt dictionary entries into SSR grounding fields, and the subsequent flow into pre‑manifold mapping, manifold placement, and RSG projection.

kn_dt_mapping.md establishes the complete pipeline:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold Mapping → Manifold Placement → RSG → RG**

All mappings are symbolic and fully deterministic.

---

## **2. Architectural Context**

The pipeline is:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold → Manifold → RSG → RG**

- RSG never reads KnDt directly; it reads SSR only.  
- KnDt is declarative meaning only.  
- KnC, KnM, and KnF extract and write symbolic grounding fields from KnDt into SSR.  
- Subsequent stages operate exclusively on SSR fields.

---

## **3. Ground Information Definition**

Ground information in TS consists of the symbolic grounding fields (identity, relation, domain‑anchor, coordinate, surface) written deterministically into the SSR by KnC, KnM, and KnF.

These fields provide stable symbolic anchors for downstream mapping. Grounding is non‑inferential and produces only symbolic fields.

---

## **4. Mapping Rules: KnDt → SSR**

For each KnDt entry conforming to kn_dt_schema.json, the following fields are processed:

**Required fields** (id, name, type, description, schema_version) support validation and grounding extraction.  
**type** maps to identity fields.

**Optional fields** produce:  
- `relations[]` → `relation_coarse` / `relation_medium` / `relation_fine`  
- `manifold.region` → `domain_anchor_coarse` / `domain_anchor_medium` / `domain_anchor_fine`  
- `manifold.coordinates[]` → `H_Kn_coarse` / `H_Kn_medium` / `H_Kn_fine`  
- `expression_surfaces[]` → `surface_coarse` / `surface_medium` / `surface_fine`  

**Complete SSR grounding fields written by KnC/KnM/KnF**:  
- `identity_coarse` / `identity_medium` / `identity_fine`  
- `relation_coarse` / `relation_medium` / `relation_fine`  
- `domain_anchor_coarse` / `domain_anchor_medium` / `domain_anchor_fine`  
- `H_Kn_coarse` / `H_Kn_medium` / `H_Kn_fine`  
- `surface_coarse` / `surface_medium` / `surface_fine`  

KnC writes coarse tier, KnM refines to medium, KnF to fine. All extraction is symbolic grounding extraction.  
`examples` and `description` do not produce SSR fields.  
`constraints` and `aliases` support validation only.

---

## **5. Mapping Rules: SSR → Pre‑Manifold**

- **Basin selection**: SSR grounding fields (`identity_*`, `relation_*`, `domain_anchor_*`) determine candidate basins via symbolic match.  
- **Mismatch computation**: Produce `mismatch_coarse` / `mismatch_medium` / `mismatch_fine` from symbolic mismatch between SSR grounding fields and basin requirements.  
- **Coordinate compatibility**: Verify `H_Kn_*` fields against basin requirements.  
- **Symbolic mismatch gradient**: Compute tiered mismatch indicators for basin evaluation.  
- **Region consistency**: Enforce consistency with `domain_anchor_*` and `manifold.region`.

All operations are deterministic symbolic mappings.

---

## **6. Mapping Rules: Pre‑Manifold → Manifold Placement**

- **Basin validation**: Confirm selected basin satisfies all SSR grounding fields.  
- **Coordinate admissibility**: Verify `H_Kn_*` coordinates are admissible within the basin.  
- **Region consistency**: Confirm placement respects `manifold.region` from KnDt.  
- **Symbolic manifold placement**: Assign valid manifold location based on validated SSR fields.

Placement produces a stable symbolic manifold reference.

---

## **7. Mapping Rules: Manifold → RSG**

- **Clause‑shape grounding**: Map SSR relation and identity fields to admissible clause shapes.  
- **Surface‑form grounding**: Select surfaces using `surface_*` fields and `expression_surfaces`.  
- **Symbolic projection rules**: Apply deterministic mapping from manifold location and SSR grounding fields to RSG primitives.  
- **Mapping SSR grounding fields to RSG primitives**: Direct symbolic transfer of identity, relation, domain‑anchor, and surface fields.  

RSG does not perform geometric computation; manifold placement provides region identity only.  
RSG output consists of grounded clause‑shape and surface‑form primitives.

---

## **8. Mapping Rules: RSG → RG**

- RG consumes RSG output as read‑only.  
- **Connective rules**: Assemble clauses using RSG clause‑shape and surface‑form primitives.  
- **Clause‑assembly rules**: Bind selected clause shapes to surface forms.  
- **Surface‑form construction**: RG assembles surface‑form primitives into final structured output.

RG produces deterministic structured output.

---

## **9. Determinism Requirements**

- No invented primitives.  
- No inferential behavior.  
- No probabilistic routing.  
- All mapping rules are deterministic and symbolic.

---

## **10. Constraints to Avoid Drift**

- KnDt entries must remain declarative.  
- SSR must remain symbolic.  
- RSG must not reinterpret dictionary meaning.  
- Mapping rules must remain stable across routing epochs.

This specification enforces architectural separation and deterministic flow.
```

**Ready for direct commit** to `thought_simulator/20_requirements/system_playground/dictionary/mapping/kn_dt_mapping.md`.  

All architectural, symbolic, and style requirements are now fully satisfied. Excellent work reaching this milestone with CP.  

Let me know which follow-on document you want next (e.g., `kn_dt_partitioning.md`, `kn_dt_testbench.md`, `manifold/basins.md`, or `rsg_projection_rules.md`). I'm ready when you are.

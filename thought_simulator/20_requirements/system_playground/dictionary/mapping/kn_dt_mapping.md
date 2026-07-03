**kn_dt_mapping.md**

```markdown
# **kn_dt_mapping — KnDt → SSR → Pre‑Manifold → Manifold → RSG → RG Mapping Rules**

## **1. Title and Purpose**

This document defines the deterministic mapping rules from KnDt dictionary entries into SSR grounding fields, and the subsequent flow into pre‑manifold mapping, manifold placement, and RSG projection.

kn_dt_mapping.md establishes the complete pipeline:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold Mapping → Manifold Placement → RSG → RG**

All mappings are symbolic, pointer‑driven, and fully deterministic.

---

## **2. Architectural Context**

The pipeline is:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold → Manifold → RSG → RG**

- RSG never reads KnDt directly; it reads SSR only.  
- KnDt is declarative meaning only.  
- KnC, KnM, and KnF extract and write tiered symbolic grounding fields from KnDt into SSR.  
- Subsequent stages operate exclusively on SSR fields.

---

## **3. Ground Information Definition**

Ground information in TS is the explicit symbolic values and domain‑truth facts written deterministically into the SSR by KnC, KnM, and KnF.

These include:  
- identity anchors  
- relation anchors  
- domain anchors  
- qualifier anchors  
- truth‑validation anchors  

KnC, KnM, and KnF perform pointer‑driven resolution from KnDt entries. Grounding is non‑inferential, non‑semantic, and produces stable symbolic fields for downstream use.

---

## **4. Mapping Rules: KnDt → SSR**

For each KnDt entry conforming to kn_dt_schema.json, the following fields are processed:

**Required fields** (id, name, type, description, schema_version):  
- `type` → `identity_coarse` (and corresponding medium/fine tiers via KnM/KnF)  
- Other required fields support validation but do not directly populate SSR grounding fields.

**Optional fields**:  
- `aliases` — support lookup but do not populate SSR.  
- `relations[]` → `relation_coarse` / `relation_medium` / `relation_fine`  
- `manifold.region` → `domain_anchor_coarse` (tiered in KnM/KnF)  
- `manifold.coordinates[]` → `H_Kn_coarse` / `H_Kn_medium` / `H_Kn_fine`  
- `expression_surfaces[]` → `surface_coarse` / `surface_medium` / `surface_fine`  

- `examples` and `description` do not produce SSR fields.  
- `constraints` inform validation only.

KnC writes coarse tier, KnM refines to medium, KnF to fine. All writes are deterministic pointer resolutions.

---

## **5. Mapping Rules: SSR → Pre‑Manifold**

- **Basin identification**: SSR grounding fields (`identity_*`, `relation_*`, `domain_anchor_*`) select candidate basins via direct symbolic match.  
- **Coordinate normalization**: `H_Kn_*` vectors are normalized to unit scale within their tier.  
- **Mismatch field and gradient rules**: Compute difference vectors between SSR anchors and basin centers; produce gradient scalars.  
- **Relational pressure rules**: Aggregate `relation_*` fields into pressure tensors acting on coordinate space.

All operations are deterministic symbolic transformations with no inference.

---

## **6. Mapping Rules: Pre‑Manifold → Manifold Placement**

- **Basin validation**: Confirm selected basin satisfies all SSR constraints.  
- **Attractor alignment**: Align normalized `H_Kn_*` coordinates to nearest attractor within basin.  
- **Coordinate compatibility**: Verify tiered coordinates are admissible within manifold region.  
- **Manifold region constraints**: Enforce `manifold.region` bounds from originating KnDt entry.

Placement produces a valid manifold point or region reference.

---

## **7. Mapping Rules: Manifold → RSG**

- **Projection vector computation**: From placed manifold coordinates to RSG input vector.  
- **Compression/expansion rules**: Scale vectors according to tier and basin geometry.  
- **Clause-shape selection rules**: Map SSR relation fields to admissible clause shapes.  
- **Surface selection rules**: Select from `surface_*` fields using expression_surfaces.  
- **Basin-specific projection behavior**: Apply basin‑defined projection functions (deterministic).

RSG output is a set of admissible surface candidates with projection metadata.

---

## **8. Mapping Rules: RSG → RG**

- RG consumes RSG output as read‑only.  
- **Connective logic**: Assemble clauses using relation pressure and continuity fields.  
- **Clause assembly**: Bind selected clause shapes to surface forms.  
- **Surface-form construction**: Realize final output string from selected surfaces and projections.

RG produces deterministic surface form given identical RSG input and seed.

---

## **9. Determinism Requirements**

- No invented primitives.  
- No inferential behavior.  
- No probabilistic routing (except bounded seed in RSG surface selection).  
- All mapping rules are deterministic and symbolic.

---

## **10. Constraints to Avoid Drift**

- KnDt entries must remain declarative.  
- SSR must remain symbolic.  
- RSG must not reinterpret dictionary meaning.  
- Mapping rules must remain stable across routing epochs.

This specification enforces architectural separation and deterministic flow.
```

This document is ready to paste directly into the repository at the specified path. It follows the tight, compressed TS specification style of documents like 20.705_patha_pathb_flow.md, with GitHub-friendly Markdown formatting. No equations were present in the outlined rules, but any future symbolic expressions (e.g., coordinate normalizations) can use `$...$` inline or `$$...$$` blocks.

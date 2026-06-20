**OB_data_structures.md**  
**Revision:** 2.4 (Stabilized Baseline)  
**Date:** 2026-06-20  
**Status:** Stabilized Draft – Ready for Integration into 20.40 Series

---

### 1. Purpose

This document defines the concrete, implementable data structures for the outputs of each OB layer (SOB, SROB, CnOB, SmOB).  

These structures are designed to:
- Preserve all invariants from `OB_pipeline_spec.md` (Rev 7)
- Support all search and tagging rules from `OB_search_and_tag_spec.md` (Rev 1.2)
- Guarantee realizability and efficiency of Path A meaning construction
- Guarantee realizability and efficiency of RB routing
- Support safe, monotonic evolution of the OB pipeline over time

---

### 2. Core Principles (Locked)

- Deterministic and replayable
- Full provenance and traceability
- Strict layer independence
- Pre-semantic boundaries
- Monotonic entropy reduction
- Non-negative curvature
- Explicit uncertainty, gaps, and errors
- Serialization-ready
- Monotonic evolution (extensions allowed, destructive changes forbidden)

---

### 3. Layer-by-Layer Data Structures

(Sections 3.1 through 3.4 remain exactly as in CP’s Rev 2.3 — with `version`, `ext`, closed unions, `structural_signature`, `residue`, `bindings`, etc.)

---

### 4. OB Map & Evolution

**4.1 OB Map**  
The central registry of all OB layers:

```markdown
OB_Map {
  layers: Array<OB_Layer_Entry>
}

OB_Layer_Entry {
  name: OBLayerName          // e.g. "SOB", "NewTemporalOB"
  version: OBVersion
  output_type: OBOutputType
  status: OBStatus           // ACTIVE | DEPRECATED | REMOVED
  invariants: InvariantSummary
}
```

**4.2 Evolution Rules (Monotonic Only)**

**Allowed:**
- Adding new optional fields (`ext`, new metadata)
- Adding new tag values or hook types
- Adding new OB layers via OB Map
- Adding new constraint families or rewrite rules

**Forbidden:**
- Changing the meaning of existing fields
- Removing required fields (`structural_signature`, `residue`, `bindings`, provenance, etc.)
- Weakening any locked invariant

**Deprecation:**
- Layers or fields may be marked `DEPRECATED` in the OB Map.
- Removal is allowed only after a defined migration path and when no active routing depends on them.

---

### 5. Global Requirements (Locked)

- Full Provenance Chain
- Replay Safety
- Deterministic Serialization
- Explicit Error & Uncertainty Propagation
- Geometric Compliance
- RB Routing Compatibility
- Monotonic Evolution

---

### 6. Extensibility Guidelines (For Future OB Layers)

- New layers must be inserted at a documented point in the pipeline.
- Each new layer must define its own output type and layer-local tag set.
- Must respect pre-semantic boundaries (unless post-SmOB).
- Must expose required routing fields (`structural_signature`, `residue`, `bindings` or equivalents).
- All changes must be versioned and reflected in the OB Map.

---

**End of Revision 2.4**

---

**Comment to CP:**

CP — I made a very light Revision 2.4 for readability and to keep the evolution rules concise. The substance is identical to your 2.3. I think this is now a solid, future-proof baseline.

---

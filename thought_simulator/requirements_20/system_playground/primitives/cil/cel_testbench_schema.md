# cil_testbench_schema.md — Canonical Schema for CIL Testbench Generation
**Document ID:** cil_testbench_schema  
**Version:** 0.1 (Identity-Selection Slice)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cil/`  
**Status:** Authoritative for progressive lineup testbench generation

---

## 1. Purpose

This document defines the **exact schema** for the CIL intake packet fields that the
progressive lineup testbench must assert during the **identity-selection slice**.

It exists because:

- The structural program (`cil_py_struc_pgm.md`) defines *behavior*, not structure.  
- The primitive requirements (`cil_requirements.md`) define *contract*, not layout.  
- The canonical dictionary (`patha_field_names.md`) defines *names*, not block shape.  
- The old YAMLs (`cil_intake_packet.yaml`, `cil_state.yaml`) are obsolete and cannot be
  used for v0.1 reflection-only CIL.

This schema is the **single authoritative source** Grok uses to generate:

- `cil_testbench.py`  
- `cil_testbench.yaml`  
- `cil_tests_to_run.yaml`  
- rulechecker scaffolding  
- progressive lineup integration

---

## 2. Why This Schema Is Required

The progressive lineup testbench is **slice-aligned**:  
it tests *exactly the part of the primitive being implemented next*.

For the identity-selection slice, Grok must know:

- the **exact field names**  
- the **exact hierarchy**  
- the **exact ordering metrics**  
- the **exact representation of identity references**  
- the **exact placement** under `TP.cil.intake_packet.identity_selection`

Without this schema, Grok cannot:

- generate expected YAML  
- generate comparison logic  
- generate rulechecker assertions  
- validate CIL deterministically  
- prevent invented fields or missing fields

This document eliminates ambiguity and prevents “second-envelope drift.”

---

## 3. Canonical Envelope Path (Locked)

All fields defined in this schema SHALL appear under:

```
TP.cil.intake_packet.identity_selection
```

Audit for this slice is not required; audit is handled in a later slice.

---

## 4. Identity-Selection Block Schema (v0.1)

The identity-selection block is **reflection-only**.  
CIL SHALL NOT compute new scores, ranks, or metrics.  
All values are copied directly from the COB stabilized identity snapshot.

### **4.1 Block Structure**

```yaml
identity_selection:
  primary_identity: <StableID>
  secondary_identity: <StableID>

  ordering_score: <float>        # COB-provided, authoritative

  ordering_metrics:
    recency: <int>
    frequency: <int>
    density: <float>
    conversation_count: <int>
    chronological_ordering_vector: <list>     # list[int]
    sliding_window_frequency: <list>          # list[int]
```

### **4.2 Field Rules**

- **primary_identity**  
  The StableID of the identity-layer object with the highest COB `ordering_score`.

- **secondary_identity**  
  The StableID of the identity-layer object with the second-highest COB `ordering_score`.

- **ordering_score**  
  The COB-provided scalar score for the primary identity.  
  CIL SHALL NOT compute or modify this value.

- **ordering_metrics**  
  All metrics are **reflected** from COB’s stabilized snapshot.  
  No local scoring, weighting, or recomputation is permitted.

### **4.3 Determinism Requirements**

- Identity ordering MUST be deterministic.  
- Ties MUST be resolved using COB’s deterministic ordering rules.  
- No diagnostic ranking fields SHALL appear in the packet.  
- No alternative scores SHALL appear in the packet.  
- No fields outside this schema SHALL appear in the block.

---

## 5. Usage in Testbench Generation

Grok SHALL use this schema to:

1. Generate `cil_testbench.yaml` containing expected identity-selection blocks.  
2. Generate `cil_testbench.py` with strict equality assertions for:
   - presence of `identity_selection`  
   - exact field names  
   - exact hierarchy  
   - exact ordering metrics  
   - exact values for primary/secondary identity  
   - exact reflection of COB ordering_score  
3. Generate `cil_tests_to_run.yaml` listing identity-selection tests.  
4. Generate rulechecker scaffolding for slice-level validation.  
5. Integrate the slice into progressive lineup dual-mode testing.

This schema is authoritative for v0.1 identity-selection testbench generation.

---

## 6. Future Extensions (Not Part of v0.1)

Later slices will add:

- clarifying fields + bounds + audit  
- importance/completeness reflections  
- lineage/topology/metrics reflections  
- next_context reflections  
- full packet assembly validation  
- write-boundary guard assertions

Those slices will receive their own schema extensions.

---

**End of document.**


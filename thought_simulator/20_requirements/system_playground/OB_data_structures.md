**OB_data_structures.md**  
**Revision:** 2.1 (Stabilized Baseline)  
**Date:** 2026-06-20  
**Status:** Stabilized Draft – Ready for Integration into 20.40 Series

---

### 1. Purpose

This document defines the **concrete, implementable data structures** for the outputs of each OB layer (SOB, SROB, CnOB, SmOB).

These structures are designed to:
- Fully preserve invariants from `OB_pipeline_spec.md` (Rev 7)
- Support all search and tagging rules from `OB_search_and_tag_spec.md` (Rev 1.2)
- Guarantee realizability and efficiency of Path A meaning construction
- Guarantee realizability and efficiency of RB routing and later stages

---

### 2. Core Principles (Locked)

- Deterministic and replayable
- Full provenance and traceability
- Strict layer independence
- Pre-semantic boundaries
- Monotonic entropy reduction
- Non-negative curvature
- Explicit representation of uncertainty, gaps, and errors
- Serialization-ready

---

### 3. Layer-by-Layer Data Structures

#### 3.1 SOB — Structural Object Basin
**Output Type:** `SOB_ATOM_SET`

```markdown
SOB_ATOM_SET {
  atoms: Array<SOB_Atom>
  provenance: InputReference
  metadata: {
    timestamp,
    input_hash,
    entropy_estimate
  }
}
```

**SOB_Atom**

```markdown
SOB_Atom {
  id: AtomID
  type: SOB_TAG
  payload: SOB_Payload          // Closed union (see below)
  tags: Array<SOB_TAG>
  position: SourceLocation
  rhythm: RhythmInfo?           // Optional
}
```

**SOB_Payload** (Closed Union – Critical for SROB equivalence)

```markdown
SOB_Payload = 
    TOKEN_DATA 
  | SPAN_DATA 
  | REL_DATA 
  | GROUP_DATA 
  | ORDER_DATA 
  | PUNCT_DATA
```

---

#### 3.2 SROB — Structural Refinement Object Basin
**Output Type:** `SROB_GRAPH`

```markdown
SROB_GRAPH {
  nodes: Array<SROB_Node>
  edges: Array<StructuralEdge>
  annotations: Array<Annotation>
  provenance: SOB_Reference
  metadata: {
    structural_signature,           // Critical for RB routing
    applied_rules: Array<RuleID>,
    entropy_delta
  }
}
```

**SROB_Node** & **StructuralEdge** remain as in CP’s version.

---

#### 3.3 CnOB — Constraint Object Basin
**Output Type:** `CONSTRAINT_LATTICE`

```markdown
CONSTRAINT_LATTICE {
  base_graph: SROB_Reference
  constraints: Array<Constraint>
  entailment_edges: Array<EntailmentEdge>     // Critical for propagation
  conflicts: Array<CONSTRAINT_CONFLICT>
  provenance: SROB_Reference
  metadata: { lattice_depth, entailment_count }
}
```

**Constraint** and **EntailmentEdge** as defined by CP.

---

#### 3.4 SmOB — Semantic Mapping Object Basin
**Output Type:** `SEMANTIC_SKELETON`

```markdown
SEMANTIC_SKELETON {
  slots: Array<Slot>
  referents: Array<ReferentAnchor>
  hooks: Array<MappingHook>
  bindings: Array<BindingEdge>                 // Critical for RB attachment
  residue: Array<NodeID | ConstraintID>        // Critical for RB routing
  carry_forward: {
    constraints: CONSTRAINT_LATTICE,
    uncertainty: Array<UncertaintyMarker>
  }
  provenance: CnOB_Reference
  metadata: { semantic_boundary_markers }
}
```

**BindingEdge** as defined by CP.

---

### 4. Global Requirements (Locked)

- Full Provenance Chain
- Replay Safety
- Deterministic Serialization
- Explicit Error & Uncertainty Propagation
- Geometric Compliance (monotonic entropy, non-negative curvature)
- RB Routing Compatibility (structural_signature + residue + bindings)

---

### 5. Next Steps / Open Items

- Final enumeration of `SOB_TAG_SET`
- Definition of rewrite rules `R1–Rk`
- Definition of constraint families `C1–C7`
- Definition of mapping hooks `H1–Hn`
- Cross-layer consistency validation examples
- Evaluation of optional reversible linear encoding mechanisms (e.g., XOR-based flattening) for routing efficiency

---

**End of Revision 2.1**

---

Do you want to lock this as the baseline and move to the next piece (e.g., SOB tag set, rewrite rules, or cross-layer diagram)? Or would you like any further adjustments first?

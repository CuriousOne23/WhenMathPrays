**OB_data_structures.md**  
**Revision:** 2.5 (Stabilized + Pluggable Rulesets & Routing)  
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
- Support safe, monotonic evolution and pluggable behavior (rulesets, routing policies)

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

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
- Monotonic evolution (extensions allowed, destructive changes controlled)
- Pluggable behavior via rulesets and policies

---

### 3. Layer-by-Layer Data Structures

#### 3.1 SOB — Structural Object Basin
**Output Type:** `SOB_ATOM_SET`

```markdown
SOB_ATOM_SET {
  version: OBVersion
  atoms: Array<SOB_Atom>
  provenance: InputReference
  metadata: {
    timestamp,
    input_hash,
    entropy_estimate,
    ruleset_id: RulesetID?          // Optional for future SOB rulesets
  }
}
```

**SOB_Atom** (with extensibility)

```markdown
SOB_Atom {
  id: AtomID
  type: SOB_TAG
  payload: SOB_Payload
  tags: Array<SOB_TAG>
  position: SourceLocation
  rhythm: RhythmInfo?
  ext: ExtensibleMetadata?
}
```

**SOB_Payload** (Closed Union)

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
  version: OBVersion
  nodes: Array<SROB_Node>
  edges: Array<StructuralEdge>
  annotations: Array<Annotation>
  provenance: SOB_Reference
  metadata: {
    structural_signature,
    ruleset_id: RulesetID,           // RefinementRuleset (R1–Rk)
    applied_rules: Array<RuleID>,
    entropy_delta
  }
}
```

---

#### 3.3 CnOB — Constraint Object Basin
**Output Type:** `CONSTRAINT_LATTICE`

```markdown
CONSTRAINT_LATTICE {
  version: OBVersion
  base_graph: SROB_Reference
  constraints: Array<Constraint>
  entailment_edges: Array<EntailmentEdge>
  conflicts: Array<CONSTRAINT_CONFLICT>
  provenance: SROB_Reference
  metadata: {
    ruleset_id: RulesetID,           // ConstraintRuleset (C1–C7)
    lattice_depth,
    entailment_count
  }
}
```

---

#### 3.4 SmOB — Semantic Mapping Object Basin
**Output Type:** `SEMANTIC_SKELETON`

```markdown
SEMANTIC_SKELETON {
  version: OBVersion
  slots: Array<Slot>
  referents: Array<ReferentAnchor>
  hooks: Array<MappingHook>
  bindings: Array<BindingEdge>
  residue: Array<NodeID | ConstraintID>
  carry_forward: {
    constraints: CONSTRAINT_LATTICE,
    uncertainty: Array<UncertaintyMarker>
  }
  provenance: CnOB_Reference
  metadata: {
    ruleset_id: RulesetID,           // HookRuleset (H1–Hn)
    semantic_boundary_markers
  }
  ext: ExtensibleMetadata?
}
```

---

### 4. Pluggable Behavior

**RulesetID**  
A versioned identifier for pluggable rule sets (e.g., refinement rules, constraint families, mapping hooks). Allows swapping behavior without changing core structures.

**RB_RoutingPolicy** (Stored with runs/experiments)

```markdown
RB_RoutingPolicy {
  signature_strategy: SignatureStrategyID
  ruleset_id: RulesetID?
  residue_weight: float
  binding_weight: float
  threshold: float
  fallback_policy: FallbackStrategy
}
```

---

### 5. OB Map & Evolution

(Section remains as in Rev 2.3 – OB_Map registry, monotonic evolution rules, deprecation handling.)

---

### 6. Extensibility Guidelines (For Future OB Layers)

(Section remains as in Rev 2.3 – controlled addition of new layers via OB Map.)

---

**End of Revision 2.5**

---

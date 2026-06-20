**OB Pipeline Specification — Revision 7 (Stabilized Baseline)**

This is the current agreed baseline. Suitable for integration into 20.40.

**1. SOB — Structural Object Basin**  
**Purpose:** Maximal raw structural extraction with zero transformation.  
**Output Type:** `SOB_ATOM_SET`

**Geometric Invariants:**
- Entropy-maximal (no collapsing)
- Monotonic (no internal contradictions)
- Zero curvature

**Allowed Operations:**
- Tokenization, span detection, adjacency graph construction
- Tagging using a strictly frozen finite tag set `SOB_TAG_SET` (to be enumerated)

**Forbidden:**
- Any normalization, reordering, cleaning, or noise removal
- Any operation implying meaning, intent, or plausibility

**Error Handling:** `STRUCTURAL_ERROR(input, provenance)`

---

**2. SROB — Structural Refinement Object Basin**  
**Purpose:** Apply strictly licensed, semantics-free structural rewrites.  
**Output Type:** `SROB_GRAPH`

**Geometric Invariants:**
- Monotonic entropy reduction (never increases)
- Reversible except for provable noise
- Non-negative curvature

**Allowed Operations:**
- Canonicalization
- Collapse of provable duplicates
- Reordering only under formally defined equivalence rules (R1–Rk)

**Forbidden:**
- Any rewrite requiring semantic knowledge
- Removal of legitimate structural ambiguity

**Error Handling:** `REFINEMENT_UNCERTAINTY(rule, location, provenance)`

---

**3. CnOB — Constraint Object Basin** (Highest Risk Layer)  
**Purpose:** Build constraint lattice over refined structure without filling gaps.  
**Output Type:** `CONSTRAINT_LATTICE`

**Geometric Invariants:**
- Constraint monotonicity (only accumulate, never weaken)
- All constraints must be structurally entailed
- No semantic influence

**Allowed Operations:**
- Gap and structural contradiction detection
- Application of defined constraint families (C1–C7)

**Forbidden:**
- Gap filling or silent repairs
- Use of world knowledge or semantic plausibility

**Error Handling:** `CONSTRAINT_CONFLICT(c1, c2, provenance)`

---

**4. SmOB — Semantic Mapping Object Basin**  
**Purpose:** Produce neutral semantic skeleton for RB/TB handoff.  
**Output Type:** `SEMANTIC_SKELETON`

**Geometric Invariants:**
- Semantic neutrality (no interpretive bias)
- Full traceability
- No premature semantic collapse

**Allowed Operations:**
- Creation of typed slots, referent anchors, and mapping hooks (H1–Hn)
- Packaging of structure + constraints + gaps + uncertainty markers

**Forbidden:**
- Ambiguity resolution
- Interpretation, stance, or truth assignment

**Error Handling:** Propagate all prior errors and uncertainty unchanged

---

**Global OB Chain Requirements (Locked)**
1. Strict Layer Independence (no forward peeking)
2. Full Provenance & Traceability
3. Replay Equivalence
4. Monotonic Entropy Reduction
5. Non-Negative Curvature
6. Explicit Uncertainty / Error Propagation
7. Routing & Epoch Compatibility (trip-level, OBG evolution)

---

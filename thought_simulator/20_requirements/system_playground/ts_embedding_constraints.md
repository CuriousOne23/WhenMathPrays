# **ts_embedding_constraints.md**
### **Embedding Constraints for φ(G) in the Thought Simulator**

---

## **1. Introduction**

The embedding function φ(G) is the critical bridge between TS’s structured meaning pipeline (TP → G) and its geometric substrate (the TS manifold). Unlike statistical embeddings, φ(G) is not learned, stochastic, or emergent. It is a **deterministic, structure‑preserving, invertible mapping** designed to encode the essential invariants of meaning, identity, truth, governance, and coherence.

This paper formalizes the **constraints** that shape φ(G). These constraints arise from four independent but convergent sources:

1. Linguistic structure
2. TS architectural requirements
3. Manifold geometry and basin taxonomy
4. Hardware realizability on a normal laptop

The purpose of this document is to show that φ(G)’s dimensionality, block structure, and invariants are not arbitrary design choices. They are **forced** by the nature of language, the needs of TS, and the practical realities of implementation.

---

## **2. Purpose of This Paper**

This paper defines the **minimum set of constraints** that any TS embedding must satisfy. Specifically, it aims to:

- Justify the dimensionality of φ(G)
- Justify the block‑structured layout
- Explain why certain features must be preserved
- Show how linguistic and computational constraints converge
- Ensure φ(G) is implementable on ordinary hardware
- Provide a foundation for the manifold embedding function E(φ(G))
- Support future refinement without breaking compatibility

This is not a specification of φ(G) itself (that appears in a separate document).  
This is the **theoretical justification** for why φ(G) must look the way it does.

---

## **3. Constraints from Linguistic Structure**

Human language is one of the most deeply studied systems in cognitive science. Across typology, syntax, semantics, morphology, pragmatics, and discourse theory, we have a stable, cross‑linguistic inventory of structural categories.

These include:
- semantic roles (≈ 30–40)
- syntactic roles (≈ 20–30)
- morphological categories (≈ 40–60)
- discourse functions (≈ 20–30)
- pragmatic operators (≈ 20–30)
- referential structures (≈ 20–40)
- logical operators (≈ 10–20)
- conceptual categories (≈ 50–100)

These categories are finite, well‑defined, and empirically grounded. Most require multiple degrees of freedom to encode strength, salience, polarity, or hierarchy.

This yields a natural embedding range of **hundreds of dimensions** to faithfully preserve linguistic structure. This is the first independent constraint on φ(G).

---

## **4. Constraints from TS Architecture**

TS imposes its own structural requirements. φ(G) must preserve:

- OB type counts
- relation type counts
- structural invariants (depth, branching, degree)
- ΔH% entropy measures
- identity anchors (CBMn-series)
- truth markers (TBMn-series)
- governance markers (GBMn-series)
- coherence markers (ChBMn-series)
- provenance and versioning flags
- windowed OB fields (local independence between structural regions)

Each of these categories requires a fixed number of slots to remain invertible and deterministic. When enumerated, these constraints independently imply **≈ 512 dimensions** as the minimal viable embedding.

This is the second independent constraint.

---

## **5. Constraints from Basin Geometry**

The TS manifold contains several basin families:

- **CBMn-series** (Context / Identity Basins) — persistent anchors
- **Concept Basins** (Semantic Attractors) — relational neighborhoods
- **TBMn-series** (Truth Basins) — factual stability
- **GBMn-series** (Governance Basins) — policy and safety constraints
- **ChBMn-series** (Coherence Basins) — low-entropy stability regions
- **IBMn-series** (Inquiry Basins) — uncertainty and ambiguity regions

Each basin family requires its own **feature block** in φ(G) to ensure separability, stability, curvature alignment, and predictable trajectories. This enforces a **block‑structured embedding**, not a flat vector.

This is the third independent constraint.

---

## **6. Constraints from Invertibility and Windowed Fields**

TS requires that φ(G) preserve counts, structure, identity anchors, governance flags, ΔH%, and referential consistency. This rules out low-dimensional, learned, stochastic, or collapsing embeddings.

Additionally, the windowed nature of OB fields (as defined in the OB Data Structures specification) enforces **local independence** between structural regions of G. Windowing prevents cross-contamination and requires that φ(G) preserve window boundaries in a separable, identifiable way.

These requirements force φ(G) to be **high-dimensional and block-structured**.

---

## **7. Constraints from Hardware Realizability**

TS is designed to run reliably on a normal laptop configuration sold today. This imposes strict engineering constraints:

- φ(G) must fit comfortably in L2/L3 cache
- E(φ(G)) must use simple integer/float operations
- basin evaluation must be branch-predictable
- curvature modeling must avoid large matrix multiplications
- the entire pipeline must run without GPU acceleration
- memory footprint must remain small and stable
- cycle counts must be predictable and bounded

These constraints rule out extremely high-dimensional embeddings, dynamic feature sets, and GPU-dependent operations. They strongly favor a **fixed-size, 512-dimensional, block-structured embedding**.

This is the fourth independent constraint.

---

## **8. Constraints on Extra-Structural Fields and Partitioning Across OB Layers**

TS requires a set of fields that extend beyond the linguistic categories enumerated in Section 3. These additional fields arise from TS-specific invariants: governance, truth-tracking, coherence, identity persistence, entropy modeling, windowing, and provenance. Although these fields are not linguistic in origin, they are essential for determining manifold location, curvature, and gradient.

To maintain determinism, invertibility, and hardware feasibility, these extra fields must be strictly bounded and partitioned across the OB layers.

### **8.1. Upper Bound on Extra Fields**

The total number of non-linguistic fields must remain small relative to the linguistic core. TS imposes the following constraints:

- Extra fields must not exceed 25–35% of φ(G)’s dimensionality.
- For a 512-dimensional embedding, this yields a maximum of ≈120–160 extra dimensions.
- These fields must be block-structured, not interleaved with linguistic features.
- Each block must be independently interpretable and window-preserving.

This ensures φ(G) remains compact, cache-friendly, and invertible.

### **8.2. Partitioning of Extra Fields Across OB Layers**

The OB pipeline is responsible for extracting both linguistic and TS-specific invariants. The partitioning is as follows:

**SOB (Structural OB)**  
Carries syntactic structure, morphological triggers, window boundaries.  
Extra fields: window independence flags, structural anomaly markers.

**SROB (Semantic-Role OB)**  
Carries semantic roles, predicate–argument structure, event frames.  
Extra fields: ΔH% local entropy around role assignments, ambiguity markers.

**CnOB (Conceptual OB)**  
Carries conceptual categories, referential structures, ontological commitments.  
Extra fields: identity-stability hints, conceptual neighborhood curvature hints.

**SmOB (Semantic-Meaning OB)**  
Carries discourse functions, pragmatic operators, logical operators.  
Extra fields: coherence markers, unresolved reference counts, discourse-level ΔH%.

**IdOB (Identity OB)**  
IdOB is structurally different. It does not extract linguistic categories. It extracts persistent identity invariants across turns.  
Carries identity anchors, context profile hashes, worldview curvature hints, long-range referential stability.  
Extra fields: identity basin proximity, identity-based governance constraints, cross-turn coherence markers.

IdOB is the only OB whose fields directly influence cross-turn manifold continuity.

### **8.3. How Extra Fields Affect Manifold Location and Gradient**

Every extra field influences one of the following:

- **Location**: identity anchors, conceptual curvature hints, governance boundary proximity, truth-value hints
- **Gradient**: ΔH% (global and local), coherence stability, contradiction markers, safety constraint triggers
- **Curvature**: governance markers, worldview curvature, identity-based curvature
- **Basin Pull**: truth markers → TBMn, identity markers → CBMn, coherence markers → ChBMn, uncertainty markers → IBMn

There are no unused fields. Every field contributes to placement, movement, or stability.

---

## **9. Convergence of Constraints**

We now have four independent systems:

| Constraint Source          | Implied Dimensionality       |
|----------------------------|------------------------------|
| Linguistic structure       | Hundreds of dimensions       |
| TS architecture            | ≈ 512 dimensions             |
| Basin geometry             | Block-structured, multi-hundred dims |
| Hardware realizability     | ≤ 512–640 dimensions         |

These converge on:
> **A 512-dimensional, block-structured φ(G)**

as the natural, principled embedding for TS. This is not a guess. It is the intersection of linguistic, architectural, geometric, and hardware constraints.

---

## **10. Summary**

φ(G) is constrained by the structure of human language, the requirements of TS, the geometry of the manifold, and the realities of laptop-class hardware. These constraints converge on a **512-dimensional, block-structured embedding** that is:

- deterministic
- invertible
- cache-friendly
- basin-aligned
- governance-aware
- linguistically grounded
- implementable today

This paper establishes the theoretical foundation for φ(G). The companion document, `ts_embedding_schema_v0.1.md`, defines the concrete layout.

---

## **11. Conclusion**

The embedding constraints defined here are not arbitrary design choices — they are the principled outcome of converging requirements from language, architecture, geometry, and practical hardware limits. By grounding φ(G) in this way, TS maintains a clean, deterministic bridge from structured meaning (TP → G) to geometric representation (the TS manifold), while remaining faithful to its core invariants and laptop-class philosophy.

This framework is a hypothesis in the scientific sense: structured, testable, and open to refinement. It provides a solid foundation for the nonlinear manifold embedding E(φ(G)) and for the next phase of TS development — implementing the manifold module in the minimal interpreter.

The road is now visible.

---

**End of Document**

---

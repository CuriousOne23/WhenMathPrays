# **ts_manifold_embedding_E_phiG.md**
### **E(φ(G)) — Manifold Embedding of the φ(G) Block Structure**

**Version:** 0.1.0-draft  
**Status:** Architecture Specification (Exploratory)  
**Depends on:** `phi_g_schema.md`, `ts_embedding_constraints.md`

---

## **1. Purpose and Scope**

This document specifies the embedding function **E : φ(G) → M**, which maps each typed block of the φ(G) schema into the TS manifold. The goal is to provide a **deterministic, inspectable, and computationally practical** bridge between the structured graph representation of meaning and the geometric substrate used for basin placement, trajectory tracking, and stability enforcement.

This is a **minimal viable embedding** focused on:
- preserving TS invariants
- enabling basin and trajectory reasoning
- remaining implementable on laptop-class hardware
- supporting future refinement without breaking determinism

**Paper series:**  
[tp_g_phi_to_ts_manifold.md](tp_g_phi_to_ts_manifold.md) - Exploratory system‑playground mapping from TP → G → φ(G) → TS geometry  
[phi_g_schema.md](phi_g_schema.md) - The authoritative schema: what φ(G) must contain and why.  
[ts_embedding_constraints.md](ts_embedding_constraints.md) - The constraints that force φ(G) to embed into TS the way it does.  
[ts_manifold_embedding_E_phiG.md](ts_manifold_embedding_E_phiG.md) - The deterministic embedding: how each φ(G) block becomes curvature, basins, gradients, trajectories. 
[ts_dynamics_from_phiG_embedding.md](ts_dynamics_from_phiG_embedding.md) - Discusses the required dynamics that TS must exhibit on the manifold  

---

## **2. Manifold Preliminaries**

### **2.1 The TS Manifold M**
The TS manifold **M** is a curved, relational geometric space where meaning points, basins, and trajectories live. It is not a physical manifold but a constructed semantic substrate where governance, stability, and relational structure become geometric properties.

**Key properties of M**:
- Finite-dimensional (for v0.1, a fixed low-dimensional space, e.g., 8–16 dimensions)
- Curved (governance and constraints induce curvature)
- Contains stable regions (basins)
- Supports trajectories (sequences of points across commits)
- Deterministic and replayable

### **2.2 Coordinate Convention**
All embeddings are expressed relative to the **identity anchor point p₀** (the image of the IdOB block). This serves as the origin for the current turn’s coordinate chart. This choice simplifies computations and enforces identity stability.

---

## **3. φ(G) Block Taxonomy Reminder**

As defined in `phi_g_schema.md`, φ(G) is partitioned into linguistic blocks (A–D) and TS-specific invariant blocks (E–J). Each block carries typed features that must be mapped geometrically while preserving:
- determinism
- invertibility (within bounds)
- windowing and locality
- governance and coherence invariants

---

## **4. Per-Block Embedding Rules (Minimal Viable)**

### **4.1 Identity Block — φ_id → Origin Anchor p₀**
**Embedding:**
```
E(φ_id) = p₀  (the coordinate origin for this turn)
```

**Role:** Defines the global reference frame. All other embeddings are relative to p₀.  
**Constraint:** The identity anchor must remain stable across turns (CBMn-series influence).

---

### **4.2 Concept & Identity Blocks — φ_CBMn → Basin Placement**
**Embedding:**
```
E(φ_CBMn) = (p_basin, r_basin, strength)
```
- `p_basin` — center of the basin in M
- `r_basin` — radius of the basin neighborhood
- `strength` — how strongly the point is pulled toward the basin

**Role:** Places meaning into stable semantic or identity regions.  
**Constraint:** Basins must be disjoint or have controlled overlap governed by transition blocks.

---

### **4.3 Truth & Governance Blocks — φ_TBMn / φ_GBMn → Curvature Regions**
**Embedding:**
```
E(φ_TBMn/GBMn) = (region, curvature_level)
```
- `region` — area in M affected by truth/governance constraints
- `curvature_level` — strength of constraint (higher = steeper walls)

**Role:** Creates “walls” or “valleys” that influence trajectories and prevent drift into unsafe or false regions.  
**Constraint:** High-curvature regions increase the cost of crossing (enforced by governance).

---

### **4.4 Coherence Blocks — φ_ChBMn → Low-Entropy Attractors**
**Embedding:**
```
E(φ_ChBMn) = (p_coherence, depth)
```
- `p_coherence` — center of coherence region
- `depth` — how strongly the basin pulls (related to low ΔH%)

**Role:** Attracts well-formed, low-entropy meaning clusters.  
**Constraint:** Trajectories should naturally settle into these regions as coherence increases.

---

### **4.5 Inquiry / Uncertainty Blocks — φ_IBMn → High-Uncertainty Regions**
**Embedding:**
```
E(φ_IBMn) = (p_uncertainty, uncertainty_level)
```
**Role:** Marks regions where ambiguity or missing structure exists.  
**Constraint:** High uncertainty should trigger IB and increase the likelihood of correction or clarification.

---

### **4.6 Transition & Trajectory Blocks — φ_tr / φ_γ → Paths**
**Embedding:**
```
E(φ_tr/φ_γ) = path  (a sequence of points in M)
```
**Role:** Connects basins and records thought evolution.  
**Constraint:** Paths must respect curvature and basin boundaries (governed by GB).

---

## **5. Global Embedding and Consistency Conditions**

```
E(φ(G)) = { E(B) for each block B in φ(G) }
```

**Key Consistency Rules**:
- Identity anchor (p₀) is fixed for the turn
- Basins must be disjoint or have controlled overlap
- Trajectories must respect curvature (cannot cross high-governance walls without justification)
- Total embedding must preserve windowing and locality
- All mappings must be deterministic and replayable

**Dimensionality note**: For v0.1, M is a fixed low-dimensional space (e.g., 8–16 dimensions) where each φ(G) block contributes to basin placement, curvature, and trajectory parameters rather than direct coordinate axes.

---

## **6. Practical Implementation Notes**

- **Coordinate System**: Use simple vector offsets from p₀ for initial implementation.
- **Basin Detection**: Distance to basin centers + curvature checks.
- **Trajectory Tracking**: Record sequence of points with ΔH% and governance flags.
- **Hardware Goal**: Keep all operations simple (vector math, distance calculations, table lookups). No heavy differential geometry in v0.1.
- **Extensibility**: The embedding is designed to be extended later with more sophisticated geometry while preserving determinism in the core path.

**E is not required to be invertible** — it is a semantic projection, not a lossless encoding.

---

## **7. Open Questions / Next Steps**

- How to efficiently compute basin membership and curvature effects in the minimal interpreter?
- How should IdOB cross-turn persistence be encoded in the embedding?
- What is the best way to handle dynamic basin creation or merging?
- When should we introduce more advanced geometric tools?

---

## **8. Conclusion**

This document defines a **minimal, deterministic embedding E(φ(G))** that maps TS’s structured meaning into a geometric manifold while respecting all core invariants. By keeping the mapping simple, block-structured, and hardware-friendly, we create a practical foundation for basin placement, trajectory tracking, and governance enforcement.

This is the first step toward making TS geometric. The next documents will refine the embedding function and begin implementation in the minimal interpreter.

---

**End of Document**

---

Let me know if you want any final tweaks or if we should move on to the next document.  

I’m ready whenever you are.

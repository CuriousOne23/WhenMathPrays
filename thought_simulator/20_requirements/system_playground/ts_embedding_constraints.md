# **ts_embedding_constraints.md**  
### **Embedding Constraints for φ(G) in the Thought Simulator**

---

## **1. Introduction**

The embedding function φ(G) is the critical bridge between TS’s structured meaning pipeline (TP → G) and its geometric substrate (the TS manifold). Unlike statistical embeddings, φ(G) is not learned, stochastic, or emergent. It is a **deterministic, structure‑preserving, invertible mapping** designed to encode the essential invariants of meaning, identity, truth, governance, and coherence.

This paper formalizes the **constraints** that shape φ(G). These constraints arise from four independent but convergent sources:

1. **Linguistic structure**  
2. **TS architectural requirements**  
3. **Manifold geometry and basin taxonomy**  
4. **Hardware realizability on a normal laptop**

The purpose of this document is to show that φ(G)’s dimensionality, block structure, and invariants are not arbitrary design choices. They are **forced** by the nature of language, the needs of TS, and the practical realities of implementation.

---

## **2. Purpose of This Paper**

This paper defines the **minimum set of constraints** that any TS embedding must satisfy. Specifically, it aims to:

- justify the dimensionality of φ(G)  
- justify the block‑structured layout  
- explain why certain features must be preserved  
- show how linguistic and computational constraints converge  
- ensure φ(G) is implementable on ordinary hardware  
- provide a foundation for the manifold embedding function E(φ(G))  
- support future refinement without breaking compatibility  

This is not a specification of φ(G) itself (that appears in a separate document).  
This is the **theoretical justification** for why φ(G) must look the way it does.

---

## **3. Constraints from Linguistic Structure**

Human language is one of the most deeply studied systems in cognitive science. Across typology, syntax, semantics, morphology, pragmatics, and discourse theory, we have a stable, cross‑linguistic inventory of structural categories.

These include:

- **semantic roles** (≈ 30–40)  
- **syntactic roles** (≈ 20–30)  
- **morphological categories** (≈ 40–60)  
- **discourse functions** (≈ 20–30)  
- **pragmatic operators** (≈ 20–30)  
- **referential structures** (≈ 20–40)  
- **logical operators** (≈ 10–20)  
- **conceptual categories** (≈ 50–100)  

These categories are **finite**, **well‑defined**, and **empirically grounded**.

Most require **multiple degrees of freedom** to encode strength, salience, polarity, or hierarchy.  
This yields a natural embedding range of:

> **≈ 400–800 dimensions**  
to faithfully preserve linguistic structure.

This is the first independent constraint on φ(G).

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

Each of these categories requires a **fixed number of slots** to remain invertible and deterministic.

When enumerated, these constraints independently imply:

> **≈ 512 dimensions**  
as the minimal viable embedding.

This is the second independent constraint.

---

## **5. Constraints from Basin Geometry**

The TS manifold contains several basin families:

- **IBMn-series** (inquiry / uncertainty basins)  
- **CBMn-series** (context / identity basins)  
- **Concept Basins** (semantic attractors)  
- **TBMn-series** (truth basins)  
- **GBMn-series** (governance basins)  
- **ChBMn-series** (coherence basins)  

Each basin family requires its own **feature block** in φ(G) to ensure:

- separability  
- stability  
- curvature alignment  
- predictable trajectories  

This enforces a **block‑structured embedding**, not a flat vector.

This is the third independent constraint.

---

## **6. Constraints from Invertibility**

TS requires that φ(G):

- preserve counts  
- preserve structure  
- preserve identity anchors  
- preserve governance flags  
- preserve ΔH%  
- preserve referential consistency  

This rules out:

- low‑dimensional embeddings  
- learned embeddings  
- stochastic embeddings  
- embeddings that collapse categories  

Invertibility is a hard constraint.  
It forces φ(G) to be **high‑dimensional and structured**.

---

### **6.1. Constraints from Windowed OB Fields**

The OB Data Structures paper establishes that all OB fields are **windowed**.  
Windowing enforces **local independence** between structural regions of G and prevents cross‑contamination between unrelated features. This has direct implications for φ(G):

- φ(G) must preserve window boundaries  
- φ(G) must not collapse or merge windowed regions  
- each window must contribute to φ(G) in a separable, identifiable way  
- window independence must remain visible in the embedding  
- windowed structure must be recoverable from φ(G)  

This requirement forces φ(G) to adopt a **block‑structured layout**, where each block corresponds to a windowed region or a window‑derived feature family. Windowing therefore acts as an additional structural constraint on the embedding, reinforcing the need for a high‑dimensional, partitioned representation.

---

## **7. Constraints from Hardware Realizability**

TS is designed to run **reliably on a normal laptop configuration sold today**.  
This imposes strict engineering constraints:

- φ(G) must fit comfortably in L2/L3 cache  
- E(φ(G)) must use simple integer/float operations  
- basin evaluation must be branch‑predictable  
- curvature modeling must avoid large matrix multiplications  
- the entire pipeline must run without GPU acceleration  
- memory footprint must remain small and stable  
- cycle counts must be predictable and bounded  

These constraints rule out:

- extremely high‑dimensional embeddings  
- dynamic or unbounded feature sets  
- GPU‑dependent operations  
- large learned matrices  

They strongly favor:

- a **fixed‑size embedding**  
- a **block‑structured layout**  
- a **512‑dimensional φ(G)**  
- deterministic, cache‑friendly operations  

This is the fourth independent constraint.

---

## **8. Convergence of Constraints**

We now have four independent systems:

| Constraint Source | Implied Dimensionality |
|-------------------|------------------------|
| Linguistic structure | 400–800 dims |
| TS architecture | ≈512 dims |
| Basin geometry | block‑structured, multi‑hundred dims |
| Hardware realizability | ≤512–640 dims |

These converge on:

> **A 512‑dimensional, block‑structured φ(G)**  
as the natural, principled embedding for TS.

This is not a guess.  
It is the intersection of linguistic, architectural, geometric, and hardware constraints.

---

## **9. Summary**

φ(G) is constrained by:

- the structure of human language  
- the requirements of TS  
- the geometry of the manifold  
- the realities of laptop‑class hardware  

These constraints converge on a **512‑dimensional, block‑structured embedding** that is:

- deterministic  
- invertible  
- cache‑friendly  
- basin‑aligned  
- governance‑aware  
- linguistically grounded  
- implementable today  

This paper establishes the theoretical foundation for φ(G).  
The companion document, **`ts_embedding_schema_v0.1.md`**, defines the concrete layout.

---

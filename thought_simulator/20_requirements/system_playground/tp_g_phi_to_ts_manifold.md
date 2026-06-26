# **`tp_g_phi_to_ts_manifold.md`**  
### *Mapping TP → G → φ(G) into the TS Manifold*  
### *System Playground Document — Exploratory, Non‑Normative*

---

# **1. Purpose of This Document**

This paper defines the conceptual and mathematical bridge between:

- **TP** (Thought Primitive structures)  
- **G** (graph representation of TP)  
- **φ(G)** (linear vector transform of G)  
- **the TS manifold** (the geometric substrate where basins, trajectories, and stability live)

This is the first document that explains **how TS becomes geometric**, not just procedural.

It is exploratory and non‑normative. Once stabilized, it will graduate into the 20.900‑series.

---

# **2. The Mapping Pipeline**

```
TP → G → φ(G) → E(φ(G)) → manifold point M → basin placement → trajectory update
```

Where:

- **TP** = structured thought primitives  
- **G** = graph representation (nodes = OBs, edges = relations)  
- **φ(G)** = deterministic vector embedding  
- **E** = nonlinear manifold embedding  
- **M** = point in the TS manifold  
- **basins** = IBMn, TBMn, GBMn, CBMn, ChBMn  
- **trajectory** = sequence of manifold points across commits  

This pipeline is the backbone of TS geometry.

---

# **3. What the TS Manifold *Is***  
### **Crisp Definition**

> **The TS manifold is a curved, relational geometric space where meaning points, basins, and trajectories live. It is not a physical manifold but a constructed semantic substrate where governance, stability, and relational structure become geometric properties.**

The manifold provides:

- **basins** (stable attractors: IBMn, TBMn, GBMn, CBMn, ChBMn)  
- **curvature** (constraints and governance)  
- **geodesics** (preferred reasoning paths)  
- **semantic neighborhoods** (conceptual proximity)  
- **identity anchors** (persistent objects)  

This is the geometric layer that gives TS long‑term coherence.

---

# **4. TP → G: Structured Graph Representation**

TP structures (OuB, IdOB, REx, SROB, CnOB, SmOB, etc.) are converted into a graph **G**:

- **nodes** = OB instances  
- **edges** = typed relations (identity, reference, containment, semantic link)  
- **metadata** = ΔH%, provenance, timestamps, basin hints  

G is:

- deterministic  
- replayable  
- invariant‑preserving  
- fully inspectable  

This is the **pre‑geometric** representation of meaning.

---

# **5. G → φ(G): Linear Vector Transform**

φ(G) is a **linear, structure‑preserving transform** that maps the graph into a fixed‑dimension vector.

### **Concrete Example (tightened)**  
φ(G) might encode:

- node types (OuB, IdOB, REx…)  
- relation counts (agent, patient, modifier…)  
- ΔH%  
- structural features (depth, branching, degree)  
- provenance bits  

into a fixed‑dimension vector such as:

```
φ(G) = [type_counts, relation_counts, ΔH%, depth, branching, provenance_bits]
```

Properties:

- deterministic  
- invertible (within TS constraints)  
- invariant‑respecting  
- no curvature  
- no basins  

φ(G) is **not** the manifold.  
It is the **coordinate seed** for the manifold.

---

# **6. Why φ(G) Alone Is Not Enough**

φ(G) is linear.  
The TS manifold is **curved**.

TS needs:

- basins (IBMn, TBMn, GBMn, CBMn, ChBMn)  
- attractors  
- stability regions  
- geodesics  
- curvature from governance  
- semantic neighborhoods  
- identity persistence  

None of these can be expressed in a purely linear space.

Thus, φ(G) must be **embedded** into a nonlinear manifold.

---

# **7. φ(G) → E(φ(G)): Nonlinear Embedding into the TS Manifold**

The embedding function **E** maps φ(G) into the TS manifold **M**.

### **Concrete Implementation Hint (clarified)**  
E may be implemented as:

- a composition of deterministic geometric transforms  
- with optional **bounded** neural guidance  
- while strictly preserving governance constraints and invariants  

Formally:

```
M = E(φ(G))
```

Where M is a point in a curved manifold with basin structure.

This is where TS becomes geometric.

---

# **8. Basin Types (Updated to IBMn/TBMn/GBMn/CBMn/ChBMn)**

TS defines several basin classes, now expressed in the canonical manifold naming scheme:

---

### **1. CBMn-series (Context Basins)**  
Stable attractors for persistent contextual anchors such as identity, demographic priors, worldview, and long‑term interpretive bias.

Examples:  
- CBMn1: identity anchor for “the cat”  
- CBMn2: demographic prior  
- CBMn3: worldview curvature field  

---

### **2. Concept Basins (Semantic Attractors)**  
These remain conceptually basins but are not part of the IBMn/TBMn/GBMn series.  
They are semantic attractors defined by relational structure.

Examples:  
- “cat” in the *animal* semantic neighborhood  
- “chase” in the *interaction* neighborhood  

These are **deterministic semantic attractors**.

---

### **3. TBMn-series (Truth Basins)**  
Regions shaped by governance constraints and factual stability.

Examples:  
- TBMn1: physical truths  
- TBMn2: definitional truths  
- TBMn3: stable factual clusters  

---

### **4. GBMn-series (Governing Basins)**  
Regions where governance curvature is strong.

Examples:  
- GBMn1: safety constraints  
- GBMn2: policy boundaries  
- GBMn3: high-curvature governance walls  

---

### **5. ChBMn-series (Coherence Basins)**  
Low‑entropy attractors where ΔH% naturally decreases.

Examples:  
- ChBMn1: stable meaning cluster  
- ChBMn2: narrative coherence region  

---

### **6. IBMn-series (Inquiry Basins)**  
Regions representing structured uncertainty, ambiguity, or missing structure.

Examples:  
- IBMn1: ambiguity attractor  
- IBMn2: contradiction attractor  
- IBMn3: missing‑structure attractor  

These are **not** the TS primitives — they are geometric uncertainty regions.

---

# **9. Trajectories in the TS Manifold**

A **trajectory** is a sequence of manifold points:

```
M₀ → M₁ → M₂ → … → Mₙ
```

Each Mᵢ corresponds to a **commit_id**.

Trajectory bending occurs when:

- IBMn-series regions are entered (ambiguity)  
- IMR fires (output mismatch correction)  
- GBMn-series curvature applies  
- ΔH% changes significantly  

Trajectories allow TS to:

- detect drift  
- enforce stability  
- govern token usage  
- route to coprocessors  
- maintain long‑term coherence  

---

# **10. Curvature: How Governance Shapes Geometry**

Curvature in the TS manifold is induced by:

- invariants  
- governance rules  
- TS‑concept constraints  
- semantic consistency requirements  

Examples:

- approaching a GBMn boundary increases curvature  
- CBMn basins have strong local minima  
- TBMn basins have steep walls  
- concept basins have smooth gradients  

Curvature determines:

- allowed trajectories  
- correction paths  
- when to escalate to COP2  
- how ΔH% is interpreted  

---

# **11. Why TS Needs a Manifold**

The manifold enables:

### **1. Long‑term coherence**  
Meaning stays stable across turns.

### **2. Token‑efficient agent behavior**  
TS only calls COP2 when the trajectory enters high‑curvature or high‑entropy regions.

### **3. Hybrid routing**  
Different coprocessors handle different regions of the manifold.

### **4. Identity stability**  
Objects remain anchored in CBMn-series basins.

### **5. Drift detection**  
TS can detect when meaning is sliding out of a basin.

### **6. Governance enforcement**  
GBMn curvature becomes geometric, not procedural.

This geometric layer allows TS to implement the **functional properties of coherent thought** without claiming to solve the underlying mystery of cognition.

---

# **12. Minimal Mathematical Sketch (Refined)**

Let:

- φ(G) ∈ ℝⁿ  
- E: ℝⁿ → M (nonlinear embedding)  
- M = TS manifold  

Then:

- basins = local minima of potential function V(M)  
- trajectories = geodesics under metric g(M)  
- curvature = ∂²V/∂M²  
- ΔH% = local entropy estimate along trajectory  

This sketch is intentionally minimal — enough to guide implementation without overcommitting.

---

# **13. Example Walkthrough**

### **Input:**  
User says: “The cat chased the mouse.”

### **TP → G:**  
Nodes: Cat, Mouse, Chase  
Edges: agent(cat, chase), patient(mouse, chase)

### **G → φ(G):**  
Linear vector encoding of structure.

### **φ(G) → M:**  
Embedding places the meaning in:

- **Concept Basin:** “animal interaction”  
- **CBMn-series:** identity anchors for cat, mouse  
- **TBMn-series:** neutral truth region  
- **ChBMn-series:** low ΔH% coherence region  

### **Trajectory:**  
If user later says: “Actually, the mouse chased the cat,”  
trajectory bends sharply → enters IBMn-series region.

---

# **14. Conclusion**

This paper establishes the first geometric bridge between TS’s structured meaning (TP → G → φ(G)) and its long‑term semantic stability (the TS manifold). By defining basins, curvature, and trajectories using the IBMn/TBMn/GBMn/CBMn/ChBMn taxonomy, TS gains the ability to maintain coherence, govern token usage, and integrate hybrid coprocessors in a principled way.

This geometric layer is the foundation for the next phase of TS development:  
**implementing the manifold module in the minimal interpreter.**

---

# **End of Document**

---

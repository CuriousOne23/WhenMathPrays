**Draft Section: The Four Pre‑Semantic OB Layers and Their Geometric Requirements**

#### **1. Overview**
Before TS reaches deep semantic OBs, it passes through four foundational OB layers that progressively refine structure, reduce entropy, and stabilize routing. These layers ensure that semantic OBs never guess, never hallucinate, and never drift. They also enforce the geometric properties required for deterministic routing.

The four layers are:

1. **SOB — Structural OBs**  
2. **PrSOB — Pre‑Semantic OBs**  
3. **CrOB — Constraint OBs**  
4. **FsOB — First‑Semantic OBs**

Each layer has a distinct role, fingerprint, and routing behavior.

---

#### **2. SOB — Structural OBs**
**Definition:**  
SOBs are the most general OBs. They extract structure before meaning.

**Functions:**  
- segmentation (sentences, clauses, lists, tables, code blocks)  
- grammar and modality hints  
- operator hints (summarize, derive, classify, plan)  
- domain hints (math‑like, narrative‑like, code‑like)  
- tone/subculture hints  
- constraint hints (precision, safety, conciseness)

**Trip Level:**  
Always first. Every message enters through SOBs.

**Output:**  
A structured TP and residue that is now addressable.

---

#### **3. PrSOB — Pre‑Semantic OBs**
**Definition:**  
PrSOBs refine the coarse structure and hints extracted by SOBs. They do not extract meaning; they prepare the residue for semantic extraction.

**Functions:**  
- sharpen domain classification  
- sharpen operator classification  
- refine tone/subculture  
- normalize structure  
- detect contradictions  
- detect missing metadata  
- detect implicit operators  
- reduce entropy

**Trip Level:**  
Triggered when SOBs leave non‑trivial residue with ambiguous or incomplete metadata.

**Output:**  
A cleaner, sharper, lower‑entropy residue.

---

#### **4. CrOB — Constraint OBs**
**Definition:**  
CrOBs extract and enforce constraints that shape downstream semantic interpretation.

**Functions:**  
- precision level  
- determinism level  
- safety constraints  
- politeness constraints  
- conciseness constraints  
- formatting constraints  
- domain‑specific constraints (e.g., math rigor, legal formality)

**Trip Level:**  
Triggered when residue contains explicit or implicit constraints.

**Output:**  
A residue with explicit constraints and no hidden assumptions.

---

#### **5. FsOB — First‑Semantic OBs**
**Definition:**  
FsOBs perform the first layer of true semantic extraction. They are not deep semantic OBs; they are the first interpreters.

**Functions:**  
- extract high‑level meaning  
- identify semantic roles  
- identify entities  
- identify relationships  
- identify intent  
- identify semantic operators  
- produce structured semantic fragments

**Trip Level:**  
Triggered when structure, domain, operators, and constraints are sufficiently refined.

**Output:**  
A partially interpreted semantic structure + remaining residue.

---

#### **6. Geometric Requirements for Routing**
For routing to be stable, deterministic, and drift‑free, the OB address space must satisfy strict geometric properties:

##### **6.1 Monotonicity**
If similarity increases, routing confidence must never decrease.  
If similarity decreases, routing confidence must never increase.

This prevents routing chaos and ensures stable behavior.

##### **6.2 Smoothness**
The similarity gradient must have no discontinuities or sharp kinks.  
Small changes in residue → small changes in routing confidence.

This ensures graceful partial matches and predictable routing.

##### **6.3 Curvature Invariance**
This is the key requirement you articulated:

- Same distance → same slope  
- Same distance → same curvature  
- Same distance → same second derivative  

Across **all** OBs (SOB, PrSOB, CrOB, FsOB, semantic OBs).

This ensures that the routing space is a **true metric space** with consistent meaning.

##### **6.4 OB‑Invariant Geometry**
The gradient function must be identical across all OBs.  
FsOB1 and FsOB2 must behave identically at the same similarity score.

This guarantees:

- deterministic routing  
- stable partial matches  
- predictable fallback  
- zero drift  
- perfect replay  

---

#### **7. Summary**
The four pre‑semantic OB layers form the backbone of TS routing. They progressively refine structure, reduce entropy, and stabilize the residue before semantic extraction. Their behavior is only correct if the routing space is monotonic, smooth, and curvature‑invariant across all OBs.

This geometric consistency is what makes TS efficient, deterministic, and hallucination‑free.

---

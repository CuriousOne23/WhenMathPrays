# **phi_g_schema.md**
### **Schema for φ(G) in the Thought Simulator (TS)**

---

## **1. Purpose and Scope**

This document defines the **concrete schema** for the TS embedding function `$φ(G)$`:

- total dimensionality  
- block partitioning  
- field definitions  
- ranges and invariants  
- integration of long‑range context (IdOB, COB, CIL)  

The filename `phi_g_schema.md` refers to the embedding function `$φ(G)$`.  
`ts_embedding_constraints.md` explains **why** `$φ(G)$` must be high‑dimensional and block‑structured.  
This schema paper explains **what `$φ(G)$` looks like** in practice.

Target: **512‑dimensional, fixed‑size, block‑structured embedding**, implementable on laptop‑class hardware.

---

## **2. High‑Level Partitioning of φ(G)**

`$φ(G)$` is partitioned into **linguistic blocks** and **TS‑specific invariant blocks**.

### **2.1 Dimensional Budget**

- **Total dimensions:** 512  
- **Linguistic core:** ≈ 340–380 dims (approximate to allow future tuning)  
- **TS‑specific invariants:** ≈ 130–170 dims (≤ 25–35%)

The v0.1 allocation in Section 2.2 sums to exactly 512.

### **2.2 Block Overview (v0.1)**

| Block | Source | Dims | Purpose |
|-------|--------|------|---------|
| A | SOB | 80 | Syntax, morphology, windowing |
| B | SROB | 70 | Semantic roles, event frames |
| C | CnOB | 100 | Concepts, referents, ontology |
| D | SmOB | 90 | Discourse, pragmatics, logic |
| E | IdOB | 40 | Cross‑turn identity & worldview |
| F | TBMn | 30 | Truth invariants |
| G | GBMn | 30 | Governance invariants |
| H | ChBMn | 30 | Coherence invariants |
| I | IBMn | 20 | Inquiry/uncertainty invariants |
| J | COB/CIL | 22 | Long‑range context injection |

**Total:**  
`$80 + 70 + 100 + 90 + 40 + 30 + 30 + 30 + 20 + 22 = 512$`

---

## **3. Linguistic Blocks (Per‑Turn, Windowed, Stateless)**

These blocks encode **only the current utterance**.  
They reset every turn and never contain long‑range memory.

---

### **3.1 Block A — SOB (80 dims)**  
**Role:** Structural skeleton of the utterance.

**Subfields:**

- **A1 — Syntactic role vector (24 dims)**  
  Distribution over subject, object, modifier, etc.  
  Range: `$[0,1]$`, normalized.

- **A2 — Dependency structure summary (20 dims)**  
  Depth, branching factor, key arcs.

- **A3 — Phrase/clause structure (16 dims)**  
  Major phrase types, clause segmentation.

- **A4 — Morphological triggers (12 dims)**  
  Tense, aspect, mood, number, person.

- **A5 — Window markers (8 dims)**  
  Window boundaries, local independence flags.

**Why 80 dims?**  
Sufficient to encode cross‑linguistic syntactic variety without collapsing distinctions.

---

### **3.2 Block B — SROB (70 dims)**  
**Role:** Semantic roles and event structure.

**Subfields:**

- **B1 — Semantic role distribution (30 dims)**  
- **B2 — Predicate–argument frame summary (20 dims)**  
- **B3 — Event frame features (12 dims)**  
- **B4 — Local `$ΔH\%$` around role assignments (8 dims)**  

**Why 70 dims?**  
Semantic roles require multiple degrees of freedom for strength, salience, and ambiguity.

---

### **3.3 Block C — CnOB (100 dims)**  
**Role:** Conceptual and referential structure.

**Subfields:**

- **C1 — Conceptual category vector (50 dims)**  
- **C2 — Referential structure (20 dims)**  
- **C3 — Ontological commitments (20 dims)**  
- **C4 — Identity‑stability hints (10 dims)**  

**Why 100 dims?**  
Conceptual space is large; this block must support manifold concept basins and identity basins.

---

### **3.4 Block D — SmOB (90 dims)**  
**Role:** Discourse, pragmatics, logic.

**Subfields:**

- **D1 — Discourse function vector (30 dims)**  
- **D2 — Pragmatic operator vector (25 dims)**  
- **D3 — Logical operator vector (15 dims)**  
- **D4 — Coherence markers (12 dims)**  
- **D5 — Discourse‑level `$ΔH\%$` (8 dims)**  

**Why 90 dims?**  
Discourse/pragmatics are rich but bounded; 90 dims balances expressiveness and hardware limits.

---

## **4. Identity and TS‑Specific Invariant Blocks**

These blocks encode **cross‑turn** and **system‑level invariants**.  
They must remain ≤ 25–35% of `$φ(G)$`.

---

### **4.1 Block E — IdOB (40 dims)**  
**Role:** Cross‑turn identity and worldview continuity.

**Subfields:**

- **E1 — Identity anchor strength (12 dims)**  
- **E2 — Context profile summary (10 dims)**  
- **E3 — Worldview curvature hints (10 dims)**  
- **E4 — Cross‑turn coherence markers (8 dims)**  

**Why 40 dims?**  
Enough to carry persistent identity invariants without overwhelming the linguistic core.

---

### **4.2 Block F — TBMn (30 dims)**  
**Role:** Truth‑tracking invariants.

**Subfields:**

- **F1 — Factual support score (10 dims)**  
- **F2 — Contradiction markers (8 dims)**  
- **F3 — Truth stability (8 dims)**  
- **F4 — Conflict with known facts (4 dims)**  

---

### **4.3 Block G — GBMn (30 dims)**  
**Role:** Governance and safety invariants.

**Subfields:**

- **G1 — Governance boundary proximity (10 dims)**  
- **G2 — Policy conflict markers (8 dims)**  
- **G3 — Safety constraint triggers (8 dims)**  
- **G4 — Governance curvature hints (4 dims)**  

---

### **4.4 Block H — ChBMn (30 dims)**  
**Role:** Coherence invariants.

**Subfields:**

- **H1 — Narrative coherence score (10 dims)**  
- **H2 — Referential consistency score (8 dims)**  
- **H3 — Unresolved reference count (8 dims)**  
- **H4 — Local coherence `$ΔH\%$` (4 dims)**  

---

### **4.5 Block I — IBMn (20 dims)**  
**Role:** Inquiry / uncertainty invariants.

**Subfields:**

- **I1 — Uncertainty level (8 dims)**  
- **I2 — Ambiguity markers (6 dims)**  
- **I3 — Inquiry drive (6 dims)**  

---

## **5. COB/CIL Long‑Range Context Block**

### **5.1 Block J — COB/CIL Context (22 dims)**  
**Role:** Small, controlled, precise, slow‑moving feedback block injected **after** SOB/SROB/CnOB/SmOB and RBU, at CTP.

**Subfields:**

- **J1 — Long‑range referential candidates (8 dims)**  
- **J2 — Context continuity hints (6 dims)**  
- **J3 — Worldview continuity hints (4 dims)**  
- **J4 — Identity‑based governance hints (4 dims)**  

**Why 22 dims?**  
J1–J4 are deliberately small to keep long‑range feedback stable and prevent contamination of within‑turn structure.

---

## **6. Windowing and Block Separability**

Linguistic blocks (A–D) are **windowed** as defined in `ts_embedding_constraints.md`.  
TS‑specific blocks (E–J) are **global per turn** but remain block‑separable.

This ensures:

- no cross‑contamination  
- invertibility back to G  
- predictable manifold behavior  

---

## **7. Invertibility and Implementation Notes**

### **7.1 Invertibility**

Each block:

- has fixed dimensionality  
- has named fields with defined ranges  
- is deterministically constructed  

This allows:

$$
φ^{-1}(G): \mathbb{R}^{512} \rightarrow G
$$

### **7.2 Hardware Realizability**

The schema respects:

- 512‑dimensional fixed size  
- contiguous block layout  
- simple float/int operations  
- no dynamic resizing  
- no GPU requirement  

---

## **8. Summary**

`phi_g_schema.md` defines:

- a **512‑dimensional**, **block‑structured** embedding  
- with **≈340–380 dims** for linguistic structure  
- and **≈130–170 dims** for TS‑specific invariants  
- including a **small, controlled, precise, slow‑moving** COB/CIL context block  

This schema is **v0.1**: stable enough to implement and test, yet modular enough to refine without breaking the architecture.

The next document is the **manifold embedding spec** (`ts_manifold_embedding_E_phiG.md`), defining how each block of `$φ(G)$` maps into curvature, basins, and gradient.

---

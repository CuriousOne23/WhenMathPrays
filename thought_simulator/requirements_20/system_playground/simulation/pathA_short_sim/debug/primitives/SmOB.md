# **SmOB.md — Semantic Object Basin**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Semantic Object Basin (SmOB)** is the fourth primitive in the Path‑A short simulation chain.  
SmOB performs two jobs:

1. **Semantic‑adjacent cue extraction**  
   It identifies semantic‑adjacent, modality, affect, conflict‑adjacent, and underspecification‑adjacent signals emerging from SOB → SROB → CnOB residue.

2. **Deterministic pre‑semantic compression**  
   It compresses upstream residue plus SmOB cues into:
   - a **deterministic pre‑semantic hash**, and  
   - a **TR‑input cue vector** used by the Thought Router and SSG.

SmOB is not a semantic interpreter.  
It is a **pre‑semantic basin** that stabilizes upstream structure and prepares deterministic routing inputs.

This aligns with your normative definition in 20.40.040.

---

## **2. Purpose and Function**

SmOB answers the question:

> **“What semantic‑adjacent cues exist, and how do we compress all upstream residue into a deterministic representation for routing?”**

SmOB performs:

- semantic‑adjacent cue extraction  
- modality cue extraction  
- affect marker extraction  
- conflict‑adjacent and underspecification‑adjacent signal detection  
- deterministic pre‑semantic hashing  
- TR‑input cue vector formation  
- stabilization of upstream residue  
- preparation of routing‑adjacent geometry  

SmOB ensures that downstream primitives (SSG, TR, IdOB) receive a **canonical, replay‑safe representation**.

---

## **3. Allowed SmOB Values**

SmOB may activate any of the following basin geometries:

- **semantic_adjacent_cue**  
- **modality_cue**  
- **affect_marker**  
- **routing_adjacent_cue**  
- **presemantic_residue_hash**  
- **tr_input_vector**

These correspond to the basin geometries defined in your semantic‑adjacent and routing dictionaries.

---

# **4. Structural Variables Filled by SmOB (Local View)**  
SmOB is the fourth primitive in the Path‑A pipeline.  
It fills **all semantic‑adjacent and pre‑semantic compression variables**.

For the **full IdOB structural envelope**, see:  
**`IdOB.md — Section 4: IdOB Structural Envelope (Canonical)`**

### **4.1 Structural Origin Mini‑Table (SmOB View)**

| Structural Term            | Filled by SmOB? | Notes |
|----------------------------|------------------|-------|
| **segments**               | ✘                | Provided by SOB. |
| **segment_tokens**         | ✘                | Provided by SOB. |
| **roles**                  | ✘                | Provided by SROB. |
| **constraints_matched**    | ✘                | Provided by CnOB. |
| **residue**                | ✘                | Provided by CnOB. |
| **smoothing_operations**   | ✔                | SmOB applies basin‑level smoothing to stabilize upstream residue. |
| **smoothing_residue**      | ✔                | Residue after basin smoothing. |
| **semantic_adjacent_cues** | ✔                | **Primary output** — semantic‑adjacent, modality, affect, conflict‑adjacent cues. |
| **semantic_core**          | ✘                | Constructed by IdOB. |
| **truth_relation**         | ✘                | Determined by IdOB. |
| **token_relations**        | ✘                | Determined by IdOB. |
| **ob_set_notes**           | ✔                | SmOB may add notes about cue extraction and basin compression. |

### **4.2 Summary**

SmOB fills:

- `semantic_adjacent_cues`  
- `smoothing_operations`  
- `smoothing_residue`  
- `ob_set_notes` (basin‑related notes)

All other structural, relational, and semantic variables are filled by other primitives:

```
SOB → SROB → CnOB → SmOB → IdOB
```

---

## **5. Effects**

SmOB produces the following effects:

- extracts semantic‑adjacent cues needed for IdOB  
- stabilizes upstream residue for deterministic routing  
- prepares TR‑input cue vectors  
- supports constraint satisfaction continuity  
- influences identity confirmation pathways  
- ensures replay‑safe pre‑semantic geometry  

These effects ensure that identity formation and routing operate on stable, deterministic inputs.

---

## **6. Examples**

Examples adapted from your current debug format:

- `"SmOB applied: semantic_adjacent_cues=[interrogative_scope], smoothing_operations=[adjacency_smoothing]"`  
- `"SmOB applied: semantic_adjacent_cues=[modality_cue], smoothing_residue=presemantic_residue"`  

These illustrate cue extraction and basin stabilization.

---

## **7. Notes**

- SmOB is **not** a semantic interpreter.  
- SmOB does **not** assign roles.  
- SmOB does **not** evaluate constraints.  
- SmOB is required for deterministic meaning: without basin compression, IdOB cannot form identity deterministically.  
- SmOB provides the **canonical pre‑semantic representation** for routing and identity.

---

# **Appendix A — What SmOB Means by Smoothing, Adjacency, and Smoothing Residue**

SmOB = **Semantic Object Basin**, not “Smoothing Object Block.”  
The term *smoothing* inside SmOB refers to **basin‑level stabilization**, not semantic interpretation and not cumulative residue across primitives.

This appendix defines the three key concepts SmOB uses.

---

# **A.1 What is “Smoothing” in SmOB?**  
### **Definition**  
In SmOB, *smoothing* means:

> **Deterministic basin‑level stabilization of upstream structural residue so that semantic‑adjacent cues can be extracted and compressed into a replay‑safe pre‑semantic representation.**

It is **not** semantic smoothing, statistical smoothing, or linguistic smoothing.

It is a **basin operation** that:

- resolves adjacency discontinuities  
- resolves continuity breaks  
- resolves role‑alignment inconsistencies  
- resolves segment‑alignment inconsistencies  
- prepares deterministic pre‑semantic compression  

### **Why SmOB performs smoothing**  
Because SOB → SROB → CnOB produce **structural residue** that is:

- partially matched  
- discontinuous  
- adjacency‑incomplete  
- role‑incomplete  
- constraint‑incomplete  

SmOB must stabilize this residue before IdOB can form identity.

### **Outputs of smoothing**  
- `smoothing_operations`  
- `smoothing_residue`  
- `semantic_adjacent_cues`  

---

# **A.2 What is “Adjacency” in SmOB?**  
### **Definition**  
Adjacency in SmOB means:

> **Semantic‑adjacent relationships between segments, roles, constraints, or cues that are not explicitly connected but are implicitly related.**

Examples of semantic‑adjacent relationships:

- interrogative scope adjacency  
- modality adjacency  
- affect adjacency  
- conflict adjacency  
- underspecification adjacency  
- descriptive adjacency  
- locative adjacency  
- state adjacency  

### **Why adjacency matters**  
Adjacency determines:

- which cues SmOB extracts  
- which cues IdOB uses  
- which truth‑relations are possible  
- which identity geometries are valid  

### **Adjacency cues SmOB extracts**  
Examples:

- `interrogative_scope`  
- `modality_cue`  
- `affect_marker`  
- `conflict_adjacent`  
- `underspecification_adjacent`  
- `descriptive_adjacent`  
- `locative_adjacent`  
- `state_adjacent`  

These become part of:

- `semantic_adjacent_cues`  
- `tr_input_vector`  
- `presemantic_residue_hash`

---

# **A.3 What is “Smoothing Residue”?**  
### **Definition**  
`smoothing_residue` is:

> **The leftover structural material after SmOB performs basin‑level smoothing.**

It is **not**:

- cumulative residue from SOB  
- cumulative residue from SROB  
- cumulative residue from CnOB  
- residue from the entire pipeline  

It is **only** the residue produced by SmOB’s basin operations.

### **Why smoothing_residue exists**  
Because SmOB’s basin operations may leave:

- unresolved adjacency  
- unresolved modality cues  
- unresolved affect markers  
- unresolved conflict‑adjacent signals  
- unresolved underspecification signals  

These must be passed to IdOB **separately** from CnOB residue.

### **IdOB needs both residues**  
- **CnOB residue** → constraint failures  
- **SmOB residue** → basin smoothing failures  

These are distinct failure modes.

---

# **A.4 Examples**

### **Example 1 — Adjacency Smoothing**
Input residue from CnOB:
```
residue: ['interrogative_scope', 'state_adjacent']
```

SmOB applies adjacency smoothing:
```
smoothing_operations: ['adjacency_smoothing']
semantic_adjacent_cues: ['interrogative_scope', 'state_adjacent']
smoothing_residue: []
```

### **Example 2 — Continuity Smoothing**
Input residue:
```
residue: ['modality_cue', 'underspecification_adjacent']
```

SmOB applies continuity smoothing:
```
smoothing_operations: ['continuity_smoothing']
semantic_adjacent_cues: ['modality_cue']
smoothing_residue: ['underspecification_adjacent']
```

### **Example 3 — Role‑Alignment Smoothing**
Input residue:
```
residue: ['modifier_chain']
```

SmOB applies role smoothing:
```
smoothing_operations: ['role_smoothing']
semantic_adjacent_cues: ['modifier_chain']
smoothing_residue: []
```

### **Example 4 — Segment‑Alignment Smoothing**
Input residue:
```
residue: ['locative_adjacent']
```

SmOB applies segment smoothing:
```
smoothing_operations: ['segment_smoothing']
semantic_adjacent_cues: ['locative_adjacent']
smoothing_residue: []
```

---

## **A.4.1 Detailed Examples of Each SmOB Smoothing Type**

These examples use the *actual* kinds of residue and cues your simulator produces in `debug_out.md` (e.g., `interrogative_scope`, `modifier_chain`, `locative_adjacent`, `underspecification_adjacent`, etc.).

Each example shows:

- **input residue** (from SOB → SROB → CnOB)  
- **the smoothing type SmOB applies**  
- **semantic‑adjacent cues extracted**  
- **smoothing_residue** (leftover basin material)

---

### ⭐ **1. Adjacency Smoothing**  
Adjacency smoothing resolves **semantic‑adjacent relationships** that are present but structurally discontinuous.

#### **Example**
Input residue:
```
residue: ['interrogative_scope', 'state_adjacent']
```

SmOB applies adjacency smoothing:
```
smoothing_operations: ['adjacency_smoothing']
semantic_adjacent_cues: ['interrogative_scope', 'state_adjacent']
smoothing_residue: []
```

#### **Interpretation**
SmOB recognizes that:

- `interrogative_scope` is adjacent to the main clause  
- `state_adjacent` is adjacent to the predicate  

Both cues are valid and stable → no leftover residue.

---

### ⭐ **2. Continuity Smoothing**  
Continuity smoothing resolves **breaks in semantic continuity**, especially modality and underspecification.

#### **Example**
Input residue:
```
residue: ['modality_cue', 'underspecification_adjacent']
```

SmOB applies continuity smoothing:
```
smoothing_operations: ['continuity_smoothing']
semantic_adjacent_cues: ['modality_cue']
smoothing_residue: ['underspecification_adjacent']
```

#### **Interpretation**
SmOB stabilizes:

- `modality_cue` (“might”, “could”, “should”) → extractable  
- `underspecification_adjacent` (“something”, “somewhere”) → still unresolved → becomes smoothing_residue

This is a **classic basin split**: one cue extracted, one left unresolved.

---

### ⭐ **3. Role‑Alignment Smoothing**  
Role smoothing resolves mismatches between segment roles and semantic adjacency.

### **Example**
Input residue:
```
residue: ['modifier_chain']
```

SmOB applies role smoothing:
```
smoothing_operations: ['role_smoothing']
semantic_adjacent_cues: ['modifier_chain']
smoothing_residue: []
```

#### **Interpretation**
SmOB stabilizes the modifier chain:

- “the rain **in Spain**”  
- “the book **on the table**”  

Role alignment is clean → no leftover residue.

---

### ⭐ **4. Segment‑Alignment Smoothing**  
Segment smoothing resolves adjacency between segments that are structurally separated but semantically linked.

#### **Example**
Input residue:
```
residue: ['locative_adjacent']
```

SmOB applies segment smoothing:
```
smoothing_operations: ['segment_smoothing']
semantic_adjacent_cues: ['locative_adjacent']
smoothing_residue: []
```

#### **Interpretation**
SmOB stabilizes:

- NP → LOC adjacency  
- “the book” → “on the table”  
- “the rain” → “in the plain”

Segment alignment is clean → no leftover residue.

---

### ⭐ **5. Basin Compression Smoothing**  
This is the “catch‑all” smoothing type used when residue is mixed or ambiguous.

### **Example**
Input residue:
```
residue: ['conflict_adjacent', 'modality_cue', 'underspecification_adjacent']
```

SmOB applies basin compression smoothing:
```
smoothing_operations: ['basin_compression_smoothing']
semantic_adjacent_cues: ['modality_cue', 'conflict_adjacent']
smoothing_residue: ['underspecification_adjacent']
```

#### **Interpretation**
SmOB extracts:

- `modality_cue` (“might”, “could”)  
- `conflict_adjacent` (“but”, “however”)  

But leaves:

- `underspecification_adjacent` (“something”, “somewhere”)  

This is the most common multi‑cue basin pattern.

---

## ⭐ **A.4.2 Summary Table of Smoothing Types and Examples**

| Smoothing Type | Example Input | Extracted Cues | Smoothing Residue |
|----------------|---------------|----------------|-------------------|
| adjacency_smoothing | `['interrogative_scope', 'state_adjacent']` | both cues | none |
| continuity_smoothing | `['modality_cue', 'underspecification_adjacent']` | modality only | underspecification |
| role_smoothing | `['modifier_chain']` | modifier_chain | none |
| segment_smoothing | `['locative_adjacent']` | locative_adjacent | none |
| basin_compression_smoothing | `['conflict_adjacent','modality_cue','underspecification_adjacent']` | conflict + modality | underspecification |

---

# **A.5 Summary**

- **Smoothing** = basin‑level stabilization  
- **Adjacency** = semantic‑adjacent relationships SmOB extracts  
- **Smoothing_residue** = leftover material after SmOB’s basin operations  

SmOB is the **Semantic Object Basin**, not a semantic interpreter.  
Its job is to produce a **deterministic pre‑semantic representation** for IdOB and the Thought Router.

---



# **idob_sufficiency.md**  
### *Information Sufficiency for Identity Formation in Path‑A*

## **1. Overview**

IdOB (Identity Observation Block) is the final primitive in the Path‑A short simulator chain:

```
SOB → SROB → CnOB → SmOB → IdOB
```

Its purpose is to determine whether the simulator has **enough structural, relational, and semantic information** to form a coherent **identity packet** and interpret meaning deterministically.

This document defines the **sufficiency conditions** for IdOB, the **failure modes**, and the **diagnostic process** used to determine whether meaning is **deterministic** or **probabilistic**.

---

## **2. Core Principle**

Path‑A is a deterministic thought simulator.  
Meaning is not guessed — it is **constructed**.

IdOB sufficiency follows a simple rule:

> **If everything is assigned, meaning is deterministic.  
> If anything is unassigned, meaning is probabilistic.**

“Assigned” means:

- segments recognized  
- tokens known  
- roles assigned  
- constraints matched  
- smoothing cues resolved  
- semantic core fields fillable  
- truth relation determinable  

If any of these fail, IdOB cannot form identity deterministically.

---

## **3. Upstream Sufficiency Conditions**

IdOB depends on the successful output of all upstream primitives.

### **3.1 SOB Sufficiency (Structural Segmentation)**  
IdOB requires:

- at least one segment  
- all segment tokens known in `input_dictionary.yaml`  
- each segment matching a pattern in `segment_patterns.yaml`  

If segmentation fails, IdOB cannot proceed.

---

### **3.2 SROB Sufficiency (Role Assignment)**  
IdOB requires:

- each segment assigned a role or explicitly marked `none`  
- any non‑`none` role matching `role_patterns.yaml`  

If roles cannot be assigned, identity cannot propagate.

---

### **3.3 CnOB Sufficiency (Constraint Matching)**  
IdOB requires:

- at least one matched constraint  
- residue not containing contradictions  
- constraint geometry satisfied  

If constraints fail, semantic core cannot be formed.

---

### **3.4 SmOB Sufficiency (Smoothing & Adjacency)**  
IdOB requires:

- smoothing operations applied or explicitly no‑op  
- semantic adjacency cues present when expected  
- smoothing residue not blocking identity formation  
- a candidate truth relation (e.g., `interrogative_open`)  

If smoothing fails, identity cannot be harmonized.

---

## **4. IdOB Internal Sufficiency Conditions**

Once upstream primitives succeed, IdOB must satisfy:

### **4.1 Selected Operations**
`selected_ops` must be non‑empty and consistent with upstream geometry.  
Examples:

- `query_resolution`  
- `interrogative_identity_request`  
- `modifier_resolution`

---

### **4.2 Truth Relation**
IdOB must determine a `truth_relation`, even if it is:

- `interrogative_open`  
- `unknown`  
- `contradiction`  

Truth relation is required for identity formation.

---

### **4.3 Minimal Semantic Core**
At least one of the following must be determinable:

- `query_focus`  
- `predicate`  
- `theme`  
- `agent`  
- `patient`  

Empty‑but‑valid fields are allowed.  
Empty‑and‑invalid fields are not.

---

### **4.4 Identity Packet Coherence**
The identity packet must:

- reference only known segments/roles/tokens  
- not contradict upstream constraints  
- satisfy identity geometry  
- maintain referential consistency  

If coherence fails, IdOB is insufficient.

---

## **5. Deterministic vs Probabilistic Meaning**

### **Deterministic Meaning (IdOB sufficient)**  
Occurs when:

- all upstream primitives succeed  
- semantic core can be formed  
- truth relation can be assigned  
- identity packet is coherent  

### **Probabilistic Meaning (IdOB insufficient)**  
Occurs when:

- any upstream primitive fails  
- semantic core cannot be formed  
- truth relation cannot be determined  
- identity packet is incoherent  

Probabilistic meaning is logged for post‑processing.

---

## **6. Failure Diagnostics**

When IdOB is insufficient, the simulator produces a structured failure report:

```yaml
idob_failure:
  sufficient: false
  stage_of_failure: "CnOB"
  reasons:
    - "No constraints matched."
    - "Unknown token 'quargle'."
  missing_information:
    structural:
      - "No NP segment for theme."
    roles:
      - "No agent role assigned."
    constraints:
      - "query-focus-predicate not matched."
    semantic_core:
      - "predicate empty."
  suggested_actions:
    - "Add missing tokens to input_dictionary.yaml."
    - "Extend segment_patterns.yaml for new NP forms."
    - "Update role_patterns.yaml for agent/theme roles."
```

This failure file is used by post‑processing scripts to propose controlled updates to dictionaries and patterns.

---

## **7. Controlled Dictionary & Pattern Evolution**

IdOB insufficiency is the mechanism by which Path‑A evolves:

1. **Random sentences** are run through the simulator.  
2. **Failures** are logged with reasons.  
3. **Post‑processing** uses dictionary libraries to classify unknown tokens.  
4. **Candidate updates** are generated for:
   - `input_dictionary.yaml`  
   - `segment_patterns.yaml`  
   - `role_patterns.yaml`  
   - constraint dictionaries  
5. **Human review** approves updates.  
6. **Testbenches** validate updates.  
7. **Canonical YAML artifacts** are updated deterministically.

This preserves reproducibility, determinism, and cross‑language compatibility.

---

## **8. Summary**

IdOB sufficiency is the formal test of whether Path‑A has enough information to interpret meaning deterministically.

It is the boundary between:

- **deterministic identity formation**  
- **probabilistic meaning inference**

This specification defines:

- the sufficiency conditions  
- the failure modes  
- the diagnostic process  
- the controlled evolution loop  

It is a foundational part of Path‑A’s architecture and a key component of its theoretical framework.

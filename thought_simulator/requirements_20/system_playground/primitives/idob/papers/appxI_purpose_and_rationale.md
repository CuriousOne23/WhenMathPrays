# **Appendix I — How A × B Drives Identity Geometry**  
### *The Deterministic Interaction Between Meaning Coupling and Identity Structure*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix I explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **identity geometry**, the structured identity representation maintained by IdOB.

This appendix shows:

- how A (stated content) influences identity geometry  
- how B (context) influences identity geometry  
- how IdOB refines identity geometry  
- how identity geometry appears in TP metadata  
- how identity geometry drives continuity, routing, semantic‑importance, and next‑turn context  
- how identity geometry stabilizes meaning  
- how identity geometry prevents identity drift  
- how identity geometry interacts with residues and CCR alignment  

Identity geometry is the **identity backbone** of TS.

---

# **2. What Identity Geometry Is**

Identity geometry is defined in IdOB’s internal model:

```
idob_geometry: {
    neighborhood: string,
    k_id: string
}
```

### **Identity geometry is:**

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Identity geometry is the **structured representation of identity** inside TS.

It answers:

- *Where does the speaker’s identity sit in the semantic landscape?*  
- *How stable is the speaker’s identity?*  
- *How does identity relate to the current meaning?*  
- *How does identity relate to prior turns?*  
- *How does identity relate to residues and routing?*  

Identity geometry is the **identity map** of the conversation.

---

# **3. Components of Identity Geometry**

Identity geometry has two canonical components:

### **3.1 neighborhood**  
The identity neighborhood represents the **identity region** the speaker occupies.

Examples:

- `identity_defense`  
- `identity_alignment`  
- `identity_neutral`  
- `identity_conflict`  
- `identity_transition`  
- `identity_correction`  
- `identity_stable_core`  

### **3.2 k_id (identity kernel)**  
The identity kernel represents the **core identity state**:

Examples:

- `stable_core`  
- `drifting_core`  
- `threatened_core`  
- `corrective_core`  
- `expanding_core`  
- `contracting_core`  

Identity geometry is the **identity coordinate system** IdOB maintains.

---

# **4. How “What Is Stated” (A) Drives Identity Geometry**

A influences identity geometry through:

### **4.1 Identity‑relevant propositions**
Statements about:

- self  
- beliefs  
- commitments  
- knowledge  
- corrections  
- denials  
- clarifications  

These shift identity geometry.

Example:  
“I didn’t say that” → identity neighborhood moves toward **identity_defense**.

---

### **4.2 Expression markers**
Negation, correction, emphasis, hedging influence:

- neighborhood  
- k_id  

Example:  
“That’s not what I meant” → identity kernel moves toward **corrective_core**.

---

### **4.3 Semantic residues**
Residues from OB‑Set influence identity geometry:

- contradiction → identity_defense  
- correction → identity_correction  
- planning → identity_alignment  
- affirmation → identity_neutral  

---

### **4.4 Propositional skeleton**
The subject–verb–object structure determines:

- whether identity is implicated  
- whether identity is stable or threatened  

Example:  
“You said X” → identity geometry shifts toward **identity_conflict**.

---

# **5. How “Context” (B) Drives Identity Geometry**

B influences identity geometry through:

### **5.1 Identity continuity**
If identity continuity is stable:

- neighborhood = identity_stable_core  

If identity continuity is unstable:

- neighborhood = identity_transition  

---

### **5.2 Referent continuity**
If referent affects identity:

- k_id = threatened_core  

If referent is stable:

- k_id = stable_core  

---

### **5.3 CCR alignment**
If CCR alignment indicates identity conflict:

- neighborhood = identity_conflict  
- k_id = threatened_core  

If CCR alignment indicates identity alignment:

- neighborhood = identity_alignment  
- k_id = stable_core  

---

### **5.4 Routing regime**
If RB indicates:

- Transition → identity_transition  
- Collapse → identity_conflict  
- Drift → identity_correction  
- Refinement → identity_alignment  
- Stable → identity_neutral  

---

### **5.5 Entropy trajectory**
High entropy → identity geometry becomes unstable.  
Low entropy → identity geometry stabilizes.

---

### **5.6 Freeze signatures**
Freeze signatures indicate:

- identity locks  
- identity commitments  

These stabilize identity geometry.

---

# **6. How IdOB Refines Identity Geometry**

IdOB is the **only primitive** that refines identity geometry.

IdOB refines identity geometry by:

### **6.1 Interpreting identity‑relevant content**
If A expresses identity correction:

- neighborhood = identity_correction  
- k_id = corrective_core  

If A expresses identity defense:

- neighborhood = identity_defense  
- k_id = threatened_core  

---

### **6.2 Interpreting identity continuity**
If identity continuity is stable:

- k_id = stable_core  

If identity continuity is unstable:

- k_id = drifting_core  

---

### **6.3 Interpreting referent continuity**
If referent affects identity:

- neighborhood = identity_defense  
- k_id = threatened_core  

---

### **6.4 Interpreting residues**
Residues influence identity geometry:

- contradiction → identity_conflict  
- correction → identity_correction  
- planning → identity_alignment  
- affirmation → identity_neutral  

---

### **6.5 Interpreting CCR alignment**
If CCR alignment indicates identity conflict:

- neighborhood = identity_conflict  
- k_id = threatened_core  

If CCR alignment indicates identity alignment:

- neighborhood = identity_alignment  
- k_id = stable_core  

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- neighborhood = identity_transition  

If RB indicates large displacement:

- k_id = drifting_core  

IdOB produces a **canonical identity geometry object**.

---

# **7. How Identity Geometry Appears in TP Metadata**

Identity geometry appears in:

```
TP.metadata.identity.geometry.neighborhood
TP.metadata.identity.geometry.k_id
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Identity geometry is the **identity map** stored in the TP.

---

# **8. How Identity Geometry Drives Continuity**

Identity geometry influences:

- identity continuity  
- referent continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

If identity geometry indicates:

- identity_conflict → continuity_next = correction  
- identity_alignment → continuity_next = continuation  
- identity_transition → continuity_next = stabilization  

Identity geometry is the **continuity anchor**.

---

# **9. How Identity Geometry Drives Routing (RB)**

RB uses identity geometry to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

If identity geometry indicates:

- identity_conflict → RB escalates  
- identity_alignment → RB stabilizes  
- identity_transition → RB enters Transition regime  

Identity geometry is the **routing anchor**.

---

# **10. Worked Example — Identity Geometry in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- neighborhood = identity_defense  
- k_id = corrective_core  

### **Identity geometry entry:**

```
idob_geometry: {
    neighborhood: identity_defense,
    k_id: corrective_core
}
```

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Identity geometry becomes the **semantic and cognitive anchor** for the next turn.

---

# **11. Summary**

Appendix I shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- identity neighborhood  
- identity kernel  
- identity continuity  
- identity stability  
- identity roles  
- identity refinement  
- identity‑conditioned meaning  
- identity‑conditioned routing  
- identity‑conditioned continuity  

Identity geometry is the **identity backbone** of TS.  
It is the invariant that stabilizes identity across turns and ensures:

- meaning stability  
- routing stability  
- continuity stability  
- replay determinism  

Identity geometry is the **identity map** of TS.

---

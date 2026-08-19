# **Appendix T — How A × B Drives Coherence Geometry**  
### *The Deterministic Interaction Between Meaning Coupling and Semantic Fit*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix T explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **coherence geometry**, the invariant that determines:

- whether the turn fits the conversation  
- whether the turn disrupts the conversation  
- whether the turn aligns with identity  
- whether the turn aligns with topic  
- whether the turn aligns with referents  
- whether the turn aligns with continuity  
- whether the turn aligns with routing  

Coherence geometry is the **semantic fit engine** of TS.

---

# **2. What Coherence Geometry Is**

Coherence geometry is defined internally in IdOB:

```
coherence_geometry: {
    neighborhood: string,
    k_coh: string
}
```

Coherence geometry is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Coherence geometry answers:

- *Does this turn fit the conversation?*  
- *Is the turn aligned or misaligned?*  
- *Is the turn coherent or incoherent?*  
- *Is the turn stabilizing or destabilizing?*

Coherence geometry is the **semantic alignment map** of TS.

---

# **3. Components of Coherence Geometry**

Coherence geometry has two canonical components:

### **3.1 neighborhood**  
The coherence neighborhood represents the **coherence region** the turn occupies.

Examples:

- `coh_continuation`  
- `coh_refinement`  
- `coh_drift`  
- `coh_transition`  
- `coh_conflict`  
- `coh_correction`  
- `coh_collapse`  

### **3.2 k_coh (coherence kernel)**  
The coherence kernel represents the **core coherence state**:

Examples:

- `stable_core`  
- `drifting_core`  
- `corrective_core`  
- `conflicted_core`  
- `expanding_core`  
- `contracting_core`  

Coherence geometry is the **semantic fit coordinate system** IdOB maintains.

---

# **4. How “What Is Stated” (A) Drives Coherence Geometry**

A influences coherence geometry through:

### **4.1 Coherence‑relevant propositions**
Statements that:

- contradict prior meaning  
- correct prior meaning  
- refine prior meaning  
- collapse prior meaning  
- affirm prior meaning  

produce coherence geometry shifts.

Example:  
“That’s not what I meant” → `coh_correction`.

---

### **4.2 Expression markers**
Negation, correction, emphasis, hedging influence:

- neighborhood  
- k_coh  

Example:  
“I never said that” → `coh_conflict`.

---

### **4.3 Semantic residues**
Residues from OB‑Set influence coherence geometry:

- contradiction → `coh_conflict`  
- correction → `coh_correction`  
- planning → `coh_refinement`  
- affirmation → `coh_continuation`  

---

### **4.4 Propositional skeleton**
The subject–verb–object structure determines:

- whether coherence is implicated  
- whether coherence is stable or threatened  

Example:  
“You said X” → `coh_transition`.

A is the **coherence trigger**.

---

# **5. How “Context” (B) Drives Coherence Geometry**

B influences coherence geometry through:

### **5.1 Continuity**
If continuity is unstable:

- neighborhood = coh_drift  

If continuity is stable:

- neighborhood = coh_continuation  

---

### **5.2 Identity continuity**
If identity is threatened:

- neighborhood = coh_conflict  

Identity pressure destabilizes coherence.

---

### **5.3 Referent continuity**
If referent is ambiguous:

- neighborhood = coh_correction  

Referent pressure destabilizes coherence.

---

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- neighborhood = coh_conflict  

If CCR alignment indicates alignment:

- neighborhood = coh_refinement  

---

### **5.5 Routing regime**
If RB indicates:

- Transition → coh_transition  
- Collapse → coh_collapse  
- Drift → coh_drift  
- Refinement → coh_refinement  
- Stable → coh_continuation  

---

### **5.6 Curvature**
High curvature → coh_conflict or coh_transition.  
Low curvature → coh_continuation or coh_refinement.

---

### **5.7 Entropy trajectory**
High entropy → coherence instability.  
Low entropy → coherence stability.

---

### **5.8 Freeze signatures**
Freeze signatures indicate:

- coherence locks  
- coherence constraints  

These produce:

- coh_correction  
- coh_stabilization  

B is the **coherence lens**.

---

# **6. How IdOB Refines Coherence Geometry**

IdOB is the **only primitive** that refines coherence geometry.

IdOB refines coherence geometry by:

### **6.1 Interpreting coherence‑relevant content**
If A expresses correction:

- neighborhood = coh_correction  
- k_coh = corrective_core  

If A expresses contradiction:

- neighborhood = coh_conflict  
- k_coh = conflicted_core  

---

### **6.2 Interpreting continuity**
If continuity is stable:

- k_coh = stable_core  

If continuity is unstable:

- k_coh = drifting_core  

---

### **6.3 Interpreting referents**
If referent affects coherence:

- neighborhood = coh_correction  

---

### **6.4 Interpreting residues**
Residues influence coherence geometry:

- contradiction → coh_conflict  
- correction → coh_correction  
- planning → coh_refinement  
- affirmation → coh_continuation  

---

### **6.5 Interpreting CCR alignment**
If CCR alignment indicates coherence conflict:

- neighborhood = coh_conflict  

If CCR alignment indicates coherence alignment:

- neighborhood = coh_refinement  

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- neighborhood = coh_transition  

If RB indicates large displacement:

- k_coh = drifting_core  

IdOB produces a **canonical coherence geometry object**.

---

# **7. How Coherence Geometry Appears in TP Metadata**

Coherence geometry appears in:

```
TP.metadata.coherence.geometry.neighborhood
TP.metadata.coherence.geometry.k_coh
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Coherence geometry is the **semantic fit record** stored in the TP.

---

# **8. How Coherence Geometry Drives Continuity**

Coherence geometry influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- coh_conflict → continuity correction  
- coh_correction → continuity correction  
- coh_refinement → continuity refinement  
- coh_continuation → continuity continuation  

Coherence geometry is the **continuity anchor**.

---

# **9. How Coherence Geometry Drives Routing (RB)**

RB uses coherence geometry to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

Examples:

- coh_conflict → Transition or Collapse  
- coh_correction → Drift or Transition  
- coh_refinement → Refinement  
- coh_continuation → Stable  

Coherence geometry is the **routing anchor**.

---

# **10. Worked Example — Coherence Geometry in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

```
coherence_geometry: {
    neighborhood: coh_correction,
    k_coh: corrective_core
}
```

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Coherence geometry becomes the **semantic fit anchor** for the next turn.

---

# **11. Summary**

Appendix T shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- coh_continuation  
- coh_refinement  
- coh_drift  
- coh_transition  
- coh_conflict  
- coh_correction  
- coh_collapse  

Coherence geometry is the **semantic fit engine** of TS.  
It ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Coherence geometry is the **semantic alignment backbone** of TS.

---

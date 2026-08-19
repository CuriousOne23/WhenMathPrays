# **Appendix V — How A × B Drives Continuity Geometry**  
### *The Deterministic Interaction Between Meaning Coupling and Temporal Stability*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix V explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **continuity geometry**, the invariant that determines:

- how stable the conversation is  
- how meaning is evolving across turns  
- whether continuity is stable, drifting, correcting, collapsing, or transitioning  
- how continuity interacts with identity, topic, referents, coherence, routing, and commit  
- how continuity shapes next‑turn context  

Continuity geometry is the **temporal stability engine** of TS.

---

# **2. What Continuity Geometry Is**

Continuity geometry is defined internally in IdOB:

```
continuity_geometry: {
    neighborhood: string,
    k_cont: string
}
```

Continuity geometry is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Continuity geometry answers:

- *Is the conversation stable?*  
- *Is the conversation drifting?*  
- *Is the conversation correcting?*  
- *Is the conversation collapsing?*  
- *Is the conversation transitioning?*

Continuity geometry is the **temporal map** of TS.

---

# **3. Components of Continuity Geometry**

Continuity geometry has two canonical components:

### **3.1 neighborhood**  
The continuity neighborhood represents the **temporal region** the conversation occupies.

Examples:

- `cont_continuation`  
- `cont_refinement`  
- `cont_drift`  
- `cont_transition`  
- `cont_conflict`  
- `cont_correction`  
- `cont_collapse`  

### **3.2 k_cont (continuity kernel)**  
The continuity kernel represents the **core continuity state**:

Examples:

- `stable_core`  
- `drifting_core`  
- `corrective_core`  
- `conflicted_core`  
- `expanding_core`  
- `contracting_core`  

Continuity geometry is the **temporal coordinate system** IdOB maintains.

---

# **4. How “What Is Stated” (A) Drives Continuity Geometry**

A influences continuity geometry through:

### **4.1 Continuity‑relevant propositions**
Statements that:

- contradict prior meaning  
- correct prior meaning  
- refine prior meaning  
- collapse prior meaning  
- affirm prior meaning  

produce continuity shifts.

Example:  
“That’s not what I meant” → `cont_correction`.

---

### **4.2 Expression markers**
Negation, correction, emphasis, hedging influence:

- neighborhood  
- k_cont  

Example:  
“I never said that” → `cont_conflict`.

---

### **4.3 Semantic residues**
Residues from OB‑Set influence continuity geometry:

- contradiction → `cont_conflict`  
- correction → `cont_correction`  
- planning → `cont_refinement`  
- affirmation → `cont_continuation`  

---

### **4.4 Propositional skeleton**
The subject–verb–object structure determines:

- whether continuity is implicated  
- whether continuity is stable or threatened  

Example:  
“You said X” → `cont_transition`.

A is the **continuity trigger**.

---

# **5. How “Context” (B) Drives Continuity Geometry**

B influences continuity geometry through:

### **5.1 Topic continuity**
If topic continuity is unstable:

- neighborhood = cont_drift  

If topic continuity is stable:

- neighborhood = cont_continuation  

---

### **5.2 Identity continuity**
If identity is threatened:

- neighborhood = cont_conflict  

Identity pressure destabilizes continuity.

---

### **5.3 Referent continuity**
If referent is ambiguous:

- neighborhood = cont_correction  

Referent pressure destabilizes continuity.

---

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- neighborhood = cont_conflict  

If CCR alignment indicates alignment:

- neighborhood = cont_refinement  

---

### **5.5 Routing regime**
If RB indicates:

- Transition → cont_transition  
- Collapse → cont_collapse  
- Drift → cont_drift  
- Refinement → cont_refinement  
- Stable → cont_continuation  

---

### **5.6 Curvature**
High curvature → cont_conflict or cont_transition.  
Low curvature → cont_continuation or cont_refinement.

---

### **5.7 Entropy trajectory**
High entropy → continuity instability.  
Low entropy → continuity stability.

---

### **5.8 Freeze signatures**
Freeze signatures indicate:

- continuity locks  
- continuity constraints  

These produce:

- cont_correction  
- cont_stabilization  

B is the **continuity lens**.

---

# **6. How IdOB Refines Continuity Geometry**

IdOB is the **only primitive** that refines continuity geometry.

IdOB refines continuity geometry by:

### **6.1 Interpreting continuity‑relevant content**
If A expresses correction:

- neighborhood = cont_correction  
- k_cont = corrective_core  

If A expresses contradiction:

- neighborhood = cont_conflict  
- k_cont = conflicted_core  

---

### **6.2 Interpreting continuity stability**
If continuity is stable:

- k_cont = stable_core  

If continuity is unstable:

- k_cont = drifting_core  

---

### **6.3 Interpreting referents**
If referent affects continuity:

- neighborhood = cont_correction  

---

### **6.4 Interpreting residues**
Residues influence continuity geometry:

- contradiction → cont_conflict  
- correction → cont_correction  
- planning → cont_refinement  
- affirmation → cont_continuation  

---

### **6.5 Interpreting CCR alignment**
If CCR alignment indicates continuity conflict:

- neighborhood = cont_conflict  

If CCR alignment indicates continuity alignment:

- neighborhood = cont_refinement  

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- neighborhood = cont_transition  

If RB indicates large displacement:

- k_cont = drifting_core  

IdOB produces a **canonical continuity geometry object**.

---

# **7. How Continuity Geometry Appears in TP Metadata**

Continuity geometry appears in:

```
TP.metadata.continuity.geometry.neighborhood
TP.metadata.continuity.geometry.k_cont
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Continuity geometry is the **temporal stability record** stored in the TP.

---

# **8. How Continuity Geometry Drives Continuity**

Continuity geometry influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- cont_conflict → continuity correction  
- cont_correction → continuity correction  
- cont_refinement → continuity refinement  
- cont_continuation → continuity continuation  

Continuity geometry is the **continuity anchor**.

---

# **9. How Continuity Geometry Drives Routing (RB)**

RB uses continuity geometry to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

Examples:

- cont_conflict → Transition or Collapse  
- cont_correction → Drift or Transition  
- cont_refinement → Refinement  
- cont_continuation → Stable  

Continuity geometry is the **routing anchor**.

---

# **10. Worked Example — Continuity Geometry in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

```
continuity_geometry: {
    neighborhood: cont_correction,
    k_cont: corrective_core
}
```

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Continuity geometry becomes the **temporal anchor** for the next turn.

---

# **11. Summary**

Appendix V shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- cont_continuation  
- cont_refinement  
- cont_drift  
- cont_transition  
- cont_conflict  
- cont_correction  
- cont_collapse  

Continuity geometry is the **temporal stability engine** of TS.  
It ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Continuity geometry is the **temporal backbone** of TS.

---

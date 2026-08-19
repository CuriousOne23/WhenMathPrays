# **Appendix L — How A × B Drives Routing Curvature**  
### *The Geometric Interaction Between Meaning Coupling and Routing Stability*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix L explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **routing curvature**, the invariant RB uses to detect:

- semantic instability  
- identity instability  
- referent instability  
- continuity instability  
- routing instability  

Curvature is the **geometric measure** of how meaning bends across turns.

This appendix shows:

- how A (stated content) influences curvature  
- how B (context) influences curvature  
- how IdOB refines curvature  
- how curvature appears in TP metadata  
- how curvature drives routing, continuity, identity, and commit  
- how curvature interacts with entropy trajectory  
- how curvature interacts with freeze signatures  

Curvature is the **semantic geometry** of TS.

---

# **2. What Routing Curvature Is**

Routing curvature is defined in RB‑prm:

```
TP.metadata.routing.curvature: number
```

Curvature is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Curvature measures **how sharply meaning bends** between turns.

High curvature → instability.  
Low curvature → stability.

Curvature is the **semantic slope** RB uses to classify routing pressure.

---

# **3. Why Curvature Exists**

Curvature exists because:

1. Meaning changes across turns.  
2. Some changes are smooth.  
3. Some changes are sharp.  
4. Sharp changes indicate semantic pressure.  
5. Semantic pressure must be detected early.  
6. Routing must respond to pressure.  
7. Commit must be blocked during pressure.  
8. Identity must be stabilized during pressure.  
9. Continuity must be stabilized during pressure.  
10. Replay determinism requires curvature tracking.

Curvature is the **early‑warning system** of TS.

---

# **4. How “What Is Stated” (A) Drives Curvature**

A influences curvature through:

### **4.1 Contradiction**
If A contradicts prior meaning:

- curvature ↑↑  

### **4.2 Correction**
If A corrects prior meaning:

- curvature ↑  

### **4.3 Identity‑relevant content**
If A affects identity:

- curvature ↑↑↑  

### **4.4 Referent placeholders**
If A introduces ambiguous referents:

- curvature ↑  

### **4.5 Expression markers**
Negation, emphasis, hedging influence curvature:

- negation → curvature ↑  
- emphasis → curvature ↑  
- hedging → curvature ↔  

### **4.6 Semantic residues**
Residues from OB‑Set influence curvature:

- contradiction → curvature ↑↑  
- correction → curvature ↑  
- planning → curvature ↔  
- affirmation → curvature ↓  

A is the **semantic force** that bends the meaning trajectory.

---

# **5. How “Context” (B) Drives Curvature**

B influences curvature through:

### **5.1 Continuity**
If continuity is unstable:

- curvature ↑  

If continuity is stable:

- curvature ↓  

---

### **5.2 Identity continuity**
If identity is threatened:

- curvature ↑↑↑  

If identity is stable:

- curvature ↓  

---

### **5.3 Referent continuity**
If referent is ambiguous:

- curvature ↑  

If referent is stable:

- curvature ↓  

---

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- curvature ↑↑  

If CCR alignment indicates alignment:

- curvature ↓  

---

### **5.5 Routing regime**
If RB indicates:

- Transition → curvature ↑↑  
- Collapse → curvature ↑↑↑  
- Drift → curvature ↑  
- Refinement → curvature ↓  
- Stable → curvature ↓↓  

---

### **5.6 Entropy trajectory**
High entropy → curvature ↑↑  
Low entropy → curvature ↓↓

Entropy and curvature are **dual measures** of instability.

---

### **5.7 Freeze signatures**
Freeze signatures indicate:

- semantic locks  
- identity locks  
- referent locks  

These increase curvature because they indicate instability.

B is the **semantic lens** that determines how sharply meaning bends.

---

# **6. How IdOB Refines Curvature**

IdOB is the **only primitive** that refines curvature.

IdOB refines curvature by:

### **6.1 Interpreting identity**
If identity is threatened:

- curvature ↑↑↑  

If identity is stable:

- curvature ↓  

---

### **6.2 Interpreting referents**
If referent is ambiguous:

- curvature ↑  

If referent is stable:

- curvature ↓  

---

### **6.3 Interpreting continuity**
If continuity is unstable:

- curvature ↑  

If continuity is stable:

- curvature ↓  

---

### **6.4 Interpreting residues**
Residues influence curvature:

- contradiction → curvature ↑↑  
- correction → curvature ↑  
- planning → curvature ↔  
- affirmation → curvature ↓  

---

### **6.5 Interpreting semantic‑importance**
High importance → curvature ↑  
Low importance → curvature ↓  

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- curvature ↑  

If RB indicates large displacement:

- curvature ↑↑  

IdOB produces a **canonical curvature value**.

---

# **7. How Curvature Appears in TP Metadata**

Curvature appears in:

```
TP.metadata.routing.curvature
```

This field is:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Curvature is the **routing geometry** stored in the TP.

---

# **8. How Curvature Drives Routing (RB)**

RB uses curvature to:

### **8.1 Escalate routing**
High curvature → RB escalates.

### **8.2 Stabilize routing**
Low curvature → RB stabilizes.

### **8.3 Classify adjacency**
High curvature → non‑local adjacency.  
Low curvature → local adjacency.

### **8.4 Compute displacement**
High curvature → large displacement.  
Low curvature → small displacement.

### **8.5 Emit regime hints**
High curvature → Transition or Collapse.  
Low curvature → Stable or Refinement.

Curvature is the **routing pressure gauge**.

---

# **9. How Curvature Drives Continuity**

Curvature influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

High curvature → continuity correction.  
Low curvature → continuity continuation.

Curvature is the **continuity pressure gauge**.

---

# **10. How Curvature Drives Identity**

Curvature influences:

- identity geometry  
- identity roles  
- identity stability  
- identity continuity  

High curvature → identity_defense.  
Low curvature → identity_neutral.

Curvature is the **identity pressure gauge**.

---

# **11. Worked Example — Curvature in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- curvature = high  
- identity geometry = identity_defense  
- residue = identity_conflict  
- continuity_next = correction  
- identity_next = defense  
- importance_next = high  

### **Effects:**

- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- commit blocked  
- IdOB cycle required  

Curvature becomes the **geometric indicator** of semantic instability.

---

# **12. Summary**

Appendix L shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- routing curvature  
- semantic instability  
- identity instability  
- referent instability  
- continuity instability  
- routing escalation  
- commit blocking  

Curvature is the **semantic geometry** of TS.  
It is the invariant that ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Curvature is the **semantic slope** of TS.

---

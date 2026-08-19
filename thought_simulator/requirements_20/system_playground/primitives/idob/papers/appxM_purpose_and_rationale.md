# **Appendix M — How A × B Drives Entropy Trajectory**  
### *The Temporal Interaction Between Meaning Coupling and Semantic Stability*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix M explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **entropy trajectory**, the invariant that measures:

- semantic stability  
- semantic drift  
- semantic conflict  
- semantic collapse  
- identity instability  
- referent instability  
- continuity instability  

Entropy trajectory is the **semantic stability meter** of TS.

This appendix shows:

- how A (stated content) influences entropy  
- how B (context) influences entropy  
- how IdOB refines entropy  
- how entropy appears in TP metadata  
- how entropy drives routing, continuity, identity, and commit  
- how entropy interacts with curvature  
- how entropy interacts with freeze signatures  

Entropy trajectory is the **semantic heartbeat** of TS.

---

# **2. What Entropy Trajectory Is**

Entropy trajectory is defined in RB‑prm and TP metadata:

```
TP.metadata.entropy.trajectory: number
TP.metadata.entropy.density: number
```

### **Entropy trajectory is:**

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Entropy trajectory measures **how meaning stability changes over time**.

High entropy → instability.  
Low entropy → stability.

Entropy trajectory is the **semantic trendline** RB uses to detect drift.

---

# **3. Why Entropy Trajectory Exists**

Entropy trajectory exists because:

1. Meaning changes across turns.  
2. Some changes are stable.  
3. Some changes drift.  
4. Some changes collapse.  
5. TS must detect drift early.  
6. TS must detect collapse immediately.  
7. Routing must respond to instability.  
8. Commit must be blocked during instability.  
9. Identity must be stabilized during instability.  
10. Replay determinism requires entropy tracking.

Entropy trajectory is the **semantic stability monitor** of TS.

---

# **4. How “What Is Stated” (A) Drives Entropy**

A influences entropy through:

### **4.1 Contradiction**
If A contradicts prior meaning:

- entropy ↑↑  

### **4.2 Correction**
If A corrects prior meaning:

- entropy ↑  

### **4.3 Identity‑relevant content**
If A affects identity:

- entropy ↑↑↑  

### **4.4 Referent placeholders**
If A introduces ambiguous referents:

- entropy ↑  

### **4.5 Expression markers**
Negation, emphasis, hedging influence entropy:

- negation → entropy ↑  
- emphasis → entropy ↑  
- hedging → entropy ↔  

### **4.6 Semantic residues**
Residues from OB‑Set influence entropy:

- contradiction → entropy ↑↑  
- correction → entropy ↑  
- planning → entropy ↔  
- affirmation → entropy ↓  

A is the **semantic force** that destabilizes or stabilizes meaning.

---

# **5. How “Context” (B) Drives Entropy**

B influences entropy through:

### **5.1 Continuity**
If continuity is unstable:

- entropy ↑  

If continuity is stable:

- entropy ↓  

---

### **5.2 Identity continuity**
If identity is threatened:

- entropy ↑↑↑  

If identity is stable:

- entropy ↓  

---

### **5.3 Referent continuity**
If referent is ambiguous:

- entropy ↑  

If referent is stable:

- entropy ↓  

---

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- entropy ↑↑  

If CCR alignment indicates alignment:

- entropy ↓  

---

### **5.5 Routing regime**
If RB indicates:

- Transition → entropy ↑↑  
- Collapse → entropy ↑↑↑  
- Drift → entropy ↑  
- Refinement → entropy ↓  
- Stable → entropy ↓↓  

---

### **5.6 Curvature**
High curvature → entropy ↑↑  
Low curvature → entropy ↓↓

Curvature and entropy are **dual measures** of instability.

---

### **5.7 Freeze signatures**
Freeze signatures indicate:

- semantic locks  
- identity locks  
- referent locks  

These increase entropy because they indicate instability.

B is the **semantic lens** that determines how meaning stability evolves.

---

# **6. How IdOB Refines Entropy**

IdOB is the **only primitive** that refines entropy.

IdOB refines entropy by:

### **6.1 Interpreting identity**
If identity is threatened:

- entropy ↑↑↑  

If identity is stable:

- entropy ↓  

---

### **6.2 Interpreting referents**
If referent is ambiguous:

- entropy ↑  

If referent is stable:

- entropy ↓  

---

### **6.3 Interpreting continuity**
If continuity is unstable:

- entropy ↑  

If continuity is stable:

- entropy ↓  

---

### **6.4 Interpreting residues**
Residues influence entropy:

- contradiction → entropy ↑↑  
- correction → entropy ↑  
- planning → entropy ↔  
- affirmation → entropy ↓  

---

### **6.5 Interpreting semantic‑importance**
High importance → entropy ↑  
Low importance → entropy ↓  

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- entropy ↑  

If RB indicates large displacement:

- entropy ↑↑  

IdOB produces a **canonical entropy trajectory value**.

---

# **7. How Entropy Appears in TP Metadata**

Entropy appears in:

```
TP.metadata.entropy.trajectory
TP.metadata.entropy.density
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Entropy trajectory is the **semantic stability record** stored in the TP.

---

# **8. How Entropy Drives Routing (RB)**

RB uses entropy to:

### **8.1 Escalate routing**
High entropy → RB escalates.

### **8.2 Stabilize routing**
Low entropy → RB stabilizes.

### **8.3 Classify adjacency**
High entropy → non‑local adjacency.  
Low entropy → local adjacency.

### **8.4 Compute displacement**
High entropy → large displacement.  
Low entropy → small displacement.

### **8.5 Emit regime hints**
High entropy → Transition or Collapse.  
Low entropy → Stable or Refinement.

Entropy is the **routing stability gauge**.

---

# **9. How Entropy Drives Continuity**

Entropy influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

High entropy → continuity correction.  
Low entropy → continuity continuation.

Entropy is the **continuity stability gauge**.

---

# **10. How Entropy Drives Identity**

Entropy influences:

- identity geometry  
- identity roles  
- identity stability  
- identity continuity  

High entropy → identity_defense.  
Low entropy → identity_neutral.

Entropy is the **identity stability gauge**.

---

# **11. Worked Example — Entropy in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- entropy ↑↑↑  
- curvature ↑↑  
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

Entropy trajectory becomes the **semantic instability trendline**.

---

# **12. Summary**

Appendix M shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- entropy trajectory  
- semantic instability  
- identity instability  
- referent instability  
- continuity instability  
- routing escalation  
- commit blocking  

Entropy trajectory is the **semantic heartbeat** of TS.  
It ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Entropy trajectory is the **semantic trendline** of TS.

---

# **Appendix W — How A × B Drives Displacement and Adjacency**  
### *The Deterministic Interaction Between Meaning Coupling and Routing Geometry*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix W explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces:

- **adjacency** — *how close the turn is to prior meaning*  
- **displacement** — *how far the turn moves from prior meaning*

These two invariants determine:

- routing regime  
- routing escalation  
- routing stabilization  
- continuity correction  
- continuity continuation  
- identity pressure  
- referent pressure  
- commit eligibility  

Adjacency and displacement are the **routing geometry engine** of TS.

---

# **2. What Adjacency and Displacement Are**

RB defines:

```
TP.metadata.routing.adjacency: "local" | "non_local"
TP.metadata.routing.displacement: "small" | "medium" | "large"
```

These invariants are:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

### **Adjacency = semantic proximity.**  
Is the turn close to prior meaning?

### **Displacement = semantic distance.**  
How far did the turn move?

Adjacency = *closeness*.  
Displacement = *distance*.

---

# **3. Why Adjacency and Displacement Exist**

Adjacency and displacement exist because:

1. Meaning moves across turns.  
2. Movement can be small or large.  
3. TS must detect movement deterministically.  
4. Movement determines routing regime.  
5. Movement determines continuity correction.  
6. Movement determines identity pressure.  
7. Movement determines referent pressure.  
8. Movement determines commit eligibility.  
9. Replay determinism requires geometric tracking.

Adjacency and displacement are the **semantic geometry backbone** of TS.

---

# **4. How “What Is Stated” (A) Drives Adjacency**

A influences adjacency through:

### **4.1 Contradiction**
Contradiction → **non_local adjacency**

### **4.2 Correction**
Correction → **non_local adjacency**

### **4.3 Identity‑relevant content**
Identity pressure → **non_local adjacency**

### **4.4 Referent placeholders**
Ambiguous referents → **non_local adjacency**

### **4.5 Affirmation**
Affirmation → **local adjacency**

### **4.6 Planning**
Planning → **local adjacency**

### **4.7 Hedging**
Hedging → **local adjacency**

A is the **adjacency trigger**.

---

# **5. How “What Is Stated” (A) Drives Displacement**

A influences displacement through:

### **5.1 Contradiction**
Contradiction → **large displacement**

### **5.2 Correction**
Correction → **medium displacement**

### **5.3 Identity‑relevant content**
Identity pressure → **large displacement**

### **5.4 Referent placeholders**
Referent ambiguity → **medium displacement**

### **5.5 Affirmation**
Affirmation → **small displacement**

### **5.6 Planning**
Planning → **small displacement**

A is the **displacement trigger**.

---

# **6. How “Context” (B) Drives Adjacency**

B influences adjacency through:

### **6.1 Continuity**
Unstable continuity → non_local  
Stable continuity → local  

---

### **6.2 Identity continuity**
Identity threat → non_local  
Identity stable → local  

---

### **6.3 Referent continuity**
Referent ambiguous → non_local  
Referent stable → local  

---

### **6.4 CCR alignment**
Conflict → non_local  
Alignment → local  

---

### **6.5 Routing regime**
Transition → non_local  
Collapse → non_local  
Drift → medium/local  
Refinement → local  
Stable → local  

---

### **6.6 Curvature**
High curvature → non_local  
Low curvature → local  

---

### **6.7 Entropy trajectory**
High entropy → non_local  
Low entropy → local  

---

### **6.8 Freeze signatures**
Freeze signatures → non_local  

B is the **adjacency lens**.

---

# **7. How “Context” (B) Drives Displacement**

B influences displacement through:

### **7.1 Continuity**
Unstable continuity → medium/large  
Stable continuity → small  

---

### **7.2 Identity continuity**
Identity threat → large  
Identity stable → small  

---

### **7.3 Referent continuity**
Referent ambiguous → medium  
Referent stable → small  

---

### **7.4 CCR alignment**
Conflict → large  
Alignment → small  

---

### **7.5 Routing curvature**
High curvature → large  
Low curvature → small  

---

### **7.6 Entropy trajectory**
High entropy → large  
Low entropy → small  

---

### **7.7 Freeze signatures**
Freeze signatures → large  

B is the **displacement lens**.

---

# **8. How IdOB Refines Adjacency and Displacement**

IdOB is the **only primitive** that refines adjacency and displacement.

IdOB refines adjacency by:

- interpreting identity geometry  
- interpreting topic geometry  
- interpreting referent continuity  
- interpreting coherence geometry  
- interpreting residues  
- interpreting continuity geometry  
- interpreting routing regime  

IdOB refines displacement by:

- interpreting curvature  
- interpreting entropy  
- interpreting identity pressure  
- interpreting referent pressure  
- interpreting semantic‑importance  
- interpreting routing adjacency  

IdOB produces:

```
adjacency
displacement
```

These are written into:

```
TP.metadata.routing
```

---

# **9. How Adjacency and Displacement Drive Routing (RB)**

RB uses adjacency and displacement to:

### **9.1 Determine regime**
- non_local + large → Transition or Collapse  
- non_local + medium → Drift or Transition  
- local + small → Stable or Refinement  

### **9.2 Escalate routing**
High displacement → escalate  
Low displacement → stabilize  

### **9.3 Classify adjacency**
Adjacency directly sets local vs non_local.

### **9.4 Compute displacement**
Displacement sets small/medium/large.

### **9.5 Block commit**
Non_local + large → commit blocked.

Adjacency + displacement = **routing geometry**.

---

# **10. How Adjacency and Displacement Drive Continuity**

Continuity_next is determined by:

- non_local → correction  
- local → continuation  

Displacement influences:

- large → correction  
- medium → refinement  
- small → continuation  

Adjacency + displacement = **continuity geometry input**.

---

# **11. Worked Example — Adjacency & Displacement in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- adjacency = non_local  
- displacement = large  

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- commit blocked  

Adjacency + displacement become the **routing geometry** for the next turn.

---

# **12. Summary**

Appendix W shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- adjacency (local vs non_local)  
- displacement (small, medium, large)  

Adjacency = *semantic proximity*.  
Displacement = *semantic distance*.

Together they ensure:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Adjacency and displacement are the **routing geometry backbone** of TS.

---

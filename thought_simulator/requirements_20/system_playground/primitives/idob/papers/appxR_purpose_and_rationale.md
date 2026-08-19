# **Appendix R — How A × B Drives Stance and Direction**  
### *The Deterministic Interaction Between Meaning Coupling and Semantic Motion*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix R explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **stance** and **direction**, the two invariants that describe:

- how meaning is moving  
- how identity is moving  
- how the topic is moving  
- how semantic pressure is applied  
- how continuity should respond  
- how routing should respond  
- how next‑turn context should be shaped  

Stance and direction are the **motion operators** of TS.

---

# **2. What Stance and Direction Are**

Stance and direction appear in:

```
TP.metadata.next_context_metadata.stance_next
TP.metadata.next_context_metadata.direction_next
```

They are:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

### **Stance = the speaker’s semantic posture.**  
Examples:

- corrective  
- clarifying  
- defensive  
- neutral  
- affirmative  
- planning  
- stabilizing  

### **Direction = the speaker’s semantic motion.**  
Examples:

- backward motion  
- forward motion  
- lateral motion  
- neutral motion  

Stance = *how the speaker is positioned*.  
Direction = *how the speaker is moving*.

---

# **3. Why Stance and Direction Exist**

Stance and direction exist because:

1. Meaning is not static.  
2. Meaning moves across turns.  
3. Movement must be tracked deterministically.  
4. Movement influences routing.  
5. Movement influences continuity.  
6. Movement influences identity.  
7. Movement influences topic geometry.  
8. Movement influences next‑turn context.  
9. Replay determinism requires motion invariants.

Stance and direction are the **semantic motion engine** of TS.

---

# **4. How “What Is Stated” (A) Drives Stance**

A influences stance through:

### **4.1 Contradiction**
If A contradicts prior meaning:

- stance = corrective  

### **4.2 Correction**
If A corrects prior meaning:

- stance = clarifying  

### **4.3 Identity‑relevant content**
If A affects identity:

- stance = defensive  

### **4.4 Affirmation**
If A affirms prior meaning:

- stance = affirmative  

### **4.5 Planning**
If A projects future meaning:

- stance = planning  

### **4.6 Hedging**
If A hedges:

- stance = stabilizing  

A is the **semantic posture trigger**.

---

# **5. How “What Is Stated” (A) Drives Direction**

A influences direction through:

### **5.1 Contradiction**
Contradiction pulls meaning **backward**:

- direction = backward motion  

### **5.2 Correction**
Correction also pulls meaning **backward**:

- direction = backward motion  

### **5.3 Planning**
Planning pushes meaning **forward**:

- direction = forward motion  

### **5.4 Affirmation**
Affirmation continues meaning **forward**:

- direction = forward motion  

### **5.5 Topic shift**
Topic shift produces **lateral motion**:

- direction = lateral motion  

A is the **semantic motion trigger**.

---

# **6. How “Context” (B) Drives Stance**

B influences stance through:

### **6.1 Continuity**
If continuity is unstable:

- stance = corrective  

If continuity is stable:

- stance = neutral  

---

### **6.2 Identity continuity**
If identity is threatened:

- stance = defensive  

If identity is stable:

- stance = affirmative  

---

### **6.3 Referent continuity**
If referent is ambiguous:

- stance = clarifying  

If referent is stable:

- stance = neutral  

---

### **6.4 CCR alignment**
If CCR alignment indicates conflict:

- stance = corrective  

If CCR alignment indicates alignment:

- stance = affirmative  

---

### **6.5 Routing regime**
If RB indicates:

- Transition → stance = corrective  
- Collapse → stance = defensive  
- Drift → stance = stabilizing  
- Refinement → stance = clarifying  
- Stable → stance = neutral  

---

### **6.6 Entropy trajectory**
High entropy → stance = corrective or defensive.  
Low entropy → stance = affirmative or neutral.

---

### **6.7 Freeze signatures**
Freeze signatures indicate:

- identity locks  
- semantic locks  
- referent locks  

These produce:

- stance = corrective or defensive  

B is the **semantic posture lens**.

---

# **7. How “Context” (B) Drives Direction**

B influences direction through:

### **7.1 Continuity**
If continuity is unstable:

- direction = backward motion  

If continuity is stable:

- direction = forward motion  

---

### **7.2 Identity continuity**
If identity is threatened:

- direction = backward motion  

If identity is stable:

- direction = forward motion  

---

### **7.3 Referent continuity**
If referent is ambiguous:

- direction = backward motion  

If referent is stable:

- direction = forward motion  

---

### **7.4 CCR alignment**
Conflict → backward motion.  
Alignment → forward motion.

---

### **7.5 Routing curvature**
High curvature → backward motion.  
Low curvature → forward motion.

---

### **7.6 Entropy trajectory**
High entropy → backward motion.  
Low entropy → forward motion.

---

### **7.7 Freeze signatures**
Freeze signatures → backward motion.

B is the **semantic motion lens**.

---

# **8. How IdOB Refines Stance and Direction**

IdOB is the **only primitive** that refines stance and direction.

IdOB refines stance by:

- interpreting identity geometry  
- interpreting topic geometry  
- interpreting residues  
- interpreting continuity  
- interpreting semantic‑importance  
- interpreting routing regime  

IdOB refines direction by:

- interpreting adjacency  
- interpreting displacement  
- interpreting curvature  
- interpreting entropy  
- interpreting identity pressure  
- interpreting referent pressure  

IdOB produces:

```
stance_next
direction_next
```

These are written by MCB into:

```
TP.metadata.next_context_metadata
```

---

# **9. How Stance and Direction Drive Routing (RB)**

RB uses stance and direction to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

Examples:

- corrective + backward → Transition  
- defensive + backward → Collapse  
- clarifying + forward → Refinement  
- affirmative + forward → Stable  

Stance and direction are the **routing motion operators**.

---

# **10. How Stance and Direction Drive Continuity**

Stance and direction influence:

- topic continuity  
- referent continuity  
- identity continuity  
- coherence continuity  

Examples:

- corrective + backward → continuity correction  
- clarifying + forward → continuity refinement  
- affirmative + forward → continuity continuation  

Stance and direction are the **continuity motion operators**.

---

# **11. Worked Example — Stance and Direction in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- stance_next = corrective  
- direction_next = backward_motion  

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Stance and direction become the **motion operators** for the next turn.

---

# **12. Summary**

Appendix R shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- stance_next  
- direction_next  

Stance = *semantic posture*.  
Direction = *semantic motion*.

Together they ensure:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Stance and direction are the **semantic motion backbone** of TS.

---

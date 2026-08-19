# **Appendix J — How A × B Drives Freeze Signatures**  
### *The Deterministic Interaction Between Meaning Coupling and Commit Constraints*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix J explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **freeze signatures**, the commit‑time constraints that:

- prevent premature commit  
- prevent semantic drift  
- prevent identity drift  
- prevent referent drift  
- stabilize meaning  
- stabilize identity  
- stabilize routing  
- stabilize continuity  
- enforce replay determinism  

Freeze signatures are the **semantic locks** of TS.

This appendix shows:

- how A (stated content) influences freeze signatures  
- how B (context) influences freeze signatures  
- how IdOB refines freeze signatures  
- how freeze signatures appear in TP metadata  
- how freeze signatures influence routing (RB)  
- how freeze signatures influence commit (OuBA)  
- how freeze signatures influence continuity and identity  

---

# **2. What Freeze Signatures Are**

Freeze signatures are defined in 20.105.010:

```
TP.metadata.freeze_metadata: {
    semantic_freeze,
    identity_freeze,
    referent_freeze,
    importance_freeze,
    continuity_freeze
}
```

Freeze signatures are:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Freeze signatures are the **commit constraints** of TS.

---

# **3. Why Freeze Signatures Exist**

Freeze signatures exist because:

1. Meaning must be **stable** before commit.  
2. Identity must be **stable** before commit.  
3. Referents must be **stable** before commit.  
4. Semantic‑importance must be **stable** before commit.  
5. Continuity must be **stable** before commit.  
6. Commit must be **deterministic**.  
7. Commit must be **replay‑safe**.  
8. Commit must not occur during semantic conflict.  
9. Commit must not occur during identity conflict.  
10. Commit must not occur during referent ambiguity.

Freeze signatures enforce these constraints.

---

# **4. How “What Is Stated” (A) Drives Freeze Signatures**

A influences freeze signatures through:

### **4.1 Contradiction**
If A contradicts prior meaning:

- semantic_freeze = true  
- continuity_freeze = true  

### **4.2 Correction**
If A corrects prior meaning:

- semantic_freeze = true  
- identity_freeze = true  

### **4.3 Identity‑relevant content**
If A affects identity:

- identity_freeze = true  

### **4.4 Referent placeholders**
If A contains ambiguous referents:

- referent_freeze = true  

### **4.5 Expression markers**
Negation, emphasis, hedging influence:

- semantic_freeze  
- identity_freeze  
- continuity_freeze  

### **4.6 Semantic residues**
Residues from OB‑Set influence freeze signatures:

- contradiction → freeze  
- correction → freeze  
- planning → no freeze  
- affirmation → no freeze  

A is the **semantic trigger** for freeze signatures.

---

# **5. How “Context” (B) Drives Freeze Signatures**

B influences freeze signatures through:

### **5.1 Identity continuity**
If identity continuity is unstable:

- identity_freeze = true  

### **5.2 Referent continuity**
If referent continuity is unstable:

- referent_freeze = true  

### **5.3 Topic continuity**
If topic continuity is unstable:

- continuity_freeze = true  

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- semantic_freeze = true  
- identity_freeze = true  

### **5.5 Routing regime**
If RB indicates:

- Transition → freeze  
- Collapse → freeze  
- Drift → partial freeze  
- Refinement → no freeze  
- Stable → no freeze  

### **5.6 Entropy trajectory**
High entropy → freeze.  
Low entropy → no freeze.

### **5.7 Freeze signatures from prior turns**
Freeze signatures propagate across turns.

B is the **contextual trigger** for freeze signatures.

---

# **6. How IdOB Refines Freeze Signatures**

IdOB is the **only primitive** that refines freeze signatures (besides SSRGn for freeze‑related updates).

IdOB refines freeze signatures by:

### **6.1 Interpreting identity**
If identity is threatened:

- identity_freeze = true  

If identity is stable:

- identity_freeze = false  

---

### **6.2 Interpreting referents**
If referent is ambiguous:

- referent_freeze = true  

If referent is stable:

- referent_freeze = false  

---

### **6.3 Interpreting continuity**
If continuity is unstable:

- continuity_freeze = true  

If continuity is stable:

- continuity_freeze = false  

---

### **6.4 Interpreting residues**
Residues influence freeze signatures:

- contradiction → semantic_freeze  
- correction → semantic_freeze  
- planning → no freeze  
- affirmation → no freeze  

---

### **6.5 Interpreting semantic‑importance**
High importance → freeze.  
Low importance → no freeze.

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- semantic_freeze = true  

If RB indicates large displacement:

- continuity_freeze = true  

IdOB produces a **canonical freeze signature object**.

---

# **7. How Freeze Signatures Appear in TP Metadata**

Freeze signatures appear in:

```
TP.metadata.freeze_metadata.semantic_freeze
TP.metadata.freeze_metadata.identity_freeze
TP.metadata.freeze_metadata.referent_freeze
TP.metadata.freeze_metadata.importance_freeze
TP.metadata.freeze_metadata.continuity_freeze
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Freeze signatures are the **commit constraints** stored in the TP.

---

# **8. How Freeze Signatures Drive Routing (RB)**

RB uses freeze signatures to:

### **8.1 Block commit**
If any freeze signature is true:

- RB blocks commit  
- RB routes to IdOB  

### **8.2 Escalate routing**
If freeze signatures indicate conflict:

- RB escalates routing  
- RB enters Transition or Collapse regime  

### **8.3 Stabilize routing**
If freeze signatures indicate stability:

- RB stabilizes routing  
- RB enters Stable or Refinement regime  

Freeze signatures are the **routing brakes**.

---

# **9. How Freeze Signatures Drive Commit (OuBA)**

OuBA uses freeze signatures to determine commit eligibility.

### **Commit allowed when:**

- semantic_freeze = false  
- identity_freeze = false  
- referent_freeze = false  
- importance_freeze = false  
- continuity_freeze = false  

### **Commit blocked when:**

- any freeze signature = true  

Freeze signatures are the **commit gatekeepers**.

---

# **10. Worked Example — Freeze Signatures in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- semantic_freeze = true  
- identity_freeze = true  
- referent_freeze = true  
- importance_freeze = true  
- continuity_freeze = true  

### **Effects:**

- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- commit blocked  
- IdOB cycle required  
- next‑turn context = correction + defense  

Freeze signatures prevent premature commit.

---

# **11. Summary**

Appendix J shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- semantic_freeze  
- identity_freeze  
- referent_freeze  
- importance_freeze  
- continuity_freeze  

Freeze signatures are the **semantic locks** of TS.  
They ensure:

- meaning stability  
- identity stability  
- referent stability  
- continuity stability  
- routing stability  
- commit stability  
- replay determinism  

Freeze signatures are the **commit constraints** of TS.

---

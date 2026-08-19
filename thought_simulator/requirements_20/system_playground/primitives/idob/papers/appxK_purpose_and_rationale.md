# **Appendix K — How A × B Drives Semantic‑Residue Alignment**  
### *The Deterministic Interaction Between Meaning Coupling and Residue Interpretation*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix K explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **semantic‑residue alignment**, the invariant that determines:

- what kind of semantic pressure exists  
- how meaning should be refined  
- how identity should be stabilized  
- how routing should behave  
- how continuity should be maintained  
- how referents should be resolved  
- how next‑turn context should be predicted  

Semantic‑residue alignment is the **semantic diagnostic engine** of TS.

This appendix shows:

- how A (stated content) produces residues  
- how B (context) shapes residue interpretation  
- how IdOB aligns residues  
- how CCR alignment interacts with residues  
- how residues appear in TP metadata  
- how residues drive routing, continuity, identity, and next‑turn context  

---

# **2. What Semantic Residue Is**

Semantic residue is defined in 20.105.010 and OB‑Set:

```
TP.metadata.semantic_residue: {
    structural_residue,
    semantic_adjacent_residue,
    constraint_residue
}
```

Residue is the **semantic leftover** after CE canonicalization.

Residue captures:

- contradiction  
- correction  
- affirmation  
- planning  
- hedging  
- uncertainty  
- semantic adjacency  
- constraint pressure  

Residue is the **semantic evidence** IdOB uses to refine meaning.

---

# **3. What Semantic‑Residue Alignment Is**

Semantic‑residue alignment is the **interpretation** of residue inside IdOB.

It answers:

- *What kind of semantic pressure is present?*  
- *Is the user correcting?*  
- *Is the user contradicting?*  
- *Is the user planning?*  
- *Is the user affirming?*  
- *Is the user hedging?*  
- *Is the user expressing identity pressure?*  
- *Is the user expressing referent pressure?*  

Semantic‑residue alignment is the **semantic diagnostic layer** of IdOB.

---

# **4. How “What Is Stated” (A) Produces Residue**

A produces residue through:

### **4.1 Expression markers**
- negation → contradiction residue  
- correction → correction residue  
- emphasis → affirmation residue  
- hedging → hedging residue  

### **4.2 Propositional skeleton**
If A contradicts prior meaning:

- contradiction residue  

If A clarifies prior meaning:

- correction residue  

If A continues prior meaning:

- affirmation residue  

### **4.3 Lexical meaning**
Words like:

- “not”  
- “never”  
- “actually”  
- “really”  
- “maybe”  
- “should”  
- “must”  

produce residues.

### **4.4 Structural residue**
OB‑Set produces structural residue:

- adjacency  
- ordering  
- referent placeholders  
- syntactic conflict  

### **4.5 Semantic‑adjacent residue**
SmOB produces semantic‑adjacent residue:

- semantic conflict  
- semantic drift  
- semantic alignment  

### **4.6 Constraint residue**
CnOB produces constraint residue:

- constraint violation  
- constraint pressure  

A is the **semantic generator** of residue.

---

# **5. How “Context” (B) Shapes Residue Interpretation**

B shapes residue interpretation through:

### **5.1 Continuity**
If continuity is unstable:

- residue interpreted as correction  

If continuity is stable:

- residue interpreted as affirmation  

### **5.2 Identity continuity**
If identity is threatened:

- residue interpreted as identity conflict  

If identity is stable:

- residue interpreted as semantic correction  

### **5.3 Referent continuity**
If referent is ambiguous:

- residue interpreted as referent conflict  

If referent is stable:

- residue interpreted as semantic correction  

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- residue interpreted as semantic conflict  

If CCR alignment indicates alignment:

- residue interpreted as semantic affirmation  

### **5.5 Routing regime**
If RB indicates:

- Transition → residue escalated  
- Collapse → residue escalated  
- Drift → residue stabilized  
- Refinement → residue clarified  
- Stable → residue neutral  

### **5.6 Entropy trajectory**
High entropy → residue interpreted as conflict.  
Low entropy → residue interpreted as alignment.

### **5.7 Freeze signatures**
Freeze signatures indicate:

- identity locks  
- semantic locks  
- referent locks  

These influence residue interpretation.

B is the **semantic lens** for residue.

---

# **6. How IdOB Aligns Residue**

IdOB is the **only primitive** that aligns residue.

IdOB aligns residue by:

### **6.1 Interpreting identity**
If identity is threatened:

- residue = identity_conflict  

### **6.2 Interpreting referents**
If referent is ambiguous:

- residue = referent_conflict  

### **6.3 Interpreting continuity**
If continuity is unstable:

- residue = correction  

### **6.4 Interpreting stance/direction**
If stance is backward:

- residue = correction  

If stance is forward:

- residue = planning  

### **6.5 Interpreting semantic‑importance**
High importance → residue escalated.  
Low importance → residue neutral.

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- residue escalated  

If RB indicates large displacement:

- residue escalated  

IdOB produces a **canonical residue alignment object**.

---

# **7. How Residue Appears in TP Metadata**

Residue appears in:

```
TP.metadata.semantic_residue.structural_residue
TP.metadata.semantic_residue.semantic_adjacent_residue
TP.metadata.semantic_residue.constraint_residue
TP.metadata.idob_residue
```

Residue alignment appears in:

```
TP.metadata.idob_residue
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Residue alignment is the **semantic diagnostic record** stored in the TP.

---

# **8. How Residue Drives Routing (RB)**

RB uses residue alignment to:

### **8.1 Classify adjacency**
- contradiction → non_local  
- correction → non_local  
- planning → local  
- affirmation → local  

### **8.2 Compute displacement**
- contradiction → large  
- correction → medium  
- planning → small  
- affirmation → small  

### **8.3 Emit regime hints**
- contradiction → Transition  
- identity conflict → Collapse  
- correction → Drift  
- planning → Refinement  
- affirmation → Stable  

Residue alignment is the **semantic pressure map** RB uses.

---

# **9. How Residue Drives Continuity**

Residue alignment influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

If residue indicates:

- contradiction → continuity correction  
- identity conflict → continuity correction  
- referent conflict → continuity correction  
- planning → continuity continuation  
- affirmation → continuity continuation  

Residue alignment is the **continuity pressure map**.

---

# **10. How Residue Drives Identity**

Residue alignment influences:

- identity geometry  
- identity roles  
- identity stability  
- identity continuity  

If residue indicates:

- identity conflict → identity_defense  
- correction → identity_correction  
- affirmation → identity_neutral  
- planning → identity_alignment  

Residue alignment is the **identity pressure map**.

---

# **11. Worked Example — Residue Alignment in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- idob_residue = identity_conflict  
- structural_residue = contradiction  
- semantic_adjacent_residue = semantic_conflict  
- constraint_residue = none  

### **Effects:**

- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- continuity_next = correction  
- identity_next = defense  
- importance_next = high  

Residue alignment becomes the **semantic diagnostic** for the next turn.

---

# **12. Summary**

Appendix K shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- structural residue  
- semantic‑adjacent residue  
- constraint residue  
- identity‑conditioned residue  
- referent‑conditioned residue  
- continuity‑conditioned residue  
- routing‑conditioned residue  
- importance‑conditioned residue  

Semantic‑residue alignment is the **semantic diagnostic engine** of TS.  
It is the invariant that determines how meaning should be refined, routed, stabilized, committed, and projected.

---

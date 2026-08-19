# **Appendix P — How A × B Drives Identity Roles**  
### *The Deterministic Interaction Between Meaning Coupling and Identity Function*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix P explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **identity roles**, the functional identity operators IdOB emits each turn.

Identity roles determine:

- what identity is *doing*  
- what semantic pressure identity is responding to  
- how identity interacts with meaning  
- how identity interacts with routing  
- how identity interacts with continuity  
- how identity interacts with residues  
- how identity interacts with next‑turn context  

Identity roles are the **behavioral expression** of identity geometry.

---

# **2. What Identity Roles Are**

Identity roles are defined internally in IdOB:

```
idob_roles: string[]
```

Identity roles are:

- **functional**  
- **turn‑local**  
- **context‑dependent**  
- **derived from A × B**  
- **deterministic**  
- **replay‑safe**

Identity roles answer:

- *What is the speaker doing right now?*  
- *Is the speaker correcting?*  
- *Is the speaker defending identity?*  
- *Is the speaker clarifying?*  
- *Is the speaker planning?*  
- *Is the speaker affirming?*  
- *Is the speaker expressing conflict?*

Identity roles are the **operators** IdOB uses to refine meaning.

---

# **3. Identity Roles vs. Identity Geometry**

Identity geometry is **who the speaker is** (identity state).  
Identity roles are **what the speaker is doing** (identity function).

Identity geometry is:

- stable  
- geometric  
- slow‑moving  
- continuous across turns  

Identity roles are:

- functional  
- categorical  
- fast‑moving  
- updated every turn  

Identity geometry = *identity substrate*.  
Identity roles = *identity operators*.

---

# **4. Canonical Identity Roles**

IdOB emits identity roles from a canonical set:

### **4.1 correction_role**  
Identity is performing semantic correction.

### **4.2 identity_role**  
Identity is defending or asserting itself.

### **4.3 referent_role**  
Identity is resolving referent ambiguity.

### **4.4 planning_role**  
Identity is projecting future meaning.

### **4.5 affirmation_role**  
Identity is confirming meaning.

### **4.6 conflict_role**  
Identity is expressing semantic or identity conflict.

### **4.7 stability_role**  
Identity is stabilizing meaning.

### **4.8 alignment_role**  
Identity is aligning with context or CCR.

### **4.9 defense_role**  
Identity is protecting itself from threat.

### **4.10 expansion_role**  
Identity is expanding topic or meaning.

Identity roles are **compositional** — multiple roles may be active in a single turn.

---

# **5. How “What Is Stated” (A) Drives Identity Roles**

A influences identity roles through:

### **5.1 Identity‑relevant propositions**
Statements about:

- self  
- beliefs  
- commitments  
- knowledge  
- corrections  
- denials  

produce identity roles.

Example:  
“I didn’t say that” → identity_role + correction_role.

---

### **5.2 Expression markers**
Negation, correction, emphasis, hedging influence identity roles:

- negation → correction_role  
- correction → correction_role  
- emphasis → identity_role  
- hedging → stability_role  

---

### **5.3 Semantic residues**
Residues from OB‑Set influence identity roles:

- contradiction → conflict_role  
- correction → correction_role  
- planning → planning_role  
- affirmation → affirmation_role  

---

### **5.4 Propositional skeleton**
The subject–verb–object structure determines:

- whether identity is implicated  
- whether identity must respond  

Example:  
“You said X” → identity_role + conflict_role.

A is the **functional trigger** for identity roles.

---

# **6. How “Context” (B) Drives Identity Roles**

B influences identity roles through:

### **6.1 Identity continuity**
If identity continuity is unstable:

- defense_role  
- conflict_role  

If identity continuity is stable:

- stability_role  
- affirmation_role  

---

### **6.2 Referent continuity**
If referent is ambiguous:

- referent_role  

If referent is stable:

- affirmation_role  

---

### **6.3 CCR alignment**
If CCR alignment indicates conflict:

- conflict_role  
- identity_role  

If CCR alignment indicates alignment:

- alignment_role  

---

### **6.4 Routing regime**
If RB indicates:

- Transition → correction_role + identity_role  
- Collapse → conflict_role + defense_role  
- Drift → stability_role  
- Refinement → alignment_role  
- Stable → affirmation_role  

---

### **6.5 Curvature**
High curvature → conflict_role.  
Low curvature → stability_role.

---

### **6.6 Entropy trajectory**
High entropy → defense_role.  
Low entropy → affirmation_role.

---

### **6.7 Freeze signatures**
Freeze signatures indicate:

- identity locks  
- semantic locks  

These produce:

- identity_role  
- defense_role  
- stability_role  

B is the **functional lens** for identity roles.

---

# **7. How IdOB Refines Identity Roles**

IdOB is the **only primitive** that refines identity roles.

IdOB refines identity roles by:

### **7.1 Interpreting identity geometry**
If identity geometry = identity_defense:

- defense_role  
- identity_role  

If identity geometry = corrective_core:

- correction_role  

---

### **7.2 Interpreting residues**
Residues influence identity roles:

- contradiction → conflict_role  
- correction → correction_role  
- planning → planning_role  
- affirmation → affirmation_role  

---

### **7.3 Interpreting continuity**
If continuity is unstable:

- correction_role  
- stability_role  

If continuity is stable:

- affirmation_role  

---

### **7.4 Interpreting semantic‑importance**
High importance → identity_role + conflict_role.  
Low importance → affirmation_role.

---

### **7.5 Interpreting routing**
If RB indicates non‑local adjacency:

- correction_role  
- identity_role  

If RB indicates large displacement:

- conflict_role  

IdOB produces a **canonical identity role set**.

---

# **8. How Identity Roles Appear in TP Metadata**

Identity roles appear in:

```
TP.metadata.idob_roles[]
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Identity roles are the **functional identity record** stored in the TP.

---

# **9. How Identity Roles Drive Continuity**

Identity roles influence:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- correction_role → continuity correction  
- conflict_role → continuity correction  
- affirmation_role → continuity continuation  
- planning_role → continuity expansion  

Identity roles are the **continuity operators**.

---

# **10. How Identity Roles Drive Routing (RB)**

RB uses identity roles to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

Examples:

- conflict_role → Transition or Collapse  
- correction_role → Drift or Transition  
- affirmation_role → Stable  
- alignment_role → Refinement  

Identity roles are the **routing operators**.

---

# **11. Worked Example — Identity Roles in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- idob_roles = [correction_role, identity_role, conflict_role]  

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Identity roles become the **functional identity operators** for the next turn.

---

# **12. Summary**

Appendix P shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- correction_role  
- identity_role  
- referent_role  
- planning_role  
- affirmation_role  
- conflict_role  
- stability_role  
- alignment_role  
- defense_role  
- expansion_role  

Identity roles are the **functional identity operators** of TS.  
They ensure:

- meaning refinement  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Identity roles are the **identity action layer** of TS.

---

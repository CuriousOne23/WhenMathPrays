# **Appendix Q — How A × B Drives Topic Roles**  
### *The Deterministic Interaction Between Meaning Coupling and Topic Function*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix Q explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **topic roles**, the functional operators IdOB emits each turn to describe *what the speaker is doing to the topic*.

Topic roles determine:

- how the topic is being manipulated  
- how the topic is being corrected, refined, expanded, collapsed, or stabilized  
- how semantic pressure is being applied to the topic  
- how routing and continuity should respond  
- how next‑turn context should be shaped  

Topic roles are the **behavioral expression** of topic geometry.

---

# **2. What Topic Roles Are**

Topic roles are defined internally in IdOB:

```
idob_roles: string[]   // includes topic-related roles
```

Topic roles are:

- **functional**  
- **turn‑local**  
- **context‑dependent**  
- **derived from A × B**  
- **deterministic**  
- **replay‑safe**

Topic roles answer:

- *What is the speaker doing to the topic right now?*  
- *Correcting it?*  
- *Refining it?*  
- *Affirming it?*  
- *Collapsing it?*  
- *Shifting it?*  
- *Defending it?*

Topic roles are the **operators** IdOB uses to refine topic meaning.

---

# **3. Topic Roles vs. Topic Geometry**

Topic geometry is **what the topic is** (topic state).  
Topic roles are **what the speaker is doing to the topic** (topic function).

Topic geometry is:

- stable  
- geometric  
- slow‑moving  
- continuous across turns  

Topic roles are:

- functional  
- categorical  
- fast‑moving  
- updated every turn  

Topic geometry = *topic substrate*.  
Topic roles = *topic operators*.

---

# **4. Canonical Topic Roles**

IdOB emits topic roles from a canonical set:

### **4.1 topic_correction_role**  
The speaker is correcting the topic.

### **4.2 topic_refinement_role**  
The speaker is refining or sharpening the topic.

### **4.3 topic_continuation_role**  
The speaker is continuing the existing topic.

### **4.4 topic_conflict_role**  
The speaker is expressing topic conflict.

### **4.5 topic_transition_role**  
The topic is shifting or being re‑anchored.

### **4.6 topic_collapse_role**  
The topic is breaking or collapsing.

### **4.7 topic_expansion_role**  
The speaker is expanding the topic.

### **4.8 topic_alignment_role**  
The speaker is aligning the topic with context or CCR.

Topic roles are **compositional** — multiple roles may be active in a single turn.

---

# **5. How “What Is Stated” (A) Drives Topic Roles**

A influences topic roles through:

### **5.1 Topic‑relevant propositions**
Statements that:

- introduce a new topic  
- shift the topic  
- contradict the topic  
- refine the topic  
- collapse the topic  

produce topic roles.

Example:  
“I didn’t say that” → topic_correction_role + topic_conflict_role.

---

### **5.2 Expression markers**
Negation, correction, emphasis, hedging influence topic roles:

- negation → topic_correction_role  
- correction → topic_correction_role  
- emphasis → topic_transition_role  
- hedging → topic_refinement_role  

---

### **5.3 Semantic residues**
Residues from OB‑Set influence topic roles:

- contradiction → topic_conflict_role  
- correction → topic_correction_role  
- planning → topic_expansion_role  
- affirmation → topic_continuation_role  

---

### **5.4 Propositional skeleton**
The subject–verb–object structure determines:

- whether the topic is implicated  
- whether the topic must respond  

Example:  
“You said X” → topic_conflict_role + topic_transition_role.

A is the **functional trigger** for topic roles.

---

# **6. How “Context” (B) Drives Topic Roles**

B influences topic roles through:

### **6.1 Topic continuity**
If topic continuity is unstable:

- topic_transition_role  
- topic_correction_role  

If topic continuity is stable:

- topic_continuation_role  

---

### **6.2 Identity continuity**
If identity is threatened:

- topic_conflict_role  
- topic_transition_role  

Identity pressure bends the topic.

---

### **6.3 Referent continuity**
If referent is ambiguous:

- topic_correction_role  

Referent pressure bends the topic.

---

### **6.4 CCR alignment**
If CCR alignment indicates conflict:

- topic_conflict_role  

If CCR alignment indicates alignment:

- topic_alignment_role  

---

### **6.5 Routing regime**
If RB indicates:

- Transition → topic_transition_role  
- Collapse → topic_collapse_role  
- Drift → topic_refinement_role  
- Refinement → topic_alignment_role  
- Stable → topic_continuation_role  

---

### **6.6 Curvature**
High curvature → topic_conflict_role.  
Low curvature → topic_continuation_role.

---

### **6.7 Entropy trajectory**
High entropy → topic_transition_role.  
Low entropy → topic_continuation_role.

---

### **6.8 Freeze signatures**
Freeze signatures indicate:

- topic locks  
- topic constraints  

These produce:

- topic_correction_role  
- topic_alignment_role  
- topic_stability_role  

B is the **functional lens** for topic roles.

---

# **7. How IdOB Refines Topic Roles**

IdOB is the **only primitive** that refines topic roles.

IdOB refines topic roles by:

### **7.1 Interpreting topic geometry**
If topic geometry = topic_correction:

- topic_correction_role  

If topic geometry = topic_conflict:

- topic_conflict_role  

If topic geometry = topic_refinement:

- topic_refinement_role  

---

### **7.2 Interpreting residues**
Residues influence topic roles:

- contradiction → topic_conflict_role  
- correction → topic_correction_role  
- planning → topic_expansion_role  
- affirmation → topic_continuation_role  

---

### **7.3 Interpreting continuity**
If continuity is unstable:

- topic_correction_role  
- topic_transition_role  

If continuity is stable:

- topic_continuation_role  

---

### **7.4 Interpreting semantic‑importance**
High importance → topic_conflict_role + topic_correction_role.  
Low importance → topic_continuation_role.

---

### **7.5 Interpreting routing**
If RB indicates non‑local adjacency:

- topic_transition_role  

If RB indicates large displacement:

- topic_conflict_role  

IdOB produces a **canonical topic role set**.

---

# **8. How Topic Roles Appear in TP Metadata**

Topic roles appear in:

```
TP.metadata.idob_roles[]   // topic-related roles included
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Topic roles are the **functional topic record** stored in the TP.

---

# **9. How Topic Roles Drive Continuity**

Topic roles influence:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- topic_correction_role → continuity correction  
- topic_conflict_role → continuity correction  
- topic_continuation_role → continuity continuation  
- topic_expansion_role → continuity expansion  

Topic roles are the **continuity operators**.

---

# **10. How Topic Roles Drive Routing (RB)**

RB uses topic roles to:

- classify adjacency  
- compute displacement  
- emit regime hints  
- escalate routing  
- stabilize routing  

Examples:

- topic_conflict_role → Transition or Collapse  
- topic_correction_role → Drift or Transition  
- topic_continuation_role → Stable  
- topic_alignment_role → Refinement  

Topic roles are the **routing operators**.

---

# **11. Worked Example — Topic Roles in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- topic roles = [topic_correction_role, topic_conflict_role, topic_transition_role]

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- importance_next = high  

Topic roles become the **functional topic operators** for the next turn.

---

# **12. Summary**

Appendix Q shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- topic_correction_role  
- topic_refinement_role  
- topic_continuation_role  
- topic_conflict_role  
- topic_transition_role  
- topic_collapse_role  
- topic_expansion_role  
- topic_alignment_role  

Topic roles are the **functional topic operators** of TS.  
They ensure:

- meaning refinement  
- topic stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Topic roles are the **topic action layer** of TS.

---

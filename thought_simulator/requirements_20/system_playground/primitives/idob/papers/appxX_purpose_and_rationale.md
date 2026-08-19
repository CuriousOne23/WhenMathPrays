# **Appendix X — How A × B Drives Freeze‑Propagation Across Turns**  
### *The Deterministic Interaction Between Meaning Coupling and Semantic Locking*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix X explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **freeze‑propagation**, the invariant that determines:

- when a freeze is created  
- what type of freeze is created  
- how freezes propagate across turns  
- how freezes interact with identity, topic, referents, coherence, continuity  
- how freezes influence routing, adjacency, displacement, regime transitions  
- how freezes block commit  
- how freezes shape next‑turn context  

Freeze‑propagation is the **semantic lock engine** of TS.

---

# **2. What Freeze‑Propagation Is**

Freeze‑propagation appears in:

```
TP.metadata.freeze.current
TP.metadata.freeze.next
TP.metadata.freeze.propagation
```

A **freeze** is a semantic lock indicating:

- identity instability  
- referent instability  
- topic instability  
- coherence instability  
- continuity instability  

Freeze‑propagation is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Freeze‑propagation answers:

- *Is the conversation locked?*  
- *What is locked?*  
- *How long does the lock persist?*  
- *Does the lock escalate or resolve?*

Freeze‑propagation is the **semantic lock propagation system** of TS.

---

# **3. Why Freeze‑Propagation Exists**

Freeze‑propagation exists because:

1. Meaning can become unstable.  
2. Instability must be tracked across turns.  
3. Instability cannot be ignored.  
4. TS must prevent premature commit.  
5. TS must prevent semantic drift during instability.  
6. TS must stabilize identity, topic, referents, coherence, continuity.  
7. TS must detect when instability resolves.  
8. Replay determinism requires freeze tracking.

Freeze‑propagation is the **semantic safety mechanism** of TS.

---

# **4. Types of Freezes**

IdOB emits freezes from a canonical set:

### **4.1 identity_freeze**  
Identity is unstable or threatened.

### **4.2 referent_freeze**  
Referent is ambiguous or collapsing.

### **4.3 topic_freeze**  
Topic is unstable or shifting.

### **4.4 coherence_freeze**  
Turn does not fit the conversation.

### **4.5 continuity_freeze**  
Conversation trajectory is unstable.

### **4.6 compound_freeze**  
Multiple freezes active simultaneously.

Freeze‑propagation determines how these locks persist.

---

# **5. How “What Is Stated” (A) Creates Freezes**

A creates freezes through:

### **5.1 Contradiction**
Contradiction → identity_freeze + coherence_freeze.

### **5.2 Correction**
Correction → referent_freeze + topic_freeze.

### **5.3 Identity‑relevant content**
Identity pressure → identity_freeze.

### **5.4 Referent placeholders**
Ambiguous referents → referent_freeze.

### **5.5 Topic shifts**
Topic instability → topic_freeze.

### **5.6 Clarifications**
Clarification → freeze resolution.

### **5.7 Affirmations**
Affirmation → freeze resolution.

A is the **freeze trigger**.

---

# **6. How “Context” (B) Creates or Resolves Freezes**

B influences freeze‑propagation through:

### **6.1 Continuity**
Unstable continuity → continuity_freeze.  
Stable continuity → freeze resolution.

---

### **6.2 Identity continuity**
Identity threat → identity_freeze.  
Identity stable → identity_freeze resolution.

---

### **6.3 Referent continuity**
Referent ambiguous → referent_freeze.  
Referent stable → referent_freeze resolution.

---

### **6.4 CCR alignment**
Conflict → coherence_freeze.  
Alignment → coherence_freeze resolution.

---

### **6.5 Routing regime**
Transition → freeze escalation.  
Collapse → compound_freeze.  
Drift → freeze persistence.  
Refinement → freeze resolution.  
Stable → freeze resolution.

---

### **6.6 Curvature**
High curvature → freeze escalation.  
Low curvature → freeze resolution.

---

### **6.7 Entropy trajectory**
High entropy → freeze escalation.  
Low entropy → freeze resolution.

B is the **freeze lens**.

---

# **7. How IdOB Refines Freeze‑Propagation**

IdOB is the **only primitive** that refines freeze‑propagation.

IdOB refines freezes by:

### **7.1 Interpreting identity geometry**
Identity_defense → identity_freeze.  
Identity_conflict → compound_freeze.  
Identity_neutral → freeze resolution.

---

### **7.2 Interpreting topic geometry**
Topic_conflict → topic_freeze.  
Topic_correction → topic_freeze.  
Topic_continuation → freeze resolution.

---

### **7.3 Interpreting referent continuity**
Referent conflict → referent_freeze.  
Referent collapse → compound_freeze.  
Referent continuation → freeze resolution.

---

### **7.4 Interpreting coherence geometry**
Coh_conflict → coherence_freeze.  
Coh_correction → coherence_freeze.  
Coh_continuation → freeze resolution.

---

### **7.5 Interpreting continuity geometry**
Cont_conflict → continuity_freeze.  
Cont_correction → continuity_freeze.  
Cont_continuation → freeze resolution.

---

### **7.6 Interpreting residues**
Contradiction → freeze escalation.  
Correction → freeze persistence.  
Planning → freeze resolution.  
Affirmation → freeze resolution.

---

### **7.7 Interpreting routing**
Non_local adjacency → freeze escalation.  
Large displacement → freeze escalation.  
Local adjacency → freeze resolution.

IdOB produces a **canonical freeze‑propagation object**.

---

# **8. How Freeze‑Propagation Appears in TP Metadata**

Freeze‑propagation appears in:

```
TP.metadata.freeze.current
TP.metadata.freeze.next
TP.metadata.freeze.propagation
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Freeze‑propagation is the **semantic lock record** stored in the TP.

---

# **9. How Freeze‑Propagation Drives Routing (RB)**

RB uses freeze‑propagation to:

### **9.1 Escalate routing**
Active freeze → escalate.

### **9.2 Block commit**
Active freeze → commit blocked.

### **9.3 Classify adjacency**
Freeze → non_local adjacency.

### **9.4 Compute displacement**
Freeze → medium or large displacement.

### **9.5 Emit regime hints**
Freeze → Transition or Collapse.

Freeze‑propagation is the **routing lock engine**.

---

# **10. How Freeze‑Propagation Drives Continuity**

Freeze‑propagation influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- identity_freeze → continuity correction  
- referent_freeze → continuity correction  
- topic_freeze → continuity correction  
- coherence_freeze → continuity correction  
- continuity_freeze → continuity correction  

Freeze‑propagation is the **continuity lock engine**.

---

# **11. Worked Example — Freeze‑Propagation in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

```
freeze.current = referent_freeze + identity_freeze
freeze.next = identity_freeze
freeze.propagation = escalated
```

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- commit blocked  

Freeze‑propagation becomes the **semantic lock** for the next turn.

---

# **12. Summary**

Appendix X shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- identity_freeze  
- referent_freeze  
- topic_freeze  
- coherence_freeze  
- continuity_freeze  
- compound_freeze  
- freeze escalation  
- freeze persistence  
- freeze resolution  

Freeze‑propagation is the **semantic lock engine** of TS.  
It ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Freeze‑propagation is the **semantic safety backbone** of TS.

---

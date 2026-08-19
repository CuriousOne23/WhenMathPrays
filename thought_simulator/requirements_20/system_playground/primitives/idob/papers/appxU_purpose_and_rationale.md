# **Appendix U — How A × B Drives Semantic‑Importance**  
### *The Deterministic Interaction Between Meaning Coupling and Importance Weighting*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix U explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **semantic‑importance**, the invariant that determines:

- how much weight the turn carries  
- how strongly the turn influences meaning  
- how strongly the turn influences identity  
- how strongly the turn influences topic  
- how strongly the turn influences routing  
- how strongly the turn influences continuity  
- how strongly the turn influences commit eligibility  

Semantic‑importance is the **scalar pressure signal** of TS.

---

# **2. What Semantic‑Importance Is**

Semantic‑importance appears in:

```
TP.metadata.semantic_importance.current
TP.metadata.semantic_importance.next
```

Semantic‑importance is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Semantic‑importance answers:

- *How much does this turn matter?*  
- *How much pressure does this turn apply?*  
- *How strongly should TS respond?*  
- *How much should routing escalate or stabilize?*  
- *How much should continuity adjust?*

Semantic‑importance is the **importance weight** of TS.

---

# **3. Why Semantic‑Importance Exists**

Semantic‑importance exists because:

1. Not all turns carry equal weight.  
2. Some turns apply strong semantic pressure.  
3. Some turns apply weak semantic pressure.  
4. TS must detect pressure deterministically.  
5. Routing must respond proportionally.  
6. Continuity must respond proportionally.  
7. Identity must respond proportionally.  
8. Commit must be blocked during high pressure.  
9. Replay determinism requires importance tracking.

Semantic‑importance is the **pressure meter** of TS.

---

# **4. How “What Is Stated” (A) Drives Semantic‑Importance**

A influences semantic‑importance through:

### **4.1 Contradiction**
Contradiction produces **high importance**.

### **4.2 Correction**
Correction produces **medium‑high importance**.

### **4.3 Identity‑relevant content**
Identity pressure produces **high importance**.

### **4.4 Referent placeholders**
Referent ambiguity produces **medium importance**.

### **4.5 Affirmation**
Affirmation produces **low importance**.

### **4.6 Planning**
Planning produces **medium importance**.

### **4.7 Hedging**
Hedging produces **low importance**.

### **4.8 Expression markers**
Negation, emphasis, urgency increase importance.

A is the **importance trigger**.

---

# **5. How “Context” (B) Drives Semantic‑Importance**

B influences semantic‑importance through:

### **5.1 Continuity**
If continuity is unstable:

- importance ↑  

If continuity is stable:

- importance ↓  

---

### **5.2 Identity continuity**
If identity is threatened:

- importance ↑↑↑  

If identity is stable:

- importance ↓  

---

### **5.3 Referent continuity**
If referent is ambiguous:

- importance ↑  

If referent is stable:

- importance ↓  

---

### **5.4 CCR alignment**
Conflict → importance ↑↑  
Alignment → importance ↓  

---

### **5.5 Routing regime**
Transition → importance ↑↑  
Collapse → importance ↑↑↑  
Drift → importance ↑  
Refinement → importance ↓  
Stable → importance ↓↓

---

### **5.6 Curvature**
High curvature → importance ↑↑  
Low curvature → importance ↓↓

---

### **5.7 Entropy trajectory**
High entropy → importance ↑↑  
Low entropy → importance ↓↓

---

### **5.8 Freeze signatures**
Freeze signatures indicate:

- semantic locks  
- identity locks  
- referent locks  

These produce **high importance**.

B is the **importance lens**.

---

# **6. How IdOB Refines Semantic‑Importance**

IdOB is the **only primitive** that refines semantic‑importance.

IdOB refines importance by:

### **6.1 Interpreting identity geometry**
Identity_defense → importance ↑↑  
Identity_conflict → importance ↑↑↑  
Identity_neutral → importance ↓  

---

### **6.2 Interpreting topic geometry**
Topic_conflict → importance ↑↑  
Topic_correction → importance ↑  
Topic_continuation → importance ↓  

---

### **6.3 Interpreting residues**
Contradiction → importance ↑↑  
Correction → importance ↑  
Planning → importance ↔  
Affirmation → importance ↓  

---

### **6.4 Interpreting continuity**
Unstable continuity → importance ↑  
Stable continuity → importance ↓  

---

### **6.5 Interpreting routing**
Non‑local adjacency → importance ↑  
Large displacement → importance ↑↑  

IdOB produces a **canonical importance value**.

---

# **7. How Semantic‑Importance Appears in TP Metadata**

Semantic‑importance appears in:

```
TP.metadata.semantic_importance.current
TP.metadata.semantic_importance.next
```

These fields are:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Semantic‑importance is the **importance record** stored in the TP.

---

# **8. How Semantic‑Importance Drives Routing (RB)**

RB uses semantic‑importance to:

### **8.1 Escalate routing**
High importance → RB escalates.

### **8.2 Stabilize routing**
Low importance → RB stabilizes.

### **8.3 Classify adjacency**
High importance → non‑local adjacency.  
Low importance → local adjacency.

### **8.4 Compute displacement**
High importance → large displacement.  
Low importance → small displacement.

### **8.5 Emit regime hints**
High importance → Transition or Collapse.  
Low importance → Stable or Refinement.

Semantic‑importance is the **routing pressure scalar**.

---

# **9. How Semantic‑Importance Drives Continuity**

Semantic‑importance influences:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Examples:

- high importance → continuity correction  
- medium importance → continuity refinement  
- low importance → continuity continuation  

Semantic‑importance is the **continuity pressure scalar**.

---

# **10. How Semantic‑Importance Drives Identity**

Semantic‑importance influences:

- identity geometry  
- identity roles  
- identity stability  
- identity continuity  

Examples:

- high importance → identity_defense  
- medium importance → identity_alignment  
- low importance → identity_neutral  

Semantic‑importance is the **identity pressure scalar**.

---

# **11. Worked Example — Semantic‑Importance in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high entropy + high curvature  

### **IdOB refinement:**

- semantic_importance.current = high  
- semantic_importance.next = high  

### **Effects:**

- continuity_next = correction  
- identity_next = defense  
- RB adjacency = non_local  
- RB displacement = large  
- RB regime = Transition  
- commit blocked  

Semantic‑importance becomes the **pressure scalar** for the next turn.

---

# **12. Summary**

Appendix U shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- high importance  
- medium importance  
- low importance  

Semantic‑importance is the **pressure scalar** of TS.  
It ensures:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Semantic‑importance is the **semantic weight backbone** of TS.

---

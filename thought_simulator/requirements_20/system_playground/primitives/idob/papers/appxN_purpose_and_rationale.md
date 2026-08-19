# **Appendix N — How A × B Drives Regime Transitions**  
### *The Deterministic Interaction Between Meaning Coupling and Routing Macro‑States*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix N explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

drives **regime transitions**, the macro‑state changes RB uses to classify:

- semantic stability  
- semantic drift  
- semantic conflict  
- semantic collapse  
- identity pressure  
- referent pressure  
- continuity pressure  

Regime transitions are the **macro‑routing backbone** of TS.

This appendix shows:

- how A (stated content) influences regime transitions  
- how B (context) influences regime transitions  
- how IdOB refines regime transitions  
- how regime transitions appear in TP metadata  
- how regime transitions drive routing, continuity, identity, and commit  
- how regime transitions interact with curvature and entropy  
- how regime transitions interact with freeze signatures  

Regime transitions are the **semantic state machine** of TS.

---

# **2. What Regimes Are**

RB defines five canonical regimes:

| Regime | Meaning |
|--------|---------|
| **Stable** | Meaning is continuous and aligned |
| **Refinement** | Meaning is being clarified |
| **Drift** | Meaning is shifting but not in conflict |
| **Transition** | Meaning is in conflict or identity pressure |
| **Collapse** | Meaning is breaking; identity or referent crisis |

Regimes are:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**

Regimes are the **macro‑states** of routing.

---

# **3. Why Regimes Exist**

Regimes exist because:

1. Meaning changes across turns.  
2. Some changes are stable.  
3. Some changes require refinement.  
4. Some changes drift.  
5. Some changes conflict.  
6. Some changes collapse.  
7. TS must detect these states deterministically.  
8. Routing must respond to these states.  
9. Commit must be blocked during unstable states.  
10. Replay determinism requires regime tracking.

Regimes are the **semantic state machine** of TS.

---

# **4. How “What Is Stated” (A) Drives Regime Transitions**

A influences regime transitions through:

### **4.1 Contradiction**
If A contradicts prior meaning:

- regime → Transition  

### **4.2 Correction**
If A corrects prior meaning:

- regime → Drift or Transition (depending on B)  

### **4.3 Identity‑relevant content**
If A affects identity:

- regime → Transition or Collapse  

### **4.4 Referent placeholders**
If A introduces ambiguous referents:

- regime → Drift  

### **4.5 Expression markers**
Negation, emphasis, hedging influence regime:

- negation → Transition  
- emphasis → Drift  
- hedging → Refinement  

### **4.6 Semantic residues**
Residues from OB‑Set influence regime:

- contradiction → Transition  
- correction → Drift  
- planning → Refinement  
- affirmation → Stable  

A is the **semantic trigger** for regime transitions.

---

# **5. How “Context” (B) Drives Regime Transitions**

B influences regime transitions through:

### **5.1 Continuity**
If continuity is unstable:

- regime → Drift  

If continuity is stable:

- regime → Stable  

---

### **5.2 Identity continuity**
If identity is threatened:

- regime → Transition or Collapse  

If identity is stable:

- regime → Stable or Refinement  

---

### **5.3 Referent continuity**
If referent is ambiguous:

- regime → Drift  

If referent is stable:

- regime → Stable  

---

### **5.4 CCR alignment**
If CCR alignment indicates conflict:

- regime → Transition  

If CCR alignment indicates alignment:

- regime → Stable  

---

### **5.5 Routing curvature**
High curvature → Transition or Collapse.  
Low curvature → Stable or Refinement.

---

### **5.6 Entropy trajectory**
High entropy → Transition or Collapse.  
Low entropy → Stable or Refinement.

---

### **5.7 Freeze signatures**
Freeze signatures indicate:

- semantic locks  
- identity locks  
- referent locks  

These push regime → Transition or Collapse.

B is the **semantic lens** that determines regime transitions.

---

# **6. How IdOB Refines Regime Transitions**

IdOB is the **only primitive** that refines regime transitions.

IdOB refines regime transitions by:

### **6.1 Interpreting identity**
If identity is threatened:

- regime → Transition or Collapse  

If identity is stable:

- regime → Stable or Refinement  

---

### **6.2 Interpreting referents**
If referent is ambiguous:

- regime → Drift  

If referent is stable:

- regime → Stable  

---

### **6.3 Interpreting continuity**
If continuity is unstable:

- regime → Drift  

If continuity is stable:

- regime → Stable  

---

### **6.4 Interpreting residues**
Residues influence regime:

- contradiction → Transition  
- identity conflict → Collapse  
- correction → Drift  
- planning → Refinement  
- affirmation → Stable  

---

### **6.5 Interpreting semantic‑importance**
High importance → regime escalated.  
Low importance → regime stabilized.

---

### **6.6 Interpreting routing**
If RB indicates non‑local adjacency:

- regime → Transition  

If RB indicates large displacement:

- regime → Transition or Collapse  

IdOB produces a **canonical regime_hint**.

---

# **7. How Regime Transitions Appear in TP Metadata**

Regime transitions appear in:

```
TP.metadata.routing.regime_hint
```

This field is:

- deterministic  
- canonical  
- replay‑safe  
- identity‑conditioned  
- context‑conditioned  

Regime transitions are the **macro‑routing record** stored in the TP.

---

# **8. How Regime Transitions Drive Routing (RB)**

RB uses regime transitions to:

### **8.1 Escalate routing**
Transition/Collapse → RB escalates.

### **8.2 Stabilize routing**
Stable/Refinement → RB stabilizes.

### **8.3 Classify adjacency**
Transition/Collapse → non‑local adjacency.  
Stable/Refinement → local adjacency.

### **8.4 Compute displacement**
Transition/Collapse → large displacement.  
Stable/Refinement → small displacement.

### **8.5 Block commit**
Transition/Collapse → commit blocked.

Regime transitions are the **routing macro‑state controller**.

---

# **9. How Regime Transitions Drive Continuity**

Regime transitions influence:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  
- coherence continuity  

Transition/Collapse → continuity correction.  
Stable/Refinement → continuity continuation.

Regime transitions are the **continuity macro‑state controller**.

---

# **10. How Regime Transitions Drive Identity**

Regime transitions influence:

- identity geometry  
- identity roles  
- identity stability  
- identity continuity  

Transition → identity_defense.  
Collapse → identity_crisis.  
Stable → identity_neutral.  
Refinement → identity_alignment.

Regime transitions are the **identity macro‑state controller**.

---

# **11. Worked Example — Regime Transition in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- regime_hint = Transition  
- identity geometry = identity_defense  
- residue = identity_conflict  
- continuity_next = correction  
- identity_next = defense  
- importance_next = high  

### **Effects:**

- RB adjacency = non_local  
- RB displacement = large  
- commit blocked  
- IdOB cycle required  

Regime transitions become the **macro‑routing state** for the next turn.

---

# **12. Summary**

Appendix N shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- Stable  
- Refinement  
- Drift  
- Transition  
- Collapse  

Regime transitions are the **semantic state machine** of TS.  
They ensure:

- meaning stability  
- identity stability  
- routing stability  
- continuity stability  
- commit stability  
- replay determinism  

Regime transitions are the **macro‑routing backbone** of TS.

---

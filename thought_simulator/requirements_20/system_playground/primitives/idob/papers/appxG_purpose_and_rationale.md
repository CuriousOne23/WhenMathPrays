# **Appendix G — How A × B Drives Semantic‑Importance**  
### *The Deterministic Interaction Between Meaning Coupling and Importance Roles*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix G explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

produces **semantic‑importance**, the invariant that determines:

- which entities matter  
- which facts matter  
- how strongly they matter  
- why they matter  
- how meaning should be refined  
- how routing should behave  
- how continuity should be maintained  
- how identity should be stabilized  

Semantic‑importance is not a score.  
Semantic‑importance is a **structured meaning invariant**.

This appendix shows:

- how A (stated content) influences importance  
- how B (context) influences importance  
- how IdOB refines importance  
- how importance appears in TP metadata  
- how importance drives routing, continuity, identity, CCR, COB, and CIL  

---

# **2. What Semantic‑Importance Is**

Semantic‑importance is defined in 20.105.010:

```
TP.semantic.importance.entities[]: {
    value: string,
    role: string,
    score: number,
    provenance
}

TP.semantic.importance.facts[]: {
    value: string,
    role: string,
    score: number,
    provenance
}
```

Semantic‑importance is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **replay‑safe**  

Semantic‑importance is the **semantic weight** of entities and facts in the meaning state.

---

# **3. How “What Is Stated” (A) Drives Semantic‑Importance**

A influences importance through:

### **3.1 Lexical emphasis**
Words like:

- “must”  
- “critical”  
- “important”  
- “urgent”  
- “never”  
- “always”  

increase importance.

### **3.2 Expression markers**
Negation, correction, affirmation, hedging, and emphasis influence importance.

Examples:

- “I didn’t say that” → importance of the misattributed claim increases  
- “That’s exactly what I meant” → importance of the clarified referent increases  

### **3.3 Propositional skeleton**
The subject–verb–object structure determines:

- which entity is central  
- which fact is central  
- which referent is central  

### **3.4 Semantic residues**
Residues from OB‑Set influence importance:

- contradiction → high importance  
- correction → high importance  
- planning → medium importance  
- affirmation → medium importance  
- hedging → low importance  

### **3.5 Identity‑relevant content**
Statements about:

- self  
- beliefs  
- commitments  
- knowledge  
- identity roles  

increase importance.

---

# **4. How “Context” (B) Drives Semantic‑Importance**

B influences importance through:

### **4.1 Continuity**
If a topic persists across turns, its importance increases.

### **4.2 Identity continuity**
If a referent affects identity, importance increases.

### **4.3 Referent continuity**
If a referent persists across turns, importance increases.

### **4.4 CCR alignment**
CCR alignment signals:

- identity alignment  
- context alignment  
- semantic‑residue alignment  

These increase importance.

### **4.5 Routing regime**
RB’s regime_hint influences importance:

- Stable → low importance  
- Refinement → medium importance  
- Drift → medium importance  
- Transition → high importance  
- Collapse → very high importance  

### **4.6 Entropy trajectory**
High entropy increases importance because instability increases semantic weight.

### **4.7 Freeze signatures**
Freeze signatures indicate:

- commitments  
- constraints  
- identity locks  

These increase importance.

---

# **5. How IdOB Refines Semantic‑Importance**

IdOB is the **only primitive** allowed to refine semantic‑importance (besides SSRGn for freeze‑related updates).

IdOB refines importance by:

### **5.1 Interpreting residues**
- contradiction → importance ↑  
- correction → importance ↑  
- planning → importance ↑  
- affirmation → importance ↔  
- hedging → importance ↓  

### **5.2 Interpreting identity**
If a referent affects identity:

- importance ↑↑  

### **5.3 Interpreting continuity**
If a referent persists:

- importance ↑  

If a referent drifts:

- importance ↓  

### **5.4 Interpreting stance/direction**
- backward motion → importance ↑  
- forward motion → importance ↑  
- neutral → importance ↔  

### **5.5 Interpreting CCR alignment**
If CCR alignment indicates:

- semantic_residue conflict → importance ↑  
- identity conflict → importance ↑↑  
- context alignment → importance ↑  

### **5.6 Interpreting routing**
If RB indicates:

- non‑local adjacency → importance ↑  
- large displacement → importance ↑↑  
- Transition/Collapse regime → importance ↑↑↑  

IdOB produces **canonical importance roles**:

- correction_role  
- identity_role  
- referent_role  
- planning_role  
- affirmation_role  
- conflict_role  
- stability_role  

These roles appear in:

```
TP.semantic.importance.entities[].role
TP.semantic.importance.facts[].role
```

---

# **6. How Semantic‑Importance Appears in TP Metadata**

Semantic‑importance appears in:

### **6.1 TP.semantic.importance**
Entities and facts with:

- value  
- role  
- score  
- provenance  

### **6.2 TP.metadata.semantic_residue**
Residue alignment influences importance.

### **6.3 TP.cex.ccr**
CCR alignment influences importance.

### **6.4 TP.metadata.cil**
CIL substrate selection depends on importance.

### **6.5 TP.metadata.continuity**
Continuity metadata influences importance.

### **6.6 TP.metadata.identity**
Identity metadata influences importance.

Semantic‑importance is the **semantic weight map** of the TP.

---

# **7. How Semantic‑Importance Drives Routing (RB)**

RB uses importance to:

- escalate routing  
- stabilize routing  
- classify adjacency  
- compute displacement  
- emit regime hints  
- decide whether IdOB must run  
- decide whether commit is allowed  

High importance → IdOB must run.  
Low importance → commit may be allowed.

---

# **8. How Semantic‑Importance Drives Continuity**

Continuity uses importance to:

- stabilize referents  
- stabilize identity  
- stabilize topic  
- stabilize stance/direction  
- stabilize coherence  

High importance → continuity must be preserved.  
Low importance → continuity may drift.

---

# **9. How Semantic‑Importance Drives Identity**

Identity uses importance to:

- protect identity  
- update identity geometry  
- update identity roles  
- update identity stability  

High importance → identity refinement required.  
Low importance → identity stable.

---

# **10. How Semantic‑Importance Drives CCR, COB, and CIL**

### **10.1 CCR**
CCR alignment uses importance to:

- detect semantic conflict  
- detect identity conflict  
- detect context conflict  

### **10.2 COB**
COB uses importance to:

- project meaning into the selected conversation  
- determine projection strength  

### **10.3 CIL**
CIL uses importance to:

- maintain continuity  
- maintain identity  
- maintain referent lineage  

Semantic‑importance is the **semantic backbone** of the conversation layer.

---

# **11. Worked Example — Importance in Action**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + semantic conflict + high importance  

### **IdOB refinement:**

- role: correction_role  
- score: high  
- identity continuity: unstable  
- referent continuity: unstable  
- residue: contradiction  
- CCR alignment: semantic_residue + identity  
- routing: non‑local adjacency  
- regime: Transition  
- displacement: large  

### **Semantic‑importance entry:**

```
TP.semantic.importance.entities[]:
{
    value: "interpretation_of_prior_turn",
    role: "identity_role",
    score: 0.92,
    provenance: ...
}

TP.semantic.importance.facts[]:
{
    value: "user_correction",
    role: "correction_role",
    score: 0.88,
    provenance: ...
}
```

Semantic‑importance captures the **semantic weight** of the correction.

---

# **12. Summary**

Appendix G shows how:

- **A (stated content)**  
- **B (context)**  

drive:

- semantic‑importance roles  
- semantic‑importance scores  
- identity‑conditioned importance  
- context‑conditioned importance  
- residue‑conditioned importance  
- routing‑conditioned importance  
- continuity‑conditioned importance  

Semantic‑importance is the **semantic weight map** of TS.  
It is the invariant that determines how meaning should be refined, routed, stabilized, committed, and projected.

---

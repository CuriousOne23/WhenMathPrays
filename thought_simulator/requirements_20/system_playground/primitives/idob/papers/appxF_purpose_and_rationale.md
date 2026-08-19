# **Appendix F — How A × B Appears in Cognitive‑History Entries**  
### *The Replay‑Deterministic Record of Meaning Coupling Across Path‑A*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix F explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

is recorded inside **cognitive‑history entries**, the append‑only, replay‑deterministic log written by CTP‑prm.

This appendix shows:

- how A (what is stated) appears in cognitive‑history  
- how B (context) appears in cognitive‑history  
- how IdOB’s refinement appears in cognitive‑history  
- how routing (RB) appears in cognitive‑history  
- how residues appear in cognitive‑history  
- how continuity and identity appear in cognitive‑history  
- how entropy and curvature appear in cognitive‑history  
- how CCR alignment appears in cognitive‑history  

This appendix is the bridge between **meaning theory** and **TP replay determinism**.

---

# **2. Cognitive‑History Is the Replay‑Deterministic Log of Meaning Coupling**

Every cycle of Path‑A produces a cognitive‑history entry:

```
TP.metadata.cognitive_history[] {
    cycle_id
    timestamp
    invariants: {
        I_stab,
        R_res,
        P_cont,
        L_depth,
        Rt_adj,
        ΔH,
        E_dens,
        C_coh
    }
    idob_geometry: {
        neighborhood,
        k_id
    }
    idob_roles
    idob_residue
    idob_stability
    rb_adjacency_class
    rb_displacement_scale
    rb_regime_hint
    rb_route_proposal
}
```

This entry is **append‑only**, **immutable**, and **replay‑safe**.

It is the **historical record** of how A × B shaped meaning, routing, and identity.

---

# **3. How “What Is Stated” (A) Appears in Cognitive‑History**

A (propositional content) appears indirectly through:

### **3.1 Structural invariants**
- **R_res** — structural residue  
- **idob_residue** — IdOB’s interpretation of residue  
- **C_coh** — coherence invariant  
- **L_depth** — structural depth  

These fields encode:

- propositional skeleton  
- lexical meaning  
- negation/correction/affirmation markers  
- semantic‑adjacent residue  
- constraint residue  

### **3.2 Routing invariants**
- **rb_adjacency_class**  
- **rb_displacement_scale**  
- **rb_regime_hint**  

These fields encode how A influenced:

- adjacency  
- displacement  
- routing regime  

### **3.3 Identity invariants**
- **idob_roles**  
- **idob_geometry**  
- **idob_stability**  

These encode how A influenced:

- identity roles  
- identity geometry  
- identity stability  

A is not stored directly — it is stored as **invariants** derived from A.

This is what makes cognitive‑history **bounded** and **replay‑safe**.

---

# **4. How “Context” (B) Appears in Cognitive‑History**

B (contextual structure) appears through:

### **4.1 Continuity invariants**
- **P_cont** — continuity invariant  
- **I_stab** — identity stability  
- **idob_stability** — IdOB’s continuity assessment  

These encode:

- topic continuity  
- referent continuity  
- identity continuity  
- stance/direction continuity  

### **4.2 Routing context**
- **Rt_adj** — routing adjacency  
- **rb_adjacency_class**  
- **rb_displacement_scale**  
- **rb_regime_hint**  

These encode:

- continuity pressure  
- identity pressure  
- semantic pressure  
- routing pressure  

### **4.3 Entropy and curvature**
- **ΔH** — entropy trajectory  
- **E_dens** — entropy density  

These encode:

- contextual instability  
- semantic drift  
- identity drift  

### **4.4 CCR alignment**
Although not stored directly, CCR alignment influences:

- **idob_roles**  
- **idob_geometry**  
- **idob_residue**  
- **rb_regime_hint**  

B is not stored directly — it is stored as **context invariants**.

This is what makes cognitive‑history **bounded** and **deterministic**.

---

# **5. How IdOB’s Refinement Appears in Cognitive‑History**

IdOB’s refinement appears through:

### **5.1 Identity geometry**
```
idob_geometry.neighborhood
idob_geometry.k_id
```

These encode:

- identity neighborhood  
- identity kernel  

### **5.2 Identity roles**
```
idob_roles
```

These encode:

- stance roles  
- direction roles  
- semantic‑importance roles  

### **5.3 Identity stability**
```
idob_stability
```

This encodes:

- identity continuity  
- identity drift  
- identity correction  

### **5.4 Residue interpretation**
```
idob_residue
```

This encodes:

- contradiction  
- correction  
- planning  
- affirmation  
- semantic‑adjacent cues  

IdOB’s refinement is the **semantic core** of cognitive‑history.

---

# **6. How Routing (RB) Appears in Cognitive‑History**

RB’s routing decisions appear through:

### **6.1 Adjacency**
```
rb_adjacency_class
```

### **6.2 Displacement**
```
rb_displacement_scale
```

### **6.3 Regime**
```
rb_regime_hint
```

### **6.4 Route proposal**
```
rb_route_proposal
```

These encode:

- semantic adjacency  
- identity adjacency  
- referent adjacency  
- routing pressure  
- routing stability  
- routing escalation  

RB’s invariants show how A × B shaped routing.

---

# **7. How Residues Appear in Cognitive‑History**

Residues appear through:

### **7.1 Structural residue**
```
R_res
```

### **7.2 IdOB residue**
```
idob_residue
```

### **7.3 Coherence**
```
C_coh
```

Residues encode:

- contradiction  
- correction  
- planning  
- semantic adjacency  
- constraint pressure  

Residues are the **semantic evidence** IdOB uses.

---

# **8. How Continuity Appears in Cognitive‑History**

Continuity appears through:

### **8.1 Continuity invariant**
```
P_cont
```

### **8.2 Identity stability**
```
I_stab
idob_stability
```

### **8.3 Routing adjacency**
```
Rt_adj
rb_adjacency_class
```

Continuity invariants encode:

- topic continuity  
- referent continuity  
- identity continuity  
- stance continuity  
- direction continuity  

Continuity is the **semantic glue** across turns.

---

# **9. How Identity Appears in Cognitive‑History**

Identity appears through:

### **9.1 Identity geometry**
```
idob_geometry
```

### **9.2 Identity roles**
```
idob_roles
```

### **9.3 Identity stability**
```
idob_stability
I_stab
```

Identity invariants encode:

- who is speaking  
- what they know  
- what they believe  
- what TS has committed  
- how identity changed  
- how identity stabilized  

Identity is the **cognitive glue** across turns.

---

# **10. Worked Example — Cognitive‑History Entry for a Meaning Conflict**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: literal correction  
- B: identity threat + semantic conflict + high importance  

### **Cognitive‑history entry (conceptual):**

```
cycle_id: 42
timestamp: ...
invariants: {
    I_stab: unstable,
    R_res: contradiction,
    P_cont: backward_motion,
    L_depth: medium,
    Rt_adj: non_local,
    ΔH: high,
    E_dens: rising,
    C_coh: correction
}
idob_geometry: {
    neighborhood: identity_defense,
    k_id: stable_core
}
idob_roles: correction_role
idob_residue: contradiction_residue
idob_stability: stabilizing
rb_adjacency_class: non_local
rb_displacement_scale: large
rb_regime_hint: Transition
rb_route_proposal: IdOB_cycle_required
```

This entry is **deterministic**, **bounded**, **canonical**, and **replay‑safe**.

It is the historical record of how A × B shaped meaning.

---

# **11. Summary**

Appendix F shows:

- how A (stated content) appears in cognitive‑history  
- how B (context) appears in cognitive‑history  
- how IdOB refinement appears in cognitive‑history  
- how routing appears in cognitive‑history  
- how residues appear in cognitive‑history  
- how continuity appears in cognitive‑history  
- how identity appears in cognitive‑history  

Cognitive‑history is the **replay‑deterministic log** of meaning coupling.

It is the **historical backbone** of TS.

---

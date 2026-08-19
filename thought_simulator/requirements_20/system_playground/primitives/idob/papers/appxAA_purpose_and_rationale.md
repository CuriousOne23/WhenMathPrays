# **Appendix AA — How A × B Drives the IdOB Cycle Itself**  
### *The Deterministic Interaction Between Meaning Coupling and the Full IdOB → MCB → TP Loop*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix AA explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

drives the **entire IdOB cycle**, including:

- how IdOB interprets A × B  
- how IdOB emits geometry, roles, continuity, stance, direction, residues, freezes, importance  
- how MCB writes these into TP metadata  
- how TP metadata becomes next‑turn context  
- how next‑turn context shapes the next A × B  
- how the cycle repeats deterministically  

This appendix shows the **full semantic engine** of TS.

---

# **2. The IdOB Cycle (High‑Level Overview)**

The IdOB cycle is:

1. **User produces A (stated content).**  
2. **TS provides B (context).**  
3. **IdOB computes A × B.**  
4. **IdOB emits geometry, roles, continuity, stance, direction, residues, freezes, importance.**  
5. **MCB writes these into TP metadata.**  
6. **TP metadata becomes next‑turn context.**  
7. **Next A × B uses updated context.**  
8. **Cycle repeats.**

The IdOB cycle is:

- deterministic  
- replay‑safe  
- geometry‑driven  
- pressure‑driven  
- continuity‑driven  

It is the **semantic heartbeat** of TS.

---

# **3. Step 1 — A (Stated Content)**

A is the raw user utterance.

A contains:

- propositions  
- corrections  
- contradictions  
- affirmations  
- clarifications  
- referent markers  
- identity markers  
- topic markers  
- coherence markers  
- continuity markers  
- pressure markers  

A is the **input vector**.

---

# **4. Step 2 — B (Context)**

B is the full context TS provides:

- identity geometry  
- topic geometry  
- referent continuity  
- coherence geometry  
- continuity geometry  
- stance_next  
- direction_next  
- semantic‑importance  
- adjacency  
- displacement  
- routing regime  
- freeze‑propagation  
- basin/surface state  

B is the **context vector**.

---

# **5. Step 3 — IdOB Computes A × B**

IdOB computes:

$$
\text{Meaning} = A \times B
$$

This produces:

- identity roles  
- topic roles  
- referent roles  
- coherence roles  
- continuity roles  
- stance_next  
- direction_next  
- semantic‑importance.next  
- adjacency  
- displacement  
- routing hints  
- freeze signatures  
- basin/surface classification  
- geometry updates  

IdOB is the **semantic interpreter**.

---

# **6. Step 4 — IdOB Emits Geometry and Roles**

IdOB emits:

### **6.1 Geometry**
- identity geometry  
- topic geometry  
- coherence geometry  
- continuity geometry  

### **6.2 Roles**
- identity roles  
- topic roles  
- referent roles  
- coherence roles  
- continuity roles  

### **6.3 Motion**
- stance_next  
- direction_next  

### **6.4 Pressure**
- semantic‑importance  
- curvature  
- entropy  

### **6.5 Routing**
- adjacency  
- displacement  
- regime hints  

### **6.6 Safety**
- freeze signatures  
- freeze‑propagation  
- commit eligibility  

IdOB is the **semantic emitter**.

---

# **7. Step 5 — MCB Writes Metadata into TP**

MCB writes IdOB outputs into:

```
TP.metadata.identity.geometry
TP.metadata.topic.geometry
TP.metadata.coherence.geometry
TP.metadata.continuity.geometry

TP.metadata.idob_roles[]
TP.metadata.next_context_metadata.stance_next
TP.metadata.next_context_metadata.direction_next

TP.metadata.semantic_importance.current
TP.metadata.semantic_importance.next

TP.metadata.routing.adjacency
TP.metadata.routing.displacement
TP.metadata.routing.regime

TP.metadata.freeze.current
TP.metadata.freeze.next
TP.metadata.freeze.propagation

TP.metadata.commit.eligible
TP.metadata.commit.reason

TP.metadata.global_geometry.basin_state
TP.metadata.global_geometry.surface_state
```

MCB is the **semantic recorder**.

---

# **8. Step 6 — TP Metadata Becomes Next‑Turn Context**

The metadata written by MCB becomes the next B:

- identity geometry → identity continuity  
- topic geometry → topic continuity  
- referent continuity → referent stability  
- coherence geometry → coherence stability  
- continuity geometry → temporal stability  
- stance_next → next stance  
- direction_next → next motion  
- semantic‑importance → next pressure  
- adjacency/displacement → next routing  
- freeze‑propagation → next safety state  
- basin/surface → next global geometry  

TP metadata is the **context engine**.

---

# **9. Step 7 — Next A × B Uses Updated Context**

The next user utterance A interacts with updated B:

- new identity geometry  
- new topic geometry  
- new referent continuity  
- new coherence geometry  
- new continuity geometry  
- new stance_next  
- new direction_next  
- new semantic‑importance  
- new adjacency/displacement  
- new freeze‑propagation  
- new basin/surface state  

This produces the next IdOB cycle.

The cycle is **self‑updating**.

---

# **10. Step 8 — Cycle Repeats**

The IdOB cycle repeats deterministically:

$$
A \times B \rightarrow \text{IdOB} \rightarrow \text{MCB} \rightarrow \text{TP} \rightarrow B_{\text{next}} \rightarrow A_{\text{next}} \times B_{\text{next}}
$$

This produces:

- stable meaning  
- stable identity  
- stable topic  
- stable referents  
- stable coherence  
- stable continuity  
- stable routing  
- stable commit  
- stable replay  

The cycle is the **semantic engine** of TS.

---

# **11. Worked Example — Full IdOB Cycle**

### **Utterance:**  
“That’s not what I meant.”

### **A × B coupling:**  
- A: correction  
- B: identity threat + referent ambiguity + topic conflict + high curvature + high entropy  

### **IdOB emits:**

- identity roles: correction_role + identity_role  
- topic roles: topic_correction_role + topic_conflict_role  
- referent continuity: conflict  
- coherence geometry: coh_correction  
- continuity geometry: cont_correction  
- stance_next: corrective  
- direction_next: backward  
- semantic‑importance: high  
- adjacency: non_local  
- displacement: large  
- freeze: identity_freeze + referent_freeze  
- commit: blocked  
- basin/surface: transition_surface  

### **MCB writes metadata.**

### **Next B contains:**

- identity_defense  
- topic_correction  
- referent_conflict  
- coh_correction  
- cont_correction  
- stance_next = corrective  
- direction_next = backward  
- importance_next = high  
- adjacency = non_local  
- displacement = large  
- freeze = active  
- surface_state = transition_surface  

### **Next A × B uses updated context.**

The cycle continues.

---

# **12. Summary**

Appendix AA shows how:

- **A (stated content)**  
- **B (context)**  

drive the **entire IdOB cycle**, including:

- geometry  
- roles  
- continuity  
- stance  
- direction  
- importance  
- routing  
- freezes  
- commit  
- basins/surfaces  

The IdOB cycle is the **semantic heartbeat** of TS.  
It ensures:

- meaning stability  
- identity stability  
- topic stability  
- referent stability  
- coherence stability  
- continuity stability  
- routing stability  
- commit stability  
- replay determinism  

The IdOB cycle is the **core engine** of TS.

---

# **TS Continuity Theory**  
### *A Formal Model of Temporal Stability, Meaning Evolution, and Deterministic Cognition*

This paper defines **continuity** — the rules and constraints governing how meaning evolves from one turn to the next inside the Thought Simulator (TS).

It builds directly on *difficulty_of_meaning.md* and *ts_meaning_theory.md*, and supplies the temporal backbone of TS’s cognitive architecture.

Continuity is essential for:

- deterministic cognition  
- identity stability  
- referent stability  
- replay determinism  
- long-horizon reasoning  
- coherent conversation  

TS cannot function without continuity.  
This paper formalizes it.

---

# **1. Introduction**

Continuity is the property that ensures:

> **A conversation at turn $t+1$ is meaningfully connected to turn $t$.**

Human cognition achieves continuity implicitly.  
TS must achieve it explicitly, deterministically, and with bounded state.

Continuity theory defines:

1. the continuity function  
2. the continuity constraints  
3. how continuity interacts with canonical meaning  
4. how continuity absorbs residual canonicalization error  
5. how continuity supports identity  
6. how continuity supports replay determinism  
7. how continuity routes meaning through the TP layers  
8. where continuity is extendable  

Continuity operates on **canonical** meaning states.  
It does not operate directly on raw meaning.

---

# **2. The Continuity Function**

Continuity is defined structurally as:

$$
C_{t+1} = f(M_t, M_{t+1})
$$

Where:

- $M_t$ = canonical meaning at turn $t$  
- $M_{t+1}$ = canonical meaning at turn $t+1$  
- $f$ = deterministic continuity function  

The equation is structural: it names the required relationship.  
Concrete realizations of $f$ (rules, metrics, thresholds, or soft constraints) are left to later specification.

Continuity is not a scalar.  
It is a **relationship** between successive meaning states.

Continuity requires that:

- changes are bounded  
- transitions are deterministic  
- identity is preserved  
- referents remain stable  
- commitments remain valid  
- importance is respected  
- topic drift is controlled  

Continuity is the temporal constraint system of TS.

---

# **3. Continuity Constraints**

Continuity is enforced across multiple invariant attributes of meaning.

TS requires continuity over:

### **3.1 Topic Continuity**
Topic drift must be bounded, explainable, and connected to prior meaning.

### **3.2 Intent Continuity**
Intent must evolve coherently (e.g., questions → answers, requests → fulfillment).

### **3.3 Stance Continuity**
Stance must remain stable unless an explicit change is signaled.

### **3.4 Referent Continuity**
Referents (“he”, “that idea”, “the previous assumption”) must remain stable.  
Referent continuity is essential for identity and replay.

### **3.5 Identity Continuity**
Identity continuity ensures that who is speaking, what they know, what they believe, and what TS has committed remain coherent across turns.

**Division of labor:**  
Continuity Theory governs the temporal relationship and cross‑attribute constraints involving identity.  
Identity Theory defines the internal structure and update rules of identity itself.

### **3.6 Importance Continuity (Expanded)**
Importance continuity ensures that:

- high‑importance items remain active until explicitly resolved  
- commitments cannot be silently dropped  
- constraints remain in force until satisfied  
- low‑importance items cannot override high‑importance ones  
- long‑horizon reasoning remains stable  

Importance continuity is one of the strongest determinism constraints in TS.  
It prevents TS from losing track of critical commitments or shifting priorities unpredictably.

These constraints are currently qualitative.  
Quantitative thresholds or soft scoring methods will be defined in later specification work.

---

# **4. Continuity and Canonicalization**

Canonicalization is lossy.  
Continuity is the mechanism that absorbs and corrects residual discrepancy.

Residual error is structured — it is not a numeric difference but a set of per‑attribute deviations.

### **Concrete Example (Added)**  
Suppose raw meaning suggests a slight positive stance shift (“agree-ish”), but canonicalization maps stance to **neutral**.  
Continuity may:

- preserve the prior stance (“neutral”) if the shift is weak or transient  
- update stance only if the shift persists across multiple turns  
- flag the shift for clarification if it contradicts prior commitments  

This illustrates how continuity stabilizes meaning across turns.

Continuity keeps residual deviations bounded by:

- enforcing bounded transitions  
- maintaining referent stability  
- maintaining identity coherence  
- preserving commitments  
- smoothing or flagging unexplained drift  

Continuity is the error‑stabilization layer of the meaning pipeline.

---

# **5. Continuity and Identity**

Continuity and identity are tightly coupled.

Identity continuity is expressed structurally as:

$$
I_{t+1} = g(I_t, M_t)
$$

Continuity ensures that identity does not drift unboundedly, that referents remain usable, that commitments remain valid, and that provenance and freeze signatures remain consistent.

Continuity supplies the temporal stabilizer for identity.  
Identity Theory supplies the internal model of identity itself.

---

# **6. Continuity and Replay Determinism**

Replay determinism requires:

$$
M_t = \mathrm{Replay}(M_t)
$$

Continuity contributes the necessary temporal guarantees:

- meaning transitions are deterministic  
- identity transitions are deterministic  
- referent transitions are deterministic  
- commitment state evolves deterministically  

Without deterministic continuity, replay determinism cannot be maintained across turns.

---

# **7. Continuity and Routing (Expanded)**

Continuity is a major routing substrate for the TP layers.

Routing decisions depend on whether changes in meaning are:

- expected  
- anomalous  
- ambiguous  
- contradictory  
- commitment‑relevant  
- identity‑relevant  

Examples:

- **Expected drift** (e.g., topic refinement) routes through the semantic layer.  
- **Ambiguous drift** (e.g., unclear stance change) routes through the alignment or clarification layer.  
- **Commitment‑relevant drift** routes through the commit layer.  
- **Identity‑relevant drift** routes through the identity layer.

Continuity provides the signals that allow routing to be deterministic and meaning‑driven.

---

# **8. Extendability of Continuity**

Continuity is intentionally extendable.

- New invariants may be incorporated once they satisfy TS’s six criteria.  
- Additional stability constraints may be added.  
- New routing conditions may be supported.  
- New identity‑related signals (provenance types, freeze signatures) may be integrated.

Continuity is a framework, not a closed rule set.

---

# **9. Why Continuity Enables Laptop‑Scale Cognition (Strengthened)**

Continuity allows TS to:

- avoid recomputing meaning from scratch  
- avoid semantic drift  
- avoid identity drift  
- avoid referent drift  
- keep state bounded  
- maintain deterministic transitions  

The key insight:

> **Continuity prevents combinatorial explosion by ensuring that each turn builds deterministically on the previous one.**

This temporal compression mechanism is one of the reasons TS can operate at laptop scale rather than requiring trillion‑parameter models.

---

# **10. Relationship to Historical Work (Expanded)**

Continuity theory draws on ideas from:

- discourse coherence  
- adjacency pairs  
- situation models  
- schema theory  
- dialogue‑state tracking  

**Clarification (Added):**  
Dialogue‑state tracking identifies some invariants, but does not integrate them into a deterministic raw → canonical pipeline with replay guarantees.

TS’s contribution lies in the integration of continuity with:

- canonical meaning  
- invariant attributes  
- identity continuity  
- replay determinism  
- laptop‑scale constraints  

---

# **11. Conclusion**

Continuity theory defines:

- how meaning evolves  
- how residual canonicalization discrepancy is stabilized  
- how identity and referents remain coherent  
- how commitments remain valid  
- how replay determinism is supported  
- how continuity participates in routing  
- how TS achieves bounded, deterministic, laptop‑scale cognition  

Continuity is the temporal backbone of TS.  
It supports identity theory, routing theory, and commit theory.

---

# **End of ts_continuity_theory.md (Revised)**

---

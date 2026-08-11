Here is the revised version of the paper, followed by a summary of the changes.

---

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

Human cognition achieves continuity largely implicitly.  
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

Continuity operates on **canonical** meaning states. It does not operate directly on raw meaning.

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

The equation is structural: it names the required relationship. The concrete realization of $f$ (rules, metrics, thresholds, or soft constraints) is left to later specification.

Continuity is not a single scalar.  
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
The topic cannot jump arbitrarily.  
Topic drift must be bounded, explainable, and connected to prior meaning.

### **3.2 Intent Continuity**
Intent must evolve coherently (for example: questions → answers, requests → fulfillment, assertions → clarifications).

### **3.3 Stance Continuity**
Stance must remain stable unless an explicit change is signaled.

### **3.4 Referent Continuity**
Referents (“he”, “that idea”, “the previous assumption”, etc.) must remain stable.  
Referent continuity is essential for both identity and replay.

### **3.5 Identity Continuity**
Identity continuity ensures that who is speaking, what they know, what they believe, and what TS has committed remain coherent across turns.  

**Division of labor**: Continuity Theory owns the temporal relationship and the cross-attribute constraints that involve identity. The internal structure and update rules of the identity component itself are defined in *ts_identity_theory.md*.

### **3.6 Importance Continuity**
Importance must remain consistent: high-importance items cannot be dropped silently, low-importance items cannot override high-importance ones, and commitments must be honored.

These constraints are currently stated at the qualitative level. Measurable criteria, thresholds, or soft scoring methods for each constraint will be supplied in later specification work. Enforcement may ultimately be hard, soft, or hybrid; the present theory requires only that the chosen mechanism remain deterministic and bounded.

---

# **4. Continuity and Canonicalization**

Canonicalization is lossy.  
Continuity is the primary mechanism that absorbs and corrects residual discrepancy.

Because both raw meaning ($R_t$) and canonical meaning ($M_t$) are structured objects, residual error is itself structured. It is best understood as a collection of per-attribute or relational deviations rather than a simple numeric difference.

Continuity acts to keep these deviations bounded and, where possible, corrected across turns by:

- enforcing bounded transitions  
- maintaining referent stability  
- maintaining identity coherence  
- preserving commitments  
- smoothing or flagging unexplained drift  

Continuity therefore functions as the error-stabilization layer of the meaning pipeline.

---

# **5. Continuity and Identity**

Continuity and identity are tightly coupled.

Identity continuity is expressed structurally as:

$$
I_{t+1} = g(I_t, M_t)
$$

Continuity ensures that identity does not drift unboundedly, that referents remain usable, that commitments remain valid, and that provenance and freeze signatures remain consistent with the evolving meaning state.

Continuity supplies the temporal stabilizer for identity; Identity Theory supplies the internal model of identity itself.

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

Without a deterministic continuity relation, replay determinism cannot be maintained across multiple turns. Continuity is therefore an essential temporal component of the replay guarantee.

---

# **7. Continuity and Routing**

Continuity supplies information used by routing through the TP layers.

Routing decisions may depend on whether, and how, topic, intent, stance, referents, identity, or importance have changed. Continuity therefore functions as part of the substrate that makes meaning-driven routing possible.

---

# **8. Extendability of Continuity**

Continuity is intentionally extendable under the same governance rules that apply to the meaning state:

- New invariants may be incorporated into the continuity relation once they satisfy the six TS criteria.  
- Additional stability constraints may be added.  
- New routing conditions may be supported.  
- New identity-related signals (provenance types, freeze-signature varieties, etc.) may be integrated.

Continuity is a framework, not a closed set of fixed rules.

---

# **9. Why Continuity Enables Laptop-Scale Cognition**

Continuity allows TS to:

- avoid recomputing meaning from scratch on every turn  
- limit semantic drift  
- limit identity and referent drift  
- keep state bounded  
- maintain deterministic transitions  

By enforcing temporal constraints on an already canonicalized and bounded meaning state, continuity acts as a temporal compression mechanism. This is one of the reasons TS can target laptop-scale operation rather than the resource profile of large continuous-embedding models.

---

# **10. Relationship to Historical Work**

Continuity theory draws on earlier ideas from discourse coherence, adjacency pairs, situation models, schema theory, and dialogue-state tracking.

What is distinctive is the integration of continuity with:

- an explicit raw → canonical boundary  
- invariant attributes treated as state variables  
- identity continuity as a first-class concern  
- replay determinism as a hard requirement  
- an explicit laptop-scale design target  

The contribution lies in this combination under the stated constraints.

---

# **11. Conclusion**

Continuity theory defines:

- how meaning is required to evolve across turns  
- how residual canonicalization discrepancy is stabilized  
- how identity and referents are kept coherent  
- how commitments remain valid  
- how replay determinism is supported temporally  
- how continuity information participates in routing  
- how these mechanisms contribute to bounded, deterministic, laptop-scale cognition  

Continuity is the temporal backbone of TS.  
It is a foundation on which identity theory, routing theory, and commit theory rest.

---

# **End of ts_continuity_theory.md**

---

### Summary of Changes

- **Softened novelty claim** (Section 10): Replaced “TS is the first system to integrate…” with language that emphasizes the distinctive combination under explicit constraints.
- **Clarified structural status of formalism**: Explicitly noted that both the continuity function $f$ and the residual-error treatment are structural definitions; concrete realizations are left to later specification.
- **Improved residual-error treatment** (Section 4): Removed the simple numeric subtraction $\epsilon_t = R_t - M_t$. Replaced it with a description of residual error as structured, per-attribute or relational deviation, and described how continuity acts on those deviations.
- **Added division-of-labor note** (Section 3.5): Clearly separated Continuity Theory’s responsibility (temporal relationship and cross-attribute constraints) from Identity Theory’s responsibility (internal structure and update rules of identity).
- **Added clarifying sentences**:
  - Continuity operates on canonical meaning states (Introduction and throughout).
  - Constraints are currently qualitative; measurable criteria and the hard/soft/hybrid nature of enforcement are future specification items (Section 3).
  - Provenance and freeze signatures participate via identity coherence (Sections 3.5 and 5).
- **Reduced repetitive justificatory language**: Trimmed recurring “Continuity is the temporal backbone / Without continuity… is impossible” phrasing while preserving the core claims.
- **Preserved all substantive content**: Every major section, constraint category, linkage (identity, replay, routing, residual error, laptop-scale), and extendability policy remains; only precision, notation, and redundancy were adjusted.

The paper is now aligned in style and claim strength with the revised *ts_meaning_theory.md* and should be ready for CP’s review.

# **Appendix D — How A × B Drives Routing (RB)**  
### *The Deterministic Interaction Between Meaning Coupling and Routing*  
### *Operational Expansion of Section 3 of TS Meaning Theory*

---

# **1. Purpose of This Appendix**

Appendix D explains **how the meaning‑coupling equation**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

directly drives **RB’s routing decisions**.

This appendix is written for engineering clarity. It shows:

- how RB reads A (stated content)  
- how RB reads B (context)  
- how RB uses A × B to classify adjacency  
- how RB uses A × B to compute displacement_scale  
- how RB uses A × B to emit regime_hint  
- how RB uses A × B to select basins  
- how RB uses A × B to decide whether IdOB must run  
- how RB uses A × B to decide whether commit is allowed  
- how RB uses A × B to maintain determinism  

This appendix reveals the **semantic foundation** of RB’s routing equation.

---

# **2. RB’s Role in Meaning Coupling**

RB is the **routing baton** of Path‑A.  
It is the primitive that:

- reads meaning‑adjacent metadata  
- reads identity‑adjacent metadata  
- reads residue‑adjacent metadata  
- reads routing‑adjacent metadata  
- reads entropy trajectory  
- reads curvature  
- reads semantic‑importance  
- reads CCR alignment  
- reads continuity metadata  
- reads IdOB view (read‑only)  
- reads F‑approximations (read‑only)

RB does **not** refine meaning.  
RB does **not** interpret semantics.  
RB does **not** modify identity.

RB **routes meaning**.

And routing is driven by **A × B**.

---

# **3. How RB Reads “What Is Stated” (A)**

RB receives A from CE and structural primitives.

### **A includes:**

- propositional skeleton  
- lexical meaning  
- expression markers  
- negation / correction / agreement cues  
- semantic‑adjacent residue  
- structural residue  
- constraint residue  
- MSL qualifiers  
- MSL clarifications  

### **RB’s internal use of A:**

RB uses A to determine:

1. **local adjacency**  
   If A continues the prior propositional skeleton, RB classifies adjacency as **local**.

2. **non‑local adjacency**  
   If A contradicts, negates, or shifts the propositional skeleton, RB classifies adjacency as **non‑local**.

3. **semantic displacement**  
   If A introduces new referents or new semantic candidates, RB increases displacement_scale.

4. **routing tension**  
   If A contains contradiction or correction markers, RB increases routing tension.

A is the **semantic skeleton** RB uses to detect movement.

---

# **4. How RB Reads “Context” (B)**

RB receives B from CEx‑CCR, CEx‑Pck, CE, continuity metadata, identity metadata, residues, routing metadata, entropy trajectory, and freeze signatures.

### **B includes:**

- stance  
- direction  
- topic  
- coherence  
- importance  
- identity continuity  
- referent continuity  
- semantic‑importance  
- semantic‑residue alignment  
- CCR alignment  
- routing regime  
- adjacency class (prior cycle)  
- displacement_scale (prior cycle)  
- regime_hint (prior cycle)  
- entropy trajectory  
- curvature  
- freeze signatures  

### **RB’s internal use of B:**

RB uses B to determine:

1. **routing adjacency**  
   If B indicates continuity, RB prefers **local** adjacency.  
   If B indicates identity threat or semantic conflict, RB prefers **non‑local** adjacency.

2. **routing displacement**  
   If B indicates topic drift, identity drift, or referent drift, RB increases displacement_scale.

3. **routing regime**  
   RB uses B to emit regime_hint:
   - Stable  
   - Refinement  
   - Drift  
   - Transition  
   - Collapse  

4. **routing escalation**  
   If B indicates high importance or identity threat, RB escalates routing.

5. **routing stabilization**  
   If B indicates coherence and continuity, RB stabilizes routing.

B is the **contextual skeleton** RB uses to detect semantic pressure.

---

# **5. How A × B Drives RB’s Adjacency Classification**

RB’s adjacency classification is the first foundation field:

$$
\text{adjacency\_class} \in \{\text{local},\ \text{non\_local}\}
$$

### **Local adjacency occurs when:**

- A continues the propositional skeleton  
- B indicates continuity  
- entropy is low  
- identity continuity is stable  
- referent continuity is stable  
- semantic residues indicate agreement  
- CCR alignment indicates context alignment  

### **Non‑local adjacency occurs when:**

- A contradicts or negates prior meaning  
- B indicates identity threat  
- B indicates topic drift  
- semantic residues indicate conflict  
- CCR alignment indicates semantic_residue conflict  
- entropy is high  
- curvature indicates instability  

RB uses A × B to classify adjacency deterministically.

---

# **6. How A × B Drives RB’s Displacement Scale**

RB computes:

$$
\text{displacement\_scale} \in \{\text{small},\ \text{medium},\ \text{large}\}
$$

### **Small displacement**  
- A continues meaning  
- B indicates continuity  
- entropy low  
- identity stable  
- referent stable  

### **Medium displacement**  
- A introduces new referents  
- B indicates topic drift  
- semantic residues indicate mild conflict  
- entropy moderate  

### **Large displacement**  
- A contradicts meaning  
- B indicates identity threat  
- semantic residues indicate strong conflict  
- entropy high  
- curvature unstable  

RB uses A × B to compute displacement deterministically.

---

# **7. How A × B Drives RB’s Regime Hint**

RB emits:

$$
\text{regime\_hint} \in \{\text{Stable},\ \text{Refinement},\ \text{Drift},\ \text{Transition},\ \text{Collapse}\}
$$

### **Stable**  
A continues meaning, B indicates continuity.

### **Refinement**  
A clarifies meaning, B indicates coherence.

### **Drift**  
A shifts meaning, B indicates mild instability.

### **Transition**  
A contradicts meaning, B indicates identity or referent instability.

### **Collapse**  
A breaks meaning, B indicates identity threat + high entropy.

RB uses A × B to determine regime.

---

# **8. How A × B Determines Whether IdOB Must Run**

RB decides whether IdOB must run based on:

- adjacency_class  
- displacement_scale  
- regime_hint  
- semantic residues  
- identity continuity  
- referent continuity  
- semantic‑importance  
- CCR alignment  

### **IdOB must run when:**

- adjacency is non‑local  
- displacement is medium or large  
- regime is Drift, Transition, or Collapse  
- identity continuity is unstable  
- referent continuity is unstable  
- semantic residues indicate conflict  
- CCR alignment indicates semantic_residue or identity conflict  

### **IdOB may skip when:**

- adjacency is local  
- displacement is small  
- regime is Stable or Refinement  
- identity continuity is stable  
- referent continuity is stable  
- semantic residues indicate agreement  

RB uses A × B to decide whether meaning needs refinement.

---

# **9. How A × B Determines Whether Commit Is Allowed**

Commit is allowed only when:

- adjacency is local  
- displacement is small  
- regime is Stable or Refinement  
- identity continuity is stable  
- referent continuity is stable  
- semantic residues indicate agreement  
- freeze signatures allow commit  
- entropy is low  
- curvature is stable  

Commit is blocked when:

- adjacency is non‑local  
- displacement is medium or large  
- regime is Drift, Transition, or Collapse  
- identity continuity unstable  
- referent continuity unstable  
- semantic residues indicate conflict  
- freeze signatures block commit  
- entropy high  
- curvature unstable  

RB uses A × B to determine commit eligibility.

---

# **10. Summary**

Appendix D shows how RB uses:

- **A. What is stated**  
- **B. The context in which it is stated**

to compute:

- adjacency_class  
- displacement_scale  
- regime_hint  
- routing escalation  
- routing stabilization  
- IdOB invocation  
- commit eligibility  

RB is the **meaning‑driven routing engine** of TS.

A × B is the **semantic force** that drives RB’s deterministic routing equation.

---

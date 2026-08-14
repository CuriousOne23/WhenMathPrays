# **Identity Basin (IdOB)**  
### *The Identity‑Conditioned Meaning Layer of Path‑A*

The Identity Basin (IdOB) is the deterministic, bounded, replay‑safe mechanism that performs identity‑conditioned meaning construction inside Path‑A. It integrates:

- referent refinement  
- qualifier interpretation  
- subculture assignment  
- stance / direction / coherence refinement  
- semantic‑importance refinement  
- identity continuity flags  
- commitments  
- freeze signatures  
- context metadata  
- semantic‑adjacent and semantic‑layer cues  

IdOB is the **only** primitive in Path‑A that updates identity‑conditioned meaning. It is the operational realization of TS Identity Theory.

This paper defines:

1. the purpose of IdOB  
2. IdOB inputs  
3. IdOB outputs  
4. IdOB internal responsibilities  
5. IdOB cycles  
6. IdOB interaction with routing  
7. IdOB interaction with continuity and identity theory  
8. IdOB interaction with commitments and freeze signatures  
9. IdOB interaction with the Context Frame  
10. deterministic invariants  
11. extendability  

IdOB is the identity engine of the Thought Pipeline.

---

# **1. Purpose of IdOB**

IdOB exists to:

- refine referents deterministically  
- interpret qualifiers and qualifier clusters  
- assign or refine subculture  
- refine stance, direction, and coherence  
- refine semantic‑importance entities and facts  
- enforce identity continuity  
- enforce commitments  
- enforce freeze signatures  
- produce identity‑conditioned meaning metadata  
- stabilize identity‑conditioned meaning before commit  

IdOB is the identity‑conditioned interpretation layer of Path‑A.

---

# **2. Inputs to IdOB**

IdOB consumes signals from multiple layers:

### **2.1 Context Layer (CEx → CE)**
- stabilized Context Frame  
- clarifying metadata  
- MSL tokens  
- next_context  
- continuity signals  
- identity continuity flags  

### **2.2 OB Family (SOB → SROB → CnOB → SmOB → SSG → STPX)**
- structural residue  
- constraint residue  
- semantic‑adjacent cues  
- semantic‑layer cues  
- semantic‑importance residues  
- semantic‑layer hash  
- frame‑compatible markers  
- **IdOB consumes the fully refined OB residue, ensuring identity‑conditioned interpretation is based on stabilized structural, constraint, semantic‑adjacent, and semantic‑layer cues.**

### **2.3 Identity Layer**
- referent lineage  
- qualifier lineage  
- subculture continuity  
- stance / direction / coherence continuity  
- commitments  
- freeze signatures  
- identity continuity flags  

### **2.4 Routing Layer (RB → TR → DCB → RBU)**
- basin selection  
- routing vector TP.TR  
- curvature signals  
- routing update state  

IdOB integrates these signals deterministically.

**Ownership note**  
Identity is the authoritative owner of referents, provenance, freeze signatures, and related identity‑conditioned attributes. Meaning holds projections. IdOB updates the authoritative identity‑side representations; consistency with meaning‑state projections is maintained through the update and continuity mechanisms.

---

# **3. Outputs of IdOB**

IdOB produces:

### **3.1 Refined referents**
- referent lineage, stability, disambiguation, and conflict resolution  

### **3.2 Refined qualifiers**
- qualifier interpretation, clusters, lineage, and qualifier‑driven meaning shifts  

### **3.3 Refined subculture**
- assignment, continuity, and shifts  

### **3.4 Refined stance, direction, coherence**
- stance, direction, and coherence refinements  

### **3.5 Refined semantic‑importance**
- entities, facts, and continuity  

### **3.6 Identity continuity flags**
- raised when additional identity‑conditioned cycles are required  
- cleared when identity is stable  

### **3.7 Identity‑conditioned metadata**
- written into TP metadata fields  
- consumed by the long‑term conversation components (COB, CST‑CORE, CST‑MS, CST‑MUX)  

### **3.8 Contribution to next_context**
IdOB produces the identity‑conditioned payload (qualifiers, clarifications, stance/direction/coherence, subculture, and related metadata).  
**MCB** packages and writes the next_context field. IdOB does not itself perform the write.  
**IdOB’s identity‑conditioned outputs become part of the next turn’s Context Frame via MCB.**

IdOB is the sole producer of identity‑conditioned meaning content.

---

# **4. Internal Responsibilities of IdOB**

IdOB performs five core responsibilities:

### **4.1 Referent Refinement**
Resolves ambiguous, conflicting, or underspecified referents and maintains referent lineage continuity. Refinement is deterministic and replay‑safe.

### **4.2 Qualifier Interpretation**
Interprets qualifiers and qualifier clusters, tracks qualifier lineage, and accounts for qualifier‑driven meaning shifts. Qualifiers are treated as identity‑conditioned signals.

### **4.3 Subculture Assignment**
Assigns or refines subculture and maintains subculture continuity. Subculture is an identity‑conditioned attribute.

### **4.4 Stance / Direction / Coherence Refinement**
Refines stance, direction, and coherence as identity‑conditioned attributes.

### **4.5 Semantic‑Importance Refinement**
Refines semantic‑importance entities and facts and maintains their continuity as identity‑conditioned metadata.

---

# **5. IdOB Cycles**

IdOB may run multiple cycles within a single turn.

Cycles are triggered when:

- referents, qualifiers, subculture, stance/direction/coherence, or semantic‑importance require refinement  
- identity continuity flags are raised  
- freeze‑signature conflicts exist  
- commitments require enforcement  
- routing selects the identity basin  

**Conflict handling**  
Unresolved freeze‑signature or commitment conflicts raise (or keep raised) identity continuity flags and force additional IdOB cycles until the conflicts are resolved or stably carried.

Cycles continue until:

- identity is stable  
- continuity requirements are satisfied  
- freeze signatures are respected  
- commitments are stable or stably carried  
- curvature and semantic‑layer cues are acceptable  
- routing selects the commit path  

IdOB cycles are deterministic.  
**Commit gating provides the deterministic termination condition for IdOB recursion.**

---

# **6. IdOB and Routing**

Routing determines when IdOB must run.

IdOB is selected when identity continuity flags are raised, referent or qualifier conflicts exist, subculture / stance / direction / coherence shifts are detected, semantic‑importance refinement is required, freeze‑signature conflicts exist, commitments require enforcement, or semantic‑layer cues require identity‑conditioned interpretation.

Routing bounds IdOB recursion by selecting identity cycles only when identity‑conditioned meaning construction is required.

---

# **7. IdOB and Continuity Theory**

IdOB operationalizes continuity constraints that involve identity‑conditioned attributes by:

- resolving relevant drift  
- stabilizing referents, commitments, qualifiers, stance/direction/coherence, subculture, and semantic‑importance  
- clearing or stably carrying identity continuity flags  

It is the primary operational realization of the identity‑related portion of Continuity Theory inside Path‑A.

---

# **8. IdOB and Identity Theory**

IdOB is the operational realization of Identity Theory. It maintains identity continuity, referent and qualifier lineage, subculture continuity, and stance/direction/coherence continuity; enforces commitments and freeze signatures; and produces or clears identity continuity flags.

---

# **9. IdOB and Commit**

Commit occurs only after required IdOB cycles have completed and the relevant identity‑conditioned refinements are stable (or stably open), with identity continuity flags cleared or consistently carried and freeze‑signature conflicts resolved.

Commit terminates the identity‑conditioned meaning construction phase of the current turn.

---

# **10. IdOB and the Context Frame**

IdOB consumes the stabilized Context Frame:

$$
\mathrm{ContextFrame}_t = h(M_t, I_t, C_t)
$$

It uses the stabilized topic, intent, stance, referents, commitments, importance, identity continuity flags, freeze‑signature status, clarifying metadata, and related fields.

IdOB’s identity‑conditioned outputs contribute to the metadata that the long‑term conversation layer and the next turn’s Context & Relevance Layer will consume.

---

# **11. Deterministic Invariants**

- **Deterministic ordering** — IdOB cycles occur only when routing selects the identity basin.  
- **Replay determinism** — IdOB is a deterministic function of the available signals (Context Frame, identity state, continuity signals, OB residue, semantic cues, identity flags, curvature).  
- **No global state leakage** — IdOB reads only TP‑stream fields and explicitly supplied signals.  
- **Identity‑conditioned stability** — Identity must be stable (or stably open) before commit.  
- **Freeze‑signature enforcement** — Freeze signatures are hard constraints.  
- **Commitment continuity** — Commitments must be stable or stably carried.  
- **Bounded recursion** — IdOB cycles are bounded by routing, commit gating, and the resource limit to be specified later.  
- **Freeze‑signature precedence** — Freeze signatures override all other identity‑conditioned signals and force additional IdOB cycles until resolved or stably carried.

---

# **12. Extendability**

IdOB is extendable under TS’s six criteria.  
Possible extensions include new identity‑conditioned attributes, qualifier or subculture categories, stance/direction/coherence categories, semantic‑importance categories, identity continuity flags, or freeze‑signature types.

All extensions must preserve determinism, boundedness, replay safety, identity continuity, and continuity stability.

---

# **13. Why IdOB Enables Laptop‑Scale Cognition**

IdOB:

- limits drift in referents, qualifiers, subculture, stance/direction/coherence, and semantic‑importance  
- keeps identity cycles bounded  
- produces stable identity‑conditioned state  
- prevents recomputation of identity across turns  
- **performs identity‑conditioned compression**, enabling deterministic reuse of identity state  

IdOB is the identity‑conditioned compression and stabilization mechanism that contributes to laptop‑scale operation.

---

# **14. Conclusion**

IdOB refines referents, interprets qualifiers, assigns subculture, refines stance/direction/coherence and semantic‑importance, enforces commitments and freeze signatures, maintains identity continuity, and stabilizes identity‑conditioned meaning before commit.

It is the identity engine of the Thought Pipeline and the architectural counterpart to TS Identity Theory.

---

# **End of tp_identity_basin.md (Converged Revision)**

---

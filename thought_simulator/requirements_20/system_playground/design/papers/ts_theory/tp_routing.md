# **TP Routing**  
### *The Routing Architecture of the Thought Pipeline (TP)*

Routing is the deterministic mechanism that decides where meaning flows next inside Path‑A. It integrates:

- structural residue  
- constraint residue  
- semantic‑adjacent cues  
- semantic‑layer cues  
- continuity signals  
- identity continuity flags  
- commitments  
- freeze signatures  
- curvature signals  
- routing metadata (TP.TR)  

Routing determines:

- whether meaning requires structural refinement  
- whether meaning requires semantic refinement  
- whether meaning requires identity‑conditioned interpretation  
- whether meaning requires correction  
- whether meaning is stable enough to commit  

This paper defines:

1. the purpose of routing  
2. the routing primitives  
3. the routing signals  
4. the routing cycle  
5. deterministic basin‑selection logic  
6. relationship to continuity, identity, and the Context Frame  
7. invariants that make routing replay‑safe and laptop‑scale  
8. extendability  

Routing is the primary decision mechanism of the Thought Pipeline.

---

# **1. Purpose of Routing**

Routing exists to:

- interpret structural, constraint, semantic‑adjacent, and semantic‑layer cues  
- integrate continuity and identity constraints  
- detect drift and escalate appropriately  
- select the correct basin (structural, semantic, identity)  
- determine whether meaning is stable or requires additional cycles  
- determine whether correction is required  
- determine whether commit is allowed  
- maintain deterministic, replay‑safe flow through Path‑A  

Routing provides the control logic that keeps Path‑A bounded and deterministic.

---

# **2. Routing Primitives**

Routing is implemented by four primitives:

### **2.1 RB — Routing Basin (20.40.070)**  
- Deterministic basin selector  
- Reads TP‑stream fields, OB residue, semantic cues, identity flags  
- Does not modify TP content  
- Selects among: structural basin, semantic basin, identity basin (IdOB), correction path, or commit path  

### **2.2 TR — Thought Router (20.37)**  
- Computes routing vector TP.TR  
- Consumes OB residue and DCB curvature signals  
- Guides RB but does not itself select basins  
- Produces deterministic routing metadata  

### **2.3 DCB — Deterministic Curvature Basin (20.705)**  
- Computes curvature signals  
- Detects trajectory shifts and instability  
- Influences TR and RB  
- **Curvature signals also act as commit‑gating indicators**, preventing commit when trajectory instability is detected.

### **2.4 RBU — Routing Basin Update (20.705)**  
- Routing update step between cycles  
- Integrates new cues from IdOB, OB, SSG, STPX  
- Prepares routing state for the next RB decision  

These four primitives form the routing subsystem.

---

# **3. Routing Signals**

Routing consumes signals from multiple layers:

### **3.1 Structural Layer (SOB → SROB)**  
- clause boundaries  
- structural anchors  
- punctuation masks  
- structural‑importance roles  

### **3.2 Constraint Layer (CnOB)**  
- missing‑slot signals  
- conflict indicators  
- constraint‑importance facts  

### **3.3 Semantic‑Adjacent Layer (SmOB → SSG)**  
- modality and affect cues  
- conflict‑adjacent signals  
- underspecification markers  
- semantic‑adjacent importance residues  
- pre‑semantic hash  
- activation vectors  

### **3.4 Semantic‑Layer (STPX)**  
- semantic‑role adjacency  
- frame‑compatible markers  
- semantic‑layer hash  

### **3.5 Continuity Layer**  
- topic, intent, stance, referent, identity, and importance drift  
- freeze‑signature conflicts  

### **3.6 Identity Layer**  
- identity continuity flags  
- commitments  
- referent lineage  
- qualifier lineage  
- subculture / stance / direction / coherence continuity  

### **3.7 Context Layer**  
- stabilized **Context Frame**  
- clarifying metadata  
- MSL tokens  
- next_context  

### **3.8 Curvature Layer (DCB)**  
- trajectory curvature  
- instability signals  
- shift_required flags  
- **commit‑gating curvature indicators**

Routing integrates these signals deterministically.  
When signals conflict, RB applies a deterministic precedence / arbitration rule (concrete ordering defined in later implementation documents).

---

# **4. Routing Cycle**

Routing occurs in cycles that correspond to the Path‑A flow:

1. **Cue Extraction** — SOB → SROB → CnOB → SmOB → SSG → STPX  
2. **Routing Update** — RBU  
3. **Curvature Evaluation** — DCB  
4. **Routing Vector Computation** — TR  
5. **Basin Selection** — RB  
6. **Identity‑Conditioned Meaning Construction** — IdOB → MCB  
7. **Consolidation & Scheduling** — CTP → TrSch  
8. **Repeat or Commit** — continue cycles until stable, or proceed to OuBA  

This cycle is the operational realization of the normative Path‑A sequence in 20.705.

---

# **5. Deterministic Basin‑Selection Logic**

RB selects basins according to deterministic rules.  
Conditions below are architectural; concrete predicates will be defined later.

### **5.1 Structural Basin**  
Selected when structural residue is incomplete, anchors conflict, structural‑importance roles require refinement, or clause boundaries are ambiguous.

### **5.2 Semantic Basin**  
Selected when semantic‑adjacent or semantic‑layer cues require refinement, semantic‑role adjacency is ambiguous, or the semantic‑layer hash indicates underspecification.

### **5.3 Identity Basin (IdOB)**  
Selected when referent conflict exists, qualifier clusters or subculture / stance / direction / coherence shifts are detected, identity continuity flags are raised, or commitments / freeze signatures require enforcement.  
This is the most frequently selected basin in long‑horizon conversation.

### **5.4 Correction Path (TPU)**  
Selected when ISc scoring or related checks indicate correction is required (referent mismatch, message‑item mismatch, constraint violation, semantic inconsistency).

### **5.5 Commit Path (OuBA)**  
Selected when meaning and identity are stable, continuity is satisfied, curvature is low, no drift flags remain, and no correction is required.  
Freeze‑signature conflicts override all other routing signals and force identity‑conditioned interpretation.

**Single‑writer note:** RB evaluates commit *eligibility*. Only OuBA performs the actual commit.

---

# **6. Relationship to Theory Papers**

Routing is the operational realization of:

### **6.1 Continuity Theory**  
Uses continuity signals to detect drift, escalate ambiguous cases, enforce bounded transitions, and protect commitments and freeze signatures.

### **6.2 Identity Theory**  
Uses identity signals to detect identity drift, enforce referent and commitment continuity, respect freeze signatures, and select IdOB when identity‑conditioned interpretation is required.

### **6.3 Context Layer Theory**  
Routing consumes the **stabilized Context Frame**:

$$
\mathrm{ContextFrame}_t = h(M_t, I_t, C_t)
$$

Routing consumes the stabilized meaning state $M_t$ as part of the Context Frame.

Routing is the point where the theory papers become operational decision logic.

---

# **7. Routing and the Context Frame**

Routing is the first major consumer of the Context Frame.  
It reads stabilized topic, intent, stance, referents, commitments, importance, identity continuity flags, freeze‑signature status, clarifying metadata, next_context, and uses them with cue and curvature signals to make basin‑selection decisions.

---

# **8. Routing and Identity‑Conditioned Meaning Construction**

Routing determines when IdOB must run.  
IdOB is selected when referents, qualifiers, subculture, stance/direction/coherence, or semantic‑importance residues require identity‑conditioned interpretation, or when identity continuity flags require resolution.

Routing bounds IdOB recursion by selecting identity cycles only when identity‑conditioned meaning construction is required.

---

# **9. Routing and Commit**

Routing determines commit *eligibility*.  
Commit requires:

- no material drift  
- no required correction  
- no identity or freeze‑signature conflicts  
- acceptable curvature  
- stable semantic‑layer cues  
- stable referent lineage  
- stable commitments  
- stable stance/direction/coherence  

OuBA performs the commit, preserving the single‑writer invariant.

---

# **10. Deterministic Invariants**

Routing obeys:

- **Deterministic ordering** — fixed Path‑A sequence  
- **Replay determinism** — routing is a deterministic function of signals  
- **No global state leakage** — routing primitives read only TP‑stream fields  
- **Identity‑conditioned routing** — identity continuity flags and commitments influence basin selection  
- **Freeze‑signature enforcement** — freeze signatures are hard constraints  
- **Single‑writer invariant** — routing never writes meaning  

---

# **11. Extendability**

Routing is intentionally extendable under TS’s six criteria.  
Extendability includes:

- new signal sources  
- new basin types  
- refined arbitration rules  
- additional curvature indicators  

All extensions must preserve determinism, boundedness, replay safety, and the single‑writer invariant.

---

# **12. Why Routing Enables Laptop‑Scale Cognition**

Routing keeps processing bounded by:

- avoiding unnecessary IdOB or refinement cycles  
- bounding IdOB recursion  
- avoiding recomputation of stable meaning or identity  
- ensuring deterministic transitions  
- allowing commit only when stability criteria are met  

Routing is a principal control mechanism enabling laptop‑scale operation.

---

# **13. Conclusion**

Routing integrates structural, constraint, semantic‑adjacent, semantic‑layer, continuity, and identity signals to select basins deterministically, drive identity‑conditioned meaning construction when required, enforce commitments and freeze signatures, detect and escalate drift, and determine correction versus commit eligibility.

It provides the decision logic that keeps the Thought Pipeline replay‑safe, bounded, and aligned with the continuity, identity, and context‑layer theories.

---

# **End of tp_routing.md (Converged Revision)**

---

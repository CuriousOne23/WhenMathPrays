# **idob_output_contract.md**  
### *The Deterministic Contract Governing Identity Outputs from IdOB in Path‑A*  
### *Boundary Conditions for Identity‑Conditioned Meaning Emission*

---

# **1. Purpose of This Paper**

This paper defines the **IdOB Output Contract** — the deterministic rules governing:

- what IdOB emits  
- how IdOB outputs are structured  
- how IdOB outputs propagate across turns  
- how IdOB outputs update geometry, continuity, routing, freezes, and basins  
- how IdOB outputs maintain identity stability  
- how IdOB outputs maintain replay determinism  

IdOB is the **identity interpreter** of Path‑A.  
This paper defines the **contract** that ensures IdOB emits only valid, bounded, stable identity outputs.

---

# **2. What IdOB Outputs**

IdOB emits **identity‑conditioned meaning**, structured into seven canonical output classes:

### **2.1 Identity Geometry Updates**
- updated geometry  
- refined geometry  
- corrected geometry  
- collapsed geometry  
- bifurcated geometry  

### **2.2 Identity Role Outputs**
- identity roles  
- identity stance_next  
- identity direction_next  

### **2.3 Identity Continuity Outputs**
- continuity_next  
- continuity correction  
- continuity refinement  
- continuity stabilization  

### **2.4 Identity Pressure Outputs**
- pressure_next  
- pressure gradients  
- pressure decay  
- pressure escalation  

### **2.5 Identity Residual Outputs**
- residual vectors  
- residual collapse  
- residual explosion  

### **2.6 Identity Freeze Outputs**
- freeze.current  
- freeze.next  
- freeze.propagation  

### **2.7 Identity Basin/Surface Outputs**
- basin_state  
- surface_state  

These outputs form the **identity output vector**:

$$
O_{\text{IdOB}} = \\{ G', R', C', P', K', E', F', B \\}
$$

Where:

- $G'$ = geometry updates  
- $R'$ = roles  
- $C'$ = continuity  
- $P'$ = pressure  
- $K'$ = curvature  
- $E'$ = entropy  
- $F'$ = freezes  
- $B$ = basin/surface  

---

# **3. Output Boundary Conditions**

IdOB enforces **six boundary conditions** on all outputs:

### **3.1 Boundedness**
Outputs must remain within the identity geometry domain.

### **3.2 Determinism**
Outputs must be deterministic under replay.

### **3.3 Stability**
Outputs must not destabilize identity geometry.

### **3.4 Continuity**
Outputs must align with continuity_next.

### **3.5 Pressure Integrity**
Outputs must produce measurable, bounded pressure.

### **3.6 Replay Safety**
Outputs must produce identical results under replay.

These conditions ensure identity remains stable.

---

# **4. Geometry Output Contract**

IdOB emits geometry updates that:

### **4.1 Refine geometry**
Small residual → geometry refinement.

### **4.2 Correct geometry**
Medium residual → geometry correction.

### **4.3 Collapse geometry**
Large residual → geometry collapse.

### **4.4 Split geometry**
Two basins → geometry bifurcation.

### **4.5 Merge geometry**
Two basins converge → geometry merging.

Geometry outputs determine the **shape** of identity.

---

# **5. Role Output Contract**

IdOB emits identity roles that:

- interpret identity‑conditioned meaning  
- determine stance_next  
- determine direction_next  
- determine identity motion  
- determine identity alignment  

Role outputs determine the **operators** of identity.

---

# **6. Continuity Output Contract**

IdOB emits continuity outputs that:

### **6.1 Continue identity**
Small residual → continuation.

### **6.2 Refine identity**
Medium residual → refinement.

### **6.3 Correct identity**
Large residual → correction.

### **6.4 Stabilize identity**
Residual collapse → stabilization.

Continuity outputs determine the **trajectory** of identity.

---

# **7. Pressure Output Contract**

IdOB emits pressure outputs that:

### **7.1 Decay pressure**
Small residual → pressure decay.

### **7.2 Persist pressure**
Medium residual → pressure persistence.

### **7.3 Escalate pressure**
Large residual → pressure escalation.

Pressure outputs determine the **forces** acting on identity.

---

# **8. Residual Output Contract**

IdOB emits residual outputs that:

- measure identity drift  
- measure identity conflict  
- measure identity correction  
- measure identity collapse  
- measure identity bifurcation  

Residual outputs determine the **error field** of identity.

---

# **9. Freeze Output Contract**

IdOB emits freeze outputs that:

### **9.1 Lock identity instability**
identity_freeze

### **9.2 Propagate identity instability**
freeze.propagation

### **9.3 Resolve identity instability**
freeze resolution

Freeze outputs determine the **safety locks** of identity.

---

# **10. Basin/Surface Output Contract**

IdOB emits basin/surface outputs that:

### **10.1 Enter basins**
Low pressure → basin entry.

### **10.2 Exit basins**
Medium pressure → basin drift.

### **10.3 Enter surfaces**
High pressure → transition surface.

### **10.4 Cross surfaces**
Residual explosion → surface crossing.

Basin/surface outputs determine the **global geometry** of identity.

---

# **11. Output Propagation**

IdOB outputs propagate into:

### **11.1 TP Metadata**
All outputs are written into TP metadata.

### **11.2 Next‑Turn Context**
Outputs become next B.

### **11.3 Routing**
Outputs determine adjacency, displacement, regime.

### **11.4 Continuity**
Outputs determine continuity_next.

### **11.5 Commit**
Outputs determine commit eligibility.

### **11.6 Global Geometry**
Outputs determine basin/surface transitions.

Output propagation is the **identity motion engine**.

---

# **12. Output Failure Modes**

IdOB output failure occurs when:

### **12.1 Geometry Failure**
Geometry becomes undefined.

### **12.2 Role Failure**
Roles conflict.

### **12.3 Continuity Failure**
Continuity collapses.

### **12.4 Pressure Failure**
Pressure becomes unbounded.

### **12.5 Residual Failure**
Residuals explode.

### **12.6 Freeze Failure**
Freezes contradict.

### **12.7 Basin Failure**
Basins collapse.

Failure triggers:

- identity_freeze  
- continuity correction  
- routing escalation  
- commit block  

---

# **13. Worked Example — Identity Output Conflict**

### **Utterance:**  
“That’s not the identity I meant.”

IdOB outputs:

- geometry: divergent  
- continuity: correction  
- pressure: high  
- residuals: large  
- freeze: identity_freeze  
- basin/surface: transition_surface  

Outcome:

- routing escalation  
- commit blocked  
- identity splitting required  

---

# **14. Worked Example — Identity Output Alignment**

### **Utterance:**  
“Yes, that’s the identity I meant.”

IdOB outputs:

- geometry: convergent  
- continuity: continuation  
- pressure: low  
- residuals: small  
- freeze: resolved  
- basin/surface: basin entry  

Outcome:

- identity stability  
- commit eligible  
- identity merging possible  

---

# **15. Summary**

This paper defines the **IdOB Output Contract**, including:

- geometry outputs  
- role outputs  
- continuity outputs  
- pressure outputs  
- residual outputs  
- freeze outputs  
- basin/surface outputs  
- propagation rules  
- failure modes  

The IdOB Output Contract ensures identity remains:

- stable  
- clear  
- deterministic  
- replay‑safe  
- non‑fuzzy  
- non‑fragmented  

This paper completes the **identity emission architecture** of Path‑A.

---

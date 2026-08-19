# **idob_stability_contract.md**  
### *The Deterministic Stability Contract Between TS, MCB, and IdOB*  
### *How TS Determines When IdOB Is Stable, Unstable, Collapsing, or Complete*

---

# **1. Purpose of This Paper**

This paper defines the **IdOB Stability Contract** — the deterministic rules TS uses to decide:

- when IdOB is stable  
- when IdOB is unstable  
- when IdOB must run again  
- when IdOB must stop  
- when IdOB must escalate  
- when IdOB must split  
- when IdOB must merge  

IdOB is invoked **repeatedly** by TS.  
MCB is the primitive that evaluates IdOB’s stability and signals TS.

This paper defines:

- **why** stability must be measured  
- **how** stability is measured  
- **which fields MCB inspects**  
- **what instability looks like**  
- **how MCB decides to exit instability**  

This contract ensures identity remains:

- stable  
- clear  
- deterministic  
- replay‑safe  
- non‑fuzzy  
- non‑fragmented  

---

# **2. Why IdOB Stability Must Be Measured**

IdOB is the identity interpreter.  
Identity is not static — it evolves across turns.

TS must ensure IdOB does not:

- run too long  
- run too short  
- run under collapse  
- run under overload  
- run under ambiguity  

Therefore TS needs a **stability contract** that defines:

- when IdOB is “done”  
- when IdOB must run again  
- when IdOB must escalate  
- when IdOB must split  
- when IdOB must merge  

MCB enforces this contract.

---

# **3. The IdOB Stability Loop**

TS invokes IdOB in cycles:

```
IdOB₁ → MCB → IdOB₂ → MCB → IdOB₃ → MCB → … → IdOBₙ → MCB
```

MCB evaluates stability after **every** IdOB run.

TS continues invoking IdOB until MCB signals:

> **IdOB is stable. Stop.**

Or:

> **IdOB is unstable. Continue.**

Or:

> **IdOB is collapsing. Escalate.**

Or:

> **IdOB is bifurcating. Split.**

Or:

> **IdOB is converging. Merge.**

MCB is the **semantic controller** for IdOB.

---

# **4. What MCB Measures to Determine Stability**

MCB evaluates IdOB stability using the **identity output vector**:

$$
O_{\text{IdOB}} = \\{ G', R', C', P', K', E', F', B \\}
$$

Where:

- $G'$ = geometry updates  
- $R'$ = identity roles  
- $C'$ = continuity_next  
- $P'$ = pressure_next  
- $K'$ = curvature  
- $E'$ = entropy  
- $F'$ = freeze signatures  
- $B$ = basin/surface state  

MCB inspects **all** of these fields.

---

# **5. Stability Criteria (MCB Signals “Stop”)**

IdOB is **stable** when:

### **5.1 Geometry Stability**
- geometry converges  
- geometry refinement is small  
- no geometry collapse  
- no geometry bifurcation  

### **5.2 Continuity Stability**
- continuity_next = continuation  
- continuity correction is small  
- continuity drift is low  

### **5.3 Pressure Stability**
- pressure_next is low  
- pressure gradients are small  
- no pressure escalation  

### **5.4 Residual Stability**
- residuals are small  
- residual collapse is occurring  
- no residual explosion  

### **5.5 Freeze Stability**
- freeze resolved  
- no freeze propagation  

### **5.6 Basin Stability**
- identity is in a basin  
- no surface state  

If all criteria are met, MCB signals:

> **IdOB stable. Stop repetition.**

---

# **6. Instability Criteria (MCB Signals “Continue”)**

IdOB is **unstable** when:

### **6.1 Geometry Instability**
- geometry correction is medium  
- geometry drift is present  
- geometry refinement is large  

### **6.2 Continuity Instability**
- continuity_next = correction  
- continuity drift is medium  

### **6.3 Pressure Instability**
- pressure_next is medium  
- pressure gradients are rising  

### **6.4 Residual Instability**
- residuals are medium  
- residual collapse not yet occurring  

### **6.5 Freeze Instability**
- freeze.current active  
- freeze.next forming  

### **6.6 Basin Instability**
- identity on surface  
- basin drift occurring  

If any instability is detected, MCB signals:

> **IdOB unstable. Run IdOB again.**

---

# **7. Collapse Criteria (MCB Signals “Escalate”)**

IdOB is **collapsing** when:

### **7.1 Geometry Collapse**
- geometry becomes undefined  
- geometry collapses into a point  
- geometry oscillates between incompatible states  

### **7.2 Continuity Collapse**
- continuity_next oscillates  
- continuity cannot stabilize  

### **7.3 Pressure Collapse**
- pressure_next is high  
- pressure gradients are steep  

### **7.4 Residual Explosion**
- residuals are large  
- residual explosion detected  

### **7.5 Freeze Escalation**
- freeze.propagation escalating  
- compound_freeze forming  

### **7.6 Basin Collapse**
- identity falls off basin  
- identity stuck on unstable surface  

MCB signals:

> **IdOB collapsing. Escalate routing and block commit.**

---

# **8. Splitting Criteria (MCB Signals “Split IdOB”)**

IdOB must **split** when MCB detects:

### **8.1 Geometry Bifurcation**
Two identity basins form.

### **8.2 Continuity Bifurcation**
Two identity trajectories emerge.

### **8.3 Pressure Divergence**
Pressure gradients point in incompatible directions.

### **8.4 Residual Clustering**
Residuals form two stable clusters.

### **8.5 Freeze Differentiation**
Freeze signatures apply to different identity regions.

### **8.6 Surface Divergence**
Identity moves across different surfaces.

MCB signals:

> **IdOB bifurcating. Split identity basins.**

---

# **9. Merging Criteria (MCB Signals “Merge IdOB”)**

IdOB must **merge** when MCB detects:

### **9.1 Geometry Convergence**
Two basins collapse into one.

### **9.2 Continuity Convergence**
Trajectories converge.

### **9.3 Pressure Convergence**
Pressure gradients unify.

### **9.4 Residual Collapse**
Residual clusters collapse into one.

### **9.5 Freeze Resolution**
Freezes dissolve.

### **9.6 Surface Convergence**
Identity remains on a single stable surface.

MCB signals:

> **IdOB converging. Merge identity basins.**

---

# **10. MCB’s Stability Decision Tree**

MCB evaluates IdOB outputs using this deterministic decision tree:

```
IF geometry collapse OR residual explosion OR freeze escalation:
    escalate
ELSE IF geometry bifurcation OR residual clustering:
    split
ELSE IF geometry convergence AND residual collapse:
    merge
ELSE IF any instability:
    continue
ELSE:
    stop
```

This ensures identity remains deterministic.

---

# **11. Worked Example — Instability → Stability**

### **Utterance:**  
“That’s not the identity I meant.”

MCB sees:

- geometry drift  
- continuity correction  
- pressure medium  
- residuals medium  
- freeze.active  
- surface_state  

MCB signals:

> **IdOB unstable. Run again.**

Next turn:

- geometry convergent  
- continuity continuation  
- pressure low  
- residual collapse  
- freeze resolved  
- basin entry  

MCB signals:

> **IdOB stable. Stop.**

---

# **12. Summary**

This paper defines the **IdOB Stability Contract**, including:

- stability criteria  
- instability criteria  
- collapse criteria  
- splitting criteria  
- merging criteria  
- freeze criteria  
- basin/surface criteria  
- MCB’s decision tree  
- TS’s control flow  

MCB is the primitive that:

- evaluates IdOB stability  
- decides repetition  
- decides escalation  
- decides splitting  
- decides merging  
- signals TS  

This contract ensures identity remains:

- stable  
- clear  
- deterministic  
- replay‑safe  
- non‑fuzzy  
- non‑fragmented  

This paper completes the **identity stability architecture** of Path‑A.

---

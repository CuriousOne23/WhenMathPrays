# **idob_upstream_relationships.md**  
### *The Upstream Primitives and Fields Required for IdOB Operation in Path‑A*  
### *How Identity Object Basins Depend on Upstream Geometry, Continuity, Routing, Pressure, and Semantic Signals*

---

# **1. Purpose of This Paper**

This paper defines the **upstream relationships** that IdOB depends on.  
IdOB is not a standalone primitive — it is a **downstream interpreter** that requires:

- geometry  
- continuity  
- routing  
- pressure  
- semantic‑importance  
- freeze signatures  
- basin/surface state  

from upstream primitives.

This paper explains:

- **which upstream primitives IdOB depends on**  
- **which fields those primitives must produce**  
- **why IdOB needs those fields**  
- **how IdOB uses those fields**  
- **what happens when upstream fields are missing or malformed**

This is the “dependency contract” for IdOB.

---

# **2. The Upstream Chain Feeding IdOB**

IdOB sits deep in Path‑A:

```
InB → IIInB → IE → CEx → CE → TPU → SOB → SROB → CnOB → SmOB → ISc → SSG → STPX → RBU → DCB → RB → TR → CTP → RTU → IdOB
```

IdOB depends on **every primitive upstream of it**.

But only certain primitives produce fields IdOB *must* have.

Those are:

- **SOB**  
- **SROB**  
- **CnOB**  
- **SmOB**  
- **ISc**  
- **SSG**  
- **STPX**  
- **RBU**  
- **DCB**  
- **RB**  
- **TR**  
- **CTP**  
- **RTU**

These primitives produce the **identity‑conditioned substrate** IdOB interprets.

---

# **3. Upstream Primitives and Their Required Fields**

Below is the complete list of upstream primitives and the fields IdOB requires from each.

---

## **3.1 SOB → Structural Object Basin**  
### **Required Fields**
- structural geometry  
- adjacency  
- displacement  
- structural curvature  

### **Why IdOB Needs It**
Identity meaning must sit on top of structural geometry.  
Without SOB geometry, IdOB has no “shape” to interpret identity within.

---

## **3.2 SROB → Structural Residue Object Basin**  
### **Required Fields**
- structural residues  
- structural conflict signals  
- structural correction signals  

### **Why IdOB Needs It**
Identity meaning inherits structural residues.  
IdOB must know where structural conflict exists before interpreting identity conflict.

---

## **3.3 CnOB → Continuity Object Basin**  
### **Required Fields**
- continuity geometry  
- continuity drift  
- continuity correction  
- continuity_next  

### **Why IdOB Needs It**
Identity continuity depends on global continuity.  
IdOB cannot compute identity continuity without upstream continuity geometry.

---

## **3.4 SmOB → Semantic Object Basin**  
### **Required Fields**
- semantic geometry  
- semantic adjacency  
- semantic displacement  
- semantic curvature  
- semantic entropy  

### **Why IdOB Needs It**
Identity geometry is a *subset* of semantic geometry.  
IdOB cannot form identity basins without semantic basins.

---

## **3.5 ISc → Importance Scoring**  
### **Required Fields**
- semantic‑importance  
- importance gradients  
- importance decay  

### **Why IdOB Needs It**
Identity pressure is scaled by semantic‑importance.  
IdOB cannot measure identity pressure without importance signals.

---

## **3.6 SSG → Semantic Scoring Geometry**  
### **Required Fields**
- scoring geometry  
- scoring curvature  
- scoring entropy  

### **Why IdOB Needs It**
Identity curvature and entropy derive from scoring geometry.  
IdOB needs these to detect identity instability.

---

## **3.7 STPX → Structural Transform Pipeline**  
### **Required Fields**
- structural transforms  
- structural propagation  
- structural correction  

### **Why IdOB Needs It**
Identity geometry inherits structural transforms.  
IdOB must know how meaning was structurally transformed before interpreting identity.

---

## **3.8 RBU → Routing Boundary Updates**  
### **Required Fields**
- routing boundaries  
- routing boundary drift  
- routing boundary correction  

### **Why IdOB Needs It**
Identity routing depends on global routing boundaries.  
IdOB cannot compute identity routing without boundary updates.

---

## **3.9 DCB → Discourse Boundary Consolidation**  
### **Required Fields**
- discourse boundaries  
- discourse drift  
- discourse correction  

### **Why IdOB Needs It**
Identity meaning is constrained by discourse boundaries.  
IdOB must know the discourse region identity belongs to.

---

## **3.10 RB → Routing Basin**  
### **Required Fields**
- routing basin state  
- routing basin drift  
- routing basin collapse  

### **Why IdOB Needs It**
Identity basin transitions depend on routing basin transitions.  
IdOB cannot compute identity basin/surface state without routing basin state.

---

## **3.11 TR → Transform Routing**  
### **Required Fields**
- routing regime  
- adjacency  
- displacement  
- curvature  
- entropy  

### **Why IdOB Needs It**
Identity routing inherits global routing regime.  
IdOB must know whether identity is in:

- Stable  
- Transition  
- Collapse  
- Correction  
- Drift  

regime.

---

## **3.12 CTP → Continuity Transform Pipeline**  
### **Required Fields**
- continuity transforms  
- continuity propagation  
- continuity correction  

### **Why IdOB Needs It**
Identity continuity is a transformed version of global continuity.  
IdOB must know how continuity was transformed before interpreting identity continuity.

---

## **3.13 RTU → Routing Turn Update**  
### **Required Fields**
- routing_next  
- stance_next  
- direction_next  

### **Why IdOB Needs It**
Identity stance_next and direction_next derive from RTU.  
IdOB cannot compute identity stance/direction without RTU outputs.

---

# **4. Summary Table — Upstream Fields IdOB Requires**

| **Upstream Primitive** | **Required Fields** | **Why IdOB Needs Them** |
|------------------------|---------------------|--------------------------|
| SOB | structural geometry, adjacency | identity geometry sits on structural geometry |
| SROB | structural residues | identity conflict inherits structural conflict |
| CnOB | continuity geometry, continuity_next | identity continuity depends on global continuity |
| SmOB | semantic geometry, semantic curvature | identity geometry is subset of semantic geometry |
| ISc | semantic‑importance | identity pressure is scaled by importance |
| SSG | scoring geometry | identity curvature/entropy derive from scoring |
| STPX | structural transforms | identity geometry inherits structural transforms |
| RBU | routing boundaries | identity routing depends on global routing boundaries |
| DCB | discourse boundaries | identity meaning constrained by discourse boundaries |
| RB | routing basin state | identity basin transitions depend on routing basin transitions |
| TR | routing regime | identity routing inherits global routing regime |
| CTP | continuity transforms | identity continuity inherits continuity transforms |
| RTU | stance_next, direction_next | identity stance/direction derive from RTU |

This table is the **IdOB upstream dependency contract**.

---

# **5. What Happens When Upstream Fields Are Missing**

If any required upstream field is missing:

### **5.1 Geometry Missing**
Identity geometry cannot form → IdOB collapse.

### **5.2 Continuity Missing**
Identity continuity cannot stabilize → IdOB oscillation.

### **5.3 Pressure Missing**
Identity pressure cannot be measured → IdOB blind to instability.

### **5.4 Residues Missing**
Identity drift cannot be detected → IdOB misinterpretation.

### **5.5 Routing Missing**
Identity routing cannot be computed → IdOB directionless.

### **5.6 Basin/Surface Missing**
Identity stability cannot be determined → IdOB unsafe.

Missing upstream fields cause IdOB to:

- freeze  
- escalate  
- block commit  
- request upstream correction  
- refuse identity interpretation  

This protects TS from identity collapse.

---

# **6. Summary**

This paper defines the **upstream relationships** IdOB depends on:

- structural geometry  
- semantic geometry  
- continuity geometry  
- routing boundaries  
- routing regime  
- semantic‑importance  
- scoring geometry  
- structural transforms  
- discourse boundaries  
- routing basin state  
- continuity transforms  
- stance_next  
- direction_next  

IdOB cannot function without these upstream fields.

This paper completes the **IdOB dependency architecture** of Path‑A.

---


# **Serviceability and Fault Localization**

## **Abstract**

Serviceability in MDCS is the ability to **diagnose, localize, and repair** faults without destabilizing the system or requiring global retraining.  
Fault localization is the geometric mechanism that identifies **where** mismatch originates, **why** it persists, and **which components** require intervention.

Unlike modern AI systems — where faults diffuse across millions of parameters — MDCS provides:

- explicit stance vectors  
- explicit mismatch geometry  
- explicit routing traces  
- explicit diagnostic activations  
- explicit basin transitions  

This makes faults **local**, **visible**, and **repairable**.

Serviceability is not an operational layer.  
It is a **geometric property** of the architecture.

---

# **1. Motivation**

Modern AI systems are notoriously difficult to service:

- no clear fault boundaries  
- no localized failure surfaces  
- no stable fallback modes  
- no interpretable routing  
- no diagnostic checkpoints  
- no predictable shutdown behavior  

MDCS solves this by making:

- mismatch **traceable**  
- routing **inspectable**  
- diagnostics **explicit**  
- basins **visible**  
- shutdown **controlled**  
- recovery **bounded**  

Serviceability is built into the manifold itself.

---

# **2. What Serviceability Means in MDCS**

Serviceability is the ability to:

- identify failing OBs  
- detect unstable routing  
- isolate faulty channels  
- diagnose insufficiency  
- inspect basin transitions  
- trigger controlled shutdown  
- perform targeted repair  
- restore normal operation  

This is possible because MDCS exposes:

- stance  
- mismatch  
- curvature  
- routing  
- diagnostics  
- attractors  
- basins  
- transitions  

as **first‑class engineering objects**.

---

# **3. Fault Geometry Overview**

A fault in MDCS is not a parameter error.  
It is a **geometric inconsistency**:

- stance mismatch  
- curvature collapse  
- routing instability  
- diagnostic activation  
- basin violation  

Let:

- $x$ = current stance  
- $x^\*$ = required stance  
- $e = x^\* - x$ = mismatch  

A fault occurs when:

$$
\| e \| > \theta_{\text{fault}}
$$

and the mismatch **cannot** be resolved locally or routed safely.

Faults are **geometric**, not statistical.

---

# **4. OB‑Level Fault Localization**

Each OB exposes:

- stance $x$  
- required stance $x^\*$  
- mismatch $e = x^\* - x$  
- curvature $C(x)$  
- basin membership $x \in B_{\text{OB}}$  
- fallback or shutdown transitions  

An OB is flagged as faulty when:

$$
\| x - x^\* \| > \theta_{\text{OB}}
$$

and:

- local correction fails  
- routing repeatedly returns mismatch  
- curvature collapses  
- basin boundaries are crossed  

OB‑level faults are **precise and local**.

---

# **5. RB‑Level Fault Localization**

RBs expose:

- incoming mismatch $e_{\text{in}}$  
- outgoing mismatch $e_{\text{out}}$  
- routing transform $R$  
- suppression events  
- quarantine events  

An RB is faulty when:

- routing becomes unstable  
- mismatch amplifies unexpectedly  
- routing violates locality  
- quarantine triggers repeatedly  

Formally, instability is detected when:

$$
\| e_{\text{out}} \| > \alpha \| e_{\text{in}} \|, \quad \alpha > 1
$$

RB faults indicate **routing instability**.

---

# **6. IB‑Level Fault Localization**

IBs detect **structural insufficiency**.

An IB fires when:

$$
\| e_{\text{IB}} \| > \theta_{\text{IB}}
$$

IB activation indicates:

- persistent mismatch  
- unresolved routing  
- insufficient local capability  
- need for adaptation or service  

IB faults are **diagnostic**, not catastrophic.

---

# **7. GB‑Level Fault Localization**

GBs expose:

- current attractor $A_i$  
- basin membership $x \in B_i$  
- global potential $\Phi(x)$  
- transitions between attractors  

A GB‑level fault occurs when:

- the system leaves $B_{\text{normal}}$ unexpectedly  
- global inhibition triggers repeatedly  
- shutdown basin is entered  
- attractor transitions oscillate  

Formally:

$$
x \notin B_{\text{normal}} \quad \Rightarrow \quad \text{global fault condition}
$$

GB faults indicate **system‑level instability**.

---

# **8. Distributed Error Channels as Fault Traces**

DECs provide the **fault localization pathway**.

A DEC trace includes:

- origin OB  
- routing path  
- diagnostic checkpoints  
- global transitions  
- resolution or escalation  

Engineers can follow a fault from:

1. **where mismatch originated**  
2. **how it propagated**  
3. **where it was suppressed**  
4. **where diagnostics fired**  
5. **where global basins shifted**  

DECs make fault localization **deterministic**.

---

# **9. Quarantine and Isolation**

When a fault is detected:

- RBs quarantine channels  
- OBs enter fallback  
- IBs freeze adaptation  
- GBs apply global inhibition  

Quarantine is **local**, not global.

Let $Q$ be the quarantine operator:

$$
Q(e_{\text{in}}) = 0
$$

This prevents cascading failures.

---

# **10. Controlled Shutdown for Service**

If faults persist:

- OBs move to shutdown stance  
- RBs suppress routing  
- IBs escalate  
- GBs move system to shutdown attractor  

Shutdown is a **basin**, not a switch.

Let:

- $A_{\text{shutdown}}$ = shutdown attractor  

Then:

$$
x \rightarrow A_{\text{shutdown}}
$$

This ensures:

- bounded collapse  
- predictable behavior  
- safe service conditions  

---

# **11. Service Workflow**

A service event proceeds as follows:

### **1. Fault detection**  
OB, RB, IB, or GB triggers.

### **2. Fault localization**  
DEC trace identifies origin and path.

### **3. Quarantine**  
Faulty channels isolated.

### **4. Controlled shutdown**  
System enters $A_{\text{shutdown}}$.

### **5. Inspection and repair**  
Engineer examines:

- stance logs  
- routing logs  
- diagnostic logs  
- basin transitions  

### **6. Recovery**  
System transitions:

$$
A_{\text{shutdown}} \rightarrow A_{\text{safe}} \rightarrow A_{\text{normal}}
$$

Recovery is **gradual and bounded**.

---

# **12. Long‑Term Maintainability**

MDCS is maintainable because:

- primitives never change  
- faults are local  
- mismatch is traceable  
- basins are visible  
- shutdown is controlled  
- recovery is predictable  

Serviceability is a **first‑class architectural property**.

---

# **13. Summary**

Serviceability and fault localization in MDCS are:

- geometric  
- distributed  
- diagnosable  
- bounded  
- predictable  
- non‑agentic  

The system exposes:

- where faults originate  
- how they propagate  
- how they are contained  
- how they are repaired  

**MDCS is not only structured for stability and observability — it is architected so that it can be made *serviceable* as well.**

Next paper  → [*Efficiency Metrics and Health](./efficiency_metrics_and_health.md)

---

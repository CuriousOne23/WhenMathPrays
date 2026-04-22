# **Distributive Primitives**

## **Abstract**

Distributive primitives are the foundational units of the Minimal Distributive Control System (MDCS).  
They provide the minimal geometric machinery required for:

- local stabilization  
- mismatch extraction  
- residual routing  
- diagnostic insufficiency detection  
- composite stabilization  
- safe capability extension  

This paper formalizes the conceptual architecture of distributive primitives — OBs, RBs, IBs, and GBs — and describes how they interact to produce stable, interpretable, and extensible system‑level behavior.

---

# **1. Overview**

MDCS is built from four primitive structures:

- **Observation Basins (OBs)** — local stabilizers  
- **Routing Basins (RBs)** — mismatch routers  
- **Inquiry Basins (IBs)** — diagnostic insufficiency detectors  
- **Governing Basins (GBs)** — composite stabilizers  

These primitives operate on **local relational geometry**, not semantics, symbols, or global representations.

The system’s global behavior emerges from:

- local stance updates  
- distributed mismatch propagation  
- composite stabilization  
- persistent mismatch detection  
- safe extension through new primitives  

This paper defines each primitive and the geometric relationships between them.

---

# **2. Observation Basins (OBs)**

## **2.1 Definition**

An OB is a **local stabilizer**.  
It maintains a stance vector $x$ and a required stance $x^\*$, producing mismatch:

$$
e = x^\* - x
$$

The OB performs one operation:

> **Absorb the component of the incoming signal that correlates with its stance and pass on the rest.**

OBs do not interpret signals.  
They stabilize **relational structure**, not content.

---

## **2.2 Local Geometry**

Each OB exposes:

- stance vector $x$  
- local curvature  
- covariance signature  
- stability thresholds  
- residual mismatch  

The stance vector is the OB’s **identity**:  
a stable geometric posture that defines what it can stabilize.

---

## **2.3 Dimensionality**

The stance vector has the **minimum number of dimensions** required to maintain stable correlation with:

- the signals it digests  
- its neighbors  
- its composite structures  

Typical ranges:

- **3–10 dims** — IO‑proximal OBs  
- **10–50 dims** — coordination OBs  
- **50–200 dims** — composite OBs  

Dimensionality is determined by:

- domain complexity  
- neighbor count  
- required precision  
- safety envelope  
- hardware constraints  

---

## **2.4 Local Stabilization (“Digestion”)**

Given incoming signal $s$, the OB computes:

- correlation with stance  
- stabilized component  
- residual mismatch  

The stabilized component updates stance:

$$
\Delta x = F(x, s)
$$

The residual mismatch is:

$$
e_{\text{residual}} = s - \text{stabilized component}
$$

This residual is routed by RBs.

---

# **3. Resonance and Mismatch**

## **3.1 Resonance**

Resonance measures how well an incoming signal aligns with an OB’s stance.

High resonance:

- strong stabilization  
- low residual  
- low routing pressure  

Low resonance:

- weak stabilization  
- high residual  
- high routing pressure  

---

## **3.2 Steepness**

Steepness is the local inconsistency pressure:

- high steepness → OB cannot stabilize  
- steepness activates RBs  
- steepness increases routing urgency  

Steepness is a geometric signal, not a semantic one.

---

# **4. Routing Basins (RBs)**

## **4.1 Definition**

An RB routes **residual mismatch** toward OBs with higher resonance.

Given incoming mismatch $e_in$, the outgoing mismatch is:

$$
e_{\text{out}} = R(e_{\text{in}})
$$

Outgoing significance:

$$
S_{\text{out}} = \lVert R(e_{\text{in}}) \rVert
$$

---

## **4.2 Routing Behavior**

RBs enforce:

- locality  
- bounded amplification  
- suppression under instability  
- quarantine under safety violation  

Routing is:

- distributed  
- non‑semantic  
- purely geometric  

---

## **4.3 Input and Output Symmetry**

Input and output use the same mechanism:

- input: mismatch propagates inward until stabilized  
- output: stabilized stances propagate outward  

Timing emerges from **duration of unresolved mismatch**, not clocks.

---

# **5. Stabilization Dynamics**

System‑level behavior emerges from:

1. OB stabilization  
2. RB routing  
3. composite stabilization  
4. mismatch dissipation  
5. diagnostic escalation  

Stabilization is complete when:

$$
\lVert e \rVert \rightarrow 0
$$

If mismatch persists, the system transitions into diagnostic mode.

---

# **6. Failure Detection**

## **6.1 Persistent Mismatch**

Failure is detected when:

- mismatch remains high  
- steepness does not collapse  
- routing loops  
- no OB absorbs the signal  

This indicates **structural insufficiency**, not noise.

---

## **6.2 Composite Failure**

Even when multiple OBs co‑activate:

- no composite attractor forms  
- no stable configuration emerges  
- residuals remain high  

This rules out the possibility that the system already has the needed structure.

---

# **7. Inquiry Basins (IBs)**

## **7.1 Definition**

An IB is a **region of persistent mismatch** that no existing OB or composite can stabilize.

It forms when:

1. mismatch persists  
2. routing saturates  
3. composite stabilization fails  

---

## **7.2 System‑Level Meaning**

An IB is geometric evidence that:

> **“There is no existing primitive capable of stabilizing this region.”**

The system reports:

> **“I cannot stabilize this region with my current basins.”**

This is the architecture’s structural honesty mechanism.

---

## **7.3 What the System Can Infer**

From the mismatch field, the system can infer:

- required stance direction  
- required covariance structure  
- required dimensionality  
- required training signals  
- expected cost (parameters, energy, bandwidth)  

This is the system’s **self‑extension interface**.

---

# **8. Creation of New OBs**

## **8.1 Self‑Creation (Training)**

If the system is exposed to repeated examples:

- the IB collapses into a new OB  
- RBs reorganize  
- mismatch drops  
- composite structures update  

---

## **8.2 Human‑Defined OB**

If the system cannot self‑create:

It reports:

> **“I need a new basin of type X, connected here, trained under these conditions.”**

Humans define:

- stance  
- dimensionality  
- covariance  
- neighbors  
- training regime  

The system integrates the new OB automatically.

---

# **9. Governing Basins (GBs)**

## **9.1 Definition**

A GB is a **stable composite configuration** of OBs that repeatedly co‑stabilize a region of relational space.

A GB:

- has no parameters of its own  
- has no stance of its own  
- is a stable relational pattern  

---

## **9.2 Roles of GBs**

GBs provide:

- domain‑level stability  
- coordination without centralization  
- reduced routing overhead  
- integration of new OBs  
- safety envelope enforcement  

---

## **9.3 Categories of GBs**

- **Truth Basins** — stabilize domain‑level truth  
- **Diagnostic Basins** — track mismatch patterns  
- **Safety Basins** — enforce operational bounds  
- **Shutdown Basins** — stabilize controlled deactivation  
- **Performance Basins** — optimize routing and energy  
- **Maintenance Basins** — correct drift and recalibrate  
- **Integration Basins** — incorporate new OBs  

---

# **10. System‑Level Adaptation**

The full adaptive loop:

1. OBs stabilize locally  
2. RBs route residual mismatch  
3. GBs stabilize composite structure  
4. IBs detect insufficiency  
5. new OBs are created  
6. GBs reorganize to incorporate new OBs  

This loop ensures:

- stability  
- extensibility  
- safety  
- coherence  
- realizability  

The system grows capability **without destabilizing itself**.

---

# **Summary**

Distributive primitives provide the minimal geometric machinery for:

- local stabilization  
- distributed routing  
- diagnostic insufficiency detection  
- composite stabilization  
- safe capability extension  

OBs, RBs, IBs, and GBs form a coherent architecture that is:

- stable  
- interpretable  
- maintainable  
- extensible  
- non‑agentic  
- physically realizable  

This completes the conceptual foundation for MDCS distributive primitives.

Next paper  →  [Local Stance and Direction](./local_stance_and_direction.md)

---

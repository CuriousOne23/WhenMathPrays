# ⭐ **ts_tr_semantic_geometry.md**
### *Geometric Substrate for TR Semantic Routing*
### *Theory Foundation (Informative + Proposed Normative Expansion)*

---

# **0. Purpose, Scope, What This Paper Does / Doesn’t Do**

## **0.1 Purpose of This Paper**

The purpose of **ts_tr_semantic_geometry.md** is to define the **geometric substrate** required for TR to compute:

- stance
- affect
- epistemic_shading
- politeness
- tension

These five fields depend on **semantic geometry**, not just symbolic cues.
This paper provides:

- geometric axes
- geometric distances
- geometric continuity
- geometric drift
- geometric curvature
- geometric adjacency

This geometry is the missing foundation beneath the mapping families defined in **ts_tr_mapping_families.md**.

Without semantic geometry:

- stance cannot be computed deterministically
- affect cannot be computed deterministically
- shading cannot be computed deterministically
- politeness cannot be computed deterministically
- tension cannot be computed deterministically

This paper closes that gap.

---

## **0.2 What This Paper *Does***

This paper defines:

- semantic axes
- geometric coordinate system
- geometric adjacency
- geometric continuity
- geometric drift
- geometric curvature
- geometric projection rules
- geometric stability rules
- geometric SSR rules
- **composition order** for multi-signal updates
- **minimal-input geometry path** (diagnostic signals absent)

It also defines:

- how meaning‑semantics is projected into geometry
- how identity‑conditioned meaning modifies geometry
- how adjacency modifies geometry
- how continuity modifies geometry
- how curvature modifies geometry

This paper is **normative for geometry**, but **informative for mapping**.

---

## **0.3 What This Paper *Does Not* Do**

This paper does **not** define:

- mapping families (already defined in ts_tr_mapping_families.md)
- invariant drift estimator $H_t$
- lineage append predicate
- routing_fields schema
- adjacency theory (full version)
- continuity‑curvature interaction theory (full version)

Those are separate papers.

This paper defines **geometry only**.

---

## **0.4 Scope**

This paper defines:

- semantic coordinate system
- geometric axes
- geometric distances
- geometric drift
- geometric curvature
- geometric adjacency
- geometric continuity
- geometric projection rules

It defines geometry for:

- stance
- affect
- shading
- politeness
- tension

It does **not** define geometry for:

- logical_structure
- epistemic_delta_h
- lineage_additions
- routing_fields

Those are non‑geometric fields.

---

# **1. Semantic Coordinate System**

TR uses a **5‑dimensional semantic coordinate system**:

$$
\mathbb{S} = (x_s, x_a, x_e, x_p, x_t)
$$

Where:

- $x_s$ = stance axis
- $x_a$ = affect axis
- $x_e$ = epistemic shading axis
- $x_p$ = politeness axis
- $x_t$ = tension axis

Each axis is **ordinal**, **bounded**, and **SSR‑projectable**.

---

# **2. Axes Definitions**

## **2.1 Stance Axis ($x_s$)**

Stance is represented on an ordinal axis:

$$
x_s \in \\{0,1,2,3,4\\}
$$

Where:

- 0 = supportive
- 1 = neutral
- 2 = corrective
- 3 = adversarial
- 4 = exploratory

This axis measures **identity‑conditioned semantic direction**.

---

## **2.2 Affect Axis ($x_a$)**

Affect is represented on a signed axis:

$$
x_a \in \\{-1,0,+1\\}
$$

Where:

- -1 = negative
- 0 = neutral
- +1 = positive

This axis measures **semantic adjacency valence**.

---

## **2.3 Epistemic Shading Axis ($x_e$)**

Shading is represented on an ordinal axis:

$$
x_e \in \\{0,1,2,3\\}
$$

Where:

- 0 = confident
- 1 = neutral
- 2 = uncertain
- 3 = speculative

This axis measures **epistemic stability**.

---

## **2.4 Politeness Axis ($x_p$)**

Politeness is represented on an ordinal axis:

$$
x_p \in \\{0,1,2\\}
$$

Where:

- 0 = direct
- 1 = neutral
- 2 = polite

This axis measures **semantic adjacency softening**.

---

## **2.5 Tension Axis ($x_t$)**

Tension is represented on an ordinal axis:

$$
x_t \in \\{0,1,2\\}
$$

Where:

- 0 = low
- 1 = medium
- 2 = high

This axis measures **curvature‑derived instability**.

---

# **3. Semantic Geometry: Distances**

Semantic geometry uses **Manhattan distance** for ordinal axes:

$$
d(\mathbb{S}_1, \mathbb{S}_2) = 
|x_s^1 - x_s^2| +
|x_a^1 - x_a^2| +
|x_e^1 - x_e^2| +
|x_p^1 - x_p^2| +
|x_t^1 - x_t^2|
$$

This distance is:

- deterministic
- bounded
- SSR‑projectable
- stable under replay

Manhattan distance is chosen because:

- axes are ordinal
- axes are independent
- axes are bounded
- axes are discrete

Euclidean distance is not used because:

- axes are not continuous
- axes are not metric‑smooth
- axes do not support interpolation

---

# **4. Semantic Geometry: Drift**

Semantic drift is defined as:

$$
drift = d(\mathbb{S}_t, \mathbb{S}_{t+1})
$$

Where:

- $\mathbb{S}_t$ = semantic state at cycle $t$
- $\mathbb{S}_{t+1}$ = semantic state at cycle $t+1$

Drift is:

- deterministic
- bounded
- SSR‑projectable

Drift is used to compute:

- tension
- shading
- stance stability
- adjacency stability

---

# **5. Semantic Geometry: Curvature**

Curvature measures **instability** in semantic geometry.

Curvature is defined as:

$$
curvature = d(\mathbb{S}_t, \mathbb{S}_{t+1}) - d(\mathbb{S}_{t-1}, \mathbb{S}_t)
$$

Curvature is:

- positive → instability increasing
- zero → stable
- negative → instability decreasing

Curvature is used to compute:

- tension
- stance instability
- shading instability

Curvature is **not** used to compute:

- affect
- politeness

Those depend on adjacency, not curvature.

---

# **6. Semantic Adjacency Geometry**

Semantic adjacency is the geometric representation of *how close* the user’s phrasing is to:

- positive affect
- negative affect
- hedging
- directness
- softening
- intensification

Adjacency is represented as a **signed scalar**:

$$
A \in [-1, +1]
$$

Where:

- $A = +1$ → positive adjacency (praise, agreement, softening)
- $A = 0$ → neutral adjacency
- $A = -1$ → negative adjacency (critique, disagreement, intensification)

Adjacency influences:

- affect ($x_a$)
- politeness ($x_p$)
- stance ($x_s$)
- reservation

### **Adjacency Projection**

Adjacency is projected into geometry as:

$$
x_a = A
$$

$$
x_p = 
\begin{cases}
2 & A > 0 \\
1 & A = 0 \\
0 & A < 0
\end{cases}
$$

$$
x_s = x_s + \text{adjacency\\_modifier}(A)
$$

Where `adjacency_modifier` is a **versioned free parameter**, provisional default bounded in $\{-1,0,+1\}$ (see §13).

---

# **7. Continuity Geometry**

Continuity measures whether the user’s semantic trajectory is:

- stable
- drifting
- oscillating
- reversing

Continuity is represented as:

$$
C \in \\{-1,0,+1\\}
$$

Where:

- $C = +1$ → stable continuation
- $C = 0$ → neutral / ambiguous continuation
- $C = -1$ → reversal / discontinuity

Continuity influences:

- stance stability
- shading stability
- tension stability

### **Continuity Projection**

Continuity modifies stance and shading:

$$
x_s = x_s + C
$$

$$
x_e = x_e + \max(0, -C)
$$

Meaning:

- stable continuation → stance becomes more supportive/neutral
- discontinuity → shading becomes more uncertain/speculative

---

# **8. Identity‑Conditioned Geometry**

Identity‑conditioned meaning modifies geometry based on:

- commitments
- freeze signatures
- referent lineage
- qualifier lineage

Identity geometry is represented as:

$$
I \in \\{-1,0,+1\\}
$$

Where:

- $I = +1$ → identity‑aligned meaning
- $I = 0$ → identity‑neutral meaning
- $I = -1$ → identity‑conflicting meaning

Identity geometry influences:

- stance
- shading
- tension

### **Identity Projection**

$$
x_s = x_s + I
$$

$$
x_e = x_e + \max(0, -I)
$$

$$
x_t = x_t + \max(0, -I)
$$

Meaning:

- identity alignment → stance stabilizes
- identity conflict → shading and tension increase

---

# **9. Combined Semantic Geometry**

The full semantic geometry state is:

$$
\mathbb{S} = (x_s, x_a, x_e, x_p, x_t)
$$

Where each axis is computed from:

- meaning‑semantics
- adjacency
- continuity
- identity geometry
- curvature

---

# **9.1 Composition Order (Authoritative)**

When multiple signals are present, projections **must** be applied in the following fixed order so that structural programs and progressive tests remain unambiguous:

1. **Base from meaning-semantics** — initialize $x_s, x_e$ from $M$ (and defaults for others).
2. **Adjacency** — set $x_a$, $x_p$; apply `adjacency_modifier` to $x_s$.
3. **Continuity** — add $C$ effects to $x_s$ and $x_e$.
4. **Identity** — add $I$ effects to $x_s$, $x_e$, $x_t$.
5. **Curvature** — set / update $x_t$ from curvature (may overwrite or clamp after identity contribution; implementation must document the chosen clamp rule and keep it deterministic).
6. **Clamp** — force every axis into its declared ordinal range.

Formally (after clamp):

$$
\mathbb{S}_{t+1} = \mathrm{clamp}\big(\mathbb{S}_{\text{base}} + \Delta A + \Delta C + \Delta I + \Delta K\big)
$$

Companion papers (continuity-curvature, adjacency, invariant drift) **must** respect this order when describing joint effects. If a companion paper defines a local formula, the global order above remains authoritative for the final $\mathbb{S}$.

---

# **10. Projection Rules**

Projection rules define how raw signals map into geometry.

### **10.1 Meaning‑Semantics Projection**

Meaning‑semantics is projected into stance and shading:

$$
x_s = f_s(M)
$$

$$
x_e = f_e(M)
$$

### **10.2 Adjacency Projection**

Adjacency is projected into affect and politeness:

$$
x_a = A
$$

$$
x_p = f_p(A)
$$

### **10.3 Continuity Projection**

Continuity modifies stance and shading:

$$
x_s = x_s + C
$$

$$
x_e = x_e + \max(0, -C)
$$

### **10.4 Identity Projection**

Identity modifies stance, shading, tension:

$$
x_s = x_s + I
$$

$$
x_e = x_e + \max(0, -I)
$$

$$
x_t = x_t + \max(0, -I)
$$

### **10.5 Curvature Projection**

Curvature modifies tension:

$$
x_t = f_t(curvature)
$$

---

# **11. Minimal-Input Geometry Path (Diagnostic Signals Absent)**

When only the **narrow normative read-set** (20.37) is present and diagnostic signals (adjacency, continuity, identity geometry, full curvature envelope, etc.) are missing, geometry **must** collapse to the following deterministic defaults:

```
x_s = 1          # neutral
x_a = 0          # neutral
x_e = 1          # neutral
x_p = 1          # neutral
x_t = 0          # low
```

No invention of missing signals is permitted. Meaning-semantics (if present) may still seed $x_s$ / $x_e$ via $f_s$, $f_e$; all other axes remain at the defaults above. This path guarantees that TR remains fully deterministic and progressive-lineup green under minimal inputs.

---

# **12. SSR Projection Rules**

Semantic geometry must be SSR‑projectable:

### **12.1 Stability Under Replay**

$$
SSR(\mathbb{S}) = \mathbb{S}
$$

### **12.2 No Ephemeral Geometry**

All axes must be:

- bounded
- deterministic
- ordinal

### **12.3 No Nondeterministic Drift**

Drift must satisfy:

$$
drift = d(\mathbb{S}_t, \mathbb{S}_{t+1})
$$

Where $d$ is Manhattan distance.

### **12.4 No Nondeterministic Curvature**

Curvature must satisfy:

$$
curvature = d(\mathbb{S}_t, \mathbb{S}_{t+1}) - d(\mathbb{S}_{t-1}, \mathbb{S}_t)
$$

---

# **13. Versioned Free Parameters (Provisional Defaults)**

The following parameters are **versioned free parameters**. Implementations and progressive tests must lock the provisional defaults below until a later refinement is promoted:

| Parameter | Provisional default | Notes |
|-----------|---------------------|-------|
| `adjacency_modifier` range | $\\{-1,0,+1\\}$ | applied to $x_s$ |
| stance base from missing $M$ | 1 (neutral) | minimal-input path |
| shading base from missing $M$ | 1 (neutral) | minimal-input path |
| curvature → $x_t$ map | 0→0, mild→1, strong→2 | see continuity-curvature paper |

Changing a provisional default is a **minor version** event and requires fixture updates.

---

# **14. Closing Summary**

This paper defines the **semantic geometry** required for TR routing:

- 5‑axis semantic coordinate system
- stance / affect / shading / politeness / tension axes
- adjacency, continuity, identity, curvature geometry
- **authoritative composition order**
- **minimal-input geometry path**
- projection rules, SSR rules, versioned free parameters

This geometry is the foundation beneath stance, affect, shading, politeness, and tension mapping and keeps TR deterministic under both full and minimal input conditions.

---

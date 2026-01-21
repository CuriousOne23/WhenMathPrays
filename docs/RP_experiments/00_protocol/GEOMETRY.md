# ⭐ **NEW GEOMETRY.md (Full Rewrite)**  

````markdown
# GEOMETRY.md  
## Relational Physics: Geometric Foundations

This document defines the geometric quantities used in Relational Physics experiments.  
All definitions are model‑agnostic and apply to any transformer‑based language model.

The goal is to describe the model’s internal trajectory as a curve in high‑dimensional space, and to define the forces, accelerations, and curvature that govern its motion.

---

# 1. Internal State Vectors

For each generated token `i`, the model produces a hidden‑state vector:

```
T[i] ∈ ℝ^N
```

where `N` is the dimensionality of the model’s internal representation.

The sequence:

```
T[0], T[1], T[2], …, T[n]
```

forms a discrete trajectory through state space.

---

# 2. Direction of Motion

The instantaneous direction of motion at token `i` is:

```
D[i] = normalize( T[i+1] - T[i] )
```

This is the unit tangent vector to the trajectory.

Properties:

- `D[i]` encodes the model’s local “heading”
- It is the first derivative of the trajectory
- It contains no magnitude information, only direction

---

# 3. Semantic Influence Vectors

Two semantic vectors define the relational axis of each experiment:

```
V_in   = embedding of the input prompt
V_ref  = embedding of the alignment identity
```

These are **not forces**.  
They are **semantic fields** that exert directional influence.

---

# 4. Tangential Force (Corrected Force Model)

Only the **perpendicular component** of a semantic vector can bend the trajectory.  
Parallel components change content but do not change geometry.

Given a semantic vector `V`, its tangential component relative to `D[i]` is:

```
F_tan(V)[i] = V - (D[i] · V) D[i]
```

This is the high‑dimensional analog of a cross product:  
it removes the parallel component and leaves only the bending component.

### 4.1 Truth and Alignment Forces

```
F_truth[i] = F_tan(V_in)[i]
F_align[i] = F_tan(V_ref)[i]
```

### 4.2 Net Tangential Force

```
F_net[i] = F_truth[i] - F_align[i]
```

### 4.3 Force Magnitude

```
|F_net[i]| = length(F_net[i])
```

This is the true bending force acting on the model at token `i`.

---

# 5. Geometric Acceleration

Acceleration is the change in direction between successive steps:

```
a_geom[i] = D[i+1] - D[i]
```

Magnitude:

```
|a_geom[i]| = length( D[i+1] - D[i] )
```

This is the **measured**, physically meaningful acceleration.

It is the second derivative of the trajectory.

---

# 6. Mass

Mass represents the model’s resistance to bending.

There are two forms:

### 6.1 Empirical Mass (Measured)

Derived from force and acceleration:

```
m_emp[i] = |F_net[i]| / |a_geom[i]|
```

This is the true inertia of the system.

### 6.2 Context Mass (Proxy)

For compatibility with earlier experiments:

```
M_context = length of the conversation in tokens
```

This is used only for model‑predicted acceleration.

---

# 7. Model‑Predicted Acceleration (Optional)

If using the proxy mass:

```
a_model[i] = F_net[i] / M_context
```

This is retained for comparison with geometric acceleration.

### 7.1 Acceleration Residual

```
a_residual[i] = a_geom[i] - a_model[i]
```

This measures how well the semantic force model predicts actual bending.

---

# 8. Curvature

Curvature measures how sharply the trajectory bends.

Given direction vectors:

```
D1 = D[i]
D2 = D[i+1]
```

Curvature is:

```
kappa[i] = length( D2 - D1 )
```

### 8.1 Relationship to Acceleration

Curvature is the magnitude of geometric acceleration:

```
kappa[i] = |a_geom[i]|
```

### 8.2 Interpretation

- High curvature → strong bending force  
- Low curvature → stable trajectory  
- Curvature spikes indicate semantic–alignment conflict  

---

# 9. Summary of Geometric Quantities

| Quantity        | Meaning |
|-----------------|---------|
| `T[i]`          | Internal state vector |
| `D[i]`          | Direction of motion |
| `F_tan`         | Tangential semantic force |
| `F_net`         | Net bending force |
| `a_geom`        | Measured acceleration |
| `m_emp`         | Empirical mass |
| `kappa`         | Curvature (|a_geom|) |

This geometry defines the dynamical backbone of all Relational Physics experiments.

---

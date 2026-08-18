# ⭐ **ts_tr_continuity_and_curvature_interaction.md**
### *Continuity Geometry, Curvature Geometry, Interaction Rules, Stability, Drift, TR Field Influence*

---

# **0. Purpose, Scope**

Defines continuity geometry, curvature geometry, their interaction, and influence on TR fields, drift, lineage, and routing_fields. Normative for continuity and curvature; informative for mapping.

Does **not** redefine mapping families, geometry axes, invariant drift estimator, lineage append predicate, or routing_fields key set.

**Composition order:** any axis updates driven by $C$ or $K$ **must** respect `ts_tr_semantic_geometry.md` §9.1.

---

# **1. Continuity Geometry**

$$
C \in \{-1, 0, +1\}
$$

- $+1$ stable continuation
- $0$ neutral / ambiguous
- $-1$ reversal / discontinuity

$$
x_s = x_s + C
$$

$$
x_e = x_e + \max(0, -C)
$$

---

# **2. Curvature Geometry**

$$
curvature = d(\mathbb{S}_t, \mathbb{S}_{t+1}) - d(\mathbb{S}_{t-1}, \mathbb{S}_t)
$$

$$
K \in \{0, 1, 2\}
$$

Provisional map: stable→0, mild→1, strong→2.

$$
x_t = K
$$

---

# **3. Continuity–Curvature Interaction**

| C | K | Interpretation |
|---|---|----------------|
| +1 | 0 | stable trajectory |
| +1 | 1–2 | stable but unstable/turbulent |
| 0 | 0–2 | ambiguous ± instability |
| -1 | 0–2 | reversal ± instability/turbulence |

---

# **4. Projection Rules (after geometry composition order)**

$$
x_s = x_s + C - K
$$

$$
x_e = x_e + \max(0, -C) + K
$$

$$
x_t = K
$$

Routing fields:

```
continuity_state = C
curvature_level = K
stance_instability = (C < 0 or K > 0)
shading_instability = (C < 0 or K > 0)
tension_instability = (K > 0)
semantic_drift = (C < 0 or K > 0)
```

---

# **5–8. Drift, SSR, Invariant Drift, Lineage**

$$
drift = d(\mathbb{S}_t, \mathbb{S}_{t+1}) + \max(0, -C) + K
$$

SSR: $SSR(C)=C$, $SSR(K)=K$.

Invariant drift influence: $\Delta H = \Delta H - C - K$ (freeze conflict still forces $\Delta H=-2$).

Lineage: reversal or $K>0$ may force append / lineage_instability True.

---

# **9–10. Routing Fields & Omission**

If continuity or curvature missing:

```
continuity_state = 0
curvature_level = 0
stance_instability = False
shading_instability = False
tension_instability = False
semantic_drift = False
routing_severity = 0
```

---

# **11. Closing Summary**

Continuity and curvature jointly determine semantic stability, drift, reversal, turbulence, and related TR / routing_fields signals. Axis composition remains governed by geometry §9.1.

---

# **Appendix — Versioned Parameters & Composition**

- Continuity and curvature effects on axes **must** respect geometry §9.1.
- Curvature → tension provisional defaults: stable→0, mild→1, strong→2.
- Missing signals → $C=0$, $K=0$ and geometry minimal-input path.

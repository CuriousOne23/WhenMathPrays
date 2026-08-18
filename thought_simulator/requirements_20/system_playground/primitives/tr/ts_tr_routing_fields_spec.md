# ⭐ **ts_tr_routing_fields_spec.md**
### *Specification of TR Routing Fields*
### *Key Set, Definitions, Deterministic Construction, Stability Rules, SSR Rules*

---

# **0. Purpose, Scope**

Defines the complete key set and deterministic construction rules for `TP.TR.routing_fields{}`.

Normative for routing_fields; informative for mapping. Does not redefine mapping families, semantic geometry, invariant drift estimator, lineage append predicate, or continuity‑curvature theory.

---

# **1. Overview**

```
routing_fields: dict[str, Any]
```

Must be deterministic, bounded, SSR-projectable, independent of raw meaning/identity/TPU/intake/truth hypotheses. Contains only drift, stability, conflict, lineage, curvature, adjacency, commitment, and freeze signals.

---

# **2. Complete Key Set**

```
semantic_drift
identity_drift
commitment_instability
freeze_conflict
topology_instability
curvature_level
stance_instability
shading_instability
tension_instability
lineage_instability
adjacency_valence
continuity_state
invariant_delta_h
routing_severity
```

No other keys allowed. Every key must be present.

---

# **3. Key Definitions (summary)**

- **semantic_drift** — bool; $(drift(\mathbb{S}) > \tau_s)$; provisional $\tau_s = 2$
- **identity_drift** — bool; $(I < 0)$ or $(\Delta H < 0)$
- **commitment_instability** — bool; $(H^{com}_t < 0)$
- **freeze_conflict** — bool; $(H^{freeze}_t = -2)$; overrides
- **topology_instability** — bool; $(H^{topo}_t < 0)$
- **curvature_level** — int $\in \{0,1,2\}$
- **stance_instability** — bool; $(|x_s^{t+1}-x_s^t| > 1)$
- **shading_instability** — bool; $(x_e^{t+1}-x_e^t > 1)$
- **tension_instability** — bool; $(x_t^{t+1}-x_t^t > 1)$
- **lineage_instability** — bool; $(|lineage\_additions| > 0)$
- **adjacency_valence** — int $\in \{-1,0,+1\}$
- **continuity_state** — int $\in \{-1,0,+1\}$
- **invariant_delta_h** — int; $\Delta H$
- **routing_severity** — int $\in \{0,1,2,3\}$; via deterministic severity_classifier

---

# **4. Deterministic Construction**

All keys constructed from geometry, invariant drift, lineage, commitments, freeze, topology, adjacency, continuity, curvature only. Full dictionary always emitted.

---

# **5–6. Stability & SSR**

Under no drift all instability flags False and severity 0. Freeze conflict overrides. SSR: $SSR(routing\_fields) = routing\_fields$.

---

# **7. Deterministic Omission**

If required signals missing, all flags False / 0 / empty as specified in the full omission table (severity defaults).

---

# **8–10. Interaction with TR Fields, Invariant Drift, Lineage**

Stance/shading/tension instability flags from axis deltas; identity/commitment/freeze/topology from $\Delta H$ components; lineage_instability from non-empty lineage_additions.

---

# **11. Closing Summary**

Routing fields are the complete semantic routing metadata interface for RB and related consumers, fully deterministic under both full and minimal inputs.

---

# **Appendix — Versioned Parameters**

| Parameter | Provisional default | Notes |
|-----------|---------------------|-------|
| $\tau_s$ | 2 | semantic_drift threshold |
| severity_classifier | deterministic table TBD | lock before golden tests |
| curvature_level map | 0/1/2 | aligned with geometry |

Changing a provisional default is a **minor version** event and requires progressive-lineup fixture updates.

# ts_semantic_residue_topology.md

## 1. Purpose

This document defines the **first‑order topological model of semantic residue** in TS.  
It complements:

- `ts_invariant_relational_model.md`
- `ts_invariant_to_idob_theory.md`
- `ts_identity_geometry.md`
- `ts_routing_entropy_dynamics.md`

by describing how semantic residue behaves as a **topological object** relevant to **IdOB inheritance/reset** and **RB continuity signals**.

This is a **rudimentary, first‑order model** for observation and early IdOB design—not a finished semantic theory.

---

## 2. Semantic residue space (SRT)

Residue vector:

$$
\mathbf{R} = (r_1, r_2, \ldots, r_n)
$$

Persistence invariant: $R_{\text{res}}$ (definition and measurement in the relational model).

Regimes that govern residue inherit vs reset use the **shared regime table** (Stable / Refinement / Drift / Transition / Collapse).

---

## 3. Residue distance, clusters, attractors

$$
d_R(\mathbf{R}_1, \mathbf{R}_2)
=
\sum_i w_i \, |R_{1,i} - R_{2,i}|
$$

Same cluster if $d_R < \epsilon_{\text{cluster}}$.

Residue attractor $\mathbf{A}_R$: distance decreases over multiple cycles.

**IdOB:** attractors support stable identity anchors.  
**RB:** persistent residue clusters bias local routing under Stable/Refinement.

---

## 4. Persistence trails

Sequence $\mathbf{R}_{t-k}, \ldots, \mathbf{R}_{t}$.

First‑order persistence form:

$$
R_{\text{res}}
=
\frac{|\mathbf{R}_{t} \cap \mathbf{R}_{t-1}|}
{\max(1, |\mathbf{R}_{t}|)}
$$

- High → strong semantic continuity
- Low → semantic reset pressure (Collapse / hard Transition)

**Must observe:** does IdOB residue field track this scalar directionally?

---

## 5. Drift and curvature

$$
\vec{D}_R = \mathbf{R}_{t+1} - \mathbf{R}_{t},
\qquad
\|\vec{D}_R\| = d_R(\mathbf{R}_{t+1}, \mathbf{R}_{t})
$$

Residue curvature $\kappa_R$ uses the same three‑point ratio form as $\kappa_{\text{id}}$, on residue space.

- Small drift → refinement
- Large drift → transition / reconfiguration

---

## 6. Collapse and transition surfaces

- **Collapse:** $R_{\text{res}} < 0.3$ (aligned with shared Collapse when also low $I_{\text{stab}}$).
- **Transition surface:** $\|\vec{D}_R\| = D_{R,\text{crit}}$ (placeholder).

Effects: residue reset, weakened identity stability, provenance coherence risk.

---

## 7. Builder hooks (IdOB / RB)

| Question | Why it matters |
|----------|----------------|
| Does IdOB reset residue only under Collapse/Transition? | Prevents silent residue loss in Stable windows |
| Does high $R_{\text{res}}$ predict RB local adjacency? | Tests IR‑1 / IR‑5 coupling |
| Are residue clusters stable when roles are stable? | Validates attractor language |
| Which TP field is the actual $\mathbf{R}$ source? | Bridge map completeness |

---

## 8. Must‑observe vs defer

**Must observe**

- Log $R_{\text{res}}$ and residual field presence per cycle.
- Compare IdOB residue inherit/reset with regime label.
- Check IR‑1: high $I_{\text{stab}}$ vs high $R_{\text{res}}$.

**Defer**

- Rich residue feature learning.
- Final cluster algorithms.
- Continuous topological invariants beyond first‑order distance.

---

## 9. Status and next steps

**Status:** First‑order residue topology for IdOB/RB examination.

**Next steps:** Wire residue logging to progressive tests; validate clusters against IdOB outputs; keep thresholds provisional.

This document is the topological foundation of **TS Semantic Dynamics** for first‑order identity work.

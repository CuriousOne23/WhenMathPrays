# ts_identity_geometry.md

## 1. Purpose

This document defines the **first‑order geometric model of identity** in TS.  
It extends:

- `ts_invariant_relational_model.md`
- `ts_invariant_to_idob_theory.md`

by describing how identity behaves as a **geometric object** in the invariant space.

Identity geometry provides:

- structure for IdOB grouping,
- a basis for statistical hashing,
- measures of identity drift and stability,
- language for RB neighborhood proposals,
- and a framework for observing TR‑relevant identity motion.

This is a **rudimentary, first‑order model** for early testing and IdOB guidance—not a finished manifold theory.

---

## 2. Identity geometry space (IGM)

Identity geometry lives in the invariant vector space:

$$
\mathbf{F} =
\left(
I_{\text{stab}},
R_{\text{res}},
P_{\text{cont}},
L_{\text{depth}},
Rt_{\text{adj}},
\Delta H,
E_{\text{dens}},
C_{\text{coh}}
\right)
$$

Each IdOB / cycle observation corresponds to a point in this space.  
We call this space the **Identity Geometry Manifold (IGM)**.

Regimes on the IGM use the **shared regime table** in `ts_invariant_relational_model.md`.

---

## 3. Curvature naming (do not collapse layers)

| Symbol | Layer | Use |
|--------|-------|-----|
| $\kappa_{\text{id}}$ | Identity trajectory on IGM | This paper; IdOB geometry diagnostics |
| $\kappa_{\text{route}}$ | Routing trajectory | RED / RB paper |
| $\kappa_{\text{exec}}$ | Path‑A execution‑flow (DCB) | **Not** an identity geometry quantity |

Builders: never feed DCB `geometric_state.curvature` into $\kappa_{\text{id}}$ formulas without an explicit, separate bridge experiment.

---

## 4. Identity neighborhoods

First‑order identity distance:

$$
d(\mathbf{F}_1, \mathbf{F}_2)
=
\sum_i w_i \, |F_{1,i} - F_{2,i}|
$$

- $w_i$ initially uniform.
- Same neighborhood if $d(\mathbf{F}_1, \mathbf{F}_2) < \epsilon_{\text{nbhd}}$.

**IdOB use:** grouping candidates; **RB use:** local vs non‑local adjacency class.

---

## 5. Stability basins

Aligned to **Stable** regime (shared table):

$$
I_{\text{stab}} \ge 0.7
\quad\text{and}\quad
R_{\text{res}} \ge 0.6
$$

Inside a basin: roles persist, residue persists, routing tends local, $\|\Delta H\|$ tends small.

---

## 6. Drift vectors

$$
\vec{D} = \mathbf{F}_{t+1} - \mathbf{F}_{t},
\qquad
\|\vec{D}\| = d(\mathbf{F}_{t+1}, \mathbf{F}_{t})
$$

- Small $\|\vec{D}\|$ → refinement
- Medium → drift
- Large → transition

**Observation:** log $\|\vec{D}\|$ beside IdOB envelope and RB `adjacency_class`.

---

## 7. Identity curvature $\kappa_{\text{id}}$

Given $\mathbf{F}_{t-1}, \mathbf{F}_{t}, \mathbf{F}_{t+1}$:

$$
\kappa_{\text{id}}
=
\frac{
d(\mathbf{F}_{t-1}, \mathbf{F}_{t+1})}
{d(\mathbf{F}_{t-1}, \mathbf{F}_{t}) + d(\mathbf{F}_{t}, \mathbf{F}_{t+1})}
$$

- $\kappa_{\text{id}} \approx 0$ → straight trajectory (stable thinking)
- $\kappa_{\text{id}} \approx 1$ → sharp turn (identity shift)

---

## 8. Manifolds, attractors, collapse, transition

- **Manifold $\mathcal{M}$:** cluster of points with $d(\mathbf{F}, \mathbf{F}_{\text{center}}) < \epsilon_{\mathcal{M}}$ (families, modes, attractors).
- **Attractor $\mathbf{A}$:** $d(\mathbf{F}_{t+1}, \mathbf{A}) < d(\mathbf{F}_{t}, \mathbf{A})$ over multiple cycles.
- **Collapse region:** shared **Collapse** regime ($I_{\text{stab}} < 0.3$ and $R_{\text{res}} < 0.3$).
- **Transition surface:** $\|\Delta H\| = H_{\text{crit}}$ (shared placeholders).

---

## 9. How IdOB and RB use this geometry (first‑order)

| Actor | Geometric use |
|-------|----------------|
| **IdOB** | Place/update identity point; report neighborhood membership; detect basin vs collapse |
| **RB** | Read neighborhood / stability; classify local vs non‑local; propose next neighborhood |
| **DCB** | Independent execution‑flow indexer; supplies cycle context, not $\kappa_{\text{id}}$ |

---

## 10. Must‑observe (geometry layer)

Before enriching geometry:

1. Can we log $\mathbf{F}$ each cycle?
2. Do Stable basins co‑occur with IdOB role inheritance?
3. Do large $\|\vec{D}\|$ co‑occur with RB non‑local and Transition regime?
4. Is $\kappa_{\text{id}}$ distinguishable from $\kappa_{\text{exec}}$ in real runs?

---

## 11. Status and next steps

**Status:** First‑order geometric language for IdOB/RB examination.

**Next steps:** Integrate logging; validate neighborhoods empirically; connect residue topology; keep thresholds provisional.

This document is the geometric foundation of **TS Identity Dynamics** for first‑order IdOB work.

# ts_routing_entropy_dynamics.md

## 1. Purpose

This document defines the **first‑order dynamical model of routing and entropy** in TS and the **RB operator sketch** builders need to enter the space.

It complements:

- `ts_invariant_relational_model.md` (invariants, shared regimes, TP bridge)
- `ts_invariant_to_idob_theory.md` (IdOB operator $\mathcal{I}$)
- `ts_identity_geometry.md`
- `ts_semantic_residue_topology.md`

by describing how routing behavior and entropy changes interact, and what **RB** is responsible for as a first‑order Path‑A primitive concept.

This is a **rudimentary guide for building RB**, not a finished dynamics theory.

---

## 2. Routing space and RED

Routing operates over the identity geometry manifold (IGM). Each cognitive routing step moves:

$$
\mathbf{F}_t \rightarrow \mathbf{F}_{t+1}
$$

- Routing adjacency: $Rt_{\text{adj}}$
- Entropy change: $\Delta H = H_{t+1} - H_t$

Together they define **Routing–Entropy Dynamics (RED)**.

**Naming**

- $\kappa_{\text{route}}$ — routing trajectory curvature on IGM (this paper)
- $\kappa_{\text{id}}$ — identity trajectory curvature (identity geometry paper)
- $\kappa_{\text{exec}}$ — DCB Path‑A execution‑flow curvature (**not** used as routing curvature)

---

## 3. RB operator (first‑order)

RB is the Path‑A concept responsible for **routing proposals and adjacency observation** under RED. IdOB forms identity; RB proposes where thinking goes next in neighborhood terms.

$$
\mathcal{R} : (\mathbf{F}, \text{IdOB}_{\text{view}}, \text{context}_{\text{allowed}}) \rightarrow \text{RB\_out}
$$

### 3.1 RB_out (first‑order envelope)

| Field | Intent |
|-------|--------|
| `route_proposal` | Next neighborhood / role‑family target (symbolic or ordinal proxy) |
| `adjacency_class` | `local` \| `non_local` (first‑order) |
| `rt_adj` | Scalar or structured $Rt_{\text{adj}}$ observation/update |
| `regime_hint` | Stable / Refinement / Drift / Transition / Collapse (from shared table) |
| `displacement_scale` | Small / medium / large from RED interaction law |

### 3.2 Read set (first‑order)

- $\mathbf{F}$ components available (especially $I_{\text{stab}}$, $\Delta H$, $Rt_{\text{adj}}$ prior)
- IdOB stability / geometry **view** (read‑only; no IdOB mutation)
- Allowed continuity / context markers
- Optional: DCB `geometric_state` as **execution‑flow context only** (do not reinterpret as identity curvature)

### 3.3 Write set (first‑order)

- RB_out fields only (TP paths RB will own in its primitive requirements)
- **Must not** write IdOB envelope, DCB geometric history ownership, RBU meaning commits, or Path‑B truth fields

### 3.4 Determinism

Same $\mathbf{F}$ + IdOB view + allowed context → same RB_out.

---

## 4. Local vs non‑local routing

Use shared placeholders $a_{\text{local}}$, $a_{\text{nonlocal}}$, $H_{\text{small}}$, $H_{\text{crit}}$ from the relational model.

### 4.1 Local routing

$$
Rt_{\text{adj}} < a_{\text{local}}
\quad\text{and}\quad
\|\Delta H\| < H_{\text{small}}
$$

Effects: small geometric displacement; refinement; stable trajectory; residue strengthening tendency.

### 4.2 Non‑local routing

$$
Rt_{\text{adj}} > a_{\text{nonlocal}}
\quad\text{or}\quad
\|\Delta H\| > H_{\text{crit}}
$$

Effects: large displacement; identity shift pressure; residue reconfiguration; provenance branching risk.

**RB rule (first‑order):** Prefer local proposals when regime is Stable or Refinement; allow non‑local proposals when regime is Transition (and do not fake locality under Collapse).

---

## 5. Entropy regimes (aligned to shared table)

| RED emphasis | Shared regime link | Identity / routing behavior |
|--------------|--------------------|-----------------------------|
| $\|\Delta H\| < H_{\text{small}}$ | Refinement (and often Stable) | Local refinement, stable residue/provenance |
| moderate $\|\Delta H\|$ | Drift | Partial residue drift, weakening provenance, higher $\kappa_{\text{route}}$ |
| $\|\Delta H\| \ge H_{\text{crit}}$ | Transition | Jumps, geometry shift, branching |
| with collapse thresholds | Collapse | Reset pressures; RB must not invent false continuity |

---

## 6. Routing–entropy interaction law

$$
\text{routing displacement} \propto Rt_{\text{adj}} \cdot \|\Delta H\|
$$

| Adjacency | Entropy | Displacement (first‑order) |
|-----------|---------|----------------------------|
| Local | Small | Small |
| Local | Large | Medium |
| Non‑local | Small | Medium |
| Non‑local | Large | Large |

This is the **cognitive motion** sketch RB implements as `displacement_scale`.

---

## 7. Routing curvature

Given $\mathbf{F}_{t-1}, \mathbf{F}_{t}, \mathbf{F}_{t+1}$:

$$
\kappa_{\text{route}}
=
\frac{
d(\mathbf{F}_{t-1}, \mathbf{F}_{t+1})}
{d(\mathbf{F}_{t-1}, \mathbf{F}_{t}) + d(\mathbf{F}_{t}, \mathbf{F}_{t+1})}
$$

- $\kappa_{\text{route}} \approx 0$ → stable routing direction
- $\kappa_{\text{route}} \approx 1$ → routing turn / shift

Use for **observation and diagnostics**, not as a substitute for DCB $\kappa_{\text{exec}}$.

---

## 8. Attractors, collapse, transition surfaces

- **Routing attractors:** points $\mathbf{A}$ with decreasing distance over multiple cycles (stable roles / anchors).
- **Collapse surface (joint):** high $Rt_{\text{adj}}$ and high $\|\Delta H\|$ with Collapse regime → identity/residue/provenance reset pressure.
- **Transition surface:** $\|\Delta H\| = H_{\text{crit}}$ → non‑local pressure, geometry jump, residue reconfiguration.

---

## 9. Must‑prove vs defer (RB v1 foundation)

**Must prove**

- Deterministic $\mathcal{R}$ for fixed inputs.
- Clear local vs non‑local classification.
- `displacement_scale` consistent with RED interaction law directionally.
- Write boundary: no IdOB / DCB ownership leakage.
- Regime_hint consistent with shared regime table given $\mathbf{F}$.
- Progressive‑test structural checks on RB_out shape.

**Defer**

- Multi‑lane / rich continuous routing geometry.
- Learned adjacency metrics.
- Full attractor discovery algorithms.
- Binding RB proposals to final TR policy (TR remains downstream).

---

## 10. Observation questions (proper questions for RB)

1. When $I_{\text{stab}}$ is high, does RB actually keep `adjacency_class = local`?
2. When $\|\Delta H\|$ crosses $H_{\text{crit}}$, does RB emit non‑local without waiting for IdOB collapse?
3. Does RB over‑stabilize (force local) under Drift, masking real transitions?
4. How does RB behave if IdOB view is missing vs present?
5. Are $Rt_{\text{adj}}$ logs consistent with DCB execution order, or do they conflict (exec vs cognitive layers)?

---

## 11. Status and next steps

**Status:** First‑order RED model + **RB operator** build guide.

**Next steps:**

- Draft RB primitive requirements + structural program from $\mathcal{R}$.
- Log RB_out beside $\mathbf{F}$ and IdOB envelope in progressive tests.
- Falsify local/non‑local and displacement laws before enriching geometry.
- Keep IdOB as identity engine; RB as routing proposal engine; DCB as execution‑flow indexer.

This document is the dynamical foundation of **TS Routing and Entropy Dynamics** and the first‑order **RB build guide**.

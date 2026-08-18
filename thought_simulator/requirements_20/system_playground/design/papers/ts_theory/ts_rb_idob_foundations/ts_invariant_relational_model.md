# ts_invariant_relational_model.md

## 1. Purpose

**Goal:** Define a first‑order relational model for TS invariants so that:

- **Space:** The TS cognitive space is structurally definable.
- **Observation:** Relationships among invariants are observable and loggable.
- **Theory:** Early laws of TS cognitive dynamics can be stated and tested.
- **Build guide:** RB and IdOB can be designed against a shared feature space, regime table, and measurement contract.

This is a **rudimentary, first‑order model**—a starting point for progressive lineup testing and primitive design, not a final theory.

**Reading order for builders**

1. This file (invariants, laws, regimes, TP bridge)
2. `ts_invariant_to_idob_theory.md` (IdOB operator)
3. `ts_routing_entropy_dynamics.md` (RB operator + RED)
4. `ts_identity_geometry.md` / `ts_semantic_residue_topology.md` (geometry language)

---

## 2. Core invariants (first pass)

**Invariant set (symbolic):**

| Symbol | Name | Role for RB / IdOB |
|--------|------|--------------------|
| $I_{\text{stab}}$ | Identity stability | IdOB primary; RB reads for local vs exploratory routing |
| $R_{\text{res}}$ | Semantic‑residue persistence | IdOB residue inheritance; RB continuity signal |
| $P_{\text{cont}}$ | Provenance continuity | IdOB provenance depth; RB trusts chain integrity |
| $L_{\text{depth}}$ | Lineage depth | IdOB lineage markers; long‑range process scale |
| $Rt_{\text{adj}}$ | Routing adjacency | **RB primary write/observe**; IdOB geometry shift input |
| $\Delta H$ | Entropy change per cycle | Regime classifier; RB displacement scale |
| $E_{\text{dens}}$ | Expressive metadata density | IdOB alignment; expression richness |
| $C_{\text{coh}}$ | Continuity metadata coherence | IdOB alignment; narrative vs spray |

Each invariant is assumed to be:

- **Bounded per cycle** (finite scalar or small vector).
- **Deterministic** (same inputs → same value).
- **Loggable** (available to testbenches and replay).

Feature vector for an IdOB / cycle observation:

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

---

## 3. Shared regime table (provisional, single source)

All sibling papers in this folder **use this table**. Thresholds are placeholders for first‑order examination only.

| Regime | Provisional conditions | Expected behavior (first‑order) |
|--------|------------------------|----------------------------------|
| **Stable** | $I_{\text{stab}} \ge 0.7$, $R_{\text{res}} \ge 0.6$, $P_{\text{cont}} \ge 0.5$ | Roles persist; residue persists; RB stays local; small $\|\Delta H\|$ |
| **Refinement** | $\|\Delta H\| < H_{\text{small}}$, $Rt_{\text{adj}}$ local | Roles sharpen; residue strengthens; local geometry tighten |
| **Drift** | $I_{\text{stab}} < 0.5$ or $P_{\text{cont}} < 0.4$; moderate $\|\Delta H\|$ | Roles weaken; partial residue drift; increased $\kappa_{\text{id}}$ |
| **Transition** | $\|\Delta H\| \ge H_{\text{crit}}$ or $Rt_{\text{adj}}$ non‑local | Geometry jump; provenance branch; partial residue reset |
| **Collapse** | $I_{\text{stab}} < 0.3$ and $R_{\text{res}} < 0.3$ | Roles reset; residue reset; provenance break; reinitialize |

**Placeholder scalars (tune later):**

- $H_{\text{small}} = 0.15$
- $H_{\text{crit}} = 0.40$
- $a_{\text{local}} = 0.30$ (routing adjacency scale; define with neighborhood metric)
- $a_{\text{nonlocal}} = 0.70$

**Builder rule:** Classify each logged cycle into exactly one primary regime using this table before interpreting RB or IdOB behavior.

---

## 4. First‑order relational laws (qualitative)

These are **directional hypotheses**—co‑variation tendencies to falsify, not closed equations.

### 4.1 IR‑1 — Identity stability ↔ residue persistence

- High $I_{\text{stab}}$ → $R_{\text{res}}$ tends high.
- Low $I_{\text{stab}}$ → $R_{\text{res}}$ tends low or frequently resets.

**Observation question:** When identity descriptors hold over a window, does residue token overlap also hold?

### 4.2 IR‑2 — Lineage depth ↔ provenance continuity

- High $L_{\text{depth}}$ + high $P_{\text{cont}}$ → coherent long‑range process.
- High $L_{\text{depth}}$ + low $P_{\text{cont}}$ → accumulated drift / noise.

**Observation question:** Does deep lineage without continuous provenance correlate with collapse / transition flags?

### 4.3 IR‑3 — $\Delta H$ ↔ routing adjacency

- Large $\|\Delta H\|$ → non‑local routing transitions.
- Small $\|\Delta H\|$ → local refinement.

**Observation question:** Do large entropy jumps co‑occur with $Rt_{\text{adj}}$ leaving the prior neighborhood?

### 4.4 IR‑4 — Expressive density ↔ continuity coherence

- High $E_{\text{dens}}$ + high $C_{\text{coh}}$ → structured sustained expression.
- High $E_{\text{dens}}$ + low $C_{\text{coh}}$ → fragmented expression.

### 4.5 IR‑5 — Identity stability ↔ routing adjacency

- High $I_{\text{stab}}$ → $Rt_{\text{adj}}$ remains in a small neighborhood.
- Low $I_{\text{stab}}$ → frequent non‑local $Rt_{\text{adj}}$ jumps.

**RB / IdOB implication:** Stable identity should bias RB toward local proposals; unstable identity should not be forced local by RB.

---

## 5. Measurement notes (operational first‑order)

Use a fixed **window** $W = 10$ cycles for rate‑style invariants unless a test specifies otherwise.

| Invariant | First‑order measurement |
|-----------|-------------------------|
| $I_{\text{stab}}$ | Fraction of cycles in $W$ where identity descriptors stay within a fixed variation band (band defined by IdOB field equality or distance $< \epsilon_{\text{id}}$) |
| $R_{\text{res}}$ | Overlap $\|R_t \cap R_{t-1}\| / \max(1, \|R_t\|)$ averaged over $W$, or token persistence fraction |
| $P_{\text{cont}}$ | Fraction of steps in $W$ with unbroken provenance links |
| $L_{\text{depth}}$ | Max linked cycle length for current identity trajectory |
| $Rt_{\text{adj}}$ | Fraction of routing steps that remain inside the prior OB/role neighborhood (or continuous distance on IGM) |
| $\Delta H$ | Scalar entropy difference $H_{t+1}-H_t$ using **one fixed** TS entropy definition |
| $E_{\text{dens}}$ | Normalized count of expressive metadata tokens per cycle |
| $C_{\text{coh}}$ | Overlap / coherence of continuity markers (topic, goal, stance) across adjacent cycles |

**Must log per cycle in progressive tests when examining RB/IdOB:** $\mathbf{F}$ components (even crude scalars), regime label, and TP source fields used.

---

## 6. Bridge map — invariants to Path‑A TP / primitives (first‑order)

This does **not** freeze implementation. It tells builders **where to look first** when computing or approximating $\mathbf{F}$.

| Invariant | Primary TP / primitive sources (provisional) |
|-----------|-----------------------------------------------|
| $I_{\text{stab}}$ | IdOB identity fields over $W$; RBU committed `semantic.identity` / stance stability |
| $R_{\text{res}}$ | `metadata.residue` (or semantic residue trails); persistence across cycles |
| $P_{\text{cont}}$ | `metadata.provenance` chains; unbroken `dcb_last_update` / primitive provenance links |
| $L_{\text{depth}}$ | `metadata.lineage_markers`, `lineage_log[]` |
| $Rt_{\text{adj}}$ | **RB outputs** (proposed); DCB `geometric_state` / history as **execution‑flow** context only |
| $\Delta H$ | Entropy metadata if present; otherwise fixed function of semantic + residue + geometry deltas |
| $E_{\text{dens}}$ | Expressive metadata; STPX cue density as optional proxy |
| $C_{\text{coh}}$ | Continuity / context markers (`metadata.context`, continuity_metadata) |

### 6.1 Curvature disambiguation (mandatory naming)

| Symbol | Layer | Meaning |
|--------|-------|---------|
| $\kappa_{\text{exec}}$ | **DCB / Path‑A accounting** | Binary sequential deviation on PATH_A ordinals (`geometric_state.curvature`) |
| $\kappa_{\text{id}}$ | **Identity geometry** | Trajectory bend of $\mathbf{F}$ on the identity manifold |
| $\kappa_{\text{route}}$ | **Routing–entropy dynamics** | Trajectory bend of successive routing positions on IGM |

**Do not** treat DCB $\kappa_{\text{exec}}$ as identity or routing curvature. RB/IdOB theory uses $\kappa_{\text{id}}$ / $\kappa_{\text{route}}$ only.

---

## 7. Hooks for IdOB grouping and statistical hashing

- **Feature vector:** $\mathbf{F}$ as above.
- **Relational constraints:** IR‑1…IR‑5 define expected co‑variation; deviations mark drift, collapse, or novel regimes.
- **Statistical hash (conceptual):** Map $\mathbf{F}$ to a lower‑dimensional signature that preserves stability regions, residue regimes, lineage/provenance coherence, and routing/entropy dynamics.

This file does **not** define the hash—it defines the **relational backbone** a hash must respect.

---

## 8. First‑order questions this model is designed to enable

1. Do IR‑1…IR‑5 hold under progressive lineup logs?
2. Which regime dominates healthy Path‑A runs vs pathological ones?
3. Does RB’s local/non‑local proposal track $I_{\text{stab}}$ and $\Delta H$ as IR‑3/IR‑5 predict?
4. Does IdOB’s role inheritance track the stable/refinement regimes?
5. Where do elemental TP fields fail to support a reliable $\mathbf{F}$ component?

---

## 9. Status and next steps

**Status:** First‑order relational model + shared regimes + TP bridge for RB/IdOB guidance.

**Next steps:**

- Log $\mathbf{F}$ and regime labels in progressive tests.
- Empirically test IR‑1…IR‑5.
- Refine thresholds from observed distributions.
- Design first IdOB statistical hash constrained by this backbone.
- Keep RB and IdOB primitive requirements aligned to operators in sibling papers.

This document is the **seed** of **TS Invariant Relational Dynamics** and the shared guide for first‑order RB / IdOB examination.

# ts_invariant_to_idob_theory.md

## 1. Purpose

This document defines a **first‑order generative theory** that maps TS invariants to IdOB formation.  
It complements `ts_invariant_relational_model.md` by specifying:

- the **input space** (invariant vector $\mathbf{F}$),
- the **output space** (IdOB envelope),
- the **operator** $\mathcal{I}$,
- **regimes** (shared table),
- **must‑prove vs defer** for a first IdOB realization,
- and **observation questions** for progressive testing.

This is a **rudimentary guide for building IdOB**, not a finished cognitive theory.

---

## 2. Invariant input space

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

Definitions, measurements, and the **shared regime table** live in `ts_invariant_relational_model.md`.  
IdOB **reads** $\mathbf{F}$ (or TP fields that approximate it). IdOB does **not** invent a second regime system.

---

## 3. IdOB output space (first‑order envelope)

$$
\text{IdOB} =
\left(
\text{roles},
\text{candidates},
\text{provenance},
\text{geometry},
\text{residue},
\text{stability},
\text{alignment},
\text{lineage}
\right)
$$

**First‑order field intent**

| Field | Intent |
|-------|--------|
| roles | Active identity roles (inherit vs new) |
| candidates | Provisional identity candidates under consideration |
| provenance | Identity‑side provenance extension / truncation |
| geometry | Local position / neighborhood markers on IGM ($\kappa_{\text{id}}$‑relevant) |
| residue | Inherited or reset semantic residue markers |
| stability | Stability indicator (typically mirrors $I_{\text{stab}}$) |
| alignment | Alignment markers from $E_{\text{dens}}, C_{\text{coh}}$ |
| lineage | Lineage markers (typically mirrors $L_{\text{depth}}$) |

**Boundary (first‑order):** IdOB forms and updates **identity structure**. It does not own Path‑A execution‑flow indexing (DCB) and does not own routing proposals (RB).

---

## 4. The generative operator

$$
\mathcal{I} : \mathbf{F} \rightarrow \text{IdOB}
$$

$\mathcal{I}$ is a **set of relational generative laws**, not a single closed equation.  
Implementation may be deterministic rule tables + pure functions over $\mathbf{F}$ and prior IdOB state.

**Read set (first‑order)**

- $\mathbf{F}$ (or TP approximations per bridge map)
- prior IdOB envelope if present
- allowed TP identity / residue / lineage / provenance fields

**Write set (first‑order)**

- IdOB envelope fields only (or the TP paths IdOB is specified to own in its primitive requirements)
- no DCB geometric_state, no RB routing proposal fields, no Path‑B truth fields

---

## 5. Regimes (shared table)

Use the **shared regime table** in `ts_invariant_relational_model.md`:

Stable · Refinement · Drift · Transition · Collapse

### 5.1 Effects on IdOB (by regime)

| Regime | IdOB first‑order effect |
|--------|-------------------------|
| **Stable** | Inherit prior roles; extend provenance; persist residue; geometry stays local |
| **Refinement** | Sharpen roles; strengthen residue; deepen provenance; tighten geometry |
| **Drift** | Weaken/fragment roles; partial residue drift; discontinuous provenance; geometry shifts |
| **Transition** | Shift roles; geometry jump; branch provenance; partial residue reset |
| **Collapse** | Reset roles; reset residue; break provenance; reinitialize geometry |

---

## 6. First‑order generative laws

### 6.1 Identity roles

$$
\text{roles} \leftarrow
\begin{cases}
\text{prior roles}, & \text{Stable or Refinement} \\
\text{weakened / new roles}, & \text{Drift or Transition} \\
\text{reset}, & \text{Collapse}
\end{cases}
$$

### 6.2 Semantic residue

$$
\text{residue inheritance strength} \propto R_{\text{res}}
$$

High persistence → inherit; low → reset (especially Collapse).

### 6.3 Provenance

$$
\text{provenance depth} \propto P_{\text{cont}} \cdot L_{\text{depth}}
$$

Broken $P_{\text{cont}}$ → truncated provenance.

### 6.4 Identity geometry

$$
\text{geometry shift scale} \propto f(Rt_{\text{adj}}, \|\Delta H\|)
$$

Local + small $\|\Delta H\|$ → small moves; non‑local or large $\|\Delta H\|$ → jumps.  
Use $\kappa_{\text{id}}$, **not** DCB $\kappa_{\text{exec}}$.

### 6.5 Stability indicators

$$
\text{stability} \approx I_{\text{stab}}
$$

### 6.6 Alignment markers

$$
\text{alignment} \propto C_{\text{coh}} \cdot E_{\text{dens}}
$$

### 6.7 Lineage markers

$$
\text{lineage} \approx L_{\text{depth}}
$$

### 6.8 Combined sketch

$$
\text{IdOB} = \mathcal{I}(\mathbf{F}, \text{IdOB}_{\text{prev}})
$$

---

## 7. Must‑prove vs defer (IdOB v1 foundation)

**Must prove (before treating IdOB as a build foundation)**

- Deterministic $\mathcal{I}$ given same $\mathbf{F}$ and prior IdOB.
- Explicit read/write boundary (no DCB / RB / Path‑B leakage).
- Regime‑conditioned role inherit vs reset behavior is observable.
- Residue inherit vs reset tracks $R_{\text{res}}$ directionally.
- Provenance extend vs truncate tracks $P_{\text{cont}}$.
- Envelope shape stable enough for progressive test structural checks.
- Replay: identical inputs → identical IdOB outputs.

**Defer**

- Final role taxonomies and candidate scoring sophistication.
- Learned statistical hash parameters.
- Continuous geometry beyond first‑order neighborhood markers.
- Empirical threshold tuning as “truth” (keep provisional).
- Cross‑primitive optimization of meaning density.

---

## 8. Observation questions (proper questions for the space)

1. Under Stable windows, how often does IdOB actually inherit roles vs silently rewrite?
2. At Collapse, does every identity‑owned field reset, or do hidden residues remain?
3. Does Transition produce geometry jumps that RB later treats as non‑local?
4. Which components of $\mathbf{F}$ are still missing reliable TP sources?
5. Do IR‑1 and IR‑2 hold when IdOB is in the loop, or only on synthetic $\mathbf{F}$?

---

## 9. Status and next steps

**Status:** First‑order IdOB build guide: operator, envelope, regimes, must‑prove list.

**Next steps:**

- Draft IdOB primitive requirements + structural program from this operator.
- Log $\mathbf{F}$ + regime + IdOB envelope in progressive tests.
- Falsify generative laws before expanding envelope complexity.
- Keep RB operator (`ts_routing_entropy_dynamics.md`) as the routing counterpart, not a second identity engine.

This document is the **first generative guide** for **TS Invariant‑Driven Identity Dynamics (IdOB)**.

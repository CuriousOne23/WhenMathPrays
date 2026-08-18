# ts_invariant_to_idob_theory.md

## 1. Purpose

This document defines a **first‑order generative theory** that maps TS invariants to IdOB formation.  
It complements `ts_invariant_relational_model.md` by specifying:

- the **input space** (invariant vector),
- the **output space** (IdOB envelope),
- the **mapping** between them,
- the **regimes** that govern identity formation,
- and the **first‑order laws** that describe how invariants produce IdOB structure.

This is a **rudimentary, first‑order theory** intended for early testing and refinement.

---

## 2. Invariant input space

The invariant vector is:

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

Each component is defined in `ts_invariant_relational_model.md` and is:

- deterministic per cycle,
- bounded per cycle,
- loggable,
- observable.

This vector represents the **state of TS cognitive dynamics** at a given cycle.

---

## 3. IdOB output space

An IdOB envelope contains:

- identity candidates  
- identity roles  
- identity provenance  
- identity geometry  
- semantic residues  
- stability indicators  
- alignment markers  
- lineage markers  

We denote an IdOB as:

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

The goal of this theory is to define how $\mathbf{F}$ produces this structure.

---

## 4. The generative mapping

We define the identity‑formation operator:

$$
\mathcal{I} : \mathbf{F} \rightarrow \text{IdOB}
$$

This operator is **not** a single equation.  
It is a **set of relational generative laws** that determine how invariants shape IdOB fields.

The mapping is governed by **regimes** and **first‑order laws**.

---

## 5. Identity regimes

Identity formation behaves differently depending on invariant thresholds.  
We define five first‑order regimes.

### 5.1 Stable identity regime

Conditions:

$$
I_{\text{stab}} > 0.8,\quad
R_{\text{res}} > 0.7,\quad
P_{\text{cont}} > 0.6
$$

Effects:

- IdOB inherits prior identity roles.
- Provenance chains extend.
- Semantic residue persists.
- Identity geometry remains in a local neighborhood.

### 5.2 Drift regime

Conditions:

$$
I_{\text{stab}} < 0.5,\quad
P_{\text{cont}} < 0.4
$$

Effects:

- Identity roles weaken or fragment.
- Residue partially resets.
- Provenance becomes discontinuous.
- Geometry begins to shift.

### 5.3 Collapse regime

Conditions:

$$
I_{\text{stab}} < 0.3,\quad
R_{\text{res}} < 0.3
$$

Effects:

- Identity roles collapse.
- Residue resets.
- Provenance breaks.
- Geometry reinitializes.

### 5.4 Refinement regime

Conditions:

$$
|\Delta H| < H_{\text{small}},\quad
Rt_{\text{adj}} \text{ local}
$$

Effects:

- Identity roles sharpen.
- Residue strengthens.
- Provenance deepens.
- Geometry tightens.

### 5.5 Transition regime

Conditions:

$$
|\Delta H| > H_{\text{crit}},\quad
Rt_{\text{adj}} \text{ non‑local}
$$

Effects:

- Identity roles shift.
- Geometry jumps.
- Provenance branches.
- Residue partially resets.

---

## 6. First‑order generative laws

These laws define how invariants produce IdOB fields.

### 6.1 Identity roles

$$
\text{roles} \leftarrow 
\begin{cases}
\text{prior roles}, & I_{\text{stab}} \text{ high} \\
\text{new roles}, & I_{\text{stab}} \text{ low}
\end{cases}
$$

### 6.2 Semantic residue

$$
\text{residue} \propto R_{\text{res}}
$$

High residue persistence → strong residue inheritance.  
Low persistence → residue reset.

### 6.3 Provenance

$$
\text{provenance depth} \propto P_{\text{cont}} \cdot L_{\text{depth}}
$$

Continuous provenance + deep lineage → extended provenance.  
Broken provenance → truncated provenance.

### 6.4 Identity geometry

$$
\text{geometry shift} \propto Rt_{\text{adj}} \cdot \Delta H
$$

Local adjacency + small entropy → small geometric moves.  
Non‑local adjacency + large entropy → geometric jumps.

### 6.5 Stability indicators

$$
\text{stability} = I_{\text{stab}}
$$

Direct mapping.

### 6.6 Alignment markers

$$
\text{alignment} \propto C_{\text{coh}} \cdot E_{\text{dens}}
$$

High expressive density + high continuity → strong alignment.  
High expressive density + low continuity → fragmented alignment.

### 6.7 Lineage markers

$$
\text{lineage} = L_{\text{depth}}
$$

Direct mapping.

---

## 7. Combined generative model

Putting the laws together:

$$
\text{IdOB} = \mathcal{I}(\mathbf{F}) =
\left(
\text{roles}(I_{\text{stab}}),
\text{residue}(R_{\text{res}}),
\text{provenance}(P_{\text{cont}}, L_{\text{depth}}),
\text{geometry}(Rt_{\text{adj}}, \Delta H),
\text{stability}(I_{\text{stab}}),
\text{alignment}(E_{\text{dens}}, C_{\text{coh}}),
\text{lineage}(L_{\text{depth}})
\right)
$$

This is the **first‑order generative theory** for IdOB formation.

---

## 8. Status and next steps

**Status:**  
- This is a first‑order generative model.  
- All laws are hypotheses.  
- Regimes are provisional.

**Next steps:**  
- Integrate with progressive lineup testing.  
- Empirically validate regime boundaries.  
- Refine generative laws based on observed IdOB behavior.  
- Connect this theory to the statistical hash model.

This document is the **first generative theory** in the emerging field of  
**TS Invariant‑Driven Identity Dynamics**.

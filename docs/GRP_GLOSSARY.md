# **GRP_GLOSSARY.md**  
### *General Relational Physics — Formal Glossary of Terms*  
### *A canonical lexicon for relational geometry, posture, and motion*

This glossary defines the core terminology introduced or formalized by General Relational Physics (GRP).  
Each entry includes:

- **Definition** — the formal meaning  
- **Role in GRP** — why the term matters  
- **Mathematical / geometric interpretation**  
- **Cross‑links** to relevant documents  

For conceptual context, see:  
- `grp_principles.md`  
- `PRIMITIVES_AND_RELATIONAL_SPACE.md`  
- `THE_STORY_OF_GRP.md`  
- `RELATIONAL_SUPPRESSION_LOAD.md`  

---

# **A. Foundational Geometry**

---

## **γ_self (gamma_self)**  
**Definition:**  
A complex coordinate representing an agent’s relational posture toward another agent at a given moment.

**Role in GRP:**  
The fundamental observable of relational identity and motion.

**Mathematical Meaning:**  
A point in the relational manifold:  
- Re(γ_self): Ego ↔ We  
- Im(γ_self): Hate ↔ Love  

**Cross‑links:**  
`grp_principles.md`, `PRIMITIVES_AND_RELATIONAL_SPACE.md`

---

## **Relational Manifold**  
**Definition:**  
The geometric space of all possible relational postures; the topology in which γ_self lives and moves.

**Role in GRP:**  
Defines the shape of relational possibility and constrains trajectories.

**Mathematical Meaning:**  
A continuous, differentiable manifold supporting curvature, basins, divergence, and asymmetry.

**Cross‑links:**  
`grp_principles.md`

---

## **Trajectory of Relation**  
**Definition:**  
The path traced by γ_self through the relational manifold over time.

**Role in GRP:**  
The primary unit of analysis; relational phenomena are trajectories, not states.

**Mathematical Meaning:**  
A sequence {γ_self(0), γ_self(1), …, γ_self(N)} with curvature κ and velocity v.

**Cross‑links:**  
`grp_principles.md`, `SCENARIO_CONFIGURATION_GUIDE.md`

---

## **Relational Meaning Field**  
**Definition:**  
The field induced by motion through the relational manifold; meaning emerges from the gradient of relational motion.

**Role in GRP:**  
Unifies phenomenology, physics, and engineering.

**Mathematical Meaning:**  
Meaning = ∂γ_self/∂t (directional derivative) + curvature effects.

**Cross‑links:**  
`grp_principles.md`

---

## **Relational Stability Basin**  
**Definition:**  
A region of the relational manifold where trajectories naturally converge; the geometric representation of trust, coherence, or alignment.

**Role in GRP:**  
Models long‑term relational patterns and stable relational identity.

**Mathematical Meaning:**  
An attractor region with defined boundaries and curvature.

**Cross‑links:**  
`grp_principles.md`, `SCENARIO_CONFIGURATION_GUIDE.md`

---

## **Relational Asymmetry**  
**Definition:**  
The structural divergence between two agents’ relational positions; the fact that M1’s γ_self toward M2 differs from M2’s γ_self toward M1.

**Role in GRP:**  
A foundational principle; asymmetry is not noise but structure.

**Mathematical Meaning:**  
γ_self(M1→M2) ≠ γ_self(M2→M1)

**Cross‑links:**  
`grp_principles.md`, Omnisyndetics article (philosophical precursor)

---

# **B. Relational Dynamics**

---

## **Relational Posture**  
**Definition:**  
The stance an agent takes toward another at a given moment, represented as a coordinate in γ_self.

**Role in GRP:**  
The instantaneous relational identity.

**Cross‑links:**  
`grp_principles.md`

---

## **Relational Motion**  
**Definition:**  
The dynamic evolution of relational posture over time.

**Role in GRP:**  
The core phenomenon GRP models.

**Mathematical Meaning:**  
Δγ_self = f(v, r, f, a, S)

---

## **Autocorrelation Period**  
**Definition:**  
The persistence window of a relational posture before drift becomes significant.

**Role in GRP:**  
Determines how long a stance remains stable without new relational input.

**Cross‑links:**  
`grp_principles.md`

---

## **Relational Rupture**  
**Definition:**  
A divergence of trajectories beyond the boundary of a stability basin.

**Role in GRP:**  
Models breakdowns in coherence, trust, or shared identity.

**Cross‑links:**  
`grp_principles.md`

---

## **Relational Repair Path**  
**Definition:**  
A trajectory that returns an agent to a stability basin after rupture.

**Role in GRP:**  
Models reconciliation, healing, and re‑alignment.

**Cross‑links:**  
`grp_principles.md`

---

# **C. Forces, Loads, and Constraints**

---

## **RSL (Relational Suppression Load)**  
**Definition:**  
The geometric distortion introduced when an agent suppresses relational primitives.

**Role in GRP:**  
Models internal strain, incoherence, and destabilization.

**Mathematical Meaning:**  
RSL increases curvature and reduces basin depth.

**Cross‑links:**  
`RELATIONAL_SUPPRESSION_LOAD.md`

---

## **Entropy Drift (ΔS)**  
**Definition:**  
The natural tendency of γ_self to drift when relational input is absent.

**Role in GRP:**  
Models decay, forgetting, and loss of coherence.

**Mathematical Meaning:**  
γ_self(n+1) = γ_self(n) − ΔS·Δt

**Cross‑links:**  
`grp_principles.md`

---

# **D. Structural Concepts**

---

## **Technical Diary**  
**Definition:**  
A structured record of γ_self trajectories over time.

**Role in GRP:**  
Captures relational motion without narrative interpretation.

**Cross‑links:**  
`grp_principles.md`, `SCENARIO_CONFIGURATION_GUIDE.md`

---

## **Event Density N(x, y)**  
**Definition:**  
A measure of how frequently γ_self visits regions of the relational manifold.

**Role in GRP:**  
Encodes memory as spatial density rather than symbolic storage.

**Cross‑links:**  
`PRIMITIVES_AND_RELATIONAL_SPACE.md`

---

## **Relational Character Geometry**  
**Definition:**  
The overarching framework that models relational identity, motion, and meaning as geometric structures.

**Role in GRP:**  
The field GRP inaugurates.

**Cross‑links:**  
`grp_principles.md`

---

# **E. Removed or Deprecated Terms**

---

## **W(t)**  
**Definition:**  
Formerly the “we‑trajectory” computed via gates; removed in December 2025.

**Role in GRP:**  
Replaced by γ_self position itself.

**Cross‑links:**  
`grp_principles.md`, `GRP_rev3.5.md`

---

# **F. Cross‑Reference Map**

| Term | Primary Doc | Secondary Docs |
|------|-------------|----------------|
| γ_self | grp_principles.md | PRIMITIVES_AND_RELATIONAL_SPACE.md |
| Relational Manifold | grp_principles.md | — |
| Stability Basin | grp_principles.md | SCENARIO_CONFIGURATION_GUIDE.md |
| RSL | RELATIONAL_SUPPRESSION_LOAD.md | grp_principles.md |
| Technical Diary | grp_principles.md | SCENARIO_CONFIGURATION_GUIDE.md |
| Relational Asymmetry | grp_principles.md | Omnisyndetics article |

---

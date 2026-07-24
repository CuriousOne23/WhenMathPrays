# Phi‑G Field Specification for SOB, SROB, CnOB, SmOB and SSG

## 1. Purpose and scope

This document specifies the **field‑level design** for the phi‑G data structure, focusing on:

- **SSG** (Structural Signature Generator)  
- **SOB** (Structural Observation Block)  
- **SROB** (Structural Relational Observation Block)  
- **CnOB** (Contextual Observation Block)  
- **SmOB** (Semantic Observation Block)  

The goal is to translate the **Round 2.5 stress test** and the constraints in `phi_g_data_struc_cnstrnts.md` into **concrete field definitions, ranges, and properties** that can be implemented directly.

This paper assumes:

- Δ‑norm per step must remain in the **0.08–0.12** band (≤ 0.12 ceiling).  
- Determinism must remain **≥ 99.8%** (observed 100%).  
- Output validity must remain **≥ 97%** (one scenario at 96.9% is acceptable but tight).  
- Performance must remain **≤ 10 ms/step** on laptop hardware (observed 5.9–7.3 ms).  
- Structural TP field budget is **~20–40 fields** total.

All field specifications below are designed to respect these constraints.

---

## 2. Global field design principles

### 2.1 Shared conventions

- **Field type:** All structural fields are real‑valued scalars or small fixed‑size vectors.  
- **Normalization:** All fields are normalized into **[-1, 1]** or **[0, 1]** before aggregation into G.  
- **Contribution to Δ‑norm:** Each block’s total contribution to the structural vector field must respect its budget (see below).  
- **Coupling:** Cross‑field coupling is allowed but must be **bounded and sparse** to avoid resonance explosions.  
- **Determinism:** No stochastic components are allowed in field computation for TS V1.

### 2.2 Block‑level Δ‑norm budgets

Approximate per‑block contribution to the structural Δ‑norm:

- **SSG:** ≤ 0.04  
- **SOB:** ≤ 0.03  
- **SROB:** ≤ 0.04 (especially during basin transitions)  
- **CnOB:** ≤ 0.02  
- **SmOB:** ≤ 0.03  

These are **design targets**, not hard mathematical equalities, but they must be respected in implementation.

### 2.3 Dimensionality budget

Within the **20–40 structural TP fields**:

- **SSG:** 6–10 fields  
- **SOB:** up to 10 fields  
- **SROB:** 5–10 fields  
- **CnOB:** up to 8 fields  
- **SmOB:** up to 8 fields  

Overlap is allowed (e.g., some fields may be shared or reused), but the **effective independent dimensions** must remain in the 20–40 range.

---

## 3. SSG (Structural Signature Generator) field specification

### 3.1 Role

SSG produces the **core structural signature** that seeds the G manifold. It encodes the “shape” of the structural regime: symmetry, sparsity, curvature, and dominant axes.

### 3.2 Field list and properties

**SSG.1 – Global curvature magnitude**

- **Type:** scalar, float  
- **Range:** [0, 1] (0 = flat, 1 = highly curved)  
- **Source:** aggregated from SOB + SROB structural features  
- **Effect:** scales curvature‑sensitive channels in G  
- **Constraint:** must be smoothed over time (e.g., EMA) to avoid spikes that push Δ > 0.12.

---

**SSG.2 – Structural anisotropy**

- **Type:** scalar, float  
- **Range:** [-1, 1]  
- **Interpretation:**  
  - -1 = strongly anisotropic in one direction  
  - 0 = isotropic  
  - +1 = strongly anisotropic in another direction  
- **Effect:** biases G towards specific structural axes (e.g., tree‑like vs grid‑like).  
- **Constraint:** derivative per step must be bounded (|Δ| ≤ 0.1).

---

**SSG.3 – Basin complexity index**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** approximate number/complexity of basins in the current structural regime.  
- **Effect:** modulates SROB sensitivity to boundary transitions.  
- **Constraint:** must not exceed 0.8 in TS V1 to avoid over‑complex basin structures.

---

**SSG.4 – Dominance / singularity proximity**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:**  
  - 0 = no dominant singular structure  
  - 1 = strong singular dominance  
- **Effect:** controls singularity‑aware normalization and damping.  
- **Constraint:** when > 0.7, additional damping is applied to SROB and SmOB contributions.

---

**SSG.5 – Structural sparsity**

- **Type:** scalar, float  
- **Range:** [0, 1] (0 = dense, 1 = very sparse)  
- **Effect:** modulates how aggressively SOB and CnOB prune or compress structural features.  
- **Constraint:** must be consistent with observed SOB field occupancy (no large jumps).

---

**SSG.6–SSG.8 – Structural basis weights**

- **Type:** 3‑dim vector (or 3 scalars)  
- **Range:** [-1, 1] each  
- **Interpretation:** weights over 3 canonical structural bases (e.g., hierarchical, sequential, relational).  
- **Effect:** used by SOB/SROB/SmOB to align their fields with the active structural regime.  
- **Constraint:** L2 norm ≤ 1 (normalized).

---

## 4. SOB (Structural Observation Block) field specification

### 4.1 Role

SOB encodes **local structural features**: adjacency, degree, pattern regularity, and local curvature. It should be **low‑frequency and stable**, not a source of oscillation.

### 4.2 Field list and properties

**SOB.1 – Local degree / branching factor**

- **Type:** scalar, float  
- **Range:** [0, 1] (normalized from raw degree)  
- **Effect:** influences perceived structural complexity and local branching.  
- **Constraint:** smoothed over neighborhood; no per‑step jump > 0.2.

---

**SOB.2 – Local symmetry score**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** 0 = asymmetric, 1 = highly symmetric.  
- **Effect:** interacts with SSG.2 (anisotropy) to adjust structural expectations.  
- **Constraint:** must not oscillate rapidly; apply temporal smoothing.

---

**SOB.3 – Pattern regularity**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** periodicity / regularity of local structure.  
- **Effect:** used to detect high‑frequency oscillation regimes.  
- **Constraint:** when combined with SSG.1 and SSG.2, must not push Δ > 0.03 from SOB alone.

---

**SOB.4 – Local curvature sign**

- **Type:** scalar, float  
- **Range:** [-1, 1]  
- **Interpretation:**  
  - negative = concave / converging  
  - positive = convex / diverging  
- **Effect:** informs SROB about likely basin boundaries.  
- **Constraint:** derivative bounded; |Δ| ≤ 0.3 per step.

---

**SOB.5–SOB.8 – Structural feature channels**

- **Type:** 4 scalars, float  
- **Range:** [-1, 1]  
- **Examples:**  
  - SOB.5: clustering coefficient (normalized)  
  - SOB.6: path length density (normalized)  
  - SOB.7: local redundancy / overlap  
  - SOB.8: structural “noise” level  
- **Constraint:** combined L2 norm ≤ 1; SOB total contribution to Δ ≤ 0.03.

---

## 5. SROB (Structural Relational Observation Block) field specification

### 5.1 Role

SROB encodes **relations between structural regions**: basin boundaries, transitions, conflicts, and multi‑basin interactions. It is the main actor in **multi‑basin collision** scenarios.

### 5.2 Field list and properties

**SROB.1 – Basin membership confidence**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** confidence that the current state belongs to a specific basin.  
- **Effect:** used to stabilize behavior inside basins.  
- **Constraint:** must not flip rapidly between basins; apply hysteresis.

---

**SROB.2 – Boundary proximity**

- **Type:** scalar, float  
- **Range:** [0, 1] (0 = deep inside basin, 1 = at boundary)  
- **Effect:** increases damping and caution near boundaries.  
- **Constraint:** when > 0.8, SROB’s own contribution to Δ must be reduced.

---

**SROB.3 – Basin conflict index**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** degree of competition between multiple candidate basins.  
- **Effect:** triggers multi‑basin resolution logic.  
- **Constraint:** when > 0.6, additional normalization is applied to keep Δ ≤ 0.12.

---

**SROB.4 – Relational curvature**

- **Type:** scalar, float  
- **Range:** [-1, 1]  
- **Interpretation:** curvature of transitions between basins (smooth vs sharp).  
- **Effect:** modulates how aggressively transitions are taken.  
- **Constraint:** |Δ| ≤ 0.3 per step.

---

**SROB.5–SROB.8 – Relational channels**

- **Type:** 4 scalars, float  
- **Range:** [-1, 1]  
- **Examples:**  
  - SROB.5: cross‑basin similarity  
  - SROB.6: cross‑basin contradiction  
  - SROB.7: relational tension (conflicting constraints)  
  - SROB.8: relational coherence (agreement across structures)  
- **Constraint:** combined L2 norm ≤ 1; SROB total Δ contribution ≤ 0.04.

---

## 6. CnOB (Contextual Observation Block) field specification

### 6.1 Role

CnOB encodes **contextual state** over time: long‑run coherence, drift, and context pressure. It is the main actor in **long‑run drift** scenarios.

### 6.2 Field list and properties

**CnOB.1 – Context stability**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** 0 = rapidly changing context, 1 = stable context.  
- **Effect:** modulates how much past structure is retained.  
- **Constraint:** must be smoothed; no rapid oscillation.

---

**CnOB.2 – Drift magnitude**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** accumulated deviation from initial context.  
- **Effect:** triggers corrective mechanisms when high.  
- **Constraint:** when > 0.7, CnOB reduces its own influence to prevent runaway drift.

---

**CnOB.3 – Context pressure**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** how strongly context is constraining current structure.  
- **Effect:** biases structural choices towards context‑consistent options.  
- **Constraint:** must not dominate SSG/SOB; CnOB Δ ≤ 0.02.

---

**CnOB.4–CnOB.6 – Context channels**

- **Type:** 3 scalars, float  
- **Range:** [-1, 1]  
- **Examples:**  
  - CnOB.4: temporal coherence  
  - CnOB.5: topic coherence  
  - CnOB.6: task alignment  
- **Constraint:** combined L2 norm ≤ 1; slow temporal dynamics (low‑frequency).

---

## 7. SmOB (Semantic Observation Block) field specification

### 7.1 Role

SmOB encodes **semantic modulation**: meaning, style, and hybrid family switching. It is the main actor in **hybrid switching** scenarios.

### 7.2 Field list and properties

**SmOB.1 – Semantic family ID (soft)**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** soft assignment to a semantic family (e.g., narrative, analytic, procedural).  
- **Effect:** used with SSG basis weights to align structure with semantics.  
- **Constraint:** transitions must be smooth; no hard jumps.

---

**SmOB.2 – Style intensity**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** strength of stylistic modulation.  
- **Effect:** modulates how strongly semantics shape structure.  
- **Constraint:** when > 0.7, additional damping applied to avoid mode collapse.

---

**SmOB.3 – Semantic tension**

- **Type:** scalar, float  
- **Range:** [0, 1]  
- **Interpretation:** conflict between semantic expectations and structural state.  
- **Effect:** triggers adjustments in SOB/SROB to reconcile structure and meaning.  
- **Constraint:** when > 0.6, SmOB reduces its own Δ contribution.

---

**SmOB.4–SmOB.7 – Semantic channels**

- **Type:** 4 scalars, float  
- **Range:** [-1, 1]  
- **Examples:**  
  - SmOB.4: concreteness vs abstraction  
  - SmOB.5: narrative vs analytic  
  - SmOB.6: local vs global focus  
  - SmOB.7: literal vs figurative bias  
- **Constraint:** combined L2 norm ≤ 1; SmOB total Δ ≤ 0.03.

---

## 8. Interaction with SSG

All OB blocks must be **SSG‑aware**:

- SSG.1 (curvature) gates how aggressively SROB and SOB can change structure.  
- SSG.2 (anisotropy) biases SOB and SmOB fields towards specific axes.  
- SSG.3 (basin complexity) limits SROB’s relational complexity.  
- SSG.4 (singularity proximity) triggers damping in SROB and SmOB.  
- SSG.5 (sparsity) modulates SOB and CnOB pruning.  
- SSG.6–8 (basis weights) provide a shared structural coordinate system for all OBs.

Implementation rule:

> **Each OB field update must be a deterministic function of its local inputs AND the current SSG vector.**

This ensures global coherence and respects the stress‑tested stability.

---

## 9. Summary and implementation notes

- The **field definitions above are concrete enough** to implement directly.  
- All ranges, norms, and budgets are chosen to respect the **Δ‑norm ≤ 0.12** ceiling and **20–40 field** structural budget.  
- SSG provides the **global structural signature**; SOB, SROB, CnOB, and SmOB provide **local, relational, contextual, and semantic modulation** respectively.  
- The Round 2.5 stress test validates that this overall design is **robust, deterministic, stable, and laptop‑realizable**.

# **ts_tr_mapping_families.md**
### *Deterministic Mapping Families for TR Fields*
### *Version: Theory Foundation (Informative + Proposed Normative Expansion)*

---

# **0. What This Paper Does, Doesn’t Do, and Purpose**

## **0.1 What This Paper *Does***
This paper defines the **deterministic mapping families** for every TR output field:

- stance
- intent
- affect
- epistemic_shading
- tension
- politeness
- commitment
- reservation
- logical_structure
- epistemic_delta_h
- lineage_additions
- routing_fields

For each field, this paper provides:

- allowed inputs
- deterministic mapping family
- mapping formula (GitHub math)
- stability rules
- ordering rules
- SSR projection rules
- deterministic omission rules
- example mapping tables

This paper is the **mapping‑side companion** to:

- `ts_tr_semantic_routing_theory.md`
- `ts_tr_readset_update_proposal.md`
- `ts_tr_semantic_geometry.md` (composition order + minimal-input path)

Together, these papers make TR implementable.

---

## **0.2 What This Paper *Does Not* Do**
This paper does **not** define:

- semantic geometry (stance/affect/shading/politeness/tension geometry)
- invariant drift estimator $H_t$
- lineage append predicate
- routing_fields key set
- continuity‑curvature interaction theory
- semantic adjacency theory

Those are separate papers.

This paper defines **mapping families only**, using signals available under the current read‑set discipline.

---

## **0.3 Purpose of This Paper**

The purpose of this paper is to:

- provide deterministic mapping families for TR
- eliminate ambiguity in TR structural program
- support progressive lineup test construction
- prepare the ground for future 20.37 updates
- ensure replay determinism and SSR projection
- define stable, bounded, deterministic mapping rules

This paper is **normative for mapping**, but **informative for read‑set expansion**.

---

# **1. Mapping Family Structure**

Each TR field has a mapping family defined as:

1. **Allowed Inputs**
2. **Mapping Function**
3. **Stability Rules**
4. **Ordering Rules**
5. **SSR Projection Rules**
6. **Deterministic Omission Rules**
7. **Example Mapping Table**

Geometry-backed fields (stance, affect, shading, politeness, tension) **must** respect the composition order defined in `ts_tr_semantic_geometry.md` §9.1.

---

# **2. stance — Mapping Family**

### **2.1 Allowed Inputs**
- semantic meaning‑semantics
- idob_semantics
- qualifier lineage
- continuity signals
- semantic importance residues

### **2.2 Mapping Function**

$$
stance = f_s(M, I, C, A)
$$

### **2.3 Ordinal Values**

| stance | value |
|--------|--------|
| supportive | 0 |
| neutral | 1 |
| corrective | 2 |
| adversarial | 3 |
| exploratory | 4 |

### **2.4 Stability Rule**

If identity continuity is stable:

$$
stance_{t+1} = stance_t
$$

### **2.5 Deterministic Omission Rule**

If adjacency or continuity signals are missing:

```
stance = neutral   # value 1
```

### **2.6 Example Mapping Table**

| meaning cue | continuity | adjacency | stance |
|-------------|------------|-----------|--------|
| correction request | stable | neutral | corrective |
| disagreement | unstable | negative | adversarial |
| agreement | stable | positive | supportive |

---

# **3. intent — Mapping Family**

### **3.1 Allowed Inputs**
- semantic meaning‑semantics
- STPX cues
- semantic adjacency

### **3.2 Mapping Function**

$$
intent = f_i(M, S)
$$

### **3.3 Categories**

| intent | meaning |
|--------|---------|
| inform | declarative |
| request | interrogative |
| correct | corrective |
| clarify | ambiguous |
| commit | commitment |
| speculate | hypothetical |

### **3.4 Deterministic Omission Rule**

If STPX cues are missing:

```
intent = inform
```

---

# **4. affect — Mapping Family**

### **4.1 Allowed Inputs**
- semantic adjacency
- semantic importance residues

### **4.2 Mapping Function**

$$
affect = f_a(A)
$$

### **4.3 Ordinal Values**

| affect | value |
|--------|--------|
| negative | -1 |
| neutral | 0 |
| positive | +1 |

### **4.4 Deterministic Omission Rule**

If adjacency is missing:

```
affect = neutral   # 0
```

---

# **5. epistemic_shading — Mapping Family**

### **5.1 Allowed Inputs**
- semantic meaning‑semantics
- invariant drift
- commitments

### **5.2 Mapping Function**

$$
shading = f_e(\Delta H, C)
$$

### **5.3 Ordinal Values**

| shading | value |
|---------|--------|
| confident | 0 |
| neutral | 1 |
| uncertain | 2 |
| speculative | 3 |

### **5.4 Deterministic Omission Rule**

If $\Delta H$ is missing:

```
epistemic_shading = neutral   # 1
```

---

# **6. tension — Mapping Family**

### **6.1 Allowed Inputs**
- curvature
- semantic drift
- identity drift

### **6.2 Mapping Function**

$$
tension = f_t(curvature)
$$

### **6.3 Ordinal Values**

| tension | value |
|---------|--------|
| low | 0 |
| medium | 1 |
| high | 2 |

### **6.4 Deterministic Omission Rule**

If curvature is missing:

```
tension = low   # 0
```

---

# **7. politeness — Mapping Family**

### **7.1 Allowed Inputs**
- semantic adjacency
- qualifier lineage

### **7.2 Mapping Function**

$$
politeness = f_p(A)
$$

### **7.3 Ordinal Values**

| politeness | value |
|------------|--------|
| direct | 0 |
| neutral | 1 |
| polite | 2 |

### **7.4 Deterministic Omission Rule**

If adjacency is missing:

```
politeness = neutral   # 1
```

---

# **8. commitment — Mapping Family**

### **8.1 Allowed Inputs**
- commitments
- identity continuity

### **8.2 Mapping Function**

$$
commitment = f_c(C)
$$

### **8.3 Ordinal Values**

| commitment | value |
|------------|--------|
| weak | 0 |
| medium | 1 |
| strong | 2 |

### **8.4 Deterministic Omission Rule**

If commitments are missing:

```
commitment = weak   # 0
```

### **8.5 Stability Rule**

If freeze signatures are present:

$$
commitment_{t+1} = commitment_t
$$

---

# **9. reservation — Mapping Family**

### **9.1 Allowed Inputs**
- semantic adjacency
- epistemic_shading

### **9.2 Mapping Function**

$$
reservation = f_r(shading)
$$

### **9.3 Ordinal Values**

| reservation | value |
|-------------|--------|
| none | 0 |
| mild | 1 |
| strong | 2 |

### **9.4 Deterministic Omission Rule**

If shading is missing:

```
reservation = none   # 0
```

---

# **10. logical_structure — Mapping Family**

### **10.1 Allowed Inputs**
- STPX cues
- structural residue

### **10.2 Mapping Function**

$$
logical\\_structure = f_l(S)
$$

### **10.3 Categories**

| logical structure | meaning |
|-------------------|---------|
| conditional | if/then |
| causal | because |
| contrastive | but/however |
| additive | and/also |
| corrective | actually/in fact |

### **10.4 Deterministic Omission Rule**

If STPX cues are missing:

```
logical_structure = additive
```

---

# **11. epistemic_delta_h — Mapping Family**

### **11.1 Allowed Inputs**
- invariant drift
- semantic lineage

### **11.2 Mapping Function**

$$
\Delta H = H_{t+1} - H_t
$$

Where $H_t$ is defined in `ts_tr_invariant_drift_theory.md`.

### **11.3 Deterministic Omission Rule**

If either $H_t$ or $H_{t+1}$ is missing:

```
epistemic_delta_h = 0
```

---

# **12. lineage_additions — Mapping Family**

### **12.1 Allowed Inputs**
- semantic lineage
- referent lineage
- qualifier lineage

### **12.2 Mapping Function**

$$
lineage\\_additions = f_{la}(L)
$$

### **12.3 Deterministic Omission Rule**

If lineage signals are missing:

```
lineage_additions = []
```

### **12.4 Bounding Rule**

$$
|lineage\\_additions| \le k
$$

Where provisional default $k = 3$ (see `ts_tr_lineage_extension_theory.md`). Changing $k$ is a versioned event.

---

# **13. routing_fields — Mapping Family**

### **13.1 Allowed Inputs**
- routing_metadata
- semantic adjacency
- identity continuity
- curvature

### **13.2 Mapping Function**

$$
routing\\_fields = f_{rf}(metadata)
$$

### **13.3 Deterministic Omission Rule**

If metadata is missing:

```
routing_fields = {}
```

(Full key set and construction in `ts_tr_routing_fields_spec.md`.)

---

# **14. SSR Projection Rules (Global)**

All TR fields must satisfy:

$$
SSR(TR_v) = TR_v
$$

All fields must be stable, bounded, and deterministic. Lineage additions must be deterministic and bounded.

---

# **15. Deterministic Omission Rules (Global)**

If any diagnostic signal is missing:

- stance → neutral (1)
- intent → inform
- affect → neutral (0)
- shading → neutral (1)
- tension → low (0)
- politeness → neutral (1)
- commitment → weak (0)
- reservation → none (0)
- logical_structure → additive
- epistemic_delta_h → 0
- lineage_additions → []
- routing_fields → {}

This aligns with the minimal-input geometry path in `ts_tr_semantic_geometry.md` §11.

---

# **16. Versioned Free Parameters (Provisional Defaults)**

| Parameter | Provisional default | Owner paper |
|-----------|---------------------|-------------|
| stance omission | neutral (1) | this paper + geometry |
| intent omission | inform | this paper |
| affect / politeness / shading omission | neutral | this paper + geometry |
| tension omission | low (0) | this paper + geometry |
| lineage bound $k$ | 3 | lineage_extension_theory |
| $\tau_s$ (semantic drift threshold) | 2 | routing_fields_spec |
| severity_classifier | deterministic table TBD | routing_fields_spec |
| adjacency_modifier | $\{-1,0,+1\}$ | semantic_geometry |

Changing a provisional default is a **minor version** event and requires progressive-lineup fixture updates.

---

# **17. Closing Summary**

This paper defines the **deterministic mapping families** for all TR fields, with explicit omission defaults and versioned free parameters aligned to the geometry composition order and minimal-input path. It is the mapping backbone for the TR structural program and progressive lineup tests.

---

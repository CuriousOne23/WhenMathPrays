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

Those are separate papers:

- ts_tr_semantic_geometry.md  
- ts_tr_invariant_drift_theory.md  
- ts_tr_lineage_extension_theory.md  
- ts_tr_routing_fields_spec.md  
- ts_tr_continuity_and_curvature_interaction.md  
- ts_tr_semantic_adjacency_theory.md  

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

All math uses GitHub formatting:

Inline: `$x$`  
Block:

```
$$
x = y
$$
```

---

# **2. stance — Mapping Family**

### **2.1 Allowed Inputs**
- semantic meaning‑semantics  
- idob_semantics  
- qualifier lineage  
- continuity signals  
- semantic importance residues  

### **2.2 Mapping Function**

Stance is computed as:

```
stance = f_s(meaning, identity, continuity, adjacency)
```

Or in math:

$$
stance = f_s(M, I, C, A)
$$

Where:

- $M$ = meaning‑semantics  
- $I$ = identity‑conditioned meaning  
- $C$ = continuity signals  
- $A$ = semantic adjacency  

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
stance = neutral
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

Where:

- $M$ = meaning‑semantics  
- $S$ = STPX structural cues  

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

### **3.5 Example Mapping Table**

| STPX cue | meaning | intent |
|----------|---------|--------|
| question | request |
| correction marker | correct |
| declarative | inform |

---

# **4. affect — Mapping Family**

### **4.1 Allowed Inputs**
- semantic adjacency  
- semantic importance residues  

### **4.2 Mapping Function**

$$
affect = f_a(A)
$$

Where:

- $A$ = semantic adjacency  

### **4.3 Ordinal Values**

| affect | value |
|--------|--------|
| negative | -1 |
| neutral | 0 |
| positive | +1 |

### **4.4 Deterministic Omission Rule**

If adjacency is missing:

```
affect = neutral
```

### **4.5 Example Mapping Table**

| adjacency cue | affect |
|---------------|--------|
| praise | positive |
| insult | negative |
| neutral phrasing | neutral |

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

Where:

- $\Delta H$ = invariant drift  
- $C$ = commitment strength  

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
epistemic_shading = neutral
```

### **5.5 Example Mapping Table**

| ΔH | commitment | shading |
|----|------------|---------|
| 0 | strong | confident |
| 1 | weak | uncertain |
| 2 | weak | speculative |

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
tension = low
```

### **6.5 Example Mapping Table**

| curvature | tension |
|-----------|---------|
| stable | low |
| mild instability | medium |
| strong instability | high |

---

Understood, Jeff — delivering **ts_tr_mapping_families.md (Delivery 2 of 2)** with **clarity**, **coverage**, and **brevity as a subgoal**, exactly as you requested.

No agent.  
No delegation.  
Pure manual theory.

This continues directly from Delivery 1.

---

# ⭐ **ts_tr_mapping_families.md — DELIVERY 2 OF 2**  
*(Final half of the paper)*

---

# **7. politeness — Mapping Family**

### **7.1 Allowed Inputs**
- semantic adjacency  
- qualifier lineage  

### **7.2 Mapping Function**

Politeness is derived from adjacency cues:

$$
politeness = f_p(A)
$$

Where:

- $A$ = semantic adjacency (hedging, softening, directness)

### **7.3 Ordinal Values**

| politeness | value |
|------------|--------|
| direct | 0 |
| neutral | 1 |
| polite | 2 |

### **7.4 Deterministic Omission Rule**

If adjacency is missing:

```
politeness = neutral
```

### **7.5 Example Mapping Table**

| adjacency cue | politeness |
|---------------|------------|
| hedging | polite |
| blunt phrasing | direct |
| neutral phrasing | neutral |

---

# **8. commitment — Mapping Family**

### **8.1 Allowed Inputs**
- commitments  
- identity continuity  

### **8.2 Mapping Function**

Commitment strength is mapped as:

$$
commitment = f_c(C)
$$

Where:

- $C$ = commitment strength from IdOB

### **8.3 Ordinal Values**

| commitment | value |
|------------|--------|
| weak | 0 |
| medium | 1 |
| strong | 2 |

### **8.4 Deterministic Omission Rule**

If commitments are missing:

```
commitment = weak
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

Reservation increases with epistemic uncertainty:

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
reservation = none
```

### **9.5 Example Mapping Table**

| shading | reservation |
|---------|-------------|
| confident | none |
| uncertain | mild |
| speculative | strong |

---

# **10. logical_structure — Mapping Family**

### **10.1 Allowed Inputs**
- STPX cues  
- structural residue  

### **10.2 Mapping Function**

Logical structure is derived from STPX markers:

$$
logical\_structure = f_l(S)
$$

Where:

- $S$ = STPX structural cues

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

Epistemic delta is:

$$
\Delta H = H_{t+1} - H_t
$$

Where $H_t$ is the invariant state (defined in a separate paper).

### **11.3 Deterministic Omission Rule**

If either $H_t$ or $H_{t+1}$ is missing:

```
epistemic_delta_h = 0
```

### **11.4 Stability Rule**

If invariant drift is stable:

$$
\Delta H = 0
$$

---

# **12. lineage_additions — Mapping Family**

### **12.1 Allowed Inputs**
- semantic lineage  
- referent lineage  
- qualifier lineage  

### **12.2 Mapping Function**

Lineage additions occur when new referents or qualifiers appear:

$$
lineage\_additions = f_{la}(L)
$$

Where:

- $L$ = lineage signals

### **12.3 Deterministic Omission Rule**

If lineage signals are missing:

```
lineage_additions = []
```

### **12.4 Bounding Rule**

$$
|lineage\_additions| \le k
$$

Where $k$ is defined in `ts_tr_lineage_extension_theory.md`.

---

# **13. routing_fields — Mapping Family**

### **13.1 Allowed Inputs**
- routing_metadata  
- semantic adjacency  
- identity continuity  
- curvature  

### **13.2 Mapping Function**

Routing fields are constructed as:

$$
routing\_fields = f_{rf}(metadata)
$$

### **13.3 Deterministic Omission Rule**

If metadata is missing:

```
routing_fields = {}
```

### **13.4 Example Keys**  
*(Full key set defined in ts_tr_routing_fields_spec.md)*

- semantic_drift  
- identity_drift  
- structural_drift  
- commitment_instability  
- freeze_conflict  
- curvature_level  

---

# **14. SSR Projection Rules (Global)**

All TR fields must satisfy:

### **14.1 Stability Under Replay**

$$
SSR(TR_v) = TR_v
$$

### **14.2 No Ephemeral Fields**

All fields must be:

- stable  
- bounded  
- deterministic  

### **14.3 No Nondeterministic Lineage**

Lineage additions must be deterministic and bounded.

---

# **15. Deterministic Omission Rules (Global)**

If any diagnostic signal is missing:

- stance → neutral  
- intent → inform  
- affect → neutral  
- shading → neutral  
- tension → low  
- politeness → neutral  
- commitment → weak  
- reservation → none  
- logical_structure → additive  
- epistemic_delta_h → 0  
- lineage_additions → []  
- routing_fields → {}  

This ensures TR is fully deterministic under minimal inputs.

---

# **16. Closing Summary**

This paper defines the **deterministic mapping families** for all TR fields.

It provides:

- mapping functions  
- stability rules  
- ordering rules  
- SSR rules  
- deterministic omission rules  
- example mapping tables  

This paper **does not** define:

- semantic geometry  
- invariant drift estimator  
- lineage append predicate  
- routing_fields schema  
- adjacency theory  
- continuity‑curvature theory  

Those are separate papers.

This paper is the **mapping backbone** required for:

- TR structural program  
- progressive lineup tests  
- future 20.37 updates  

---


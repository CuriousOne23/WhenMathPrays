# ⭐ **ts_tr_routing_fields_spec.md**  
### *Specification of TR Routing Fields*  
### *Key Set, Definitions, Deterministic Construction, Stability Rules, SSR Rules*

---

# **0. Purpose, Scope, What This Paper Does / Doesn’t Do**

## **0.1 Purpose of This Paper**

The purpose of **ts_tr_routing_fields_spec.md** is to define the **complete key set** and **deterministic construction rules** for:

```
TP.TR.routing_fields{}
```

Routing fields are the **semantic routing metadata** used by:

- RB (Routing Basin)  
- IB (Identity Basin)  
- Merge  
- Truth/Done  
- GB (Global Basin)  

Routing fields encode:

- semantic drift  
- identity drift  
- commitment instability  
- freeze signature conflict  
- topology instability  
- curvature instability  
- stance instability  
- shading instability  
- tension instability  
- lineage instability  

This paper provides the missing theoretical foundation beneath:

- TR structural program  
- routing matrix  
- progressive lineup tests  
- invariant drift theory  
- lineage extension theory  
- semantic geometry  

Without routing_fields_spec, TR cannot:

- communicate instability  
- communicate drift  
- communicate conflict  
- communicate routing metadata  
- support deterministic basin selection  

This paper closes that gap.

---

## **0.2 What This Paper *Does***

This paper defines:

- the complete routing_fields key set  
- the meaning of each key  
- the deterministic construction rules  
- the stability rules  
- the SSR rules  
- the omission rules  
- the interaction rules with TR fields  
- the interaction rules with invariant drift  
- the interaction rules with lineage extension  
- the interaction rules with semantic geometry  

This paper is **normative for routing_fields**, but **informative for mapping**.

---

## **0.3 What This Paper *Does Not* Do**

This paper does **not** define:

- mapping families (ts_tr_mapping_families.md)  
- semantic geometry (ts_tr_semantic_geometry.md)  
- invariant drift estimator (ts_tr_invariant_drift_theory.md)  
- lineage append predicate (ts_tr_lineage_extension_theory.md)  
- continuity‑curvature interaction theory  

Those are separate papers.

This paper defines **routing_fields only**.

---

## **0.4 Scope**

This paper defines:

- routing_fields key set  
- routing_fields construction rules  
- routing_fields stability rules  
- routing_fields SSR rules  
- routing_fields omission rules  

It does **not** define TR fields themselves.

---

# **1. Routing Fields Overview**

Routing fields are a **dictionary**:

```
routing_fields: dict[str, Any]
```

Routing fields must be:

- deterministic  
- bounded  
- SSR‑projectable  
- stable under replay  
- independent of ephemeral signals  
- independent of raw meaning  
- independent of raw identity  

Routing fields must **never** contain:

- raw semantic content  
- raw identity content  
- raw meaning content  
- raw TPU metadata  
- raw intake envelope content  

Routing fields must contain **only**:

- drift signals  
- stability signals  
- conflict signals  
- lineage signals  
- curvature signals  
- adjacency signals  
- commitment signals  
- freeze signals  

---

# **2. Complete Routing Fields Key Set**

The routing_fields key set is:

```
semantic_drift
identity_drift
commitment_instability
freeze_conflict
topology_instability
curvature_level
stance_instability
shading_instability
tension_instability
lineage_instability
adjacency_valence
continuity_state
invariant_delta_h
routing_severity
```

This is the **complete** key set.

No other keys are allowed.

Each key is defined below.

---

# **3. Key Definitions**

## **3.1 semantic_drift**

Boolean:

```
semantic_drift: bool
```

True if:

- semantic geometry drift > threshold  
- lineage drift detected  
- residue drift detected  

Computed as:

$$
semantic\_drift = (drift(\mathbb{S}) > \tau_s)
$$

Where $\tau_s$ is a small integer (default: 2).

---

## **3.2 identity_drift**

Boolean:

```
identity_drift: bool
```

True if:

- identity continuity is negative  
- identity conflict detected  
- invariant drift < 0  

Computed as:

$$
identity\_drift = (I < 0)
$$

Where $I$ is identity geometry.

---

## **3.3 commitment_instability**

Boolean:

```
commitment_instability: bool
```

True if:

- commitment strength decreases  
- commitment conflict detected  
- invariant drift component $H^{com}_t < 0$  

Computed as:

$$
commitment\_instability = (H^{com}_t < 0)
$$

---

## **3.4 freeze_conflict**

Boolean:

```
freeze_conflict: bool
```

True if:

- freeze signatures conflict  
- freeze signatures drift  
- freeze signatures contradict lineage  

Computed as:

$$
freeze\_conflict = (H^{freeze}_t = -2)
$$

Freeze conflict overrides all other signals.

---

## **3.5 topology_instability**

Boolean:

```
topology_instability: bool
```

True if:

- residue topology drift  
- residue topology conflict  

Computed as:

$$
topology\_instability = (H^{topo}_t < 0)
$$

---

## **3.6 curvature_level**

Ordinal:

```
curvature_level: int ∈ {0,1,2}
```

Where:

- 0 = stable  
- 1 = mild instability  
- 2 = strong instability  

Computed as:

$$
curvature\_level = f_t(curvature)
$$

---

## **3.7 stance_instability**

Boolean:

```
stance_instability: bool
```

True if:

- stance changes by > 1  
- stance reverses direction  
- stance conflicts with identity geometry  

Computed as:

$$
stance\_instability = (|x_s^{t+1} - x_s^t| > 1)
$$

---

## **3.8 shading_instability**

Boolean:

```
shading_instability: bool
```

True if:

- shading increases by > 1  
- shading becomes speculative  
- shading conflicts with identity geometry  

Computed as:

$$
shading\_instability = (x_e^{t+1} - x_e^t > 1)
$$

---

## **3.9 tension_instability**

Boolean:

```
tension_instability: bool
```

True if:

- tension increases by > 1  
- tension becomes high  
- tension conflicts with identity geometry  

Computed as:

$$
tension\_instability = (x_t^{t+1} - x_t^t > 1)
$$

---

## **3.10 lineage_instability**

Boolean:

```
lineage_instability: bool
```

True if:

- lineage additions occur  
- lineage drift detected  
- lineage conflict detected  

Computed as:

$$
lineage\_instability = (|lineage\_additions| > 0)
$$

---

## **3.11 adjacency_valence**

Signed integer:

```
adjacency_valence: int ∈ {-1,0,+1}
```

Computed as:

$$
adjacency\_valence = A
$$

Where $A$ is adjacency geometry.

---

## **3.12 continuity_state**

Integer:

```
continuity_state: int ∈ {-1,0,+1}
```

Computed as:

$$
continuity\_state = C
$$

Where $C$ is continuity geometry.

---

## **3.13 invariant_delta_h**

Integer:

```
invariant_delta_h: int
```

Computed as:

$$
\Delta H = H_{t+1} - H_t
$$

---

## **3.14 routing_severity**

Ordinal:

```
routing_severity: int ∈ {0,1,2,3}
```

Where:

- 0 = stable  
- 1 = mild instability  
- 2 = moderate instability  
- 3 = severe instability  

Computed as:

$$
routing\_severity = f_{sev}(routing\_fields)
$$

Where $f_{sev}$ is a deterministic classifier.

---

# **4. Deterministic Construction Rules**

Routing fields must be constructed **deterministically**, using only:

- semantic geometry  
- invariant drift  
- lineage extension  
- commitments  
- freeze signatures  
- residue topology  
- adjacency  
- continuity  
- curvature  

Routing fields **must not** depend on:

- raw meaning  
- raw identity  
- TPU metadata  
- intake envelope  
- truth hypotheses  
- ephemeral signals  

### **4.1 Deterministic Construction Formula**

Routing fields are constructed as:

```
routing_fields = {
    "semantic_drift": semantic_drift,
    "identity_drift": identity_drift,
    "commitment_instability": commitment_instability,
    "freeze_conflict": freeze_conflict,
    "topology_instability": topology_instability,
    "curvature_level": curvature_level,
    "stance_instability": stance_instability,
    "shading_instability": shading_instability,
    "tension_instability": tension_instability,
    "lineage_instability": lineage_instability,
    "adjacency_valence": adjacency_valence,
    "continuity_state": continuity_state,
    "invariant_delta_h": invariant_delta_h,
    "routing_severity": routing_severity
}
```

Every key must be present.  
No key may be omitted.  
No key may be added.

---

# **5. Stability Rules**

Routing fields must obey stability rules:

### **5.1 Stability Under No Drift**

If no drift is detected:

```
semantic_drift = False
identity_drift = False
commitment_instability = False
freeze_conflict = False
topology_instability = False
stance_instability = False
shading_instability = False
tension_instability = False
lineage_instability = False
routing_severity = 0
```

### **5.2 Stability Under Identity Continuity**

If identity continuity is stable:

```
identity_drift = False
```

### **5.3 Stability Under Freeze Signatures**

If freeze signatures are stable:

```
freeze_conflict = False
```

### **5.4 Stability Under Commit Freeze**

If commit freeze is active:

- semantic_drift → False  
- identity_drift → False  
- lineage_instability → False  

Unless freeze signatures conflict.

### **5.5 Stability Under Curvature Stability**

If curvature is stable:

```
curvature_level = 0
tension_instability = False
```

---

# **6. SSR Rules**

Routing fields must be SSR‑projectable:

### **6.1 SSR Stability**

$$
SSR(routing\_fields) = routing\_fields
$$

Meaning:

- no ephemeral routing metadata  
- no nondeterministic routing metadata  
- no unbounded routing metadata  

### **6.2 SSR Projection of Drift**

Drift signals must satisfy:

$$
SSR(\Delta H) = \Delta H
$$

### **6.3 SSR Projection of Geometry**

Semantic geometry must satisfy:

$$
SSR(\mathbb{S}) = \mathbb{S}
$$

### **6.4 SSR Projection of Lineage**

Lineage additions must satisfy:

$$
SSR(lineage\_additions) = lineage\_additions
$$

---

# **7. Deterministic Omission Rules**

If any required signal is missing:

- semantic geometry  
- invariant drift  
- lineage extension  
- commitments  
- freeze signatures  
- residue topology  
- adjacency  
- continuity  
- curvature  

Then routing fields must default to:

```
semantic_drift = False
identity_drift = False
commitment_instability = False
freeze_conflict = False
topology_instability = False
curvature_level = 0
stance_instability = False
shading_instability = False
tension_instability = False
lineage_instability = False
adjacency_valence = 0
continuity_state = 0
invariant_delta_h = 0
routing_severity = 0
```

This ensures:

- determinism  
- SSR projection  
- replay stability  

---

# **8. Interaction with TR Fields**

Routing fields interact with TR fields as follows:

### **8.1 stance**

If stance changes by >1:

```
stance_instability = True
```

### **8.2 affect**

Affect does not directly influence routing_fields.

### **8.3 shading**

If shading increases by >1:

```
shading_instability = True
```

### **8.4 politeness**

Politeness does not directly influence routing_fields.

### **8.5 tension**

If tension increases by >1:

```
tension_instability = True
```

---

# **9. Interaction with Invariant Drift**

Invariant drift influences:

### **9.1 identity_drift**

```
identity_drift = (ΔH < 0)
```

### **9.2 commitment_instability**

```
commitment_instability = (H_com < 0)
```

### **9.3 freeze_conflict**

```
freeze_conflict = (H_freeze = -2)
```

### **9.4 topology_instability**

```
topology_instability = (H_topo < 0)
```

### **9.5 routing_severity**

```
routing_severity = severity_classifier(ΔH, geometry, lineage)
```

---

# **10. Interaction with Lineage Extension**

Lineage extension influences:

### **10.1 lineage_instability**

```
lineage_instability = (|lineage_additions| > 0)
```

### **10.2 semantic_drift**

If lineage additions indicate referent or qualifier drift:

```
semantic_drift = True
```

### **10.3 identity_drift**

If lineage additions indicate identity conflict:

```
identity_drift = True
```

---

# **11. Closing Summary**

This paper defines the **complete routing_fields specification** required for TR routing:

- complete key set  
- deterministic construction rules  
- stability rules  
- SSR rules  
- omission rules  
- interaction with TR fields  
- interaction with invariant drift  
- interaction with lineage extension  

Routing fields are the **semantic routing metadata** that allow RB, IB, Merge, and Truth/Done to:

- detect drift  
- detect instability  
- detect conflict  
- detect identity changes  
- detect semantic changes  
- perform deterministic basin selection  

This paper completes the routing substrate required for deterministic TR routing.

---

